---
description: Quick gut-check — does this output or decision align with Olytic's core values?
argument-hint: "[describe the decision or action, or paste content]"
allowed-tools: Read
---

Run a quick values alignment check on the provided content or decision.

Steps:

1. Load the `olytic-company-strategy` skill (Core Values are defined there)
2. Review the content or decision from `$ARGUMENTS` or the user's message
3. Check each core value and produce a one-line assessment:

| Value | Status | Rationale |
|-------|--------|-----------|
| Clarity over noise | ✓ Pass / ⚠ Flag | [one-line rationale] |
| Embedded partnership | ✓ Pass / ⚠ Flag | [one-line rationale] |
| Amplification, not automation | ✓ Pass / ⚠ Flag | [one-line rationale] |
| Systems thinking | ✓ Pass / ⚠ Flag | [one-line rationale] |
| Earned expertise | ✓ Pass / ⚠ Flag | [one-line rationale] |

4. For any flagged value, provide a specific and concrete suggestion for how to bring it into alignment.

Keep this fast. This is a gut-check, not a full audit. If the user wants a comprehensive cross-dimensional scan, recommend the `consistency-auditor` agent instead.
