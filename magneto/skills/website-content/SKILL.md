---
name: olytic-website-content
description: >
  This skill should be used when the user asks to "create a webpage", "write HTML",
  "build a blog post page", "make a landing page", "draft website content",
  "create a page for the site", or needs to produce HTML website content for
  Olytic Solutions. Covers page structure, HTML patterns, content formatting,
  and templates for both blog posts and landing pages.
  Assumes The One Ring plugin is installed for brand standards.
version: 0.1.0
---

# Website Content Creation — Olytic Solutions

Use this skill when producing website content. Brand voice, ICP, and messaging rules come from The One Ring's `olytic-brand-standards` skill — load that too.

## Content Types

### Blog Posts / Articles

**Purpose:** Demonstrate expertise, attract ICP through search, build credibility toward winning our first client.

**Structure:**

- **Title:** Specific, practical, expert-level. Not clickbait. Pattern: "[Doing X] in [Context Y]" or "[Concept]: [Practical Subtitle]"
- **Subtitle:** One line clarifying what the reader gets
- **Table of Contents:** Required for posts with 4+ sections. Use anchor links.
- **Sections:** Clear H2 headers, each covering one distinct idea
- **Body format:** Bullet points, numbered lists, tables, bold terms. Minimize paragraph blocks. If a paragraph exceeds 3 sentences, break it up.
- **Scenarios/Examples:** Use structured formats (Description, Example, Approach, Solution, Consideration) when walking through use cases
- **CTA:** Subtle. "Call us" or "reach out" — not "SCHEDULE A DEMO NOW"

**Typical length:** 1,500–3,000 words.

### Landing Pages

**Purpose:** Convert ICP visitors into conversations.

**Structure:**

- **Hero section:** Clear headline + subtitle + single CTA. Headline states the outcome, not the service.
- **Problem section:** 3–4 bullet points describing the ICP's pain in their language
- **Solution section:** How Olytic addresses it — reference O/G/O, embedded model, or relevant unique
- **How it works:** 3-step or similar structured breakdown
- **Differentiation:** Quick comparison table or "Why Olytic" bullets
- **Social proof:** Client outcomes, metrics, or testimonials (when available)
- **CTA section:** Repeat primary CTA with brief reinforcing line

### GTM-Specific Page Types

The Zero Case Study Playbook introduces several priority page types beyond standard blog posts and landing pages:

**Interactive Assessment Tool Landing Page:**
- Hero: outcome-focused headline about getting a personalized AI strategy in 10 minutes
- Value proposition: what the prospect gets (AI Readiness Score, 3 prioritized opportunities, quick win they can start in 30 days)
- Social proof placeholder (completion count, average readiness score once data exists)
- Clear CTA to start the assessment
- Brief "what happens next" — the bridge to the paid AI Strategy Blueprint

**O/G/O Framework Page:**
- NOT a blog post — a framework page. Think "Design Thinking" by IDEO or Salesforce's V2MOM.
- Detailed enough that a smart operator can understand the architecture
- This IS the credential when there are no case studies
- Sections: the three layers (Operator, Governor, Optimizer), how the closed loop works, how it applies to their business, the philosophy ("amplification, not automation")

**"Working With Us" Page:**
- Engagement models: assessments vs. retainers, what to expect
- How the engagement starts — frictionless entry
- What the first 30 days look like
- Pricing transparency where appropriate

**"Build vs. Hire vs. Partner" Comparison Page:**
- Positions the embedded model against three alternatives the ICP actually weighs:
  - Buy a tool (Salesforce Agentforce, generic AI platforms) — tools without strategy are shelf-ware
  - Hire a "Head of AI" — $200K+ for a bet they can't de-risk
  - Wing it (ChatGPT + hope) — experiments that never become systems
- Use a structured comparison table
- End with Olytic's positioning: "embedded AI strategy partner for companies too smart to wing it and too lean to staff it"

**GEO Long-Form Pages (AI Answer Engine Optimization):**
- 3–4 definitive pages answering questions the ICP asks AI assistants
- Target queries: "How should a mid-market B2B company approach AI strategy?", "What's the ROI of AI consulting for SMBs?", "What should a company without a Head of AI do first?", "How to evaluate AI readiness for a $20M B2B company"
- Structure with clear headings, specific numbers, opinionated positions
- AI assistants prefer specificity and structured data over generality
- Be the most useful answer, not the most comprehensive one

**Transformation Playbook Page:**
- How Olytic has run technology transformations before (Salesforce era)
- Positioned as methodology proof: "Here's how we've done this motion before. Here's how we do it now."
- Bridges "transformation experience" to "AI expertise" — the objection neutralizer in page form

### General HTML Guidelines

- Clean, semantic HTML (`<article>`, `<section>`, `<header>`, `<nav>`)
- Structure with `<h1>` (page title), `<h2>` (sections), `<h3>` (subsections)
- Use `<ul>`, `<ol>` liberally — matches the brand voice
- Use `<table>` for comparisons and structured data
- Use `<strong>` for key terms (scannability)
- Include `<meta>` description optimized for ICP search intent
- Add `alt` attributes to all images
- Keep inline styles minimal — use class names for the site's CSS framework

## Content Planning Checklist

Before writing any page, confirm:

1. **What type of page?** Blog post or landing page?
2. **Who is the audience?** ICP persona, awareness stage, specific pain point
3. **What's the one thing?** Single core message or takeaway
4. **What's the CTA?** What should the reader do next?
5. **Which Olytic uniques apply?** Revenue systems expertise / O/G/O model / Strategic value creation
6. **Competitive context?** Is this addressing a space where competitors exist?
7. **Does this help win our first client?** If not directly, does it build toward that?

## SEO Guidance

- Target long-tail keywords: "AI for revenue operations," "go-to-market AI architecture," "RevOps AI strategy for SMBs"
- Use the target keyword naturally in H1, first paragraph, and at least one H2
- Write meta descriptions that speak to ICP pain
- Internal link to other Olytic content where relevant
- Don't keyword-stuff — the expert voice naturally incorporates relevant terms

## Templates

For HTML page templates, see `references/page-templates.md`.
