---
name: aule-verifier
description: >
  Compliance scanner. Reads every plugin in workspace.json and checks each against current Olytic
  plugin standards: required components present, plugin.json Identity Block valid, schema compliance,
  hook declarations, telemetry skill present, connector declarations match. Emits a structured
  compliance report. Never writes — detect only. Optionally hands off failing plugins to trashbot
  for remediation. Invoke with: "verify all plugins", "check plugin compliance", "audit plugins",
  "run aule-verifier", or via the verify-plugins command. Runs daily via scheduled-verifier.
version: 0.1.0
---

# Aule Verifier — Compliance Scanner

Reads every plugin in `workspace.json` and produces a structured compliance report. **This skill is detect-only — it never modifies files.**

---

## What This Skill Does

1. **Reads** `workspace.json` to get the list of all installed plugins
2. **Scans** each plugin's source folder against the current Olytic plugin standards
3. **Emits** a structured compliance report with pass/fail status per plugin per check
4. **Optionally hands off** failing plugins to trashbot if `--fix` is requested

---

## Standards This Skill Checks

### 1. plugin.json Validity

Fetch the authoritative field list at runtime:
```
invoke skill: olytic-core-schemas
schema: plugin-identity
```

Required checks:
- `name` present, kebab-case, matches folder name
- `version` present, valid semver
- `description` present, ≤120 characters
- `author` present with `name` and `email`
- `hooks` field present if any hook files exist
- No `connectors` key present (the Claude validator requires connector URLs — org-installed MCP servers are documented in skill instructions instead)

### 2. Required Components

Every plugin must have:

| Component | Path | Required |
|-----------|------|----------|
| `plugin.json` | `.claude-plugin/plugin.json` | Mandatory |
| At least one skill | `skills/*/SKILL.md` | Mandatory |
| Telemetry skill | `skills/*telemetry*/SKILL.md` | Mandatory |
| README | `README.md` | Mandatory |
| Hooks config | `hooks/hooks.json` | If any hooks declared |

### 3. Telemetry Skill Compliance

For each plugin's telemetry skill:
- Verify it references the 8 canonical event types: `skill_invoke`, `decision_trace`, `feedback`, `violation`, `not_found_reported`, `verification_gate`, `permission_gate`, `agent_trigger`
- Verify it uses HTTP POST transport to Olytic Gateway (not file-write)
- Verify it invokes `olytic-core-schemas` skill with `schema: telemetry-event` at runtime (skill-invocation pattern — not a filesystem read, not baked-in)

### 4. Schema Conformance — Memory Access

If plugin has `memory_scope: persistent` in any skill:
- Verify `memory_access_control` is declared (`private`, `shared`, or `org-wide`)
- If `shared`: verify `memory_access_readers` list is present
- If not `private`: verify `memory_access_justification` is present

### 5. No Unrecognized Keys in plugin.json

The Claude org plugin uploader enforces a strict whitelist of keys. Any unrecognized key causes an upload failure. The following keys are confirmed blockers and must not appear in `plugin.json`:

| Blocked Key | Reason | Severity |
|-------------|--------|----------|
| `connectors` | Validator requires valid `http://` or `https://` URLs — org-installed MCP servers cannot provide these at build time | High (upload blocker) |
| `dependencies` | Not in the validator's recognized key whitelist — rejected on upload | High (upload blocker) |

Rules:
- Verify `plugin.json` does NOT contain `connectors` or `dependencies` keys
- If either is present, flag as **High severity** (upload blocker) and remove it
- MCP server dependencies and plugin inter-dependencies should be documented in skill/agent instructions, not declared in `plugin.json`
- When new upload errors citing "Unrecognized key" are encountered, add that key to this blocked list

### 6. Hook Declarations

- Verify hooks listed in `plugin.json` `hooks` field match the `hooks/hooks.json` file structure
- Verify hook matchers are valid regex patterns
- Verify hook event types are from the canonical list (PostToolUse, UserPromptSubmit, SessionClose, PreToolUse)
- Invoke `olytic-core-schemas` skill with `schema: hook-event` at runtime for authoritative hook structure

### 7. Session Summarizer (Persistent Plugins Only)

For plugins with `memory_scope: persistent`:
- Verify a session summarizer skill exists (`SessionClose` hook present)
- Verify it invokes `olytic-core-schemas` skill with `schema: session-summary` at runtime
- Verify it invokes `olytic-core-schemas` skill with `schema: vault-entry` at runtime

### 8. Package Integrity

For each plugin, **both** `[name].plugin` and `[name].zip` must exist alongside the source folder. These are **always required together** — one without the other is a failure.

- **Both files exist:** Verify `[name].plugin` AND `[name].zip` are present alongside the source folder. If either is missing, flag as **High severity** — they must always be produced together. `.plugin` is required for org plugin upload; `.zip` is required for distribution and non-plugin-runtime platforms.
- **Exactly one `plugin.json`:** Unzip and count `plugin.json` entries in `.plugin` (and optionally `.zip`). Must be exactly 1. If 2+ are found, the zip was built from the wrong directory level (parent instead of inside `src-[name]/`) — flag as **High severity** (upload blocker).
- **Built from correct root:** Confirm the zip contains `.claude-plugin/plugin.json` at the root (not `src-[name]/.claude-plugin/plugin.json`). If the path includes the `src-[name]/` prefix, the zip is stale and must be rebuilt from inside `src-[name]/`.
- **In sync with source:** Compare the `version` field inside the zipped `plugin.json` against `src-[name]/.claude-plugin/plugin.json`. If they differ, the package is stale — flag as **Medium severity**.
- **Both files in sync with each other:** Verify `[name].plugin` and `[name].zip` have identical file sizes. If they differ, they were built at different times — flag as **High severity** and rebuild both.

```python
import zipfile, json, os

def check_package(plugin_path, plugin_name):
    plugin_file = f"{plugin_path}/{plugin_name}.plugin"
    zip_file = f"{plugin_path}/{plugin_name}.zip"
    src_json_path = f"{plugin_path}/src-{plugin_name}/.claude-plugin/plugin.json"
    failures = []

    # Both files must exist — no exceptions
    if not os.path.exists(plugin_file):
        failures.append(f"{plugin_name}.plugin not found — ALWAYS required for org plugin upload")
    if not os.path.exists(zip_file):
        failures.append(f"{plugin_name}.zip not found — ALWAYS required alongside .plugin")

    if failures:
        return {"status": "fail", "reason": "; ".join(failures)}

    # Both files must be identical in size (same archive, different extension)
    plugin_size = os.path.getsize(plugin_file)
    zip_size = os.path.getsize(zip_file)
    if plugin_size != zip_size:
        return {"status": "fail", "reason": f"{plugin_name}.plugin ({plugin_size}B) and {plugin_name}.zip ({zip_size}B) are different sizes — they were built at different times, rebuild both"}

    # Verify archive integrity using .plugin
    with zipfile.ZipFile(plugin_file) as z:
        names = z.namelist()
        plugin_json_entries = [n for n in names if n.endswith('plugin.json')]

        if len(plugin_json_entries) != 1:
            return {"status": "fail", "reason": f"zip contains {len(plugin_json_entries)} plugin.json files (expected 1) — rebuild from inside src-{plugin_name}/"}

        if any(f"src-{plugin_name}/" in e for e in plugin_json_entries):
            return {"status": "fail", "reason": f"zip built from wrong directory — plugin.json path includes src-{plugin_name}/ prefix, rebuild from inside src-{plugin_name}/"}

        with z.open(plugin_json_entries[0]) as f:
            zipped_version = json.load(f).get('version')

    if os.path.exists(src_json_path):
        src_version = json.load(open(src_json_path)).get('version')
        if zipped_version != src_version:
            return {"status": "warn", "reason": f"package version {zipped_version} does not match source version {src_version} — rebuild needed"}

    return {"status": "pass"}
```

Report output additions for this check:

```json
"package_integrity": "pass"
// or
"package_integrity": "fail — magneto.zip not found — ALWAYS required alongside .plugin"
// or
"package_integrity": "fail — magneto.plugin (71680B) and magneto.zip (70400B) are different sizes — rebuild both"
// or
"package_integrity": "warn — package version 0.1.0 does not match source version 0.2.0"
```

---

## How to Run a Scan

```python
import os, json, re

workspace = json.load(open('workspace.json'))
plugins = workspace.get('plugins', [])

report = {
    'scan_timestamp': '<ISO 8601 UTC>',
    'total_plugins': len(plugins),
    'passing': 0,
    'failing': 0,
    'results': []
}

for plugin in plugins:
    plugin_path = plugin.get('path', '')
    src_path = f"{plugin_path}/src-{plugin['name']}"
    result = scan_plugin(src_path, plugin['name'])
    report['results'].append(result)
    if result['status'] == 'pass':
        report['passing'] += 1
    else:
        report['failing'] += 1
```

---

## Output — Compliance Report Format

```json
{
  "scan_timestamp": "2026-01-01T00:00:00Z",
  "standards_version": "0.3.0",
  "total_plugins": 4,
  "passing": 3,
  "failing": 1,
  "results": [
    {
      "plugin": "gaudi",
      "status": "pass",
      "checks": {
        "plugin_json_valid": "pass",
        "required_components": "pass",
        "telemetry_compliance": "pass",
        "schema_conformance": "pass",
        "connector_declarations": "pass",
        "hook_declarations": "pass",
        "package_integrity": "pass"
      }
    },
    {
      "plugin": "magneto",
      "status": "fail",
      "checks": {
        "plugin_json_valid": "pass",
        "required_components": "fail",
        "telemetry_compliance": "fail",
        "schema_conformance": "pass",
        "connector_declarations": "pass",
        "hook_declarations": "pass",
        "package_integrity": "fail"
      },
      "failures": [
        "required_components: telemetry skill missing",
        "telemetry_compliance: cannot verify — telemetry skill absent",
        "package_integrity: magneto.plugin not found — cannot upload as org plugin"
      ]
    }
  ]
}
```

---

## --fix Mode (Remediation Handoff)

When invoked with `--fix` (via `verify-plugins --fix`):

1. Complete the full compliance scan as normal
2. Collect all failing plugins into a remediation list
3. Hand off to trashbot: *"Aule-verifier scan found [N] failing plugins: [names]. Run a targeted sweep on each and apply current standards."*
4. Do NOT modify any files directly — trashbot handles remediation

---

## Scheduled Operation

This skill runs daily via `scheduled-verifier`. On scheduled runs:
- Full scan of all plugins in workspace.json
- Write results to `telemetry` via Olytic Gateway (event type: `verification_gate`)
- If failures found: emit a `violation` event with `violation_type: "compliance_failure"` listing failing plugins
- Do NOT auto-fix on scheduled runs — remediation requires explicit user intent or trashbot invocation

---

## Operating Principles

- **Read-only:** Never modify any plugin file during a scan
- **Runtime-fetched schemas:** Invoke `olytic-core-schemas` skill for all schema lookups at invocation — do not read filesystem paths, do not bake in field lists. This works whether olytic-core is mounted or installed as an Organizational Plugin.
- **Complete report:** Always report all checks for all plugins, not just failures
- **Standards version pinning:** Include the Aule version used for the scan in every report
- **No hallucination:** If a file is missing, report the specific path as missing — do not assume its contents

Telemetry: This skill logs all invocations via aule-telemetry.
