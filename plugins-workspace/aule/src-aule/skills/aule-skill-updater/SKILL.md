---
name: aule-skill-updater
description: >
  Automatically updates plugin-generation/SKILL.md when plugin standards change. Reads reference
  files as source of truth, identifies what changed, and intelligently updates the generation skill
  to include new requirements. Invoked automatically by aule-change-analyzer when a generation
  requirement is detected. Ensures Aule's generation logic is always in sync with reference documentation.
---

# Aule Skill Updater

Automatically keeps plugin-generation/SKILL.md in sync with reference documentation.

## Core Principle

**"Aule's generation logic is always derived from its reference documentation."**

This skill implements that principle by:
1. Reading changed reference files
2. Understanding what changed
3. Automatically updating SKILL.md to include the new requirement
4. Validating the updated file
5. Logging what was changed

## What This Skill Does

When called with a reference file path:

1. **Reads** the changed reference file
2. **Identifies** what needs updating in SKILL.md
3. **Locates** the corresponding section
4. **Updates or injects** new content
5. **Validates** the updated file
6. **Logs** what was changed

## Reference File → SKILL.md Mapping

| Reference File | Target SKILL.md Section | Update Type |
|---|---|---|
| `hooks-configuration.md` | Step 4: hooks/hooks.json | Add/Update template |
| `component-templates.md` | Step 4: Component generation | Update all components |
| `telemetry-template.md` | Step 4.X + Step 5 | Update telemetry specs |
| `olytic-patterns.md` | Naming Conventions | Update examples |

## Update Algorithm

```
1. Read reference file
2. Identify what's new/changed
3. Find target section in SKILL.md
   - If section exists: Update it
   - If section doesn't exist: Inject it
4. Preserve existing content
5. Merge new content
6. Validate Markdown syntax
7. Verify all placeholders present
8. Write updated SKILL.md to disk
9. Log what was changed
```

## Inputs and Outputs

### Input (from aule-change-analyzer)

The skill receives:
- `changed_file_path` — Absolute path to reference file that changed

### Output

**To filesystem:**
- Updated `plugin-generation/SKILL.md` with new requirements

**To logs:**
```
event: "skill_updated"
description: "Updated plugin-generation/SKILL.md for [file] changes"
changes_made: "[what was updated]"
validation_result: "pass|fail"
```

## Failure Modes and Recovery

### Failure 1: Reference File Can't Be Read
```
→ Log error: "Cannot read reference file: [path]"
→ Don't update SKILL.md
→ Return error
```

### Failure 2: Target Section Not Found
```
→ Log warning: "Could not locate [section] in SKILL.md"
→ Attempt safe injection at end of file
→ If successful: Log what was injected
→ If unsuccessful: Return error
```

### Failure 3: Update Creates Invalid Markdown
```
→ Validate updated content
→ If invalid: Revert changes
→ Log error: "Validation failed. SKILL.md reverted."
```

### Failure 4: Placeholder Removal
```
→ Before updating: Scan for placeholders like [PLUGIN_NAME]
→ After updating: Verify all still exist
→ If any missing: Revert update
→ Log error: "Placeholder removed. Reverted."
```

## Key Design Principles

1. **Reference Files are Source of Truth:** Always read from references; never hardcode
2. **Preserve Existing Content:** Updates add or modify, never destroy unrelated sections
3. **Validate Before Persisting:** Always validate before writing to disk
4. **Graceful Degradation:** If update fails, SKILL.md is unchanged
5. **Clear Audit Trail:** Log every change for transparency

## Example: Complete Flow

**What the user does:**
1. Creates `references/hooks-configuration.md`
2. Documents: "Every plugin must configure hooks"

**What happens automatically:**
1. PostToolUse hook detects file
2. aule-change-analyzer categorizes: "Generation Requirement"
3. aule-change-analyzer invokes aule-skill-updater
4. aule-skill-updater reads hooks-configuration.md
5. aule-skill-updater locates "Step 4: Generate Each File"
6. aule-skill-updater adds hooks/hooks.json subsection
7. aule-skill-updater copies requirements from reference
8. aule-skill-updater validates updated SKILL.md
9. aule-skill-updater writes updated file
10. aule-skill-updater logs: "Updated SKILL.md for hooks requirement"
11. aule-change-analyzer triggers trashbot
12. trashbot sweeps all plugins
13. Log: "✓ SKILL.md updated, ✓ Plugins swept, ✓ Ready for next generation"

**Result:**
- Reference file created ✓
- SKILL.md updated automatically ✓
- All plugins updated automatically ✓
- Next plugin will have hooks automatically ✓
- Zero manual work ✓
