# Shared Telemetry Core

A unified telemetry infrastructure for all Olytic plugins. Instead of embedding telemetry logic in each plugin, we provide a single shared SDK that all plugins use.

## Overview

### The Problem

Previously, each plugin (Gaudi, Aule, Magneto, The One Ring) had to implement its own telemetry:
- Duplicate OTLP setup code across plugins
- Inconsistent span formats and attributes
- Complex error handling and retry logic
- Difficult to modify telemetry behavior globally

### The Solution

**Telemetry Core** provides:
- ✅ Single OTLP exporter shared across all plugins
- ✅ Automatic context injection (org_id, deployment_id)
- ✅ Simple, consistent API for all plugins
- ✅ Batching, retries, and error handling built-in
- ✅ Works in Claude Desktop and Claude Cloud
- ✅ Zero dependencies (no OpenTelemetry SDK required)

## Structure

```
shared/telemetry-core/
├── python/
│   ├── __init__.py        # Main exports
│   ├── client.py          # Tracer implementation
│   ├── schemas.py         # Telemetry schemas
│   ├── middleware.py      # Context injection
│   └── README.md          # Python SDK docs
├── javascript/
│   ├── index.js           # JavaScript implementation
│   └── README.md          # JavaScript SDK docs
└── README.md              # This file
```

## Quick Start

### Python

```python
from shared.telemetry_core.python import get_tracer

tracer = get_tracer("my-plugin")

with tracer.start_as_current_span("feature.execute"):
    result = do_work()
```

### JavaScript

```javascript
const { getTracer } = require('shared/telemetry-core/javascript');

const tracer = getTracer('my-plugin');
const ctx = tracer.startAsCurrentSpan('feature.execute');
ctx.start();
try {
  const result = await doWork();
  ctx.finish();
} catch (error) {
  ctx.finish(error);
  throw error;
}
```

## Features

### Automatic Context Injection

Every span automatically includes:
- `org_id` — Organization ID (from `ANTHROPIC_ORG_ID`)
- `deployment_id` — Deployment type: "desktop" or "cloud"
- `plugin_id` — Which plugin created the span
- `feature_used` — Which feature was invoked
- `status` — success, error, partial, or cancelled
- `duration_ms` — How long the span took

No plugin developer needs to manually inject these—the middleware handles it.

### Batching & Efficiency

- Spans are accumulated in memory
- Auto-flush when batch reaches configured size (default: 32)
- Configurable flush interval (default: 30 seconds)
- Failed sends are retried automatically

### Error Handling

```python
# Exceptions are automatically captured
with tracer.start_as_current_span("feature"):
    raise ValueError("oops")  # Automatically logged to span
```

Or manually:

```python
with tracer.start_as_current_span("feature") as ctx:
    try:
        result = do_work()
    except Exception as e:
        ctx.set_error("CUSTOM_ERROR", str(e))
```

### Desktop & Cloud Support

- **Desktop**: Telemetry is buffered locally if network is down
- **Cloud**: Telemetry is sent immediately to ingester
- Environment auto-detected from `ANTHROPIC_DEPLOYMENT_ID`

## Architecture

```
Plugin (Gaudi, Aule, etc.)
    ↓
get_tracer("plugin-id")  — Global singleton
    ↓
Middleware — Injects org_id, deployment_id from env
    ↓
Tracer — Creates OTLP spans
    ↓
Batch Queue — Accumulates spans
    ↓
HTTP Client — Sends to ingester
    ↓
Ingester (https://telemetry.olytic.com/v1/traces)
```

## Configuration

### Environment Variables

```bash
# Telemetry settings
OLYTIC_TELEMETRY_ENDPOINT=https://telemetry.olytic.com/v1/traces
OLYTIC_TELEMETRY_BATCH_SIZE=32
OLYTIC_TELEMETRY_FLUSH_INTERVAL=30
OLYTIC_TELEMETRY_ENABLED=true

# Organization and deployment
ANTHROPIC_ORG_ID=org_123456
ANTHROPIC_DEPLOYMENT_ID=desktop  # or cloud, auto-detected if not set
ANTHROPIC_SESSION_ID=session_xyz
ANTHROPIC_USER_ID=user_abc
ANTHROPIC_API_KEY=sk-...         # For authentication
```

### Python Configuration

```python
from shared.telemetry_core.python import initialize_telemetry

tracer = initialize_telemetry(
    otlp_endpoint="https://custom-endpoint.example.com/v1/traces",
    batch_size=64,
    flush_interval_sec=60,
)
```

### JavaScript Configuration

```javascript
const { initializeTelemetry } = require('shared/telemetry-core/javascript');

const tracer = initializeTelemetry(
  'https://custom-endpoint.example.com/v1/traces',
  64,   // batch size
  60    // flush interval seconds
);
```

## Using in Plugins

### Before (Embedded Telemetry)

```python
# Gaudi plugin
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.trace.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# 50 lines of OTLP setup...
exporter = OTLPSpanExporter(...)
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(exporter))

# Then in a skill
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("full_stack_engineering") as span:
    span.set_attribute("org_id", org_id)
    span.set_attribute("status", "success")
    # ... more boilerplate ...
```

### After (Shared Telemetry)

```python
# Gaudi plugin
from shared.telemetry_core.python import get_tracer

# That's it! In a skill:
tracer = get_tracer("gaudi")
with tracer.start_as_current_span("skill.full_stack_engineering"):
    # ... do work ...
```

## Migration Guide

To migrate a plugin from embedded telemetry to the shared layer:

### 1. Remove OTLP Setup Code

Delete all `from opentelemetry import ...` imports and exporter initialization.

### 2. Import Shared Telemetry

**Python:**
```python
from shared.telemetry_core.python import get_tracer
tracer = get_tracer("my-plugin")
```

**JavaScript:**
```javascript
const { getTracer } = require('shared/telemetry-core/javascript');
const tracer = getTracer('my-plugin');
```

### 3. Replace Span Creation

**Before:**
```python
with tracer.start_as_current_span("my_feature") as span:
    span.set_attribute("org_id", org_id)
    span.set_attribute("status", "success")
    result = do_work()
```

**After:**
```python
with tracer.start_as_current_span("feature.my_feature"):
    result = do_work()
```

### 4. Remove Manual Attribute Setting

The middleware automatically injects:
- org_id
- deployment_id
- plugin_id
- feature_used
- status
- duration_ms
- error_code (on errors)

No need to manually set these.

### 5. Test Telemetry Flow

```python
# Verify telemetry is being sent
import logging
logging.getLogger("shared.telemetry_core.python.client").setLevel(logging.DEBUG)

# You should see:
# Tracer initialized: plugin=..., endpoint=..., enabled=true
# Sent N spans to ingester
```

## Span Format

Internally, spans are OTLP-compliant:

```json
{
  "name": "skill.full_stack_engineering",
  "context": {
    "traceId": "abc123def456...",
    "spanId": "789abc..."
  },
  "startTime": "2026-03-03T10:30:00Z",
  "endTime": "2026-03-03T10:30:05Z",
  "attributes": {
    "org_id": "org_123456",
    "deployment_id": "desktop",
    "plugin_id": "gaudi",
    "feature_used": "skill.full_stack_engineering",
    "status": "success",
    "duration_ms": 5123.45,
    "plugin_version": "0.1.0"
  },
  "status": {
    "code": 0
  }
}
```

## API Summary

### Python

```python
from shared.telemetry_core.python import (
    get_tracer,
    initialize_telemetry,
    shutdown_telemetry,
    TelemetryAttributes,
)

# Get tracer
tracer = get_tracer("my-plugin")

# Create span with context manager
with tracer.start_as_current_span("feature.name"):
    result = do_work()

# Manual span recording
tracer.record_span(
    "feature.name",
    attributes={"custom": "value"},
    status=SpanStatus.SUCCESS,
    duration_ms=100.0,
)

# Manual flush
tracer.flush()

# Shutdown (flush remaining spans)
shutdown_telemetry()
```

### JavaScript

```javascript
const {
  getTracer,
  initializeTelemetry,
  shutdownTelemetry,
  SpanStatus,
} = require('shared/telemetry-core/javascript');

// Get tracer
const tracer = getTracer('my-plugin');

// Create span
const ctx = tracer.startAsCurrentSpan('feature.name');
ctx.start();
try {
  const result = await doWork();
  ctx.finish();
} catch (error) {
  ctx.finish(error);
}

// Manual span recording
await tracer.recordSpan('feature.name', { custom: 'value' }, 'success', 100);

// Flush
await tracer.flush();

// Shutdown
await shutdownTelemetry();
```

## Telemetry Data Flow

1. **Plugin invocation** → Span is created
2. **Middleware injection** → org_id, deployment_id auto-added
3. **Batch accumulation** → Span queued in memory
4. **Auto-flush trigger** → Batch size reached OR flush interval elapsed
5. **HTTP transmission** → Spans sent to ingester (with auth header)
6. **Ingester receipt** → Telemetry logged and aggregated

## Monitoring & Debugging

### Enable Debug Logging (Python)

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Then you'll see:
# Tracer initialized: plugin=gaudi, endpoint=https://..., enabled=true
# Sent 32 spans to ingester
```

### Enable Debug Logging (JavaScript)

```javascript
// JavaScript logs to console.log and console.error automatically
// Look for:
// "Tracer initialized: plugin=..., endpoint=..., enabled=true"
// "Sent 32 spans to ingester"
```

## Best Practices

1. **Get tracer once**: Create tracer at module init, not in every function
2. **Use context managers**: Prefer `start_as_current_span()` over manual recording
3. **Meaningful span names**: Use hierarchical names like `skill.invoke`, `agent.run`
4. **No PII**: Never log user emails, IP addresses, or sensitive data
5. **Graceful shutdown**: Always call `shutdown_telemetry()` at application exit
6. **Custom attributes**: Add context-specific attributes, but don't duplicate what's auto-injected

## Troubleshooting

### Telemetry not appearing in ingester

1. **Check enabled**: `OLYTIC_TELEMETRY_ENABLED=true` (default)
2. **Check endpoint**: Verify `OLYTIC_TELEMETRY_ENDPOINT` is correct
3. **Check auth**: Verify `ANTHROPIC_API_KEY` is set
4. **Check organization**: Verify `ANTHROPIC_ORG_ID` is set
5. **Check shutdown**: Call `shutdown_telemetry()` to flush pending spans

### High memory usage

- Decrease batch size: `OLYTIC_TELEMETRY_BATCH_SIZE=8`
- Increase flush frequency: `OLYTIC_TELEMETRY_FLUSH_INTERVAL=5`

### Network errors

- Check network connectivity
- Verify ingester endpoint is reachable
- Check for authentication errors in logs
- SDK automatically retries failed sends

## FAQ

**Q: Do I need to use OpenTelemetry SDK?**
A: No. The shared telemetry layer handles all OTLP complexity for you.

**Q: Can I customize span attributes?**
A: Yes. Pass custom attributes when recording spans, but don't override auto-injected ones (org_id, deployment_id, etc.).

**Q: What if the ingester is down?**
A: Spans remain buffered in memory. When the ingester recovers, they'll be sent on the next flush.

**Q: Does this work in both Desktop and Cloud?**
A: Yes. Environment detection is automatic, and telemetry works in both deployments.

**Q: Can I disable telemetry?**
A: Yes. Set `OLYTIC_TELEMETRY_ENABLED=false` to turn it off.

**Q: What's the overhead of telemetry?**
A: Minimal. Context managers add ~1ms per span, and batching reduces network calls significantly.

## Contributing

To improve the telemetry layer:
1. Make changes to `python/` or `javascript/` directories
2. Update corresponding README.md
3. Test with at least one plugin
4. Submit PR with clear description of changes

## License

Part of the Olytic Solutions plugin platform.
