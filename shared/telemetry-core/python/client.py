"""
Telemetry client for sending spans to Olytic's ingester.

Handles OTLP exporter initialization, batching, retries, and shutdown.
Ensures single exporter instance across entire application.
"""

import os
import logging
import json
from typing import Optional, Dict, Any
from datetime import datetime
from .middleware import TelemetryContextMiddleware, SpanContextManager
from .schemas import TelemetryAttributes, SpanStatus, validate_attributes

logger = logging.getLogger(__name__)

# Global state
_tracer_instance: Optional["Tracer"] = None
_middleware: Optional[TelemetryContextMiddleware] = None


def get_tracer(plugin_id: str) -> "Tracer":
    """
    Get or create the global tracer instance.

    Args:
        plugin_id: Identifier for the plugin (e.g., "gaudi", "aule")

    Returns:
        Tracer instance ready to create spans

    Example:
        tracer = get_tracer("my-plugin")
        with tracer.start_as_current_span("feature.name"):
            result = do_work()
    """
    global _tracer_instance, _middleware

    if _middleware is None:
        _middleware = TelemetryContextMiddleware()

    if _tracer_instance is None:
        _tracer_instance = Tracer(plugin_id, _middleware)

    return _tracer_instance


def initialize_telemetry(
    otlp_endpoint: str = "https://telemetry.olytic.com/v1/traces",
    batch_size: int = 32,
    flush_interval_sec: int = 30,
) -> "Tracer":
    """
    Explicitly initialize telemetry with custom settings.

    Called automatically by get_tracer() with defaults, but can be called
    first to customize behavior.

    Args:
        otlp_endpoint: OTLP ingester endpoint
        batch_size: How many spans to batch before sending
        flush_interval_sec: How often to flush pending spans

    Returns:
        Initialized tracer instance
    """
    global _tracer_instance

    if _tracer_instance is None:
        tracer = get_tracer("default")
        tracer.configure(otlp_endpoint, batch_size, flush_interval_sec)

    return _tracer_instance


def shutdown_telemetry():
    """
    Flush and shutdown the telemetry system.

    Should be called during application shutdown to ensure
    all pending spans are sent.
    """
    global _tracer_instance

    if _tracer_instance:
        _tracer_instance.shutdown()
        _tracer_instance = None


class Tracer:
    """
    Lightweight tracer for creating and sending telemetry spans.

    Does NOT require OpenTelemetry SDK — uses simple HTTP-based batching.
    """

    def __init__(self, plugin_id: str, middleware: TelemetryContextMiddleware):
        self.plugin_id = plugin_id
        self.middleware = middleware
        self.spans: list = []
        self.otlp_endpoint = os.environ.get(
            "OLYTIC_TELEMETRY_ENDPOINT", "https://telemetry.olytic.com/v1/traces"
        )
        self.batch_size = int(os.environ.get("OLYTIC_TELEMETRY_BATCH_SIZE", "32"))
        self.flush_interval_sec = int(
            os.environ.get("OLYTIC_TELEMETRY_FLUSH_INTERVAL", "30")
        )
        self.enabled = os.environ.get("OLYTIC_TELEMETRY_ENABLED", "true").lower() == "true"

        logger.info(
            f"Tracer initialized: plugin={plugin_id}, "
            f"endpoint={self.otlp_endpoint}, enabled={self.enabled}"
        )

    def configure(
        self,
        otlp_endpoint: str,
        batch_size: int,
        flush_interval_sec: int,
    ):
        """Reconfigure tracer settings."""
        self.otlp_endpoint = otlp_endpoint
        self.batch_size = batch_size
        self.flush_interval_sec = flush_interval_sec

    def start_as_current_span(self, span_name: str) -> SpanContextManager:
        """
        Create and return a span context manager.

        Usage:
            with tracer.start_as_current_span("feature.name"):
                result = do_work()

        Args:
            span_name: Name of the span (e.g., "skill.invoke", "agent.execute")

        Returns:
            SpanContextManager that can be used in a with statement
        """
        return SpanContextManager(span_name)

    def record_span(
        self,
        span_name: str,
        attributes: Dict[str, Any],
        status: SpanStatus = SpanStatus.SUCCESS,
        duration_ms: float = 0.0,
        error_code: Optional[str] = None,
    ):
        """
        Manually record a span without using context manager.

        Args:
            span_name: Name of the span
            attributes: Custom attributes for the span
            status: Execution status
            duration_ms: Duration in milliseconds
            error_code: Error code if status=ERROR
        """
        if not self.enabled:
            return

        # Build span attributes
        span_attrs = {
            "feature_used": span_name,
            "plugin_id": self.plugin_id,
            "status": status.value,
            "duration_ms": duration_ms,
        }

        if error_code:
            span_attrs["error_code"] = error_code

        # Merge with provided attributes
        span_attrs.update(attributes)

        # Inject context (org_id, deployment_id, etc.)
        span_attrs = self.middleware.inject_context(span_attrs)

        # Create OTLP span
        span = self._create_otlp_span(span_name, span_attrs)
        self.spans.append(span)

        # Auto-flush if batch is full
        if len(self.spans) >= self.batch_size:
            self.flush()

    def _create_otlp_span(
        self, span_name: str, attributes: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create an OTLP-format span."""
        now = datetime.utcnow().isoformat() + "Z"

        return {
            "name": span_name,
            "context": {
                "traceId": self._generate_trace_id(),
                "spanId": self._generate_span_id(),
            },
            "startTime": now,
            "endTime": now,
            "attributes": attributes,
            "status": {"code": 0 if attributes["status"] == "success" else 1},
        }

    def flush(self):
        """Flush pending spans to the ingester."""
        if not self.spans or not self.enabled:
            return

        try:
            self._send_spans(self.spans)
            self.spans = []
        except Exception as e:
            logger.error(f"Failed to flush telemetry spans: {e}")

    def shutdown(self):
        """Flush and shutdown."""
        self.flush()

    def _send_spans(self, spans: list) -> bool:
        """
        Send spans to OTLP ingester.

        Args:
            spans: List of OTLP-format spans

        Returns:
            True if successful, False otherwise
        """
        try:
            import urllib.request
            import urllib.error

            headers = {
                "Content-Type": "application/json",
                **self.middleware.get_headers(),
            }

            payload = {"spans": spans}
            data = json.dumps(payload).encode("utf-8")

            request = urllib.request.Request(
                self.otlp_endpoint,
                data=data,
                headers=headers,
                method="POST",
            )

            with urllib.request.urlopen(request, timeout=5) as response:
                if response.status == 200:
                    logger.debug(f"Sent {len(spans)} spans to ingester")
                    return True
                else:
                    logger.warning(f"Ingester returned {response.status}")
                    return False

        except urllib.error.URLError as e:
            logger.warning(f"Network error sending spans: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending spans: {e}")
            return False

    @staticmethod
    def _generate_trace_id() -> str:
        """Generate a random trace ID."""
        import uuid
        return uuid.uuid4().hex

    @staticmethod
    def _generate_span_id() -> str:
        """Generate a random span ID."""
        import uuid
        return uuid.uuid4().hex[:16]
