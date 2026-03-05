# Telemetry Testing & Troubleshooting Strategy
**Status:** Living document
**Owner:** Joshua Kambour
**Last updated:** 2026-03-04 (added unmounted-folder guidance throughout)
**Companion to:** `TELEMETRY-ARCHITECTURE.md`

---

## ⚠️ Fundamental Cowork VM Constraints

**These two constraints govern every telemetry architecture decision. Any approach that conflicts with either of these will not work — confirmed by live testing on 2026-03-04.**

**1. The Cowork VM has no outbound network access to anything not on Anthropic's allowlist.**
All outbound traffic routes through a local proxy at `localhost:3128`. Any external URL — including Supabase, AWS RDS, Neon, Firebase, or any other database or API endpoint — returns `403 Forbidden` with `X-Proxy-Error: blocked-by-allowlist`. DNS resolution for external hostnames also fails (`EAI_AGAIN`). There is no workaround from inside the VM. HTTP POST, curl, WebFetch, direct Postgres TCP connections, and SOCKS5 proxy all fail. Switching database providers does not help — the constraint is the network layer, not the destination.

**2. The Cowork VM cannot read or write any files outside the working folder mounted in the specific chat session.**
The VM filesystem is ephemeral and resets between sessions. Only files written to the mounted working folder (`/sessions/.../mnt/`) persist on the user's Mac. Paths like `~/.claude/telemetry/` or any other location outside the mount point do not accumulate — writes go to the VM sandbox and are lost when the session ends. The working folder mount is session-specific: a folder mounted in one chat is not automatically available in another.

---

## How to Use This Document

The telemetry pipeline has several distinct layers, and failures can happen at any one of them. Rather than diagnosing from the middle, this document gives you a structured approach: **always test from the bottom up**, starting with the database and working outward. Each layer is a prerequisite for the one above it.

If you're in a hurry, jump to the [Quick Diagnostic Checklist](#quick-diagnostic-checklist) at the bottom.

> **🔧 Need to run diagnostics right now?**
> Use the `gaudi:telemetry-diagnostic` skill. It is fully self-contained — all architecture knowledge is embedded, no files need to be mounted. It will scan the current session, confirm whether a row should have been logged, run live layer tests, and produce a structured verdict with the specific fix. This guide is the reference document; the diagnostic skill is the active tool.

---

> **⚠️ Working Folder Not Mounted?**
> This guide can still be run in full without a locally mounted working folder. The only steps that require local file access are:
> - Layer 3: reading/editing `claude_desktop_config.json` on your Mac
> - Layer 3: running the manual bash test command in Terminal
> - Known Issue (auto-sync): running `ls -lt` to verify zip timestamps
>
> All database tests (Layers 1, 2, 4, 5) run entirely through Supabase or Claude and do not require a mounted folder. Where local file access is needed, this guide will note it explicitly and offer an alternative path.

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

> **📁 Working folder not mounted?** You can still read and edit `claude_desktop_config.json` directly on your Mac using a text editor (TextEdit, VS Code, etc.) — you don't need the working folder mounted for this. The config file lives on your Mac at `~/Library/Application Support/Claude/claude_desktop_config.json`. Open it in any editor, make corrections, save, and restart Claude Desktop.

See `claude_desktop_config_options.md` for pre-built config blocks for different Node.js setups. If your working folder isn't mounted and you can't access this companion doc, the most common config looks like:
```json
{
  "mcpServers": {
    "olytic-telemetry": {
      "command": "/opt/homebrew/bin/npx",
      "args": ["-y", "@supabase/mcp-server-supabase@latest",
               "--project-ref", "kxnmgutidehncnafrwbu",
               "--read-only", "false",
               "--supabase-access-token", "<your-token>"]
    }
  }
}
```
Replace `/opt/homebrew/bin/npx` with the output of `which npx` if different.

**Common failure: wrong flag name.** Some versions of `@supabase/mcp-server-supabase` don't accept `--supabase-access-token`. If you see this error in Terminal when running the command manually, check `troubleshoot-mcp-connector.md` for the correct flag for your installed version. If you can't access that file (folder not mounted), the alternative flag to try is `--access-token` instead of `--supabase-access-token`.

To test the command manually in Terminal:
```bash
/opt/homebrew/bin/npx -y @supabase/mcp-server-supabase@latest --project-ref kxnmgutidehncnafrwbu --supabase-access-token sbp_173d82e4ab04962d954bcd0412a72f07b5a142dd
```
(Replace the path and token with your actual values. If it runs without errors, the command is valid.)

> **📁 Working folder not mounted?** You can still run this Terminal command directly — it does not require the working folder. Open Terminal on your Mac and paste the command above with your actual token substituted in.

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

**Current compliance status (as of 2026-03-04 — post HTTP POST migration):**

| Plugin | Blueprint Version in Skill | Transport | org_id in payload | user_id in payload | Status |
|--------|---------------------------|-----------|-------------------|--------------------|----|
| Gaudi | v2.2.0 | `supabase-edge-function-http` | ✅ Injected server-side via JWT | ✅ Required in body | ✅ Compliant |
| The One Ring | v2.2.0 | `supabase-edge-function-http` | ✅ Injected server-side via JWT | ✅ Required in body | ✅ Compliant |
| Magneto | v2.2.0 | `supabase-edge-function-http` | ✅ Injected server-side via JWT | ✅ Required in body | ✅ Compliant |
| Aulë | v2.2.0 | `supabase-edge-function-http` | ✅ Injected server-side via JWT | ✅ Required in body | ✅ Compliant |

> **Note on org_id:** With the HTTP POST transport, `org_id` is NOT sent in the request body — it is injected server-side by the Edge Function from the JWT claim. All four plugins are correctly updated to omit `org_id` from the body. The Edge Function extracts it from the Bearer token and inserts it into the `telemetry_events` row with RLS enforcement.

> **Transport migration completed:** All plugins migrated from `org-scoped-supabase-mcp-connector` to `supabase-edge-function-http` on 2026-03-04. ZIPs regenerated and re-uploaded to marketplace. The MCP connector approach is deprecated — see TELEMETRY-ARCHITECTURE.md for details.

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
| Updated plugin source but uploaded version doesn't have the changes | .ZIP file is stale (not regenerated after source edit) | Auto-sync system should trigger automatically. If not, manually run: "repackage [plugin-name]". See "Known Issue: Plugin Source vs. .ZIP File Drift" for details |
| Smoke test Steps 1–4 all pass but real skill invocation produces no telemetry row | Steps 1–4 only test the connector in isolation — they do NOT test whether the plugin's telemetry skill fires autonomously. The plugin's silent-fail path is masking the error | Run Step 5 (real invocation in a new session), then use `gaudi:telemetry-diagnostic` to identify which layer broke. Most likely cause: wrong session type, stale cached plugin, or plugin packaging issue |

---

## Smoke Test: Full Pipeline Verification

Run this sequence after any significant change (new plugin uploaded, connector config updated, blueprint version change, new machine setup). Each step must pass before proceeding to the next.

> **⚠️ Known limitation of Steps 1–4:** These steps verify that the database is reachable and the connector is usable when Claude is *explicitly told* to use it. They do NOT verify that the plugin's telemetry skill will autonomously fire during normal use. It is fully possible to pass Steps 1–4 and still have telemetry silently fail in real sessions. **Step 5 is the only true end-to-end test.** Do not declare the pipeline working until Step 5 passes.

---

**Step 1 — Database reachable:**
```sql
SELECT NOW();
```
✅ Returns a timestamp

---

**Step 2 — Table and schema valid:**
```sql
SELECT column_name FROM information_schema.columns WHERE table_name = 'telemetry_events';
```
✅ Returns expected columns including `org_id` and `user_id`

---

**Step 3 — Direct INSERT works (Supabase SQL Editor):**
```sql
INSERT INTO telemetry_events (timestamp, event, plugin, plugin_version, org_id, user_id, component, trigger)
VALUES (NOW(), 'skill_invoke', 'smoke-test', '0.0.0', 'olytic-internal', 'support@olyticsolutions.com', 'smoke-test-direct', 'full pipeline verification step 3');
```
✅ No error

---

**Step 4 — INSERT via org-scoped MCP connector (connector reachability test):**

> **What this tests:** That the `mcp__olytic-telemetry__execute_sql` tool is available in the session and Claude can use it when explicitly instructed. **What this does NOT test:** Whether the plugin's telemetry skill will independently find and use it.

Ask Claude to use `mcp__olytic-telemetry__execute_sql` to run:
```sql
INSERT INTO telemetry_events (timestamp, event, plugin, plugin_version, org_id, user_id, component, trigger)
VALUES (NOW(), 'skill_invoke', 'smoke-test', '0.0.0', 'olytic-internal', 'support@olyticsolutions.com', 'smoke-test-mcp', 'full pipeline verification step 4');
```
✅ Claude confirms it used `mcp__olytic-telemetry__execute_sql`, row appears in Supabase

If this step fails (tool not found), the connector is not in this session — fix Layer 3 before continuing.

---

**Step 5 — Real plugin telemetry fires autonomously (the only true end-to-end test):**

> **This is the step that actually matters.** Steps 1–4 can all pass while this step fails. Only this step proves that a plugin's telemetry skill is correctly wired up.

Open a **new Claude session** (not the same session where you ran Steps 1–4). Make sure the plugin you want to test is active. Invoke a skill naturally — for example, ask Gaudi a data modeling question, or ask The One Ring to check something for brand compliance. Then immediately run:

```sql
SELECT id, timestamp, plugin, plugin_version, org_id, user_id, component, trigger
FROM telemetry_events
WHERE org_id = 'olytic-internal'
  AND plugin != 'smoke-test'
  AND plugin != 'diagnostic-test'
ORDER BY created_at DESC
LIMIT 5;
```

**Verify:**
- A new row appeared after your invocation
- `plugin` matches the plugin you used
- `component` matches the skill you invoked
- `org_id = 'olytic-internal'` (not null)
- `user_id` is not null

✅ All of the above confirmed = pipeline is genuinely working end-to-end

**If no row appeared after Step 5 (even though Steps 1–4 passed):** The most likely cause is that the plugin's telemetry skill is hitting its silent-fail path ("if tool not found, continue without logging"). This can happen because:
- The session type where skills run is different from the session where you ran Steps 1–4 (some session configurations don't expose the same MCP tools)
- The plugin cached in Claude is an older version without working telemetry
- The plugin's skill file calls the connector by exact name but the connector ID in the session has changed

In all of these cases, use `gaudi:telemetry-diagnostic` to run an active diagnosis — it will identify exactly which layer broke.

---

**Step 6 — No rows with null org_id (last hour):**
```sql
SELECT COUNT(*) FROM telemetry_events
WHERE org_id IS NULL AND created_at > NOW() - INTERVAL '1 hour';
```
✅ Returns 0

---

**Steps 1–4 passing + Step 5 passing + Step 6 passing = pipeline is verified end-to-end.**

Steps 1–4 passing but Step 5 failing = connector works when Claude is told to use it, but the plugin's telemetry skill is not autonomously firing. Use `gaudi:telemetry-diagnostic` to find why.

---

## Quick Diagnostic Checklist

For fast triage when something seems off:

- [ ] Is the Supabase project Active (not paused)?
- [ ] Does `telemetry_events` table exist with correct schema?
- [ ] Is `olytic-telemetry` showing Connected in Claude Desktop?
- [ ] Does `which npx` in Terminal match the `"command"` in `claude_desktop_config.json`? *(Open this file directly on your Mac at `~/Library/Application Support/Claude/claude_desktop_config.json` — no working folder needed)*
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

## Known Issue: Plugin Source vs. .ZIP File Drift

### The Problem

**What happened:** Plugin source files were being updated (skills added, README modified, etc.), but the .zip files packaged for upload were not being regenerated. This created a critical mismatch where:

- The local source folder (e.g., `Plugins/gaudi/src-gaudi/`) had the latest changes ✅
- The packaged .zip file (e.g., `Plugins/gaudi/gaudi.zip`) was stale ❌
- When uploading to the marketplace, the old .zip was uploaded, so users never saw the new changes
- This led to confusion: "I added telemetry-testing to Gaudi, but the uploaded version still doesn't have it"

**Root cause:** There was no automatic mechanism to regenerate .zip files when source files changed. Developers assumed updating source = automatic zip update, but this didn't happen. The zips were only updated manually, and often forgotten.

**Impact:**
- New skills/features added to source weren't visible when plugins were used
- Updates to plugin documentation didn't propagate
- Marketplace versions were consistently behind the local development versions

### The Fix: Auto-Sync System

**What was implemented:** Created a two-part auto-sync system to ensure source and .zip files are always in sync:

1. **New Skill: `aule-plugin-repackager`**
   - Detects when plugin source files change
   - Automatically regenerates the corresponding .zip file
   - Verifies the .zip contains all expected files
   - Logs every repackage operation with timestamp and file inventory

2. **Extended PostToolUse Hook**
   - Modified `Plugins/aule/src-aule/hooks/hooks.json` to monitor plugin source paths
   - When any file is written/edited in `Plugins/*/src-*/` folders, the hook triggers automatically
   - Hook invokes `aule-plugin-repackager` skill with the changed file path
   - No user action required — the .zip updates itself

**Current Status (as of 2026-03-04):**

All four organizational plugins are now synced:

| Plugin | Source Folder | ZIP File | Status |
|--------|---------------|----------|--------|
| **gaudi** | `src-gaudi/` (updated 18:31) | `gaudi.zip` (regenerated 18:35) | ✅ SYNCED (includes telemetry-testing skill) |
| **the-one-ring** | `src-one-ring/` (updated 18:31) | `the-one-ring.zip` (regenerated 18:35) | ✅ SYNCED |
| **magneto** | `src-magneto/` (updated 18:31) | `magneto.zip` (regenerated 18:35) | ✅ SYNCED |
| **aule** | `src-aule/` (updated 04:58) | `aule.zip` (regenerated 18:35) | ✅ SYNCED (includes aule-plugin-repackager skill) |

**Going forward:**
- When you edit any plugin source file, the PostToolUse hook automatically invokes the repackager skill
- The .zip file is regenerated within seconds
- You can upload to marketplace immediately — the .zip always contains your latest changes
- Marketplace version will match local development version

### How to Verify the Fix is Working

**If working folder is mounted**, after editing plugin source, run:
```bash
ls -lt Plugins/gaudi/gaudi.zip Plugins/gaudi/src-gaudi/
```
If the .zip timestamp is within 1-2 seconds of the source folder timestamp, auto-sync is working.

**If working folder is not mounted**, you cannot check file timestamps via bash. Instead:
1. Ask Claude: `"List files in the gaudi plugin folder and show the most recent modification times for gaudi.zip and the src-gaudi directory."` — Claude can use its file tools to check this without a bash shell.
2. Alternatively, open Finder on your Mac, navigate to the `olytic-plugins/Plugins/gaudi/` folder, and compare the "Date Modified" timestamps of `gaudi.zip` vs. the `src-gaudi/` folder visually.
3. If the .zip is much older than the source, the hook may not have triggered — in that case, manually invoke: `"repackage the gaudi plugin"` in a Claude session where the working folder **is** mounted (the repackager skill requires file write access).

---

## Known Issue: MCP Connector Startup Failure (2026-03-04)

### The Problem

**Status:** ✅ Resolved — Migrated to HTTP POST Edge Function transport on 2026-03-04
**Discovered:** March 4, 2026 during smoke test verification
**Resolved:** March 4, 2026 — all plugins migrated to `supabase-edge-function-http` transport
**Severity (at time of discovery):** Critical — blocked Layer 5 (plugin skill telemetry autonomously firing)

The `olytic-telemetry` MCP connector (powered by `@supabase/mcp-server-supabase@latest`) fails to start and hangs indefinitely with zero output or error messages when invoked.

**Symptoms:**
- Claude Desktop shows `olytic-telemetry` connector as grey/disconnected (not green)
- After full Claude restart, connector remains disconnected
- Running the npx command directly in Terminal hangs with no output
- `npx -y @supabase/mcp-server-supabase@latest [args]` produces nothing after 15+ seconds
- No error messages — complete silence

**Environment:**
- Node: v20.20.0 (via nvm)
- npm: 10.8.2
- Package: `@supabase/mcp-server-supabase@latest`
- Project ref: `kxnmgutidehncnafrwbu`
- Config path: `~/Library/Application Support/Claude/claude_desktop_config.json`

### What We've Tested

**Layer 1–4 (automated tests): All PASS**
- Database reachable (SELECT NOW() works)
- Schema valid (telemetry_events table exists with all required columns)
- Direct INSERTs work (rows land in Supabase via SQL Editor)
- When Claude is explicitly told to use the connector via `mcp__olytic-telemetry__execute_sql`, it works perfectly

**Layer 5 (real plugin invocations): FAIL**
- Gaudi `telemetry-testing` skill invoked → no row appeared in Supabase
- The One Ring `values-check` skill invoked → no row appeared in Supabase
- Gaudi `telemetry-diagnostic` skill invoked → no row appeared in Supabase
- Most recent real skill invocation row in Supabase is from 18:19 UTC (Gaudi `product-management` skill)
- No `telemetry-testing`, `values-check`, or `telemetry-diagnostic` rows exist

**Plugin source and zip files: Both confirmed correct**
- `gaudi/src-gaudi/skills/gaudi-telemetry/SKILL.md` references `mcp__olytic-telemetry__execute_sql` by exact name ✅
- `the-one-ring/src-the-one-ring/skills/the-one-ring-telemetry/SKILL.md` references `mcp__olytic-telemetry__execute_sql` by exact name ✅
- `gaudi.zip` contains correct telemetry skill (verified via unzip) ✅
- `the-one-ring.zip` contains correct telemetry skill (verified via unzip) ✅

**Connector configuration: Verified correct**
- npx path in config: `/Users/joshuakambour/.nvm/versions/node/v20.20.0/bin/npx`
- `which npx` returns: `/Users/joshuakambour/.nvm/versions/node/v20.20.0/bin/npx`
- Paths match exactly ✅
- Service role token replaced (old JWT token was invalid) ✅
- npm cache cleared (`npm cache clean --force`) ✅
- Full Claude restart performed multiple times ✅

**Direct command execution: Hangs**
```bash
/Users/joshuakambour/.nvm/versions/node/v20.20.0/bin/npx -y @supabase/mcp-server-supabase@latest \
  --project-ref kxnmgutidehncnafrwbu \
  --access-token "[service-role-jwt]" \
2>&1
```
Result: Complete hang, no output, no error, must Ctrl+C to exit.

### Root Cause Analysis

The hanging behavior with zero output suggests:

1. **Most likely:** The `@supabase/mcp-server-supabase@latest` package has a bug or incompatibility that prevents startup
2. **Possible:** The package is trying to reach Supabase at startup and timing out (network issue)
3. **Possible:** The service role token is being rejected at connection time (silent failure)
4. **Possible:** Node v20.20.0 has compatibility issues with the package

### Next Steps for Future Investigation

1. **Try pinning to a specific version** instead of `@latest`:
   ```json
   "@supabase/mcp-server-supabase@1.0.0"
   ```
   (Replace with a known stable version from npm registry)

2. **Enable verbose logging** to see what the package is doing:
   ```bash
   DEBUG=* /Users/joshuakambour/.nvm/versions/node/v20.20.0/bin/npx -y @supabase/mcp-server-supabase@latest ...
   ```

3. **Check npm registry for the package** — visit https://www.npmjs.com/package/@supabase/mcp-server-supabase and verify if there are known issues, deprecations, or recent breaking changes

4. **Try a different Supabase MCP package** if one exists — search npm for `supabase mcp` alternatives

5. **Implement a custom minimal MCP connector** if the existing package cannot be fixed — a simple Node.js script that wraps Supabase SQL execution

6. **Check if the issue is specific to this machine** — test on another Mac or in a fresh Terminal environment

### Resolution

The MCP connector approach was abandoned in favor of HTTP POST to a Supabase Edge Function. This eliminates the connector startup failure entirely:

- All four plugins (Gaudi, The One Ring, Magneto, Aulë) updated to use `telemetry_transport: "supabase-edge-function-http"`
- All telemetry skills rewritten to HTTP POST instead of SQL INSERT via MCP
- Aulë's telemetry-template.md updated so all future generated plugins use HTTP POST from day one
- TELEMETRY-STANDARDS.md bumped to v2.3.0 to document the new canonical transport
- All plugin .zip files regenerated and re-uploaded to the organizational marketplace
- Edge function confirmed working: `{"success":true}` from user's Mac on 2026-03-04

**Impact on Telemetry Pipeline (post-resolution):**
- **Layer 5:** Plugin skills now use HTTP POST — no MCP connector dependency at runtime
- **org_id:** Server-side injection from JWT claim — the Edge Function enforces org isolation
- **user_id:** Required in request body by all telemetry skills
- **MCP connector:** Deprecated for telemetry transport. Still available for diagnostic tools (gaudi:telemetry-diagnostic, gaudi:telemetry-testing) that need to query Supabase directly.

### Document This Issue In

- `TELEMETRY-ARCHITECTURE.md` — add as Known Issue with "Open" status
- Future engineering sessions should reference this section and the troubleshooting steps taken

---

## Document Maintenance

Update this document whenever:
- A known issue is resolved (update the issue status in `TELEMETRY-ARCHITECTURE.md` and remove it from the troubleshooting table here)
- A new failure mode is discovered
- The plugin cache path is identified (update Issue 1 in architecture doc and the error table here)
- A new plugin is added to the compliance audit table
- The blueprint version changes (update smoke test SQL and compliance table)
- Plugin source/zip drift detected (see "Known Issue: Plugin Source vs. .ZIP File Drift" above)
- MCP connector startup issues occur (see "Known Issue: MCP Connector Startup Failure" above)
