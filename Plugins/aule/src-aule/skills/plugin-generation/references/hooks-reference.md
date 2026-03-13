# Hooks Reference

Claude plugins support four hook event types. This reference defines each event, its use cases, and the registration format. Read this file when generating or validating hook declarations in any plugin.

---

## Hook Architecture

Hooks are declared in `hooks/hooks.json` at the root of the plugin source folder. The platform fires hooks automatically when the matching event occurs — no user action required.

Hooks are listed in `plugin.json` via the `hooks` field:
```json
"hooks": "hooks/hooks.json"
```

---

## The Four Hook Events

### 1. PostToolUse

**Fires after:** Any tool call completes (Write, Edit, Read, Bash, etc.)

**Use when:**
- A file write should trigger an automatic downstream action
- You want to repackage, re-analyze, or re-validate after a mutation
- A standard file changes and other files need updating

**Don't use when:**
- You need to intercept a tool call *before* it runs (use PreToolUse)
- You want to respond to user input (use UserPromptSubmit)

**Matcher:** Regex matched against the tool name that just ran. Common patterns:
- `"Write|Edit"` — fires after any file write or edit
- `"Write"` — fires after file writes only
- `"Bash"` — fires after any bash command

**Example:**
```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "A file was just written. Check if [condition]. If yes, invoke [skill].",
          "timeout": 20
        }
      ]
    }
  ]
}
```

---

### 2. UserPromptSubmit

**Fires when:** The user submits a message to Claude

**Use when:**
- A specific phrase or keyword should automatically route to a skill
- You want to detect intent and pre-invoke a skill before Claude responds
- You need to provide guardrails for certain user actions

**Don't use when:**
- You want to respond to file changes (use PostToolUse)
- You want to capture session end (use SessionClose)

**Matcher:** Regex matched against the full user message text. Design matchers to be specific — overly broad matchers cause false triggers.

**Example:**
```json
{
  "UserPromptSubmit": [
    {
      "matcher": "run.*audit|audit.*all|check.*compliance",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "The user wants to run a compliance audit. Invoke aule-verifier immediately.",
          "timeout": 10,
          "decision": "approve|skip"
        }
      ]
    }
  ]
}
```

**The `decision` field:** Optional. When set to `"approve|skip"`, Claude decides whether to fire the hook based on context. When omitted, the hook always fires on match.

---

### 3. SessionClose

**Fires when:** The user closes or ends the session

**Use when:**
- Capturing episodic memory (session summaries for persistent-memory plugins)
- Running end-of-session cleanup or log flush
- Emitting lifecycle telemetry on session completion

**Don't use when:**
- The plugin has `memory_scope: ephemeral` — no session summary needed
- The plugin is stateless (pure read/write tool, no context to preserve)

**Matcher:** Use `".*"` — SessionClose should fire on every session end, not selectively.

**Required timeout:** ≥30 seconds (vault writes take time)

**Example:**
```json
{
  "SessionClose": [
    {
      "matcher": ".*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "The session is closing. Invoke the [plugin-name]-session-summarizer skill.",
          "timeout": 30
        }
      ]
    }
  ]
}
```

**Generation rule:** Only add SessionClose hook to plugins with `memory_scope: persistent`. See `anti-drift-protocols.md` for the full SessionClose hook pattern.

---

### 4. PreToolUse

**Fires before:** A tool call executes

**Use when:**
- You need to validate or gate a destructive operation before it runs
- You want to add a confirmation step before writes to critical files
- You need to log or audit what's about to happen

**Don't use when:**
- You want to react to something that already happened (use PostToolUse)
- The overhead of a pre-check is not justified by the risk

**Matcher:** Regex matched against the tool name about to run.

**Example:**
```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "A bash command is about to run. If it contains 'rm -rf' or 'delete', ask the user to confirm before proceeding.",
          "timeout": 10,
          "decision": "approve|skip"
        }
      ]
    }
  ]
}
```

---

## Natural Language Routing Pattern

Hooks work best when paired with the Natural Language Routing pattern. Instead of writing complex logic in the hook prompt, route to a named skill and let that skill handle the logic:

**❌ Complex inline logic (avoid):**
```json
"prompt": "A file was just written. If the path contains 'skills/plugin-generation' and the content contains 'MUST', then update SKILL.md, then invoke trashbot, then log a Category 1 change..."
```

**✅ Route to a skill (preferred):**
```json
"prompt": "A file was just written at [path]. Invoke the aule-change-analyzer skill to categorize the change and route it appropriately."
```

This keeps hook prompts simple and readable, while keeping logic encapsulated in skills.

---

## Trigger Phrase Rules

For `UserPromptSubmit` hooks, follow these rules when designing matchers:

1. **Use pipe-separated alternatives:** `"sync|update|refresh"` rather than a single word
2. **Include common variations:** `"run.*verify|verify.*plugin|check.*compliance"`
3. **Avoid single common words** — `"check"` or `"update"` will match too broadly
4. **Test with real user phrases:** Write matchers based on how users actually talk, not how developers think
5. **3–5 phrase fragments** is usually enough to cover the natural language space for a given intent

---

## Hook Registration Format

Full `hooks.json` schema (read `olytic-core/contracts/schemas/hook-event-schema.json` for the authoritative structure):

```json
{
  "PostToolUse": [
    {
      "matcher": "<regex string>",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "<instruction to Claude>",
          "timeout": <seconds — integer>,
          "decision": "approve|skip"   ← optional
        }
      ]
    }
  ],
  "UserPromptSubmit": [ ... ],
  "SessionClose": [ ... ],
  "PreToolUse": [ ... ]
}
```

**Field rules:**
- `matcher`: Required. Valid regex. Test before deploying.
- `type`: Always `"prompt"` for current hook implementations
- `prompt`: Required. The instruction Claude receives when the hook fires.
- `timeout`: Required. Seconds Claude has to execute the hook action. Minimum 10, use 30 for vault writes.
- `decision`: Optional. `"approve|skip"` means Claude may decide not to fire based on context.

---

## Reference Relationships

This file is read by:
- `plugin-generation/SKILL.md` — to generate correct `hooks.json` for new plugins
- `plugin-discovery/SKILL.md` — during Q5/Q6 discovery to explain hook capabilities
- `aule-change-analyzer/SKILL.md` — for hook-type routing decisions

For the hook-event data shape, see: `olytic-core/contracts/schemas/hook-event-schema.json`
