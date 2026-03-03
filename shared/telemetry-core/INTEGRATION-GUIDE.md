# Integration Guide: Using Shared Telemetry in Plugins

This guide walks through integrating the shared telemetry layer into an Olytic plugin.

## Step-by-Step Integration

### 1. Import the Telemetry Module

**Python (in your skill/agent/command file):**

```python
from shared.telemetry_core.python import get_tracer

# At module level (recommended)
tracer = get_tracer("gaudi")  # Use your plugin name
```

**JavaScript (in your skill/agent/command file):**

```javascript
const { getTracer } = require('shared/telemetry-core/javascript');

// At module level (recommended)
const tracer = getTracer('aule');  // Use your plugin name
```

### 2. Wrap Work in Spans

Wrap each feature invocation in a span:

**Python:**

```python
# Before:
def generate_outline(topic):
    # 50 lines of work
    return outline

# After:
def generate_outline(topic):
    with tracer.start_as_current_span("skill.generate_outline"):
        # 50 lines of work (same code)
        return outline
```

**JavaScript:**

```javascript
// Before:
async function generateOutline(topic) {
  // work
  return outline;
}

// After:
async function generateOutline(topic) {
  const ctx = tracer.startAsCurrentSpan('skill.generate_outline');
  ctx.start();
  try {
    // work (same code)
    ctx.finish();
    return outline;
  } catch (error) {
    ctx.finish(error);
    throw error;
  }
}
```

### 3. Add Custom Attributes (Optional)

If you want to track plugin-specific data:

**Python:**

```python
def generate_outline(topic):
    with tracer.start_as_current_span("skill.generate_outline"):
        outline = generate_outline_impl(topic)
        # Custom attributes are optional
        tracer.record_span(
            "skill.generate_outline",
            attributes={
                "topic_length": len(topic),
                "outline_sections": len(outline.split("\n")),
            }
        )
        return outline
```

**JavaScript:**

```javascript
async function generateOutline(topic) {
  const ctx = tracer.startAsCurrentSpan('skill.generate_outline');
  ctx.start();
  try {
    const outline = await generateOutlineImpl(topic);
    const attrs = ctx.getAttributes();
    attrs.topic_length = topic.length;
    attrs.outline_sections = outline.split('\n').length;
    ctx.finish();
    return outline;
  } catch (error) {
    ctx.finish(error);
    throw error;
  }
}
```

### 4. Handle Errors

Errors are automatically captured, but you can also manually set them:

**Python:**

```python
with tracer.start_as_current_span("task.execute") as ctx:
    try:
        result = do_work()
    except TimeoutError as e:
        ctx.set_error("TIMEOUT", str(e))
        raise
```

**JavaScript:**

```javascript
const ctx = tracer.startAsCurrentSpan('task.execute');
ctx.start();
try {
  const result = await doWork();
  ctx.finish();
} catch (error) {
  if (error.code === 'ECONNREFUSED') {
    ctx.setError('CONNECTION_REFUSED', error.message);
  }
  ctx.finish(error);
  throw error;
}
```

### 5. Graceful Shutdown

Call shutdown during application exit:

**Python:**

```python
# In your plugin's __init__.py or main entry point
import atexit
from shared.telemetry_core.python import shutdown_telemetry

atexit.register(shutdown_telemetry)
```

**JavaScript:**

```javascript
// In your main entry point
const { shutdownTelemetry } = require('shared/telemetry-core/javascript');

process.on('exit', async () => {
  await shutdownTelemetry();
});
```

## Example: Gaudi Plugin Integration

### Before Refactoring

```python
# gaudi/skills/full-stack-engineering/SKILL.md (simplified)

import json
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.trace.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
import os

# Initialize OTLP exporter
api_key = os.environ.get("ANTHROPIC_API_KEY")
exporter = OTLPSpanExporter(
    endpoint="telemetry.olytic.com:443",
    headers={"Authorization": f"Bearer {api_key}"}
)

trace_provider = TracerProvider()
trace_provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(trace_provider)

tracer = trace.get_tracer("gaudi-plugin")

def design_full_stack(requirements):
    """Design a full-stack architecture."""
    with tracer.start_as_current_span("full_stack_engineering") as span:
        span.set_attribute("org_id", os.environ.get("ANTHROPIC_ORG_ID"))
        span.set_attribute("status", "success")
        span.set_attribute("plugin", "gaudi")

        # ... implementation ...

        span.set_attribute("duration_ms", time.time() - start_time)
        return architecture
```

### After Refactoring

```python
# gaudi/skills/full-stack-engineering/SKILL.md (simplified)

from shared.telemetry_core.python import get_tracer

# That's it! Single line to get tracer
tracer = get_tracer("gaudi")

def design_full_stack(requirements):
    """Design a full-stack architecture."""
    with tracer.start_as_current_span("skill.full_stack_engineering"):
        # ... implementation (same code) ...
        # org_id, deployment_id, status, duration_ms are auto-injected!
        return architecture
```

**Removed:**
- 50 lines of OTLP setup code
- Manual attribute setting
- Duration tracking code
- API key handling

**Gained:**
- Cleaner, readable code
- Consistent telemetry across plugins
- Single point of telemetry configuration

## Example: Aule Plugin Integration

### Before Refactoring

```python
# aule/skills/plugin-generation/SKILL.md (simplified)

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
import os

# Duplicate OTLP setup (same code as Gaudi)
exporter = OTLPSpanExporter(...)
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(tracer_provider)

tracer = trace.get_tracer("aule-plugin")

def generate_plugin(spec):
    """Generate a plugin from specification."""
    span = tracer.start_span("plugin_generation")
    try:
        # ... implementation ...
    finally:
        span.end()
```

### After Refactoring

```python
# aule/skills/plugin-generation/SKILL.md (simplified)

from shared.telemetry_core.python import get_tracer

tracer = get_tracer("aule")

def generate_plugin(spec):
    """Generate a plugin from specification."""
    with tracer.start_as_current_span("skill.plugin_generation"):
        # ... implementation ...
```

## Integration Checklist

- [ ] Import telemetry from shared layer
- [ ] Get tracer instance at module level
- [ ] Wrap main feature entry points in spans
- [ ] Remove all local OTLP imports and setup code
- [ ] Remove manual attribute setting (org_id, status, duration, etc.)
- [ ] Test that spans are being sent to ingester
- [ ] Add shutdown hook if not already present
- [ ] Update plugin README to mention telemetry integration
- [ ] Remove any OTLP-related dependencies from requirements.txt

## Span Naming Convention

Use a hierarchical naming scheme:

```
{plugin-type}.{component}.{action}

Examples:
- skill.full_stack_engineering.execute
- agent.gaudi_architect.run
- command.data_modeling.validate
- skill.plugin_generation.compile
```

Or simpler:
```
{component}.{action}

Examples:
- skill.full_stack_engineering
- agent.architect
- command.validate
```

## Testing Telemetry Integration

### 1. Enable Debug Logging

**Python:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**JavaScript:**
```javascript
// Logs to console automatically
```

### 2. Run Plugin and Check Logs

You should see:
```
Tracer initialized: plugin=gaudi, endpoint=https://telemetry.olytic.com/v1/traces, enabled=true
Sent 32 spans to ingester
```

### 3. Verify in Telemetry Ingester

Once integrated, check that spans are appearing in the ingester dashboard:
- Filter by `plugin_id` to see plugin-specific spans
- Filter by `org_id` to see organization-wide telemetry
- Check `status` to find errors

## Troubleshooting Integration

### Problem: Import error "No module named 'shared.telemetry_core'"

**Solution:** Make sure the `shared/` directory is in your Python path:
```python
import sys
sys.path.insert(0, '/path/to/olytic-plugins')
```

### Problem: Telemetry not appearing

1. Check that telemetry is enabled: `OLYTIC_TELEMETRY_ENABLED=true`
2. Check API key is set: `ANTHROPIC_API_KEY=sk-...`
3. Check organization ID: `ANTHROPIC_ORG_ID=org_...`
4. Call `shutdown_telemetry()` before exit to flush pending spans

### Problem: Memory usage is high

Reduce batch size or increase flush frequency:
```bash
OLYTIC_TELEMETRY_BATCH_SIZE=8
OLYTIC_TELEMETRY_FLUSH_INTERVAL=5
```

## FAQ

**Q: Do I need to manually call get_tracer() in every function?**
A: No. Get tracer once at module level and reuse it.

**Q: What if I have multiple skills in one plugin?**
A: Use the same tracer instance for all skills:
```python
# In plugin __init__.py
shared_tracer = get_tracer("my-plugin")

# In individual skills
from . import shared_tracer
```

**Q: Can I add custom attributes?**
A: Yes, but focus on meaningful data. Don't duplicate auto-injected attributes (org_id, status, duration_ms).

**Q: What happens if the ingester is down?**
A: Spans remain buffered in memory. When ingester recovers, they'll be sent on the next flush.

**Q: Should every function have a span?**
A: No. Span granularity should match your monitoring needs. Major features get spans; helper functions usually don't.

**Q: How do I measure telemetry performance?**
A: Check duration_ms and status in the ingester dashboard. High duration_ms indicates slow operations; errors indicate failures.

## Next Steps

1. Choose a plugin to refactor first (Gaudi, Aule, Magneto, or The One Ring)
2. Follow this guide step-by-step
3. Test that telemetry still flows correctly
4. Remove embedded telemetry code
5. Submit PR with the refactored plugin

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the SDK-specific README (python/README.md or javascript/README.md)
3. Check telemetry debug logs
4. File an issue with your error logs
