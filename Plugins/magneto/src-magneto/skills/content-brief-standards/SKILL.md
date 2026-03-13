---
name: magneto-content-brief-standards
description: >
  Use this skill to "create a content brief", "brief me on this topic",
  "plan this article before writing", "what should I cover in this post",
  "give me a brief for", "outline this piece before we write it", or "what's
  the structure for this content". Establishes the required fields every piece
  of content must define before drafting begins.
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


# Content Brief — Olytic Solutions

A content brief is a required pre-writing planning document. No substantive content should be drafted without completing the brief first. This is not bureaucracy — it is the discipline that keeps every piece of content strategically grounded instead of generically interesting.

For a complete brief-generation workflow from a topic, use the `/content-brief` command.

---

## Why Briefs Are Required

The three most common content failures at Olytic's stage:

1. **Wrong funnel stage** — writing awareness content when the bottleneck is decision-stage conversions
2. **Wrong ICP pain** — writing about AI strategy in the abstract when the ICP's actual question is "where do we start?"
3. **No differentiation** — writing content a generic AI consultant could have published

A brief prevents all three by forcing explicit answers before a word is written.

---

## The Brief Format

Every content brief must include all of the following fields. No field is optional.

### Required Fields

**Topic:** The working title or specific angle — not just a subject area. Not "AI strategy" but "Why AI pilots fail when no one asks the revenue question first."

**Content Type:** One of:
- Blog post (credibility + visibility)
- Landing page (conversion)
- GEO long-form page (AI citation + visibility — see `magneto-geo-content` skill)
- LinkedIn post series (awareness + traffic)
- Framework page (IP credential — O/G/O, AI Readiness Score, etc.)
- Case study page (proof — only once clients are live)

**Funnel Stage:** TOFU / MOFU / BOFU. Be explicit. If it serves multiple stages, name the primary one.

**Strategic Purpose:** One of the three strategic purposes this content serves:
- **Credibility** — demonstrates expertise that makes the ICP trust Olytic before working with us
- **Visibility** — gets in front of the right people through content or search
- **Conversion** — makes it easy for a prospect to understand what we do and start a conversation

**Target ICP Pain:** The specific frustration or question this content addresses, written in the ICP's language — not Olytic's. Not "we explain AI strategy" but "they don't know where to start and feel embarrassed to admit it."

**Primary Keyword / Query:** The search term or natural language question being targeted. For GEO pages, this is the exact question an AI assistant would answer. For blog posts, it's the keyword phrase.

**Core Argument / Thesis:** One sentence. The single idea this piece exists to make. If you can't write it in one sentence, the argument isn't clear enough to write the piece.

**Key Claims:** 3–5 specific claims that support the thesis. Each claim should be falsifiable — something that could be wrong, not just an obvious observation.

**Olytic Differentiator:** Which of Olytic's three uniques this content demonstrates:
- Revenue systems and operations expertise
- The O/G/O model (methodology differentiation)
- Strategic value creation (outcome focus, not tool focus)

**Competitive Context:** What are competitors publishing on this topic? What's the received wisdom Olytic is challenging or improving on?

**Recommended Structure:** Section-by-section outline, with H2 heading suggestions. Minimum three sections, maximum seven for a blog post.

**Primary CTA:** What should the reader do when they finish? Be specific. "Take the AI Strategy Architect assessment" is a CTA. "Learn more" is not.

**Meta Description (draft):** ≤155 characters. Written for the ICP, includes the keyword or query.

**Headline Options (3):** Three distinct headline approaches:
- Option A: Specific, practical, expert-level
- Option B: Contrarian or provocative
- Option C: Problem-first or question-based

**Priority:** High / Medium / Low, based on the content strategy prioritization matrix:
- Does this directly help win one of the first 3 case study clients? → High
- Does this address a specific ICP pain of a disappointed AI adopter? → High
- Does this capitalize on the GEO first-mover window? → High
- Does this fill a BOFU gap? → High
- Does this fill a TOFU gap when BOFU is already covered? → Medium/Low

### Claude OS Content Extension

**For content about Olytic's Claude OS service specifically**, add one additional required field:

**Strategic OS Dimension(s):** Which of the Five Dimensions of the Claude OS does this content speak to? Select one or more:
- **Unified** — the value of one integrated system vs. point tools (Salesforce analogy, reducing fragmentation)
- **Custom** — personalization to the company's workflows, language, and processes
- **Augmenting** — amplification and strategic augmentation, not task automation
- **Agentic** — powered by advanced AI reasoning and autonomous decision-making
- **Compounding** — how the system improves itself over time through the O/G/O loop (Operate → Govern → Optimize)

Example: A brief for "Why Unified AI Systems Beat Tool Stacks" would declare `Dimension: Unified`. A brief for "How the Optimizer Loop Keeps Your Plugins Aligned" would declare `Dimension: Compounding`.

This field ensures Claude OS content explicitly ties to the strategic philosophy and avoids generic AI service positioning.

---

## Constraints That Apply to Every Brief

Before a brief is considered complete, verify:

- [ ] The core argument could not have been written by a generic AI consultant
- [ ] The ICP pain is written in the ICP's language, not Olytic's
- [ ] A specific Olytic differentiator is identified (not "we know what we're doing" — which one of the three uniques?)
- [ ] The CTA connects to a specific next step in the funnel, not a generic "contact us"
- [ ] The funnel stage has been explicitly declared
- [ ] A meta description is drafted (not "to be written")
- [ ] For Claude OS content: The Strategic OS Dimension(s) has been declared (if applicable)

---

## Brief Review Checklist

Before moving to drafting, confirm:

1. **Does the thesis challenge something?** A thesis that everyone already agrees with isn't worth writing.
2. **Could only Olytic credibly write this?** If a generic AI blog could publish it, the angle needs sharpening.
3. **Is the ICP pain specific?** "They want to use AI" is not a pain. "They ran a ChatGPT pilot that produced generic outputs and now the CEO is skeptical" is a pain.
4. **Is the CTA appropriate for the funnel stage?** TOFU content shouldn't ask for a sales conversation. BOFU content should.
5. **Is the priority score honest?** Don't inflate priority to justify writing something interesting but strategically low-value.
6. **For Claude OS content: Does the dimension declaration match the core argument?** If the brief is about unified systems vs. point tools, the dimension should be "Unified." If they don't align, clarify the angle.

## Operating Principles

- **Discovery first:** Check existing briefs and published content to understand what's already been covered. Don't create briefs for duplicate angles.
- **Source of truth:** ICP pain and strategic priorities from The One Ring take precedence. Verify against `olytic-brand-standards` and company strategy.
- **Atomic operations:** Create or edit individual briefs. Don't bulk-rewrite the entire brief archive.
- **Verify after writing:** Validate that every required field is complete before considering the brief ready for drafting.
- **No hallucination:** If a competitor claim, ICP quote, or Olytic differentiator can't be verified, report "Not Found." Don't fabricate competitive intelligence.
