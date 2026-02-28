---
name: plugin-discovery
description: >
  Use this skill when the user wants to "create a plugin", "build a plugin",
  "design a plugin", "start a new plugin", "plan a plugin", or needs to go through
  the discovery process for gathering requirements before generating a plugin.
  This skill drives a structured 7-question discovery flow that adapts dynamically
  based on the user's answers. Works for both Olytic internal plugins and client-facing plugins.
version: 0.1.0
---

# Plugin Discovery Protocol

Walk users through a structured discovery conversation to gather everything needed to generate a complete plugin. Ask one question at a time. Use AskUserQuestion where appropriate, but allow free-text answers for open-ended questions.

**Tone:** Plain language. No jargon. Frame everything in terms of what the plugin will do for people, not how files are structured.

## Agentic Protocols for Discovery

- **Discovery first:** Before starting questions, check if a plugin with the intended name already exists. Use Glob/search to map the environment. Don't recreate what's already built.
- **Source of truth:** Store discovery answers as structured data. This data takes precedence over conversational memory. If the user contradicts an earlier answer, update the stored data and confirm the change.
- **No hallucination:** If the user references an integration, repo, or property ID, note it as-given. Do NOT verify or assume it's correct — flag as "user-provided, unverified" in the summary. The verification gate happens during generation.
- **No redundancy:** Don't repeat back long answers verbatim. Summarize, confirm, and move on. Present the full summary only once at the end.

## The 7 Questions

### Question 1: Plugin Identity

**Ask:** "What should this plugin be called, and what's its core purpose? What problem does it solve?"

**Why it matters:** The name and purpose drive every downstream decision — what components to build, what integrations to include, who uses it. A clear purpose prevents scope creep.

**Listen for:**
- A working name (will be converted to kebab-case)
- The primary problem it solves
- Whether it's for Olytic internal use, a specific client, or both

**Store:**
- `plugin_name` — working name
- `plugin_purpose` — 1-2 sentence purpose statement
- `plugin_audience` — "olytic-internal", "client", or "both"

**Examples to offer if the user is stuck:**
- "A plugin that enforces our proposal writing standards"
- "A plugin that helps our sales team prepare for discovery calls"
- "A plugin that manages client onboarding documentation"

---

### Question 2: Users & Key Functions

**Ask:** "Who would use this plugin? What are the 3-5 key things they'd use it for?"

**Why it matters:** This determines which component types to generate (skills for knowledge, commands for actions, agents for complex workflows) and how to write trigger descriptions.

**Listen for:**
- Role/persona of the primary user (e.g., "content marketer", "sales rep", "delivery consultant")
- Specific actions they'd take (e.g., "draft proposals", "review contracts", "analyze metrics")
- Whether they're technical or non-technical

**Store:**
- `user_profile` — who uses it and their context
- `key_functions` — list of 3-5 primary use cases
- `user_technical_level` — "technical", "non-technical", or "mixed"

**Follow-up if vague:** "Can you walk me through a typical day for this person? When would they reach for this plugin?"

---

### Question 3: Strategic Questions

**Ask:** "When someone uses this plugin, what are the important questions they should be asking themselves? These are the 'am I thinking about this the right way?' questions."

**Why it matters:** These become the guiding principles embedded in skills and agents. They prevent the plugin from being used mechanically without judgment.

**Listen for:**
- Decision-making questions (e.g., "Is this the right audience for this content?")
- Quality checks (e.g., "Does this proposal address their actual pain point?")
- Strategic alignment (e.g., "Does this support our current quarterly goals?")

**Store:**
- `strategic_questions` — list of 3-6 questions

**Examples by domain if user needs help:**

*Content creation:*
- "Does this build credibility, visibility, or conversion?"
- "Would a competitor say the same thing?"
- "Does this speak to the ICP's actual pain?"

*Sales enablement:*
- "Do I understand this prospect's real problem?"
- "Am I leading with outcomes or features?"
- "Is this the right engagement model for their stage?"

*Operations:*
- "Is this process repeatable or a one-off?"
- "What breaks if this scales 10x?"
- "Who owns this after I hand it off?"

*Client delivery:*
- "Does the client understand what they're getting?"
- "Are we building something they can maintain?"
- "Does this align with the SOW?"

---

### Question 4: Constraints & Boundaries

**Ask:** "What should this plugin absolutely NOT be used for? Any hard constraints or guardrails?"

**Why it matters:** Constraints prevent misuse and scope creep. They also feed directly into the telemetry system — the plugin will flag when someone tries to use it outside these boundaries.

**Listen for:**
- Out-of-scope use cases
- Compliance or legal boundaries
- Quality thresholds (e.g., "never publish without human review")
- Tool restrictions (e.g., "never access production databases")

**Store:**
- `constraints` — list of hard boundaries
- `out_of_scope` — things the plugin should explicitly refuse or redirect

**Prompt if the user says "nothing comes to mind":** "Think about the worst way someone could misuse this. What would make you cringe?"

---

### Question 5: External Integrations (DYNAMIC)

**Ask:** "What external systems should this plugin connect to?"

**Why it matters:** Integrations determine the .mcp.json configuration and which MCP tools are available to commands and agents.

**BRANCHING LOGIC — Suggest integrations based on Q1 and Q2 answers:**

*If purpose involves content/marketing:*
- GitHub (content repos)
- Google Analytics / GA4
- WordPress / CMS
- Social media platforms

*If purpose involves sales:*
- Salesforce
- HubSpot
- LinkedIn
- Email platforms

*If purpose involves operations/delivery:*
- GitHub (code repos)
- Jira / Linear / Asana
- Slack / Teams
- Google Workspace

*If purpose involves analytics/reporting:*
- Google Analytics / GA4
- Salesforce reports
- Snowflake / BigQuery
- Tableau / Looker

*Always offer:*
- GitHub (most common)
- "None — this plugin works standalone"
- "Something else" (free text)

**Store:**
- `integrations` — list of selected systems
- `integration_details` — any specifics (repo names, property IDs, workspace URLs)

**Follow-up for each selected integration:** "Any specifics? For example, a GitHub repo name, a GA4 property ID, or an API endpoint?"

---

### Question 6: Success Metrics

**Ask:** "How would you know this plugin is actually working? What business metrics would improve if this plugin does its job well?"

**Why it matters:** Metrics connect the plugin to business outcomes. They inform the telemetry system and give users a way to evaluate whether the plugin is earning its keep.

**Listen for:**
- Quantitative metrics (e.g., "page visits", "conversion rate", "deal velocity")
- Qualitative metrics (e.g., "proposal quality scores", "brand compliance rate")
- Time-based metrics (e.g., "time to first draft", "review cycle time")

**Store:**
- `success_metrics` — list of 2-5 metrics with descriptions

**Examples by domain:**

*Content:* Page visits, form conversions, time on page, organic traffic growth, brand compliance score
*Sales:* Pipeline velocity, win rate, proposal acceptance rate, time to proposal
*Operations:* Cycle time, error rate, manual intervention rate, throughput
*Delivery:* Client satisfaction score, deliverable acceptance rate, scope adherence

---

### Question 7: Data Sources

**Ask:** "Where does the data live to actually measure those metrics? What systems or reports would you pull from?"

**Why it matters:** This determines whether the plugin can self-measure or whether it relies on external reporting. If data sources are accessible, the plugin can include performance analysis commands.

**Listen for:**
- Specific tools (e.g., "GA4", "Salesforce dashboards", "GitHub insights")
- Manual processes (e.g., "we track it in a spreadsheet")
- Gaps (e.g., "we don't measure this yet")

**Store:**
- `data_sources` — list of sources mapped to metrics from Q6
- `measurement_gaps` — metrics that don't have a data source yet

**If gaps exist, note them:** "Good to know. The plugin won't be able to auto-measure [gap metric] yet, but we'll build the structure so it's ready when you add that data source."

---

## After All 7 Questions

### Present the Discovery Summary

Format the collected answers as a structured summary:

```
## Plugin Discovery Summary

**Name:** [plugin_name]
**Purpose:** [plugin_purpose]
**Audience:** [plugin_audience]

**Users & Functions:**
- Profile: [user_profile]
- Key functions: [key_functions as bullet list]

**Strategic Questions:**
[strategic_questions as numbered list]

**Constraints:**
[constraints as bullet list]

**Integrations:**
[integrations as bullet list with details]

**Success Metrics:**
[success_metrics as bullet list]

**Data Sources:**
[data_sources mapped to metrics]
[measurement_gaps noted]
```

### Confirm Before Proceeding

Ask: "Does this capture everything? Anything you'd add, change, or remove before we start building?"

If the user wants changes, update the relevant answers and re-present.

Once confirmed, this discovery output feeds directly into the **plugin-generation** skill.
