# Olytic Plugin Creator

Meta-plugin for creating other plugins. Guides a structured discovery process, generates complete plugin files with automatic telemetry, and manages the Olytic plugin marketplace.

Works for both Olytic internal plugins and client-facing plugins.

## Components

### Skills

- **plugin-discovery** — 7-question dynamic discovery protocol that gathers plugin requirements: name, purpose, users, strategic questions, constraints, integrations, success metrics, and data sources.
- **plugin-generation** — Takes discovery output and generates a complete, ready-to-use plugin with all standard components, telemetry, and documentation. Includes reference templates for every component type.
- **marketplace-management** — Reads, diffs, and stages updates to the Olytic plugin marketplace at `SupportOlyticSolutions/olytic-plugins`. Stages changes on feature branches for review — never auto-merges.

### Commands

- `/create-plugin [name]` — Start the full plugin creation workflow from discovery through delivery
- `/update-marketplace [plugin-name]` — Add or update a plugin entry in the Olytic marketplace

### Agents

- **plugin-builder** — End-to-end orchestrator that manages the 6-phase plugin creation workflow: discovery → component planning → generation → review → delivery → marketplace

### Integrations

- **GitHub** — Reads and updates the marketplace at `SupportOlyticSolutions/olytic-plugins`

## What Every Generated Plugin Gets

Every plugin created by this tool automatically includes:

1. **Plugin telemetry skill** — Tracks usage events (skill/agent/command invocations), version tags, constraint violations, and user feedback. Logs as structured JSONL.
2. **Proper plugin.json** — With correct author info, versioning, and keywords.
3. **README.md** — Documenting all components, strategic questions, boundaries, and success metrics.
4. **Olytic naming conventions** — Skills as `[domain]-[function]`, commands as `[verb]-[object]`, agents as `[role]-[responsibility]`.
5. **Strategic questions embedded** — From discovery, baked into skills and agents as decision frameworks.
6. **Constraint enforcement** — From discovery, embedded in skills and tracked by telemetry.

## The 7 Discovery Questions

1. What is the plugin name and purpose?
2. Who uses it and what are their key functions?
3. What strategic questions should users ask when using it?
4. What should it NOT be used for? Constraints?
5. What external systems should it interact with? *(dynamic based on Q1-Q2)*
6. What business metrics measure success?
7. What data sources feed those metrics?

## Usage

**Create a new plugin:**
```
/create-plugin sales-enablement
```
Then follow the guided discovery flow.

**Update the marketplace after building a plugin:**
```
/update-marketplace sales-enablement
```

## Customization

- **Discovery questions:** Edit `skills/plugin-discovery/SKILL.md` to add, remove, or modify questions
- **Generation templates:** Edit files in `skills/plugin-generation/references/` to change how plugins are generated
- **Telemetry template:** Edit `skills/plugin-generation/references/telemetry-template.md` to change what every plugin logs
- **Olytic patterns:** Edit `skills/plugin-generation/references/olytic-patterns.md` to update naming and structure conventions
- **Marketplace repo:** Edit `skills/marketplace-management/SKILL.md` to point to a different marketplace repository
