# Quick Reference: Manual Plugin Zip Update

## Problem
New skill created in source but not in distributed zip file.

## Solution in 4 Steps

```bash
# Step 1: Navigate to plugin directory
cd /sessions/serene-zealous-cannon/mnt/olytic-plugins/Plugins/gaudi

# Step 2: Remove old zip
rm -f gaudi.zip

# Step 3: Regenerate from source
cd src-gaudi && zip -r ../gaudi.zip . && cd ..

# Step 4: Verify the skill is included
unzip -l gaudi.zip | grep "telemetry-testing"
```

## Expected Output for Step 4
```
    0  2026-03-04 18:18   skills/telemetry-testing/
 7327  2026-03-04 18:18   skills/telemetry-testing/SKILL.md
```

## Test Results
| Item | Status |
|------|--------|
| telemetry-testing folder exists | ✓ PASS |
| gaudi.zip regenerated | ✓ PASS |
| telemetry-testing in zip | ✓ PASS |
| File integrity verified | ✓ PASS |

## Files Modified
- `/Plugins/gaudi/gaudi.zip` (regenerated, 74 KB)

## Files Analyzed
- `/Plugins/gaudi/src-gaudi/skills/telemetry-testing/SKILL.md` (7327 bytes)

## Output Documents
1. **test-case-1-report.md** - Comprehensive test report with results
2. **technical-log.txt** - Detailed technical log with all steps
3. **APPROACH_AND_RESULTS.md** - Full approach explanation and findings
4. **QUICK_REFERENCE.md** - This quick reference guide
