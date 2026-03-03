"""
Olytic Shared Telemetry Core — Python SDK

A lightweight, unified telemetry layer for all Olytic plugins.
Handles OTLP exporter setup, span creation, attribute injection, and batching.

Usage:
    from shared.telemetry_core.python import get_tracer

    tracer = get_tracer("my-plugin")
    with tracer.start_as_current_span("feature.generate_outline"):
        result = generate_outline(topic)
"""

from .client import get_tracer, initialize_telemetry, shutdown_telemetry
from .schemas import TelemetryAttributes, required_attributes

__all__ = [
    "get_tracer",
    "initialize_telemetry",
    "shutdown_telemetry",
    "TelemetryAttributes",
    "required_attributes",
]

__version__ = "0.1.0"
