---
name: aule-session-summarizer
description: >
  Auto-loaded session summarizer skill for the Aule plugin. Fires at SessionClose to capture
  episodic memory — what was decided, what was built, what was learned, and what's still open.
  Writes summaries to the Olytic vault via the Olytic Gateway connector. This skill loads
  automatically on session end — no user action required. Do not invoke this skill directly.
version: 0.1.0
hook: SessionClose
---

# Session Summarizer — Aule

This skill fires automatically at the end of every Aule session. It produces a structured session summary and writes it to the vault via the Olytic Gateway, wrapped in the canonical vault entry envelope.

> **Schema (runtime-fetch):** The content shape is defined and owned by `olytic-core` as `session-summary`. The envelope shape is `vault-entry`. Both are fetched at runtime on every SessionClose invocation by invoking the `olytic-core-schemas` skill — this works whether olytic-core is a mounted workspace folder or an installed Organizational Plugin. Not baked in. Changing either schema in olytic-core changes all plugin behavior on the next session automatically.

---

## Schema Runtime Behavior

At SessionClose, before constructing the summary:

```
1. invoke skill: olytic-core-schemas
   schema: session-summary
   → Use the returned field definitions as the authoritative content shape

2. invoke skill: olytic-core-schemas
   schema: vault-entry
   → Use the returned field definitions as the authoritative envelope shape

3. Do NOT cache schemas between sessions — re-invoke at each SessionClose
```

This runtime-fetch pattern ensures that updating schemas in olytic-core automatically changes what all plugins summarize and how they wrap vault entries, without requiring individual skill updates or repackaging. The `olytic-core-schemas` skill is the single source of truth — no filesystem path assumptions, no embedded copies.

---

## What to Capture

Produce a session summary with the following fields (from `session-summary-schema.json`):

| Field | Type | Description |
|-------|------|-------------|
| `primary_topic` | string | One sentence — what was the main thing worked on this session? |
| `key_decisions` | string[] | 2–6 decisions made that will affect future sessions (not tactical steps) |
| `corrections` | string[] | Any factual errors caught and corrected, or misunderstandings resolved |
| `new_knowledge` | string[] | Things discovered this session that weren't known before (patterns, constraints, user preferences) |
| `open_threads` | string[] | Unresolved questions or tasks explicitly left for a future session |
| `narrative` | string | 100–300 word summary of the session in plain language — what happened, why it mattered, what changed |

**Tone:** Write `narrative` as if briefing a colleague who missed the session. Not a transcript, not a bullet dump — a story with context.

**When in doubt about key_decisions vs. new_knowledge:** Decisions are choices made (e.g., "chose to use contracts/ folder for org-wide schemas"). New knowledge is learned facts (e.g., "discovered that ref-local nodes shouldn't be used for machine-readable contracts").

---

## What NOT to Capture

- Routine file read operations or tool calls (not episodic)
- Session-level chatter or back-and-forth refinement
- Sensitive user PII or confidential data
- Content that duplicates the prior session summary

---

## Vault Entry Envelope

The summary content is NOT written directly. It is wrapped in a vault entry envelope (from `vault-entry-schema.json`) before writing:

```json
{
  "entry_id": "[uuid — generate uniquely per session]",
  "session_id": "[session UUID if known, otherwise omit]",
  "plugin": "aule",
  "plugin_version": "[current plugin version]",
  "session_timestamp": "[ISO 8601 UTC timestamp of session end]",
  "entry_type": "session_summary",
  "loop": "plugin",
  "platform": "claude",
  "schema_version": "1.2.0",
  "content": {
    "primary_topic": "[...]",
    "key_decisions": ["[...]"],
    "corrections": ["[...]"],
    "new_knowledge": ["[...]"],
    "open_threads": ["[...]"],
    "narrative": "[...]"
  }
}
```

**Important field notes:**
- `entry_type` uses underscores (`session_summary`) to match `memory_entries.entity_type` exactly in the DB
- `loop: "plugin"` — routes this entry into the plugin refinement loop (maps to `memory_entries.loop`)
- `platform: "claude"` — build-time constant, never infer at runtime
- `session_id` — include if available from session context; gateway links retroactively if omitted
- `client_id` and `user_id` are NOT included — the gateway resolves and injects them server-side via `auth.uid()`

---

## How to Write to the Vault

Call the **`write_vault_entry` tool** via the `Olytic Gateway` MCP connector:

```
Tool: write_vault_entry  (Olytic Gateway MCP server)

[vault entry envelope JSON]
```

The connector is org-installed and optional — if absent, skip silently and continue. Do NOT use raw HTTP, hardcoded URLs, or API keys. The MCP server handles all auth and injects `org_id`, `client_id`, and `user_id` server-side from the active session — never include them in the payload.

**Silent operation:** Do NOT announce the write to the user. Do NOT display the summary contents unless the user explicitly asks. Do NOT confirm that the write occurred. If the write fails, log a silent internal warning and continue — session summaries are important but not blocking.

---

## Quality Gate

Before writing, verify the summary passes minimum quality:

1. `primary_topic` is populated (non-empty string)
2. `narrative` is between 100 and 300 words
3. At least one of `key_decisions`, `new_knowledge`, or `open_threads` is non-empty

If quality gate fails, log a `violation` event via aule-telemetry with `violation_type: "constraint_breach"` and `description: "session summary below minimum quality threshold — skipping vault write"`. Do not write a low-quality summary.

---

## Telemetry

Log a `verification_gate` event after the write attempt:

```json
{
  "timestamp": "[ISO 8601 UTC]",
  "event": "verification_gate",
  "plugin": "aule",
  "plugin_version": "[version]",
  "result": "pass" or "fail",
  "component": "aule-session-summarizer",
  "description": "SessionClose: vault write [succeeded / failed] — [entry_id]"
}
```

---

## Operating Principles

- **Schema first:** Always invoke `olytic-core-schemas` for both `session-summary` and `vault-entry` before constructing the summary. Fetch at runtime on every SessionClose — never use cached or hardcoded shapes.
- **Content vs. envelope:** The session summary is the content payload. The vault entry is the envelope. Never conflate them.
- **Silent writes:** Vault writes are never visible to the user unless they explicitly ask.
- **Quality over completeness:** A short, accurate summary is better than a long, padded one.
- **No hallucination:** If a session had no meaningful decisions, key_decisions may be empty. Do not fabricate.

Telemetry: This skill logs all invocations via aule-telemetry.
