# Telemetry Testing & Troubleshooting Strategy
**Status:** Living document
**Owner:** Joshua Kambour
**Last updated:** 2026-03-04
**Companion to:** `TELEMETRY-ARCHITECTURE.md`

---

## How to Use This Document

The telemetry pipeline has several distinct layers, and failures can happen at any one of them. Rather than diagnosing from the middle, this document gives you a structured approach: **always test from the bottom up**, starting with the database and working outward. Each layer is a prerequisite for the one above it.

If you're in a hurry, jump to the [Quick Diagnostic Checklist](#quick-diagnostic-checklist) at the bottom.

---

## The Five Layers You're Testing

Think of the pipeline as a stack. Data has to pass through every layer to land in Supabase correctly. A failure at any layer stops everything above it.

```
Layer 5 │  Plugin Skill Behavior
         │  (Does the telemetry skill fire when a skill is invoked?)
         │
Layer 4 │  MCP Connector Discovery
         │  (Can Claude find the olytic-telemetry connector in this session?)
         │
Layer 3 │  MCP Connector Health
         │  (Is the connector installed and running — not "disconnected"?)
         │
Layer 2 │  Supabase RLS + Schema
         │  (Are INSERTs accepted? Do org_id and user_id pass the policy check?)
         │
Layer 1 │  Supabase Database Reachability
         │  (Can we reach the database at all? Is the project active?)
```

Test Layer 1 first. If it fails, nothing else matters yet.

---

## Layer 1: Supabase Database Reachability

**What you're testing:** Can we connect to the Supabase project and read from it?

**How to test:**

Run this SQL in the Supabase dashboard (Table Editor → SQL Editor), or via the MCP connector in a Claude session:

```sql
SELECT NOW();
```

If this returns the current timestamp, the database is reachable. If it times out or errors, the Supabase project may be paused or the project ref is wrong.

**Also verify the project is active:**
- Go to: https://supabase.com/dashboard/project/kxnmgutidehncnafrwbu
- Check that it shows "Active" status, not "Paused"
- Free-tier Supabase projects pause after 7 days of inactivity. If paused, click "Restore."

**Expected outcome:** `NOW()` returns a timestamp. Project shows Active.

---

## Layer 2: Supabase RLS + Schema

**What you're testing:** Does the `telemetry_events` table exist, and will it accept a correctly-formed INSERT with valid `org_id` and `user_id`?

### Step 2a: Verify the table exists

```sql
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'telemetry_events'
ORDER BY ordinal_position;
```

You should see columns including: `id`, `timestamp`, `event`, `plugin`, `plugin_version`, `org_id`, `user_id`, `component`, `trigger`, `created_at`. If the table doesn't exist, the schema hasn't been applied yet.

### Step 2b: Test a direct INSERT

Run this in the Supabase SQL Editor (not via Claude — this bypasses RLS, which is intentional for baseline testing):

```sql
INSERT INTO telemetry_events (timestamp, event, plugin, plugin_version, org_id, user_id, component, trigger)
VALUES (NOW(), 'skill_invoke', 'test', '0.0.0', 'olytic-internal', 'support@olyticsolutions.com', 'smoke-test', 'layer 2 baseline test');
```

Then confirm it landed:

```sql
SELECT id, timestamp, event, plugin, org_id, component
FROM telemetry_events
WHERE component = 'smoke-test'
ORDER BY created_at DESC
LIMIT 3;
```

**Expected outcome:** Row appears immediately with the correct values.

**If the INSERT is rejected:** Check for RLS policy errors in the Supabase logs (Dashboard → Logs → Postgres). The most common cause is a missing `org_id` field or a mismatch between the value in the INSERT and the JWT claim.

### Step 2c: Verify the RLS policy exists

```sql
SELECT policyname, cmd, qual
FROM pg_policies
WHERE tablename = 'telemetry_events';
```

You should see a `plugin_insert` policy that references `org_id`. If no policies are listed, RLS is not enabled or was not configured — meaning any insert would go through unguarded, which is also a problem (no isolation).

---

## Layer 3: MCP Connector Health

**What you're testing:** Is the `olytic-telemetry` MCP connector installed on this machine and showing as connected in Claude?

### Step 3a: Check Claude Desktop

Open Claude Desktop and look at the bottom-left corner. MCP servers appear there with a status indicator. The `olytic-telemetry` connector should show as connected (green), not disconnected (red/grey).

**If it shows disconnected:**

1. Open Terminal and run: `which npx`
2. Compare the path it returns to the `"command"` value in your `claude_desktop_config.json`
3. If they don't match, update the config file with the correct path
4. Restart Claude Desktop after any config change

Config file location:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

See `claude_desktop_config_options.md` for pre-built config blocks for different Node.js setups.

**Common failure: wrong flag name.** Some versions of `@supabase/mcp-server-supabase` don't accept `--supabase-access-token`. If you see this error in Terminal when running the command manually, check `troubleshoot-mcp-connector.md` for the correct flag for your installed version.

To test the command manually in Terminal:
```bash
/opt/homebrew/bin/npx -y @supabase/mcp-server-supabase@latest --project-ref kxnmgutidehncnafrwbu --supabase-access-token sbp_173d82e4ab04962d954bcd0412a72f07b5a142dd
```
(Replace the path and token with your actual values. If it runs without errors, the command is valid.)

### Step 3b: Restart Claude after config changes

Claude Desktop reads `claude_desktop_config.json` **only at startup**. If you edit the config while Claude is open, you must fully quit and relaunch for changes to take effect.

---

## Layer 4: MCP Connector Discovery at Runtime

**What you're testing:** When Claude is in a session with a plugin active, can it actually find and use the `mcp__olytic-telemetry__execute_sql` tool?

This is the layer most likely to be confused with other Supabase access (see Known Issue 4 in the architecture doc). The critical distinction:

- ✅ **Correct path:** Claude uses `mcp__olytic-telemetry__execute_sql` (the org-scoped connector)
- ❌ **False positive:** Claude uses a global Supabase tool from a separate integration (like `mcp__supabase__execute_sql` or similar), which bypasses org-scoping

### Step 4a: Run the org-scoped smoke test via Claude

Open a new Claude Cowork session (with any plugin active, or no plugin — just the connector needs to be available). Paste this prompt:

> "Using the olytic-telemetry MCP connector — specifically the tool that matches the pattern `mcp__olytic-telemetry__execute_sql` — run this INSERT:
> ```sql
> INSERT INTO telemetry_events (timestamp, event, plugin, plugin_version, org_id, user_id, component, trigger)
> VALUES (NOW(), 'skill_invoke', 'test', '0.0.0', 'olytic-internal', 'support@olyticsolutions.com', 'connector-discovery-test', 'manual layer 4 test');
> ```
> Tell me which tool name you used to run this."

**Expected outcome:** Claude confirms it used `mcp__olytic-telemetry__execute_sql` (not a different Supabase tool). Then verify the row landed in Supabase:

```sql
SELECT id, timestamp, event, org_id, component
FROM telemetry_events
WHERE component = 'connector-discovery-test'
ORDER BY created_at DESC
LIMIT 3;
```

**If Claude used a different tool:** This means either the org-scoped connector isn't visible in the session, or Claude is defaulting to a different Supabase integration. Check Layer 3 first (is the connector connected?). Then explicitly instruct Claude to use only the org-scoped connector.

**If Claude says it can't find any `execute_sql` tool:** The connector is not available in this session. Go back to Layer 3.

---

## Layer 5: Plugin Skill Behavior

**What you're testing:** When you actually invoke a plugin skill in a real session, does the telemetry fire automatically — and does it fire with the correct fields?

This is the full end-to-end test. It requires Layers 1–4 to already be confirmed working.

### Step 5a: Choose a plugin and invoke a skill

Open a Claude Cowork session with one of the Olytic organizational plugins active (e.g., Gaudi, The One Ring, Magneto). Invoke a skill naturally — for example, ask Gaudi a data modeling question.

### Step 5b: Check Supabase for the resulting row

Immediately after the response, query Supabase:

```sql
SELECT id, timestamp, event, plugin, plugin_version, org_id, user_id, component, trigger
FROM telemetry_events
WHERE org_id = 'olytic-internal'
ORDER BY created_at DESC
LIMIT 5;
```

**Expected outcome:** A `skill_invoke` row appears with the correct `plugin`, `component`, `org_id = 'olytic-internal'`, and a non-null `user_id`.

**Diagnosis if no row appears:**
1. Was the connector found? (Layer 4 issue)
2. Does the plugin's telemetry skill include `org_id` and `user_id` in its INSERT pattern? (Known Issue 5 — v2.2.0 compliance)
3. Did the RLS policy reject the insert? (Check Supabase Postgres logs)

### Step 5c: Validate org_id and user_id are present

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(org_id) AS rows_with_org_id,
  COUNT(user_id) AS rows_with_user_id,
  COUNT(*) FILTER (WHERE org_id IS NULL) AS missing_org_id,
  COUNT(*) FILTER (WHERE user_id IS NULL) AS missing_user_id
FROM telemetry_events
WHERE created_at > NOW() - INTERVAL '1 hour';
```

If `missing_org_id` or `missing_user_id` is greater than zero for recent rows, you have a v2.2.0 compliance issue in one or more plugin telemetry skills.

---

## Plugin Compliance Audit (v2.2.0)

Run this audit whenever you update a plugin or after any change to the telemetry blueprint. The goal is to verify each plugin's telemetry skill is compliant with the current standard.

**For each plugin (Gaudi, The One Ring, Magneto, Aulë), check:**

1. Open the plugin's `skills/plugin-telemetry/SKILL.md` file
2. Check frontmatter: does it declare `telemetry_blueprint: "TELEMETRY-STANDARDS.md v2.2.0"`?
3. Find the INSERT example in "How to Write Logs" — does it include `org_id` and `user_id` columns?
4. Verify the INSERT pattern hardcodes `org_id = 'olytic-internal'` for internal plugins

**Quick audit checklist per plugin (from TELEMETRY-STANDARDS.md Section 12):**

- [ ] `skills/plugin-telemetry/SKILL.md` exists
- [ ] Frontmatter declares current blueprint version
- [ ] All 9 event types are documented
- [ ] INSERT examples include `org_id` and `user_id`
- [ ] Success Metrics table is present
- [ ] Every other skill in the plugin references: "This skill logs all invocations via plugin-telemetry"

**Current compliance status (as of 2026-03-04):**

| Plugin | Blueprint Version in Skill | org_id in INSERT | user_id in INSERT | Status |
|--------|---------------------------|------------------|-------------------|--------|
| Gaudi | Unknown — needs audit | Unknown | Unknown | ⚠️ Audit needed |
| The One Ring | Unknown — needs audit | Unknown | Unknown | ⚠️ Audit needed |
| Magneto | Unknown — needs audit | Unknown | Unknown | ⚠️ Audit needed |
| Aulë | Unknown — needs audit | Unknown | Unknown | ⚠️ Audit needed |

*Update this table as each plugin is audited and updated.*

---

## Troubleshooting Decision Tree

Use this when something isn't working and you're not sure where to start.

```
START: Telemetry rows aren't appearing in Supabase
        │
        ├─► Is the Supabase project Active?
        │         No → Restore it at supabase.com/dashboard
        │         Yes ↓
        │
        ├─► Does the telemetry_events table exist?
        │         No → Apply the schema migration
        │         Yes ↓
        │
        ├─► Does a direct INSERT from Supabase SQL Editor work?
        │         No → RLS policy problem or schema issue
        │              → Check pg_policies, check for missing org_id
        │         Yes ↓
        │
        ├─► Is olytic-telemetry showing as "Connected" in Claude Desktop?
        │         No → Config problem: check claude_desktop_config.json
        │              → Verify npx path with `which npx` in Terminal
        │              → Quit and relaunch Claude after any config change
        │         Yes ↓
        │
        ├─► When you explicitly ask Claude to use mcp__olytic-telemetry__execute_sql,
        │   does it find and use that specific tool?
        │         No → Connector isn't visible in this session type
        │              → Verify it's installed at machine level, not in a plugin
        │         Yes ↓
        │
        ├─► When a plugin skill fires in a real session, does a row appear?
        │         No → Plugin telemetry skill has a bug
        │              → Check: is org_id/user_id included in INSERT?
        │              → Is the skill at blueprint v2.2.0?
        │         Yes ↓
        │
        └─► Does the row have correct org_id = 'olytic-internal'?
                  No → Plugin is using wrong connector (global vs. org-scoped)
                       → Or org_id value is hardcoded incorrectly in skill
                  Yes → Pipeline is working correctly ✅
```

---

## Common Error Messages and Fixes

| Error / Symptom | Most Likely Cause | Fix |
|----------------|-------------------|-----|
| Connector shows "Disconnected" in Claude | Wrong `npx` path in config | Run `which npx`, update `claude_desktop_config.json`, restart Claude |
| `Unknown option '--supabase-access-token'` | Cached older version of MCP package | See `troubleshoot-mcp-connector.md` for correct flags |
| INSERT silently ignored, no row in Supabase | Connector not found in session | Verify Layer 3 and 4; check connector is at machine level |
| INSERT rejected with RLS error | Missing or wrong `org_id` | Check plugin telemetry skill INSERT pattern for `org_id` field |
| Row appears but `org_id` is null or wrong | Plugin not at v2.2.0 | Update plugin telemetry skill INSERT template |
| Row appears with wrong connector name | Claude used global Supabase, not org-scoped | Explicitly specify `mcp__olytic-telemetry__execute_sql` in prompt |
| Plugin loads old skill content | Stale plugin cache | Delete plugin cache directory, restart Claude (cache path TBD) |
| Claude looks for files in wrong location | Local vs. remote plugin confusion | State clearly in prompt: "using organizational version" or "locally mounted" |

---

## Smoke Test: Full Pipeline Verification

Run this sequence after any significant change (new plugin uploaded, connector config updated, blueprint version change, new machine setup). Each step must pass before proceeding to the next.

**Step 1 — Database reachable:**
```sql
SELECT NOW();
```
✅ Returns a timestamp

**Step 2 — Table and schema valid:**
```sql
SELECT column_name FROM information_schema.columns WHERE table_name = 'telemetry_events';
```
✅ Returns expected columns including `org_id` and `user_id`

**Step 3 — Direct INSERT works (Supabase SQL Editor):**
```sql
INSERT INTO telemetry_events (timestamp, event, plugin, plugin_version, org_id, user_id, component, trigger)
VALUES (NOW(), 'skill_invoke', 'smoke-test', '0.0.0', 'olytic-internal', 'support@olyticsolutions.com', 'smoke-test-direct', 'full pipeline verification step 3');
```
✅ No error

**Step 4 — INSERT via org-scoped MCP connector (via Claude):**
Ask Claude to use `mcp__olytic-telemetry__execute_sql` to run:
```sql
INSERT INTO telemetry_events (timestamp, event, plugin, plugin_version, org_id, user_id, component, trigger)
VALUES (NOW(), 'skill_invoke', 'smoke-test', '0.0.0', 'olytic-internal', 'support@olyticsolutions.com', 'smoke-test-mcp', 'full pipeline verification step 4');
```
✅ Claude confirms it used `mcp__olytic-telemetry__execute_sql`, row appears in Supabase

**Step 5 — Real plugin telemetry fires automatically:**
Invoke any skill from Gaudi, The One Ring, Magneto, or Aulë. Then:
```sql
SELECT id, timestamp, plugin, org_id, user_id, component
FROM telemetry_events
WHERE org_id = 'olytic-internal'
  AND plugin != 'smoke-test'
ORDER BY created_at DESC
LIMIT 5;
```
✅ A row appears with correct `org_id`, `user_id`, and the plugin name you invoked

**Step 6 — No rows with null org_id (last hour):**
```sql
SELECT COUNT(*) FROM telemetry_events
WHERE org_id IS NULL AND created_at > NOW() - INTERVAL '1 hour';
```
✅ Returns 0

All six steps passing = pipeline is verified end-to-end.

---

## Quick Diagnostic Checklist

For fast triage when something seems off:

- [ ] Is the Supabase project Active (not paused)?
- [ ] Does `telemetry_events` table exist with correct schema?
- [ ] Is `olytic-telemetry` showing Connected in Claude Desktop?
- [ ] Does `which npx` in Terminal match the `"command"` in `claude_desktop_config.json`?
- [ ] Did I fully quit and relaunch Claude after the last config change?
- [ ] When rows appear, do they have `org_id = 'olytic-internal'` (not null, not different)?
- [ ] Is the plugin's telemetry skill at blueprint v2.2.0?
- [ ] Am I using the org-scoped connector, not a global Supabase integration?

---

## What "Verified" Actually Means

Due to Known Issue 4 (Gaudi's global connector confusion), it's important to be precise about what counts as proof:

| Claim | Does It Prove the Pipeline Works? |
|-------|----------------------------------|
| A row appeared in Supabase | Only if it was inserted via `mcp__olytic-telemetry__execute_sql` |
| Gaudi inserted a row | Not by itself — need to confirm which tool it used |
| A direct INSERT from Supabase SQL Editor worked | No — this bypasses both the MCP connector and RLS |
| A skill fired and a row appeared with `org_id = 'olytic-internal'` via the correct connector | ✅ Yes — this is the definition of end-to-end verified |

When in doubt, run the full smoke test above rather than relying on partial signals.

---

## Document Maintenance

Update this document whenever:
- A known issue is resolved (update the issue status in `TELEMETRY-ARCHITECTURE.md` and remove it from the troubleshooting table here)
- A new failure mode is discovered
- The plugin cache path is identified (update Issue 1 in architecture doc and the error table here)
- A new plugin is added to the compliance audit table
- The blueprint version changes (update smoke test SQL and compliance table)
