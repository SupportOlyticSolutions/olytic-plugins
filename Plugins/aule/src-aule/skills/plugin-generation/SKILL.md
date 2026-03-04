---
name: plugin-generation
description: >
  Use this skill after completing plugin discovery, when you need to "generate the plugin",
  "create the plugin files", "build out the plugin", "produce the plugin", "write the plugin code",
  "generate plugin from discovery", "make the plugin from our plan", or "turn this into a plugin".
  Takes the discovery summary and produces a complete, ready-to-use plugin following Olytic conventions.
  Every generated plugin automatically includes telemetry, integrity controls, permissions manifest,
  and documentation. See references/ for templates and patterns.
version: 0.2.0
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

## Folder Structure Reference

**Read this first:** `references/olytic-folder-structure.md` — Complete guide to how plugins are organized in the repo.

**Quick summary:**
- All plugins live in `plugins-workspace/[plugin-name]/`
- Inside: `src-[plugin-name]/` (actual plugin source), `[plugin-name].metadata.json` (metadata sidecar), and `[plugin-name].zip` (packaged plugin)
- Metadata and zip files are **sidecars in the parent folder**, NOT inside the `src-[plugin-name]/` folder

## Generation Process

### Step 0: Discovery First — Map the Environment

Before generating anything:
1. Check if a plugin with this name already exists in `plugins-workspace/[plugin-name]/src-[plugin-name]/` (use Glob)
2. Check if a marketplace entry already exists (use the marketplace-management skill)
3. If the plugin exists, ask: "A plugin named [name] already exists. Do you want to update it or create a new one?"
4. If not, proceed to Step 1

**Folder structure awareness:**
- All plugins live in `plugins-workspace/[plugin-name]/`
- Each plugin has: `src-[plugin-name]/` (the actual plugin source), `[plugin-name].zip`, and `[plugin-name].metadata.json`
- When you generate a plugin, you're writing files into the `src-[plugin-name]/` folder
- The zip and metadata files are sidecars in the parent folder, created after generation

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
| Memory scope declared (from Q5) | Memory declaration in skill + README | Plugin declares its context retention requirements |
| Workflow context mapped (from Q6) | Augmentation framing in README + skill descriptions | Positions plugin around new capabilities, not just task speedup |
| Augmentation signal weak | Advisory note in README | Flags the plugin as primarily an accelerator, suggests augmentation opportunities |
| Claude OS framing (from new questions) | Claude OS Identity block in README | Declares hat role, relationships, governance, dimension, compounding |

**Rules:**
- Every plugin gets at least ONE skill (the primary domain skill)
- Every plugin gets the telemetry skill (non-negotiable — see `references/telemetry-template.md`)
- Only create agents if the workflow genuinely requires multi-step orchestration
- Only create commands if there's a clear, repeatable user-initiated action
- Create a performance/metrics command if at least one data source from Q8 is programmatically accessible
- Every plugin must include a Claude OS Identity block in its README (see Step 4b below)

### Step 2: Name Components

Follow Olytic naming conventions from `references/olytic-patterns.md`:

- **Plugin name:** kebab-case, 2-4 words, descriptive (e.g., `customer-success-tracker`)
- **Skills:** `[domain]-[function]` (e.g., `proposal-standards`, `deal-qualification`)
- **Commands:** `[verb]-[object]` (e.g., `pull-metrics`, `score-health`, `review-proposal`)
- **Agents:** `[role]-[responsibility]` (e.g., `deal-analyst`, `proposal-reviewer`)

### Step 2a: Validate Component Name Uniqueness

Before proceeding to file generation, check that **no two components share the same name** across skills, commands, and agents. Skills, commands, and agents share the same qualified namespace (`plugin-name:component-name`), so names must be unique across all three types within a plugin.

Collect all planned names:
- Skill directory names (e.g., `proposal-standards`)
- Command file names without `.md` (e.g., `review-proposal`)
- Agent file names without `.md` (e.g., `proposal-reviewer`)

If any duplicates exist, rename the component with the weaker claim to the name:
- **Skills** (knowledge/standards) should add a suffix like `-standards`, `-guide`, or `-framework`
- **Commands** (actions) keep the verb-object name since users invoke them directly
- **Agents** (roles) keep the role-responsibility name

**This check is non-negotiable.** A duplicate will cause the plugin to register the same qualified name for two different components, creating unpredictable behavior.

### Step 3: Generate Plugin Structure

Create this directory structure **inside** `plugins-workspace/[plugin-name]/src-[plugin-name]/`:

```
plugins-workspace/
└── [plugin-name]/
    ├── src-[plugin-name]/       # The actual plugin source code (this is what you generate into)
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   ├── .mcp.json            # Only if integrations exist
    │   ├── README.md
    │   ├── skills/
    │   │   ├── [plugin-name]-telemetry/    # ALWAYS included — non-negotiable
    │   │   │   └── SKILL.md
    │   │   └── [domain-skill]/
    │   │       ├── SKILL.md
    │   │       └── references/      # Only if domain needs detailed reference material
    │   │           └── [reference].md
    │   ├── agents/                  # Only if agents are needed
    │   │   └── [agent-name].md
    │   └── commands/                # Only if commands are needed
    │       └── [command-name].md
    ├── [plugin-name].metadata.json  # Sidecar metadata (in parent folder, NOT in src/)
    └── [plugin-name].zip            # Packaged plugin (in parent folder)
```

**Key:** Write all plugin files into the `src-[plugin-name]/` subfolder. The metadata and zip files are siblings in the parent folder (`plugins-workspace/[plugin-name]/`).

### Step 4: Generate Each File

#### plugin.json

Write to `.claude-plugin/plugin.json`. Use ONLY these keys — no others:

```json
{
  "name": "[kebab-case-name]",
  "version": "0.1.0",
  "description": "[plugin_purpose from discovery — one sentence, under 120 chars]",
  "author": {
    "name": "[Olytic Solutions for internal, client name for client plugins]",
    "email": "[support@olyticsolutions.com for internal, client email for client plugins]"
  },
  "keywords": ["keyword1", "keyword2", "keyword3"]
}
```

**⚠️ Valid keys only:** `name`, `version`, `description`, `author`, `keywords`, `hooks`. Do NOT include `sublabel`, `icon`, `displayName`, `permissions`, or any other key — unrecognized keys cause upload failure. Keywords must be an array of plain strings, not a single placeholder string.

**Immediately after writing plugin.json**, run this validation bash command to confirm the file was written correctly. Do NOT proceed until this passes:

```bash
python3 -c "
import json, sys
try:
    with open('.claude-plugin/plugin.json') as f:
        content = f.read()
    if not content.strip():
        print('FAIL: plugin.json is empty — rewrite the file')
        sys.exit(1)
    data = json.loads(content)
    valid_keys = {'name','version','description','author','keywords','hooks'}
    bad_keys = [k for k in data if k not in valid_keys]
    missing = [k for k in ['name','version','description','author'] if k not in data]
    if bad_keys:
        print('FAIL: unrecognized keys (will cause upload failure):', bad_keys)
        sys.exit(1)
    if missing:
        print('FAIL: missing required fields:', missing)
        sys.exit(1)
    print('OK — plugin.json is valid')
    print(json.dumps(data, indent=2))
except json.JSONDecodeError as e:
    print('FAIL: invalid JSON —', e)
    sys.exit(1)
except FileNotFoundError:
    print('FAIL: .claude-plugin/plugin.json not found — check the write path')
    sys.exit(1)
"
```

If this script exits with an error, fix the file and re-run before continuing.

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
- `[SUCCESS_METRICS]` → metrics from discovery Q8

**Blueprint compliance:** The telemetry template implements `shared/telemetry-blueprint/TELEMETRY-STANDARDS.md` — the canonical standard Aulë owns. Before generating the telemetry skill for any plugin, confirm the template in `references/telemetry-template.md` matches the current blueprint version. The blueprint defines the nine required event types, the JSONL format, field ordering, and visibility rules. Do not deviate from it. If the blueprint has changed since the template was last updated, update the template first, then generate.

#### Domain Skills

For each domain skill, generate using the pattern from `references/component-templates.md`. Key rules:

- **Frontmatter description** must include 4-6 specific trigger phrases in the user's language
- **Body** starts with a context paragraph explaining scope
- **Strategic questions** from Q3 are embedded as a "Before You Start" or "Decision Framework" section
- **Constraints** from Q4 are embedded as a "Boundaries" or "Out of Scope" section
- **Memory scope** (from Q5): If the skill requires context persistence or retrieval, include a Memory Scope section declaring what information must be retained across sessions and for how long. If discovery Q5 indicates 'retrieval' memory scope, include retrieval configuration in the skill: what sources to search, freshness requirements, and fallback behavior when sources are unavailable.
- **Content processing security** (from Q7): If the plugin processes external content (user uploads, web data, third-party API responses), include prompt injection defense patterns: input validation, output filtering, and clear boundaries between trusted instructions and untrusted data.
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

- **Frontmatter YAML structure (critical):** The `---` frontmatter block must contain ONLY valid YAML key-value pairs: `name`, `description`, `model`, `color`, `tools`. The `<example>` blocks are NOT valid YAML and must be placed AFTER the closing `---`, not inside it. Placing examples inside the frontmatter causes a YAML parse error that breaks plugin upload.
- **Agent description format (critical):** Always write agent descriptions using the `description: >` block scalar format. Never use a single-line unquoted description. A single-line description containing `: ` (colon + space) will cause a "mapping values are not allowed here" YAML parse error on upload.
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

### Step 4a: Generate Permissions Manifest

**This is mandatory for every generated plugin.** Create a new section in the README (see Step 4b's README.md template below).

The permissions manifest is a structured declaration of:

- **Tools accessed:** Which Claude tools does the plugin use? (Read, Write, Grep, Glob, WebSearch, WebFetch, etc.)
- **MCP servers:** What external systems does it connect to? (GitHub, Slack, databases, APIs, etc.)
- **Data reads:** What data sources does the plugin read from? (local files, APIs, databases, user uploads)
- **Data writes:** What does it write to? (files, external APIs, logs, caches)
- **External services called:** Third-party APIs, webhooks, or cloud services
- **Human-in-the-loop checkpoints:** Which operations require user confirmation before execution? (destructive actions, payments, access grants, data transmission)

Example structure:

```markdown
## Permissions Manifest

### Tools
- Read: Local filesystem access
- Write: Skill and command file creation
- Grep: Code searching
- Glob: Directory traversal
- WebFetch: External documentation fetching

### Integrations
- GitHub API: Read repository contents, create issues

### Data Access
**Reads:** Repository files, issue metadata
**Writes:** Local skill cache, telemetry logs
**Retention:** Telemetry logs stored for 90 days

### Human-in-the-Loop Checkpoints
- ✓ Required before creating issues
- ✓ Required before modifying repository permissions
- ✓ Required before sharing analysis results externally
```

### Step 4b: Generate Claude OS Identity Block

**This is mandatory for every generated plugin.** Create a new section in the README called **Claude OS Identity** that appears early in the document, after the opening description and before Components.

Populate this block using answers from the Claude OS Framing Questions in discovery:

```markdown
## Claude OS Identity

**Hat:** [Plugin Name] is the [role] hat in the Claude OS — the platonic ideal of [job-to-be-done description from hat_identity].

**Dimension:** This plugin primarily serves the [Unified / Custom / Augmenting / Agentic / Compounding] dimension of the Claude OS. [Brief statement of why: does it help plugins work together, enable personalization, create new capabilities, leverage advanced reasoning, or feed the improvement loop?]

**Governance dependency:** [This plugin assumes The One Ring is installed / This plugin works standalone / Other]. [List which skills it references: e.g., "Uses The One Ring's olytic-brand-standards skill for voice and positioning rules."]

**Relationships to other hats:**
- [Plugin A]: [How this plugin uses or feeds Plugin A — e.g., "proposal-builder feeds completed proposals to proposal-auditor for review"]
- [Plugin B]: [How this plugin interacts]

**Compounding contribution:** [What telemetry does this plugin log that feeds the Optimizer? e.g., "Logs every audit result, constraint violation, and user feedback signal. The Optimizer watches violation patterns to recommend improvements to both proposal-builder and brand standards."]
```

Use the discovery answers to populate each field. If a field wasn't answered (e.g., no other plugins exist yet), note it explicitly (e.g., "No other hats yet" or "Governance dependency: This standalone client plugin does not reference The One Ring").

#### README.md

Generate from discovery data:

```markdown
# [Plugin Name]

Enables [user] to [new capability] — [one paragraph describing what makes this augmentation valuable, not just what it automates].

**Audience:** [user_profile]
**Requires:** [dependencies — e.g., "The One Ring governance plugin" if Olytic internal]

## Claude OS Identity

[See Step 4b — mandatory block declaring hat role, dimension, governance, relationships, and compounding contribution]

## Components

### Skills
- **[skill-name]** — [description]
- **[plugin-name]-telemetry** — Automatic usage logging, version tagging, violation tracking, and feedback capture

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

## Memory Scope

This plugin [retains/does not retain] context across sessions:
- [What information is retained]
- [Retention period or conditions]
- [How to clear retained context if needed]

## Permissions Manifest

[See Step 4a — structured declaration of tools, integrations, data access, and human-in-the-loop checkpoints]

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
| Skill | Telemetry | [plugin-name]-telemetry | Usage logging and violation tracking |
| Command | Action | /[name] | [purpose] |
| Agent | Workflow | [name] | [purpose] |

Total files: [count]
```

Ask: "Does this look right? Any components to add, remove, or change before I generate the files?"

### Step 6: Write Files, Validate, and Package

1. **Write all files** using the Write tool with absolute paths. plugin.json goes at `.claude-plugin/plugin.json` inside the plugin directory.

2. **Run the plugin.json validation script** (shown in Step 4 above) immediately after writing it. Fix and rewrite if it fails. Do not skip this step.

3. **Verify all required files exist:**
   ```bash
   ls .claude-plugin/plugin.json README.md skills/[plugin-name]-telemetry/SKILL.md
   ```
   If any file is missing, write it now.

4. **Verify Claude OS Identity block exists in README:**
   ```bash
   grep -q "## Claude OS Identity" README.md && echo "OK — Claude OS Identity block found" || echo "FAIL: missing Claude OS Identity block"
   ```
   If missing, add it now using the template from Step 4b.

5. **Verify no duplicate component names** across skills, commands, and agents:
   ```bash
   python3 -c "
   import os, sys
   skills = [d for d in os.listdir('skills') if os.path.isdir(f'skills/{d}')] if os.path.isdir('skills') else []
   commands = [f.replace('.md','') for f in os.listdir('commands') if f.endswith('.md')] if os.path.isdir('commands') else []
   agents = [f.replace('.md','') for f in os.listdir('agents') if f.endswith('.md')] if os.path.isdir('agents') else []
   all_names = skills + commands + agents
   dupes = [n for n in set(all_names) if all_names.count(n) > 1]
   if dupes:
       print('FAIL: duplicate component names found:', dupes)
       print('  Skills:', skills)
       print('  Commands:', commands)
       print('  Agents:', agents)
       sys.exit(1)
   print('OK — all component names are unique across skills, commands, and agents')
   print(f'  Skills ({len(skills)}):', skills)
   print(f'  Commands ({len(commands)}):', commands)
   print(f'  Agents ({len(agents)}):', agents)
   "
   ```
   If this fails, rename the conflicting component (see Step 2a rules) and rewrite the affected files.

6. **Verify agent files** (if the plugin has agents):
   - **Frontmatter structure:** Confirm the block between `---` delimiters contains only `name`, `description`, `model`, `color`, `tools`. If `<example>` tags appear inside the frontmatter, move them to after the closing `---`.
   - **Unquoted colons in descriptions:** If any agent's `description` value contains `: ` (colon followed by space) on a single line, convert it to `description: >` block scalar format.
   - **Valid keys in plugin.json:** Confirm no `displayName` or other non-standard keys exist.

7. **Create plugin metadata file.** In the parent folder `plugins-workspace/[plugin-name]/`, create `[plugin-name].metadata.json`:
   ```json
   {
     "id": "[plugin-id]",
     "name": "[Plugin Name]",
     "description": "[extended description from discovery]",
     "image": "assets/logo.png",
     "label": "[category label]",
     "version": "0.1.0",
     "lastCortexUpdate": null,
     "cortexTopics": [],
     "relationships": {
       "dependsOn": [],
       "complementaryPlugins": []
     },
     "customFields": {
       "tier": "tier-2",
       "owner": "[team]",
       "usageScore": 0,
       "maturityLevel": "beta"
     }
   }
   ```

8. **Package the plugin.** Run this from INSIDE the `src-[plugin-name]/` directory (not the parent):
   ```bash
   cd /absolute/path/to/plugins-workspace/[plugin-name]/src-[plugin-name] && \
   zip -r /tmp/[plugin-name].plugin . -x "*.DS_Store" -x ".git/*" && \
   echo "Packaged successfully"
   ```
   **Critical:** The `cd` must go INTO the `src-[plugin-name]/` directory (e.g., `plugins-workspace/my-plugin/src-my-plugin`), not the parent folder. If you zip from the parent, the zip will have a subfolder wrapper and the validator will not find `.claude-plugin/plugin.json`.

9. **Verify the zip contains the right structure AND valid plugin.json:**
   ```bash
   # Step 1: Confirm plugin.json is at root level (not inside a subfolder)
   unzip -l /tmp/[plugin-name].zip | grep -E "plugin\.json|SKILL\.md"
   ```
   The output must show `.claude-plugin/plugin.json` at the root (not inside a subdirectory). If you see `src-[plugin-name]/.claude-plugin/plugin.json`, the zip is wrong — you ran it from the parent directory. Fix the cd path and repackage.

   ```bash
   # Step 2: Extract plugin.json from the zip and validate its keys
   unzip -p /tmp/[plugin-name].zip .claude-plugin/plugin.json | python3 -c "
   import json, sys
   data = json.load(sys.stdin)
   valid_keys = {'name','version','description','author','keywords','hooks'}
   bad_keys = [k for k in data if k not in valid_keys]
   if bad_keys:
       print('FAIL: zip contains plugin.json with unrecognized keys (will cause upload failure):', bad_keys)
       sys.exit(1)
   print('OK — plugin.json inside zip is valid, no unrecognized keys')
   print('Keys present:', list(data.keys()))
   "
   ```
   If this fails, the zip is packaging the wrong plugin.json. Fix the source file, re-run the validation script from Step 4, then repackage.

10. **Copy the zip to the parent folder:**
    ```bash
    cp /tmp/[plugin-name].plugin /absolute/path/to/plugins-workspace/[plugin-name]/[plugin-name].zip
    ```

11. Present the packaged plugin structure to the user.

11. Ask: "Want me to add this to the Olytic marketplace?"
    - If yes, invoke the marketplace-management skill

---

## Telemetry Instrumentation

This skill captures the critical decision points in plugin generation — which components are created, what verification gates pass/fail, and whether the generated plugin meets the user's expectations.

### 1. Skill Invocation Event

At the **start** of generation, log:

```jsonl
{"timestamp":"2026-03-03T10:35:00Z","event":"skill_invoke","plugin":"aule","plugin_version":"0.2.0","component":"plugin-generation","trigger":"user approved plugin discovery summary and approved generation"}
```

**When:** After the user confirms the discovery summary from plugin-discovery, and before you start generating the first file.

### 2. Decision Trace Events — Component Selection

When you **decide which component types to generate** (skills, agents, commands) based on discovery answers, log:

```jsonl
{"timestamp":"2026-03-03T10:36:00Z","event":"decision_trace","plugin":"aule","plugin_version":"0.2.0","component":"plugin-generation","input_summary":"user described 3 key functions: validate content, synthesize feedback, check compliance","reasoning":["validation is a knowledge task → skill component","synthesis requires multi-step reasoning → agent component","compliance is a discrete action → command component"],"output_summary":"planned architecture: 1 agent (synthesis), 2 skills (validation, compliance), 1 command (check-status)","confidence":"high"}
```

**When:** Log this after Step 1 when you've analyzed the discovery output and decided on component breakdown.

**Why:** These decision traces show which user inputs lead to which architectural choices — essential for optimizing the generation templates.

### 3. Decision Trace Events — Template Selection

When you **select which reference templates** to use for each component, log:

```jsonl
{"timestamp":"2026-03-03T10:37:00Z","event":"decision_trace","plugin":"aule","plugin_version":"0.2.0","component":"plugin-generation","input_summary":"validation skill handles PII-sensitive content classification","reasoning":["skill processes user data → use prompt-injection-defense template","classification is deterministic → use simple lookup pattern, not agentic","compliance context required → include memory-scope declaration"],"output_summary":"selected standard-skill-template with prompt-defense injection pattern and memory declaration","confidence":"high"}
```

**When:** Log after Step 2 when you're mapping templates to components.

### 4. Permission Gate Events — Before Destructive Operations

When you're about to **write files to the file system** (especially if it's an update to an existing plugin), log:

```jsonl
{"timestamp":"2026-03-03T10:40:00Z","event":"permission_gate","plugin":"aule","plugin_version":"0.2.0","action_type":"bulk_change","description":"about to create 7 new skill files, 1 agent, 2 commands, and .claude-plugin/ directory for plugin 'content-reviewer'","user_decision":"approved"}
```

**Required fields:**
- `timestamp` — ISO 8601 UTC time with Z suffix
- `event` — literal string "permission_gate"
- `plugin` — literal string "aule"
- `plugin_version` — from the skill frontmatter
- `action_type` — "destructive" (if overwriting existing files) or "bulk_change" (if creating 5+ files)
- `description` — what files will be created/modified
- `user_decision` — "approved" or "denied" (log after user responds)

**When:** Log before calling the file creation tools in Step 3. Present the user with a summary of what will be created and ask for confirmation before writing.

**Why:** Permission gates ensure users are aware of file-system side effects and can intervene if needed.

### 5. Verification Gate Events — After File Creation

After **writing plugin files** in Step 3, verify they exist and log:

```jsonl
{"timestamp":"2026-03-03T10:41:00Z","event":"verification_gate","plugin":"aule","plugin_version":"0.2.0","result":"pass","component":"plugin-generation","description":"verified all 10 plugin files created correctly: 3 skills, 1 agent, 2 commands, plugin.json, README, .gitignore, LICENSE"}
```

**Required fields:**
- `timestamp` — ISO 8601 UTC time with Z suffix
- `event` — literal string "verification_gate"
- `plugin` — literal string "aule"
- `plugin_version` — from the skill frontmatter
- `result` — "pass" or "fail"
- `component` — literal string "plugin-generation"
- `description` — what was written and what was checked

**When:** Log after each major write operation (after Step 3 creates files, after Step 4 creates metadata).

**If result="fail":** Log what went wrong and stop — do not proceed to packaging. Ask the user for permission to retry or to debug.

**Why:** Verification gates are a critical safety mechanism. They ensure that plugin generation doesn't silently fail and leave the user with corrupted files.

### 6. Verification Gate Events — Plugin Structure Validation

After **validating plugin structure** in Step 5, log:

```jsonl
{"timestamp":"2026-03-03T10:43:00Z","event":"verification_gate","plugin":"aule","plugin_version":"0.2.0","result":"pass","component":"plugin-generation","description":"plugin structure validation passed: all component names unique, no duplicate keys in plugin.json, agent frontmatter valid"}
```

**When:** Log after Step 5 validation checks complete.

### 7. Verification Gate Events — Packaging

After **packaging the plugin** in Step 8, verify the zip is correct and log:

```jsonl
{"timestamp":"2026-03-03T10:45:00Z","event":"verification_gate","plugin":"aule","plugin_version":"0.2.0","result":"pass","component":"plugin-generation","description":"plugin packaged successfully: zip created at /tmp/content-reviewer.plugin, verified .claude-plugin/plugin.json at root level"}
```

**When:** Log after the zip is created and verified in Step 9.

### 8. Decision Trace — Packaging Success

When packaging completes successfully, optionally log a summary decision trace:

```jsonl
{"timestamp":"2026-03-03T10:46:00Z","event":"decision_trace","plugin":"aule","plugin_version":"0.2.0","component":"plugin-generation","input_summary":"plugin generation completed all 8 steps for 'content-reviewer' plugin","reasoning":["all files created without errors","structure validation passed all checks","zip packaged correctly with proper nesting"],"output_summary":"ready for marketplace registration or manual deployment","confidence":"high"}
```

### 9. Feedback Events

If the user provides **significantly positive or negative** feedback about the generated plugin, log:

```jsonl
{"timestamp":"2026-03-03T10:50:00Z","event":"feedback","plugin":"aule","plugin_version":"0.2.0","sentiment":"positive","component":"plugin-generation","context":"user said the generated plugin exactly matched what they wanted to build","output_summary":"generated complete 'content-reviewer' plugin with 3 skills, 1 agent, 2 commands"}
```

**When:** Log ONLY if the user explicitly praises ("This is perfect", "Exactly what I needed") OR explicitly criticizes ("This isn't right", "Start over") the generated plugin.

**Do NOT log:** Normal refinement requests ("Can you adjust the skill description?" or "Add one more command").

**Why:** Feedback signals help the Optimizer understand which generation templates produce user-approved plugins.

### 10. Violation Events

If a user tries to bypass generation or violates plugin-generation constraints, log:

```jsonl
{"timestamp":"2026-03-03T10:35:00Z","event":"violation","plugin":"aule","plugin_version":"0.2.0","violation_type":"constraint_breach","description":"user asked to generate a plugin with API keys hardcoded in skill files","constraint_violated":"Do NOT create plugins that embed personal data, credentials, or API keys in skill files","action_taken":"refused — explained security risk and suggested credential injection pattern instead"}
```

**Plugin-generation constraints are:**
- Do NOT generate plugin files without completing discovery first
- Do NOT create plugins with hardcoded credentials or PII
- Do NOT skip verification steps — all files must be validated before packaging
- Do NOT package the plugin from the parent directory (must cd into src-[plugin-name]/)

**When:** Log when a user explicitly tries to bypass generation or requests something that violates constraints.

**Important:** When you log a violation, explain to the user why the request is problematic and suggest the correct alternative.

---

Telemetry: This skill logs all invocations via [plugin-name]-telemetry.
