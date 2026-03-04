# Aule Self-Updating Architecture Design

**Purpose:** Enable Aule to autonomously listen for plugin standard changes and automatically update itself and all existing plugins.

**Status:** Design complete, ready for Phase 2 & 3 implementation

---

## The Problem

Currently, when a new plugin standard is established:
1. Someone creates a reference document
2. Someone manually updates plugin-generation/SKILL.md
3. Someone manually runs trashbot to sweep plugins
4. Plugins get updated manually
5. Easy to forget steps, easy to miss plugins, easy to have drift

**Better approach:** The system should detect changes, update itself, and sweep plugins automatically.

---

## Three-Layer Architecture

```
┌──────────────────────────────────────────────┐
│ Layer 1: Detection                           │
│ PostToolUse Hook detects file changes        │
│ Invokes Layer 2                              │
└──────────────┬───────────────────────────────┘
               │
               ↓
┌──────────────────────────────────────────────┐
│ Layer 2: Routing (aule-change-analyzer)      │
│ Reads changed file                           │
│ Categorizes: Generation? Reference? Schema?  │
│ Routes to appropriate handler                │
└──────────────┬───────────────────────────────┘
               │
      ┌────────┴────────┐
      │                 │
      ↓                 ↓
  Invoke            Log only
aule-skill-updater
      ↓
┌──────────────────────────────────────────────┐
│ Layer 3: Auto-Update (aule-skill-updater)    │
│ Reads reference file (source of truth)       │
│ Updates plugin-generation/SKILL.md            │
│ Validates changes                            │
│ Persists to disk                             │
└──────────────┬───────────────────────────────┘
               │
               ↓
        Trigger Trashbot
               ↓
        All plugins updated
```

---

## Layer 1: Detection (PostToolUse Hook)

**File:** `plugins-workspace/aule/src-aule/hooks/hooks.json`

**What it does:**
- Fires when files in Aule are written/edited
- Checks if file path matches known Aule standard paths
- If match: Invokes aule-change-analyzer

**Paths monitored:**
```
skills/plugin-generation/
skills/plugin-discovery/
skills/marketplace-management/
references/hooks-configuration.md
references/component-templates.md
references/telemetry-template.md
references/olytic-patterns.md
references/agentic-best-practices.md
```

---

## Layer 2: Routing (aule-change-analyzer)

**New Skill:** `aule-change-analyzer`

**What it does:**

1. **Reads** the changed file
2. **Analyzes** the content
3. **Categorizes** into three types:

   | Category | Detection | Action |
   |----------|-----------|--------|
   | **Generation Requirement** | File describes something every plugin must have. Keywords: "mandatory", "must", "every plugin" | Invoke aule-skill-updater + trigger trashbot |
   | **Reference Update** | File clarifies existing patterns. Keywords: "example", "best practice" (no structural change) | Just log it |
   | **Schema Change** | File changes data structures. Keywords: "new field", "schema", "structure" | Invoke aule-skill-updater + trigger trashbot + notify |

**Decision Logic:**

```
IF path contains "skills/plugin-generation/":
  → Generation Requirement

ELIF file is "hooks-configuration.md" OR "component-templates.md" OR "telemetry-template.md":
  IF content contains "mandatory" OR "must" OR "every plugin":
    → Generation Requirement
  ELSE:
    → Reference Update

ELIF file is "olytic-patterns.md":
  IF content introduces NEW pattern:
    → Generation Requirement
  ELSE:
    → Reference Update

ELSE:
  → Reference Update (safe default)
```

---

## Layer 3: Auto-Update (aule-skill-updater)

**New Skill:** `aule-skill-updater`

**What it does:**

1. **Reads** the reference file (source of truth)
2. **Identifies** what changed
3. **Maps** reference file → SKILL.md section
4. **Updates or injects** content
5. **Validates** the result
6. **Persists** to disk

**Reference → SKILL.md Mapping:**

| Reference File | SKILL.md Section | What to Update |
|---|---|---|
| `hooks-configuration.md` | Step 4: hooks/hooks.json | Hook template + examples |
| `component-templates.md` | Step 4: Component generation | Component specs for each type |
| `telemetry-template.md` | Step 4.X + Step 5 | Telemetry logging implementation |
| `olytic-patterns.md` | Naming Conventions | Examples (conditional) |

**Update Algorithm:**

```
1. Read reference file
2. Compare with current SKILL.md
3. Identify differences
4. Locate target section in SKILL.md
5. If section exists:
     → Merge: Keep old + Add new
   Else:
     → Inject: Add new section
6. Validate Markdown syntax
7. Verify placeholders still exist
8. Write to disk
9. Log: "Updated [section] with [changes]"
```

---

## Phased Implementation

### Phase 1: Detection Only (Already Done ✓)
- PostToolUse hook detects changes
- trashbot is manually triggered

### Phase 2: Add Routing (Next)
- Create `aule-change-analyzer` skill
- Automatically categorize changes
- Route to appropriate handlers

### Phase 3: Add Auto-Update (Next)
- Create `aule-skill-updater` skill
- Automatically update plugin-generation/SKILL.md
- Keep skill in sync with references

### Phase 4: Full Autonomy (Future)
- All three layers integrated
- Aule fully self-updating
- Zero manual intervention needed

---

## Example: The Complete Flow

### What the User Does:
```
1. Create references/hooks-configuration.md
2. Document: "Every plugin must have SessionStart hooks"
3. Save the file
```

### What Happens Automatically:

**Layer 1: Detection**
```
File saved → PostToolUse hook detects
→ Checks: Is this an Aule standard file?
→ YES: "references/hooks-configuration.md"
→ Invokes: aule-change-analyzer
```

**Layer 2: Routing**
```
aule-change-analyzer reads file
→ Checks: Does it say "every plugin" + "mandatory"?
→ YES: This is a Generation Requirement
→ Decision: Route to aule-skill-updater + trigger trashbot
```

**Layer 3: Auto-Update**
```
aule-skill-updater reads hooks-configuration.md
→ Identifies: "hooks/hooks.json is mandatory"
→ Finds: Step 4 in SKILL.md
→ Updates: Adds "hooks/hooks.json (Mandatory)" subsection
→ Copies: Template and validation rules from reference
→ Validates: Markdown syntax OK, examples complete
→ Persists: Writes updated SKILL.md
```

**Plugin Sweep**
```
trashbot receives: "Aule standard changed: hooks"
→ Audits: All 4 plugins against new requirement
→ Regenerates: All plugins with new requirement
```

**Result:**
```
✓ Reference documentation created
✓ SKILL.md automatically updated
✓ All existing plugins updated
✓ Next-generation plugin includes requirement automatically
✓ Zero manual work
```

---

## Key Design Principles

### 1. Reference Files are Source of Truth
- Reference files (hooks-configuration.md, etc.) are canonical
- SKILL.md is automatically derived from them
- If reference changes, SKILL.md automatically follows
- Eliminates drift

### 2. Intelligent Routing
- aule-change-analyzer reads and understands files
- Doesn't blindly trigger handlers
- Makes smart categorization decisions
- Safe defaults (when uncertain, just log)

### 3. Graceful Degradation
- If aule-skill-updater fails, trashbot still runs
- If validation fails, don't persist
- Never leave SKILL.md in broken state
- Comprehensive error handling

### 4. Audit Trail
- Every change logged to telemetry
- Complete visibility into what happened
- Enables future optimization
- Supports compliance and debugging

### 5. Zero Manual Intervention
- New standard → Automatic detection
- → Automatic categorization
- → Automatic SKILL.md update
- → Automatic plugin sweep
- → Ready for next generation

---

## Benefits

**Before (Manual):**
- Error-prone (easy to forget steps)
- Tedious (multiple manual steps)
- Slow (each new standard takes time)
- Risky (drift between reference and reality)

**After (Automatic):**
- Reliable (all steps happen automatically)
- Fast (happens in seconds)
- Safe (reference is always source of truth)
- Scalable (works same way for 1 new standard or 10)

---

## Files Involved

### Core Skills to Create
```
aule/src-aule/skills/aule-change-analyzer/SKILL.md
aule/src-aule/skills/aule-skill-updater/SKILL.md
```

### Hook to Update
```
aule/src-aule/hooks/hooks.json
  → PostToolUse hook invokes aule-change-analyzer
```

### Reference Files (Source of Truth)
```
aule/src-aule/references/hooks-configuration.md
aule/src-aule/references/component-templates.md
aule/src-aule/references/telemetry-template.md
aule/src-aule/references/olytic-patterns.md
```

### File to Be Auto-Updated
```
aule/src-aule/skills/plugin-generation/SKILL.md
  → Automatically updated by aule-skill-updater
```

---

## Testing Strategy

### Phase 2 Test: Routing
1. Create a test reference file
2. Verify aule-change-analyzer detects it
3. Verify it categorizes correctly
4. Verify routing decision is correct

### Phase 3 Test: Auto-Update
1. Create a test reference file
2. Verify aule-skill-updater updates SKILL.md
3. Verify SKILL.md is valid Markdown
4. Verify validation passes

### Phase 4 Test: Full Integration
1. Create real reference file
2. Watch complete flow end-to-end
3. Verify SKILL.md updated
4. Verify plugins swept
5. Verify next-generation plugin has new requirement

---

## Next Steps

1. **Implement Phase 2:** Create aule-change-analyzer skill
2. **Implement Phase 3:** Create aule-skill-updater skill
3. **Wire integration:** Update PostToolUse hook
4. **Test Phase 4:** Full end-to-end validation
5. **Monitor:** Track success rates and edge cases
6. **Optimize:** Refine based on real usage

---

## The Vision

Aule transforms from a **static plugin generator** into a **self-aware, self-updating system**.

Plugin standards → Automatically detected → Automatically implemented → Automatically propagated → Zero friction

**Result:** A sustainable, scalable, self-maintaining plugin ecosystem.
