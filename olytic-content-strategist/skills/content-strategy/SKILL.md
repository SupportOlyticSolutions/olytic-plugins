---
name: olytic-content-strategy
description: >
  This skill should be used when the user asks about "content strategy",
  "what should I write", "content calendar", "content plan", "SEO strategy",
  "content priorities", "analytics insights", or needs guidance on Olytic Solutions'
  approach to content planning, performance measurement, and strategic content decisions.
  Assumes The One Ring plugin is installed for brand and strategy context.
version: 0.2.0
---

# Content Strategy — Olytic Solutions

*Last updated: March 2026 — reflects the Complete Business Plan.*

## Strategic Content Framework

All content serves one of three purposes:

1. **Build credibility** — demonstrate expertise that makes the ICP trust us before they've worked with us
2. **Create visibility** — get in front of the right people through content and search
3. **Enable conversion** — make it easy for a prospect to understand what we do and start a conversation

Every piece of content should map to at least one of these. If it doesn't, question whether it's worth creating.

**Current phase context:** Olytic is targeting first implementation clients starting July 2026, building proof-of-concept case studies. Content right now must either win case study clients or establish Olytic as the recognized Cowork implementation specialist.

## Content Pillars

Content should cluster around Olytic's products, unfair advantages, and the Claude Cowork market opportunity:

| Pillar | Content Theme | Example Topics |
|--------|--------------|----------------|
| **Claude Cowork Implementation** | Expert guidance on getting Cowork to actually work inside a real organization | What a Claude OS implementation looks like in a 40-person agency, the 5 most common Cowork deployment mistakes, how to evaluate if your team is ready for AI plugins |
| **The Optimizer Advantage** | Why a self-improving AI system beats a static one | Why your AI tools are already out of date, how the Optimizer keeps plugins aligned with your evolving business, the difference between AI consulting and AI operations |
| **SMB AI Adoption Reality** | Honest, opinionated takes on what works and what doesn't for knowledge-work SMBs | Why 60–70% of AI pilots fail to reach production, what disappointed ChatGPT users actually need, the AI implementation gap no one is talking about |
| **Proof & Case Studies** | Evidence that Olytic's approach works — starting with our own operations | How we built three internal plugins before selling anything, before-and-after workflow stories from Claude OS clients |

## ICP Content Journey

The ICP is a 20–100 person company in marketing/PR, consulting, recruiting, or financial advisory. The decision-maker is a founder or COO. They tried AI (probably ChatGPT), got nothing sticky, and still believe AI should work — they're just frustrated it hasn't yet.

| Stage | What the ICP Is Thinking | Content Goal | Format |
|-------|-------------------------|--------------|--------|
| **Awareness** | "We tried ChatGPT, it didn't stick. Maybe we're doing it wrong." | Name the frustration. Position Olytic as the people who understand why it failed. | Blog posts, thought leadership on AI pilot failure |
| **Consideration** | "We need someone to actually implement this, not just advise us." | Differentiate between implementation (us) and consulting (everyone else). Show the case study rate as a low-risk entry. | Comparison content, methodology deep-dives, implementation process overview |
| **Decision** | "This looks like it could work. What's the first step?" | Make it frictionless to start a conversation. Surface the $10K case study offer prominently. | Landing pages, service descriptions, direct CTAs to book a call |

## Content Prioritization Framework

When recommending what to create next, score each topic against these factors:

| Factor | Weight | Question |
|--------|--------|----------|
| **Case Study Client Impact** | Very High | Does this directly help us win one of the first 3 case study clients? |
| **ICP Pain Match** | High | Does this address the specific pain of a 20–100 person knowledge-work company that tried AI and got burned? |
| **Differentiation** | High | Can only Olytic credibly write this? Would a generic AI consultant say the same thing? |
| **Cowork Timing** | High | Does this capitalize on the Claude Cowork launch (Feb 24, 2026)? The window is open now. |
| **Search Potential** | Medium | Are people searching for this topic? What's the organic traffic opportunity? |
| **Stage Coverage** | Medium | Does this fill a gap in our awareness → decision funnel? |

**High-priority content right now:**
- Anything that explains the Cowork implementation gap and positions Olytic as the specialist
- Content targeting "disappointed AI adopters" — marketers and agency founders who tried ChatGPT and got generic outputs
- Case study content once first clients are live

## Competitive Content Angles

Content that positions Olytic against the competitive field:

- **vs. freelance AI consultants:** They advise, we operate. Our Optimizer keeps improving the system every week automatically.
- **vs. generic AI tools:** Tools don't get smarter. Olytic builds systems that do.
- **vs. doing it internally:** You can build one plugin. We build three, tune them weekly, and tell you what your competitors are doing.
- **vs. waiting:** Being a Cowork implementation specialist in 2026 is the equivalent of being a Salesforce partner in 2005. The window is open right now.

## GA4 Analytics Integration

**GA4 Property ID:** 525690219

Use GA4 data to inform content decisions:

- **Which pages get traffic?** Double down on topics that resonate.
- **Which pages convert?** Understand what content drives action.
- **Where do visitors drop off?** Identify content gaps in the journey.
- **Search queries:** What terms bring people to the site? Create content that matches intent.
- **Engagement metrics:** Time on page, scroll depth — are people actually reading?

When analyzing GA4 data, always connect findings back to the three strategic purposes (credibility, visibility, conversion). In this phase, conversion is the top priority.

## Olytic Content Methodology

### The Content O/G/O Loop

Apply Olytic's own framework to content creation:

- **Operator:** Draft the content (using brand standards, templates, SEO guidance)
- **Governor:** Review against brand compliance, ICP alignment, competitive differentiation (use the brand-compliance-reviewer agent or `/brand-check` command from The One Ring)
- **Optimizer:** Analyze performance via GA4, identify what's working, feed insights back into the next content cycle

This isn't theoretical — it's literally how we produce content. Every piece should go through this loop.

### Content Cadence

Recommended starting cadence for the current pre-launch phase (through July 2026):
- 2 blog posts per month — credibility and ICP pain content targeting the Cowork adoption wave
- Core landing pages — service descriptions for Claude OS Implementation and Claude OS Care
- Case study pages — add as first clients complete implementations

Once case studies are live, shift emphasis from awareness to conversion content.

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
