---
name: telemetry-testing
description: >
  Use this skill to test, verify, or troubleshoot the telemetry pipeline: "test if telemetry is working",
  "why isn't telemetry logging", "run the smoke test", "check if rows are landing in Supabase",
  "troubleshoot the MCP connector", "verify the telemetry pipeline end-to-end", "is the connector
  connected", "audit plugin compliance with v2.2.0", "why is org_id missing", "diagnose telemetry failure",
  or "walk me through the troubleshooting steps".
version: 0.1.0
telemetry_blueprint: "shared/telemetry-blueprint/TELEMETRY-STANDARDS.md v2.2.0"
source_of_truth: "telemetry-blueprint/TELEMETRY-TESTING.md"
---

# Telemetry Testing & Troubleshooting

**Source of truth for this skill:** `olytic-plugins/telemetry-blueprint/TELEMETRY-TESTING.md`

This skill is Gaudi's operational arm for verifying, diagnosing, and fixing the telemetry pipeline. It does not redesign the pipeline — it tests and troubleshoots what exists against the architecture defined in `TELEMETRY-ARCHITECTURE.md`.

## Before You Start

Read the full testing document before attempting any diagnosis:

```
olytic-plugins/telemetry-blueprint/TELEMETRY-TESTING.md
```

That document contains the authoritative five-layer testing model, all SQL queries, the full smoke test sequence, the troubleshooting decision tree, and the plugin compliance audit table. This skill references it — it does not duplicate it.

If the testing document can't be found, report "Not Found" immediately. Do not guess at SQL queries or test procedures from memory.

## Core Mental Model

The telemetry pipeline is a five-layer stack. **Always test bottom-up.** A failure at any lower layer makes everything above it meaningless to test.

```
Layer 5 │  Plugin Skill Behavior         ← Did the right row appear when a skill fired?
Layer 4 │  MCP Connector Discovery       ← Can Claude find mcp__olytic-telemetry__execute_sql?
Layer 3 │  MCP Connector Health          ← Is the connector "Connected" in Claude Desktop?
Layer 2 │  Supabase RLS + Schema         ← Does the table exist? Do INSERTs pass the RLS policy?
Layer 1 │  Supabase Database Reachability ← Is the project active and reachable at all?
```

When a user says "telemetry isn't working," always start by asking: "Which layer are we at?" If they don't know, start at Layer 1 and work up.

## What "Verified" Means

Due to the Gaudi global connector confusion (Known Issue 4 in the architecture doc), be precise about what counts as proof that the pipeline works:

| Signal | Does It Prove End-to-End? |
|--------|--------------------------|
| A row appeared in Supabase | Only if it came via `mcp__olytic-telemetry__execute_sql` |
| Gaudi inserted a row directly | No — need to confirm which tool was used |
| Direct INSERT from Supabase SQL Editor worked | No — bypasses the MCP connector entirely |
| Skill fired → row appeared with `org_id = 'olytic-internal'` via correct connector | ✅ Yes |

Never tell a user "telemetry is working" based only on rows appearing in Supabase. Always confirm the connector identity.

## Operational Approach

### When a user asks to test telemetry

1. Read `TELEMETRY-TESTING.md` to confirm the current smoke test procedure
2. Start at Layer 1 — run `SELECT NOW()` via the MCP connector
3. Work up the stack layer by layer
4. At Layer 4, explicitly ask Claude to name which tool it used for the INSERT
5. At Layer 5, verify `org_id` is present and correct on resulting rows
6. Report pass/fail at each layer before proceeding

### When a user reports a specific error

1. Read `TELEMETRY-TESTING.md` — check the "Common Error Messages and Fixes" table
2. Match the symptom to the most likely cause
3. Direct the user to the fix and then re-test the affected layer
4. Log the resolution in the known issues section of `TELEMETRY-ARCHITECTURE.md` if it resolves a documented open issue

### When a user asks for a plugin compliance audit

1. Read `TELEMETRY-TESTING.md` — check the "Plugin Compliance Audit" section
2. Check the compliance audit table for the plugin in question
3. If status is "Audit needed," open the plugin's `skills/plugin-telemetry/SKILL.md` (or `skills/gaudi-telemetry/SKILL.md` for Gaudi) and verify:
   - Frontmatter declares `telemetry_blueprint: "TELEMETRY-STANDARDS.md v2.2.0"`
   - INSERT examples include `org_id` and `user_id` columns
   - `org_id` value is hardcoded as `'olytic-internal'` for internal plugins
4. Update the compliance audit table with the result
5. If non-compliant, update the plugin's telemetry skill INSERT pattern and repackage

### When a user resolves a known issue

1. Update the status in `TELEMETRY-ARCHITECTURE.md` under the relevant issue
2. Update or remove the row from the "Common Error Messages and Fixes" table in `TELEMETRY-TESTING.md`
3. Update the plugin compliance audit table if relevant

## Key Reference Locations

| What you need | Where to find it |
|---------------|-----------------|
| Full five-layer test procedure + SQL | `TELEMETRY-TESTING.md` |
| Six-step smoke test sequence | `TELEMETRY-TESTING.md` → "Smoke Test" section |
| Troubleshooting decision tree | `TELEMETRY-TESTING.md` → "Troubleshooting Decision Tree" |
| Plugin compliance audit table | `TELEMETRY-TESTING.md` → "Plugin Compliance Audit" |
| Known issues and open problems | `TELEMETRY-ARCHITECTURE.md` → "Known Issues" |
| MCP connector config and setup | `olytic-internal-connector-setup.md` |
| Claude desktop config options | `claude_desktop_config_options.md` |
| Connector flag mismatch fix | `troubleshoot-mcp-connector.md` |
| Telemetry standard (canonical) | `TELEMETRY-STANDARDS.md` |

All files are in: `olytic-plugins/telemetry-blueprint/`

## Boundaries

This skill should NOT be used for:

- **Redesigning the telemetry architecture** — use `TELEMETRY-ARCHITECTURE.md` and Gaudi's solution-design agent for architectural changes
- **Changing the telemetry blueprint** — Aulë owns the blueprint; update `TELEMETRY-STANDARDS.md` through Aulë
- **Writing new plugin skills from scratch** — use Aulë's plugin-generation skill
- **Diagnosing non-telemetry issues** — if the problem is with plugin behavior unrelated to logging, use the relevant plugin's own skill

If a request falls outside these boundaries, redirect to the appropriate skill or plugin.

## Operating Principles

- **Source of truth first.** Always read `TELEMETRY-TESTING.md` before advising. Never advise from memory alone.
- **Bottom-up always.** Never skip layers. A Layer 4 fix won't matter if Layer 2 is broken.
- **Name the tool.** When Claude runs an INSERT, always confirm which `execute_sql` tool was used. This is the single most important diagnostic signal.
- **No hallucination.** If a SQL query isn't in the testing document, don't invent one. Report "Not in testing doc — check TELEMETRY-STANDARDS.md or confirm with user."
- **Update the living docs.** When issues are resolved or new failure modes are discovered, update `TELEMETRY-ARCHITECTURE.md` and `TELEMETRY-TESTING.md`. These are the source of truth, not this conversation.
- **Verify after fixing.** After applying any fix, re-run the relevant layer test to confirm the fix worked before closing the issue.

---

Telemetry: This skill logs all invocations via gaudi-telemetry.
