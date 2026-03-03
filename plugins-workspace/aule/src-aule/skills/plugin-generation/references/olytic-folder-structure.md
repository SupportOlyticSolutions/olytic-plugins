# Olytic Plugin Folder Structure

The olytic-plugins repository uses a **clean, two-level plugin hierarchy** with flat Cortex for easy file management.

## Repository Root Structure

```
olytic-plugins/
├── Cortex/                          # Knowledge management system (FLAT)
│   ├── 2026-03-01-insight.md       # Drag and drop .md files here
│   ├── 2026-03-02-another.md
│   ├── _archived/                  # Auto-managed after processing
│   └── _cortex-state.json
├── plugins-workspace/               # ALL PLUGINS LIVE HERE
│   ├── aule/
│   ├── gaudi/
│   ├── magneto/
│   └── the-one-ring/
├── telemetry-blueprint/
├── README.md
├── catalog.json
├── validate-plugins.sh
└── CORTEX-SYSTEM.md
```

## Individual Plugin Organization

Each plugin in `plugins-workspace/` follows this structure:

```
plugins-workspace/
└── [plugin-name]/                           # Parent folder (workspace)
    ├── src-[plugin-name]/                   # Actual plugin source code
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   ├── .mcp.json                        # Optional
    │   ├── README.md
    │   ├── skills/
    │   │   ├── plugin-telemetry/
    │   │   │   └── SKILL.md
    │   │   ├── [domain-skill-1]/
    │   │   │   ├── SKILL.md
    │   │   │   └── references/
    │   │   │       └── [reference].md
    │   │   └── [domain-skill-2]/
    │   │       └── SKILL.md
    │   ├── agents/                          # Optional
    │   ├── commands/                        # Optional
    │   └── hooks/                           # Optional
    ├── [plugin-name].metadata.json          # Sidecar metadata (parent level)
    └── [plugin-name].zip                    # Packaged plugin (parent level)
```

## Folder Naming Convention

**Crystal Clear:**
- **Parent folder:** `[plugin-id]` (e.g., `aule`, `the-one-ring`)
  - This is the "workspace" or "namespace" for the plugin
  - Contains metadata, zip, and the source folder
- **Source folder:** `src-[plugin-id]` (e.g., `src-aule`, `src-gaudi`)
  - This is the actual plugin source code
  - Contains all the plugin files: .claude-plugin/, skills/, agents/, commands/, etc.
- **Metadata file:** `[plugin-id].metadata.json` (in parent folder)
- **Zip file:** `[plugin-id].zip` (in parent folder)

## Examples

### Aule Structure
```
plugins-workspace/aule/
├── src-aule/               # The actual Aule plugin source code
├── aule.metadata.json      # Aule's metadata (in parent)
└── aule.zip                # Aule's package (in parent)
```

### Gaudi Structure
```
plugins-workspace/gaudi/
├── src-gaudi/              # The actual Gaudi plugin source code
├── gaudi.metadata.json
└── gaudi.zip
```

### The One Ring Structure
```
plugins-workspace/the-one-ring/
├── src-the-one-ring/       # The actual One Ring plugin source code
├── the-one-ring.metadata.json
└── the-one-ring.zip
```

## Key Rules

1. **Parent folder only contains:**
   - The `src-[plugin-name]/` subfolder (actual plugin source)
   - The `.metadata.json` sidecar file
   - The `.zip` packaged file
   - Nothing else

2. **Metadata file is NEVER inside src-[plugin-name]/**
   - ✅ Correct: `plugins-workspace/aule/aule.metadata.json`
   - ❌ Wrong: `plugins-workspace/aule/src-aule/aule.metadata.json`

3. **Zip file is NEVER inside src-[plugin-name]/**
   - ✅ Correct: `plugins-workspace/aule/aule.zip`
   - ❌ Wrong: `plugins-workspace/aule/src-aule/aule.zip`

4. **Source folder is ALWAYS named `src-[plugin-id]`**
   - ✅ Correct: `plugins-workspace/aule/src-aule/`
   - ✅ Correct: `plugins-workspace/gaudi/src-gaudi/`
   - ❌ Wrong: `plugins-workspace/aule/src/`
   - ❌ Wrong: `plugins-workspace/aule/aule/`

## Cortex Folder (Flat Structure)

**No subfolders.** Just drag and drop `.md` files directly:

```
Cortex/
├── 2026-03-01-plugin-metadata-strategy.md
├── 2026-03-02-user-feedback-synthesis.md
├── 2026-03-03-aule-best-practices.md
├── _archived/                    # Auto-managed by processor
│   └── 2026-03-01-plugin-metadata-strategy.md
└── _cortex-state.json
```

**Why flat?**
- Easy drag-and-drop from your file manager
- No need to think about categorization
- Processor handles deduplication and mapping
- Archived files automatically organized by date

## When Generating a New Plugin

1. Create parent folder: `plugins-workspace/[plugin-name]/`
2. Create source subfolder inside: `plugins-workspace/[plugin-name]/src-[plugin-name]/`
3. Write all plugin files into `src-[plugin-name]/` folder
4. Create metadata file in parent: `plugins-workspace/[plugin-name]/[plugin-name].metadata.json`
5. Package from inside `src-[plugin-name]/` folder
6. Move zip to parent: `plugins-workspace/[plugin-name]/[plugin-name].zip`

## Path References in Skills

When referencing plugins in skill documentation:

**Discovery/Generation Skills:**
- Check for existing: `plugins-workspace/[plugin-name]/src-[plugin-name]/`
- Write to: `plugins-workspace/[plugin-name]/src-[plugin-name]/`

**Marketplace Management:**
- Source path: `./plugins-workspace/[plugin-name]`
- The marketplace validator finds src-*, metadata, and zip at the parent level

**Cortex Processor:**
- Metadata location: `plugins-workspace/[plugin-name]/[plugin-name].metadata.json`
- Updates: `lastCortexUpdate` timestamp and `cortexTopics` array

## Validation Checklist

Before considering a plugin "ready," verify:

- [ ] Parent folder exists: `plugins-workspace/[plugin-name]/`
- [ ] Source folder exists: `plugins-workspace/[plugin-name]/src-[plugin-name]/`
- [ ] `.claude-plugin/plugin.json` exists in `src-[plugin-name]/` folder
- [ ] Metadata file exists in parent folder (NOT in src-[plugin-name]/)
- [ ] Metadata file is valid JSON and matches schema
- [ ] Zip file exists in parent folder (NOT in src-[plugin-name]/)
- [ ] Zip contains correct structure (no wrapper subfolder)
- [ ] All skills have SKILL.md files
- [ ] plugin-telemetry skill included
- [ ] README.md exists with Claude OS Identity section
- [ ] No duplicate component names across skills/commands/agents

## Marketplace Integration

The Olytic marketplace references plugins using this structure:

```json
{
  "name": "aule",
  "source": "./plugins-workspace/aule",
  "description": "...",
  "version": "0.1.0",
  "keywords": [...],
  "category": "meta"
}
```

The `source` path points to the parent folder. The marketplace validator finds:
- Plugin files in `source/src-[plugin-name]/`
- Metadata in `source/[plugin-name].metadata.json`
- Packaged zip in `source/[plugin-name].zip`

## Visual Comparison

**Before (Confusing):**
```
plugins-workspace/aule/aule/...    # Which is which?
```

**After (Crystal Clear):**
```
plugins-workspace/aule/src-aule/...     # Parent folder, then src-aule
```

Much easier to understand and scan visually!
