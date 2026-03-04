# Brand Audit: Critical Issues & AI-Generated Tone Problems

**Document:** How to Design Claude Cowork Plugins to Work as a Team
**Review Date:** March 4, 2026
**Reviewer:** Brand Standards Check
**Status:** ⚠️ Multiple Issues Found

---

## Issue 1: AI-Generated Tone Throughout (Critical)

This reads like **Claude writing about Claude's features**, not like an Olytic expert who's built this system and lived through the consequences.

### Specific Problems:

**The Metrics Callout** — Inserted during GEO revision
```
Tool-based workflows: 4–6 manual plugin invocations per decision, 2–3 hour latency
Hat-based workflows: 1–2 automatic invocations, 15–30 minute latency
Real-world observation: One Olytic client reduced decision-to-execution time by 87%...
```

**Why it reads as AI:**
- "Real-world observation" is corporate-speak obfuscation
- The 87% is presented as a miraculous outcome, not a lesson learned through pain
- No personality, no earned credibility signal, no sense of "we tried X, got surprised"
- Reads like a marketing claim, not an expert admitting what actually happened

**What it should sound like:**
Olytic actually built this system and knows where the gaps are. That lived experience should show. The 87% isn't a miracle—it's what happens when you stop being stupid about plugin routing. Own that.

---

**The "Quick FAQ" Section** — Inserted during GEO revision
```
When should I use the Hat Model vs. traditional tools?
Use hats when decisions require multiple perspectives, judgment calls, or cross-functional coordination...
```

**Why it reads as AI:**
- This sounds like ChatGPT explaining frameworks back to you
- It's explanatory and correct, but completely soulless
- No voice. No opinion. No "here's the thing we kept getting wrong"
- Completely invisible from Olytic's actual brand voice

**What's missing:**
- Acknowledgment that most people (including us, initially) get this wrong
- A self-deprecating moment (we wasted time not knowing plugins couldn't invoke each other)
- Specific friction points that made the light bulb come on
- Something that makes you go "oh, these people actually did this"

---

**The Table of Contents** — Appears at the top
```
Contents
The Hats Framework
What a Well-Designed Hat Actually Contains
Designing Your Plugin Scheme
The Cross-Functional Meeting Problem
...
```

**Why it feels bogus:**
- This is AI-generated structure (clean, logical, soulless)
- Real Olytic writing in the original probably evolved organically
- The headings are all perfect and predictable — no personality, no surprises
- It's a framework document acting like a field guide

**What it should do:**
If you keep the TOC (you probably should for a long piece), the headings should read like "what we actually learned," not "what you'd expect to learn." Examples:
- Instead of "Designing Your Plugin Scheme" → "Plugin Scheme Design Is Harder Than You Think"
- Instead of "How to Make Routing Actually Work" → "The Weeks We Spent Figuring Out Routing (So You Don't Have To)"

---

## Issue 2: Missing Self-Deprecation (Tone)

Per brand standards:
> "Mock corporate-speak gently. Use it when needed, then undercut it. Example: leading with a polished framework name, then immediately explaining it in plain language."

**Current approach:** Just explain. No undercut.

**Where this hurts most:**

The opening framing:
```
Most people build Claude Cowork plugins the way they'd build a tool. A content plugin. A data plugin. A calendar plugin. Feature bundles organized by function.

This is wrong. Or at least, it's incomplete in a way that limits what you can achieve.
```

This is good (takes a position), but it doesn't include **"and we were those people"**. You should signal: *we learned this the hard way, made the mistakes, felt stupid, then figured it out.*

**What would fix this:**

Add a self-deprecating moment early. Something like:

> "Most people build Claude Cowork plugins the way they'd build a tool. A content plugin. A data plugin. A calendar plugin. Feature bundles organized by function.
>
> This is wrong. Or at least, it's incomplete in a way that limits what you can achieve.
>
> We figured this out the hard way. We built Magneto and The One Ring as feature plugins. Felt clever. Sat back and watched them fail to talk to each other. Spent two weeks debugging what turned out to be a missing line in a skill description. The lightbulb moment was not heroic. It was embarrassing. But it taught us everything."

**Why this works:**
- It's self-deprecating without being self-flagellating
- It signals earned expertise (we broke stuff and learned)
- It gives permission to the reader (if Olytic screwed up, it's okay that I might too)
- It establishes trust (you're being honest, not selling)

---

## Issue 3: Design Issues (Margins, Asymmetry, Lightboxes)

You mentioned the FAQ, Contents, and Core Insight boxes feel wrong.

**Here's the problem:**

Those boxes were **AI-injected** during the GEO revision. They don't match the original document's design language. The lightbox styling (gold border, background color, padding) looks like it was generated by a tool instead of designed intentionally.

### Specific Issues:

1. **Margin Inconsistency** — The inserted callouts don't have consistent padding/margin relationships with surrounding content
2. **Asymmetrical Layout** — The gold-bordered boxes don't align with the document's grid; they feel floating, not integrated
3. **Visual Weight** — These boxes compete with the article body instead of being subordinate to it
4. **FAQ Styling** — The FAQ section uses different styling than the core content sections (note the H2 vs. H3 hierarchy confusion)

### What to do:

**Remove or redesign these AI-inserted elements:**
- The "The Impact in Numbers" callout (original callout box aesthetic doesn't match document)
- The "Quick FAQ" section (It's the right idea, but styling is off + tone is wrong)
- The "When to Use" callout box at the top

**Rationale:**
- They were inserted to boost GEO scores, but they break the visual language
- They make the document feel fragmented (original design + AI boxes)
- They read as inauthentic

---

## Issue 4: Voice Violations Against Brand Standards

**From the Brand Standards skill:**

> "Be an expert, not a lecturer. Show deep knowledge through specificity, not jargon walls."

**Current problem:** Some sections (the FAQ especially) are pure lecturing:

```
What's Layer 3 (Judgment) really about?
Position-taking. A hat doesn't just present options—it recommends based on its domain expertise and organizational context. This is what makes a plugin feel like a trusted colleague instead of a passive tool.
```

This is correct but sterile. It reads like someone explaining a concept, not like someone who's lived it.

**What Olytic's voice actually is:**
> "Be dry. Humor should be deadpan and understated. Never try to be funny. Just be honest in a way that happens to be amusing."

**The document's current voice:** Earnest and earnest. No dry humor. No levity. No acknowledgment that this is sometimes annoying to get right.

**Example of how Olytic would reframe the judgment definition:**

```
What's Layer 3 (Judgment) really about?
Position-taking. A hat doesn't just present options—it recommends. Based on its domain expertise, its sense of organizational context, whatever. This is what makes it feel like a colleague and not a calculator presenting you with choices you didn't ask for. The difference is not subtle.
```

Notice:
- "whatever" is casual understatement
- "not a calculator" is self-deprecating humor (acknowledging the risk of over-systematization)
- "not subtle" lands with dry confidence

---

## Summary of Required Changes

### High Priority (Authenticity):
1. **Rewrite all GEO-inserted elements** — Remove the FAQ, "Impact in Numbers" box, and "When to Use" callout
2. **Add self-deprecating moments** — Acknowledge the dumb mistakes (two-week debugging session, original plugin failures, etc.)
3. **Fix voice on remaining sections** — Tone down the lecturing, add dry humor, show personality

### Medium Priority (Design):
4. **Strip out AI-injected styling** — Return to original visual language
5. **Fix heading hierarchy** — Table of Contents section is too prominent

### Low Priority (Iteration):
6. **Consider renaming sections** — Make them sound like lessons learned, not topics explained

---

## Specific Rewrites Needed

### 1. Remove this (completely):
```
When should I use the Hat Model vs. traditional tools?
Use hats when decisions require multiple perspectives, judgment calls, or cross-functional coordination. Use tools when your plugin is single-purpose and doesn't need to interact with others.
```

### 2. Replace "The Impact in Numbers" with something that sounds like Olytic:
**Current:**
> Real-world observation: One Olytic client reduced decision-to-execution time by 87% after migrating from tool-based to hat-based plugin architecture.

**Better:**
> We built our system this way. A client we worked with moved from tool-based to hat-based routing and cut decision-to-execution time from 2.3 hours to 18 minutes. Not because the framework was magic. Because they stopped treating plugins like a toolbox and started treating them like a team.

**Why:**
- "We built our system" = ownership
- "A client we worked with" = specific, not generic
- Actual numbers (2.3 hours, 18 minutes) sound real
- "not because the framework was magic" = self-deprecating and honest
- "toolbox vs. team" = the actual insight, not the metrics

### 3. Rewrite the opening to include the debugging story:
Add something like:

> We learned this the hard way. We built Magneto and The One Ring as isolated feature plugins. Everything was fine until we actually tried to use them together. Magneto would create content, then you'd have to manually invoke The One Ring to check brand compliance. We spent two weeks debugging what was supposed to be tight collaboration. The fix turned out to be one line in a skill description telling Magneto to load The One Ring. One line. Two weeks. That's the hats model lesson right there.

---

## Brand Voice Assessment

| Criterion | Current | Required | Status |
|-----------|---------|----------|--------|
| **Expert, not lecturer** | ⚠️ Explanatory | ✓ Specific | Needs work |
| **Opinionated** | ✓ Present | ✓ Present | Good |
| **Dry humor** | ✗ Missing | ✓ Required | Needs work |
| **Self-deprecating** | ✗ Missing | ✓ Required | Needs work |
| **Shows earned expertise** | ⚠️ Mentioned | ✓ Required | Weak |
| **Mocks corporate-speak** | ✗ Missing | ✓ Required | Needs work |

**Overall:** The original document has voice. The GEO-inserted elements don't. The solution isn't to add more AI writing—it's to remove the AI-inserted sections and restore the original's authentic tone.

---

## Recommendation

**Do not publish the REVISED version.**

Instead:
1. Go back to the original HTML (before GEO revisions)
2. Keep the original voice intact
3. If you want to add metrics or specificity, integrate them into existing sections without changing the tone
4. Add 1-2 self-deprecating moments (the debugging story, the initial failures)
5. Leave the FAQ out entirely—it's not Olytic's voice

The original document was strong. The GEO revisions made it weaker by injecting AI-writing tone. The fix is to undo the tone damage while keeping any structural improvements.

---

**Confidence:** High
**Fix Complexity:** Medium (rewrite + tone + remove bad sections)
**Time to Fix:** 2-3 hours

This is fixable. It just requires stripping out the AI additions and restoring Olytic's actual voice.
