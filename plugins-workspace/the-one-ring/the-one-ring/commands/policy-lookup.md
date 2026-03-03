---
description: Look up the relevant HR or security policy for a specific situation
argument-hint: "[describe your situation or question]"
allowed-tools: Read, Grep
---

Answer a policy question by looking up Olytic's HR or security policies.

Steps:

1. Load both `olytic-hr-policies` and `olytic-security-policies` skills
2. Understand the situation from `$ARGUMENTS` or the user's message
3. Identify which policy domain is relevant: HR/people, security/data, or both
4. Find the specific applicable rule or guidance
5. Answer directly and concisely:

**Policy:** What the rule is

**Rationale:** Why it exists (one sentence)

**Source:** Which skill and section this comes from

**Action:** What the user should do in their specific situation

If no explicit policy covers the situation, say so clearly. Don't invent policy. Instead, recommend the user escalate to company leadership with a brief description of what they're deciding.
