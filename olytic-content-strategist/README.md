# Olytic Content Strategist

Content creation and strategy plugin for Olytic Solutions. Handles website content production, GitHub integration, competitive research, GA4 analytics, and strategic content planning.

**Requires:** The One Ring governance plugin (for brand standards, company strategy, and competitive positioning).

## Components

### Skills

- **olytic-website-content** — Website content creation: HTML templates, blog post and landing page structures, formatting rules, SEO guidance, content planning checklists.
- **olytic-content-strategy** — Content strategy framework: content pillars, ICP journey mapping, prioritization framework, GA4 integration (Property ID: 525690219), Content O/G/O loop methodology.

### Commands

- `/pull-content [repo] [path]` — Fetch a page from any Olytic GitHub repo to review or edit
- `/push-content [repo] [path]` — Push new or updated content to any Olytic GitHub repo
- `/content-performance [page or "overview"]` — Analyze content performance using GA4 data

### Agents

- **content-strategist** — Recommends what to write next based on ICP needs, content gaps, competitive landscape, and GA4 performance data
- **competitive-content-analyst** — Researches competitor content and messaging, finds positioning angles only Olytic can own
- **meeting-notes-reviewer** — Extracts content ideas, ICP language, objections, and competitive intelligence from meeting notes and call transcripts

### Integrations

- **GitHub** — All repos under `SupportOlyticSolutions` org (olytic-site, olytic-lab, olytic-plugins, olytic-app, olytic-sandbox)
- **GA4** — Property ID 525690219 for content performance analysis

## How It Works With The One Ring

This plugin assumes The One Ring is always installed. Here's how they interact:

| Need | Source |
|------|--------|
| Brand voice rules | The One Ring → `olytic-brand-standards` |
| Company strategy context | The One Ring → `olytic-company-strategy` |
| Competitive positioning | The One Ring → `brand-standards/references/competitive-landscape.md` |
| Brand compliance review | The One Ring → `brand-compliance-reviewer` agent or `/brand-check` command |
| Website content templates | This plugin → `olytic-website-content` |
| Content strategy framework | This plugin → `olytic-content-strategy` |
| GitHub push/pull | This plugin → `/pull-content` and `/push-content` commands |
| GA4 analytics | This plugin → `/content-performance` command |

## Usage

**Create new content:**
1. Describe what you want (blog post, landing page, etc.)
2. Brand standards load automatically from The One Ring
3. Website content skill loads for templates and structure
4. Draft the content, then use `/brand-check` (from The One Ring) to verify
5. `/push-content olytic-site path/to/file.html` to publish

**Plan content:**
Ask "what should I write about next?" to trigger the content-strategist agent.

**Analyze performance:**
`/content-performance overview` for a site-wide report, or `/content-performance /blog/post-name` for a specific page.

**After meetings:**
Share notes to trigger the meeting-notes-reviewer agent.

## Customization

- **Templates:** Edit `skills/website-content/references/page-templates.md`
- **Strategy framework:** Edit `skills/content-strategy/SKILL.md`
- **GA4 property:** Update the property ID in `skills/content-strategy/SKILL.md` if it changes
- **Repo map:** Update the GitHub repo list in `skills/content-strategy/SKILL.md` if repos are added
