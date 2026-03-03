"""
Telemetry attribute schemas and validation.

Defines required attributes for all spans and provides helper functions
to ensure data consistency across all plugins.
"""

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional
from enum import Enum


class SpanStatus(str, Enum):
    """Standard status values for spans."""
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"
    CANCELLED = "cancelled"


@dataclass
class TelemetryAttributes:
    """
    Required attributes for all telemetry spans.

    These are auto-injected by the middleware and should be set on every span.
    """
    # Organizational context
    org_id: str
    deployment_id: str

    # Plugin context
    plugin_id: str
    plugin_version: str = "0.1.0"

    # Feature tracking
    feature_used: str  # e.g., "gaudi.full_stack_engineering", "aule.plugin_generation"

    # Execution tracking
    status: SpanStatus = SpanStatus.SUCCESS
    duration_ms: float = 0.0

    # Error tracking
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    # Additional context
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, filtering None values."""
        result = asdict(self)
        return {k: v for k, v in result.items() if v is not None}


def required_attributes() -> Dict[str, str]:
    """
    Return the set of required attributes that must be present on every span.

    These are:
    - org_id: Organization identifier
    - deployment_id: Deployment identifier (desktop vs. cloud)
    - plugin_id: Plugin name
    - feature_used: Feature/component path
    - status: Execution status
    - duration_ms: How long the operation took
    - error_code: Error code (if applicable)
    """
    return {
        "org_id": "Organization identifier",
        "deployment_id": "Deployment identifier (desktop|cloud)",
        "plugin_id": "Plugin name (gaudi|aule|magneto|the-one-ring)",
        "feature_used": "Feature component path",
        "status": "Execution status (success|error|partial|cancelled)",
        "duration_ms": "Duration in milliseconds",
        "error_code": "Error code if status=error",
    }


def validate_attributes(attrs: Dict[str, Any]) -> bool:
    """
    Validate that all required attributes are present.

    Args:
        attrs: Dictionary of span attributes

    Returns:
        True if valid, raises ValueError otherwise
    """
    required = ["org_id", "deployment_id", "plugin_id", "feature_used", "status"]
    missing = [field for field in required if field not in attrs]

    if missing:
        raise ValueError(f"Missing required telemetry attributes: {missing}")

    return True
