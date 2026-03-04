---
name: cortex-processor
description: >
  Use this skill when the user says "process my Cortex", "process the Cortex folder", "review my Cortex insights",
  "Cortex workflow", "integrate Cortex learning", "process my plugin knowledge base", or wants to batch-ingest
  accumulated plugin insights into plugin skills. Takes markdown files from the Cortex folder, deduplicates
  overlapping concepts, recommends which plugins should learn from which insights, surfaces recommendations
  for approval, then commits approved changes to plugin skills and metadata.
version: 1.0.0
---

# Cortex Processor

Process accumulated knowledge from your Cortex folder, deduplicate themes, recommend plugin updates, and commit approved changes to your plugin ecosystem.

## What Cortex Does

**Cortex** is a batched knowledge management system where you:
1. Write markdown files capturing plugin insights as they develop
2. Trigger processing (weekly or on-demand)
3. Claude deduplicates overlapping ideas across files
4. Claude recommends which plugins should learn from each insight
5. You approve/reject recommendations
6. Claude commits changes to plugin skills + metadata with full audit trail

## Cortex Folder Structure

Located at the root of your working folder. **Flat structure — no subfolders:**

```
Cortex/
├── 2026-03-01-insight-title.md      # Cortex insight files (drag & drop here)
├── 2026-03-02-another-insight.md
├── 2026-03-03-plugin-evolution.md
├── _archived/                       # Processed materials (auto-managed)
│   └── 2026-03-01-insight-title.md
└── _cortex-state.json              # System state tracking
```

**No subfolders.** Just drag and drop your `.md` files directly into the Cortex folder. The processor will automatically archive them after processing.

## Cortex File Format

**Filename:** `YYYY-MM-DD-topic-slug.md`

**Template:**
```markdown
# [Clear Title]

**Date:** YYYY-MM-DD
**Status:** Ready for processor

## The Problem
[What problem does this insight address?]

## The Insight
[Your recommendation or key idea?]

## Why It Matters
[Why should plugins care about this?]

## Relevant Plugins
- Plugin Name (reason)
- Plugin Name (reason)

## Suggested Implementation
[How should this be implemented?]
```

## Processing Workflow

### Phase 1: Ingest & Scan

- Scan `Cortex/` for all `.md` files
- Read `_cortex-state.json` to identify files modified since last run
- Extract key themes and insights from each file

### Phase 2: Deduplicate & Synthesize

- Identify similar concepts across multiple files
- Conflate overlapping ideas into unified insights
- Weight by frequency and recency
- Generate synthesis with evidence (which files contributed)

### Phase 3: Map to Plugins

- Review current plugin skills and prompts
- Determine which plugins would benefit from each insight
- Prioritize by impact and relevance
- Create structured recommendation payload

### Phase 4: Surface for Approval

Generate formatted recommendation for each plugin update:

```
RECOMMENDATION #1
Plugin: Aule
Insight: "Plugin metadata should include version tracking and audit trails"
Source Files: 2026-03-01-metadata-versioning.md
Suggested Skill Update: [proposed text]
Confidence: High (appears in 2+ Cortex files)
Impact: Aule's plugin-generation skill would incorporate metadata versioning as best practice

[ APPROVE ] [ REJECT ] [ EDIT FIRST ]
```

### Phase 5: Commit (On Approval)

- Update plugin skill prompts with approved changes
- Update `plugin-name.metadata.json`:
  - Set `lastCortexUpdate` to current timestamp
  - Add new topics to `cortexTopics` array
- Move processed Cortex files to `Cortex/_archived/` with date prefix
- Update `_cortex-state.json` with new baseline

## How to Invoke

**Manual trigger (recommended):**
```
"Process my Cortex and recommend plugin updates"
```

**With context:**
```
"I've added 3 new Cortex files about plugin metadata.
Process my Cortex and show me recommendations."
```

## Processing Steps

1. **Verify Cortex folder exists** and contains `.md` files
   - If no new files, report "No new Cortex materials since last run"
   - If files exist, proceed to Phase 1

2. **Parse each Cortex file**
   - Extract title, date, category, problem, insight, relevant plugins, implementation
   - Build a list of raw insights

3. **Deduplicate using semantic clustering**
   - Group similar concepts (e.g., "metadata schema" + "plugin schema" → single concept)
   - Weight concepts by frequency (appearing in 2+ files scores higher)
   - Create unified recommendations with evidence

4. **Map insights to plugins**
   - For each unified insight, check which plugins' skills would benefit
   - Look at current plugin metadata and skill descriptions
   - Score relevance (High/Medium/Low)
   - Create recommendation list sorted by impact

5. **Generate recommendation summaries**
   - For each recommendation, show:
     - Plugin name
     - Insight title
     - Source files (with evidence)
     - Proposed skill update (specific text to add/change)
     - Confidence level and reasoning
     - Impact statement

6. **Await user approval**
   - Present all recommendations at once
   - For each one: `[APPROVE] [REJECT] [EDIT FIRST]`
   - Allow user to edit proposed text if needed
   - Collect approval/rejection votes

7. **Commit approved changes**
   - For each APPROVED recommendation:
     - Find the plugin's skill file(s)
     - Insert the approved text at appropriate location
     - Update `plugin-name.metadata.json`:
       - `lastCortexUpdate` = ISO timestamp
       - Add insight topic to `cortexTopics` array
     - Move source Cortex file(s) to `Cortex/_archived/YYYY-MM-DD-filename.md`
   - Update `_cortex-state.json`:
     - Set `lastProcessed` = current timestamp
     - Increment counters
     - Add entry to `history`
     - Add archived materials list

8. **Generate summary**
   - Show what changed:
     - Files modified
     - Plugins updated
     - New topics learned
   - Show what was rejected and why
   - Suggest next steps

## Best Practices

**Writing Cortex Files:**
- One insight per file (makes deduplication easier)
- Date-prefix all filenames: `YYYY-MM-DD-topic.md`
- Always include "Relevant Plugins" section to speed up mapping
- Link insights to specific plugins (e.g., "Aule's plugin-generation skill")
- If revisiting a topic, create new dated file (preserves audit trail)

**Processing:**
- Batch-process weekly or after accumulating 2-3 files
- Review archived materials occasionally (see what's been integrated)
- Always review recommendations before approval (ask for edits if needed)

**Metadata Maintenance:**
- Keep plugin metadata current (manually update version, description, relationships as needed)
- Check `lastCortexUpdate` and `cortexTopics` to see what Cortex learning is reflected

## Example Workflow

**You add files:**
- `Cortex/2026-03-01-metadata-versioning.md`
- `Cortex/2026-03-02-aule-best-practices.md`

**You trigger processor:**
```
"Process my Cortex and recommend updates"
```

**Claude shows:**
```
Found 2 new files
Deduplicating...
  ✓ Consolidated: "metadata versioning" (2 mentions)
  ✓ Consolidated: "schema validation" (2 mentions)

Mapping to plugins...
  → Aule: Strong match (plugin-generation skill)
  → Gaudi: Weak match (data-modeling context)

---

RECOMMENDATION #1: Aule
Insight: "Plugin metadata should include version tracking and audit trails"
Source Files: 2026-03-01-metadata-versioning.md, 2026-03-02-aule-best-practices.md
Proposed Skill Update:
  "When generating plugin metadata, include:
   - metadataSchemaVersion field for schema versioning
   - _changeLog array tracking metadata updates and Cortex provenance
   - Validation against current schema template"
Confidence: HIGH

[ APPROVE ] [ REJECT ] [ EDIT FIRST ]
```

**You approve, Claude commits:**
```
✓ Updated aule/skills/plugin-generation/SKILL.md
✓ Updated aule/aule.metadata.json: lastCortexUpdate=2026-03-03T14:30:00Z
✓ Added "metadata-versioning" to aule's cortexTopics
✓ Archived 2026-03-01-metadata-versioning.md → Cortex/_archived/
✓ Archived 2026-03-02-aule-best-practices.md → Cortex/_archived/
✓ Updated Cortex/_cortex-state.json

Processing complete: 2 files processed, 1 recommendation approved, 1 plugin updated.
```

## Operating Principles

- **Deduplication first:** Always conflate overlapping ideas before recommending
- **Source of truth:** Cortex files are the source; recommendations must be backed by evidence
- **Atomic commits:** Only update what was approved; never auto-commit unapproved recommendations
- **Audit trail:** All changes tracked in metadata timestamps and `_cortex-state.json` history
- **No hallucination:** If a plugin or file is not found, report it explicitly
- **Verification:** Always confirm file writes succeeded and metadata is valid

## Troubleshooting

**"No new Cortex materials found"**
- Check that files are in `Cortex/` (not `cortex/` or `CORTEX/`)
- Confirm files have `.md` extension
- Check `_cortex-state.json` `lastProcessed` date matches when you last ran the processor

**"Plugin X not found"**
- Check that `plugin-name/` directory exists in workspace
- Confirm `plugin-name.metadata.json` exists
- If plugin is brand new, create metadata file first (use Aule's plugin-generation skill)

**"Recommendation text doesn't look right"**
- Use `[EDIT FIRST]` option to modify proposed text before approval
- Or reject the recommendation and rewrite the Cortex file more clearly
- Reprocess to try again

**"Want to revert a processor run?"**
- Ask: "Revert Cortex processor run from [date]"
- Claude will restore previous plugin state and `_cortex-state.json`

## Integration with Plugin Generation

When Aule's `plugin-generation` skill creates a new plugin, it should:

1. Create a `plugin-name.metadata.json` file with schema-compliant fields
2. Initialize `lastCortexUpdate` as `null` (no learning yet)
3. Initialize `cortexTopics` as empty array
4. Populate `relationships` based on plugin purpose
5. Note that the plugin can later be updated via Cortex processor

The Cortex processor will identify new plugins from their `lastCortexUpdate: null` state and can recommend initial learning topics if relevant materials exist.

---

Telemetry: This skill logs all invocations via aule's plugin-telemetry skill.
