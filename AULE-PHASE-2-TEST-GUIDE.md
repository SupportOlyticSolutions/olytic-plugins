# Aule Phase 2 Testing Guide

**Goal:** Verify that aule-change-analyzer and aule-skill-updater work correctly.

**Duration:** 5 minutes (quick check) or 30 minutes (full test)

---

## Quick Verification (5 minutes)

### Step 1: Verify Skills Exist

```bash
ls -la plugins-workspace/aule/src-aule/skills/aule-change-analyzer/
ls -la plugins-workspace/aule/src-aule/skills/aule-skill-updater/
# Should see SKILL.md in each directory
```

### Step 2: Verify Hook Configuration

```bash
grep -A 10 "PostToolUse" plugins-workspace/aule/src-aule/hooks/hooks.json
# Should see: "aule-change-analyzer" mentioned in the prompt
```

### Step 3: Verify Documentation Files

```bash
ls -la AULE-PHASE-2-*.md
ls -la AULE-ARCHITECTURE-*.md
# Should see all documentation files
```

**Result if all pass:** ✅ Phase 2 is wired correctly

---

## Full Integration Test (30 minutes)

This test creates a realistic scenario where a new reference file is created and watches the system respond.

### Test Scenario: New Security Requirement

Imagine you need to establish: "Every plugin must validate its hooks configuration before loading."

### Step 1: Create Test Reference File

```bash
cat > plugins-workspace/aule/src-aule/references/hooks-validation.md << 'EOF'
# Hooks Validation Requirement

Every plugin must validate its hooks configuration before they are loaded.

This is a mandatory requirement for all Aule plugins.

## Why This Matters

Invalid hooks can cause crashes or security issues.

## Implementation

Each plugin should include:
1. `scripts/validate-hooks.py` for validation
2. Call validation before loading hooks
3. Log validation results
EOF

echo "✓ Created test reference file"
```

### Step 2: Understand What Should Happen

The system should:
1. Detect the new file was created
2. aule-change-analyzer reads it and sees: "mandatory", "every plugin"
3. Categorizes as: Generation Requirement
4. Routes to: aule-skill-updater + trigger trashbot
5. aule-skill-updater updates SKILL.md with new requirement

### Step 3: Verify What Actually Happened

Check if SKILL.md was updated:

```bash
grep -i "hooks-validation\|validate.*hooks" \
  plugins-workspace/aule/src-aule/skills/plugin-generation/SKILL.md

# If found: ✓ aule-skill-updater worked
# If not found: ✗ aule-skill-updater didn't run
```

### Step 4: Check Telemetry Logs

Look for evidence of the system running:

```bash
# If telemetry logs exist, they should show:
# - event: aule_change_detected
# - category: generation_requirement
# - action_taken: updated_skill + swept_plugins
```

### Step 5: Verify Next-Generation Plugin

If everything worked, the next time someone generates a plugin using aule's plugin-generation skill, it should include hooks validation.

This would be verified by checking if plugin-generation/SKILL.md mentions the requirement.

### Step 6: Cleanup

Remove the test file:

```bash
rm plugins-workspace/aule/src-aule/references/hooks-validation.md
# If SKILL.md was updated with test content, revert those changes manually
```

---

## Expected Outcomes

### If Phase 2 Works Correctly

1. **Detection:** PostToolUse hook fires when reference file is created
2. **Routing:** aule-change-analyzer categorizes it correctly
3. **Update:** aule-skill-updater updates SKILL.md
4. **Sweep:** trashbot updates all plugins
5. **Logs:** All actions are logged to telemetry

### If Something Failed

**PostToolUse hook didn't fire?**
- Check hooks.json syntax (must be valid JSON)
- Verify file path matches detection pattern
- Check hook timeout (should be 30+ seconds)

**aule-change-analyzer didn't categorize correctly?**
- Review the categorization logic in the skill
- Check if reference file matches expected patterns
- Verify file path is recognized

**aule-skill-updater didn't update SKILL.md?**
- Check if reference file was read
- Verify target section exists in SKILL.md
- Check for errors in skill logic

---

## Success Criteria

✅ Phase 2 test passes when:
- Skills exist at correct paths
- Hook configuration is updated
- Reference file is detected
- Change is categorized correctly
- SKILL.md is updated (or logs show what would happen)
- System output is logged

---

## Notes for Testing

- These are the NEW skills created in Phase 2
- They work WITH the existing trashbot (doesn't replace it)
- The system is designed to handle edge cases gracefully
- If uncertain, the system defaults to safe action (just log)

---

## After Testing

Once Phase 2 testing is complete:
1. Document any findings or issues
2. Refine categorization or routing logic if needed
3. Prepare for Phase 4: Full autonomy testing
4. Push all files to GitHub
