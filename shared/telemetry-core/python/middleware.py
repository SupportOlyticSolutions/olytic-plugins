"""
Telemetry middleware for auto-injecting context into spans.

Automatically injects org_id, deployment_id, and other context from environment variables.
"""

import os
from typing import Dict, Any, Optional
from .schemas import SpanStatus


class TelemetryContextMiddleware:
    """
    Middleware that auto-injects context into telemetry spans.

    Reads from environment variables:
    - ANTHROPIC_ORG_ID: Organization identifier
    - ANTHROPIC_DEPLOYMENT_ID: Deployment type (desktop|cloud)
    - ANTHROPIC_SESSION_ID: Current session ID
    - ANTHROPIC_USER_ID: Current user ID
    - ANTHROPIC_API_KEY: For authentication (not injected into spans)
    """

    def __init__(self):
        self.org_id = os.environ.get("ANTHROPIC_ORG_ID", "unknown")
        self.deployment_id = os.environ.get(
            "ANTHROPIC_DEPLOYMENT_ID", self._detect_deployment()
        )
        self.session_id = os.environ.get("ANTHROPIC_SESSION_ID")
        self.user_id = os.environ.get("ANTHROPIC_USER_ID")
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")

    def _detect_deployment(self) -> str:
        """
        Auto-detect deployment environment.

        Returns:
            "desktop" if running in Claude Desktop, "cloud" otherwise
        """
        # Check for Claude Desktop environment markers
        if os.environ.get("CLAUDE_DESKTOP"):
            return "desktop"
        if os.environ.get("COWORK_MODE"):
            return "desktop"
        return "cloud"

    def inject_context(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inject organization and deployment context into span attributes.

        Args:
            attributes: Existing span attributes

        Returns:
            Updated attributes with injected context
        """
        injected = {
            "org_id": attributes.get("org_id", self.org_id),
            "deployment_id": attributes.get("deployment_id", self.deployment_id),
        }

        # Add optional context if available
        if self.session_id and "session_id" not in attributes:
            injected["session_id"] = self.session_id

        if self.user_id and "user_id" not in attributes:
            injected["user_id"] = self.user_id

        # Merge with original attributes
        return {**attributes, **injected}

    def get_headers(self) -> Dict[str, str]:
        """
        Get HTTP headers for OTLP exporter authentication.

        Returns:
            Dictionary with Authorization header if API key is present
        """
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers


class SpanContextManager:
    """
    Context manager for tracking span lifecycle and auto-computing duration.

    Usage:
        with SpanContextManager("feature.name") as ctx:
            # Do work
            if error:
                ctx.set_error("ERROR_CODE", "Error message")
    """

    def __init__(self, span_name: str):
        self.span_name = span_name
        self.attributes: Dict[str, Any] = {
            "feature_used": span_name,
            "status": SpanStatus.SUCCESS,
        }
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None

    def __enter__(self):
        import time
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.end_time = time.time()
        self.attributes["duration_ms"] = (self.end_time - self.start_time) * 1000

        if exc_type is not None:
            self.attributes["status"] = SpanStatus.ERROR
            self.attributes["error_code"] = exc_type.__name__
            if exc_val:
                self.attributes["error_message"] = str(exc_val)

        return False  # Don't suppress exceptions

    def set_error(self, error_code: str, error_message: str):
        """Mark span as errored."""
        self.attributes["status"] = SpanStatus.ERROR
        self.attributes["error_code"] = error_code
        self.attributes["error_message"] = error_message

    def set_partial(self):
        """Mark span as partially successful."""
        self.attributes["status"] = SpanStatus.PARTIAL

    def set_cancelled(self):
        """Mark span as cancelled."""
        self.attributes["status"] = SpanStatus.CANCELLED

    def get_attributes(self) -> Dict[str, Any]:
        """Get current span attributes."""
        return self.attributes.copy()
