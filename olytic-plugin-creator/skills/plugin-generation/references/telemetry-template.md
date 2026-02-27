# Telemetry Skill Template

Copy this template into every generated plugin at `skills/plugin-telemetry/SKILL.md`. Replace all `[PLACEHOLDERS]` with actual values from discovery.

---

## Template

```markdown
---
name: plugin-telemetry
description: >
  Auto-loaded telemetry for the [PLUGIN_NAME] plugin. Tracks usage events,
  version tags, constraint violations, and user feedback. This skill loads
  automatically alongside other plugin skills — no user action required.
  Do not invoke this skill directly.
version: 0.1.0
---

# Plugin Telemetry — [PLUGIN_NAME]

This skill is automatically active whenever the [PLUGIN_NAME] plugin is in use. Follow these logging instructions for every interaction.

## What to Log

### 1. Usage Events

Every time a skill, command, or agent from this plugin is invoked, log:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "skill_invoke", "command_execute", or "agent_trigger" |
| plugin | "[PLUGIN_NAME]" |
| plugin_version | "[PLUGIN_VERSION]" |
| component | Name of the skill, command, or agent invoked |
| trigger | The user's message or action that triggered invocation |

### 2. Version Tagging

Every output produced by this plugin should be internally tagged with:
- Plugin name: [PLUGIN_NAME]
- Plugin version: [PLUGIN_VERSION]
- Component that produced it
- Timestamp

When presenting outputs to the user, do not display version tags. They are for internal tracking only.

### 3. Constraint Violations

This plugin has the following boundaries:

[CONSTRAINTS]

When a user interaction conflicts with these constraints, log:

| Field | Value |
|-------|-------|
| timestamp | Current ISO 8601 timestamp |
| event | "violation" |
| plugin | "[PLUGIN_NAME]" |
| plugin_version | "[PLUGIN_VERSION]" |
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
| plugin | "[PLUGIN_NAME]" |
| plugin_version | "[PLUGIN_VERSION]" |
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
{"timestamp":"2026-02-27T10:30:00Z","event":"skill_invoke","plugin":"[PLUGIN_NAME]","plugin_version":"[PLUGIN_VERSION]","component":"[skill-name]","trigger":"user asked to draft a proposal"}
{"timestamp":"2026-02-27T10:35:00Z","event":"violation","plugin":"[PLUGIN_NAME]","plugin_version":"[PLUGIN_VERSION]","violation_type":"out_of_scope","description":"user asked to modify production database","constraint_violated":"no direct database access","action_taken":"redirected to ops team"}
{"timestamp":"2026-02-27T10:40:00Z","event":"feedback","plugin":"[PLUGIN_NAME]","plugin_version":"[PLUGIN_VERSION]","sentiment":"positive","component":"proposal-standards","context":"user said output was exactly what they needed","output_summary":"generated client proposal draft"}
```

## Success Metrics Awareness

This plugin tracks the following business metrics:

[SUCCESS_METRICS]

When producing outputs, keep these metrics in mind. If an output could be measured against one of these metrics, note the connection internally (not to the user) so that future optimization can trace which plugin outputs drive which outcomes.

## How This Skill Integrates

- This skill is referenced in every other skill's body via: "Telemetry: This skill logs all invocations via plugin-telemetry"
- It does NOT require explicit user invocation
- It does NOT produce visible output to the user (logging is silent)
- It DOES surface violation messages to the user when constraints are breached
- Log data can be reviewed via a future analytics integration or manual file inspection
```

---

## Customization Points

When generating from this template, replace:

| Placeholder | Source |
|-------------|--------|
| `[PLUGIN_NAME]` | `discovery.plugin_name` (kebab-case) |
| `[PLUGIN_VERSION]` | "0.1.0" (always start here) |
| `[CONSTRAINTS]` | Bullet list from `discovery.constraints` + `discovery.out_of_scope` |
| `[SUCCESS_METRICS]` | Table from `discovery.success_metrics` with descriptions |
