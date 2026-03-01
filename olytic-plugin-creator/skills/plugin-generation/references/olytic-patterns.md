# Olytic Plugin Patterns

Hard-coded standards that every Olytic-generated plugin must follow. These are non-negotiable.

## Naming Conventions

| Component | Pattern | Examples |
|-----------|---------|----------|
| Plugin name | `[domain]-[scope]` or `[product]-[function]` | `customer-success-tracker`, `proposal-builder`, `deal-qualifier` |
| Skill directory | `[domain]-[function]` | `proposal-standards`, `deal-qualification`, `customer-metrics` |
| Command file | `[verb]-[object].md` | `pull-metrics.md`, `score-health.md`, `review-proposal.md` |
| Agent file | `[role]-[responsibility].md` | `deal-analyst.md`, `proposal-reviewer.md`, `metrics-reporter.md` |
| Reference files | Descriptive, kebab-case | `scoring-formula.md`, `industry-benchmarks.md`, `template-library.md` |

**Rules:**
- All names are kebab-case (lowercase, hyphens, no spaces)
- Plugin names: 2-4 words maximum
- Command names start with a verb
- Agent names describe a role
- No abbreviations unless universally understood (e.g., "api" is fine, "cst" is not)

## Author Information

**Olytic internal plugins:**
```json
"author": {
  "name": "Olytic Solutions",
  "email": "support@olyticsolutions.com"
}
```

**Client plugins:**
```json
"author": {
  "name": "[Client Company Name]",
  "email": "[client contact email]"
}
```

## plugin.json Valid Keys

The only recognized keys in `plugin.json` are: `name`, `version`, `description`, `author`, `keywords`, `hooks`.

**`displayName` is NOT a valid key** — it will cause a validation failure on upload. Do not include it.

## Skill Writing Standards

### Frontmatter Description

Must include 4-6 specific trigger phrases using the user's natural language:

```yaml
description: >
  This skill should be used when the user asks to "[phrase 1]", "[phrase 2]",
  "[phrase 3]", "[phrase 4]", or needs [general context].
  [Dependency note if applicable.]
```

**Good:** `"write a proposal", "draft a client pitch", "create a scope document"`
**Bad:** `"handle proposal-related tasks"` (too vague, won't trigger)

### Body Structure

1. **H1 title** — descriptive name
2. **Context paragraph** — what this skill covers and when to use it
3. **Strategic Questions section** (from discovery Q3) — "Before You Start" or "Decision Framework"
4. **Main content** — organized with H2 sections, bullets, tables, bold key terms
5. **Boundaries section** (from discovery Q4) — "Out of Scope" or "Constraints"
6. **Reference links** — point to `references/` files for detailed material
7. **Telemetry note** — "Telemetry: This skill logs all invocations via plugin-telemetry"

### Voice (Olytic Internal Only)

- Expert, opinionated, structured, practical
- Use "we" to position as teammate
- Bold key terms for scannability
- Favor bullets and tables over paragraphs
- Short punchy sentences mixed with longer explanatory ones
- No fluffy language, no hollow superlatives
- Dry humor where natural — never forced

### Voice (Client Plugins)

- Match the client's brand voice if documented
- Default to clear, professional, structured if no brand guide exists
- Always practical and actionable

## Agent Writing Standards

### Frontmatter Structure

> ⚠️ **YAML structure rule:** The YAML frontmatter (between the `---` delimiters) must contain ONLY valid YAML key-value pairs: `name`, `description`, `model`, `color`, `tools`. The `<example>` blocks are NOT valid YAML — they must be placed AFTER the closing `---`, never inside it. Putting examples inside the frontmatter causes a YAML parse failure and breaks plugin upload.

> ⚠️ **Description colon rule:** If the `description` value contains a colon followed by a space (e.g., `"facets: brand voice"` or `"options: A, B"`), YAML treats it as a key-value separator and fails to parse. Always use the block scalar `description: >` format for agent descriptions — this makes any colons in the text safe.

```yaml
---
name: [role]-[responsibility]
description: >
  Use this agent when the user asks to "[phrase]", "[phrase]", or [context].
  Any colons in the description are safe because of the block scalar format.
model: inherit
color: [color]
tools: ["Tool1", "Tool2"]
---

<example>
Context: [Scenario]
user: "[Example message]"
assistant: "[Expected response]"
<commentary>
[Why this agent is appropriate]
</commentary>
</example>

<example>
Context: [Different scenario]
user: "[Example message]"
assistant: "[Expected response]"
<commentary>
[Why this agent is appropriate]
</commentary>
</example>
```

### Color Assignment

| Domain | Color |
|--------|-------|
| Governance / compliance | yellow |
| Strategy / planning | magenta |
| Research / analysis | cyan |
| Extraction / review | green |
| Creation / generation | orange |

No two agents in the same plugin share a color.

### Body Structure

1. Role description — "You are [organization]'s [role]."
2. Core Responsibilities — 3-6 bullet points
3. Process — numbered steps for how the agent works
4. Output Format — exact template (tables, sections, headers)
5. Context — current business state or priorities if relevant

## Command Writing Standards

### Frontmatter Structure

```yaml
---
description: [One-line action description]
argument-hint: [example with explanation]
allowed-tools: ["tool1", "tool2"]
---
```

### Body Structure

- Numbered steps (instructions for Claude, not docs for the user)
- Include confirmation steps before destructive or external actions
- Reference MCP tools by full name: `mcp__github__get_file_contents`
- Include error handling guidance

## Dependency Declaration

### Internal Olytic Plugins

If the plugin depends on The One Ring (most internal plugins do):
- Note in plugin.json description: "Requires The One Ring governance plugin."
- Note in README: "**Requires:** The One Ring governance plugin"
- In skills that need brand standards, add: "Brand voice, ICP, and messaging rules come from The One Ring's `olytic-brand-standards` skill — load that too."

### Client Plugins

Client plugins are typically standalone. If they depend on a governance plugin built for that client, note it the same way.

## Required Components (Every Plugin)

1. `.claude-plugin/plugin.json` — always
2. `skills/plugin-telemetry/SKILL.md` — always (from telemetry template)
3. At least one domain skill — always
4. `README.md` — always
5. `.mcp.json` — only if integrations exist
6. `commands/` — only if repeatable actions exist
7. `agents/` — only if multi-step workflows exist
