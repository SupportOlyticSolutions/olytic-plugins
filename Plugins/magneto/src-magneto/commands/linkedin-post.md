---
description: Draft 3 LinkedIn post options in Olytic's voice from a topic or existing URL
argument-hint: "[topic, idea, or URL to a piece of content]"
allowed-tools: Read, WebFetch, WebSearch
---

## Step 0: Fetch Latest Reference Files (Always First)

Before doing anything else, fetch the latest files from the Olytic reference folder in Google Drive:

1. Use `mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_search` with `api_query: "'1Sv3EIQ0w4J3AGCFuxR0qxPtilESFRDGQ' in parents"` and `order_by: "modifiedTime desc"` to list all files in the folder.
2. For each file returned, fetch its full contents using `mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_fetch` with the file's `uri` as the document ID. All files in this folder are Google Docs and are fully readable this way.
3. Read and internalize the fetched documents. These are the **source of truth** — they supersede any baked-in context for topics they cover.
4. If the folder is empty or inaccessible, continue normally and note to the user that the Drive reference files could not be loaded.

Do not skip this step.

---


Draft three LinkedIn post options based on `$ARGUMENTS`. If `$ARGUMENTS` is a URL, fetch the page and derive post angles from its content. If it's a topic or idea, draft directly.

**Steps:**

1. Parse `$ARGUMENTS`:
   - If a URL → fetch the page, extract the core argument and 2–3 supporting claims
   - If a topic/idea → proceed directly to drafting
2. Load brand standards from The One Ring (`olytic-brand-standards`) — voice rules apply fully to LinkedIn content
3. Draft three post options, each taking a distinct angle (see angles below)
4. Present all three with a recommended pick and rationale

---

## LinkedIn Post Format Rules

LinkedIn posts at Olytic follow a specific anatomy:

**Structure:**
```
[HOOK — 1 line. The entire post lives or dies here.]

[BODY — 3–6 short paragraphs or a short list. Each line is its own paragraph. No walls of text.]

[LANDING — 1 punchy line that lands the point.]

[CTA — 1 soft line linking to the assessment tool or a question to drive comments.]
```

**Hook formulas that work for Olytic's voice:**
- The blunt take: "Most AI strategies I see are just a list of tools. That's not strategy."
- The counterintuitive: "The 'Head of AI' hire is a trap for companies under $50M."
- The diagnosis: "Your AI pilot didn't fail because of the technology. It failed because nobody asked the revenue question."
- The number: "3 signs your AI implementation is already off the rails."
- The question: "What does a $20M company actually do with AI — before spending a dollar?"

**Voice reminders for LinkedIn:**
- Contrarian, specific, opinionated — not "thought leadership"
- Short sentences. Each line breathes.
- No emojis, no hollow superlatives, no "in today's rapidly evolving landscape"
- The post should read like it came from someone who's actually done this work — not a content marketer
- End with a question or a soft link to the assessment tool, never a hard pitch

**Post angles (use one per option):**
- **Contrarian take** — challenge a common assumption the ICP holds
- **Diagnosis** — name a problem the ICP has but hasn't fully articulated
- **Framework snippet** — teach one piece of the O/G/O model in plain language
- **Stakes** — what happens if they don't act (or do)
- **Pattern observation** — something you've noticed across multiple companies

---

## Output Format

Present three complete post drafts, each with:
- **Angle:** [which angle this takes]
- **Estimated length:** [word/character count]
- **Post draft:** [full text, formatted with line breaks as it would appear on LinkedIn]
- **CTA used:** [the specific CTA line]

Then: **Recommended pick** with 1–2 sentences of rationale.

Ask if the user wants to refine any of the three, or generate alternatives with different angles.
