# Aulë — The Olytic Plugin Forge

Named for the Vala of craft and making, Aulë is Olytic's meta-plugin for creating other plugins. It guides a structured discovery process, generates complete plugin files with automatic telemetry and integrity controls, and manages the Olytic plugin marketplace.

Every plugin Aulë creates is designed around **augmentation, not automation** — giving people new capabilities rather than just speeding up existing tasks. This philosophy is embedded in the discovery process, generation templates, and success metrics.

Works for both Olytic internal plugins and client-facing plugins.

## Components

### Skills

- **plugin-discovery** — 10-question dynamic discovery protocol that gathers plugin requirements: name, purpose, users, strategic questions, constraints, memory scope, workflow context, integrations, success metrics, data sources, and natural language triggers.
- **plugin-generation** — Takes discovery output and generates a complete, ready-to-use plugin with all standard components, telemetry, integrity controls, and documentation. Includes reference templates for every component type.
- **marketplace-management** — Reads, diffs, and stages updates to the Olytic plugin marketplace at `SupportOlyticSolutions/olytic-plugins`. Stages changes on feature branches for review — never auto-merges.

### Commands

- `/create-plugin [name]` — Start the full plugin creation workflow from discovery through delivery
- `/update-plugin [name or 'all']` — Audit and update existing plugins to current standards
- `/update-marketplace [plugin-name]` — Add or update a plugin entry in the Olytic marketplace

### Agents

- **plugin-builder** — End-to-end orchestrator that manages the 6-phase plugin creation workflow: discovery → component planning → generation → review → delivery → marketplace

### Integrations

- **GitHub** — Reads and updates the marketplace at `SupportOlyticSolutions/olytic-plugins`

## What Every Generated Plugin Gets

Every plugin created by Aulë automatically includes:

1. **Plugin telemetry skill** — Tracks usage events, version tags, constraint violations, decision traces, and user feedback. Logs as structured JSONL.
2. **Permissions manifest** — Declares what tools the plugin accesses, what data it reads/writes, and what external services it calls.
3. **Proper plugin.json** — With correct author info, versioning, and keywords.
4. **README.md** — Documenting all components, strategic questions, boundaries, and success metrics framed around augmentation.
5. **Olytic naming conventions** — Skills as `[domain]-[function]`, commands as `[verb]-[object]`, agents as `[role]-[responsibility]`.
6. **Strategic questions embedded** — From discovery, baked into skills and agents as decision frameworks.
7. **Constraint enforcement** — From discovery, embedded in skills and tracked by telemetry.
8. **Memory scope declaration** — Each plugin declares what context it retains and for how long.
9. **Integrity controls** — Prompt injection defenses for plugins processing external content, human-in-the-loop checkpoints for high-stakes domains.

## The 10 Discovery Questions

1. What is the plugin name and purpose?
2. Who uses it and what are their key functions?
3. What strategic questions should users ask when using it?
4. What should it NOT be used for? Constraints?
5. What context does this plugin need to remember? *(memory scope)*
6. What's the full workflow, and what new capability does this create? *(augmentation test)*
7. What external systems should it interact with? *(dynamic based on Q1-Q2)*
8. What business metrics measure success?
9. What data sources feed those metrics?
10. What phrases trigger this plugin in natural conversation?

## Design Philosophy

Aulë embeds insights from current research on AI agent integrity, memory management, and productivity:

- **Augmentation over automation** — Plugins should create new capabilities, not just speed up existing tasks. Discovery explicitly probes for this.
- **Memory as architecture** — Every plugin declares its memory scope upfront. Context that persists between sessions requires explicit justification.
- **Integrity by default** — Permissions manifests, prompt injection defenses, and human-in-the-loop checkpoints are built into the generation templates.
- **Workflow-level impact** — Discovery maps the full workflow around the target task, not just the task itself, to identify compounding opportunities.
- **Observable from day one** — Telemetry captures not just what happened, but decision traces explaining why.
- **Composability** — Plugins are designed to work together as building blocks, not just standalone tools.

## Usage

**Create a new plugin:**
```
/create-plugin sales-enablement
```
Then follow the guided discovery flow.

**Update existing plugins to current standards:**
```
/update-plugin the-one-ring
/update-plugin all
```

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
