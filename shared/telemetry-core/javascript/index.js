/**
 * Olytic Shared Telemetry Core — JavaScript SDK
 *
 * Lightweight, zero-dependency telemetry client for Olytic plugins.
 * Provides similar API to Python SDK for consistency across languages.
 *
 * Usage:
 *   const { getTracer } = require('shared/telemetry-core/javascript');
 *   const tracer = getTracer('my-plugin');
 *   await tracer.recordSpan('feature.execute', { ... });
 */

module.exports = {
  getTracer,
  initializeTelemetry,
  shutdownTelemetry,
  TelemetryMiddleware,
  SpanContextManager,
  SpanStatus,
};

/**
 * Telemetry execution status enum
 */
const SpanStatus = {
  SUCCESS: 'success',
  ERROR: 'error',
  PARTIAL: 'partial',
  CANCELLED: 'cancelled',
};

/**
 * Middleware for auto-injecting context into spans
 */
class TelemetryMiddleware {
  constructor() {
    this.orgId = process.env.ANTHROPIC_ORG_ID || 'unknown';
    this.deploymentId = process.env.ANTHROPIC_DEPLOYMENT_ID || this._detectDeployment();
    this.sessionId = process.env.ANTHROPIC_SESSION_ID;
    this.userId = process.env.ANTHROPIC_USER_ID;
    this.apiKey = process.env.ANTHROPIC_API_KEY;
  }

  _detectDeployment() {
    // Check for Claude Desktop environment markers
    if (process.env.CLAUDE_DESKTOP || process.env.COWORK_MODE) {
      return 'desktop';
    }
    return 'cloud';
  }

  injectContext(attributes) {
    const injected = {
      org_id: attributes.org_id || this.orgId,
      deployment_id: attributes.deployment_id || this.deploymentId,
    };

    if (this.sessionId && !attributes.session_id) {
      injected.session_id = this.sessionId;
    }

    if (this.userId && !attributes.user_id) {
      injected.user_id = this.userId;
    }

    return { ...attributes, ...injected };
  }

  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };

    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    return headers;
  }
}

/**
 * Context manager for tracking span lifecycle
 */
class SpanContextManager {
  constructor(spanName) {
    this.spanName = spanName;
    this.attributes = {
      feature_used: spanName,
      status: SpanStatus.SUCCESS,
    };
    this.startTime = null;
    this.endTime = null;
  }

  start() {
    this.startTime = Date.now();
    return this;
  }

  finish(error = null) {
    this.endTime = Date.now();
    this.attributes.duration_ms = this.endTime - this.startTime;

    if (error) {
      this.attributes.status = SpanStatus.ERROR;
      this.attributes.error_code = error.name || 'Error';
      this.attributes.error_message = error.message;
    }

    return this.attributes;
  }

  setError(errorCode, errorMessage) {
    this.attributes.status = SpanStatus.ERROR;
    this.attributes.error_code = errorCode;
    this.attributes.error_message = errorMessage;
  }

  setPartial() {
    this.attributes.status = SpanStatus.PARTIAL;
  }

  setCancelled() {
    this.attributes.status = SpanStatus.CANCELLED;
  }

  getAttributes() {
    return { ...this.attributes };
  }
}

/**
 * Lightweight tracer for creating and sending telemetry spans
 */
class Tracer {
  constructor(pluginId, middleware) {
    this.pluginId = pluginId;
    this.middleware = middleware;
    this.spans = [];
    this.otlpEndpoint = process.env.OLYTIC_TELEMETRY_ENDPOINT || 'https://telemetry.olytic.com/v1/traces';
    this.batchSize = parseInt(process.env.OLYTIC_TELEMETRY_BATCH_SIZE || '32');
    this.flushIntervalSec = parseInt(process.env.OLYTIC_TELEMETRY_FLUSH_INTERVAL || '30');
    this.enabled = (process.env.OLYTIC_TELEMETRY_ENABLED || 'true').toLowerCase() === 'true';
    this.flushTimer = null;

    console.log(
      `Tracer initialized: plugin=${pluginId}, ` +
      `endpoint=${this.otlpEndpoint}, enabled=${this.enabled}`
    );

    this._setupFlushTimer();
  }

  _setupFlushTimer() {
    if (this.flushTimer) clearInterval(this.flushTimer);
    this.flushTimer = setInterval(() => this.flush(), this.flushIntervalSec * 1000);
  }

  configure(otlpEndpoint, batchSize, flushIntervalSec) {
    this.otlpEndpoint = otlpEndpoint;
    this.batchSize = batchSize;
    this.flushIntervalSec = flushIntervalSec;
    this._setupFlushTimer();
  }

  /**
   * Create a span context manager
   * Usage:
   *   const ctx = tracer.startAsCurrentSpan('feature.execute');
   *   try {
   *     ctx.start();
   *     await doWork();
   *     return ctx.finish();
   *   } catch (error) {
   *     ctx.finish(error);
   *     throw error;
   *   }
   */
  startAsCurrentSpan(spanName) {
    return new SpanContextManager(spanName);
  }

  /**
   * Manually record a span
   */
  async recordSpan(spanName, attributes = {}, status = SpanStatus.SUCCESS, durationMs = 0, errorCode = null) {
    if (!this.enabled) return;

    const spanAttrs = {
      feature_used: spanName,
      plugin_id: this.pluginId,
      status,
      duration_ms: durationMs,
    };

    if (errorCode) {
      spanAttrs.error_code = errorCode;
    }

    Object.assign(spanAttrs, attributes);

    // Inject context
    const finalAttrs = this.middleware.injectContext(spanAttrs);

    // Create OTLP span
    const span = this._createOtlpSpan(spanName, finalAttrs);
    this.spans.push(span);

    // Auto-flush if batch is full
    if (this.spans.length >= this.batchSize) {
      await this.flush();
    }
  }

  _createOtlpSpan(spanName, attributes) {
    const now = new Date().toISOString();

    return {
      name: spanName,
      context: {
        traceId: this._generateTraceId(),
        spanId: this._generateSpanId(),
      },
      startTime: now,
      endTime: now,
      attributes,
      status: { code: attributes.status === 'success' ? 0 : 1 },
    };
  }

  async flush() {
    if (!this.spans.length || !this.enabled) return;

    try {
      const spansCopy = [...this.spans];
      this.spans = [];
      await this._sendSpans(spansCopy);
    } catch (error) {
      console.error(`Failed to flush telemetry spans: ${error.message}`);
    }
  }

  async shutdown() {
    if (this.flushTimer) {
      clearInterval(this.flushTimer);
      this.flushTimer = null;
    }
    await this.flush();
  }

  async _sendSpans(spans) {
    try {
      const headers = this.middleware.getHeaders();
      const payload = JSON.stringify({ spans });

      const response = await fetch(this.otlpEndpoint, {
        method: 'POST',
        headers,
        body: payload,
        timeout: 5000,
      });

      if (response.ok) {
        console.debug(`Sent ${spans.length} spans to ingester`);
        return true;
      } else {
        console.warn(`Ingester returned ${response.status}`);
        return false;
      }
    } catch (error) {
      console.warn(`Network error sending spans: ${error.message}`);
      return false;
    }
  }

  _generateTraceId() {
    return 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'.replace(/x/g, () =>
      Math.floor(Math.random() * 16).toString(16)
    );
  }

  _generateSpanId() {
    return 'xxxxxxxxxxxxxxxx'.replace(/x/g, () =>
      Math.floor(Math.random() * 16).toString(16)
    );
  }
}

// Global state
let _tracerInstance = null;
let _middleware = null;

/**
 * Get or create the global tracer instance
 *
 * @param {string} pluginId - Plugin identifier
 * @returns {Tracer} Tracer instance
 */
function getTracer(pluginId) {
  if (!_middleware) {
    _middleware = new TelemetryMiddleware();
  }

  if (!_tracerInstance) {
    _tracerInstance = new Tracer(pluginId, _middleware);
  }

  return _tracerInstance;
}

/**
 * Explicitly initialize telemetry with custom settings
 *
 * @param {string} otlpEndpoint - OTLP ingester endpoint
 * @param {number} batchSize - Batch size before flush
 * @param {number} flushIntervalSec - Flush interval in seconds
 * @returns {Tracer} Initialized tracer
 */
function initializeTelemetry(
  otlpEndpoint = 'https://telemetry.olytic.com/v1/traces',
  batchSize = 32,
  flushIntervalSec = 30
) {
  if (!_tracerInstance) {
    const tracer = getTracer('default');
    tracer.configure(otlpEndpoint, batchSize, flushIntervalSec);
  }

  return _tracerInstance;
}

/**
 * Flush and shutdown telemetry
 */
async function shutdownTelemetry() {
  if (_tracerInstance) {
    await _tracerInstance.shutdown();
    _tracerInstance = null;
  }
}
