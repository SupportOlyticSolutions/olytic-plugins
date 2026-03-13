---
name: verify-plugins
description: >
  Manual trigger for aule-verifier. Runs a full compliance scan across all plugins in workspace.json
  and returns a structured report. Accepts an optional --fix flag to pass failing plugins to trashbot
  for remediation. Use when: "verify all plugins", "check if plugins are up to date", "audit plugin
  compliance", "run a plugin scan", "are plugins compliant?", "verify plugins --fix".
---

# verify-plugins

Runs a full compliance scan across all installed plugins and returns a report.

## Usage

```
verify-plugins          → full scan, report only
verify-plugins --fix    → full scan + hand failing plugins to trashbot
```

## What This Command Does

1. Invokes `aule-verifier` to scan all plugins in `workspace.json`
2. Returns the structured compliance report to the user
3. If `--fix` is passed: hands failing plugins to trashbot for remediation

## Execution

Say: *"Run aule-verifier against all plugins in workspace.json. Return the full compliance report. [If --fix was passed: also invoke trashbot for any failing plugins.]"*

## Output Format

```
Plugin Compliance Scan — [timestamp]
Standards version: [aule version]

✅ gaudi          — PASS (6/6 checks)
✅ the-one-ring   — PASS (6/6 checks)
❌ magneto        — FAIL (4/6 checks)
   ↳ telemetry skill missing
   ↳ connector declarations: olytic-gateway not declared in plugin.json

Summary: 3/4 passing
[If --fix]: Handing 1 failing plugin to trashbot for remediation...
```

## Notes

- This command never modifies plugin files directly
- `--fix` hands off to trashbot but does not wait for trashbot to complete before returning the scan report
- The scan fetches authoritative field definitions at runtime via `olytic-core-schemas` skill invocations — not filesystem reads
- Runs daily automatically via `scheduled-verifier`; use this command for on-demand scans
