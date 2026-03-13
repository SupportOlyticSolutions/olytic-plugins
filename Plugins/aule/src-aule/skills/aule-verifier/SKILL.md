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
- `connectors` array present if plugin declares external integrations

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
- Verify it uses HTTP POST transport to olytic-gateway (not file-write)
- Verify it invokes `olytic-core-schemas` skill with `schema: telemetry-event` at runtime (skill-invocation pattern — not a filesystem read, not baked-in)

### 4. Schema Conformance — Memory Access

If plugin has `memory_scope: persistent` in any skill:
- Verify `memory_access_control` is declared (`private`, `shared`, or `org-wide`)
- If `shared`: verify `memory_access_readers` list is present
- If not `private`: verify `memory_access_justification` is present

### 5. Connector Declarations

- If plugin's skills write to olytic-gateway, verify `olytic-gateway` appears in `plugin.json` `connectors`
- If plugin uses GitHub integration, verify `github` appears in `plugin.json` `connectors`
- Cross-check: connectors declared in `plugin.json` are subset of connectors available in `workspace.json`

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
        "hook_declarations": "pass"
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
        "hook_declarations": "pass"
      },
      "failures": [
        "required_components: telemetry skill missing",
        "telemetry_compliance: cannot verify — telemetry skill absent"
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
- Write results to `telemetry` via olytic-gateway (event type: `verification_gate`)
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
