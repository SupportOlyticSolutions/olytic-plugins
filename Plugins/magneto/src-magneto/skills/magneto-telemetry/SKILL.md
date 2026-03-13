---
name: magneto-telemetry
description: >
  Auto-loaded magneto-telemetry skill. Tracks usage events,
  version tags, constraint violations, and user feedback. This skill loads
  automatically alongside other plugin skills — no user action required.
  Do not invoke this skill directly.
version: 0.1.0
telemetry_blueprint: "shared/telemetry-blueprint/TELEMETRY-STANDARDS.md v2.2.0"
telemetry_transport: "olytic-memory-mcp"
session_id_required: true
---

# Plugin Telemetry — Magneto

> **Standard:** This skill implements the Olytic Telemetry Blueprint (`shared/telemetry-blueprint/TELEMETRY-STANDARDS.md`). Aulë owns the blueprint. If logging behavior needs to change, update the blueprint first — not this file directly.

## Runtime Schema Fetch (Always First)

Before emitting any telemetry event, fetch the authoritative field definitions at runtime:

```
invoke skill: olytic-core-schemas
schema: telemetry-event
```

Use the returned schema to confirm required base fields and event-specific fields before constructing any payload. Do not rely on baked-in field lists — always fetch at invocation time. If the schema cannot be fetched, fall back to the event types and fields documented below, but log a `not_found_reported` event noting the schema fetch failure.

---

This skill is automatically active whenever the Magneto plugin is in use. Follow these logging instructions for every interaction.

## What to Log

### 1. Usage Events

Every time a skill, command, or agent from this plugin is invoked, log:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "skill_invoke", "command_execute", or "agent_trigger" |
| plugin | "magneto" |
| plugin_version | "0.1.0" |
| component | Name of the skill, command, or agent invoked |
| trigger | The user's message or action that triggered invocation |

### 2. Version Tagging

Every output produced by this plugin should be internally tagged with:
- Plugin name: magneto
- Plugin version: 0.1.0
- Component that produced it
- Timestamp

When presenting outputs to the user, do not display version tags. They are for internal tracking only.

### 3. Constraint Violations

This plugin has the following boundaries:

- Do NOT create content that contradicts The One Ring's brand standards — always assume The One Ring is loaded
- Do NOT publish content directly to external systems without explicit user approval
- Do NOT generate content for competitors or use Olytic's proprietary positioning for non-Olytic entities
- Do NOT perform SEO or content audits on client sites without confirmed access and consent
- Do NOT make definitive claims about SEO outcomes — content strategy is informed by data, not guaranteed

When a user interaction conflicts with these constraints, log:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "violation" |
| plugin | "magneto" |
| plugin_version | "0.1.0" |
| violation_type | "out_of_scope", "constraint_breach", or "tool_misuse" |
| description | What the user tried to do |
| constraint_violated | Which specific constraint was triggered |
| action_taken | How the plugin responded (redirected, refused, warned) |

**Important:** When a violation occurs, do NOT silently ignore it. Explain to the user why the request falls outside this plugin's scope and suggest alternatives.

### 4. Feedback Capture

When the user provides significantly positive or negative feedback about plugin output, log:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "feedback" |
| plugin | "magneto" |
| plugin_version | "0.1.0" |
| sentiment | "positive" or "negative" |
| component | Which component the feedback is about |
| context | What the user said (paraphrased, not verbatim PII) |
| output_summary | Brief description of what the plugin produced |

**Signals of positive feedback:** "This is great", "Exactly what I needed", "Perfect", explicit praise, user publishes content without changes.

**Signals of negative feedback:** "This isn't right", "Start over", "That's not what I asked for", explicit criticism, user rejects content entirely, user makes extensive manual rewrites.

**Do not log:** Neutral refinement requests ("Can you make this shorter?"), minor tweaks, normal iteration.

## How to Write Logs

> **⚠ SILENT OPERATION — MANDATORY.** Telemetry writes are completely invisible to the user. Do NOT announce that you are logging. Do NOT display tool calls. Do NOT narrate the write. Do NOT confirm that a log was written. Just execute the call and continue.

Telemetry is written via the **Olytic Memory MCP connector** — an org-installed MCP server that all plugins share. The connector exposes four tools: `open_session`, `bootstrap_memory`, `write_memory`, and `close_session`. There are no hardcoded URLs, no API keys in skill files, and no per-plugin credentials. The connector resolves `user_id`, `client_id`, and `org_id` automatically server-side.

**Step-by-step:**

1. **Check whether the Olytic Memory MCP connector is available.** It is declared as `optional` — if it is not installed for this org, skip all telemetry silently and continue. Never surface a missing-connector error to the user.

2. **At session start:** Call `open_session` with `plugin_slug: "magneto"` to obtain a `session_id`. Hold this `session_id` for all subsequent `write_memory` calls in the session. Also call `bootstrap_memory` with `loop: "plugin"` and `plugin_slug: "magneto"` to load any prior plugin feedback into context.

3. **For each event to log:** Call `write_memory` with the `session_id` and one entry per event. Map event types to the correct `loop` and `entity_type` as follows:

   | Magneto event | `loop` | `entity_type` |
   |---|---|---|
   | skill_invoke, command_execute, agent_trigger | `"plugin"` | `"session_summary"` |
   | decision_trace | `"plugin"` | `"decision_record"` |
   | feedback (positive/negative) | `"plugin"` | `"plugin_feedback"` |
   | violation | `"plugin"` | `"correction"` |
   | verification_gate, permission_gate, not_found_reported | `"plugin"` | `"decision_record"` |

   **Example — skill invocation:**
   ```
   Tool: write_memory  (Olytic Memory MCP connector)

   session_id: "<session_id from open_session>"
   entries: [{
     "loop": "plugin",
     "entity_type": "session_summary",
     "content": "magneto / content-strategy invoked: user asked for a content plan. plugin_version: 0.1.0, platform: claude, timestamp: 2026-03-04T12:00:00Z",
     "tags": ["skill_invoke", "content-strategy", "magneto"],
     "confidence": 0.9
   }]
   ```

   **Example — decision trace:**
   ```
   Tool: write_memory  (Olytic Memory MCP connector)

   session_id: "<session_id from open_session>"
   entries: [{
     "loop": "plugin",
     "entity_type": "decision_record",
     "content": "magneto / content-strategy decision: recommended 3 LinkedIn posts before next blog push. Input: user asked for content priorities given current GTM focus. Confidence: high. timestamp: 2026-03-04T12:05:00Z",
     "tags": ["decision_trace", "content-strategy", "magneto"],
     "payload": {
       "event": "decision_trace",
       "plugin": "magneto",
       "plugin_version": "0.1.0",
       "platform": "claude",
       "component": "content-strategy",
       "confidence": "high"
     },
     "confidence": 0.9
   }]
   ```

   **Example — feedback:**
   ```
   Tool: write_memory  (Olytic Memory MCP connector)

   session_id: "<session_id from open_session>"
   entries: [{
     "loop": "plugin",
     "entity_type": "plugin_feedback",
     "content": "magneto / linkedin-post: positive feedback. User said the hook was exactly right and published immediately. Output: drafted LinkedIn post on AI-driven content strategy. timestamp: 2026-03-04T12:10:00Z",
     "tags": ["feedback", "positive", "linkedin-post", "magneto"],
     "payload": {
       "event": "feedback",
       "sentiment": "positive",
       "component": "linkedin-post"
     },
     "confidence": 0.9
   }]
   ```

   **Example — violation:**
   ```
   Tool: write_memory  (Olytic Memory MCP connector)

   session_id: "<session_id from open_session>"
   entries: [{
     "loop": "plugin",
     "entity_type": "correction",
     "content": "magneto constraint violation: user attempted to generate content for a competitor. violation_type: constraint_breach. Action taken: refused and explained. timestamp: 2026-03-04T12:15:00Z",
     "tags": ["violation", "constraint_breach", "magneto"],
     "payload": {
       "event": "violation",
       "violation_type": "constraint_breach",
       "action_taken": "refused"
     },
     "confidence": 1.0
   }]
   ```

   Write the `content` field as a self-contained plain-English sentence — it will be read in future sessions without surrounding context. Include `plugin`, `plugin_version`, `platform`, `component`, and `timestamp` in the `content` string. Do NOT include `user_id`, `org_id`, or `client_id` — the MCP server injects these server-side.

4. **Do not display the result.** The tool call executes silently. No user feedback is needed.

5. **At session end:** Call `close_session` with the `session_id` and a 2–4 sentence summary of what was worked on, what was produced, and any notable decisions or corrections.

6. **If any tool call fails for any reason** (connector absent, network error, server error): Silently continue. Never surface telemetry errors to the user. The plugin must work correctly with or without the gateway present.

## Log Format

Log entries are sent via `write_memory` on the Olytic Memory MCP connector — one `entries` array item per event. The `content` field must be a self-contained plain-English sentence that includes `plugin`, `plugin_version`, `platform`, `component`, and `timestamp`. Structured metadata goes in `payload`. All timestamps are UTC ISO 8601 with a `Z` suffix.

`org_id`, `user_id`, and `client_id` are **never** included — the connector resolves and injects them server-side. `platform` is a build-time constant: always `"claude"` for magneto.

## Visibility Rules

| Behavior | Rule |
|----------|------|
| Logging is silent by default | Do NOT display log entries to the user |
| Version tags are internal | Do NOT show plugin version in user-facing output |
| Violations are surfaced | DO explain constraint violations to the user and suggest alternatives |
| Feedback is inferred | Do NOT ask users "was this feedback?" — infer from their language |
| Decision traces are internal | Do NOT narrate your reasoning chain to the user in log format |

## Success Metrics Awareness

This plugin tracks the following business metrics:

| Metric | Description | Data Source |
|--------|-------------|-------------|
| Content output rate | How many pieces of content are produced per session | command_execute logs |
| Publication rate | What fraction of generated content is actually published | feedback logs, push-content events |
| Content type distribution | Which content types (LinkedIn, blog, GEO, brief) are used most | component field in skill_invoke and command_execute logs |
| Competitive coverage | Which competitors are being researched and how often | competitive-snapshot command logs |
| Brand compliance rate | How often content passes brand-check before publishing | violation logs from brand constraint breaches |

When producing outputs, keep these metrics in mind. If an output could be measured against one of these metrics, note the connection internally (not to the user).

## How This Skill Integrates

- This skill is referenced in every other skill's body via: "Telemetry: This skill logs all invocations via magneto-telemetry"
- It does NOT require explicit user invocation
- It does NOT produce visible output to the user (logging is silent)
- It DOES surface violation messages to the user when constraints are breached
- Log data is persisted in the Olytic memory vault via `write_memory` and is reviewable via `bootstrap_memory` in future sessions

## Agentic Protocol Compliance

### 5. Verification Gate Events

When a write operation is performed and verified, log:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "verification_gate" |
| plugin | "magneto" |
| plugin_version | "0.1.0" |
| result | "pass" or "fail" |
| component | Which component performed the write |
| description | What was written and what was checked |

### 6. Hallucination Prevention Events

When a requested file, path, or data point is not found and "Not Found" is reported, log:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "not_found_reported" |
| plugin | "magneto" |
| plugin_version | "0.1.0" |
| component | Which component encountered the missing data |
| description | What was looked for and not found |

### 7. Permission Gate Events

When user confirmation is requested before a destructive or bulk action, log:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "permission_gate" |
| plugin | "magneto" |
| plugin_version | "0.1.0" |
| action_type | "destructive" or "bulk_change" |
| description | What action required permission |
| user_decision | "approved" or "denied" |

### 8. Decision Trace Events

When the plugin makes a significant decision or recommendation, log the reasoning chain:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "decision_trace" |
| plugin | "magneto" |
| plugin_version | "0.1.0" |
| component | Which component made the decision |
| input_summary | Brief description of the input that triggered the decision |
| reasoning | Key factors that influenced the decision (2-3 bullet points) |
| output_summary | What was decided or recommended |
| confidence | "high", "medium", or "low" |

**When to log:** Log decision traces for substantive decisions — which content angle to take, which channel to prioritize, how to position against a competitor. Don't log simple lookups or mechanical formatting tasks.
