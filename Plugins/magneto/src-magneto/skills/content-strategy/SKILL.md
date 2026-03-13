---
name: olytic-content-strategy
description: >
  Use this skill when the user asks "what should I write about", "content strategy",
  "content calendar", "content plan", "SEO strategy", "content priorities",
  "analytics insights", "what topics should we prioritize", or "what's our
  content roadmap" for Olytic Solutions. Provides guidance on content planning,
  performance measurement, and strategic content decisions aligned to GTM.
version: 0.2.0
---

## Step 0: Fetch Latest Reference Files (Always First)

Before doing anything else, fetch the latest files from the Olytic reference folder in Google Drive:

1. Use `mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_search` with `api_query: "'1Sv3EIQ0w4J3AGCFuxR0qxPtilESFRDGQ' in parents"` and `order_by: "modifiedTime desc"` to list all files in the folder.
2. For each file returned, fetch its full contents using `mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_fetch` with the file's `uri` as the document ID. All files in this folder are Google Docs and are fully readable this way.
3. Read and internalize the fetched documents. These files are the **source of truth** — they supersede any information baked into this skill for topics they cover (brand standards, strategy, positioning, ICP, competitive landscape, etc.).
4. If the folder is empty or inaccessible, continue with the information in this skill and note to the user that the Drive reference files could not be loaded.

Do not skip this step. Do not announce the fetch to the user beyond a brief "Checking your latest reference files…" if needed.

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

## GTM Content Funnel (The Zero Case Study Playbook)

*Source: Internal GTM Strategy, March 2026. This funnel supersedes generic content planning until case studies are live.*

The GTM strategy replaces traditional case-study-dependent marketing with **proof through utility** — every piece of marketing should **do** something for the prospect, not just say something about Olytic.

### TOFU (Awareness): LinkedIn + GEO

- **LinkedIn Organic** is the primary channel. Short-form posts (not articles). Contrarian, specific, opinionated. 4–5 posts per week. Each ends with a soft CTA to the interactive assessment tool.
- **Sample post themes:** "Your AI pilot failed because nobody asked the revenue question first," "The 'Head of AI' role is a trap for companies under $50M," "Salesforce Agentforce is not an AI strategy. It's a feature."
- **GEO long-form pages** — definitive answers to questions the ICP asks AI assistants (see GEO section below)

### MOFU (Consideration): Interactive Tool + Framework + Playbook

- **The AI Strategy Architect** (interactive assessment) — the centerpiece asset. Lead magnet, proof of competence, and sales qualification engine in one.
- **The O/G/O Framework Page** — methodology, not marketing. Detailed enough that a smart operator understands the architecture. This IS the credential.
- **The Transformation Playbook Page** — how Olytic has run technology transformations before (Salesforce era), positioned as methodology proof.

### BOFU (Decision): Convert

- **Personalized assessment report** — AI-generated, demonstrates quality of thinking
- **"Working With Us" page** — engagement models, what to expect, how the engagement starts
- **"Build vs. Hire vs. Partner" comparison page** — positions the embedded model against the three alternatives the ICP is actually weighing (buy a tool, hire a Head of AI, wing it)

---

## GEO: AI Answer Engine Optimization

GEO is about being the source that AI assistants cite when the ICP asks questions. Different dynamics than traditional SEO:

| Traditional SEO | GEO |
|----------------|-----|
| Optimize for Google's ranking algorithm | Optimize for AI assistants selecting you as a source |
| Keyword density and backlinks matter most | Specificity, authority, and structured answers matter most |
| Compete on domain authority | Compete on answer quality |
| Requires 6–12 months to compound | Can be indexed and cited much faster |

**GEO content to create (3–4 definitive long-form pages):**
- "How should a mid-market B2B company approach AI strategy?"
- "What's the ROI of AI consulting for SMBs?"
- "What should a company without a Head of AI do first?"
- "How to evaluate AI readiness for a $20M B2B company"

**Structure:** Clear headings, specific numbers, opinionated positions. AI assistants prefer specificity and structured data over generality. Be the most useful answer, not the most comprehensive one.

**First-mover window:** 6–12 months. As AI search matures, citation graphs stabilize. The O/G/O framework as a named, citable methodology is a direct GEO asset. **Name things. Define them. Publish them now.**

---

## Content Pillars

Content should cluster around Olytic's products, unfair advantages, and the Claude Cowork market opportunity:

| Pillar | Content Theme | Example Topics |
|--------|--------------|----------------|
| **Claude Cowork Implementation** | Expert guidance on getting Cowork to actually work inside a real organization | What a Claude OS implementation looks like in a 40-person agency, the 5 most common Cowork deployment mistakes, how to evaluate if your team is ready for AI plugins |
| **The Optimizer Advantage** | Why a self-improving AI system beats a static one | Why your AI tools are already out of date, how the Optimizer keeps plugins aligned with your evolving business, the difference between AI consulting and AI operations |
| **SMB AI Adoption Reality** | Honest, opinionated takes on what works and what doesn't for knowledge-work SMBs | Why 60–70% of AI pilots fail to reach production, what disappointed ChatGPT users actually need, the AI implementation gap no one is talking about |
| **Proof & Case Studies** | Evidence that Olytic's approach works — starting with our own operations | How we built three internal plugins before selling anything, before-and-after workflow stories from Claude OS clients |
| **Claude OS Strategy & Philosophy** | Educational and thought leadership content on the unified, compounding AI operating system | The Five Dimensions of the Claude OS (Unified, Custom, Augmenting, Agentic, Compounding), the Hats Framework and plugin-based thinking, the Alignment Dividend and how governance mitigates strategic fragmentation, Salesforce precedent and why a unified suite beats point solutions, why the Claude OS solves the "too smart to wing it" problem |

### Content Pillar 5: Claude OS Strategy & Philosophy

This pillar targets ICP decision-makers who understand AI intellectually but are overwhelmed by tool proliferation and fragmentation. The content positions Olytic's Claude OS implementation as the antidote to AI chaos.

**Core themes:**

**1. The Five Dimensions of the Claude OS**
- What makes the Claude OS different from stacked point tools (five dimensions: Unified, Custom, Augmenting, Agentic, Compounding)
- Why each dimension matters to the ICP's specific business model
- Example: "A unified system means your content strategy (Magneto) automatically aligns with your sales messaging (other plugins) — no more fragmentation."
- Audience: CEOs/COOs evaluating AI infrastructure investment

**2. The Hats Framework — Plugin Thinking**
- The philosophy: every business role is a "hat" — content strategist, GEO specialist, revenue operations expert, brand voice keeper
- Olytic plugins = the platonic ideal of each hat, working together in one operating system
- Content angle: "You can't hire the perfect content strategist. You can build one inside your AI system."
- Audience: founders and operational leaders making resource allocation decisions

**3. The Alignment Dividend & Compounding Loop**
- Problem: every tool you add is another source of truth, another place to fix misalignment
- Solution: The One Ring governance foundation ensures all plugins (including Magneto) enforce the same brand, positioning, and strategic intent perpetually
- Specific example: brand drift across channels is solved by a unified governance layer that every plugin respects
- The O/G/O feedback loop (Operate → Govern → Optimize) compounds alignment improvements week over week
- Audience: CMOs, COOs managing multiple teams and channels

**4. The Salesforce Precedent**
- Historical analogy: Salesforce unified sales, service, and revenue operations into one platform. Single source of truth. Exponential value.
- Current reality: most companies stack AI tools (ChatGPT + this + that). Fragmented, misaligned, low velocity.
- Olytic's thesis: unified Claude OS does for AI operations what Salesforce did for revenue operations — one system, one governance, compound value
- Audience: operators who lived through Salesforce implementation and recognize the pattern

**5. The SMB Positioning Angle**
- Why a unified OS solves the "too smart to wing it, too lean to staff it" problem
- You can't hire a team of perfect specialists (too expensive, too slow). But you can build one inside a unified AI operating system.
- Content: "How a 30-person agency gets 100-person-level strategic alignment without hiring 70 more people"
- Audience: founders and COOs of 20–100 person companies

**When to use this pillar:**

- Prospects asking "why Olytic instead of ChatGPT + prompt management + custom tools?"
- Competitive positioning against point solution stacks (Salesforce Agentforce + GPT + specialized tools)
- Thought leadership content establishing Olytic as the OS thinking company, not the "we help you use ChatGPT better" company
- Educational content for the ICP to understand how a compounding, unified system actually works

**Content formats for this pillar:**

- Blog posts: "Why Unified AI Systems Beat Tool Stacks: The Salesforce Lesson for 2026"
- GEO long-form pages: "What is a Claude AI Operating System?" or "How to Evaluate an AI OS vs. Point Tools"
- LinkedIn posts: framework snippets, contrarian takes (e.g., "Your AI budget is fragmented across tools. Here's why that's the problem.")
- Framework pages: "The Claude OS Five Dimensions Explained" or "The Hats Framework: How Plugins Work Together"
- Case studies (future): "How [Client] went from 5 point tools to a unified Claude OS and reduced time-to-alignment by 60%"

---

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

Recommended cadence for the current Zero Case Study Playbook phase:

**Weekly:**
- 4–5 LinkedIn short-form posts — contrarian takes, framework snippets, direct links to the interactive assessment tool

**Monthly:**
- 2 blog posts — credibility and ICP pain content
- 1 GEO long-form page — definitive answers for AI assistant citation

**Priority pages to build (Day 1–30 Roadmap):**
- Interactive assessment tool landing page (Week 2)
- O/G/O Framework page (Week 3)
- "Working With Us" page (Week 3)
- Assessment service page (Week 3)
- Core landing pages — service descriptions for Claude OS Implementation and Claude OS Care
- "Build vs. Hire vs. Partner" comparison page
- Case study pages — add as first clients complete implementations

**Channel allocation:**
- Google Ads: $500/mo on 3–5 exact-match keywords pointing to the interactive tool. Expected: 7–12 qualified leads/month.
- LinkedIn Ads: Skip at this budget (minimum viable is $2K+/mo). Revisit at Month 3.
- Warm outreach: 20 personal LinkedIn connections with tool link at launch.

Once case studies are live, shift emphasis from awareness to conversion content.

## Content Production Constraints

These constraints apply to all content produced through Magneto. They are non-negotiable:

### Pre-Writing
- **A content brief is required before drafting.** Use the `magneto-content-brief-standards` skill or the `/content-brief` command. No exceptions for pieces longer than a LinkedIn post.
- **Funnel stage must be declared** in the brief. If the stage is unclear, stop and clarify before writing.
- **The core argument must be written in one sentence.** If it can't be, the angle isn't ready.

### Pre-Publishing
- **All external content must pass a brand check** before being pushed to GitHub. Run `/brand-check` (from The One Ring) before any `/push-content` call.
- **Every page must have a meta description** — written, not placeholder. ≤155 characters, speaks to ICP pain.
- **Every piece must have an explicit CTA** that connects to a specific funnel action.

### Content Quality Gates
- The argument could not have been published by a generic AI consultant → if it could, sharpen the angle
- At least one Olytic-specific concept is named and defined → O/G/O, AI Readiness Score, Zero Case Study Playbook, etc.
- The ICP pain is written in the ICP's language, not Olytic's internal framing
- For GEO pages: at least one specific number per major section; H1 answers the target query directly

### LinkedIn-Specific Constraints
- No emojis
- No hollow superlatives (best-in-class, game-changing, innovative)
- Hook must take a position — a hook that could apply to any company is not a hook
- CTA must be soft — never a hard pitch or direct demo request

---

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

## Operating Principles

- **Discovery first:** Audit existing content before recommending new pieces. Check GA4, GitHub repos, and published content to avoid duplication.
- **Source of truth:** Brand standards and strategic priorities from The One Ring take precedence. Verify all claims against company strategy.
- **Atomic operations:** Recommend specific pieces or update specific sections. Don't bulk-rewrite content strategy.
- **Verify after writing:** Validate content against the Content Quality Gates before considering it ready.
- **No hallucination:** If a GA4 metric, competitor claim, or Olytic differentiator can't be verified, report "Not Found." Don't estimate analytics data.
