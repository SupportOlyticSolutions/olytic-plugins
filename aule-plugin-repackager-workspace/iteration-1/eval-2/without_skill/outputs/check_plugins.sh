#!/bin/bash

# Test Case 2: Check which plugins need repackaging
# Compare timestamps of source folders vs .zip files

OUTPUT_DIR="/sessions/serene-zealous-cannon/mnt/olytic-plugins/aule-plugin-repackager-workspace/iteration-1/eval-2/without_skill/outputs"
RESULTS_FILE="${OUTPUT_DIR}/repackaging_report.txt"
JSON_RESULTS="${OUTPUT_DIR}/repackaging_status.json"
SEARCH_ROOT="/sessions/serene-zealous-cannon/mnt/olytic-plugins/Plugins"

# Initialize results files
{
    echo "=== Plugin Repackaging Status Report ==="
    echo "Generated: $(date)"
    echo "Workspace: $SEARCH_ROOT"
    echo ""
} > "$RESULTS_FILE"

# Initialize JSON results
echo "{" > "$JSON_RESULTS"
echo "  \"report_date\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"," >> "$JSON_RESULTS"
echo "  \"workspace\": \"$SEARCH_ROOT\"," >> "$JSON_RESULTS"
echo "  \"approach\": \"Compare modification timestamps of source directories against .zip files\"," >> "$JSON_RESULTS"
echo "  \"plugins\": {" >> "$JSON_RESULTS"

FIRST_PLUGIN=true
NEEDS_REPACKAGE_COUNT=0
TOTAL_PLUGINS=0

# Find all src-* directories under Plugins
find "$SEARCH_ROOT" -type d -name "src-*" 2>/dev/null | sort | while read -r src_dir; do
    # Extract plugin name from path (e.g., /Plugins/gaudi/src-gaudi -> gaudi)
    plugin_name=$(basename "$src_dir" | sed 's/^src-//')

    # Get the parent directory of src- folder (e.g., /Plugins/gaudi)
    plugin_dir=$(dirname "$src_dir")

    # Look for corresponding .zip file - check multiple locations
    zip_file="${plugin_dir}/${plugin_name}.zip"

    # Alternative location: one level up
    if [ ! -f "$zip_file" ]; then
        zip_file="${SEARCH_ROOT}/${plugin_name}.zip"
    fi

    TOTAL_PLUGINS=$((TOTAL_PLUGINS + 1))

    if [ -f "$zip_file" ]; then
        # Get the most recent file timestamp in source directory tree
        src_timestamp=$(find "$src_dir" -type f -exec stat -c %Y {} \; 2>/dev/null | sort -rn | head -1)
        zip_timestamp=$(stat -c %Y "$zip_file" 2>/dev/null)

        if [ -z "$src_timestamp" ]; then
            src_timestamp=0
        fi

        src_date=$(date -d @"$src_timestamp" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "unknown")
        zip_date=$(date -d @"$zip_timestamp" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "unknown")

        time_diff=$((src_timestamp - zip_timestamp))

        # Compare timestamps
        if [ "$src_timestamp" -gt "$zip_timestamp" ]; then
            status="OUT_OF_SYNC"
            NEEDS_REPACKAGE_COUNT=$((NEEDS_REPACKAGE_COUNT + 1))
            needs_repackaging="true"
        else
            status="IN_SYNC"
            needs_repackaging="false"
        fi

        # Append to text report
        {
            echo ""
            echo "Plugin: ${plugin_name}"
            echo "  Status: ${status}"
            echo "  Source Dir: ${src_dir}"
            echo "  Source Latest Modified: ${src_date} (timestamp: ${src_timestamp})"
            echo "  Zip File: ${zip_file}"
            echo "  Zip Modified: ${zip_date} (timestamp: ${zip_timestamp})"
            if [ "$time_diff" -gt 0 ]; then
                echo "  Time Difference: ${time_diff} seconds (SOURCE IS NEWER - NEEDS REPACKAGING)"
            else
                echo "  Time Difference: $((time_diff * -1)) seconds (zip is newer - in sync)"
            fi
        } >> "$RESULTS_FILE"

        # Append to JSON
        if [ "$FIRST_PLUGIN" = false ]; then
            echo "," >> "$JSON_RESULTS"
        fi
        FIRST_PLUGIN=false

        cat >> "$JSON_RESULTS" << EOF
    "${plugin_name}": {
      "status": "${status}",
      "needs_repackaging": ${needs_repackaging},
      "source_dir": "${src_dir}",
      "source_latest_modified": "${src_date}",
      "source_timestamp": ${src_timestamp},
      "zip_file": "${zip_file}",
      "zip_modified": "${zip_date}",
      "zip_timestamp": ${zip_timestamp},
      "time_difference_seconds": ${time_diff}
    }
EOF

    else
        # No zip file found
        {
            echo ""
            echo "Plugin: ${plugin_name}"
            echo "  Status: ZIP_NOT_FOUND"
            echo "  Source Dir: ${src_dir}"
            echo "  Expected Zip: ${zip_file}"
            echo "  Note: No corresponding .zip file found"
        } >> "$RESULTS_FILE"

        if [ "$FIRST_PLUGIN" = false ]; then
            echo "," >> "$JSON_RESULTS"
        fi
        FIRST_PLUGIN=false

        cat >> "$JSON_RESULTS" << EOF
    "${plugin_name}": {
      "status": "ZIP_NOT_FOUND",
      "needs_repackaging": true,
      "source_dir": "${src_dir}",
      "expected_zip_file": "${zip_file}"
    }
EOF

        NEEDS_REPACKAGE_COUNT=$((NEEDS_REPACKAGE_COUNT + 1))
    fi

done

# Now read the actual counts to use in the summary
TOTAL_PLUGINS=$(find "$SEARCH_ROOT" -type d -name "src-*" 2>/dev/null | wc -l)
NEEDS_REPACKAGE_COUNT=0

# Recount to get accurate numbers
find "$SEARCH_ROOT" -type d -name "src-*" 2>/dev/null | sort | while read -r src_dir; do
    plugin_name=$(basename "$src_dir" | sed 's/^src-//')
    plugin_dir=$(dirname "$src_dir")
    zip_file="${plugin_dir}/${plugin_name}.zip"
    if [ ! -f "$zip_file" ]; then
        zip_file="${SEARCH_ROOT}/${plugin_name}.zip"
    fi

    if [ -f "$zip_file" ]; then
        src_timestamp=$(find "$src_dir" -type f -exec stat -c %Y {} \; 2>/dev/null | sort -rn | head -1)
        zip_timestamp=$(stat -c %Y "$zip_file" 2>/dev/null)
        if [ -z "$src_timestamp" ]; then
            src_timestamp=0
        fi
        if [ "$src_timestamp" -gt "$zip_timestamp" ]; then
            echo "OUT_OF_SYNC"
        fi
    else
        echo "ZIP_NOT_FOUND"
    fi
done > /tmp/repack_status.txt

NEEDS_REPACKAGE_COUNT=$(grep -c "OUT_OF_SYNC\|ZIP_NOT_FOUND" /tmp/repack_status.txt 2>/dev/null || echo 0)
IN_SYNC_COUNT=$((TOTAL_PLUGINS - NEEDS_REPACKAGE_COUNT))

# Close JSON
{
    echo ""
    echo "  },"
    echo "  \"summary\": {"
    echo "    \"total_plugins\": ${TOTAL_PLUGINS},"
    echo "    \"needs_repackaging\": ${NEEDS_REPACKAGE_COUNT},"
    echo "    \"in_sync\": ${IN_SYNC_COUNT}"
    echo "  }"
    echo "}"
} >> "$JSON_RESULTS"

# Add summary to text report
{
    echo ""
    echo "=== SUMMARY ==="
    echo "Total plugins found: ${TOTAL_PLUGINS}"
    echo "Plugins needing repackaging: ${NEEDS_REPACKAGE_COUNT}"
    echo "Plugins in sync: ${IN_SYNC_COUNT}"
    echo ""
    if [ "$NEEDS_REPACKAGE_COUNT" -gt 0 ]; then
        echo "RECOMMENDATION: Repackage ${NEEDS_REPACKAGE_COUNT} plugins with out-of-sync sources"
    else
        if [ "$TOTAL_PLUGINS" -gt 0 ]; then
            echo "RECOMMENDATION: All plugins are in sync"
        else
            echo "RECOMMENDATION: No plugins found in workspace"
        fi
    fi
} >> "$RESULTS_FILE"

# Output results
echo "Results saved to:"
echo "  Text Report: $RESULTS_FILE"
echo "  JSON Report: $JSON_RESULTS"
echo ""
cat "$RESULTS_FILE"
