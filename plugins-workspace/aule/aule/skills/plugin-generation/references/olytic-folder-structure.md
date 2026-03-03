# Olytic Plugin Folder Structure

The olytic-plugins repository uses a **two-level plugin hierarchy** to organize plugins cleanly:

## Repository Root Structure

```
olytic-plugins/
├── Cortex/                          # Knowledge management system
│   ├── plugin-evolution/
│   ├── domain-knowledge/
│   ├── user-feedback/
│   ├── technical-patterns/
│   ├── competitive-analysis/
│   ├── _archived/
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
└── [plugin-name]/                           # Parent folder for the plugin
    ├── [plugin-name]/                       # Actual plugin folder
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
    │   │   ├── [agent-name-1].md
    │   │   └── [agent-name-2].md
    │   ├── commands/                        # Optional
    │   │   ├── [command-name-1].md
    │   │   └── [command-name-2].md
    │   └── hooks/                           # Optional
    │       └── [hook-file].js
    ├── [plugin-name].metadata.json          # Sidecar metadata (parent level)
    └── [plugin-name].zip                    # Packaged plugin (parent level)
```

## Folder Naming Convention

- **Parent folder:** `[plugin-id]` (kebab-case, e.g., `aule`, `the-one-ring`)
- **Actual plugin folder:** `[plugin-id]` (same name as parent, e.g., `aule/aule/`)
- **Metadata file:** `[plugin-id].metadata.json` (in parent folder)
- **Zip file:** `[plugin-id].zip` (in parent folder)

## Key Rules

1. **Parent folder only contains:**
   - The actual plugin subfolder
   - The `.metadata.json` sidecar file
   - The `.zip` packaged file
   - Nothing else

2. **Metadata file is NEVER inside the plugin folder**
   - ✅ Correct: `plugins-workspace/aule/aule.metadata.json`
   - ❌ Wrong: `plugins-workspace/aule/aule/aule.metadata.json`

3. **Zip file is NEVER inside the plugin folder**
   - ✅ Correct: `plugins-workspace/aule/aule.zip`
   - ❌ Wrong: `plugins-workspace/aule/aule/aule.zip`

4. **When generating a new plugin:**
   - Create the parent folder: `plugins-workspace/[plugin-name]/`
   - Create the actual plugin folder inside it: `plugins-workspace/[plugin-name]/[plugin-name]/`
   - Write all plugin files into the actual plugin folder
   - Write the metadata file into the parent folder after generation
   - Create the zip from the actual plugin folder

## Metadata File Format

The `.metadata.json` sidecar extends Anthropic's plugin schema:

```json
{
  "id": "plugin-id",
  "name": "Plugin Name",
  "description": "Extended description (1-2 sentences)",
  "image": "assets/plugin-logo.png",
  "label": "Category Label",
  "version": "0.1.0",
  "lastCortexUpdate": null,
  "cortexTopics": [],
  "relationships": {
    "dependsOn": ["the-one-ring"],
    "complementaryPlugins": ["other-plugin-1", "other-plugin-2"]
  },
  "customFields": {
    "tier": "tier-1",
    "owner": "team-name",
    "usageScore": 0,
    "maturityLevel": "beta"
  }
}
```

**When is metadata updated?**
- `lastCortexUpdate` — Updated by Cortex processor when knowledge is integrated
- `cortexTopics` — Updated by Cortex processor to track which insights the plugin has learned
- `version` — Manually updated when plugin behavior changes significantly
- All other fields — Set at plugin creation, manually maintained

## Path References in Skills

When referencing plugins in skill documentation or code:

**Discovery/Generation Skills:**
- Reference: "Check if a plugin already exists in `plugins-workspace/[plugin-name]/[plugin-name]/`"

**Marketplace Management:**
- Reference: "Source path in marketplace is `./plugins-workspace/[plugin-name]`"

**Cortex Processor:**
- Reference: "Metadata file location: `plugins-workspace/[plugin-name]/[plugin-name].metadata.json`"

## Migration from Flat Structure

If you're migrating from a flat structure (plugins at root level), follow these steps:

1. Create `plugins-workspace/` folder at root
2. For each plugin:
   - Create `plugins-workspace/[plugin-name]/` parent folder
   - Move plugin folder to `plugins-workspace/[plugin-name]/[plugin-name]/`
   - Move metadata file to `plugins-workspace/[plugin-name]/[plugin-name].metadata.json`
   - Move zip file to `plugins-workspace/[plugin-name]/[plugin-name].zip`
3. Update any scripts or references to use the new paths
4. Update marketplace entries to use `./plugins-workspace/[plugin-name]` as source

## Directory Traversal Examples

**For Aule:**
```
Actual plugin folder: /sessions/.../plugins-workspace/aule/aule/
Metadata sidecar: /sessions/.../plugins-workspace/aule/aule.metadata.json
Packaged zip: /sessions/.../plugins-workspace/aule/aule.zip
```

**For The One Ring:**
```
Actual plugin folder: /sessions/.../plugins-workspace/the-one-ring/the-one-ring/
Metadata sidecar: /sessions/.../plugins-workspace/the-one-ring/the-one-ring.metadata.json
Packaged zip: /sessions/.../plugins-workspace/the-one-ring/the-one-ring.zip
```

## Validation Checklist

Before considering a plugin "ready," verify:

- [ ] Parent folder exists: `plugins-workspace/[plugin-name]/`
- [ ] Actual plugin folder exists: `plugins-workspace/[plugin-name]/[plugin-name]/`
- [ ] `.claude-plugin/plugin.json` exists in actual plugin folder
- [ ] Metadata file exists in parent folder (NOT in actual plugin folder)
- [ ] Metadata file is valid JSON and matches schema
- [ ] Zip file exists in parent folder (NOT in actual plugin folder)
- [ ] Zip contains correct structure (no wrapper subfolder)
- [ ] All skills have SKILL.md files
- [ ] plugin-telemetry skill included
- [ ] README.md exists with Claude OS Identity section
- [ ] No duplicate component names across skills/commands/agents

## Marketplace Integration

The Olytic marketplace at `SupportOlyticSolutions/olytic-plugins` references plugins using this structure:

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

The `source` path points to the parent folder. The marketplace validator can then find:
- Plugin files in `source/[plugin-name]/`
- Metadata in `source/[plugin-name].metadata.json`
- Packaged zip in `source/[plugin-name].zip`
