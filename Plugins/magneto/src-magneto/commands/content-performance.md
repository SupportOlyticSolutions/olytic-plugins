---
description: Analyze content performance using GA4 data
argument-hint: '[page-path or "overview"]'
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


Analyze content performance for Olytic Solutions using GA4 analytics data.

**GA4 Property ID:** 525690219

Steps:
1. If `$ARGUMENTS` is a specific page path, analyze that page's performance
2. If `$ARGUMENTS` is "overview" or empty, provide a high-level content performance summary
3. Connect findings back to the three strategic purposes:
   - **Credibility:** Is this content building trust with the ICP?
   - **Visibility:** Is this content being found through search?
   - **Conversion:** Is this content driving conversations?

4. Present findings in a structured report:

## Content Performance Report

### Traffic Summary
| Page | Sessions | Avg. Engagement Time | Bounce Rate |
|------|----------|---------------------|-------------|
| [page] | [number] | [time] | [rate] |

### Key Insights
- [What's working and why]
- [What's underperforming and why]
- [Opportunities based on search queries]

### Recommendations
| Action | Page | Rationale | Priority |
|--------|------|-----------|----------|
| [Create/Update/Optimize] | [page] | [why] | [High/Medium/Low] |

5. Always tie recommendations back to the content strategy framework (content pillars, ICP journey stage, differentiation potential).
