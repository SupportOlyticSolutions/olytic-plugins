---
name: olytic-content-strategy
description: >
  This skill should be used when the user asks about "content strategy",
  "what should I write", "content calendar", "content plan", "SEO strategy",
  "content priorities", "analytics insights", or needs guidance on Olytic Solutions'
  approach to content planning, performance measurement, and strategic content decisions.
  Assumes The One Ring plugin is installed for brand and strategy context.
version: 0.1.0
---

# Content Strategy — Olytic Solutions

## Strategic Content Framework

All content serves one of three purposes (from company strategy):

1. **Build credibility** — demonstrate expertise that makes the ICP trust us before they've worked with us
2. **Create visibility** — get in front of the right people through content and search
3. **Enable conversion** — make it easy for a prospect to understand what we do and start a conversation

Every piece of content should map to at least one of these. If it doesn't, question whether it's worth creating.

## Content Pillars

Content should cluster around Olytic's three uniques:

| Pillar | Content Theme | Example Topics |
|--------|--------------|----------------|
| **Revenue Systems Expertise** | Deep technical knowledge of RevOps, Salesforce, CPQ, revenue architecture | Amendments in Salesforce CPQ, RevOps data model design, subscription management patterns |
| **The Olytic Model (O/G/O)** | How closed-loop AI architectures work in practice | Building an AI Governor for content quality, what "amplification not automation" looks like operationally, O/G/O case studies |
| **Strategic Value Creation** | Business strategy and AI strategy for GTM teams | Why your AI strategy needs a systems architect, the real cost of DIY AI for SMBs, how to evaluate AI readiness |

## ICP Content Journey

| Stage | What the ICP Is Thinking | Content Goal | Format |
|-------|-------------------------|--------------|--------|
| **Awareness** | "We need to do something with AI but don't know what" | Educate and build trust | Blog posts, thought leadership |
| **Consideration** | "We're evaluating approaches — build vs. buy vs. partner" | Differentiate Olytic from alternatives | Comparison content, case studies, methodology deep-dives |
| **Decision** | "We think Olytic might be the right fit" | Enable the conversation | Landing pages, service descriptions, assessment offers |

## Content Prioritization Framework

When recommending what to create next, score each topic:

| Factor | Weight | Question |
|--------|--------|----------|
| **ICP Pain** | High | Does this address a real pain the ICP has expressed? |
| **Differentiation** | High | Can only Olytic credibly write this? |
| **Search Potential** | Medium | Are people searching for this topic? |
| **Stage Coverage** | Medium | Does this fill a gap in our awareness → decision funnel? |
| **First Client Impact** | High | Does this directly help win our first client? |

## GA4 Analytics Integration

**GA4 Property ID:** 525690219

Use GA4 data to inform content decisions:

- **Which pages get traffic?** Double down on topics that resonate.
- **Which pages convert?** Understand what content drives action.
- **Where do visitors drop off?** Identify content gaps in the journey.
- **Search queries:** What terms bring people to the site? Create content that matches intent.
- **Engagement metrics:** Time on page, scroll depth — are people actually reading?

When analyzing GA4 data, always connect findings back to the three strategic purposes (credibility, visibility, conversion).

## Olytic Content Methodology

### The Content O/G/O Loop

Apply Olytic's own framework to content creation:

- **Operator:** Draft the content (using brand standards, templates, SEO guidance)
- **Governor:** Review against brand compliance, ICP alignment, competitive differentiation (use the brand-compliance-reviewer agent or `/brand-check` command from The One Ring)
- **Optimizer:** Analyze performance via GA4, identify what's working, feed insights back into the next content cycle

This isn't theoretical — it's literally how we should be producing content. Every piece should go through this loop.

### Content Cadence

*[PLACEHOLDER — Define target publishing cadence when ready]*

Recommended starting cadence for early-stage:
- 2 blog posts per month (expertise/credibility building)
- 1 landing page per month (conversion enablement)
- Ongoing optimization of existing pages based on GA4 data

## GitHub Repository Map

All repos under the `SupportOlyticSolutions` org:

| Repo | Purpose | Content Relevance |
|------|---------|-------------------|
| **olytic-site** | Main website | Primary target — blog posts, landing pages |
| **olytic-lab** | Lab / experimental | Technical demos, prototypes |
| **olytic-plugins** | Plugin development | Plugin documentation |
| **olytic-app** | Application | App documentation |
| **olytic-sandbox** | Sandbox / testing | Not for production content |

Default to `olytic-site` for website content unless otherwise specified.
