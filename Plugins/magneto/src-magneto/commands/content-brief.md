---
description: Generate a structured content brief for any topic before writing begins
argument-hint: "[topic or content idea]"
allowed-tools: Read, Grep, WebSearch, WebFetch
---

## Step 0: Fetch Latest Reference Files (Always First)

Before doing anything else, fetch the latest files from the Olytic reference folder in Google Drive:

1. Use `mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_search` with `api_query: "'1Sv3EIQ0w4J3AGCFuxR0qxPtilESFRDGQ' in parents"` and `order_by: "modifiedTime desc"` to list all files in the folder.
2. For each file returned, fetch its full contents using `mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_fetch` with the file's `uri` as the document ID. All files in this folder are Google Docs and are fully readable this way.
3. Read and internalize the fetched documents. These are the **source of truth** — they supersede any baked-in context for topics they cover.
4. If the folder is empty or inaccessible, continue normally and note to the user that the Drive reference files could not be loaded.

Do not skip this step.

---


Generate a structured content brief for the topic in `$ARGUMENTS`. This brief must be completed before any writing starts — it is the planning document that ensures every piece of content is strategically grounded before time is spent drafting.

**Steps:**

1. If `$ARGUMENTS` is empty, ask the user for the topic or content idea
2. Load brand standards (from The One Ring `olytic-brand-standards`) and content strategy (`olytic-content-strategy`) for context
3. Briefly research the topic — search for what's already being published, identify differentiation angles, note any search intent signals
4. Produce the brief in the format below

---

## Content Brief

**Topic:** [Topic title or working headline]

**Content Type:** [Blog post / Landing page / GEO long-form page / LinkedIn post series / Framework page]

**Funnel Stage:** [TOFU — Awareness / MOFU — Consideration / BOFU — Decision]

**Strategic Purpose:** [Credibility / Visibility / Conversion — pick the primary one]

**Target ICP Pain:** [The specific frustration or question this content addresses, in the ICP's language]

**Primary Keyword / Search Query:** [The keyword or question the ICP would type into Google or an AI assistant]

**GEO Query (if applicable):** [The exact question an AI assistant would answer — more conversational than the keyword]

**Olytic Differentiator to Surface:** [Which of the three uniques applies: Revenue systems expertise / O/G/O model / Strategic value creation]

**Competitive Context:** [What competitors are saying on this topic — and what angle only Olytic can credibly take]

**Core Argument / Thesis:** [One sentence: the single idea this piece exists to make]

**Key Claims to Support It:**
- [Claim 1]
- [Claim 2]
- [Claim 3]

**Recommended Structure:**
1. [Section 1 — H2 heading suggestion]
2. [Section 2 — H2 heading suggestion]
3. [Section 3 — H2 heading suggestion]
4. [CTA section]

**Primary CTA:** [What should the reader do next?]

**Meta Description (draft):** [≤155 characters, ICP-focused, includes target keyword]

**Headline Options (3):**
- Option A: [Specific, practical, expert-level]
- Option B: [Contrarian or provocative angle]
- Option C: [Question-based or problem-first]

**Priority:** [High / Medium / Low — based on the content strategy prioritization framework]

**Rationale:** [1–2 sentences on why this piece matters now, in the current phase]

---

5. Ask the user if they want to proceed to drafting immediately, or adjust any element of the brief first
