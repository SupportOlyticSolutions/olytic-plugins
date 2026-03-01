---
name: plugin-discovery
description: >
  Use this skill when the user wants to "create a plugin", "build a plugin",
  "design a plugin", "start a new plugin", "plan a plugin", or needs to go through
  the discovery process for gathering requirements before generating a plugin.
  This skill drives a structured 10-question discovery flow that adapts dynamically
  based on the user's answers. Works for both Olytic internal plugins and client-facing plugins.
version: 0.2.0
---

# Plugin Discovery Protocol

Walk users through a structured discovery conversation to gather everything needed to generate a complete plugin. Ask one question at a time. Use AskUserQuestion where appropriate, but allow free-text answers for open-ended questions.

**Tone:** Plain language. No jargon. Frame everything in terms of what the plugin will do for people, not how files are structured.

## Agentic Protocols for Discovery

- **Discovery first:** Before starting questions, check if a plugin with the intended name already exists. Use Glob/search to map the environment. Don't recreate what's already built.
- **Source of truth:** Store discovery answers as structured data. This data takes precedence over conversational memory. If the user contradicts an earlier answer, update the stored data and confirm the change.
- **No hallucination:** If the user references an integration, repo, or property ID, note it as-given. Do NOT verify or assume it's correct — flag as "user-provided, unverified" in the summary. The verification gate happens during generation.
- **No redundancy:** Don't repeat back long answers verbatim. Summarize, confirm, and move on. Present the full summary only once at the end.

## The 10 Questions

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

### Question 5: Memory Scope

**Ask:** "What context does this plugin need to remember? Should it retain information between sessions, or does it start fresh every time?"

**Why it matters:** Memory architecture is a first-class design decision, not an afterthought. Every piece of stored context is also a security surface — more persistent memory means more data to protect and govern. Plugins should declare their memory requirements upfront, with session-scoped (ephemeral) context as the default and persistent memory requiring explicit justification.

**Listen for:**
- Whether the plugin needs to remember anything between conversations
- What kind of context is needed within a session
- Whether it references large knowledge bases that need retrieval strategies
- Any data lifecycle requirements

**Store:**
- `memory_scope` — "ephemeral" (session-only, default), "persistent" (retained between sessions), or "retrieval" (needs RAG/search over large knowledge bases)
- `memory_details` — what specifically needs to be retained and for how long
- `memory_justification` — if persistent, why session-scoped isn't sufficient
- `data_lifecycle` — any purge or retention requirements

**BRANCHING LOGIC:**

*If memory_scope is "ephemeral":*
- Note: "Plugin will start fresh each session. No special memory architecture needed."
- This is the default and preferred option. Move on.

*If memory_scope is "persistent":*
- Follow up: "What specific information needs to persist? And how long should it be retained?"
- Note for generation: Plugin will need a persistent storage strategy and data lifecycle policy. Flag this for the integrity review in generation.

*If memory_scope is "retrieval":*
- Follow up: "Where does this knowledge live? How large is the corpus, and how fresh does it need to be?"
- Note for generation: Plugin will need retrieval configuration (what sources, what freshness, what fallback). This feeds into the integrations question.

**If the user isn't sure:** Default to "ephemeral" and note: "We'll start with session-scoped memory. If you find the plugin needs to remember things between conversations, we can add that later."

---

### Question 6: Workflow Context & Augmentation Test

**Ask:** "Walk me through the full workflow around what this plugin handles. What happens before and after? And here's the key question: what could someone do with this plugin that they genuinely can't do today?"

**Why it matters:** This is the most important question for ensuring the plugin delivers real productivity gains. Research shows that AI tools that simply speed up existing tasks often fail to improve overall productivity. The plugins that create genuine value are the ones that give people new capabilities — synthesizing information they couldn't process manually, maintaining consistency across operations that were previously fragmented, or connecting data sources that were siloed.

This question also prevents the "duct tape" trap — overlaying AI onto a workflow designed for humans without rethinking the workflow itself. By mapping the full workflow, we can identify where the plugin should reshape the process, not just accelerate one step within it.

**Listen for:**
- The full workflow before and after the target task
- Where the current bottlenecks or pain points are
- **The augmentation signal:** What new capability does this plugin create? If the answer is only "it does the same thing faster," probe deeper:
  - "If this plugin saved you 2 hours a week, what would you actually do with that time?"
  - "Is there something you'd like to do but can't because it takes too much time or expertise?"
  - "Could this plugin help you see patterns or connections you're currently missing?"
- Whether the workflow should be restructured (not just automated)
- Opportunities for compounding impact

**Store:**
- `workflow_before` — what happens before the plugin's target task
- `workflow_after` — what happens after
- `current_bottlenecks` — pain points in the current workflow
- `augmentation_signal` — what new capability this creates (not just "faster")
- `workflow_restructure` — if the workflow should change, how
- `compounding_opportunities` — where task gains could multiply at the workflow level

**If the augmentation signal is weak (only "faster"):**
Don't block the plugin, but flag it in the discovery summary: "This plugin primarily accelerates an existing task. Consider whether the plugin could also [suggestion based on workflow context]. The strongest plugins create capabilities that didn't previously exist."

**Suggest augmentation opportunities based on domain:**

*Content:* "Could this plugin help you maintain consistency across all content, spot gaps in your content strategy, or synthesize competitive intelligence you don't currently track?"
*Sales:* "Could this plugin help you identify patterns across deals, surface insights from past proposals, or give junior reps access to senior-level preparation?"
*Operations:* "Could this plugin connect systems that are currently siloed, or catch issues proactively instead of reactively?"
*Delivery:* "Could this plugin help you see patterns across engagements, or create reusable frameworks from one-off work?"

---

### Question 7: External Integrations (DYNAMIC)

**Ask:** "What external systems should this plugin connect to?"

**Why it matters:** Integrations determine the .mcp.json configuration and which MCP tools are available to commands and agents.

**BRANCHING LOGIC — Suggest integrations based on Q1, Q2, and Q5 answers:**

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

*If memory_scope from Q5 is "retrieval":*
- Suggest: "Based on your retrieval needs, you may also want document stores or search indices. Any specific systems?"

*Always offer:*
- GitHub (most common)
- "None — this plugin works standalone"
- "Something else" (free text)

**Store:**
- `integrations` — list of selected systems
- `integration_details` — any specifics (repo names, property IDs, workspace URLs)

**Follow-up for each selected integration:** "Any specifics? For example, a GitHub repo name, a GA4 property ID, or an API endpoint?"

---

### Question 8: Success Metrics

**Ask:** "How would you know this plugin is actually working? What business metrics would improve if this plugin does its job well?"

**Why it matters:** Metrics connect the plugin to business outcomes. They inform the telemetry system and give users a way to evaluate whether the plugin is earning its keep. Without measurable impact, a plugin can look busy without actually improving productivity.

**Listen for:**
- Quantitative metrics (e.g., "page visits", "conversion rate", "deal velocity")
- Qualitative metrics (e.g., "proposal quality scores", "brand compliance rate")
- Time-based metrics (e.g., "time to first draft", "review cycle time")
- **Augmentation metrics** (from Q6): new capability indicators that didn't exist before

**Store:**
- `success_metrics` — list of 2-5 metrics with descriptions

**Examples by domain:**

*Content:* Page visits, form conversions, time on page, organic traffic growth, brand compliance score, content consistency across channels
*Sales:* Pipeline velocity, win rate, proposal acceptance rate, time to proposal, preparation quality score
*Operations:* Cycle time, error rate, manual intervention rate, throughput, cross-system visibility
*Delivery:* Client satisfaction score, deliverable acceptance rate, scope adherence, framework reuse rate

---

### Question 9: Data Sources

**Ask:** "Where does the data live to actually measure those metrics? What systems or reports would you pull from?"

**Why it matters:** This determines whether the plugin can self-measure or whether it relies on external reporting. If data sources are accessible, the plugin can include performance analysis commands.

**Listen for:**
- Specific tools (e.g., "GA4", "Salesforce dashboards", "GitHub insights")
- Manual processes (e.g., "we track it in a spreadsheet")
- Gaps (e.g., "we don't measure this yet")

**Store:**
- `data_sources` — list of sources mapped to metrics from Q8
- `measurement_gaps` — metrics that don't have a data source yet

**If gaps exist, note them:** "Good to know. The plugin won't be able to auto-measure [gap metric] yet, but we'll build the structure so it's ready when you add that data source."

---

## After All 9 Core Questions

### Question 10: Natural Language Triggers

**Ask:** "What phrases would trigger this plugin in natural conversation? Think about what someone would actually say to Claude when they need it — for example, 'review this content', 'check my proposal', 'run the weekly report'. List 4-8 phrases for each skill or agent this plugin will have."

This question is non-negotiable. Every plugin must have explicit natural language triggers defined before generation begins. These become the `description` field in every skill and agent — they are how Claude knows when to load this plugin's capabilities.

If the user says "I don't know" or gives vague answers:
- Offer examples based on the key functions from Q2
- Ask: "If someone needed [key_function], what would they say to Claude?"
- Do not proceed to the summary until at least 4 concrete trigger phrases are defined per component

**Tone:** Keep it natural. Don't say "define trigger phrases for your skill frontmatter." Say "What would someone actually say to Claude when they need this?"

**Store:**
- `trigger_phrases` — mapped per planned component (skill or agent)

---

### Natural Language Hooks Gate

Before advancing to the summary, run this check:

1. Review the Q10 answers. For each planned component (skill or agent), confirm at least 4 specific trigger phrases were defined.
2. If any component has fewer than 4 phrases, or if all phrases are generic (e.g., "use this plugin", "help me"), stop and ask for more:
   - "For the [component-name] skill/agent, I need more specific phrases. What would someone say when they actually need [key_function]? Think about the exact words they'd use, not a description of the feature."
3. Do not proceed to the summary until every planned component has 4+ concrete, user-language trigger phrases.

**Why this matters:** These phrases are how Claude decides whether to load this plugin's capabilities. Vague or missing triggers mean the plugin will never activate in natural conversation — making it useless regardless of how well it's built.

---

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

**Memory Scope:**
- Type: [memory_scope]
- Details: [memory_details]
- Lifecycle: [data_lifecycle]

**Workflow Context:**
- Before: [workflow_before]
- After: [workflow_after]
- Bottlenecks: [current_bottlenecks]
- Augmentation signal: [augmentation_signal]
- Workflow changes: [workflow_restructure]
- Compounding opportunities: [compounding_opportunities]

**Integrations:**
[integrations as bullet list with details]

**Success Metrics:**
[success_metrics as bullet list]

**Data Sources:**
[data_sources mapped to metrics]
[measurement_gaps noted]

**Natural Language Triggers:**
[trigger_phrases mapped per component]
```

### Confirm Before Proceeding

Ask: "Does this capture everything? Anything you'd add, change, or remove before we start building?"

If the user wants changes, update the relevant answers and re-present.

Once confirmed, this discovery output feeds directly into the **plugin-generation** skill.
