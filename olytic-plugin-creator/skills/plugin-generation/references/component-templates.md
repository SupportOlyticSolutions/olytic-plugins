# Component Generation Templates

Use these templates when generating plugin components from discovery data. Each template shows the exact structure with placeholders mapped to discovery fields.

## Skill Template

```markdown
---
name: [discovery.key_functions[0] as kebab-case identifier]
description: >
  This skill should be used when the user asks to "[key_function_1 as natural phrase]",
  "[key_function_2 as natural phrase]", "[key_function_3 as natural phrase]",
  or needs guidance on [discovery.plugin_purpose paraphrased as user need].
  [If Olytic internal: "Assumes The One Ring plugin is installed for brand standards."]
version: 0.1.0
---

# [Skill Title — descriptive, matches domain]

[Context paragraph: what this skill covers, who it's for, when to load it.]

## Before You Start

When using this skill, ask yourself:

[discovery.strategic_questions as numbered list]

These questions ensure you're using this plugin with judgment, not just mechanically.

## [Primary Content Section]

[Generated from discovery.key_functions — organize the domain knowledge that supports each function. Use H2 sections, bullets, tables, bold key terms.]

## [Secondary Content Section]

[Additional domain knowledge, frameworks, templates, or reference material.]

## Operating Principles

These principles govern how this skill behaves:

- **Discovery first:** Before taking action, assess the current state. Use search/glob to understand what exists. Never recreate existing files or structures.
- **Source of truth:** Local files and skill content take precedence over conversational context. If a conflict exists, the file wins.
- **Atomic operations:** Make the smallest change necessary. Use targeted edits, not full-file rewrites.
- **Verify after writing:** Confirm output is valid after every write operation.
- **No hallucination:** If a variable, file path, or data point is not found, report "Not Found" immediately. Never guess or estimate.

## Boundaries

This skill should NOT be used for:

[discovery.constraints as bullet list]
[discovery.out_of_scope as bullet list]

If a request falls outside these boundaries, explain why and suggest alternatives.

## References

[If detailed reference material is needed:]
For [topic], see `references/[filename].md`.

---
Telemetry: This skill logs all invocations via plugin-telemetry.
```

### Mapping Discovery → Skill Content

| Discovery Field | Skill Location |
|----------------|----------------|
| `plugin_purpose` | Context paragraph |
| `key_functions` | H2 sections organizing domain knowledge |
| `strategic_questions` | "Before You Start" section |
| `constraints` + `out_of_scope` | "Boundaries" section |
| `user_profile` | Informs tone and complexity level |
| `success_metrics` | Referenced where relevant to ground advice in outcomes |

---

## Agent Template

> ⚠️ **YAML structure rule:** The YAML frontmatter (between the `---` delimiters) must contain ONLY valid YAML key-value pairs. The `<example>` blocks are NOT valid YAML and must be placed AFTER the closing `---`. Putting examples inside the frontmatter causes a YAML parse failure and breaks plugin upload.

```markdown
---
name: [role]-[responsibility]
description: Use this agent when the user asks to "[key_function as action phrase]", "[related action]", "[broader context trigger]", or needs [discovery.plugin_purpose as user need requiring multi-step reasoning].
model: inherit
color: [assigned color from olytic-patterns.md]
tools: [tools needed — Read, Write, Grep, Glob, plus any MCP tools from discovery.integrations]
---

<example>
Context: [Realistic scenario from discovery.user_profile's typical day]
user: "[Natural message a user_profile person would send]"
assistant: "I'll use the [agent-name] agent to [what it will do]."
<commentary>
[Why this agent is appropriate — references the multi-step nature of the task.]
</commentary>
</example>

<example>
Context: [Different scenario from discovery.key_functions]
user: "[Different natural message]"
assistant: "Let me use the [agent-name] agent to [what it will do]."
<commentary>
[Why this agent handles this better than a simple skill or command.]
</commentary>
</example>

You are [organization]'s [role description]. [One sentence about what you do and why.]

[If Olytic internal: "This agent assumes The One Ring governance plugin is installed and will reference brand standards and company strategy from it."]

**Your Core Responsibilities:**

1. [Responsibility derived from key_function_1]
2. [Responsibility derived from key_function_2]
3. [Responsibility derived from key_function_3]
4. [Additional responsibility based on strategic_questions]
5. Connect every output to success metrics: [discovery.success_metrics as brief list]

**Decision Framework:**

Before producing output, consider:
[discovery.strategic_questions as numbered list]

**Process:**

1. [Step 1 — typically: understand the request, gather context]
2. [Step 2 — analyze, research, or process]
3. [Step 3 — produce structured output]
4. [Step 4 — validate against constraints]
5. [Step 5 — present with recommendations]

**Output Format:**

## [Output Title]

[Exact template the agent should follow — tables, sections, bullet lists. Customize based on what the agent produces.]

**Agentic Rules:**

These rules are non-negotiable for this agent:

- Map environment before acting — use search/glob to understand what exists before making changes
- Treat skill content as authoritative over conversational context
- Batch related operations to minimize token overhead
- Use targeted search (Grep/Glob) over full-file reads for large files
- Verify every write operation succeeded — confirm file structure is valid after writes
- Never fabricate data — if a file, path, or data point is not found, report "Not Found" immediately
- Confirm with user before destructive actions (delete/overwrite) or 5+ simultaneous file changes

**Boundaries:**

Do NOT:
[discovery.constraints as bullet list]

If a request falls outside scope, explain why and redirect.
```

### Mapping Discovery → Agent Content

| Discovery Field | Agent Location |
|----------------|----------------|
| `key_functions` (complex ones) | Core responsibilities + examples |
| `strategic_questions` | Decision framework section |
| `constraints` | Boundaries section + example commentary |
| `integrations` | Tools list in frontmatter |
| `success_metrics` | Referenced in responsibilities |
| `user_profile` | Informs example scenarios |

---

## Command Template

```markdown
---
description: [One-line description of the action — verb phrase]
argument-hint: [example-arg] (e.g., [concrete example with explanation])
allowed-tools: ["Tool1", "Tool2", "mcp__service__tool_name"]
---

[Action verb] [what this command does].

[If integrations involved: brief note about which systems are accessed.]

Steps:
1. **Discovery first:** Use Glob/Grep to check the current state before making changes. If the target already exists, report what you found and ask how to proceed.
2. Parse `$ARGUMENTS` for [expected input]. If missing, ask the user.
3. [Action step — be specific about what to do]
4. [Processing step — what to analyze, transform, or generate]
5. [Validation step — check against constraints if applicable]
6. **No hallucination:** If any expected file, path, or data point is not found during steps 3-5, report "Not Found" immediately. Do not guess or estimate.
7. Present results to the user in this format:

## [Output Title]

[Template for the output — tables, summaries, recommendations]

8. **Verification gate:** If this command wrote files or modified external systems, verify the operation succeeded (check file exists, validate structure, confirm API response).
9. Ask the user if they want to [next logical action — save, push, refine].

[If the command modifies external systems:]
**Permission gate:** Confirm with the user before making any changes to [system name]. For destructive actions (delete/overwrite) or 5+ simultaneous changes, always ask for explicit confirmation.
```

### Mapping Discovery → Command Content

| Discovery Field | Command Location |
|----------------|------------------|
| `key_functions` (action-oriented ones) | Command purpose and steps |
| `integrations` | allowed-tools list + step details |
| `constraints` | Validation step |
| `data_sources` | Where to pull from in action steps |
| `success_metrics` | Referenced in output format |

---

## README Template

```markdown
# [Plugin Name]

[discovery.plugin_purpose — expanded to one paragraph]

**Audience:** [discovery.user_profile]
[If dependencies: **Requires:** [dependency name and description]]

## Components

### Skills
- **[domain-skill-name]** — [description from skill frontmatter]
- **plugin-telemetry** — Automatic usage logging, version tagging, violation tracking, and feedback capture

[If commands exist:]
### Commands
- `/[command-name] [args]` — [description]

[If agents exist:]
### Agents
- **[agent-name]** — [description]

[If integrations exist:]
### Integrations
- **[Service Name]** — [what it connects to and why]

## Strategic Questions

When using this plugin, always consider:

[discovery.strategic_questions as numbered list]

## Boundaries

This plugin should NOT be used for:

[discovery.constraints + discovery.out_of_scope as bullet list]

## Success Metrics

| Metric | Data Source | How to Measure |
|--------|-----------|----------------|
[discovery.success_metrics mapped to discovery.data_sources]

## Installation

[For Olytic internal:]
```
claude plugin install [plugin-name]@olytic-marketplace
```

[For client:]
```
claude plugin install [plugin-name]
```

## Customization

- **Domain knowledge:** Edit `skills/[domain-skill]/SKILL.md`
- **Telemetry constraints:** Edit `skills/plugin-telemetry/SKILL.md` to update boundaries
- **Integrations:** Edit `.mcp.json` to add or change external connections
[Additional customization points based on components]
```

---

## Component Count Guidelines

| Plugin Complexity | Skills | Commands | Agents |
|-------------------|--------|----------|--------|
| Simple (1-2 functions) | 1 domain + telemetry | 0-1 | 0 |
| Medium (3-4 functions) | 1-2 domain + telemetry | 1-2 | 0-1 |
| Complex (5+ functions) | 2-3 domain + telemetry | 2-3 | 1-2 |

Start small. A plugin with one well-crafted skill is more useful than one with five half-baked components.
