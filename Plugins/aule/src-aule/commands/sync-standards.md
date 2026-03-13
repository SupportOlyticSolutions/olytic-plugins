---
name: sync-standards
description: >
  Manual trigger for aule-change-analyzer when a reference file is updated outside of a
  hook-detected write. Edge-case safety valve for when PostToolUse hooks don't fire (e.g., manual
  edits, external tool writes, bulk operations). Use when: "sync standards", "re-run change analyzer",
  "propagate changes", "sync aule standards", "the reference files changed, sync them", "force a
  standards sweep".
---

# sync-standards

Manual trigger for `aule-change-analyzer` when a reference file is updated outside of a hook-detected write.

## When to Use This

Normally, editing any Aule reference file automatically triggers `aule-change-analyzer` via the PostToolUse hook. Use `sync-standards` when:

- A file was modified by an external tool that didn't trigger the hook
- You're unsure whether the hook fired correctly
- You need to force a re-analysis after a bulk update
- A file was modified in a previous session and the hook didn't run

## Usage

```
sync-standards                           → analyze all recently changed Aule files
sync-standards [file-path]               → analyze a specific file
sync-standards --force-sweep             → skip analysis, go straight to trashbot
```

## What This Command Does

1. If a specific file path is given: invokes `aule-change-analyzer` with that file
2. If no file given: lists recently modified files in Aule source and references folders, asks user to confirm which to analyze
3. `aule-change-analyzer` determines change category (1/2/3) and routes to `aule-skill-updater` + trashbot if needed

## Execution

Say: *"Invoke aule-change-analyzer for [file path or 'recently modified Aule reference files']. Determine the change category and route appropriately."*

## Notes

- This command is a safety valve, not the primary mechanism — PostToolUse hooks handle the normal case
- If you're unsure what changed, use `verify-plugins` first to understand the current compliance state
- `--force-sweep` skips categorization and runs trashbot directly — use only when you know a sweep is needed
