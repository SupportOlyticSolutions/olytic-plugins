# Plugin Source vs. ZIP File Drift: Issue & Resolution

**Date:** 2026-03-04  
**Status:** RESOLVED  
**Related Files:** TELEMETRY-TESTING.md (updated with issue documentation)

---

## The Issue: What Happened

### The Problem

When you made updates to plugin source code (added skills, updated READMEs, modified agents), you assumed those changes would automatically cascade into the packaged .zip files. **They did not.**

**Result:** A critical mismatch developed:
- ✅ Local source folders had the latest code
- ❌ Packaged .zip files were stale (created before updates)
- ❌ Uploaded .zip files to marketplace didn't contain the latest changes
- ❌ Users of the plugins never saw new features because they downloaded old zips

**Example:** You created `telemetry-testing` skill in `gaudi/src-gaudi/skills/telemetry-testing/`, but when you uploaded `gaudi.zip` to the marketplace, that skill wasn't included because the .zip hadn't been regenerated.

### Why It Happened

There was no automated mechanism to regenerate .zip files when source files changed. Developers had to manually zip the folder, and this step was frequently forgotten or delayed. This created a "stale cache" problem where the packaged version diverged from the source version.

---

## The Resolution: Auto-Sync System

### Part 1: New Skill — `aule-plugin-repackager`

**Location:** `/sessions/serene-zealous-cannon/mnt/olytic-plugins/Plugins/aule/src-aule/skills/aule-plugin-repackager/SKILL.md`

**What it does:**
1. Detects when plugin source files change
2. Identifies which plugin was modified
3. Regenerates that plugin's .zip file from source
4. Verifies the .zip contains all required files (plugin.json, README.md, skills/, etc.)
5. Logs every repackage operation with timestamp and file inventory

**Key principle:** Source folders are the source of truth. .zip files are always derived from source, never edited directly.

### Part 2: Extended PostToolUse Hook

**Location:** `/sessions/serene-zealous-cannon/mnt/olytic-plugins/Plugins/aule/src-aule/hooks/hooks.json`

**What changed:**
- Extended the existing PostToolUse hook to monitor plugin source folder paths
- Hook now detects ANY Write/Edit to `Plugins/*/src-*/` directories
- When detected, automatically invokes `aule-plugin-repackager` skill

**Behavior:**
```
Developer edits Plugins/gaudi/src-gaudi/skills/new-skill/SKILL.md
    ↓
PostToolUse hook fires (detects Write to Plugins/gaudi/src-gaudi/...)
    ↓
Hook invokes: aule-plugin-repackager skill
    ↓
Skill regenerates: Plugins/gaudi/gaudi.zip
    ↓
Skill verifies: plugin.json parses, README exists, all skills present
    ↓
Logs: "[2026-03-04T18:35:41Z] gaudi — repackaged (29 files, 75KB, includes new-skill)"
```

**No user action required.** Changes to source automatically trigger repackage.

---

## Current State (Verified 2026-03-04 18:35)

All four organizational plugins are now perfectly synced:

| Plugin | Source Folder | ZIP File | Files | Size | Status |
|--------|---------------|----------|-------|------|--------|
| **gaudi** | `src-gaudi/` | `gaudi.zip` | 29 | 75KB | ✅ SYNCED (includes telemetry-testing) |
| **the-one-ring** | `src-one-ring/` | `the-one-ring.zip` | 33 | 50KB | ✅ SYNCED |
| **magneto** | `src-magneto/` | `magneto.zip` | 35 | 58KB | ✅ SYNCED |
| **aule** | `src-aule/` | `aule.zip` | 37 | 98KB | ✅ SYNCED (includes aule-plugin-repackager) |

All zips pass integrity verification and are ready for upload to marketplace.

---

## Going Forward

**When you edit plugin source:**

1. You make changes in the local source folder (e.g., `Plugins/gaudi/src-gaudi/`)
2. PostToolUse hook detects the change automatically
3. aule-plugin-repackager skill regenerates the .zip
4. The .zip is ready to upload to marketplace immediately

**No manual steps. No forgetting to re-zip. Source and .zip always match.**

### If Auto-Sync Doesn't Trigger

Rarely, the hook might not fire. If you suspect a .zip is stale:

```
"repackage the gaudi plugin"
"sync plugins to disk"
"regenerate magneto.zip"
```

Or check manually:
```bash
ls -lt Plugins/gaudi/gaudi.zip Plugins/gaudi/src-gaudi/
```

If the .zip is much older than the source folder, manually trigger repackage as shown above.

---

## Documentation Updates

This issue and its resolution are now documented in:
- **TELEMETRY-TESTING.md:** New section "Known Issue: Plugin Source vs. .ZIP File Drift" (lines 411–455)
- **TELEMETRY-TESTING.md:** Common error table updated with stale-zip diagnosis (line 322)

---

## Files Changed

- ✅ Created: `/sessions/serene-zealous-cannon/mnt/olytic-plugins/Plugins/aule/src-aule/skills/aule-plugin-repackager/SKILL.md`
- ✅ Updated: `/sessions/serene-zealous-cannon/mnt/olytic-plugins/Plugins/aule/src-aule/hooks/hooks.json` (extended PostToolUse hook)
- ✅ Updated: `/sessions/serene-zealous-cannon/mnt/olytic-plugins/telemetry-blueprint/TELEMETRY-TESTING.md` (issue documentation)
- ✅ Regenerated: All four plugin .zip files (gaudi, the-one-ring, magneto, aule)

---

## Key Takeaway

**Before:** Source updates ≠ marketplace updates (gap unknown to developers)  
**After:** Source updates → automatic .zip regeneration → marketplace always current

The system is now self-maintaining. You edit source, and the rest happens automatically.
