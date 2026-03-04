---
name: telemetry-diagnostic
description: >
  Active telemetry pipeline diagnostic. Analyzes the current session to determine whether a skill should have sent telemetry, then runs live layer-by-layer tests to find exactly where the pipeline broke and what to fix. Works without any files mounted.
version: 1.0.0
telemetry_blueprint: "shared/telemetry-blueprint/TELEMETRY-STANDARDS.md v2.2.0"
requires_mounted_folder: false
---

# Telemetry Diagnostic — Active Pipeline Troubleshooter

This skill runs live diagnostics to determine why telemetry data did not reach Supabase after a skill invocation. It is fully self-contained — all architecture knowledge is embedded here. No files need to be mounted.

**When to use this skill:**
- A skill ran in this session or a previous session but no row appeared in Supabase
- You want to verify whether the pipeline is working after a config change
- You are setting up the connector on a new machine

---

## Architecture Reference (Embedded)

The telemetry pipeline is a five-layer stack. Data must pass through every layer.

```
Layer 5 │  Plugin Skill Behavior
         │  Did the telemetry skill actually fire and attempt an INSERT?
         │
Layer 4 │  MCP Connector Discovery
         │  Can Claude find mcp__olytic-telemetry__execute_sql in this session?
         │
Layer 3 │  MCP Connector Health
         │  Is the connector installed and showing Connected in Claude Desktop?
         │
Layer 2 │  Supabase RLS + Schema
         │  Does the table exist? Do INSERTs pass the org_id RLS check?
         │
Layer 1 │  Supabase Database Reachability
         │  Is the Supabase project active and reachable?
```

**Key facts embedded for reference (no files needed):**
- Supabase project ref: `kxnmgutidehncnafrwbu`
- Supabase dashboard: `https://supabase.com/dashboard/project/kxnmgutidehncnafrwbu`
- Target table: `telemetry_events`
- Required connector tool name: `mcp__olytic-telemetry__execute_sql`
- Required org_id for Olytic internal: `olytic-internal`
- Required user_id for Olytic internal: `support@olyticsolutions.com`
- MCP connector config file (on Mac): `~/Library/Application Support/Claude/claude_desktop_config.json`
- Config uses package: `@supabase/mcp-server-supabase@latest`
- Standard config flag: `--supabase-access-token` (fallback: `--access-token`)

**What counts as a real telemetry row (not a false positive):**
- Row was inserted via `mcp__olytic-telemetry__execute_sql` (NOT a different Supabase tool)
- Row has `org_id = 'olytic-internal'` (NOT null, NOT a different value)
- Row has a non-null `user_id`

---

## Step 0: Identify What Should Have Been Logged

**Before running any live tests, establish what we're looking for.**

Scan the current conversation (or the conversation the user describes) and answer:

1. **Which plugin was active?** (Gaudi, The One Ring, Magneto, Aulë, or other)
2. **Which skill was invoked?** (e.g., `data-modeling`, `brand-check`, `linkedin-post`)
3. **What event type should have fired?** Use this mapping:
   - Skill loaded via `/skill-name` → `skill_invoke`
   - Agent activated → `agent_trigger`
   - Slash command run → `command_execute`
   - User request violated a constraint → `violation`
   - User gave explicit positive/negative feedback → `feedback`
4. **What `component` value should the row have?** (The skill directory name, e.g., `data-modeling`)
5. **Approximately when?** (Timestamp range to search in Supabase)

State your findings explicitly before proceeding:

> "Based on what I can see: plugin = [X], component = [Y], event_type = [Z], approximate time = [T]. I'll now search Supabase for a matching row, then run layer tests if none is found."

---

## Step 1: Search for the Missing Row

Before declaring the pipeline broken, confirm the row is actually missing. Run this via `mcp__olytic-telemetry__execute_sql`:

```sql
SELECT id, timestamp, event, plugin, plugin_version, org_id, user_id, component, trigger
FROM telemetry_events
WHERE org_id = 'olytic-internal'
ORDER BY created_at DESC
LIMIT 10;
```

**Interpret the result:**

| What you see | What it means |
|---|---|
| A row with matching plugin + component + correct timestamp | Pipeline worked. Row was there — check was done at wrong time or wrong table filter |
| A row exists but `org_id` is null or different | Row was inserted by the wrong connector (Known Issue 4 — global vs. org-scoped). Go to Layer 5 diagnosis |
| A row exists with correct org_id but `user_id` is null | v2.2.0 compliance issue in the plugin's telemetry skill. Go to Layer 5 |
| No row at all | Pipeline broke somewhere. Proceed to Layer 1 |
| SQL tool not found / error | Layer 4 is broken in this session. Go to Layer 4 directly |

---

## Layer 1 Test: Is the Database Reachable?

**Run via `mcp__olytic-telemetry__execute_sql`:**

```sql
SELECT NOW();
```

| Result | Verdict | Next step |
|---|---|---|
| Returns a timestamp | ✅ Layer 1 PASS | Proceed to Layer 2 |
| Tool not found or errors | ❌ Layer 4 is broken (connector not in session) | Jump to Layer 4 |
| Timeout / connection refused | ❌ Layer 1 FAIL — database unreachable | Fix: restore project at `https://supabase.com/dashboard/project/kxnmgutidehncnafrwbu` |

**Note:** If `mcp__olytic-telemetry__execute_sql` is not available in this session, you cannot run any Supabase tests from here. Skip to Layer 3/4 diagnosis (connector config) and come back.

---

## Layer 2 Test: Schema and RLS

**2a — Verify the table exists:**

```sql
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'telemetry_events'
ORDER BY ordinal_position;
```

Expected columns: `id`, `timestamp`, `event`, `plugin`, `plugin_version`, `org_id`, `user_id`, `component`, `trigger`, `created_at`.

If any of `org_id` or `user_id` are missing from the column list, the schema is out of date and needs to be updated in Supabase.

**2b — Test a direct INSERT:**

```sql
INSERT INTO telemetry_events (timestamp, event, plugin, plugin_version, org_id, user_id, component, trigger)
VALUES (NOW(), 'skill_invoke', 'diagnostic-test', '0.0.0', 'olytic-internal', 'support@olyticsolutions.com', 'telemetry-diagnostic', 'layer 2 baseline test');
```

Then verify it landed:

```sql
SELECT id, timestamp, event, org_id, component
FROM telemetry_events
WHERE component = 'telemetry-diagnostic'
ORDER BY created_at DESC
LIMIT 3;
```

| Result | Verdict | Next step |
|---|---|---|
| Row appears | ✅ Layer 2 PASS | Proceed to Layer 3/4 |
| INSERT rejected with RLS error | ❌ RLS policy problem | Check: is `org_id = 'olytic-internal'`? Run Step 2c |
| INSERT rejected with schema error | ❌ Schema missing columns | Apply schema migration in Supabase SQL editor |

**2c — Verify RLS policy:**

```sql
SELECT policyname, cmd, qual
FROM pg_policies
WHERE tablename = 'telemetry_events';
```

Should show a `plugin_insert` policy. If empty, RLS is not configured — data is unguarded. If present but failing INSERTs, the policy's `qual` condition likely requires `org_id` to match the JWT claim. Double-check the org_id value in the INSERT exactly matches `'olytic-internal'`.

---

## Layer 3/4 Test: Connector Health and Discovery

**This layer requires no SQL — it requires you to inspect what tools are available in the current session.**

**Layer 4 — Discovery test (do this first):**

Ask yourself: Is `mcp__olytic-telemetry__execute_sql` available as a tool right now?

- If you just ran the Layer 1 test above and it worked → Layer 4 PASS
- If the tool was not found → Layer 4 FAIL

**Layer 3 — If Layer 4 failed, the connector isn't in this session. Diagnose why:**

The connector must be installed in `~/Library/Application Support/Claude/claude_desktop_config.json` on the Mac. This is a machine-level config — not inside any plugin folder.

**Tell the user to check these things (no mounted folder required):**

1. Open Claude Desktop. Look at the bottom-left corner for the MCP server list. Is `olytic-telemetry` shown? Is it green (Connected) or grey/red (Disconnected)?

2. Open Terminal on the Mac. Run:
   ```bash
   which npx
   ```
   Note the output path (e.g., `/opt/homebrew/bin/npx` or `/usr/local/bin/npx`).

3. Open the config file in any text editor (TextEdit works):
   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

   Confirm it contains an entry like this (the `command` path must match the output of `which npx`):
   ```json
   "olytic-telemetry": {
     "command": "/opt/homebrew/bin/npx",
     "args": [
       "-y",
       "@supabase/mcp-server-supabase@latest",
       "--project-ref",
       "kxnmgutidehncnafrwbu",
       "--read-only",
       "false",
       "--supabase-access-token",
       "sbp_173d82e4ab04962d954bcd0412a72f07b5a142dd"
     ]
   }
   ```

4. If the config looks correct but the connector shows Disconnected: open Terminal and paste the command manually:
   ```bash
   /opt/homebrew/bin/npx -y @supabase/mcp-server-supabase@latest --project-ref kxnmgutidehncnafrwbu --supabase-access-token sbp_173d82e4ab04962d954bcd0412a72f07b5a142dd
   ```
   Replace the path with the output of `which npx`. If this command errors, the error message will reveal the exact problem.

5. **Common flag error:** If you see `Unknown option '--supabase-access-token'`, try replacing that flag with `--access-token` in the config instead.

6. **After any config change:** Fully quit Claude Desktop (Cmd+Q, not just close the window) and relaunch. Config is only read at startup.

**Layer 3 Pass criteria:** The connector shows Connected in Claude Desktop AND `SELECT NOW()` succeeds via the tool in a new session.

---

## Layer 5 Test: Plugin Skill Behavior

**This layer verifies the plugin's telemetry skill is actually firing correctly.**

Only run this after Layers 1–4 are confirmed passing.

**5a — Live invocation test:**

Ask the user to invoke any skill from the affected plugin naturally in a new Claude session. Then immediately run:

```sql
SELECT id, timestamp, event, plugin, plugin_version, org_id, user_id, component, trigger
FROM telemetry_events
WHERE org_id = 'olytic-internal'
  AND plugin != 'diagnostic-test'
ORDER BY created_at DESC
LIMIT 5;
```

**5b — Interpret the result:**

| What you see | What it means | Fix |
|---|---|---|
| Row appears with correct `org_id`, `plugin`, `component` | ✅ Layer 5 PASS — pipeline end-to-end verified | Done |
| No row appears | Telemetry skill not firing | Check Step 5c |
| Row appears with `org_id` = null | Plugin INSERT is missing `org_id` field | Update plugin telemetry skill INSERT template |
| Row appears with `user_id` = null | Plugin INSERT is missing `user_id` field | Update plugin telemetry skill INSERT template |
| Row appears but `org_id` is wrong value | Plugin's `[ORG_ID]` placeholder was not substituted | Plugin skill needs explicit `'olytic-internal'` value |
| Row appears but was inserted by a different tool | Claude used global Supabase connector (Known Issue 4) | Skill must call `mcp__olytic-telemetry__execute_sql` by exact name |

**5c — If no row at all:**

The telemetry skill likely fell into its silent-fail path ("if tool not found, continue without logging"). This means one of:
- The connector wasn't found in the session (Layer 4 issue — circle back)
- The INSERT was attempted but failed silently (check Supabase Postgres logs at `https://supabase.com/dashboard/project/kxnmgutidehncnafrwbu` → Logs → Postgres)
- The telemetry skill isn't being loaded with the plugin (plugin packaging issue — repackage and re-upload the plugin)

---

## Diagnostic Summary Template

After running all relevant tests, produce a structured verdict:

```
TELEMETRY DIAGNOSTIC REPORT
============================
Session context: [what skill ran, which plugin, approx when]

Layer 1 — Database reachable:        [PASS / FAIL / NOT TESTED]
Layer 2 — Schema + RLS valid:        [PASS / FAIL / NOT TESTED]
Layer 3 — Connector installed:       [PASS / FAIL / UNKNOWN — user must check]
Layer 4 — Connector in session:      [PASS / FAIL]
Layer 5 — Plugin skill firing:       [PASS / FAIL / NOT TESTED]

Root cause: [first layer that failed]
Missing row: [YES confirmed / NO — row was found / UNKNOWN]

Fix required:
[Specific action(s) — one per line]

Verification step:
[What to run after the fix to confirm it worked]
```

---

## What Each Fix Actually Looks Like

| Root cause | Fix |
|---|---|
| Supabase project paused | Go to `https://supabase.com/dashboard/project/kxnmgutidehncnafrwbu` → click Restore |
| `telemetry_events` table missing | Apply schema migration in Supabase SQL editor (get schema from TELEMETRY-TESTING.md or the Supabase dashboard) |
| RLS rejecting inserts | Confirm `org_id = 'olytic-internal'` exactly (case-sensitive). Check `pg_policies` for the `plugin_insert` policy |
| Connector not in config | Add the `olytic-telemetry` block to `~/Library/Application Support/Claude/claude_desktop_config.json` (see config template in Layer 3 test above) |
| Connector config has wrong npx path | Run `which npx` in Terminal, update the `"command"` field to match |
| Wrong flag (`--supabase-access-token` not accepted) | Change flag to `--access-token` in the config |
| Connector not visible after config change | Fully quit Claude Desktop (Cmd+Q) and relaunch |
| Plugin firing but using wrong connector | The plugin's telemetry skill must call `mcp__olytic-telemetry__execute_sql` by exact name. Update the skill file and repackage |
| Plugin INSERT missing `org_id` | Update plugin telemetry skill to include `org_id = 'olytic-internal'` in all INSERT statements. Repackage |
| Plugin INSERT missing `user_id` | Update plugin telemetry skill to include `user_id = 'support@olyticsolutions.com'` in all INSERT statements. Repackage |
| Plugin skill not loading at all | Repackage the plugin zip and re-upload to the marketplace. Start a fresh session |

---

## Telemetry

This skill logs its own invocation via gaudi-telemetry.
