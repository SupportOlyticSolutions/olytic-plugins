# Cortex System

Your plugin knowledge management system is now live.

## Quick Start

1. **Add insights** to `Cortex/` subdirectories as you develop plugin ideas
2. **Trigger processing** with: `"Process my Cortex and recommend plugin updates"`
3. **Review recommendations** that Claude generates
4. **Approve changes** and Claude commits them to your plugin skills + metadata

## File Format

Use this template for Cortex files:

```markdown
# [Clear Title]

**Date:** YYYY-MM-DD
**Category:** [Plugin Evolution | Domain Knowledge | User Feedback | Technical Patterns | Competitive Analysis]
**Status:** Ready for processor

## The Problem
[What problem?]

## The Insight
[Your recommendation?]

## Why It Matters
[Why should plugins care?]

## Relevant Plugins
- Plugin Name (reason)

## Suggested Implementation
[How? Code examples if helpful.]
```

Save as: `Cortex/category/YYYY-MM-DD-topic-slug.md`

## Files Included

- **Cortex/** folder structure (6 subdirectories + _archived + _cortex-state.json)
- **Aule cortex-processor skill** — the engine that processes your insights
- **Plugin metadata files** — one `.metadata.json` per plugin:
  - aule/aule.metadata.json
  - gaudi/gaudi.metadata.json
  - magneto/magneto.metadata.json
  - the-one-ring/the-one-ring.metadata.json
- **Reference files**:
  - cortex-metadata-schema.json — validate your metadata against this
  - example-aule.metadata.json — see what a populated metadata file looks like
  - example-cortex-file-1.md — example Cortex insight file
  - example-cortex-state.json — example state file after processing

## How It Works

**Phase 1: Ingest** → Scan Cortex folder for new `.md` files

**Phase 2: Deduplicate** → Conflate overlapping ideas across files

**Phase 3: Map** → Determine which plugins would benefit from each insight

**Phase 4: Recommend** → Surface structured recommendations for your approval

**Phase 5: Commit** → Update plugin skills + metadata with approved changes

## Metadata Schema

Each plugin has a `plugin-name.metadata.json` file with:

```json
{
  "id": "plugin-id",
  "name": "Plugin Name",
  "description": "Extended description (1-2 sentences)",
  "image": "assets/logo.png",
  "label": "Marketplace",
  "version": "1.0.0",
  "lastCortexUpdate": "2026-03-03T14:30:00Z",
  "cortexTopics": ["topic1", "topic2"],
  "relationships": {
    "dependsOn": ["the-one-ring"],
    "complementaryPlugins": ["other-plugin"]
  },
  "customFields": {
    "tier": "tier-1",
    "owner": "platform-engineering"
  }
}
```

The `lastCortexUpdate` timestamp and `cortexTopics` array are updated automatically when the Cortex processor commits changes. This creates an audit trail of what each plugin has learned.

## Cortex Folder Structure

```
Cortex/
├── plugin-evolution/          # How plugins should evolve
├── domain-knowledge/          # Deep domain knowledge
├── user-feedback/             # Synthesized user feedback
├── technical-patterns/        # Architecture and best practices
├── competitive-analysis/      # Market/competitive insights
├── _archived/                 # Processed materials (audit trail)
└── _cortex-state.json        # System state (auto-maintained)
```

## Using the Cortex Processor

The Cortex processor is built into Aule as the `cortex-processor` skill.

**To process:**
```
"Process my Cortex and recommend plugin updates"
```

**The processor will:**
1. Scan for new files since last run
2. Parse and deduplicate insights
3. Map to relevant plugins
4. Generate recommendations with evidence
5. Wait for your approval
6. Commit approved changes
7. Archive processed files
8. Update metadata timestamps

**You control:**
- Which recommendations get approved
- Whether to edit proposed text before committing
- When to run the processor (weekly, on-demand, or both)

## Best Practices

- **One insight per file** — easier deduplication
- **Date-prefix filenames** — `YYYY-MM-DD-topic.md` for easy scanning
- **Include "Relevant Plugins"** — speeds up the mapping phase
- **Batch process weekly** — let insights accumulate, then process
- **Review archived materials** — see what's been integrated over time

## Next Steps

1. Add 1-2 Cortex insight files to `Cortex/plugin-evolution/`
2. Run the processor: `"Process my Cortex and recommend updates"`
3. Review recommendations
4. Approve changes
5. Repeat as you develop new insights

## Reference

- **Cortex metadata schema:** cortex-metadata-schema.json
- **Example metadata:** example-aule.metadata.json
- **Example Cortex file:** example-cortex-file-1.md
- **Example state file:** example-cortex-state.json
- **Processor skill:** aule/skills/cortex-processor/SKILL.md

The system is ready to use. Start by adding insights to the Cortex folder whenever you develop plugin ideas.
