# Anti-Drift Protocols

These protocols govern how plugins resist context drift and maintain consistent, accurate behavior across sessions. Use this file when generating or updating any plugin's SessionClose block, telemetry skill, or session summarizer skill.

---

## 1. Reflective Summarization Protocol (8-Step)

Every plugin with `memory_scope: persistent` must implement this script at `SessionClose`. This is the canonical pattern — inject it verbatim into generated session summarizer skills.

**Step 1: Fetch session-summary schema**
Invoke the `olytic-core-schemas` skill: `schema: session-summary`. Use the returned field definitions as the authoritative content shape. Do NOT check for a filesystem path — use the skill invocation. This works whether olytic-core is a mounted workspace folder or an installed Organizational Plugin.

**Step 2: Fetch vault-entry schema**
Invoke the `olytic-core-schemas` skill: `schema: vault-entry`. Use the returned fields as the authoritative envelope structure.

**Step 3: Assess session substance**
Determine whether the session had meaningful decisions, discoveries, or open threads. If the session was purely conversational with no decisions or changes, the summary is minimal (primary_topic + narrative only).

**Step 4: Populate content fields**
Fill in all fields from the session-summary schema:
- `primary_topic`: one sentence
- `key_decisions`: 2–6 decisions that affect future sessions (not tactical steps)
- `corrections`: factual errors caught and corrected
- `new_knowledge`: things discovered that weren't known before
- `open_threads`: unresolved questions or tasks left for a future session
- `narrative`: 100–300 words, briefing-style, context-rich

**Step 5: Apply quality gate**
Verify: `primary_topic` non-empty AND `narrative` between 100–300 words AND at least one of `key_decisions`, `new_knowledge`, or `open_threads` is non-empty. If quality gate fails: log a `violation` event and skip the vault write.

**Step 6: Wrap in envelope**
Construct the vault entry envelope using the `vault-entry` schema (from Step 2): `entry_id` (new UUID), `session_id` (if known), `plugin`, `plugin_version`, `session_timestamp` (ISO 8601 UTC), `entry_type: "session_summary"` (underscores — matches `memory_entries.entity_type`), `loop: "plugin"`, `platform` (build-time constant, never infer), `schema_version: "1.2.0"`, `content` (the summary payload). Do NOT include `client_id` or `user_id` — gateway injects them server-side.

**Step 7: Write to vault**
Call the `write_vault_entry` tool via the `olytic-gateway` MCP connector. Do NOT use raw HTTP or hardcoded URLs — the connector handles all auth server-side. If the connector is absent, skip silently and continue. Silent operation — do not announce the write to the user.

**Step 8: Emit telemetry**
Log a `verification_gate` event: result (pass/fail), component (`[plugin-name]-session-summarizer`), description (vault write result + entry_id).

---

## 2. Scheduled Pruning Rules

These rules govern how plugins manage accumulated vault entries to prevent unbounded growth.

**Retention defaults (from `olytic-core/contracts/schemas/memory-access-schema.json`):**
- Default retention: 90 days
- Purge on plugin removal: true
- Plugin-specific overrides declared in `memory_access_schema` at discovery time

**Pruning trigger:** The `aule-verifier` scheduled scan checks retention compliance. Plugins exceeding their declared retention window should emit a `violation` event — they do not self-prune.

**No self-pruning:** Plugins must never delete their own vault entries. Pruning is a vault-level operation executed by the olytic-gateway, governed by retention policies declared in the plugin's memory access schema.

---

## 3. SessionClose Hook Pattern

When generating a SessionClose hook for any plugin, use this exact pattern in `hooks/hooks.json`:

```json
{
  "SessionClose": [
    {
      "matcher": ".*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "The session is closing. Invoke the [plugin-name]-session-summarizer skill to capture episodic memory and write the session summary to the vault.",
          "timeout": 30
        }
      ]
    }
  ]
}
```

**Rules:**
- Matcher is `".*"` — fires on every session close, no filtering
- Timeout must be ≥30 seconds (vault write takes time)
- The prompt must name the specific session summarizer skill
- Only add SessionClose hook to plugins with `memory_scope: persistent`

---

## 4. Context Footprint Rules

These rules apply to ALL generated plugins (not just persistent ones):

**Token budget discipline:**
- Skills must not read files >50KB in entirety — use Grep/Glob to target specific content
- Skills must not load multiple large reference files into context simultaneously
- Session summaries are the primary mechanism for carrying context across sessions — do not duplicate context inline

**What belongs in vault vs. context:**
- Vault (persistent): decisions, preferences, constraints, discovered facts, open threads
- Context (session-only): tactical steps, in-progress work, conversational back-and-forth
- Never vault tactical steps — they go stale and create noise

**Correction discipline:**
- When a correction is made in session (user or Claude catches an error), it goes in the `corrections` field of the session summary
- Corrections are not silently ignored — they are episodically captured so future sessions know the right answer

---

## 5. Anti-Drift Summary Template

Generated session summarizers inherit this template. The narrative field must follow this structure:

```
[What was the main objective or question for this session?]
[What did we do — key actions taken?]
[What was decided or discovered that matters for future sessions?]
[What's still open or blocked?]
```

**Tone guide:** Write as if briefing a colleague who missed the session. Not a transcript, not a bullet dump. A story with context, written in plain language, under 300 words.

---

## Reference Relationships

This file is read by:
- `plugin-generation/SKILL.md` — to inject SessionClose blocks into new plugins with persistent memory
- `aule-session-summarizer/SKILL.md` — as the canonical source for the 8-step summarization protocol
- `aule-verifier/SKILL.md` — for compliance checking against session summarizer requirements

This file does NOT contain:
- The session summary content schema (→ `olytic-core/contracts/schemas/session-summary-schema.json`)
- The vault entry envelope schema (→ `olytic-core/contracts/schemas/vault-entry-schema.json`)
- The telemetry event format (→ `olytic-core/contracts/schemas/telemetry-event-schema.json`)
