---
name: aule-change-analyzer
description: >
  Detects when Aule plugin standards change and intelligently routes them to appropriate handlers.
  Invoked automatically via PostToolUse hook when Aule core files are modified. Analyzes the changed
  file, categorizes the change type (Generation Requirement, Reference Update, Schema Change), and
  routes to aule-skill-updater or just logs. This skill is the routing layer of Aule's self-updating
  architecture.
---

# Aule Change Analyzer

Detects when Aule plugin standards change and automatically routes changes to appropriate handlers.

## What This Skill Does

When an Aule standard file changes:

1. **Reads** the changed file to understand what changed
2. **Categorizes** the change into three types
3. **Routes** to appropriate handlers based on category
4. **Logs** the change for audit trail

## Change Categories and Actions

### Category 1: Generation Requirement

**What triggers this:**
- File describes something every plugin must have
- Keywords: "mandatory", "must", "every plugin"
- Examples: hooks-configuration.md, component-templates.md, telemetry-template.md

**What to do:**
- ✅ Invoke aule-skill-updater to update plugin-generation/SKILL.md
- ✅ Trigger trashbot to sweep all existing plugins
- ✅ Log: "Generation Requirement detected — updated SKILL.md and swept plugins"

### Category 2: Reference Update

**What triggers this:**
- Clarifications to existing patterns
- Keywords: "example", "best practice" (no structural change)
- Examples: olytic-patterns.md documentation updates

**What to do:**
- ✅ Just log it
- ℹ️ Log: "Reference Update detected — no generation changes needed"
- (Existing plugins don't need updating)

### Category 3: Schema Change

**What triggers this:**
- Changes to data structures
- Keywords: "new field", "schema", "breaking change"
- Examples: telemetry event schema changes

**What to do:**
- ✅ Invoke aule-skill-updater to update plugin-generation/SKILL.md
- ✅ Trigger trashbot to sweep all existing plugins
- ✅ Notify user (log prominently)
- ℹ️ Log: "Schema Change detected — updated SKILL.md, swept plugins, manual verification recommended"

## How to Determine the Category

### Step 1: Check the File Path

```
If path contains:
  "skills/plugin-generation/" → Category 1 (Generation Requirement)
  "references/hooks-configuration" → Category 1 (Generation Requirement)
  "references/component-templates" → Category 1 (Generation Requirement)
  "references/telemetry-template" → Category 1 (Generation Requirement)
  "references/olytic-patterns" → Category 2 (Reference Update)
  "references/agentic-best-practices" → Category 2 (Reference Update)
```

### Step 2: Read the File and Check Contents

**For Generation Requirement candidates:**

Look for language indicating mandatory:
- "MUST", "REQUIRED", "mandatory"
- "Every plugin should", "All plugins must"
- "This is required for all new plugins"

**For Reference Update candidates:**

Look for documentation language:
- "example", "for instance", "consider"
- "Best practice is to..."
- "You might also want to..."

## Routing Logic

### If Generation Requirement:

```
1. Log: "Generation Requirement detected: [file path]"
2. Invoke aule-skill-updater with file_path
3. Invoke trashbot with: "Aule standard changed. Sweep all plugins."
4. Log completion: "✓ Updated SKILL.md, ✓ Swept plugins"
```

### If Reference Update:

```
1. Log: "Reference Update detected: [file path]"
2. Log reason: "This is documentation only. No generation changes needed."
3. Exit
```

### If Schema Change:

```
1. Log: "⚠️ Schema Change detected: [file path]"
2. Invoke aule-skill-updater with file_path
3. Invoke trashbot with: "Aule schema changed. Full sweep required."
4. Log prominently: "⚠️ Schema change applied. Manual verification recommended."
```

## Key Design Principles

1. **Read First:** Always read the file before making routing decisions
2. **Smart Defaults:** If uncertain, default to Reference Update (safest)
3. **Audit Trail:** Log every decision for transparency
4. **Error Tolerance:** Failures don't stop the system
5. **Communicate:** Log what's happening for user visibility
