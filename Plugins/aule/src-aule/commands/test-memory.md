---
description: Test the Olytic memory and telemetry pipeline end-to-end — fetch vault entries, write a test event, and confirm both connectors are live.
argument-hint: "[--read | --write] (default: run all three checks)"
---

# test-memory

Explicitly exercises the Olytic memory and telemetry pipeline so you can confirm both read and write paths are live and connected.

## Usage

```
test-memory          → run full read + write diagnostic
test-memory --read   → test memory read only (fetch vault)
test-memory --write  → test telemetry write only (send event)
```

## What This Command Does

### 1. Memory Read (Olytic Gateway — `read_vault_entries`)

Call the **`read_vault_entries`** tool via the `Olytic Gateway` MCP connector:

```
Tool: read_vault_entries  (Olytic Gateway MCP server)

{
  "plugin": "aule",
  "limit": 3
}
```

Report:
- ✅ **Read OK** — Show the count of entries returned and the `primary_topic` of the most recent one (if present)
- ❌ **Read FAILED** — Show the error or connector-absent message

### 2. Telemetry Write (Olytic telemetry gateway — `log_telemetry`)

Call the **`log_telemetry`** tool via the `Olytic telemetry gateway` MCP connector:

```
Tool: log_telemetry  (Olytic telemetry gateway MCP server)

{
  "timestamp": "[current UTC ISO 8601]",
  "event": "skill_invoke",
  "plugin": "aule",
  "plugin_version": "[current plugin version from plugin.json]",
  "platform": "claude",
  "component": "test-memory",
  "trigger": "user invoked /test-memory diagnostic command"
}
```

Report:
- ✅ **Write OK** — Confirm the event was accepted
- ❌ **Write FAILED** — Show the error or connector-absent message

### 3. Memory Write (Olytic Gateway — `write_vault_entry`)

Construct a minimal test vault entry using the canonical `vault-entry` schema (fetched at runtime via `olytic-core-schemas`), then call **`write_vault_entry`**:

```
Tool: write_vault_entry  (Olytic Gateway MCP server)

{
  "entry_id": "[generate a fresh UUID]",
  "plugin": "aule",
  "plugin_version": "[current plugin version]",
  "session_timestamp": "[current UTC ISO 8601]",
  "entry_type": "session_summary",
  "loop": "plugin",
  "platform": "claude",
  "schema_version": "1.2.0",
  "content": {
    "primary_topic": "test-memory diagnostic — pipeline check",
    "key_decisions": [],
    "corrections": [],
    "new_knowledge": [],
    "open_threads": [],
    "narrative": "This is a synthetic test entry written by the test-memory diagnostic command to confirm the vault write path is live and connected."
  }
}
```

Report:
- ✅ **Vault Write OK** — Confirm the entry was accepted
- ❌ **Vault Write FAILED** — Show the error or connector-absent message

## Output Format

Present a clear, human-readable diagnostic report after all calls complete:

```
Memory & Telemetry Diagnostic — [timestamp]

Read  (Olytic Gateway / read_vault_entries):   ✅ OK  — 3 entries returned, latest: "[primary_topic]"
Write (Olytic telemetry gateway / log_telemetry): ✅ OK  — event accepted
Vault (Olytic Gateway / write_vault_entry):    ✅ OK  — test entry written

All 3 paths are live. ✅
```

If any path fails, show the error in place of the status message and summarize at the bottom:

```
1/3 paths failed. Check that the Olytic Gateway MCP connector is installed and authenticated.
```

## Notes

- This command is for diagnostics only — it is safe to run at any time
- The test vault entry written is real and will persist in the vault; it is clearly labeled as a diagnostic entry via `primary_topic`
- `client_id`, `user_id`, and `org_id` are never included in payloads — the MCP servers resolve them server-side
- If either connector is absent (not installed for the org), report connector-absent rather than an error
- Telemetry: This command logs its own invocation via aule-telemetry
