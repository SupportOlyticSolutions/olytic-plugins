---
name: plugin-generation
description: >
  Use this skill after completing plugin discovery, when you need to generate the
  actual plugin files. Takes the discovery summary and produces a complete, ready-to-use
  plugin following Olytic conventions. Every generated plugin automatically includes
  telemetry, proper structure, and documentation.
  See references/ for templates and patterns.
version: 0.1.0
---

# Plugin Generation

Take a completed discovery summary and generate a complete plugin. Follow every rule in this skill exactly — these are Olytic's hard-coded standards for plugin quality.

## Agentic Best Practices (Mandatory)

Every generated plugin must comply with these protocols. See `references/agentic-best-practices.md` for full details.

**Core Protocols — embed in every generated skill, agent, and command:**
- **Discovery first:** Before acting, map the existing environment. Use search/glob to understand what exists. Never recreate existing files or structures.
- **Source of truth:** Local files (skill content, references, JSON) take precedence over conversational context. If conflict exists, the file wins.
- **Atomic operations:** Make the smallest change necessary. Use targeted edits, not full-file rewrites. Minimum API calls.
- **No redundancy:** Reference files instead of repeating their content. Use "Reference: [filename]" patterns. If knowledge exists in The One Ring, point to it — don't copy it.

**Tool & Token Management — embed in agents and commands:**
- **Search over read:** Use Grep/Glob to target specific data. Never read files >50KB in their entirety if specific information can be targeted.
- **Programmatic processing:** For data-heavy tasks, write a processing script and return only the result — don't load raw data into context.
- **Batching:** Consolidate related operations into single turns. Read multiple files in parallel, not sequentially.

**Data Governance — embed in all components:**
- **Metadata integrity:** Every automated entry (logs, commits, generated content) must include a timestamp and source tag.
- **Active workspace vs cold storage:** Telemetry logs are write-only during normal operation. Only access them when the user explicitly asks for history.

**Safety & Quality Guardrails — embed in every command and agent:**
- **Verification gate:** Every write operation must be followed by a verification check. Confirm file structure is valid after writes.
- **No hallucination:** If a variable, file path, or data point is not found, report "Not Found" immediately. Never guess or estimate.
- **Permission gate:** Ask for confirmation before destructive actions (delete, overwrite) or 5+ simultaneous file changes.

## Generation Process

### Step 0: Discovery First — Map the Environment

Before generating anything:
1. Check if a plugin with this name already exists in the working directory (use Glob)
2. Check if a marketplace entry already exists (use the marketplace-management skill)
3. If the plugin exists, ask: "A plugin named [name] already exists. Do you want to update it or create a new one?"
4. If not, proceed to Step 1

### Step 1: Determine Components

Map discovery answers to component types:

| Discovery Signal | Component Type | Reasoning |
|-----------------|----------------|----------|
| Key functions that involve **knowledge or standards** | Skill | User needs domain expertise loaded into context |
| Key functions that involve **repeatable actions** | Command | User needs a `/slash-command` entry point |
| Key functions that involve **multi-step reasoning or orchestration** | Agent | User needs an autonomous workflow |
| External integrations selected | .mcp.json | Plugin needs MCP server connections |
| Strategic questions defined | Embedded in skills and agents | Guide decision-making within components |
| Constraints defined | Embedded in skills + telemetry | Enforced as guardrails and tracked as violations |
| Success metrics + data sources | Performance command (if data source is accessible) | Enable self-measurement |

**Rules:**
- Every plugin gets at least ONE skill (the primary domain skill)
- Every plugin gets the telemetry skill (non-negotiable — see `references/telemetry-template.md`)
- Only create agents if the workflow genuinely requires multi-step orchestration
- Only create commands if there's a clear, repeatable user-initiated action
- Create a performance/metrics command if at least one data source from Q7 is programmatically accessible

### Step 2: Name Components

Follow Olytic naming conventions from `references/olytic-patterns.md`:

- **Plugin name:** kebab-case, 2-4 words, descriptive (e.g., `customer-success-tracker`)
- **Skills:** `[domain]-[function]` (e.g., `proposal-standards`, `deal-qualification`)
- **Commands:** `[verb]-[object]` (e.g., `pull-metrics`, `score-health`, `review-proposal`)
- **Agents:** `[role]-[responsibility]` (e.g., `deal-analyst`, `proposal-reviewer`)

### Step 3: Generate Plugin Structure

Create this directory structure:

```
[plugin-name]/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json                    # Only if integrations exist
├── README.md
├── skills/
│   ├── plugin-telemetry/        # ALWAYS included — non-negotiable
│   │   └── SKILL.md
│   └── [domain-skill]/
│       ├── SKILL.md
│       └── references/          # Only if domain needs detailed reference material
│           └── [reference].md
├── agents/                      # Only if agents are needed
│   └── [agent-name].md
└── commands/                    # Only if commands are needed
    └── [command-name].md
```

### Step 4: Generate Each File

#### plugin.json

```json
{
  "name": "[kebab-case-name]",
  "version": "0.1.0",
  "description": "[plugin_purpose from discovery — one sentence, under 120 chars]",
  "author": {
    "name": "[Olytic Solutions for internal, client name for client plugins]",
    "email": "[support@olyticsolutions.com for internal, client email for client plugins]"
  },
  "keywords": ["[3-6 relevant keywords from discovery]"]
}
```

#### .mcp.json (only if integrations exist)

Generate MCP server entries for each integration from discovery Q5. Common patterns:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

For integrations without a known MCP server URL, add a comment in README noting the integration needs configuration.

#### Telemetry Skill

**This is mandatory for every generated plugin.** Copy and customize from `references/telemetry-template.md`. Replace:
- `[PLUGIN_NAME]` → actual plugin name
- `[PLUGIN_VERSION]` → "0.1.0"
- `[CONSTRAINTS]` → constraints from discovery Q4
- `[SUCCESS_METRICS]` → metrics from discovery Q6

#### Domain Skills

For each domain skill, generate using the pattern from `references/component-templates.md`. Key rules:

- **Frontmatter description** must include 4-6 specific trigger phrases in the user's language
- **Body** starts with a context paragraph explaining scope
- **Strategic questions** from Q3 are embedded as a "Before You Start" or "Decision Framework" section
- **Constraints** from Q4 are embedded as a "Boundaries" or "Out of Scope" section
- **Operating Principles** section must be included (from `references/agentic-best-practices.md`):
  - Discovery first: Assess current state before taking action
  - Source of truth: Local files and skill content take precedence over conversation
  - Atomic operations: Make the smallest change necessary
  - Verify after writing: Confirm output is valid after every write operation
  - No hallucination: Report "Not Found" rather than guessing
- **Structure** uses H2 sections, bullets, tables, bold key terms (Olytic voice)
- If the skill needs detailed reference material, create `references/` files

#### Agents

For each agent, generate using the pattern from `references/component-templates.md`. Key rules:

- **Frontmatter** includes `name`, `description` with trigger phrases, 2 `<example>` blocks with `<commentary>`, `model: inherit`, `color`, `tools` list
- **Color assignment:** Pick from yellow, magenta, cyan, green, orange — no two agents in the same plugin share a color
- **Tools list** should match what the agent actually needs (Read, Write, Grep, Glob, WebSearch, WebFetch, plus any MCP tools from integrations)
- **Body** includes: role description, core responsibilities (3-6 bullets), analysis process (numbered steps), output format (exact template)
- **Strategic questions** from Q3 inform the agent's decision-making logic
- **Agentic rules section** must be included in every agent body:
  - Map environment before acting — use search/glob to understand what exists
  - Treat skill content as authoritative over conversational context
  - Batch related operations to minimize token overhead
  - Use targeted search over full-file reads for large files
  - Verify every write operation succeeded
  - Never fabricate data — report missing information explicitly
  - Confirm with user before destructive actions or 5+ file changes

#### Commands

For each command, generate using the pattern from `references/component-templates.md`. Key rules:

- **Frontmatter** includes `description` (one line), `argument-hint` (example usage), `allowed-tools` (specific tool list)
- **Body** is instructions FOR Claude, not documentation for the user
- **Steps** are numbered, specific, and include confirmation before destructive actions
- **Integration-specific tools** reference MCP servers by full name (e.g., `mcp__github__get_file_contents`)
- **Verification gate:** Every command that writes files or modifies external systems must include a verification step after the write to confirm success
- **Permission gate:** Commands that perform destructive actions or make 5+ simultaneous changes must ask for user confirmation
- **No hallucination:** Commands must report "Not Found" for missing files/data rather than guessing

#### README.md

Generate from discovery data:

```markdown
# [Plugin Name]

[plugin_purpose — one paragraph]

**Audience:** [user_profile]
**Requires:** [dependencies — e.g., "The One Ring governance plugin" if Olytic internal]

## Components

### Skills
- **[skill-name]** — [description]
- **plugin-telemetry** — Automatic usage logging, version tagging, violation tracking, and feedback capture

### Commands
- `/[command-name] [args]` — [description]

### Agents
- **[agent-name]** — [description]

### Integrations
- **[Service]** — [what it connects to and why]

## Strategic Questions

When using this plugin, always consider:
[strategic_questions as numbered list]

## Boundaries

This plugin should NOT be used for:
[constraints as bullet list]

## Success Metrics

| Metric | Data Source | How to Measure |
|--------|-----------|----------------|
| [metric] | [source] | [method] |

## Installation

[Installation command — marketplace for Olytic internal, manual for client]

## Customization

[Which files to edit for different changes]
```

### Step 5: Review Generated Structure

Before writing files, present the component plan to the user:

```
## Generated Plugin: [name]

| Component | Type | Name | Purpose |
|-----------|------|------|--------|
| Skill | Domain | [name] | [purpose] |
| Skill | Telemetry | plugin-telemetry | Usage logging and violation tracking |
| Command | Action | /[name] | [purpose] |
| Agent | Workflow | [name] | [purpose] |

Total files: [count]
```

Ask: "Does this look right? Any components to add, remove, or change before I generate the files?"

### Step 6: Write Files and Package

1. Create all files in the plugin directory
2. **Verification gate:** After writing all files, verify the plugin structure:
   - Use Glob to confirm all expected files exist
   - Verify plugin.json is valid JSON
   - Verify every skill has a SKILL.md with valid frontmatter
   - Verify every agent has valid frontmatter (name, description, model, color, tools)
   - Verify every command has valid frontmatter (description, argument-hint, allowed-tools)
   - Verify plugin-telemetry/SKILL.md exists (mandatory)
   - If any verification fails, fix the issue before proceeding
3. Package as `.plugin` file:
   ```bash
   cd /path/to/plugin-dir && zip -r /tmp/[name].plugin . -x "*.DS_Store" && cp /tmp/[name].plugin /path/to/outputs/[name].plugin
   ```
4. Present the `.plugin` file to the user
5. Ask: "Want me to add this to the Olytic marketplace?"
   - If yes, invoke the marketplace-management skill
