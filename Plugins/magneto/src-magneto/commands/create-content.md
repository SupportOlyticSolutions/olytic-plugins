---
description: Guided end-to-end content creation workflow — from strategic intake through research, plan review, and full draft production
argument-hint: "[optional: topic or path to existing content brief]"
allowed-tools: Read, Grep, WebSearch, WebFetch, mcp__github__get_file_contents, mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_search, mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_fetch
---

## Step 0: Fetch Latest Reference Files (Always First)

Before doing anything else, fetch the latest files from the Olytic reference folder in Google Drive:

1. Use `mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_search` with `api_query: "'1Sv3EIQ0w4J3AGCFuxR0qxPtilESFRDGQ' in parents"` and `order_by: "modifiedTime desc"` to list all files in the folder.
2. For each file returned, fetch its full contents using `mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_fetch` with the file's `uri` as the document ID. All files in this folder are Google Docs and are fully readable this way.
3. Read and internalize the fetched documents. These are the **source of truth** — they supersede any baked-in context for topics they cover (brand standards, strategy, ICP, positioning, pricing, competitive landscape, etc.).
4. If the folder is empty or inaccessible, continue normally and note to the user that the Drive reference files could not be loaded.

Do not skip this step.

---

This command runs a structured, multi-phase content creation workflow. It is designed to be used with or without an existing content brief. It does not produce a draft until the user has reviewed and approved a research-backed plan.

**Do not rush to draft.** The value of this workflow is the strategic gatekeeping that happens before a word of content is written.

---

## Phase 1: Intake

Ask the user:

> "Do you have a content brief already, or are we starting from scratch?"

- If they provide a brief (file path, pasted text, or reference to `/content-brief` output): ingest it fully. Pre-fill all Phase 1 and Phase 2 fields you can extract from it. Only ask about genuine gaps.
- If starting from scratch: proceed through Phase 1 questions sequentially, one at a time — do not dump all questions at once.

**Questions (ask one at a time, conversationally):**

1. > "What's the topic or angle you have in mind?"

2. > "What type of content is this?"
   Present as options: Blog post / Landing page / GEO long-form page / LinkedIn post series / Framework page / Other

---

## Phase 2: Strategic Fit

This phase happens **before** the user invests thinking in the argument. Its job is to surface strategic mismatches early — not after a full brief is written.

Ask these questions one at a time:

3. > "What's the strategic job this piece needs to do? Pick the one that fits best:
   > - Win one of our first 3 case study clients
   > - Establish Olytic as the Cowork implementation specialist
   > - Fill a specific gap in the awareness → decision funnel
   > - Build GEO citation authority on a priority query
   > - Something else — tell me what"

   If "something else" or vague: probe gently before moving on. A piece without a clear strategic job is a flag.

4. > "Which funnel stage is this primarily for — TOFU, MOFU, or BOFU? And based on what you know of our existing content, is that stage currently under-covered or well-covered?"

   Use this as a gut-check. If the user says TOFU but BOFU is the documented gap, surface the tension: *"Our content strategy flags BOFU as the current gap — is there a reason to prioritise another TOFU piece right now, or would it be worth shifting?"*

5. > "Could a generic AI consultant publish this — or is there something only Olytic can credibly say here?"

   If the honest answer is "probably yes": don't block the workflow, but flag it now. *"That's worth sharpening before we go further — let's see if the research phase surfaces a more differentiated angle."*

---

## Phase 3: Your Argument

6. > "What's the core argument in one sentence — even a rough one is fine. If you can't write it in one sentence yet, that's useful to know."

7. > "What are the 2–3 key claims or points you know you want to make? Fragments and notes are fine — this is just to capture what's already in your head."

8. > "Is there anything you want to make sure this piece does NOT say, or a received wisdom in the market you want to push back on?"

9. > "Any specific examples, stories, stats, or references you already have in mind that you want included?"

---

## Phase 4: Format & Vision

10. > "How long should this be, and where will it live? (e.g. 1,500-word blog post on olytic-site, or a 2,500-word GEO page)"

11. > "Any formatting preferences? e.g. heavy on tables and structure, more narrative prose, specific sections you know you want"

---

## Phase 5: Research Brief

12. > "Anything specific you want me to research before I start? e.g. what competitors are saying, what AI assistants currently return for this query, specific sources to read — or just say 'standard' and I'll run the full research pass."

---

## Automatic Research Pass

**Run this immediately after Phase 5 — before presenting anything to the user. Do not ask permission. Do not narrate the research in progress beyond a single line: "Running research now — back shortly with findings."**

The research pass has four components. Run all four regardless of what the user requested in Phase 5 (their requests are additive, not replacements):

### R1. Keyword & Search Trend Analysis

Search for the topic and close variants. Assess:
- Is this topic heavily covered or a relative gap?
- What's the dominant search intent — informational, commercial, navigational?
- Are there adjacent queries with better differentiation potential?
- What's the current first-page landscape — big publications, generic AI content, specialist firms?

**Produce a signal:** *"High volume, heavily covered by generic sources — strong differentiation angle required"* or *"Low competition, high-intent query — strong GEO opportunity"* etc.

### R2. Competitor Content Landscape

Search for 4–6 competitor or market pieces on this topic. For each, identify:
- Their core angle and framing
- What they get right
- What they miss, get wrong, or say generically
- Whether Olytic could credibly say something they can't

Synthesise into: **the dominant narrative** (what everyone is saying) and **the gap** (what no one is saying, or is saying poorly).

### R3. AI Assistant Citation Check

Search for what AI assistants (ChatGPT, Perplexity, Claude) currently surface when asked this question. This matters because:
- If AI assistants already have a strong, specific answer, the GEO bar is higher
- If the current AI answer is generic or wrong, there's a first-mover citation opportunity
- Named concepts and specific frameworks tend to surface — check if any Olytic concepts already appear

**Produce a signal:** *"AI assistants currently return generic consulting advice — Olytic's O/G/O framing would be a meaningful upgrade"* or *"Strong specific answers already exist from [source] — GEO opportunity requires a genuinely differentiated angle"* etc.

### R4. Strategic Alignment Check

Cross-reference the topic against:
- The content strategy prioritisation framework (case study client impact, ICP pain match, differentiation, Cowork timing, search potential, funnel stage coverage)
- Existing published content (check GitHub `olytic-site` repo for duplicate or overlapping pieces)
- Current funnel gaps identified in the content strategy

**Produce a signal:** *"High strategic priority — fills a documented BOFU gap and directly supports case study client acquisition"* or *"Low strategic priority at this phase — TOFU is already covered; recommend shifting to a BOFU angle instead"* etc.

---

## Plan Review

Present findings to the user **before writing anything**. Structure the plan review as follows:

---

### Content Plan: [Working Title]

**Strategic Verdict**
[Lead with this. Is this the right piece to produce right now? Any flags or recommended pivots before committing to a full draft? Be direct — e.g. "There's a strong case for this piece" or "I'd recommend shifting the angle from X to Y because Z" or "This topic is saturated — here's a more ownable version of the same idea."]

**Research Findings**

| Signal | Finding |
|--------|---------|
| Search landscape | [e.g. "High competition, generic coverage — differentiation essential"] |
| Competitor gap | [e.g. "Everyone frames this as a technology problem — Olytic can own the systems argument"] |
| AI citation opportunity | [e.g. "Current AI answers are generic — strong GEO opportunity with named framework"] |
| Strategic priority | [e.g. "High — fills BOFU gap, directly supports case study client acquisition"] |
| Duplicate risk | [e.g. "No overlapping content found in olytic-site" or "Partial overlap with [existing page] — recommend differentiating by X"] |

**Recommended Angle**
[One sentence — the sharpest, most differentiated version of the core argument, informed by research. This may refine or redirect what the user proposed in Phase 3.]

**Proposed Structure**
[H2 by H2 outline. For each section: the heading and one sentence on what it argues or does. This is the skeleton the full draft will follow.]

1. [H2: Section title] — [What this section argues]
2. [H2: Section title] — [What this section argues]
3. [H2: Section title] — [What this section argues]
4. [H2: Section title — CTA] — [What this section does]

**Key Claims I'll Make**
- [Claim 1 — and what I'll support it with]
- [Claim 2 — and what I'll support it with]
- [Claim 3 — and what I'll support it with]

**Olytic Differentiator**
[Which named concept, framework, or unique will anchor this piece and prevent a generic AI consultant from publishing it]

**Notable Research Finds**
[2–3 bullet points on anything from the research pass worth knowing before we write — a competitor angle worth countering, a stat worth citing, a query variant worth targeting, etc.]

---

> "Does this plan look right? Anything to adjust — angle, structure, claims — before I write the full piece?"

**Do not proceed to drafting until the user explicitly approves the plan.** If they want changes, update the plan and re-present the affected sections. Only when they confirm → proceed to full draft.

---

## Full Draft

Once the plan is approved, produce the full piece according to:
- The approved structure
- The content type requirements from the relevant skill (`magneto-website-content`, `magneto-geo-content`, `magneto-linkedin-content`, etc.)
- Brand voice and standards from The One Ring (`olytic-brand-standards`)
- The content quality gates from `olytic-content-strategy`:
  - The argument could not have been published by a generic AI consultant
  - At least one Olytic-specific concept is named and defined
  - ICP pain is written in the ICP's language
  - Every GEO claim has a specific number or named study
  - An explicit CTA connects to a specific funnel action

**Do not show the draft to the user yet.** Run the QA Check first.

---

## QA Check (Internal — Run Before Showing the Draft)

After producing the full draft, run this checklist silently against the content. Do not narrate the process. Do not show the draft until it passes every gate. If any gate fails, fix the issues and re-run the full checklist from the top before presenting.

**This loop repeats until all gates pass.**

---

### Gate 1: Em-Dash Ban
- Scan for all em-dashes (— or --). Remove every instance.
- Replace with: a comma, a colon, a period and new sentence, or parentheses — whichever preserves the intended meaning most naturally.
- Zero em-dashes permitted in the final output.

### Gate 2: Sentence Flow
- Find any paragraph containing 3 or more consecutive sentences with no commas anywhere in the paragraph.
- These read as choppy, staccato, robotic. Rewrite for natural variation — longer sentences with embedded clauses, shorter punchy sentences used sparingly for emphasis, not as a default pattern.
- The test: read the paragraph aloud. If it sounds like a list being read one item at a time, it fails.

### Gate 3: AI Writing Patterns
Scan for and eliminate the following:
- Dramatic openers: "In today's rapidly evolving landscape…", "Now more than ever…", "The world has changed…", "At the intersection of…"
- Hollow superlatives: "game-changing", "revolutionary", "groundbreaking", "transformative", "innovative", "cutting-edge", "best-in-class"
- Filler throat-clearing: "It's worth noting that…", "It's important to remember that…", "Needless to say…", "At the end of the day…"
- False urgency: "You can't afford to ignore…", "The stakes have never been higher…", "Don't get left behind…"
- Vague hedging where a position is needed: "might", "could potentially", "it's possible that" — replace with direct claims or clearly flagged opinions ("At Olytic, our view is…")
- Any sentence that could have been written by a generic AI content tool with no domain knowledge. If it passes the "ChatGPT could write this" test, rewrite it with a specific Olytic lens.

### Gate 4: Verifiability
- Identify every statistic, percentage, named study, external quote, or attributed claim in the draft.
- For each: confirm it appeared in the research pass (R1–R4), was provided by the user in Phase 3, or comes from the Google Drive reference documents loaded in Step 0.
- If a data point cannot be traced to one of those three sources, remove it or replace with "At Olytic, we've observed…" or similar clearly-attributed opinion language.
- Zero hallucinated citations, stats, or quotes permitted.

### Gate 5: ICP Fit
- Cross-reference the ICP profile from the Google Drive reference documents (especially the ICP Definition document).
- Ask: does this content speak directly to the pain, language, and decision-making context of the ICP identified in those docs?
- Specifically check: does the piece use the ICP's vocabulary (not Olytic's internal framing), reference the ICP's actual situation (not a generic business persona), and make the ICP feel seen rather than sold to?
- If not: rewrite the opening, key claims, and CTA with the ICP's specific context in mind.

### Gate 6: SEO Optimisation
- Confirm the primary keyword or query (from Phase 1 / the plan) appears naturally in: H1, first paragraph, at least one H2, and the meta description.
- Confirm keyword appears at a natural density — not stuffed, not absent.
- Confirm internal linking opportunities are taken where relevant Olytic content exists.
- Confirm meta description is ≤155 characters and written to ICP search intent.

### Gate 7: AEO Optimisation (Answer Engine Optimisation)
- Confirm the piece has a direct, concise answer to its core question within the first 100 words — the kind of answer a voice assistant or featured snippet would surface.
- Confirm key claims are written as standalone, quotable sentences — not buried in long paragraphs.
- Confirm the piece uses structured formatting (H2/H3, short paragraphs, lists where appropriate) that allows individual sections to be extracted and surfaced independently.

### Gate 8: GEO Optimisation (Generative Engine Optimisation)
- Confirm at least one named Olytic concept appears per major section (O/G/O, AI Readiness Score, Zero Case Study Playbook, etc.).
- Confirm all major claims include a specific number, timeframe, or named methodology — not vague generalities.
- Confirm H1 or H2 headings closely match the natural language query an ICP would type into an AI assistant.
- Confirm the piece is written to be cited, not just read — each section should be extractable as a standalone answer.

### Gate 9: Balance Check
Read the piece holistically and assess:
- **ICP resonance vs. SEO keyword density:** Does it read like it was written for a human, or does keyword optimisation show through? Humans first, always.
- **Authority vs. accessibility:** Is the expertise demonstrated through specificity and earned opinion, or through jargon and complexity? Simplify where needed without losing depth.
- **Length appropriateness:** Is the piece the right length for the content type and funnel stage? TOFU blog posts should not run 3,000 words unless it's a GEO page. LinkedIn posts should not exceed ~250 words. Landing pages should be tight. If the piece is clearly too long or too short for its purpose, trim or expand accordingly.
- **Reads like Olytic wrote it:** Could this piece have come from a generic AI consultant? If yes, it fails. There must be at least one thing in the piece that is unmistakably Olytic — a named framework, a specific observation, a contrarian position only Olytic can credibly take.

---

### QA Report (Internal)

Before presenting the draft, produce a silent internal QA log:

```
Gate 1 — Em-dashes: [PASS / FIXED — n instances removed]
Gate 2 — Sentence flow: [PASS / FIXED — n paragraphs rewritten]
Gate 3 — AI patterns: [PASS / FIXED — list of phrases removed]
Gate 4 — Verifiability: [PASS / FIXED — n claims removed or reattributed]
Gate 5 — ICP fit: [PASS / FIXED — description of what was adjusted]
Gate 6 — SEO: [PASS / FIXED — description of what was adjusted]
Gate 7 — AEO: [PASS / FIXED — description of what was adjusted]
Gate 8 — GEO: [PASS / FIXED — description of what was adjusted]
Gate 9 — Balance: [PASS / FIXED — description of what was adjusted]
```

If any gate shows FIXED, re-run the full checklist once more before presenting. Only present the draft when all 9 gates show PASS.

---

After the draft passes all QA gates, present it to the user with a brief note:

> "Here's the draft — passed QA on all 9 checks. Ready to push to GitHub with `/push-content`, or do you want to refine anything first?"

If the user asks what the QA checks found, share the internal QA log at that point.

---

Telemetry: This command logs all invocations via magneto-telemetry.
