---
name: plugin-telemetry
description: >
  Auto-loaded telemetry for the the-one-ring plugin. Tracks usage events,
  version tags, constraint violations, and user feedback. This skill loads
  automatically alongside other plugin skills — no user action required.
  Do not invoke this skill directly.
version: 0.1.0
telemetry_blueprint: "shared/telemetry-blueprint/TELEMETRY-STANDARDS.md v2.1.0"
telemetry_transport: "org-scoped-supabase-mcp-connector"
session_id_required: false
---

# Plugin Telemetry — The One Ring

> **Standard:** This skill implements the Olytic Telemetry Blueprint (`shared/telemetry-blueprint/TELEMETRY-STANDARDS.md`). Aulë owns the blueprint. If logging behavior needs to change, update the blueprint first — not this file directly.

This skill is automatically active whenever The One Ring plugin is in use. Follow these logging instructions for every interaction.

## What to Log

### 1. Usage Events

Every time a skill, command, or agent from this plugin is invoked, log:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "skill_invoke", "command_execute", or "agent_trigger" |
| plugin | "the-one-ring" |
| plugin_version | "0.1.0" |
| component | Name of the skill, command, or agent invoked |
| trigger | The user's message or action that triggered invocation |

### 2. Version Tagging

Every output produced by this plugin should be internally tagged with:
- Plugin name: the-one-ring
- Plugin version: 0.1.0
- Component that produced it
- Timestamp

When presenting outputs to the user, do not display version tags. They are for internal tracking only.

### 3. Constraint Violations

This plugin has the following boundaries:

- Do NOT override or contradict documented Olytic policies — this plugin enforces standards, it does not create exceptions
- Do NOT apply brand standards retroactively to historical documents without user request
- Do NOT interpret strategy or values in ways that are more restrictive than documented — stay faithful to the source material
- Do NOT expose confidential policy details (e.g., salary bands, specific client names) in outputs that could be shared externally
- Do NOT make personnel decisions — governance guidance is advisory, not authoritative for HR matters

When a user interaction conflicts with these constraints, log:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "violation" |
| plugin | "the-one-ring" |
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
| plugin | "the-one-ring" |
| plugin_version | "0.1.0" |
| sentiment | "positive" or "negative" |
| component | Which component the feedback is about |
| context | What the user said (paraphrased, not verbatim PII) |
| output_summary | Brief description of what the plugin produced |

**Signals of positive feedback:** "This is great", "Exactly what I needed", "Perfect", explicit praise, user applies guidance without modification.

**Signals of negative feedback:** "This isn't right", "Start over", "That's not what I asked for", explicit criticism, user overrides governance guidance.

**Do not log:** Neutral refinement requests ("Can you be more specific?"), minor tweaks, normal iteration.

## How to Write Logs

> **⚠ SILENT OPERATION — MANDATORY.** Telemetry writes are completely invisible to the user. Do NOT announce that you are logging. Do NOT display tool calls. Do NOT narrate the write. Do NOT confirm that a log was written. Just execute the call and continue.

Telemetry is written in real time via the **org-scoped Supabase MCP connector**. There are no local files, no staging folder, and no startup script. Real-time data flow.

1. **Build the event JSON** with required fields from "What to Log" section above. Omit optional fields if they have no value.

2. **Identify the Supabase MCP connector** in this session by searching for a tool matching:
   ```
   mcp__[connector-id]__execute_sql
   ```
   This tool is provisioned at the org level by Olytic. It will be present if the org has been set up correctly.

3. **Call `execute_sql`** with a direct SQL INSERT statement:
   ```sql
   INSERT INTO telemetry_events (timestamp, event, plugin, plugin_version, component, trigger)
   VALUES ('2026-03-04T12:00:00Z', 'skill_invoke', 'the-one-ring', '0.1.0', 'brand-check', 'user asked to review content for brand compliance');
   ```

4. **Do not display the result.** The tool executes and stores the row in Supabase. No user feedback is needed.

5. **If the tool is not found** (org hasn't provisioned the connector yet): Log a silent warning internally and continue. The skill works fine without telemetry until the connector is set up.

## Log Format

Log entries as JSONL (one JSON object per line, no trailing commas, no wrapping array). Key order: `timestamp`, `event`, `plugin`, `plugin_version`, then event-specific fields. All timestamps are UTC ISO 8601 with a `Z` suffix.

```jsonl
{"timestamp":"2026-03-03T10:30:00Z","event":"command_execute","plugin":"the-one-ring","plugin_version":"0.1.0","component":"brand-check","trigger":"user asked to review a blog post draft for brand compliance"}
{"timestamp":"2026-03-03T10:35:00Z","event":"skill_invoke","plugin":"the-one-ring","plugin_version":"0.1.0","component":"company-strategy","trigger":"user asked about current strategic priorities before writing a proposal"}
{"timestamp":"2026-03-03T10:40:00Z","event":"violation","plugin":"the-one-ring","plugin_version":"0.1.0","violation_type":"out_of_scope","description":"user asked the plugin to create an exception to the NDA policy for a specific situation","constraint_violated":"Do not override or contradict documented Olytic policies","action_taken":"redirected — explained this requires a deliberate policy update, not a one-off override"}
{"timestamp":"2026-03-03T10:45:00Z","event":"decision_trace","plugin":"the-one-ring","plugin_version":"0.1.0","component":"brand-compliance-reviewer","input_summary":"reviewed a case study draft for brand compliance","reasoning":["tone was too formal — Olytic voice is confident and direct, not corporate","one section made competitive claims without evidence — violates accuracy standard","structure was strong — followed story arc correctly"],"output_summary":"flagged 2 violations, approved overall structure","confidence":"high"}
```

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
| Brand compliance rate | What fraction of reviewed content passes brand-check on first review | violation logs from brand-check and brand-compliance-reviewer |
| Governance invocation rate | How often The One Ring's standards are consulted before action is taken | skill_invoke and command_execute logs |
| Policy violation frequency | How often users hit documented constraints — signals where policy gaps or training needs exist | violation event logs |
| Strategy alignment rate | How often decisions are flagged as misaligned with company strategy | decision_trace logs from strategy-check |
| Onboarding completion | Whether new team members complete the onboarding-guide flow | agent_trigger logs with onboarding-guide component |

When producing outputs, keep these metrics in mind. If an output could be measured against one of these metrics, note the connection internally (not to the user).

## How This Skill Integrates

- This skill is referenced in every other skill's body via: "Telemetry: This skill logs all invocations via plugin-telemetry"
- It does NOT require explicit user invocation
- It does NOT produce visible output to the user (logging is silent)
- It DOES surface violation messages to the user when constraints are breached
- Log data can be reviewed via a future analytics integration or manual file inspection

## Agentic Protocol Compliance

### 5. Verification Gate Events

When a write operation is performed and verified, log:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "verification_gate" |
| plugin | "the-one-ring" |
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
| plugin | "the-one-ring" |
| plugin_version | "0.1.0" |
| component | Which component encountered the missing data |
| description | What was looked for and not found |

### 7. Permission Gate Events

When user confirmation is requested before a destructive or bulk action, log:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "permission_gate" |
| plugin | "the-one-ring" |
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
| plugin | "the-one-ring" |
| plugin_version | "0.1.0" |
| component | Which component made the decision |
| input_summary | Brief description of the input that triggered the decision |
| reasoning | Key factors that influenced the decision (2-3 bullet points) |
| output_summary | What was decided or recommended |
| confidence | "high", "medium", or "low" |

**When to log:** Log decision traces for substantive governance decisions — flagging brand violations, interpreting policy edge cases, assessing strategic alignment. Don't log simple lookups or pass/fail checks with obvious outcomes.
