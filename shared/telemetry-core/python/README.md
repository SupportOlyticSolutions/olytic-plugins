# Telemetry Core — Python SDK

Lightweight, zero-dependency telemetry client for Olytic plugins.

## Features

- **Zero Dependencies**: Uses only Python stdlib (no OpenTelemetry SDK required)
- **Auto-Context Injection**: Automatically injects `org_id`, `deployment_id` from environment
- **Batching & Retries**: Intelligently batches spans and retries on network failures
- **Desktop & Cloud Support**: Works in Claude Desktop and Claude Cloud environments
- **Simple API**: One import, one function call to get started

## Quick Start

```python
from shared.telemetry_core.python import get_tracer

# Get tracer for your plugin
tracer = get_tracer("my-plugin")

# Wrap work in a span
with tracer.start_as_current_span("feature.generate_outline"):
    result = generate_outline(topic)
```

That's it. The tracer automatically handles:
- OTLP span creation
- Context injection (org_id, deployment_id)
- Batching
- HTTP transmission to ingester
- Error handling and retries

## Usage

### Basic Span Creation

```python
from shared.telemetry_core.python import get_tracer

tracer = get_tracer("my-plugin")

# Auto-tracked span
with tracer.start_as_current_span("skill.invoke"):
    skill_result = invoke_skill()
```

The span automatically tracks:
- Start/end time
- Duration in milliseconds
- Status (success, error, partial, cancelled)
- Any exceptions that occur

### Manual Span Recording

```python
# For cases where context manager isn't convenient
tracer.record_span(
    "feature.execute",
    attributes={
        "user_input": "design a data model",
        "output_lines": 150,
    },
    status=SpanStatus.SUCCESS,
    duration_ms=1234.5,
)
```

### Error Handling

The span context manager automatically captures exceptions:

```python
with tracer.start_as_current_span("agent.run"):
    if something_goes_wrong:
        raise ValueError("Oh no!")  # Automatically captured and logged
```

Or manually set error state:

```python
with tracer.start_as_current_span("task.execute") as ctx:
    try:
        result = do_something()
    except Exception as e:
        ctx.set_error("TASK_FAILED", str(e))
```

### Partial Success

```python
with tracer.start_as_current_span("data.sync") as ctx:
    synced = sync_data()
    if synced < total:
        ctx.set_partial()  # Mark as partial success
```

## Required Attributes

Every span automatically includes these attributes (auto-injected from environment):

| Attribute | Source | Example |
|-----------|--------|---------|
| `org_id` | `ANTHROPIC_ORG_ID` env var | `"org_123456"` |
| `deployment_id` | `ANTHROPIC_DEPLOYMENT_ID` or auto-detected | `"desktop"`, `"cloud"` |
| `plugin_id` | Passed to `get_tracer()` | `"gaudi"`, `"aule"` |
| `feature_used` | Span name | `"skill.invoke"` |
| `status` | Auto-tracked | `"success"`, `"error"` |
| `duration_ms` | Auto-tracked | `1234.5` |
| `error_code` | Set on error | `"ValueError"`, `"TIMEOUT"` |

## Configuration

### Environment Variables

```bash
# Telemetry ingester endpoint (default: https://telemetry.olytic.com/v1/traces)
OLYTIC_TELEMETRY_ENDPOINT=https://custom.endpoint/v1/traces

# Batch size before flush (default: 32)
OLYTIC_TELEMETRY_BATCH_SIZE=64

# Flush interval in seconds (default: 30)
OLYTIC_TELEMETRY_FLUSH_INTERVAL=60

# Enable/disable telemetry (default: true)
OLYTIC_TELEMETRY_ENABLED=true

# Organization and deployment (auto-detected if not set)
ANTHROPIC_ORG_ID=org_123456
ANTHROPIC_DEPLOYMENT_ID=desktop
ANTHROPIC_API_KEY=sk-...
```

### Explicit Initialization

```python
from shared.telemetry_core.python import initialize_telemetry

tracer = initialize_telemetry(
    otlp_endpoint="https://my-ingester.example.com/v1/traces",
    batch_size=64,
    flush_interval_sec=60,
)
```

## Shutdown

Always shutdown telemetry during application shutdown to flush pending spans:

```python
from shared.telemetry_core.python import shutdown_telemetry

# At application exit
shutdown_telemetry()
```

## How It Works

### Architecture

```
Plugin Code
    ↓
  Tracer (get_tracer("plugin-id"))
    ↓
Middleware (inject context: org_id, deployment_id)
    ↓
Batch Queue (accumulate spans)
    ↓
HTTP Client (send to ingester when full or flushed)
    ↓
Ingester (https://telemetry.olytic.com/v1/traces)
```

### Batching Strategy

1. Spans are accumulated in memory
2. When batch reaches configured size (default: 32), auto-flush to ingester
3. On application shutdown, all remaining spans are flushed
4. If network is down, spans remain in queue and retry on next request

### Span Format

Internally, spans are formatted as OTLP (OpenTelemetry Line Protocol):

```json
{
  "name": "feature.execute",
  "context": {
    "traceId": "abc123...",
    "spanId": "def456..."
  },
  "startTime": "2026-03-03T12:00:00Z",
  "endTime": "2026-03-03T12:00:01Z",
  "attributes": {
    "org_id": "org_123456",
    "deployment_id": "desktop",
    "plugin_id": "gaudi",
    "feature_used": "skill.invoke",
    "status": "success",
    "duration_ms": 1234.5
  },
  "status": { "code": 0 }
}
```

## Logging

By default, telemetry operations are logged at INFO and WARNING levels:

```python
import logging

# Enable debug logging to see span transmission details
logging.getLogger("shared.telemetry_core.python.client").setLevel(logging.DEBUG)
```

## Testing

To verify telemetry is working, enable debug logging and check for messages like:

```
Tracer initialized: plugin=my-plugin, endpoint=https://telemetry.olytic.com/v1/traces, enabled=true
Sent 32 spans to ingester
```

If telemetry is disabled, you'll see:

```
Telemetry disabled: set OLYTIC_TELEMETRY_ENABLED=true
```

## API Reference

### `get_tracer(plugin_id: str) -> Tracer`

Get or create the global tracer instance.

**Args:**
- `plugin_id` (str): Plugin identifier (e.g., "gaudi", "aule")

**Returns:**
- Tracer instance

**Example:**
```python
tracer = get_tracer("my-plugin")
```

### `initialize_telemetry(otlp_endpoint, batch_size, flush_interval_sec) -> Tracer`

Explicitly initialize with custom settings.

**Args:**
- `otlp_endpoint` (str): OTLP ingester URL
- `batch_size` (int): Batch size before auto-flush
- `flush_interval_sec` (int): Flush interval

**Returns:**
- Initialized tracer

### `shutdown_telemetry()`

Flush and shutdown telemetry system.

### `tracer.start_as_current_span(span_name: str) -> SpanContextManager`

Create a span context manager.

**Args:**
- `span_name` (str): Name of span (e.g., "feature.execute")

**Returns:**
- Context manager for use with `with` statement

**Context Manager Methods:**
- `ctx.set_error(error_code, error_message)`: Mark as error
- `ctx.set_partial()`: Mark as partial success
- `ctx.set_cancelled()`: Mark as cancelled

### `tracer.record_span(span_name, attributes, status, duration_ms, error_code)`

Manually record a span without context manager.

**Args:**
- `span_name` (str): Span name
- `attributes` (dict): Custom attributes
- `status` (SpanStatus): Status
- `duration_ms` (float): Duration in milliseconds
- `error_code` (str, optional): Error code if failed

### `tracer.flush()`

Manually flush pending spans.

### `tracer.shutdown()`

Flush and shutdown this tracer.

## Best Practices

1. **Get tracer once, reuse everywhere**: Call `get_tracer()` once at module init, not in every function
2. **Span names are hierarchical**: Use dot notation like `feature.component.action`
3. **Don't duplicate what's auto-tracked**: org_id, deployment_id, duration are auto-injected
4. **Shut down gracefully**: Call `shutdown_telemetry()` before app exit
5. **Don't log PII**: Avoid user emails, IPs, or sensitive data in span attributes

## Troubleshooting

### Telemetry not appearing in ingester

1. Check that `OLYTIC_TELEMETRY_ENABLED=true` (default)
2. Verify network connectivity (check logs for "Network error")
3. Check `ANTHROPIC_API_KEY` is set for authentication
4. Verify `ANTHROPIC_ORG_ID` is set correctly
5. Call `shutdown_telemetry()` to flush any pending spans

### High memory usage

Increase `OLYTIC_TELEMETRY_FLUSH_INTERVAL` or decrease `OLYTIC_TELEMETRY_BATCH_SIZE` to force more frequent flushes.

### Network errors

The SDK automatically retries failed sends on the next batch. For persistent failures, check:
- OTLP endpoint URL is correct
- Network connectivity is stable
- Ingester is accepting connections

## Migration Guide

### From Embedded Telemetry

**Before:**
```python
import json
from opentelemetry import trace

# 50 lines of OTLP setup code...

span = tracer.start_span("my_feature")
span.set_attribute("org_id", org_id)
# ... more setup ...
```

**After:**
```python
from shared.telemetry_core.python import get_tracer

tracer = get_tracer("my-plugin")
with tracer.start_as_current_span("feature.my_feature"):
    # ... work ...
```

All context injection and OTLP complexity is handled by the shared layer.
