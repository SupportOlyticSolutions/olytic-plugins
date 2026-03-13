---
name: olytic-core-schemas
description: >
  Runtime schema provider for all Olytic organizational plugins. Returns the canonical
  JSON schema content for any olytic-core contract schema by name. This skill is the
  authoritative runtime source of truth — other plugins call this skill instead of reading
  schema files from the filesystem. Invoke with: "invoke skill: olytic-core-schemas / schema:
  telemetry-event", "fetch the vault-entry schema", "get session-summary schema from olytic-core",
  "what are the required fields for plugin-identity", "return the hook-event schema".
version: 1.0.0
---

# olytic-core-schemas

**Version:** 1.0.0
**Owner:** olytic-core
**Purpose:** Runtime schema provider for all Olytic organizational plugins. Returns the canonical JSON schema content for any olytic-core contract schema by name. This skill is the authoritative runtime source of truth — other plugins call this skill instead of reading schema files from the filesystem (which is not reliable when plugins are installed as Organizational Plugins rather than mounted workspace folders).

---

## When This Skill Is Invoked

This skill is invoked by **other plugins** (not by users) when they need the current schema definition for an olytic-core contract. Common invocation points:

- Before emitting a telemetry event (fetch `telemetry-event` to confirm required fields)
- Before writing a vault entry (fetch `vault-entry` to confirm envelope structure)
- Before writing a session summary (fetch `session-summary` to confirm content payload fields)
- When generating a new plugin (fetch `plugin-identity` to confirm plugin.json field requirements)
- When handling hook events (fetch `hook-event` to confirm hook payload structure)
- When declaring memory access control (fetch `memory-access` to confirm declaration fields)

Invocation pattern (used in other plugin skills):

```
invoke skill: olytic-core-schemas
schema: <schema-name>
```

---

## Available Schemas

| Schema Name | $id | Description |
|---|---|---|
| `telemetry-event` | `telemetry-event-schema` | Base fields + event-specific fields for all 8 telemetry event types |
| `vault-entry` | `vault-entry-schema` | Envelope wrapper for all vault writes (maps to `memory_entries` row) |
| `session-summary` | `session-summary-schema` | Content payload for episodic session memory (wrapped by vault-entry) |
| `plugin-identity` | `plugin-identity-schema` | Fields for plugin.json and workspace.json registration |
| `hook-event` | `hook-event-schema` | Hook types, payload shapes, and hooks.json entry structure |
| `memory-access` | `memory-access-schema` | Vault access control declaration structure |

---

## Execution

When invoked, identify which schema is being requested and return the full schema content below verbatim. Do not summarize, abbreviate, or paraphrase — return the complete JSON object.

If the requested schema name does not match any entry in the table above, respond:

```
olytic-core-schemas: unknown schema "<requested-name>"
Valid schema names: telemetry-event, vault-entry, session-summary, plugin-identity, hook-event, memory-access
```

---

## Schema Content

### `telemetry-event`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "telemetry-event-schema",
  "title": "Olytic Telemetry Event",
  "description": "Canonical schema for all telemetry events emitted by Olytic plugins. All 8 event types share the base fields; each event type adds its own required fields.",
  "version": "1.2.0",
  "owner": "aule",
  "event_types": [
    "skill_invoke",
    "decision_trace",
    "feedback",
    "violation",
    "not_found_reported",
    "verification_gate",
    "permission_gate",
    "agent_trigger"
  ],
  "base_fields": {
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 UTC timestamp with Z suffix",
      "required": true
    },
    "event": {
      "type": "string",
      "enum": ["skill_invoke", "decision_trace", "feedback", "violation", "not_found_reported", "verification_gate", "permission_gate", "agent_trigger"],
      "required": true
    },
    "plugin": {
      "type": "string",
      "description": "Kebab-case plugin name",
      "required": true
    },
    "plugin_version": {
      "type": "string",
      "description": "Semver string",
      "required": true
    },
    "session_id": {
      "type": "string",
      "format": "uuid",
      "description": "UUID FK to sessions.id — include if known, gateway links retroactively if omitted",
      "required": false
    },
    "component": {
      "type": "string",
      "description": "Name of the skill, command, or agent that emitted this event",
      "required": true
    },
    "platform": {
      "type": "string",
      "enum": ["claude", "chatgpt", "copilot", "other"],
      "description": "Hardcoded per plugin at generation time — never inferred at runtime",
      "required": true
    }
  },
  "event_fields": {
    "skill_invoke": {
      "trigger": { "type": "string", "description": "Paraphrase of the user message that triggered invocation (5-15 words, no PII)", "required": true }
    },
    "agent_trigger": {
      "trigger": { "type": "string", "description": "Paraphrase of what triggered agent activation", "required": true }
    },
    "decision_trace": {
      "input_summary": { "type": "string", "required": true },
      "reasoning": { "type": "array", "items": { "type": "string" }, "description": "2-3 key factors", "required": true },
      "output_summary": { "type": "string", "required": true },
      "confidence": { "type": "string", "enum": ["high", "medium", "low"], "required": true }
    },
    "feedback": {
      "sentiment": { "type": "string", "enum": ["positive", "negative"], "required": true },
      "context": { "type": "string", "description": "What the user said (paraphrased, no PII)", "required": true },
      "output_summary": { "type": "string", "required": true }
    },
    "violation": {
      "violation_type": { "type": "string", "enum": ["out_of_scope", "constraint_breach", "tool_misuse"], "required": true },
      "description": { "type": "string", "required": true },
      "constraint_violated": { "type": "string", "required": true },
      "action_taken": { "type": "string", "enum": ["redirected", "refused", "warned"], "required": true }
    },
    "not_found_reported": {
      "description": { "type": "string", "required": true }
    },
    "verification_gate": {
      "result": { "type": "string", "enum": ["pass", "fail"], "required": true },
      "description": { "type": "string", "required": true }
    },
    "permission_gate": {
      "action_type": { "type": "string", "enum": ["destructive", "bulk_change"], "required": true },
      "description": { "type": "string", "required": true },
      "user_decision": { "type": "string", "enum": ["approved", "denied"], "required": true }
    }
  },
  "notes": [
    "client_id and user_id are resolved and injected server-side by the gateway — never include in the plugin payload",
    "session_id maps to sessions.id — include if known, gateway links retroactively if omitted",
    "All timestamps must be UTC ISO 8601 with Z suffix",
    "Key order in JSONL: timestamp, event, plugin, plugin_version, platform, component, then event-specific fields",
    "Logging is always silent — never announce a write to the user"
  ]
}
```

---

### `vault-entry`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "vault-entry-schema",
  "title": "Olytic Vault Entry",
  "description": "Canonical envelope schema for all vault writes. Maps 1:1 to a memory_entries row in Supabase. The content field contains the payload and is stored in memory_entries.payload (jsonb). client_id and user_id are never included in the plugin payload — they are resolved and injected by the gateway.",
  "version": "1.2.0",
  "owner": "aule",
  "db_table": "memory_entries",
  "properties": {
    "entry_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier — generate per write. Maps to memory_entries.id.",
      "required": true
    },
    "session_id": {
      "type": "string",
      "format": "uuid",
      "description": "UUID FK to sessions.id. Include if known at write time. Gateway creates/links session row if omitted.",
      "required": false
    },
    "plugin": {
      "type": "string",
      "description": "Kebab-case plugin name. Maps to memory_entries.source_plugin.",
      "required": true
    },
    "plugin_version": {
      "type": "string",
      "description": "Semver version at time of write.",
      "required": true
    },
    "session_timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 UTC timestamp of when this entry was written. Maps to memory_entries.created_at.",
      "required": true
    },
    "entry_type": {
      "type": "string",
      "enum": ["session_summary", "user_preference", "decision_record", "correction", "business_fact", "plugin_feedback"],
      "description": "Type tag mapping to memory_entries.entity_type. Uses underscores to match DB column exactly.",
      "required": true
    },
    "loop": {
      "type": "string",
      "enum": ["plugin", "user", "client"],
      "description": "Which refinement loop this entry feeds. Maps to memory_entries.loop.",
      "required": true
    },
    "schema_version": {
      "type": "string",
      "description": "Version of the content schema used (e.g., '1.2.0'). Stored in payload for server-side validation.",
      "required": true
    },
    "platform": {
      "type": "string",
      "enum": ["claude", "chatgpt", "copilot", "other"],
      "description": "Hardcoded per plugin at generation time — never inferred at runtime.",
      "required": true
    },
    "content": {
      "type": "object",
      "description": "The actual payload — shape depends on entry_type. For session_summary, this is a session-summary-schema object. Stored in memory_entries.payload (jsonb).",
      "required": true
    }
  },
  "notes": [
    "client_id and user_id are resolved and injected server-side by the gateway — never include in the entry body",
    "entry_type enum values use underscores to match memory_entries.entity_type exactly",
    "loop maps to memory_entries.loop — drives review cycle bucketing",
    "memory_entries.status defaults to 'soft' on insert — portal review cycle promotes to 'committed'"
  ]
}
```

---

### `session-summary`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "session-summary-schema",
  "title": "Olytic Session Summary",
  "description": "Canonical schema for episodic session memory content. This is the CONTENT payload — it is wrapped in vault-entry-schema before being written to the vault.",
  "version": "1.2.0",
  "owner": "aule",
  "relationship": "Content payload — wrapped in vault-entry-schema envelope before vault write",
  "properties": {
    "platform": {
      "type": "string",
      "enum": ["claude", "chatgpt", "copilot", "other"],
      "description": "Hardcoded per plugin at generation time — never inferred at runtime.",
      "required": true
    },
    "loop": {
      "type": "string",
      "enum": ["plugin", "user", "client"],
      "description": "Which refinement loop this summary feeds. Default 'plugin' for auto-generated session summaries.",
      "required": true,
      "default": "plugin"
    },
    "primary_topic": {
      "type": "string",
      "description": "One sentence describing the main thing worked on this session",
      "required": true,
      "max_length": 200
    },
    "key_decisions": {
      "type": "array",
      "items": { "type": "string" },
      "description": "2-6 decisions made this session that will affect future sessions. Choices and conclusions, not tactical steps.",
      "required": true,
      "min_items": 0,
      "max_items": 6
    },
    "corrections": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Factual errors caught and corrected, or misunderstandings resolved this session",
      "required": false
    },
    "new_knowledge": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Things discovered this session — patterns, constraints, user preferences, architectural insights",
      "required": false
    },
    "open_threads": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Unresolved questions or tasks explicitly left for a future session",
      "required": false
    },
    "narrative": {
      "type": "string",
      "description": "100-300 word plain-language summary — what happened, why it mattered, what changed. Written as if briefing a colleague who missed the session.",
      "required": true,
      "min_words": 100,
      "max_words": 300
    }
  },
  "quality_gate": {
    "required_non_empty": ["primary_topic", "narrative"],
    "at_least_one_non_empty": ["key_decisions", "new_knowledge", "open_threads"],
    "narrative_word_range": [100, 300]
  },
  "notes": [
    "Never include PII, credentials, or confidential data in session summaries",
    "Corrections and new_knowledge are optional but highly valuable for the compounding loop",
    "This schema is the content — the vault-entry envelope adds metadata like entry_id, plugin, and timestamp"
  ]
}
```

---

### `plugin-identity`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "plugin-identity-schema",
  "title": "Olytic Plugin Identity",
  "description": "Canonical schema for the fields that make a plugin uniquely identifiable in the Olytic ecosystem. These fields appear in plugin.json, workspace.json, and the marketplace registry.",
  "version": "1.0.0",
  "owner": "aule",
  "properties": {
    "name": {
      "type": "string",
      "pattern": "^[a-z0-9-]+$",
      "description": "Kebab-case plugin name — unique across the Olytic plugin catalog",
      "required": true,
      "max_length": 60
    },
    "version": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$",
      "description": "Semver version string",
      "required": true
    },
    "description": {
      "type": "string",
      "description": "One sentence, under 120 characters",
      "required": true,
      "max_length": 120
    },
    "author": {
      "type": "object",
      "required": true,
      "properties": {
        "name": { "type": "string", "required": true },
        "email": { "type": "string", "format": "email", "required": true }
      }
    },
    "keywords": {
      "type": "array",
      "items": { "type": "string" },
      "description": "3-6 terms describing the plugin domain",
      "min_items": 1,
      "max_items": 10
    },
    "connectors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string", "required": true },
          "required": { "type": "boolean", "required": true },
          "scopes": { "type": "array", "items": { "type": "string" } }
        }
      },
      "description": "External integration declarations. Omit if plugin is standalone."
    },
    "hooks": {
      "type": "string",
      "description": "Relative path to hooks.json file (e.g., 'hooks/hooks.json')"
    }
  },
  "validation_rules": [
    "name must be unique across the workspace",
    "connectors declared here must be available in workspace.json providers",
    "version must increment on every release — downgrades are rejected"
  ],
  "notes": [
    "Valid plugin.json keys: name, version, description, author, keywords, hooks, connectors — all others cause upload failure"
  ]
}
```

---

### `hook-event`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "hook-event-schema",
  "title": "Olytic Hook Event",
  "description": "Canonical schema for Claude hook events that trigger Aule's automated behaviors. Hooks are declared in hooks.json and fire on system lifecycle events.",
  "version": "1.0.0",
  "owner": "aule",
  "hook_types": {
    "PostToolUse": {
      "description": "Fires after any Write or Edit tool call completes. Used by aule-change-analyzer.",
      "payload": {
        "tool_name": "string — name of the tool that was called",
        "file_path": "string — path of the file that was written or edited"
      }
    },
    "UserPromptSubmit": {
      "description": "Fires when the user submits a prompt. Used for intent detection.",
      "payload": {
        "prompt": "string — the user's prompt text"
      }
    },
    "SessionClose": {
      "description": "Fires when a session ends. Used by aule-session-summarizer.",
      "payload": {
        "session_id": "string — the session identifier",
        "timestamp": "string — ISO 8601 UTC timestamp of session close"
      }
    },
    "PreToolUse": {
      "description": "Fires before a tool is called. Used for pre-execution validation.",
      "payload": {
        "tool_name": "string — name of the tool about to be called",
        "tool_input": "object — the input that will be passed to the tool"
      }
    }
  },
  "hook_entry_schema": {
    "matcher": { "type": "string", "description": "Regex pattern to match against trigger context", "required": true },
    "hooks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": { "type": "string", "enum": ["prompt", "command"], "required": true },
          "prompt": { "type": "string", "required_when": "type === 'prompt'" },
          "timeout": { "type": "integer", "default": 10 },
          "decision": { "type": "string", "enum": ["approve", "block", "approve|skip"] }
        }
      }
    }
  },
  "notes": [
    "Hooks are declared in the plugin's hooks.json file, referenced by plugin.json via the 'hooks' field",
    "Hook prompts are injected instructions — they run in Claude's context, not as separate processes"
  ]
}
```

---

### `memory-access`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "memory-access-schema",
  "title": "Olytic Memory Access Control",
  "description": "Canonical schema for declaring who and what can read a plugin's vault-stored data. Every plugin that writes persistent data to the vault must include a memory access declaration.",
  "version": "1.0.0",
  "owner": "aule",
  "properties": {
    "plugin": {
      "type": "string",
      "description": "The plugin ID whose vault data this declaration governs",
      "required": true
    },
    "access_control": {
      "type": "string",
      "enum": ["private", "shared", "org-wide"],
      "description": "Who can read this plugin's vault data. private = this plugin only; shared = named list; org-wide = any plugin in the org",
      "required": true,
      "default": "private"
    },
    "authorized_readers": {
      "type": "array",
      "items": { "type": "string" },
      "description": "If access_control = 'shared', the list of plugin IDs authorized to read. Required when access_control = 'shared'.",
      "required_when": "access_control === 'shared'"
    },
    "access_justification": {
      "type": "string",
      "description": "Why broader-than-private access is needed. Required when access_control is 'shared' or 'org-wide'.",
      "required_when": "access_control !== 'private'"
    },
    "data_lifecycle": {
      "type": "object",
      "properties": {
        "retention_days": {
          "type": "integer",
          "description": "Days vault entries are retained before purge. Null = indefinite.",
          "nullable": true
        },
        "purge_on_plugin_removal": {
          "type": "boolean",
          "default": true
        }
      }
    }
  },
  "defaults": {
    "access_control": "private",
    "authorized_readers": [],
    "data_lifecycle": {
      "retention_days": 90,
      "purge_on_plugin_removal": true
    }
  },
  "notes": [
    "Access defaults to 'private' if this declaration is absent",
    "org-wide access requires explicit business justification",
    "authorized_readers must list plugin IDs (kebab-case), not user IDs"
  ]
}
```
