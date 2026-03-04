# Test Case 2: Plugin Repackaging Check - Approach & Results

## Objective
Identify which plugins in the workspace need repackaging by comparing source directory modification timestamps against their corresponding .zip file timestamps.

## Approach

### Step 1: Discover Plugin Structure
Located the plugins workspace at `/sessions/serene-zealous-cannon/mnt/olytic-plugins/Plugins/`

Found 4 plugins with source directories:
- `aule/src-aule`
- `gaudi/src-gaudi`
- `magneto/src-magneto`
- `the-one-ring/src-the-one-ring`

### Step 2: Locate Corresponding .zip Files
For each plugin, identified the corresponding .zip files:
- `aule/aule.zip`
- `gaudi/gaudi.zip`
- `magneto/magneto.zip`
- `the-one-ring/the-one-ring.zip`

### Step 3: Extract Timestamps
For each plugin, compared:
1. **Source Directory Latest Modified Time**: Found the most recent file in the entire `src-*` directory tree using `find ... -exec stat -c %Y`
2. **Zip File Modified Time**: Used `stat -c %Y` to get the .zip file's timestamp

### Step 4: Compare & Classify
Classified each plugin as:
- **IN_SYNC**: Zip file timestamp >= Source directory latest timestamp (zip is current or newer)
- **OUT_OF_SYNC**: Source directory timestamp > Zip file timestamp (source has been modified since zip was created)

### Step 5: Detailed Analysis
Calculated the time difference in seconds between source and zip for each plugin to quantify staleness.

## Implementation Details

**Tool Used**: Pure bash script with `find`, `stat`, `date`, and basic arithmetic

**Key Commands**:
```bash
# Find all source directories
find "$SEARCH_ROOT" -type d -name "src-*"

# Get most recent file timestamp in directory tree
find "$src_dir" -type f -exec stat -c %Y {} \; | sort -rn | head -1

# Get .zip file timestamp
stat -c %Y "$zip_file"

# Compare and calculate difference
time_diff=$((src_timestamp - zip_timestamp))
```

## Results Summary

| Plugin | Status | Source Latest | Zip Modified | Time Diff | Action |
|--------|--------|----------------|--------------|-----------|--------|
| **aule** | OUT_OF_SYNC | 2026-03-04 18:30:20 | 2026-03-04 04:51:09 | +49,151 sec | **REPACKAGE** |
| gaudi | IN_SYNC | 2026-03-04 18:31:04 | 2026-03-04 18:31:11 | -7 sec | Up to date |
| magneto | IN_SYNC | 2026-03-04 18:31:08 | 2026-03-04 18:31:36 | -28 sec | Up to date |
| the-one-ring | IN_SYNC | 2026-03-04 18:31:06 | 2026-03-04 18:31:07 | -1 sec | Up to date |

## Key Findings

1. **Total Plugins**: 4 found in workspace
2. **Plugins Needing Repackaging**: 1 (aule)
3. **Plugins In Sync**: 3 (gaudi, magneto, the-one-ring)

### Critical Issue
The **aule** plugin has the most out-of-date .zip file:
- Source was last modified on 2026-03-04 18:30:20
- Zip was last created on 2026-03-04 04:51:09
- Gap of **13+ hours** (49,151 seconds)

This indicates that changes have been made to the aule plugin sources since the zip was last generated.

## Recommendation

**Repackage the `aule` plugin immediately** to ensure the .zip file includes all recent source changes.

The other three plugins (gaudi, magneto, the-one-ring) are current and do not require repackaging at this time.

## Output Files Generated

1. **repackaging_report.txt** - Human-readable detailed report
2. **repackaging_status.json** - Machine-parseable JSON with full metrics
3. **check_plugins.sh** - Bash script implementing the check (portable, no dependencies)
