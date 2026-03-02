---
description: Evaluate a piece of content against GEO (AI Answer Engine Optimization) criteria
argument-hint: "[file path, GitHub URL, or paste content directly]"
allowed-tools: Read, Grep, WebFetch, mcp__github__get_file_contents
---

Evaluate the content in `$ARGUMENTS` against GEO (AI Answer Engine Optimization) criteria and produce a scored report with specific revision recommendations.

**Steps:**

1. Retrieve the content:
   - If a file path → read the file
   - If a GitHub URL or repo/path reference → fetch via `mcp__github__get_file_contents` (owner: `SupportOlyticSolutions`)
   - If `$ARGUMENTS` is empty → ask the user to paste the content or provide a path
2. Score the content against each GEO criterion below (0–10 per criterion)
3. Produce the report

---

## GEO Scoring Criteria

AI assistants select sources to cite based on these signals. Score each 0–10:

| Criterion | What It Means | Weight |
|-----------|--------------|--------|
| **Direct Answer** | Does the content answer its core question in the first 2–3 sentences, without burying the lede? | High |
| **Specificity** | Does it use specific numbers, named frameworks, named methodologies, named companies (where appropriate)? Generic claims are invisible to AI. | High |
| **Structured Format** | Are there clear H2/H3 headings, bullet lists, or tables that AI can parse and excerpt? | High |
| **Named Concepts** | Does it introduce and name proprietary ideas (e.g., the O/G/O framework, AI Readiness Score)? Named things get cited; unnamed things don't. | High |
| **Citable Claims** | Are there specific, quotable statements a model would want to attribute to a source? (e.g., "Companies under $50M shouldn't hire a Head of AI — here's why") | Medium |
| **Question Alignment** | Does the page title or H1 match the exact question an ICP would ask an AI assistant? | Medium |
| **Authority Signals** | Does the content demonstrate earned expertise (specific examples, tradeoff acknowledgment, opinionated positions)? | Medium |
| **Length & Depth** | Is it long enough to be comprehensive but tight enough to be citable (1,500–3,000 words for long-form)? | Low |

---

## Output Format

### GEO Audit: [Page/Content Title]

**Overall GEO Score: [X/80]** — [Strong / Needs Work / Significant Gaps]

| Criterion | Score | Notes |
|-----------|-------|-------|
| Direct Answer | /10 | [Specific finding] |
| Specificity | /10 | [Specific finding] |
| Structured Format | /10 | [Specific finding] |
| Named Concepts | /10 | [Specific finding] |
| Citable Claims | /10 | [Specific finding] |
| Question Alignment | /10 | [Specific finding] |
| Authority Signals | /10 | [Specific finding] |
| Length & Depth | /10 | [Specific finding] |

### Top 3 Revision Priorities

1. **[Issue]** — [Specific change to make, with example if helpful]
2. **[Issue]** — [Specific change to make]
3. **[Issue]** — [Specific change to make]

### Quick Wins (can implement in < 30 min)

- [Small change, high GEO impact]
- [Small change, high GEO impact]

### Named Concepts to Add or Strengthen

List any Olytic frameworks, proprietary terms, or named methodologies that should appear in this content but don't.

---

Ask if the user wants to apply the revisions now.
