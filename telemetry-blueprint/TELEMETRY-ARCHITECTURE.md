# Olytic Telemetry Architecture
**Status:** Living document — updated as gaps are resolved
**Owner:** Joshua Kambour
**Last updated:** 2026-03-04
**Audience:** Founder + future team members (non-technical)

---

## Plain-English Framing: What Is Telemetry and Why Does It Matter?

Think of telemetry as the system that watches how our plugins get used and silently records what happened. Every time someone uses one of our Claude plugins, a small "event log" entry is created: what plugin was used, what skill fired, what decision was made. That data flows into a central database (Supabase), where it accumulates over time. Eventually, enough data builds up that we can analyze it — and use the findings to make plugins better automatically. That's the compounding loop.

Without telemetry, plugins are useful but static. With it, they improve over time.

---

## The Building Blocks

### Aulë
Aulë is our "plugin factory" — the Claude plugin that builds other plugins. When you want a new plugin created (say, a proposal-management plugin for a client), Aulë runs a structured discovery conversation, then generates all the files that make up that plugin.

Critically, **every plugin Aulë generates automatically includes a telemetry skill.** This is non-negotiable and baked into Aulë's generation templates. That telemetry skill is what makes the plugin "self-reporting."

### The Telemetry Blueprint
The Telemetry Blueprint (`TELEMETRY-STANDARDS.md`, in this same folder) is the canonical specification for how all plugins must log data. It defines:
- The **nine event types** that any plugin might log (skill invocations, decisions, constraint violations, feedback, etc.)
- The **required fields** for each event type
- The **format** (JSONL — one line per event, standardized field order)
- The **transmission mechanism** (SQL INSERT via MCP connector, described below)

Aulë owns this blueprint. When Aulë generates a plugin's telemetry skill, it stamps which version of the blueprint it followed. If the blueprint changes, Aulë's template gets updated first — then new plugins inherit the new standard automatically.

**Current version:** `TELEMETRY-STANDARDS.md v2.2.0`
**Important change in v2.2.0:** Every INSERT into Supabase now requires `org_id` and `user_id`. Inserts missing these fields are rejected at the database level.

### Plugin Telemetry Skills
Every generated plugin contains a skill file called `plugin-telemetry/SKILL.md`. This file is the plugin's local copy of the telemetry instructions — customized with the plugin's name, version, constraints, and success metrics. When that plugin's skills are invoked, the telemetry skill silently fires SQL inserts to Supabase.

The telemetry skill is invisible to the user. It runs in the background and produces no visible output unless a constraint violation occurs (in which case Claude explains what went wrong and suggests an alternative).

### The MCP Connector (org-scoped)
The MCP connector is the bridge between a Claude session and the Supabase database. It is what allows Claude — running inside Cowork — to execute SQL against a live database it otherwise couldn't reach.

**How it works:**
- The connector is a small configuration entry in the Claude desktop config file (`claude_desktop_config.json`), installed at the machine/user level — not inside any plugin
- Once installed, it exposes a tool in every Claude session matching the pattern `mcp__[connector-id]__execute_sql`
- When a plugin's telemetry skill fires, it searches for any tool matching that pattern, then calls it with a SQL INSERT statement
- Supabase receives the row and stores it immediately

**The connector is org-scoped.** Each organization gets their own connector, configured with their org's credentials. The connector encodes an `org_id` (e.g., `olytic-internal` for Olytic's own use, `client-acme` for a future client). The Supabase database uses Row Level Security (RLS) to enforce that each org can only read and write their own rows. This is how multi-tenancy works — one shared database, isolated per org.

**For Olytic internally:** The connector is already installed and configured. The org_id is `olytic-internal`, pointing to the Supabase project `kxnmgutidehncnafrwbu`.

**For future clients:** During client onboarding, we generate a new JWT for their `org_id` and install their own connector in their Cowork environment. Their telemetry flows into the same Supabase project but is isolated behind RLS.

### The Supabase Edge Function
When a plugin calls the MCP connector with a SQL INSERT, where does that INSERT go?

The Olytic telemetry Supabase project (`kxnmgutidehncnafrwbu`) has a `telemetry_events` table. The MCP connector is configured to point at this project with sufficient credentials to insert rows. The connector uses the Supabase MCP server package (`@supabase/mcp-server-supabase`) to handle the connection.

There is also a Supabase Edge Function available at:
```
https://kxnmgutidehncnafrwbu.supabase.co/functions/v1/log-telemetry
```
This is referenced in Aulë's `.mcp.json` as the `olytic-telemetry` server URL. This HTTP-based approach is an alternative connector pattern used in the remote plugin context (Cowork organizational plugins served remotely).

---

## End-to-End Data Flow

Here's the full journey of a single telemetry event, from user action to database row:

```
1. User invokes a plugin skill in a Claude Cowork session
        ↓
2. The plugin's SKILL.md loads and executes
        ↓
3. Simultaneously, plugin-telemetry/SKILL.md is active in the session
        ↓
4. Telemetry skill builds an event JSON object:
   { timestamp, event, plugin, plugin_version, org_id, user_id, component, trigger }
        ↓
5. Telemetry skill searches session tools for: mcp__*__execute_sql
        ↓
6. Found: mcp__olytic-telemetry__execute_sql  (the org's MCP connector)
        ↓
7. Calls: INSERT INTO telemetry_events (...) VALUES (...)
        ↓
8. MCP connector forwards the call to Supabase
        ↓
9. Supabase RLS checks: does org_id in the INSERT match the JWT claim?
        ↓
10. Row stored in telemetry_events table (zero delay)
        ↓
11. Event is now available for future analysis and optimization
```

Everything from step 3 onward is **invisible to the user**. No confirmation, no narration, no visible tool call output.

---

## What Gets Logged: The Nine Event Types

Every plugin must be capable of logging all nine event types. Not every event fires in every session — they fire when the right condition is met.

| Event | When It Fires |
|-------|---------------|
| `skill_invoke` | A skill is loaded and used |
| `agent_trigger` | An agent is activated |
| `command_execute` | A slash command is run |
| `violation` | A user request conflicts with a plugin's declared constraints |
| `feedback` | User signals meaningfully positive or negative reaction |
| `decision_trace` | Plugin makes a substantive recommendation or chooses between approaches |
| `verification_gate` | A write operation is performed and then verified |
| `not_found_reported` | A requested file, path, or data point doesn't exist |
| `permission_gate` | Plugin requests user confirmation before a destructive or bulk action |

---

## How the MCP Connector Is Installed

The connector lives in the Claude desktop config file — **not** inside any plugin folder. Its location on the filesystem is:

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

The relevant block looks like this:
```json
"olytic-telemetry": {
  "command": "/opt/homebrew/bin/npx",
  "args": [
    "-y",
    "@supabase/mcp-server-supabase@latest",
    "--project-ref",
    "kxnmgutidehncnafrwbu",
    "--supabase-access-token",
    "sbp_173d82e4ab04962d954bcd0412a72f07b5a142dd"
  ]
}
```

The path to `npx` may vary by machine. Run `which npx` in Terminal to find yours. See `claude_desktop_config_options.md` in this folder for pre-built config options for common setups (Homebrew Intel vs. Apple Silicon).

**Why this location?** Claude needs to be able to find the connector. The `claude_desktop_config.json` file is what Claude Desktop reads at startup to discover available MCP servers. Installing it here makes the connector available in every Cowork session automatically — the user doesn't have to do anything per session.

---

## The Multi-Tenant Model (Current and Future Clients)

The same Supabase database serves all organizations. Data isolation is enforced entirely through Row Level Security (RLS). Here's how it works:

1. Each org gets a unique `org_id` (e.g., `olytic-internal`, `client-acme`)
2. A JWT is minted for each org, encoding their `org_id` as a claim
3. The org's MCP connector is configured with that JWT (via their personal access token)
4. When a plugin inserts a row, it includes `org_id` in the INSERT
5. Supabase's RLS `plugin_insert` policy checks that `org_id` in the INSERT matches the JWT claim
6. Reads are also scoped — an org can only query their own rows

This means even if two clients use the same Supabase project, they can never see each other's data. Their telemetry is logically isolated at the database level.

See `olytic-internal-connector-setup.md` for the JWT minting script and setup instructions for adding future client orgs.

---

## Local Plugins vs. Remote (Organizational) Plugins

This is one of the most common sources of confusion. There are two different ways Claude plugins can be delivered, and they behave differently:

### Local Plugins (Folder-Mounted)
- Plugin files live in a folder on your computer
- That folder is mounted in a Claude Cowork session as the workspace folder
- Claude reads the skill files from that local folder during the session
- **You can only have one folder mounted at a time in Cowork**
- **You cannot switch which folder is mounted mid-session**
- This is typically used during plugin development and testing

### Remote (Organizational) Plugins
- Plugins are packaged as `.zip` files and uploaded to the Olytic marketplace
- They're distributed to users as organizational plugins through the Claude interface
- Claude loads them automatically when a session starts, without any folder mounted
- These show up as the plugins available under your organization in Claude

**Why this matters for telemetry:** The MCP connector setup must be in the machine-level `claude_desktop_config.json` regardless of which plugin delivery method is used. The connector is not inside any plugin folder — it's a machine-level configuration. This means it works for both local and remote plugins, as long as it's been installed correctly on that machine.

---

## Known Issues and Open Problems

This section documents current gaps in the implementation. It will be updated as issues are resolved.

### Issue 1: Plugin Cache Not Auto-Refreshing
**What happens:** After uploading a new version of an organizational plugin, Claude may continue using the old cached version in existing sessions.

**Why:** Claude caches organizational plugin content for performance. Starting a new session doesn't always clear this cache.

**Workaround:** Delete the plugin cache directory on your drive, then restart Claude to force a fresh load. (Cache location TBD — to be documented once confirmed.)

**Status:** Open. Need to identify exact cache path and document the clear procedure.

---

### Issue 2: Claude Confuses Local vs. Remote Plugin Context
**What happens:** When working with Aulë or other plugins, Claude sometimes acts as if it's reading from a locally-mounted folder when it's actually running organizational plugins (or vice versa). This leads to file path confusion, wrong skill loading, or Claude looking for files that aren't where it expects them.

**Why:** Claude has no built-in signal distinguishing "this skill came from a mounted local folder" vs. "this skill came from an organizational plugin." It infers from context, and gets it wrong sometimes.

**Workaround:** Explicitly state in your prompt which context you're working in: "I have the [plugin-name] folder mounted locally" or "I'm using the organizational version of this plugin."

**Status:** Open. No clean fix; requires prompt discipline and clearer framing in skill files.

---

### Issue 3: Cowork Cannot Mount Multiple Folders
**What happens:** You cannot have two different folders mounted simultaneously in a Cowork session. For example, you cannot mount both the plugins-workspace folder AND a client's content folder at the same time.

**Why:** This is a Cowork platform constraint. The tool only supports a single mounted workspace directory per session.

**Impact:** Any workflow that requires access to files in two different locations requires either copying files to a single folder, or running separate sessions.

**Status:** Platform limitation. No workaround currently. File a product feedback item with Anthropic if this becomes a frequent blocker.

---

### Issue 4: Gaudi Uses Global Supabase Connector, Not the Plugin MCP
**What happens:** Gaudi (the data platform plugin) currently has access to the global Supabase connector because the developer also has Supabase connected via Claude's general integrations. When Gaudi uses this to insert telemetry, it may appear to work — but it's not the same as telemetry flowing through the org-scoped MCP connector as designed.

**Why this is a problem:** Using the global Supabase connector bypasses the org_id-scoped JWT and the RLS enforcement. Even if rows appear in Supabase, they may be inserted with incorrect or missing `org_id` values, which will cause them to be rejected when RLS is fully enforced — or worse, mixed in with data from other contexts.

**What "verified" really means:** Gaudi inserting a row via the global connector does NOT prove the full telemetry pipeline works. It only proves that direct Supabase access works. The end-to-end proof requires: a plugin's telemetry skill discovers `mcp__olytic-telemetry__execute_sql`, calls it, and a row lands in `telemetry_events` with the correct `org_id = 'olytic-internal'`.

**Status:** Open. Need a dedicated smoke test procedure using only the org-scoped connector. See `olytic-internal-connector-setup.md` for the smoke test SQL.

---

### Issue 5: Existing Plugin Telemetry Skills Are Not at v2.2.0
**What happens:** The TELEMETRY-STANDARDS were updated to v2.2.0 on 2026-03-04, requiring `org_id` and `user_id` on every INSERT. Existing plugin telemetry skills (Gaudi, The One Ring, Magneto, Aulë) were generated before this update and may not include these fields in their INSERT patterns.

**Impact:** Inserts from non-compliant skills will be rejected by Supabase RLS.

**What needs to happen:** Each plugin's `plugin-telemetry/SKILL.md` needs to be updated to include `org_id` and `user_id` in INSERT statements, and frontmatter needs to be updated to declare `telemetry_blueprint: "TELEMETRY-STANDARDS.md v2.2.0"`.

**Status:** Open. Audit needed across: Gaudi, The One Ring, Magneto, Aulë. See Section 12 of `TELEMETRY-STANDARDS.md` for the compliance checklist.

---

### Issue 6: MCP Connector Package Fails to Start (CRITICAL BLOCKER)
**What happens:** The `@supabase/mcp-server-supabase@latest` package hangs indefinitely with zero output or error messages when invoked via npx. The connector never establishes a connection and shows as "grey/disconnected" in Claude Desktop, despite correct config.

**Environment:** Node v20.20.0 (nvm), npm 10.8.2, config path: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Symptoms:**
- Claude Desktop shows olytic-telemetry connector with grey circle (not green)
- After full Claude restart, connector remains disconnected
- Direct command execution: `/path/to/npx -y @supabase/mcp-server-supabase@latest --project-ref kxnmgutidehncnafrwbu --access-token [token]` produces zero output and hangs indefinitely
- No error messages, no debug output, must Ctrl+C to exit

**Impact:** Layer 5 (plugin skill telemetry) completely broken. Layers 1–4 work fine — database is reachable, schema is correct, direct INSERTs work, and the connector *can* be used when Claude is explicitly directed to use it. But plugin skills cannot autonomously fire telemetry because the MCP connector isn't running to be discovered at runtime.

**What we've ruled out:**
- Config path is correct
- npx path matches `which npx` output exactly
- Service role JWT token was used (old JWT token was invalid, replaced with fresh Supabase-generated service role key)
- npm cache cleared
- Full Claude restarts performed
- Plugin source and zip files both reference the correct connector name by exact spelling
- Nothing is wrong with the skill code itself

**Root cause theories:**
1. **Most likely:** `@supabase/mcp-server-supabase@latest` has a bug or critical incompatibility that prevents startup
2. **Possible:** The package is trying to reach Supabase at startup and silently timing out
3. **Possible:** Node v20.20.0 has compatibility issues with the package
4. **Possible:** The specific version of the package available on npm is broken

**Next steps for future investigation:**
1. Pin to a specific stable version instead of `@latest` — try older known-good versions (e.g., `@supabase/mcp-server-supabase@1.0.0`)
2. Enable verbose debugging: `DEBUG=* npx -y @supabase/mcp-server-supabase@latest ...`
3. Check npm registry at https://www.npmjs.com/package/@supabase/mcp-server-supabase for known issues, deprecations, or breaking changes
4. Try alternative Supabase MCP packages if one exists (search npm for `supabase mcp`)
5. Implement a custom minimal MCP connector in Node.js if the package cannot be fixed
6. Test on another Mac to determine if issue is machine-specific or systemic

**DO NOT spend more time troubleshooting the `@supabase/mcp-server-supabase@latest` package itself without first trying a pinned version or checking the npm registry for known issues.** The hanging-with-zero-output behavior suggests a fundamental package problem, not a config or credential issue.

**Workaround (temporary):** Manual telemetry logging is possible by explicitly running SQL inserts via Supabase, but this defeats the purpose of autonomous plugin telemetry. Use this only for critical diagnostics, not as a permanent solution.

**Status:** CRITICAL BLOCKER. This is the primary blocker preventing end-to-end telemetry verification (Layer 5). Resolving this is higher priority than Issue 5 (plugin compliance), because Issue 5 is moot if the connector doesn't run.

**Referenced in:** `TELEMETRY-TESTING.md` → "Known Issue: MCP Connector Startup Failure (2026-03-04)"

---

## Source of Truth Hierarchy

When there's a conflict between files about how telemetry should work, use this hierarchy:

1. **`TELEMETRY-STANDARDS.md`** — canonical specification (owned by Aulë)
2. **`aule/skills/plugin-generation/references/telemetry-template.md`** — the template Aulë uses when generating new plugins (must match the standard)
3. **Individual plugin `plugin-telemetry/SKILL.md` files** — each plugin's local copy (must reference the standard version they implement)

If the standard changes, update it first, then the template, then propagate to individual plugins on their next planned update.

---

## Reference Files in This Folder

| File | Purpose |
|------|---------|
| `TELEMETRY-STANDARDS.md` | Canonical telemetry specification (v2.2.0) |
| `TELEMETRY-ARCHITECTURE.md` | This file — overview and troubleshooting |
| `olytic-internal-connector-setup.md` | MCP connector config, JWT details, smoke test, client onboarding pattern |
| `claude_desktop_config_options.md` | Pre-built config blocks for different Node.js install paths |
| `troubleshoot-mcp-connector.md` | Debug prompt for a broken connector (flag mismatch error) |
