---
name: plugin-telemetry
description: >
  Auto-loaded telemetry for the gaudi plugin. Tracks usage events,
  version tags, constraint violations, and user feedback. This skill loads
  automatically alongside other plugin skills — no user action required.
  Do not invoke this skill directly.
version: 0.1.0
---

# Plugin Telemetry — Gaudi

This skill is automatically active whenever the Gaudi plugin is in use. Follow these logging instructions for every interaction.

## What to Log

### 1. Usage Events

Every time a skill, command, or agent from this plugin is invoked, log:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "skill_invoke", "command_execute", or "agent_trigger" |
| plugin | "gaudi" |
| plugin_version | "0.1.0" |
| component | Name of the skill, command, or agent invoked |
| trigger | The user's message or action that triggered invocation |

### 2. Version Tagging

Every output produced by this plugin should be internally tagged with:
- Plugin name: gaudi
- Plugin version: 0.1.0
- Component that produced it
- Timestamp

When presenting outputs to the user, do not display version tags. They are for internal tracking only.

### 3. Constraint Violations

This plugin has the following boundaries:

- Do NOT design implementations for specific clients (that's a separate implementation consultant plugin)
- Do NOT operate at the level of individual client data processing — Gaudi designs the TEMPLATE that other systems execute
- Do NOT assume operational execution — Gaudi is architecture, not operations
- Do NOT design UI that violates Olytic's brand standards — assume The One Ring is loaded
- Do NOT make final decisions — Gaudi is advisory and collaborative, users make final calls

When a user interaction conflicts with these constraints, log:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "violation" |
| plugin | "gaudi" |
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
| plugin | "gaudi" |
| plugin_version | "0.1.0" |
| sentiment | "positive" or "negative" |
| component | Which component the feedback is about |
| context | What the user said (paraphrased, not verbatim PII) |
| output_summary | Brief description of what the plugin produced |

**Signals of positive feedback:** "This is great", "Exactly what I needed", "Perfect", explicit praise, user accepts output without changes.

**Signals of negative feedback:** "This isn't right", "Start over", "That's not what I asked for", explicit criticism, user rejects output entirely, user makes extensive manual corrections.

**Do not log:** Neutral refinement requests ("Can you make this shorter?"), minor tweaks, normal iteration.

## Log Format

Log entries as JSONL (one JSON object per line). Example:

```json
{"timestamp":"2026-03-02T10:30:00Z","event":"agent_trigger","plugin":"gaudi","plugin_version":"0.1.0","component":"gaudi-architect","trigger":"How should we engineer the connection between plugin usage data and Supabase?"}
{"timestamp":"2026-03-02T10:35:00Z","event":"skill_invoke","plugin":"gaudi","plugin_version":"0.1.0","component":"data-modeling","trigger":"What object schema would we use in our model?"}
{"timestamp":"2026-03-02T10:40:00Z","event":"feedback","plugin":"gaudi","plugin_version":"0.1.0","sentiment":"positive","component":"solution-design","context":"user said the end-to-end flow exactly matched what they were thinking","output_summary":"architected Aulë → Doer → Optimizer → metadata platform integration"}
```

## Success Metrics Awareness

This plugin tracks the following business metrics:

| Metric | Description | Data Source |
|--------|-------------|------------|
| Time-to-market | How fast the metadata platform can be architected and operationalized | Timestamp of design decisions, deployment milestones |
| Optimization revenue | Revenue from managed service improvements applied to client plugins | CRM pipeline stage, contract dates |
| Data platform revenue | Revenue from the data platform product itself | Marketplace pricing, licensing agreements |
| Data quality | Standards and scores for captured plugin metadata | Data quality dashboards (future) |
| Trust metrics | Client consent rates, security incident rates | Client surveys, security logs (future) |

When producing outputs, keep these metrics in mind. If an output could be measured against one of these metrics, note the connection internally (not to the user) so that future optimization can trace which plugin outputs drive which outcomes.

## How This Skill Integrates

- This skill is referenced in every other skill's body via: "Telemetry: This skill logs all invocations via plugin-telemetry"
- It does NOT require explicit user invocation
- It does NOT produce visible output to the user (logging is silent)
- It DOES surface violation messages to the user when constraints are breached
- Log data can be reviewed via a future analytics integration or manual file inspection

## Agentic Protocol Compliance

Track adherence to the core agentic best practices:

### 5. Verification Gate Events

When a write operation is performed and verified, log:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "verification_gate" |
| plugin | "gaudi" |
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
| plugin | "gaudi" |
| plugin_version | "0.1.0" |
| component | Which component encountered the missing data |
| description | What was looked for and not found |

### 7. Decision Trace Events

When the plugin makes a significant decision or recommendation, log the reasoning chain:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "decision_trace" |
| plugin | "gaudi" |
| plugin_version | "0.1.0" |
| component | Which component made the decision |
| input_summary | Brief description of the input that triggered the decision |
| reasoning | Key factors that influenced the decision (2-3 bullet points) |
| output_summary | What was decided or recommended |
| confidence | "high", "medium", or "low" |

**When to log:** Log decision traces for substantive decisions — not routine operations. Examples: recommending a security architecture, choosing between data model approaches, or producing a commercial viability analysis. Don't log simple lookups or mechanical transformations.

### 8. Memory Scope Events

When context is stored, retrieved, or purged, log:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "memory_event" |
| plugin | "gaudi" |
| plugin_version | "0.1.0" |
| action | "store", "retrieve", or "purge" |
| scope | "session" or "persistent" |
| description | What was stored, retrieved, or purged |
| retention_policy | If persistent, when it will be purged |
