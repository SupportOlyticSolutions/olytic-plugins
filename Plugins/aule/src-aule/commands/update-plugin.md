---
description: Guided workflow to audit and update a plugin to current Aule standards — always finishes with a full verifier run and repackage
argument-hint: "[plugin-name or 'all'] (e.g., magneto, the-one-ring, all)"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
---

# /update-plugin

Runs a structured, user-guided workflow to bring one or more plugins up to current Aule standards. **Never makes changes silently.** Always presents findings before touching files. Always ends with a full verifier run and repackage — no exceptions.

---

## Step 1: Locate Target(s)

Parse `$ARGUMENTS`:
- If a specific plugin name: find `src-[name]/` in the workspace. If not found, report "Not Found" and list what is available.
- If `all` or empty: glob for all `src-*/` plugin directories in the workspace and process each in sequence.

Acknowledge the target(s) before proceeding:
> "Auditing **[plugin-name]** against current Aule standards. I'll show you what needs fixing before making any changes."

---

## Step 2: Audit

Run a full compliance scan against the plugin. Perform every check from the `aule-verifier` skill — fetch all schemas at runtime via `olytic-core-schemas`:

```
invoke skill: olytic-core-schemas
schema: plugin-identity
```
```
invoke skill: olytic-core-schemas
schema: telemetry-event
```
```
invoke skill: olytic-core-schemas
schema: hook-event
```

Checks to run:

**2.1 plugin.json Validity**
- `name` present, kebab-case, matches folder name
- `version` present, valid semver
- `description` present, ≤120 characters
- `author` with `name` and `email`
- `hooks` field present if `hooks/hooks.json` exists
- No `connectors` key (upload blocker)
- No unrecognised keys

**2.2 Required Components**
- `.claude-plugin/plugin.json` exists
- At least one `skills/*/SKILL.md` exists
- A telemetry skill (`skills/*telemetry*/SKILL.md`) exists
- `README.md` exists
- `hooks/hooks.json` exists if hooks are declared

**2.3 Telemetry Skill Compliance**
- All 8 event types referenced: `skill_invoke`, `decision_trace`, `feedback`, `violation`, `not_found_reported`, `verification_gate`, `permission_gate`, `agent_trigger`
- Transport is Olytic Memory MCP (`write_memory`) — not HTTP POST, not file-write
- `olytic-core-schemas` invoked at runtime with `schema: telemetry-event` (not baked-in)
- `session_id_required: true` in frontmatter

**2.4 Schema Conformance — Memory Access**
- If `memory_scope: persistent` declared anywhere: verify `memory_access_control`, `memory_access_readers` (if shared), `memory_access_justification` (if non-private)

**2.5 No Connectors in plugin.json**
- `connectors` key absent — flag High severity if present (upload blocker)

**2.6 Hook Declarations**
- Hook event types from canonical list only: `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SessionClose`
- All matchers are valid regex
- `hooks` field in `plugin.json` matches `hooks/hooks.json`

**2.7 Session Summarizer (persistent plugins only)**
- `SessionClose` hook present
- Session summarizer skill invokes `olytic-core-schemas` with `schema: session-summary` and `schema: vault-entry`

**2.8 Package Integrity**
- `[name].plugin` file exists alongside `src-[name]/`
- Zip contains exactly one `plugin.json`
- `plugin.json` is at root level (not prefixed with `src-[name]/`)
- Version inside zip matches version in `src-[name]/.claude-plugin/plugin.json`
- Extension is `.plugin` not `.zip`

---

## Step 3: Present Findings

**Do not make any changes yet.** Present the full audit report:

```
Audit Report — [plugin-name] — [timestamp]
Standards version: [aule version]

plugin_json_valid:       [PASS / FAIL — details]
required_components:     [PASS / FAIL — details]
telemetry_compliance:    [PASS / FAIL — details]
schema_conformance:      [PASS / N/A — details]
connector_declarations:  [PASS / FAIL — details]
hook_declarations:       [PASS / FAIL — details]
session_summarizer:      [PASS / N/A — details]
package_integrity:       [PASS / FAIL / WARN — details]

Failures: [n]
Warnings: [n]
```

For each failure, state:
- What is wrong (specific file and field)
- What the fix is
- Severity: **High** (upload blocker) / **Medium** (standards violation) / **Low** (best practice)

Then ask:
> "Ready to apply all fixes? Or would you like to review or skip any specific change?"

- If user says **apply all**: proceed to Step 4 applying every fix.
- If user wants to **review**: walk through each fix one at a time, confirming before applying.
- If user wants to **skip** specific fixes: note them as "acknowledged, not applied" and proceed with the rest.

If there are **zero failures**: skip to Step 5 (verifier + repackage) and report the plugin is already compliant.

---

## Step 4: Apply Fixes

Apply only the approved fixes. For each fix:
1. State what you are about to change: *"Updating `plugin.json` description from 239 chars to 118 chars…"*
2. Make the edit
3. Confirm: *"Done."*

Never batch-apply silently. Each fix is narrated before it happens.

**Fix patterns by check:**

- `description` too long → truncate to ≤120 chars preserving meaning
- `connectors` key present → remove the key entirely
- Telemetry transport is HTTP POST → rewrite `How to Write Logs` section to use `write_memory` MCP tool pattern per the canonical telemetry template
- `olytic-core-schemas` not invoked → add runtime fetch block to telemetry skill opening
- `session_id_required` missing → add to telemetry skill frontmatter
- Missing telemetry skill → scaffold from telemetry template (`skills/plugin-generation/references/telemetry-template.md`)
- Missing `hooks` field in `plugin.json` → add with correct path
- Invalid hook event types → correct to canonical list
- Package stale or missing → will be resolved in Step 5

---

## Step 5: Run Full Verifier

After all fixes are applied (or if no fixes were needed), run the complete `aule-verifier` scan against the updated source. This is not optional — run it even if no changes were made.

Report the full compliance output as in Step 3. Expected result: all checks PASS.

If any check still fails after fixes:
- Diagnose the remaining issue
- Apply the additional fix
- Re-run the verifier
- Repeat until all checks pass

Do not proceed to Step 6 until the verifier is clean.

---

## Step 6: Repackage

**Mandatory — always runs, even if the only change was a one-line text fix.**

```bash
cd [plugin-path]/src-[name]/
zip -r /tmp/[name].zip . --exclude "*/.DS_Store" --exclude ".DS_Store"
cp /tmp/[name].zip [plugin-path]/[name].plugin
```

Confirm:
- File exists at `[plugin-path]/[name].plugin`
- Exactly one `plugin.json` in the zip: `unzip -l [name].plugin | grep plugin.json`
- `plugin.json` at root (no `src-[name]/` prefix in path)
- Version in zip matches source version

Report:
> "✅ [plugin-name] v[version] — fully compliant, packaged at [path]/[name].plugin ([size]). Ready to upload."

---

## Step 7: If `all` Was Specified

Repeat Steps 2–6 for each plugin in sequence. After all plugins are processed, present a summary:

```
Update Run Complete — [timestamp]

✅ magneto         v0.2.0 — 2 fixes applied, repackaged
✅ the-one-ring    v1.0.0 — already compliant, repackaged
❌ gaudi           v0.3.0 — 1 fix failed (see details above)

Plugins ready to upload: 2/3
```

---

Telemetry: This command logs all invocations via aule-telemetry.
