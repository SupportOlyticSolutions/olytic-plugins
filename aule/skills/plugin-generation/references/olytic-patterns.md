# Aulë Plugin Patterns

Hard-coded standards that every Aulë-generated plugin must follow. These are non-negotiable.

---

## Olytic Business Context

When generating **Olytic-internal plugins** (audience: `olytic-internal`), ground all content in Olytic's current business reality. This context informs how skills, agents, and commands are framed, what ICP they reference, and what strategic questions they embed.

*Last updated: March 2026 — reflects the Complete Business Plan.*

### What Olytic Does

Olytic Solutions is an **AI implementation and optimization platform** — a Claude Cowork implementation and managed service specialist. The two products are:

- **Claude OS Implementation** — fixed-fee (6–8 week) engagement that installs a functioning AI operating system inside a client's organization. Pricing: $15K standard / $25K complex / $10K case study rate (first 3 clients).
- **Claude OS Care** — 12-month managed service retainer ($2,000–$2,500/mo) that keeps the client's AI OS current and improving, powered by the Optimizer.

The **Optimizer** is Olytic's proprietary technology: a weekly AI agent that pulls client analytics, CRM data, and competitive intelligence, then surfaces plugin update recommendations and content briefs automatically. This is the defensible moat — a freelance AI consultant can't replicate it.

Long-term, Olytic accumulates a **cross-client behavioral dataset** (how SMBs adopt AI tools) that becomes a standalone data intelligence product sold to PE firms, agencies, and MarTech platforms.

### Current Business Stage

Pre-launch, targeting first implementation clients July 2026. Goals in priority order:
1. Win 3 case study clients at $10K to prove the model
2. Convert implementations to Claude OS Care managed retainers (target: 60% conversion)
3. Reach 15 managed clients (Threshold 1, ~late 2028) — benchmark data unlocks at this point
4. Reach 30 managed clients → launch 'State of SMB AI Adoption' annual report
5. Reach 50 managed clients → full data licensing (~$245K/yr near-pure-margin revenue)

5-year total revenue target: $6.8M across 144 implementation clients and 66 managed clients at Y5.

### Olytic's ICP

When a plugin is for client-facing work or serves the sales/marketing function, this is who we're targeting:

- **Company size:** 20–100 employees
- **Industries:** Marketing/PR agencies, consulting firms, recruiting, financial advisory, specialty e-commerce
- **Mindset:** Disappointed AI early adopter — tried ChatGPT, got nothing, still believes in AI but frustrated
- **Decision-maker:** Founder or COO who can say yes over lunch
- **Content/ops profile:** Knowledge-work heavy — lots of content, client deliverables, or repeatable internal processes

We are **avoiding** enterprises (>200 employees) in this phase due to procurement cycles.

### Olytic's Unfair Advantages (Reference in Plugin Content Where Relevant)

- **We've done it ourselves first** — built three internal Claude plugins before selling anything
- **The Optimizer** — proprietary weekly AI agent; not replicable by freelance consultants
- **Compounding data asset** — cross-client behavioral data built as a byproduct of managed service; zero marginal cost to collect
- **Consulting DNA** — strategy, discovery, change management skills most AI vendors lack

### Strategic Questions for Olytic-Internal Plugins (Q3 Reference)

When building plugins for Olytic's internal operations (proposals, delivery, sales, content), these are the right strategic questions to embed:

*Proposal / sales:*
- "Is this prospect a realistic ICP fit (20–100 employees, knowledge-work heavy, founder or COO as DM)?"
- "Are we leading with the proof that we've done it ourselves — before pitching the methodology?"
- "Are we positioning against freelance AI consultants and generic tools, not against each other?"
- "Is this a case study candidate? Should we offer the $10K rate to build proof?"

*Client delivery:*
- "Does the client understand what they're getting and what they need to maintain?"
- "Is the Optimizer set up to run on this client's data?"
- "Are we capturing client_id and plugin_type tags from day one for the data asset?"
- "Does this align with the SOW and the agreed plugin architecture?"

*Content / marketing:*
- "Does this build credibility, visibility, or conversion — and which one do we need most right now?"
- "Does this capitalize on the Claude Cowork market window (open now, won't stay open long)?"
- "Would a generic AI consultant say the same thing? If yes, rewrite it."
- "Does this speak to a disappointed AI adopter's actual pain — not a theoretical AI skeptic?"

---

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

**Aulë internal plugins:**
```json
"author": {
  "name": "Aulë Solutions",
  "email": "support@aulesolutions.com"
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

### Voice (Aulë Internal Only)

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

> ⚠️ **argument-hint quoting rule:** If the `argument-hint` value contains `[...]` (square brackets), it MUST be wrapped in quotes. Without quotes, YAML parses `[...]` as a flow sequence (array literal), not a string — causing "invalid YAML frontmatter" upload errors. Use double quotes for standard values: `argument-hint: "[repo-name] (e.g., olytic-site)"`. If the value itself contains double quotes, use single-quote wrapping: `argument-hint: '[page-path or "overview"]'`.

```yaml
---
description: [One-line action description]
argument-hint: "[example with explanation]"
allowed-tools: ["tool1", "tool2"]
---
```

### Body Structure

- Numbered steps (instructions for Claude, not docs for the user)
- Include confirmation steps before destructive or external actions
- Reference MCP tools by full name: `mcp__github__get_file_contents`
- Include error handling guidance

## Dependency Declaration

### Internal Aulë Plugins

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

## Permissions Manifest (Every Plugin)

Every generated plugin's README must include a Permissions Manifest section that declares:

| Declaration | Description |
|------------|-------------|
| **Tools accessed** | Which MCP tools and local tools the plugin uses (e.g., "GitHub API via mcp__github, Google Analytics via mcp__ga4") |
| **Data read** | What data the plugin reads (e.g., "marketplace.json, GA4 analytics, user-uploaded documents") |
| **Data written** | What data the plugin creates or modifies (e.g., "plugin files, marketplace entries, telemetry logs") |
| **External services** | Which external systems are called (e.g., "GitHub API, Google Analytics API") |
| **Human-in-the-loop checkpoints** | Which actions require user confirmation before execution (e.g., "publishing content, modifying external systems, deleting files") |

This manifest serves as a transparency and governance tool. It allows users and administrators to understand exactly what a plugin can do before installing it.

## Memory Scope Declaration (Every Plugin)

Every generated plugin's README must include a Memory Scope section that declares:

- **Scope type:** ephemeral (session-only), persistent (retained between sessions), or retrieval (searches large knowledge bases)
- **What is retained:** specific data or context the plugin stores
- **Retention period:** how long data is kept (if persistent)
- **Data lifecycle:** when and how stored data is purged
- **Justification:** why persistent or retrieval memory is needed (if applicable)

Default is ephemeral. Persistent memory requires explicit justification during discovery.

## Integrity Controls

### Prompt Injection Defenses

Plugins that process external content (user uploads, web data, third-party API responses) must include:
- **Input validation:** Verify that external content matches expected formats before processing
- **Instruction boundary:** Clear separation between trusted plugin instructions and untrusted external data
- **Output filtering:** Validate that outputs don't contain injected instructions or unexpected behaviors

### Human-in-the-Loop Checkpoints

For high-stakes domains (finance, legal, HR, security), generated plugins should include configurable human confirmation steps:
- Before publishing or sending content externally
- Before modifying external systems (databases, APIs, repositories)
- Before actions that cannot be easily reversed
- The checkpoint mechanism should be configurable: users can enable/disable specific checkpoints based on their risk tolerance

## Composability Convention

Plugins should be designed as composable building blocks that can work together:
- Skills should be loadable independently — no implicit dependencies between skills in the same plugin
- Agents should be able to reference skills from other installed plugins using standard patterns
- Commands should produce outputs in formats that other plugins can consume
- The README should note which other plugins this one works well with (if applicable)

## Augmentation Framing

Plugin descriptions and README content should emphasize what new capabilities the plugin creates, not just what tasks it speeds up:

**Good:** "Enables content teams to maintain brand consistency across all channels simultaneously — something that previously required manual review of each piece."
**Bad:** "Automates brand compliance checking."

**Good:** "Gives junior sales reps access to senior-level deal preparation by synthesizing insights from past successful proposals."
**Bad:** "Speeds up proposal writing."

This framing is informed by the augmentation test in discovery Q6. If the augmentation signal was weak, the README should acknowledge this and suggest potential augmentation opportunities.
