---
description: Review any work product or decision for strategic alignment with Olytic's current stage and priorities
argument-hint: [file-path, URL, or describe the decision]
allowed-tools: Read, Grep
---

Review the provided content or decision against Olytic Solutions' company strategy.

Steps:

1. Load the `olytic-company-strategy` skill for context
2. Read the content from `$ARGUMENTS` (file path) or use the content / decision described by the user
3. Evaluate across three dimensions:

**Strategic Fit:**
- Does this serve Olytic's current stage (early GTM — win first client)?
- Does it advance one of the five strategic priorities: website/content, offering definition, first client acquisition, delivery framework, or internal tooling?
- Is the effort proportional to the current stage, or is this premature scaling?

**Message Alignment:**
- Does this differentiate Olytic as a systems firm (not consulting, not SaaS, not agency)?
- Does it reinforce embedded partnership over project-and-leave?
- Does it reflect the O/G/O architecture as our core differentiator?

**Values Alignment:**
- Does this reflect our core values: clarity over noise, embedded partnership, amplification not automation, systems thinking, earned expertise?
- Would we be proud to show this to a client at meeting #20?

4. Present findings as a scorecard:

| Dimension | Assessment | Notes |
|-----------|------------|-------|
| Strategic Fit | Aligned / Off-Track / Premature | [specific finding] |
| Message Alignment | Aligned / Needs Adjustment | [specific finding] |
| Values Alignment | Aligned / Needs Adjustment | [specific finding] |

5. For anything Off-Track, Premature, or Needs Adjustment: provide a specific recommendation or rewrite. Be direct — if something doesn't serve the strategy, say so.
