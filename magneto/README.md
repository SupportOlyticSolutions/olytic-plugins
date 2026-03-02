# Magneto

Content creation and strategy plugin for Olytic Solutions. Handles website content production, LinkedIn posts, GEO optimization, GitHub integration, competitive research, GA4 analytics, and strategic content planning.

**Requires:** The One Ring governance plugin (for brand standards, company strategy, and competitive positioning).

---

## Components

### Skills

| Skill | Purpose |
|-------|---------|
| **magneto-website-content** | Website content creation: HTML templates, blog post and landing page structures, formatting rules, SEO guidance, content planning checklists. GTM-specific page types (O/G/O framework page, "Working With Us", GEO pages, assessment tool landing page). |
| **magneto-content-strategy** | Content strategy framework: GTM content funnel (TOFU/MOFU/BOFU), GEO strategy, LinkedIn strategy, content pillars, ICP journey mapping, prioritization framework, GA4 integration (Property ID: 525690219), Content O/G/O loop, production constraints. |
| **magneto-linkedin-content** | LinkedIn short-form post anatomy, hook formulas, body structures, CTA patterns, voice checklist, and post themes aligned to the Zero Case Study Playbook. |
| **magneto-geo-content** | GEO (AI Answer Engine Optimization) long-form page structure and strategy. Different requirements from blog posts — answer-first format, named concepts, structured excerptability, target queries. |
| **magneto-content-brief-standards** | Required pre-writing planning format. Defines all mandatory fields (funnel stage, ICP pain, thesis, differentiator, CTA, meta description) before drafting begins. |

### Commands

| Command | Purpose |
|---------|---------|
| `/pull-content [repo] [path]` | Fetch a page from any Olytic GitHub repo to review or edit |
| `/push-content [repo] [path]` | Push new or updated content to any Olytic GitHub repo (requires brand check — see hooks) |
| `/content-performance [page or "overview"]` | Analyze content performance using GA4 data, with strategic recommendations |
| `/content-brief [topic]` | Generate a complete structured content brief before drafting — funnel stage, ICP pain, thesis, headline options, meta description, CTA |
| `/linkedin-post [topic or URL]` | Draft 3 LinkedIn post options with distinct angles, full text, and recommended pick |
| `/geo-check [file or URL]` | Score existing content against 8 GEO criteria and produce prioritized revision recommendations |
| `/competitive-snapshot [topic]` | Research competitor content on a topic and surface the differentiation angle only Olytic can own |

### Agents

| Agent | Purpose |
|-------|---------|
| **content-strategist** | Recommends what to write next based on ICP needs, content gaps, competitive landscape, and GA4 performance data |
| **competitive-content-analyst** | Researches competitor content and messaging, finds positioning angles only Olytic can own |
| **meeting-notes-reviewer** | Extracts content ideas, ICP language, objections, and competitive intelligence from meeting notes and call transcripts |

### Hooks

| Hook | Trigger | Behavior |
|------|---------|----------|
| **Pre-push brand gate** | `PreToolUse` on push-content or GitHub write | Blocks content from being pushed to GitHub unless a brand check has been run this session |
| **Post-push content log** | `PostToolUse` on push-content or GitHub write | Logs the publication event (title, type, funnel stage, keyword, repo) to conversation context |
| **Post-performance gap check** | `PostToolUse` on content-performance | Surfaces strategic follow-up: conversion gaps, missing content, next investment priority |
| **LinkedIn skill prompt** | `UserPromptSubmit` on "linkedin", "post", "social", "feed" | Suggests `/linkedin-post` command if the user is drafting LinkedIn content |
| **Brief requirement prompt** | `UserPromptSubmit` on "brief", "plan content", "outline" | Suggests `/content-brief` command if the user is planning content without a brief |
| **GEO skill prompt** | `UserPromptSubmit` on "geo", "ai search", "citation", "perplexity" | Suggests `magneto-geo-content` skill if the user is about to write GEO content |

### Integrations

- **GitHub** — All repos under `SupportOlyticSolutions` org (olytic-site, olytic-lab, olytic-plugins, olytic-app, olytic-sandbox)
- **GA4** — Property ID 525690219 for content performance analysis
- **Ahrefs** — SEO data and GEO/Brand Radar monitoring (AI citation tracking across ChatGPT, Perplexity, etc.). Powers `/geo-check` with real citation data and feeds the content-strategist agent keyword signals. Requires Ahrefs account connection.
- **Windsor.ai** — Marketing data aggregator (325+ sources including GA4). Primary bridge for GA4 data until a native connector is available. Powers `/content-performance` with real analytics. Requires Windsor.ai account connection with GA4 linked.

---

## How It Works With The One Ring

This plugin assumes The One Ring is always installed. Here's how they interact:

| Need | Source |
|------|--------|
| Brand voice rules | The One Ring → `olytic-brand-standards` |
| Company strategy context | The One Ring → `olytic-company-strategy` |
| GTM strategy context | The One Ring → `olytic-company-strategy` (Zero Case Study Playbook section) |
| Competitive positioning | The One Ring → `brand-standards/references/competitive-landscape.md` |
| Brand compliance review | The One Ring → `brand-compliance-reviewer` agent or `/brand-check` command |
| Website content templates | This plugin → `magneto-website-content` |
| Content strategy framework | This plugin → `magneto-content-strategy` |
| LinkedIn post drafting | This plugin → `magneto-linkedin-content` + `/linkedin-post` command |
| GEO content creation | This plugin → `magneto-geo-content` + `/geo-check` command |
| Content planning | This plugin → `magneto-content-brief-standards` + `/content-brief` command |
| GitHub push/pull | This plugin → `/pull-content` and `/push-content` commands |
| GA4 analytics | This plugin → `/content-performance` command |

---

## Standard Workflows

**Create a new blog post or landing page:**
1. `/content-brief [topic]` — generate the brief, confirm the angle
2. Brand standards and website-content skills load automatically
3. Draft the content
4. `/brand-check` (from The One Ring) to verify
5. `/push-content olytic-site path/to/file.html` to publish

**Write a LinkedIn post:**
1. `/linkedin-post [topic or URL]` — generates 3 options with distinct angles
2. Pick one, refine if needed
3. Post manually on LinkedIn

**Create a GEO long-form page:**
1. Load `magneto-geo-content` skill for structural requirements
2. `/content-brief [target query]` to establish the brief
3. Draft with answer-first structure, named concepts, specific numbers throughout
4. `/geo-check` to score before publishing
5. `/brand-check` → `/push-content`

**Research a competitive angle before writing:**
1. `/competitive-snapshot [topic]` — surfaces what competitors say and Olytic's differentiation angle
2. Use the output to inform `/content-brief`

**Analyze and act on content performance:**
1. `/content-performance overview` — site-wide report with strategic recommendations
2. Or `/content-performance /blog/post-name` — page-specific analysis
3. Hook surfaces follow-up: gaps, CTA issues, next investment priority

**After meetings:**
Share notes to trigger the meeting-notes-reviewer agent.

---

## Customization

- **Templates:** Edit `skills/website-content/references/page-templates.md`
- **Content strategy framework:** Edit `skills/content-strategy/SKILL.md`
- **LinkedIn voice rules:** Edit `skills/linkedin-content/SKILL.md`
- **GEO structure rules:** Edit `skills/geo-content/SKILL.md`
- **Brief required fields:** Edit `skills/content-brief-standards/SKILL.md`
- **Hooks:** Edit `hooks/hooks.json`
- **GA4 property:** Update the property ID in `skills/content-strategy/SKILL.md` if it changes
- **Repo map:** Update the GitHub repo list in `skills/content-strategy/SKILL.md` if repos are added
