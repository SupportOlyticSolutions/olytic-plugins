# Plugin Standards

**Version:** 1.0.0
**Owner:** Aulë
**Applies to:** Individual plugin design and authoring — rules for how each plugin is built

This document governs the design standards for individual Olytic plugins. Where `aule-core-standards.md` defines ecosystem-wide structural requirements, this document defines how a plugin should be designed — what components it needs, how they should behave, and what makes a plugin well-formed. These standards are used by `aule-verifier` during compliance scans and by the plugin compiler during generation.

---

## 1. Component Design

### Skills
A skill is a reusable, stateless sub-procedure. Skills are invoked by agents or commands and should do one thing well.

**Required per skill:**
- `SKILL.md` file with YAML frontmatter containing at minimum: `description` (≤200 chars) and trigger phrases
- Trigger phrases: ≥4 natural language phrases that would cause a user to invoke this skill
- Clear scope boundary — if a skill is doing two unrelated things, split it

**Prohibited:**
- Skills must not maintain state between invocations
- Skills must not call other skills directly — orchestration belongs in agents

### Agents
An agent is a stateful multi-turn orchestrator. Agents manage workflows that span multiple steps, tool calls, or user interactions.

**Required per agent:**
- Markdown file with YAML frontmatter containing at minimum: `description` and `allowed-tools`
- At least one `<example>` block in the YAML frontmatter showing a sample invocation
- Defined phases or steps — agents must have a clear progression, not open-ended behavior
- Exit conditions — every agent workflow must have a defined completion state

**Prohibited:**
- Agents must not write files outside the plugin's declared scope
- Agents must not take destructive actions without triggering a permission gate

### Commands
A command is a single-turn slash-command handler. Commands are user-facing entry points for specific, bounded actions.

**Required per command:**
- Markdown file with YAML frontmatter containing: `description`, `argument-hint`, `allowed-tools`
- Must complete in a single turn or hand off cleanly to an agent
- Must emit a `verification_gate` telemetry event after completing its action

---

## 2. Trigger Phrase Quality

Trigger phrases are how the platform routes user intent to the right component. Poor trigger phrases cause misrouting.

**Standards:**
- Each component must have ≥4 trigger phrases
- Phrases must be natural language — how a real user would phrase the request
- Phrases must be specific enough to distinguish this component from others in the same plugin
- Phrases should cover variations: question form, imperative form, task-framing form

**Examples of good trigger phrases:**
```
"build a new plugin for tracking customer tickets"
"create a plugin from scratch"
"I need a new Olytic plugin"
"start plugin creation"
```

**Examples of bad trigger phrases:**
```
"plugin"           ← too vague, will match everything
"do the thing"     ← meaningless
"create"           ← ambiguous across all creation tasks
```

---

## 3. README Requirements

Every plugin's `README.md` must include:

**Required sections:**
1. Plugin name and one-sentence description
2. **Claude OS Identity** — what the plugin is, what it does, what it does not do, and who it is for
3. Component inventory — list of all skills, agents, and commands with a one-line description each
4. Memory scope — ephemeral / persistent / retrieval, and what data is stored
5. Constraints — hard limits on what the plugin will and will not do

**Claude OS Identity block format:**
```
## Claude OS Identity

**This plugin is:** [what it is]
**This plugin does:** [key capabilities]
**This plugin does not:** [explicit boundaries]
**Built for:** [intended users or workflows]
**Memory:** [ephemeral/persistent/retrieval — what is stored and why]
```

---

## 4. Memory Scope

Plugins must declare one of three memory scopes and operate within it:

| Scope | Meaning | Vault writes |
|---|---|---|
| `ephemeral` | Session-only context — nothing persists after SessionClose | None |
| `persistent` | Structured facts and summaries written to vault at SessionClose | Via session-summarizer only |
| `retrieval` | Plugin actively reads from vault during sessions | Vault reads + session-summarizer writes |

Rules:
- A plugin cannot write to the vault unless its memory scope is `persistent` or `retrieval`
- Vault writes must always go through olytic-gateway — direct database access is prohibited
- Every vault write must conform to `contracts/schemas/vault-entry-schema.json`

---

## 5. Constraint Declaration

Every plugin must declare its constraints in both:
1. The README.md Constraints section
2. The `plugin_purpose` and `constraints` fields of its PluginSpec (used during compilation)

Constraints define the hard limits of what the plugin will do. They are not soft preferences — they are enforced behavioral boundaries. Examples:

- "This plugin does not write to any file outside `Plugins/[name]/`"
- "This plugin does not make API calls to services other than olytic-gateway"
- "This plugin requires explicit user confirmation before any file deletion"

---

## 6. Telemetry Requirements

Every plugin must emit telemetry for these events at minimum:

| Event | When to emit |
|---|---|
| `skill_invoke` | At the start of every skill invocation |
| `agent_trigger` | When an agent workflow is activated |
| `decision_trace` | When the plugin makes a non-trivial decision (branching logic, choosing between paths) |
| `verification_gate` | After any write operation is verified |
| `permission_gate` | Before any destructive or bulk action |
| `violation` | When a user request falls outside the plugin's declared constraints |

Telemetry must conform to `contracts/schemas/telemetry-event-schema.json`. Events are emitted silently — never announce logging to the user.

---

## 7. Compiler-Generated Components

The following components are auto-generated by the plugin compiler and must not be written manually:

- `[plugin-name]-telemetry/SKILL.md` — telemetry emission skill
- `[plugin-name]-session-summarizer/SKILL.md` — SessionClose vault writer
- `hooks/hooks.json` — hook declarations (if persistent or retrieval memory scope)

Manual edits to these files will be overwritten on the next compile cycle. To customize behavior, modify the PluginSpec and recompile.

---

## 8. Plugin Versioning Gates

Before a plugin version is considered releasable:

1. Compiler dry-run passes with no errors
2. `aule-verifier` reports zero compliance failures
3. All TODO placeholders resolved (no `[TODO ...]` strings in any file)
4. Trigger phrases reviewed for quality — no phrases shorter than 4 words
5. README contains all required sections

The compiler enforces gates 1 and 3. `aule-verifier` enforces gates 2 and 4. Gate 5 is a human review step.

---

## Relationship to Core Standards

```
aule-core-standards.md     ← structural requirements (what files must exist)
plugin-standards.md        ← design requirements (how components must be built)
agentic-behavior.md        ← behavioral requirements (how plugins must act at runtime)
```

All three protocols are enforced together. A plugin that passes structural checks but fails design standards is still non-compliant.
