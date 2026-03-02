---
name: magneto-content-brief
description: >
  This skill should be used when the user asks for a "content brief", "brief me on this topic",
  "plan this article before writing", "what should I cover in this post", "create a brief for",
  or needs a structured planning document before writing any piece of content.
  Establishes the required fields every piece of content must define before drafting begins.
version: 0.1.0
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

---

## Constraints That Apply to Every Brief

Before a brief is considered complete, verify:

- [ ] The core argument could not have been written by a generic AI consultant
- [ ] The ICP pain is written in the ICP's language, not Olytic's
- [ ] A specific Olytic differentiator is identified (not "we know what we're doing" — which one of the three uniques?)
- [ ] The CTA connects to a specific next step in the funnel, not a generic "contact us"
- [ ] The funnel stage has been explicitly declared
- [ ] A meta description is drafted (not "to be written")

---

## Brief Review Checklist

Before moving to drafting, confirm:

1. **Does the thesis challenge something?** A thesis that everyone already agrees with isn't worth writing.
2. **Could only Olytic credibly write this?** If a generic AI blog could publish it, the angle needs sharpening.
3. **Is the ICP pain specific?** "They want to use AI" is not a pain. "They ran a ChatGPT pilot that produced generic outputs and now the CEO is skeptical" is a pain.
4. **Is the CTA appropriate for the funnel stage?** TOFU content shouldn't ask for a sales conversation. BOFU content should.
5. **Is the priority score honest?** Don't inflate priority to justify writing something interesting but strategically low-value.
