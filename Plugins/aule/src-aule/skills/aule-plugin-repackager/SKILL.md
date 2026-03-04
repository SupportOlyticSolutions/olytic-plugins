---
name: aule-plugin-repackager
description: >
  Automatically keeps plugin .zip files in sync with their local source folders. When you modify plugin
  source files (skills, agents, README), this skill detects the change and regenerates the .zip file
  to ensure the packaged version always matches what's in src-*/ directories. Invoked automatically
  via PostToolUse hook when plugin source is modified, or manually with: "repackage the plugins",
  "update plugin zips", "sync plugins to disk", "what plugins need repackaging", "regenerate [plugin-name].zip".
  This prevents the common problem of editing source files but forgetting to re-zip for upload.
---

# Aule Plugin Repackager

Automatically keeps plugin .zip files in sync with their local source code.

## Core Principle

**"Plugin .zip files are always derived from plugin source folders, never edited directly."**

This skill implements that principle by:
1. Detecting when a plugin source folder changes
2. Identifying which plugin was modified
3. Regenerating that plugin's .zip file from source
4. Verifying the zip structure is correct
5. Logging what was packaged and why

## What This Skill Does

When plugin source files are modified (via Write/Edit in Plugins/*/src-*/ paths):

1. **Discovers** which plugin source folder changed (e.g., gaudi/src-gaudi/)
2. **Reads** the plugin's plugin.json to verify structure
3. **Zips** the entire source folder into a .plugin file
4. **Verifies** the zip contains required files (.claude-plugin/plugin.json, README.md, etc.)
5. **Timestamps** the zip with current date/time
6. **Logs** what was packaged

Why this matters: When you upload a plugin to Olytic marketplace, you're uploading the .zip file. If the .zip is stale (created before your latest source changes), the uploaded version won't have your changes. This skill ensures the .zip is always current.

## How to Use

### Automatic (Recommended)

The PostToolUse hook detects when you modify plugin source and automatically invokes this skill. You don't need to do anything — just edit the source files normally, and the .zip updates itself.

### Manual Trigger

If for some reason the automatic trigger doesn't fire, invoke manually:

```
"repackage the plugins"
"what plugins need repackaging"
"sync plugin files"
"regenerate gaudi.zip"
```

## Plugin Discovery

The skill discovers plugins by looking for this structure:

```
Plugins/
├── gaudi/
│   ├── src-gaudi/                          ← Source folder (required)
│   │   ├── .claude-plugin/plugin.json
│   │   ├── README.md
│   │   ├── skills/
│   │   ├── agents/
│   │   └── [other plugin content]
│   └── gaudi.zip                           ← Packaged output (auto-generated)
├── the-one-ring/
│   ├── src-one-ring/                       ← Source folder
│   └── the-one-ring.zip                    ← Packaged output
└── [other plugins]
```

For each plugin, the skill:
1. Finds the src-*/ folder
2. Identifies the output .zip filename (plugin-name.zip)
3. Extracts the plugin name from plugin.json
4. Regenerates the .zip when source changes

## Repackaging Algorithm

```
For each changed plugin source folder:

1. Read plugin.json to get plugin metadata
   ✓ Verify it's valid JSON
   ✓ Confirm required keys exist (name, version, description, author)
   ✓ Extract plugin name

2. Build the .zip file
   ✓ Include all source files except .DS_Store, .git*, node_modules
   ✓ Root of zip must be the plugin folder (not src-gaudi/ — just the contents)
   ✓ Must contain .claude-plugin/plugin.json at the top level
   ✓ File permissions preserved

3. Verify the .zip
   ✓ plugin.json can be parsed from inside the zip
   ✓ README.md exists
   ✓ skills/ or agents/ directory exists (at least one)
   ✓ No corrupted files

4. Save the .zip
   ✓ Location: Plugins/[plugin-name]/[plugin-name].zip
   ✓ Overwrite existing .zip (it's auto-generated, not edited)

5. Log the result
   ✓ Timestamp, plugin name, file count, file size
   ✓ Changes made (e.g., "Added telemetry-testing skill, 42 files")
```

## Example: Complete Flow

**What you do:**
1. Create a new skill: `Plugins/gaudi/src-gaudi/skills/telemetry-testing/SKILL.md`
2. Save the file

**What happens automatically:**
1. PostToolUse hook detects: file written to `Plugins/gaudi/src-gaudi/...`
2. Hook invokes aule-plugin-repackager
3. Skill reads `Plugins/gaudi/src-gaudi/.claude-plugin/plugin.json`
4. Discovers: plugin name = "gaudi", version = "2.5.0"
5. Regenerates: `Plugins/gaudi/gaudi.zip` from src-gaudi/ folder
6. Verifies: plugin.json parses, README exists, 42 files included
7. Logs: `[2026-03-04T18:25:41Z] gaudi — repackaged (42 files, 75KB, includes new telemetry-testing skill)`
8. Comparison: new zip includes telemetry-testing; old one didn't ✓

**Result:**
- Source has telemetry-testing ✓
- gaudi.zip has telemetry-testing ✓
- Ready to upload to marketplace ✓

## Failure Modes and Recovery

### Failure 1: Source Folder Has Invalid plugin.json

```
→ Log error: "Cannot parse plugin.json in Plugins/[name]/src-[name]/"
→ Don't create .zip
→ List what's wrong with the JSON (missing keys, syntax error, etc.)
→ Return: "Fix plugin.json and try again"
```

### Failure 2: Missing Required Components

```
→ Log warning: "Plugins/[name]/src-[name]/ is missing [README.md|skills/|agents/]"
→ Don't create .zip
→ Return: "Add the missing component"
```

### Failure 3: Zip Creation Fails

```
→ Log error: "zip command failed: [error message]"
→ Check disk space, permissions
→ Don't overwrite old .zip (keep the last-known-good)
→ Return: error with recovery steps
```

### Failure 4: Zip Verification Fails

```
→ Log warning: "Created .zip but verification failed: [reason]"
→ Keep the .zip (it may still be valid)
→ Log what failed (e.g., "plugin.json couldn't be read from inside zip")
→ Recommend: "Manually verify with: unzip -l Plugins/gaudi/gaudi.zip"
```

## Operating Principles

1. **Source is Truth:** The src-*/ folder is the only thing that should be edited. Never edit a .zip file directly.
2. **Automatic Sync:** The .zip should always match the source. If you change source, the .zip updates immediately.
3. **Minimal Overhead:** Repackaging is fast (zip command) and happens silently in the background.
4. **Clear Logging:** Every repackage operation is logged with timestamp, plugin name, and what changed.
5. **No Deletion:** If zip creation fails, keep the old .zip rather than deleting it.
6. **Verification Before Deploy:** Always verify the zip before you upload it to marketplace.

## Boundaries

Do NOT:
- Edit .zip files directly (always edit source/)
- Delete .zip files unless explicitly instructed
- Create .zip files for plugins that don't have src-*/ folders
- Include node_modules, .DS_Store, .git, or build artifacts in the zip
- Change the plugin's directory structure or rename plugins

Do:
- Keep source and .zip in perfect sync
- Log every repackage with timestamp and what changed
- Verify .zip integrity before calling it done
- Handle errors gracefully without losing old zips
