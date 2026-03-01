#!/bin/bash

# Plugin Validation Script for Olytic Plugins
# Validates all .plugin files for proper structure and Cloud readiness

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall status
PASSED=0
FAILED=0
WARNINGS=0

# Plugin files to validate
PLUGINS=("the-one-ring.plugin" "olytic-content-strategist.plugin" "olytic-plugin-creator.plugin")

echo "================================================"
echo "   Olytic Plugin Validation Suite"
echo "================================================"
echo ""

# Function to check if file is a valid zip
check_zip_validity() {
    local file=$1
    if unzip -t "$file" > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to check if required files exist in zip
check_required_files() {
    local file=$1
    local missing_files=0

    # Check for .claude-plugin/plugin.json
    if ! unzip -l "$file" | grep -q ".claude-plugin/plugin.json"; then
        echo -e "${RED}  ✗ Missing: .claude-plugin/plugin.json${NC}"
        ((missing_files++))
    else
        echo -e "${GREEN}  ✓ Found: .claude-plugin/plugin.json${NC}"
    fi

    return $missing_files
}

# Function to validate plugin.json structure
check_plugin_json() {
    local file=$1
    local tmpdir=$(mktemp -d)

    unzip -q "$file" ".claude-plugin/plugin.json" -d "$tmpdir"

    if ! command -v jq &> /dev/null; then
        echo -e "${YELLOW}  ⚠ jq not installed, skipping JSON validation${NC}"
        ((WARNINGS++))
    else
        local plugin_json="$tmpdir/.claude-plugin/plugin.json"

        # Check for required fields
        local name=$(jq -r '.name // empty' "$plugin_json")
        local version=$(jq -r '.version // empty' "$plugin_json")
        local description=$(jq -r '.description // empty' "$plugin_json")
        local author=$(jq -r '.author // empty' "$plugin_json")

        if [ -z "$name" ] || [ -z "$version" ] || [ -z "$description" ] || [ -z "$author" ]; then
            echo -e "${RED}  ✗ Missing required fields in plugin.json${NC}"
            return 1
        fi

        echo -e "${GREEN}  ✓ plugin.json structure valid${NC}"
        echo -e "    - Name: $name"
        echo -e "    - Version: $version"
    fi

    rm -rf "$tmpdir"
    return 0
}

# Function to check file size
check_file_size() {
    local file=$1
    local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)

    if [ "$size" -lt 1000 ]; then
        echo -e "${RED}  ✗ File too small: ${size} bytes${NC}"
        return 1
    fi

    echo -e "${GREEN}  ✓ File size OK: ${size} bytes${NC}"
    return 0
}

# Function to check for binary format (not text/base64)
check_binary_format() {
    local file=$1
    local file_type=$(file "$file")

    if [[ "$file_type" == *"ASCII text"* ]]; then
        echo -e "${RED}  ✗ File is ASCII text (should be binary ZIP)${NC}"
        return 1
    elif [[ "$file_type" == *"Zip archive"* ]]; then
        echo -e "${GREEN}  ✓ File is binary ZIP format${NC}"
        return 0
    else
        echo -e "${YELLOW}  ⚠ Unexpected file type: $file_type${NC}"
        ((WARNINGS++))
        return 0
    fi
}

# Validate each plugin
for plugin in "${PLUGINS[@]}"; do
    plugin_path="$SCRIPT_DIR/$plugin"

    if [ ! -f "$plugin_path" ]; then
        echo -e "${RED}✗ $plugin - FILE NOT FOUND${NC}"
        ((FAILED++))
        echo ""
        continue
    fi

    echo -e "${YELLOW}→ Validating: $plugin${NC}"

    # Check file format
    check_binary_format "$plugin_path"
    if [ $? -ne 0 ]; then
        ((FAILED++))
        echo ""
        continue
    fi

    # Check file size
    check_file_size "$plugin_path"
    if [ $? -ne 0 ]; then
        ((FAILED++))
        echo ""
        continue
    fi

    # Check zip validity
    if ! check_zip_validity "$plugin_path"; then
        echo -e "${RED}  ✗ Not a valid ZIP file${NC}"
        ((FAILED++))
        echo ""
        continue
    else
        echo -e "${GREEN}  ✓ Valid ZIP structure${NC}"
    fi

    # Check required files
    check_required_files "$plugin_path"
    files_status=$?
    if [ $files_status -gt 0 ]; then
        ((FAILED++))
        echo ""
        continue
    fi

    # Check plugin.json
    check_plugin_json "$plugin_path"
    if [ $? -ne 0 ]; then
        ((FAILED++))
        echo ""
        continue
    fi

    # If we got here, plugin passed
    echo -e "${GREEN}✓ $plugin - READY FOR UPLOAD${NC}"
    ((PASSED++))
    echo ""
done

# Summary
echo "================================================"
echo "   Validation Summary"
echo "================================================"
echo -e "${GREEN}Passed:${NC}  $PASSED"
echo -e "${RED}Failed:${NC}  $FAILED"
if [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
fi
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All plugins validated successfully!${NC}"
    echo "  Ready for upload to Claude Cloud"
    exit 0
else
    echo -e "${RED}✗ $FAILED plugin(s) failed validation${NC}"
    echo "  Please fix issues before uploading"
    exit 1
fi
