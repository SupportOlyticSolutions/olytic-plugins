---
name: aule-plugin-repackager
description: >
  Automatically keeps plugin packages in sync with their local source folders. When plugin
  source files are modified, this skill regenerates both the .plugin and .zip files so the
  packaged versions always match src-*/. Invoked automatically via PostToolUse hook when plugin
  source is modified, or manually with: "repackage the plugins", "update plugin packages",
  "sync plugins to disk", "what plugins need repackaging", "regenerate [plugin-name].plugin".
  Both output formats are always produced together and kept in sync — never one without the other.
version: 0.3.0
---

# Aule Plugin Repackager

Automatically keeps plugin packages in sync with their local source code.

## Core Principle

**"Plugin packages are always derived from plugin source folders, never edited directly."**

Every plugin produces **two output files**, always together:

| File | Purpose |
|------|---------|
| `[plugin-name].plugin` | Primary format. Used by Aule and the Claude OS plugin runtime. |
| `[plugin-name].zip` | Universal format. Used for distribution, uploads, and any platform that doesn't yet support `.plugin`. |

Both files are identical in content — same zip archive, different extension. They are always generated together in a single repackage operation. If one exists and the other doesn't, treat it as drift and regenerate both.

## UPSERT Behavior

Repackaging always **upserts** — create on first run, overwrite on all subsequent runs:

```
If [plugin-name].plugin exists:
  → Overwrite it (do not delete first — write directly)

If [plugin-name].plugin does not exist:
  → Create it

Apply the same logic to [plugin-name].zip
```

Never delete a package before creating the replacement. Write to `/tmp/` first, then copy to the destination — this ensures the old version is only replaced once the new version is confirmed valid.

## What This Skill Does

When plugin source files are modified (via Write/Edit in Plugins/*/src-*/ paths):

1. **Discovers** which plugin source folder changed (e.g., `aule/src-aule/`)
2. **Reads** the plugin's `plugin.json` to verify structure and extract metadata
3. **Builds** the archive to `/tmp/[plugin-name].plugin`
4. **Verifies** the archive contains required files
5. **Upserts** both output files:
   - Copy `/tmp/[plugin-name].plugin` → `Plugins/[plugin-name]/[plugin-name].plugin`
   - Copy `/tmp/[plugin-name].plugin` → `Plugins/[plugin-name]/[plugin-name].zip`
6. **Logs** what was packaged (timestamp, file count, size, what changed)

## Plugin Discovery

The skill discovers plugins by looking for this structure:

```
Plugins/
├── aule/
│   ├── src-aule/                          ← Source folder (required)
│   │   ├── .claude-plugin/plugin.json
│   │   ├── README.md
│   │   ├── skills/
│   │   ├── agents/
│   │   └── [other plugin content]
│   ├── aule.plugin                        ← Primary packaged output (auto-generated)
│   └── aule.zip                           ← Universal packaged output (auto-generated)
├── gaudi/
│   ├── src-gaudi/
│   ├── gaudi.plugin
│   └── gaudi.zip
└── [other plugins]
```

For each plugin, the skill:
1. Finds the `src-*/` folder
2. Derives both output filenames from the plugin name
3. Extracts the plugin name from `plugin.json`
4. Regenerates both files when source changes

## Repackaging Algorithm

```
For each changed plugin source folder:

1. Read plugin.json to get plugin metadata
   ✓ Verify it's valid JSON
   ✓ Confirm required keys exist (name, version, description, author)
   ✓ Extract plugin name

2. Build the archive to /tmp/[name].plugin
   ✓ Include all source files except .DS_Store, .git*, node_modules
   ✓ Root of zip must be the src-*/ contents (not a nested folder)
   ✓ Must contain .claude-plugin/plugin.json at the top level
   ✓ File permissions preserved

3. Verify the archive
   ✓ plugin.json can be parsed from inside the archive
   ✓ README.md exists
   ✓ skills/ or agents/ directory exists (at least one)
   ✓ No corrupted files

4. Upsert both output files
   ✓ cp /tmp/[name].plugin → Plugins/[name]/[name].plugin  (create or overwrite)
   ✓ cp /tmp/[name].plugin → Plugins/[name]/[name].zip     (create or overwrite)
   ✓ Both files must exist after this step — verify both

5. Log the result
   ✓ Timestamp, plugin name, file count, file size
   ✓ Whether each output was created or updated
```

## Example: Complete Flow

**What you do:**
1. Edit a skill: `Plugins/aule/src-aule/skills/aule-telemetry/SKILL.md`

**What happens automatically:**
1. PostToolUse hook detects: file written to `Plugins/aule/src-aule/...`
2. Hook invokes aule-plugin-repackager
3. Skill reads `Plugins/aule/src-aule/.claude-plugin/plugin.json` → name = "aule", version = "0.3.0"
4. Builds `/tmp/aule.plugin` (zip of src-aule/)
5. Verifies: plugin.json parses, README exists, files included ✓
6. Upserts: copies to `Plugins/aule/aule.plugin` (overwrites) and `Plugins/aule/aule.zip` (overwrites)
7. Logs: `[2026-03-12T08:30:00Z] aule v0.3.0 — repackaged (38 files, 120KB) → aule.plugin ✓ updated, aule.zip ✓ updated`

**Result:**
- `src-aule/` has the latest changes ✓
- `aule.plugin` matches source ✓
- `aule.zip` matches source ✓

## Failure Modes and Recovery

### Failure 1: Source Folder Has Invalid plugin.json

```
→ Log error: "Cannot parse plugin.json in Plugins/[name]/src-[name]/"
→ Don't create or overwrite any package files
→ List what's wrong with the JSON (missing keys, syntax error, etc.)
→ Return: "Fix plugin.json and try again"
```

### Failure 2: Missing Required Components

```
→ Log warning: "Plugins/[name]/src-[name]/ is missing [README.md|skills/|agents/]"
→ Don't create or overwrite any package files
→ Return: "Add the missing component"
```

### Failure 3: Archive Creation Fails

```
→ Log error: "zip command failed: [error message]"
→ Check disk space, permissions
→ Do NOT overwrite existing .plugin or .zip (keep last-known-good)
→ Return: error with recovery steps
```

### Failure 4: Archive Verification Fails

```
→ Log warning: "Created archive but verification failed: [reason]"
→ Do NOT copy to destination — keep last-known-good .plugin and .zip
→ Log what failed (e.g., "plugin.json couldn't be read from inside archive")
→ Recommend: "Manually verify with: unzip -l /tmp/[name].plugin"
```

### Failure 5: One Output File Written, Other Fails

```
→ Log error: "aule.plugin written but aule.zip copy failed"
→ Retry the failed copy before exiting
→ If retry fails, flag as drift: both files must always be in sync
→ Do NOT leave the plugin in a partially-updated state silently
```

## Operating Principles

1. **Source is Truth:** The `src-*/` folder is the only thing that should be edited. Never edit a package file directly.
2. **Always Both:** A repackage always produces both `.plugin` and `.zip`. Partial output is a failure.
3. **UPSERT, Never Delete-Then-Create:** Write to `/tmp/` first, copy to destination. Old file is only replaced once the new one is verified.
4. **Automatic Sync:** Both package files should always match source. If source changes, both update immediately.
5. **Clear Logging:** Every repackage operation is logged with timestamp, plugin name, version, file count, and whether each output was created or updated.
6. **No Silent Partial State:** If either file fails to write, surface the error. Do not leave `.plugin` and `.zip` out of sync.

## Boundaries

Do NOT:
- Edit package files directly (always edit source/)
- Delete package files unless explicitly instructed
- Create packages for plugins that don't have `src-*/` folders
- Include `node_modules`, `.DS_Store`, `.git`, or build artifacts in the package
- Change the plugin's directory structure or rename plugins
- Produce only `.plugin` without also producing `.zip`, or vice versa

Do:
- Always produce both `.plugin` and `.zip` in every repackage
- Keep source and both package files in perfect sync
- Log every repackage with timestamp, version, and what changed
- Verify archive integrity before copying to destination
- Handle errors gracefully without losing existing packages
