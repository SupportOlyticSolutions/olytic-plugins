---
name: olytic-website-content
description: >
  Use this skill to "create a webpage", "write HTML", "build a blog post page",
  "make a landing page", "draft website content", "create a page for the site",
  "write the copy for our homepage", or "build out a service page" for Olytic
  Solutions. Provides page structures, HTML patterns, content formatting rules,
  and templates for blog posts, landing pages, and GTM-specific page types.
  Assumes The One Ring plugin is installed for brand standards.
version: 0.1.0
---

## Step 0: Fetch Latest Reference Files (Always First)

Before doing anything else, fetch the latest files from the Olytic reference folder in Google Drive:

1. Use `mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_search` with `api_query: "'1Sv3EIQ0w4J3AGCFuxR0qxPtilESFRDGQ' in parents"` and `order_by: "modifiedTime desc"` to list all files in the folder.
2. For each file returned, fetch its full contents using `mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_fetch` with the file's `uri` as the document ID. All files in this folder are Google Docs and are fully readable this way.
3. Read and internalize the fetched documents. These files are the **source of truth** — they supersede any information baked into this skill for topics they cover (brand standards, strategy, positioning, ICP, competitive landscape, etc.).
4. If the folder is empty or inaccessible, continue with the information in this skill and note to the user that the Drive reference files could not be loaded.

Do not skip this step. Do not announce the fetch to the user beyond a brief "Checking your latest reference files…" if needed.

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

## Boutique Authority Principles

Every page Magneto produces for Olytic must embody the design discipline that separates expert boutiques from template sites. These principles were derived from studying firms like Thoughtbot, Animalz, Viget, and Barrel — small teams whose websites make them appear 10x their size.

### Visual Language: Authority Through Restraint

- **Color as system:** Use Olytic's palette with military consistency. Every button, heading, hover state, and accent follows the same logic. Inconsistency signals chaos; consistency signals "we have our act together."
- **Whitespace as confidence:** Leave 40–60% of the viewport empty at any scroll position. Resist the instinct to fill every pixel with proof. Whitespace says "we can afford to show you only what matters."
- **No stock photography. Ever.** Use screenshots of real work, custom illustrations, data visualizations, or nothing at all. Every image must earn its place by communicating something specific about Olytic's taste, clients, or process. Typography-forward pages with no imagery beat cluttered pages with generic photos every time.
- **Typography as brand:** Use distinctive heading treatments. A carefully chosen headline typeface immediately signals that someone with design sensibility made deliberate choices — exactly what a technology-enabled services firm needs to convey.

### Productization: Making the Abstract Tangible

- **Name every offering.** Don't sell "consulting" — sell the "AI Strategy Blueprint," the "Revenue System Audit," the "O/G/O Implementation." Naming a service does three things: makes the buyer feel they're purchasing a proven product; gives them vocabulary to justify the purchase internally; and allows Olytic to standardize delivery and protect margins.
- **Tier or categorize.** Use frameworks like "Assess / Design / Build / Optimize" so visitors self-select into the right conversation. Reduce cognitive load and pre-qualify leads before any human interaction.
- **List deliverables, not descriptions.** The best service pages read like a statement of work preview. Tell the reader what artifacts they'll receive, what happens in each phase, and what the timeline looks like. Specificity de-risks the purchase.
- **Signal pricing without stating it.** Use words like "select clients," engagement structures implying multi-month commitments, or scoping language that filters budget-mismatched leads before they reach the form.

### Trust Signals: Proving Expertise Without Bragging

- **Case studies as editorial content.** Write them so they're interesting to read even for someone not shopping for a vendor. Include the problem context, constraints, decision points, tradeoffs, and outcomes with actual metrics.
- **Process transparency.** Document methodology in public. Olytic's O/G/O framework page is the exemplar: a firm confident enough to publish its process signals that the value isn't in the playbook — it's in the execution.
- **Demonstrate, don't claim.** Blog posts and pages should demonstrate the same quality of thinking clients pay for. Content IS the proof. This is the most powerful trust signal available to a boutique firm because it cannot be faked with budget.
- **Named humans, not anonymous teams.** Feature real people with real names and roles. Boutique firms sell access to senior talent — buyers want to see who they'll actually work with.
- **Community contribution signals.** Open-source work, published frameworks, and public thinking are trust signals that large competitors cannot replicate because they require genuine expertise and generosity.

### User Journey: Self-Education to Qualified Lead

- **Homepage as router, not salesperson.** The homepage establishes identity ("we are X, we do Y for Z") and routes visitors to intent-matched content. Keep it to 3–5 scroll sections, decisive and link-heavy. Don't try to sell anything on the homepage.
- **Invest in self-education content.** Every piece of content should help the visitor become a more informed buyer — before asking for anything. Blog posts, methodology pages, and deep case studies all serve this purpose.
- **Service pages as pre-qualification.** Productized service pages are the middle layer between interest and a sales conversation. Visitors should be able to determine relevance without talking to a human. By the time someone fills out a form, they already know what they want.
- **Low-friction, high-signal contact.** No aggressive pop-ups, no chatbots-on-arrival, no "SCHEDULE A DEMO" on every page. A simple form at the bottom of service and work pages with one or two qualifying questions ("Tell us about your situation"). The message: "We're here when you're ready."
- **Never gate content.** No "download our whitepaper" bait. No mandatory newsletter signup before reading. The content IS the marketing — restricting access undermines the entire strategy.

## Content Planning Checklist

Before writing any page, confirm:

1. **What type of page?** Blog post, landing page, or service page?
2. **Who is the audience?** ICP persona, awareness stage, specific pain point
3. **What's the one thing?** Single core message or takeaway
4. **What's the CTA?** What should the reader do next?
5. **Which Olytic uniques apply?** Revenue systems expertise / O/G/O model / Strategic value creation
6. **Competitive context?** Is this addressing a space where competitors exist?
7. **Does this help win our first client?** If not directly, does it build toward that?
8. **Does this page embody boutique authority?** Typography-forward, generous whitespace, no stock photos, named offerings with deliverables, and zero high-pressure CTAs.

## SEO Guidance

- Target long-tail keywords: "AI for revenue operations," "go-to-market AI architecture," "RevOps AI strategy for SMBs"
- Use the target keyword naturally in H1, first paragraph, and at least one H2
- Write meta descriptions that speak to ICP pain
- Internal link to other Olytic content where relevant
- Don't keyword-stuff — the expert voice naturally incorporates relevant terms

## Templates

For HTML page templates, see `references/page-templates.md`.

## Operating Principles

- **Discovery first:** Before creating a page, assess what already exists. Check GitHub repos and existing content to avoid duplication.
- **Source of truth:** Brand standards from The One Ring take precedence. If there's a conflict, verify against The One Ring's `olytic-brand-standards` skill.
- **Atomic operations:** Make targeted edits to existing pages. Don't rewrite entire sites unless explicitly requested.
- **Verify after writing:** After creating or updating HTML, validate the structure and proofread for ICP alignment.
- **No hallucination:** If a page path, template reference, or brand guideline doesn't exist, report "Not Found." Never guess URLs or template names.
