# Telemetry Core — JavaScript SDK

Lightweight, zero-dependency telemetry client for Olytic plugins using Node.js.

## Features

- **Zero Dependencies**: Uses only Node.js built-ins (no OpenTelemetry SDK)
- **Auto-Context Injection**: Automatically injects `org_id`, `deployment_id` from environment
- **Batching & Retries**: Intelligently batches spans and retries on network failures
- **Desktop & Cloud Support**: Works in Claude Desktop and Claude Cloud
- **Simple API**: One import, minimal setup

## Quick Start

```javascript
const { getTracer } = require('shared/telemetry-core/javascript');

// Get tracer for your plugin
const tracer = getTracer('my-plugin');

// Record a span
const ctx = tracer.startAsCurrentSpan('feature.generate_outline');
ctx.start();
try {
  const result = await generateOutline(topic);
  ctx.finish();
  await tracer.recordSpan('feature.generate_outline', {}, undefined, ctx.attributes.duration_ms);
} catch (error) {
  ctx.finish(error);
  throw error;
}
```

## Usage

### Context Manager Pattern

```javascript
const { getTracer } = require('shared/telemetry-core/javascript');
const tracer = getTracer('my-plugin');

// Create context
const ctx = tracer.startAsCurrentSpan('skill.invoke');
ctx.start();

try {
  const result = await invokeSkill();
  ctx.finish();
  // Span is marked as success
} catch (error) {
  ctx.finish(error);  // Span is marked as error
  throw error;
}
```

### Manual Span Recording

```javascript
// For cases where context manager isn't convenient
await tracer.recordSpan(
  'feature.execute',
  {
    user_input: 'design a data model',
    output_lines: 150,
  },
  'success',
  1234.5
);
```

### Error Handling

```javascript
const ctx = tracer.startAsCurrentSpan('agent.run');
ctx.start();

try {
  await runAgent();
  ctx.finish();
} catch (error) {
  ctx.finish(error);  // Automatically captured
  throw error;
}
```

Or manually set error state:

```javascript
const ctx = tracer.startAsCurrentSpan('task.execute');
ctx.start();

try {
  const result = await doSomething();
  ctx.finish();
} catch (error) {
  ctx.setError('TASK_FAILED', error.message);
  ctx.finish();
}
```

## Required Attributes

Every span automatically includes:

| Attribute | Source | Example |
|-----------|--------|---------|
| `org_id` | `ANTHROPIC_ORG_ID` env var | `"org_123456"` |
| `deployment_id` | `ANTHROPIC_DEPLOYMENT_ID` or auto-detected | `"desktop"`, `"cloud"` |
| `plugin_id` | Passed to `getTracer()` | `"gaudi"`, `"aule"` |
| `feature_used` | Span name | `"skill.invoke"` |
| `status` | Auto-tracked | `"success"`, `"error"` |
| `duration_ms` | Auto-tracked | `1234.5` |
| `error_code` | Set on error | `"ValueError"`, `"TIMEOUT"` |

## Configuration

### Environment Variables

```bash
# Telemetry ingester endpoint
OLYTIC_TELEMETRY_ENDPOINT=https://telemetry.olytic.com/v1/traces

# Batch size before flush
OLYTIC_TELEMETRY_BATCH_SIZE=32

# Flush interval in seconds
OLYTIC_TELEMETRY_FLUSH_INTERVAL=30

# Enable/disable telemetry
OLYTIC_TELEMETRY_ENABLED=true

# Organization and deployment
ANTHROPIC_ORG_ID=org_123456
ANTHROPIC_DEPLOYMENT_ID=desktop
ANTHROPIC_API_KEY=sk-...
```

### Explicit Initialization

```javascript
const { initializeTelemetry } = require('shared/telemetry-core/javascript');

const tracer = initializeTelemetry(
  'https://my-ingester.example.com/v1/traces',
  64,  // batch size
  60   // flush interval seconds
);
```

## Shutdown

Always shutdown telemetry during application shutdown:

```javascript
const { shutdownTelemetry } = require('shared/telemetry-core/javascript');

// At application exit
process.on('exit', async () => {
  await shutdownTelemetry();
});
```

## How It Works

### Architecture

```
Plugin Code
    ↓
Tracer (getTracer('plugin-id'))
    ↓
Middleware (inject context: org_id, deployment_id)
    ↓
Batch Queue (accumulate spans)
    ↓
Fetch (send to ingester when full or flushed)
    ↓
Ingester (https://telemetry.olytic.com/v1/traces)
```

### Span Format

Internally, spans are formatted as OTLP:

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

## API Reference

### `getTracer(pluginId) -> Tracer`

Get or create the global tracer instance.

**Args:**
- `pluginId` (string): Plugin identifier

**Returns:**
- Tracer instance

```javascript
const tracer = getTracer('my-plugin');
```

### `initializeTelemetry(otlpEndpoint, batchSize, flushIntervalSec) -> Tracer`

Explicitly initialize with custom settings.

**Args:**
- `otlpEndpoint` (string): OTLP ingester URL
- `batchSize` (number): Batch size before auto-flush
- `flushIntervalSec` (number): Flush interval

**Returns:**
- Initialized tracer

### `shutdownTelemetry()`

Flush and shutdown telemetry system.

**Returns:**
- Promise that resolves when shutdown is complete

```javascript
await shutdownTelemetry();
```

### `tracer.startAsCurrentSpan(spanName) -> SpanContextManager`

Create a span context manager.

**Args:**
- `spanName` (string): Name of span

**Returns:**
- Context manager object

**Methods:**
- `ctx.start()`: Mark span start time
- `ctx.finish(error)`: Mark span end, optionally with error
- `ctx.setError(errorCode, errorMessage)`: Set error
- `ctx.setPartial()`: Mark as partial success
- `ctx.setCancelled()`: Mark as cancelled
- `ctx.getAttributes()`: Get current attributes

### `tracer.recordSpan(spanName, attributes, status, durationMs, errorCode)`

Manually record a span.

**Args:**
- `spanName` (string): Span name
- `attributes` (object): Custom attributes
- `status` (string): Status (success|error|partial|cancelled)
- `durationMs` (number): Duration in milliseconds
- `errorCode` (string, optional): Error code

**Returns:**
- Promise

```javascript
await tracer.recordSpan('feature.execute', { count: 42 }, 'success', 100);
```

### `tracer.flush()`

Manually flush pending spans.

**Returns:**
- Promise

### `tracer.shutdown()`

Flush and shutdown.

**Returns:**
- Promise

## Best Practices

1. **Get tracer once, reuse**: Call `getTracer()` once at module init
2. **Use context managers**: Prefer `startAsCurrentSpan()` over manual recording
3. **Async/await**: Always await `recordSpan()` and `flush()`
4. **Shutdown gracefully**: Call `shutdownTelemetry()` at application exit
5. **No PII**: Avoid user emails, IPs, or sensitive data in attributes
6. **Span naming**: Use hierarchical names like `feature.component.action`

## Troubleshooting

### Telemetry not appearing

1. Check `OLYTIC_TELEMETRY_ENABLED=true` (default)
2. Verify `await shutdownTelemetry()` is called before exit
3. Check `ANTHROPIC_API_KEY` is set
4. Verify `ANTHROPIC_ORG_ID` is correct
5. Check network connectivity

### Memory usage

Increase `OLYTIC_TELEMETRY_FLUSH_INTERVAL` or decrease `OLYTIC_TELEMETRY_BATCH_SIZE`.

## Migration Guide

### From Embedded Telemetry

**Before:**
```javascript
const tracer = require('opentelemetry-sdk-node').getTracer('my-plugin');
const span = tracer.startSpan('my_feature');
span.setAttribute('org_id', orgId);
// ... more setup ...
```

**After:**
```javascript
const { getTracer } = require('shared/telemetry-core/javascript');
const tracer = getTracer('my-plugin');
const ctx = tracer.startAsCurrentSpan('feature.my_feature');
ctx.start();
// ... work ...
ctx.finish();
```
