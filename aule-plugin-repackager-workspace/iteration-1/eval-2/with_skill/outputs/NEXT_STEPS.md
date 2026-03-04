# Next Steps: Repackaging the Plugins

Based on the analysis results, here's what to do next:

## Current Status

**4 out of 4 plugins need repackaging:**
- **gaudi** - URGENT (13+ hours behind)
- **aule** - HIGH (7 minutes behind)
- **magneto** - HIGH (6 minutes behind)
- **the-one-ring** - HIGH (6 minutes behind)

## How to Invoke the aule-plugin-repackager Skill

The skill can be invoked with any of these commands:

### Option 1: Repackage All Plugins
```
"repackage the plugins"
"what plugins need repackaging"
"sync plugin files"
"sync plugins to disk"
"update plugin zips"
```

### Option 2: Repackage a Single Plugin
```
"regenerate gaudi.zip"
"repackage aule"
"update magneto.zip"
"sync the-one-ring"
```

## What the Skill Will Do

When invoked, the aule-plugin-repackager skill will:

1. **Discover** each plugin source folder (src-*/)
2. **Validate** the plugin.json file for correctness
3. **Read** required files:
   - .claude-plugin/plugin.json
   - README.md
   - skills/ directory
   - agents/ directory
4. **Create** a new .zip file from the source folder
5. **Verify** the zip is valid and contains all required files
6. **Timestamp** the zip with the current date/time
7. **Log** the operation with details about what was packaged
8. **Overwrite** the old .zip file (safe because it's auto-generated)

## Expected Results After Repackaging

| Plugin | Files | Before | After | Status |
|--------|-------|--------|-------|--------|
| aule | 22 | 2026-03-04 04:51:09 | 2026-03-04 ~18:31 | Synced |
| gaudi | 16 | 2026-03-04 04:51:09 | 2026-03-04 ~18:31 | Synced |
| magneto | 21 | 2026-03-04 04:51:09 | 2026-03-04 ~18:31 | Synced |
| the-one-ring | 19 | 2026-03-04 04:51:09 | 2026-03-04 ~18:31 | Synced |

## Verification Steps

After repackaging, verify with:

```bash
# Check that .zip files match source folder timestamps
ls -l Plugins/*/src-*/ Plugins/*/*.zip

# Verify .zip contents
unzip -l Plugins/gaudi/gaudi.zip | head -20
unzip -l Plugins/aule/aule.zip | head -20

# Verify plugin.json can be extracted from .zip
unzip -p Plugins/gaudi/gaudi.zip .claude-plugin/plugin.json | jq .
```

## Key Principles

The aule-plugin-repackager operates on these principles:

1. **Source is Truth**: The src-*/ folder is the authoritative version
2. **Auto-Generated Zips**: .zip files are never edited directly
3. **Always Sync**: When source changes, .zip updates automatically
4. **Safe Overwrite**: Old .zip files are replaced with new ones
5. **Verified Output**: Every .zip is checked for integrity
6. **Clear Logging**: All operations are logged with timestamps

## Failure Recovery

If repackaging fails, the skill will:
- Log the error with details
- Keep the old .zip file (don't delete it)
- Provide recovery steps
- NOT create invalid or corrupted .zip files

## Readiness Check

Before invoking the repackager, confirm:

- [x] All 4 plugins have valid plugin.json files
- [x] All 4 plugins have README.md
- [x] All 4 plugins have skills/ directory
- [x] All 4 plugins have agents/ directory
- [x] No source folders are corrupted
- [x] Workspace has disk space for .zip files

**Status: ALL CHECKS PASSED - Ready to repackage**

## Timeline

**Analysis completed:** 2026-03-04 18:31 UTC
**Next step:** Invoke "repackage the plugins" command
**Expected duration:** < 30 seconds total
**Ready for upload:** After repackaging completes

---

**Note:** Once repackaged, the .zip files will be ready for upload to the Olytic marketplace and will accurately reflect all current source code changes.
