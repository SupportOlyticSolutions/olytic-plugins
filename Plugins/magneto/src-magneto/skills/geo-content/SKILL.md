---
name: magneto-geo-content
description: >
  Use this skill to "write a GEO page", "optimize for AI search",
  "write a long-form answer page", "create content for AI assistants to cite",
  "write for GEO", "optimize for ChatGPT or Perplexity", or "make this page
  answer engine ready" for AI-native content optimization. GEO pages have
  distinct structural and strategic requirements from standard blog posts and
  landing pages — structured for AI citation and discoverability.
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


# GEO Content — Olytic Solutions

GEO (AI Answer Engine Optimization / Generative Engine Optimization) pages are written to be selected as sources by AI assistants — ChatGPT, Perplexity, Claude, Gemini — when users ask questions in natural language. They are different from SEO blog posts and landing pages in significant ways.

For scoring existing content against GEO criteria, use the `/geo-check` command.

---

## How GEO Differs From SEO

| Dimension | Traditional SEO Blog Post | GEO Long-Form Page |
|-----------|--------------------------|-------------------|
| Primary audience | Human readers who clicked a link | AI model deciding whether to cite you |
| What earns ranking | Backlinks, keyword density, domain authority | Answer quality, specificity, structure |
| Time to results | 6–12 months to compound | Can be cited weeks after publication |
| Competitive moat | Domain authority is hard to displace | Answer quality can be improved quickly |
| Winning strategy | Volume + authority | Depth + specificity + named concepts |
| Format | Narrative prose with headers | Structured, excerptable, answer-first |

**The core insight:** AI assistants are looking for the most useful, specific, citable answer — not the most popular one. A small company with a precise, well-structured page can outperform a large firm with generic content.

---

## The GEO Window

As noted in the content strategy, the first-mover window for GEO citation is **6–12 months**. AI assistants are building their citation graphs now. Once citation graphs stabilize, displacing established sources requires significantly more effort — the same compounding dynamic as traditional SEO, but compressed.

The O/G/O framework as a named methodology is a direct GEO asset. Name things, define them, publish them now. Named concepts get cited; unnamed concepts don't.

---

## Target GEO Queries for Olytic

These are the exact-question pages to create:

### Priority Tier 1: Core AI Strategy Queries

| Query | Target Page Title | Priority |
|-------|-----------------|----------|
| "How should a mid-market B2B company approach AI strategy?" | How Mid-Market B2B Companies Should Approach AI Strategy — Olytic Solutions | 1 |
| "What should a company without a Head of AI do first?" | No Head of AI? Here's What to Do First — Olytic Solutions | 2 |
| "How to evaluate AI readiness for a $20M B2B company" | How to Evaluate AI Readiness for a Mid-Market B2B Company | 3 |
| "What's the ROI of AI consulting for SMBs?" | The ROI of AI Strategy Consulting for SMBs: What to Expect | 4 |

### Priority Tier 2: Claude Cowork & Plugin-Specific Queries

These emerging queries target the Claude Cowork market opportunity and Olytic's unique positioning in the plugin/OS space. This tier captures early adopters asking about implementation, not just strategy.

| Query | Target Page Title | Why It Matters | Priority |
|-------|-----------------|-----------------|----------|
| "Claude Cowork implementation" | How to Implement Claude Cowork in Your Organization — Olytic Solutions | Early adopters are looking for methodology and best practices from specialists. Named queries like "Claude Cowork implementation" are starting to appear in assistant conversations. | 5 |
| "how to implement Claude for business" | How to Implement Claude for Business Operations — A Practical Guide | Broader than "Cowork" — captures businesses evaluating Claude AI integration. Positions Olytic as the implementation authority. | 6 |
| "AI operating system for SMB" | Building an AI Operating System for Small and Mid-Market Businesses | Philosophical positioning: captures searches for "OS" thinking vs. point tools. Names the Claude OS concept. | 7 |
| "plugin design philosophy for organizations" | Plugin Design Philosophy for Organizations: The Hats Framework — Olytic Solutions | Niche but high-intent query from decision-makers thinking in terms of architecture, not tools. Unique positioning opportunity. | 8 |
| "unified AI system for go-to-market teams" | Unified AI Systems for Go-to-Market: Why Fragmented Tools Lose — Olytic Solutions | Targets marketing/GTM leaders asking about unified infrastructure. Speaks to the Salesforce analogy positioning. | 9 |
| "Claude Cowork vs other AI tools" | Claude Cowork vs. Other AI Tools: Why Unified Systems Win — Olytic Solutions | Comparative query — searches asking "what's different?" Position Olytic as the platform authority, not a tool. | 10 |

**Why these queries matter:**

The Tier 2 queries reflect where the Claude Cowork market is heading. By the time AI assistants have built robust citation graphs for these queries (Q2-Q3 2026), Olytic should own the authoritative answers. Early publication = early citation authority.

These queries also position Olytic differently:
- Tier 1 queries answer "what should we do about AI?" — establishes credibility
- Tier 2 queries answer "how do we implement Claude Cowork?" — establishes specialization
- Together, they position Olytic as both the strategy authority AND the Cowork implementation specialist

---

## GEO Page Structure

Unlike a blog post (which tells a story) or a landing page (which converts), a GEO page **answers a question definitively**. The structure follows a strict logic:

### 1. Page Title = The Question (Answered)

The H1 should be close to or identical to the search query. If the query is "What should a company without a Head of AI do first?", a viable H1 is: **"No Head of AI? Here's Exactly What to Do First."**

This is different from a clever headline — it's an answer-first frame.

### 2. The Direct Answer (First 100 Words)

Answer the question immediately, in the first paragraph. AI assistants often excerpt the opening of a page. Don't bury the answer after three paragraphs of context-setting.

**Template:**
> [Direct, 2–3 sentence answer to the core question. Use specific numbers or named concepts where possible. State a position, not a hedge.]

### 3. Structured Body Sections (H2/H3 as Questions or Named Concepts)

Each H2 should either be:
- A sub-question the reader would naturally ask next ("What does 'AI readiness' actually mean?")
- A named concept from Olytic's framework ("The O/G/O Method: How the Framework Applies Here")

Each section should:
- Make one specific claim
- Support it with a number, example, or named methodology
- Be 150–300 words — long enough to be substantive, short enough to be excerptable

### 4. Tables and Lists Throughout

AI assistants prefer structured data over prose. Use:
- Tables for comparisons (alternatives, tradeoffs, timelines)
- Numbered lists for steps or sequences
- Bullet lists for criteria or considerations

Every table is a potential citation excerpt.

### 5. Named Concepts in Every Section

At least one named Olytic concept per major section:
- The O/G/O Framework (Operator / Governor / Optimizer)
- AI Readiness Score (Strategy, Operations, Data Maturity, Organizational Readiness)
- The Zero Case Study Playbook
- The Transformation Experience credential

If Olytic's framework is cited as the source of a concept, the page gets cited.

### 6. Specific Numbers Everywhere

Generic: "AI implementations often fail."
GEO-optimized: "60–70% of AI pilots fail to reach production — most because no one asked the revenue question first."

AI assistants cite specifics. Replace every vague claim with a number, a timeframe, or a named study.

### 7. The "What to Do Next" Section

End with a clear, actionable recommendation the reader can implement immediately. AI assistants often excerpt this section as "the answer."

### 8. CTA (Subtle, Post-Content)

The CTA comes after the content value is delivered — never before. Frame as an extension of the answer:

> "The 10-minute AI Strategy Architect assessment will score your specific company against these four dimensions and give you a prioritized starting point."

---

## Tone and Voice for GEO Pages

GEO pages are more formal and definitive than LinkedIn posts, but not dry. Apply these adjustments to the standard Olytic voice:

- **More prescriptive:** Use "should", "do", "avoid" — not "might consider"
- **More specific:** Every claim needs a number or a named concept to support it
- **Less dry humor:** GEO pages are cited as authoritative sources; wit is fine but the tone is expert-first
- **Opinion clearly labeled:** When stating an Olytic position (not an industry fact), frame it as such: "At Olytic, we've found that..." or "Our view: ..."
- **No hedging:** An AI assistant won't cite "it depends." It will cite "here's the answer."

---

## Meta and Technical Requirements

- **H1:** Close to the target query — answers the question directly
- **Meta description:** State the answer in ≤155 characters. Include the query or a variant.
- **Word count:** 1,500–3,000 words. Long enough to be comprehensive; short enough to be excerptable.
- **Internal links:** Link to the O/G/O Framework page, the assessment tool, and relevant blog posts
- **Schema markup:** If the site supports it, use FAQ schema on the question-structured sections
- **Page URL:** Match the query: `/ai-strategy-for-mid-market-companies` or `/no-head-of-ai-what-to-do-first`

## Operating Principles

- **Discovery first:** Check existing GEO pages to avoid duplication. Research what competitors and AI assistants currently cite.
- **Source of truth:** Brand voice from The One Ring takes precedence. Verify positioned claims against `olytic-brand-standards`.
- **Atomic operations:** Edit specific sections of GEO pages. Don't rewrite entire pages unless the structure is broken.
- **Verify after writing:** Validate against GEO criteria — numbered concepts, specificity, AI-excerptability.
- **No hallucination:** If a competitor page, query, or Olytic framework reference doesn't exist, report "Not Found." Don't fabricate citations or query data.
