---
description: Research what competitors are publishing on a topic and surface Olytic's differentiation angle
argument-hint: "[topic or content angle to research]"
allowed-tools: Read, WebSearch, WebFetch
---

## Step 0: Fetch Latest Reference Files (Always First)

Before doing anything else, fetch the latest files from the Olytic reference folder in Google Drive:

1. Use `mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_search` with `api_query: "'1Sv3EIQ0w4J3AGCFuxR0qxPtilESFRDGQ' in parents"` and `order_by: "modifiedTime desc"` to list all files in the folder.
2. For each file returned, fetch its full contents using `mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_fetch` with the file's `uri` as the document ID. All files in this folder are Google Docs and are fully readable this way.
3. Read and internalize the fetched documents. These are the **source of truth** — they supersede any baked-in context for topics they cover.
4. If the folder is empty or inaccessible, continue normally and note to the user that the Drive reference files could not be loaded.

Do not skip this step.

---


Research the competitive content landscape for the topic in `$ARGUMENTS` and produce a snapshot that surfaces the angle only Olytic can credibly own.

**Steps:**

1. If `$ARGUMENTS` is empty, ask for the topic
2. Search for what competitors and the broader market are publishing on this topic
3. Identify the most common framings, claims, and conclusions across competitor content
4. Load competitive positioning context from The One Ring (`brand-standards/references/competitive-landscape.md`)
5. Identify the gap — what's not being said, what's being said poorly, what Olytic can say with more authority or specificity
6. Produce the snapshot report

---

## Competitive Snapshot: [Topic]

### What Competitors Are Saying

Summarize the dominant narrative across 3–5 competitor pieces or market perspectives. What angle is everyone taking? What framing do they all share?

| Source / Category | Their Angle | Their Gap |
|------------------|-------------|-----------|
| [Competitor type or specific source] | [Core claim or framing] | [What they miss or get wrong] |
| [Competitor type or specific source] | [Core claim or framing] | [What they miss or get wrong] |
| [Competitor type or specific source] | [Core claim or framing] | [What they miss or get wrong] |

### The Dominant Narrative

[1–2 sentences: What is the "received wisdom" on this topic that most content repeats?]

### The Gap Olytic Can Own

[1–2 sentences: What is NOT being said — or what is being said in a generic way that Olytic can say with specificity and earned authority?]

### Olytic's Differentiation Angle

**The contrarian position:** [The specific claim Olytic can make that no one else is making — or that most people are getting backwards]

**Why Olytic can own it:** [The specific reason our background (Salesforce/RevOps experience, O/G/O framework, embedded model) makes this claim credible]

**Headline that captures it:** [A working headline that reflects this angle]

### ICP Resonance Check

Does this angle address an ICP pain point (20–200 person B2B company, CEO/COO, trying to act on AI, doesn't know where to start)?
- **Pain addressed:** [Yes / Partially / No — with explanation]
- **Emotional trigger:** [The specific feeling this content should create: clarity, urgency, relief, vindication]

### Recommended Content Format

[Blog post / LinkedIn post series / GEO long-form page / Landing page] — with brief rationale

---

Ask if the user wants to proceed to a content brief (`/content-brief`) or directly to drafting.
