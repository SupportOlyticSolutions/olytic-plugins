---
name: magneto-linkedin-content
description: >
  Use this skill to "write a LinkedIn post", "draft a post for LinkedIn",
  "create social content", "write something for LinkedIn", "draft a LinkedIn
  update", "post about this on LinkedIn", or "write a thought leadership post"
  for Olytic Solutions. Provides the full anatomy of effective LinkedIn posts —
  hooks, body structure, CTA patterns, voice rules, and angle selection aligned
  to Olytic's GTM strategy.
version: 0.1.0
---

## Step 0: Fetch Latest Reference Files (Always First)

Before doing anything else, fetch the latest files from the Olytic reference folder in Google Drive:

1. Use `mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_search` with `api_query: "'1Sv3EIQ0w4J3AGCFuxR0qxPtilESFRDGQ' in parents"` and `order_by: "modifiedTime desc"` to list all files in the folder.
2. For each file returned, fetch its full contents using `mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_fetch` with the file's `uri` as the document ID. All files in this folder are Google Docs and are fully readable this way.
3. Read and internalize the fetched documents. These files are the **source of truth** — they supersede any information baked into this skill for topics they cover (brand standards, strategy, positioning, ICP, competitive landscape, etc.).
4. If the folder is empty or inaccessible, continue with the information in this skill and note to the user that the Drive reference files could not be loaded.

Do not skip this step. Do not announce the fetch to the user beyond a brief "Checking your latest reference files…" if needed.

---


# LinkedIn Content — Olytic Solutions

Use this skill for all LinkedIn short-form content. Brand voice rules from The One Ring's `olytic-brand-standards` apply fully — load that skill too. For a complete drafting workflow with three post options, use the `/linkedin-post` command.

---

## Why LinkedIn Is the Primary Channel

The GTM strategy designates LinkedIn organic as the primary TOFU channel. The reasons:

- The ICP (CEO/COO, 20–200 person B2B company) is active on LinkedIn, not Twitter/X or newsletters
- Short-form, opinionated posts outperform paid LinkedIn at the current budget ($500/mo threshold is Google Ads)
- Posts drive traffic to the AI Strategy Architect assessment tool — the centerpiece MOFU asset
- Consistency compounds: 4–5 posts/week, week over week, builds recognition before any case studies exist

LinkedIn posts are not a brand-awareness play. They are a **trust-building and traffic-driving** play. Every post should make the reader think "this person has actually done this work."

---

## Post Anatomy

Every LinkedIn post has four components:

### 1. The Hook (Line 1)

The entire post lives or dies on the first line. LinkedIn shows roughly 2–3 lines before "see more" — the hook has to earn the click. It appears alone, stacked above the fold.

**Hook formulas that work for Olytic's voice:**

| Formula | Example |
|---------|---------|
| **The blunt take** | "Most AI strategies I see are just a list of tools. That's not a strategy." |
| **The counterintuitive** | "Hiring a Head of AI is a trap for companies under $50M." |
| **The diagnosis** | "Your AI pilot didn't fail because of the technology." |
| **The number** | "3 reasons your AI implementation is already off the rails." |
| **The question** | "What does a $20M company actually do with AI — before spending a dollar?" |
| **The stakes** | "Companies that don't solve this in the next 18 months won't catch up." |

Rules:
- One sentence, maximum two
- No hedge words ("might", "could", "perhaps")
- No setup — land the point immediately
- If it's not a little uncomfortable to post, it's not opinionated enough

### 2. The Body (Lines 2–10)

After the hook earns the click, the body delivers the argument. Each paragraph is one to three sentences. No walls of text.

**Body structures that work:**

**The Diagnosis + Fix:**
```
[Hook: name the problem]

[Paragraph 1: why it happens — the root cause, not the symptom]

[Paragraph 2: what most people try instead — and why it fails]

[Paragraph 3: what actually works — specific, not generic]
```

**The Numbered List (use sparingly — when each point genuinely stands alone):**
```
[Hook]

Here's what we consistently see:

1. [Specific observation]
2. [Specific observation]
3. [Specific observation]

[Landing line that ties the list together]
```

**The Framework Snippet (for O/G/O and methodology content):**
```
[Hook: state the problem the framework solves]

[Brief explanation of the framework in plain language — no jargon]

[One concrete example of how it applies]

[Why this matters to the ICP]
```

### 3. The Landing Line

The last substantive line before the CTA. Should feel like the punchline — the one sentence that makes the whole post worth reading. Often the most direct statement of the thesis.

Examples:
- "The technology changed. The discipline didn't."
- "You don't have an AI problem. You have a systems problem."
- "The window for this is 12–18 months. Then it closes."

### 4. The CTA

Always the final line. Soft, never pushy. Options:

- Link to the assessment tool: "If this resonates, our AI Strategy Architect takes 10 minutes and gives you a personalized readiness score: [link]"
- Question to drive comments: "What's the biggest blocker you've hit trying to implement AI in your org?"
- Follow-up offer: "If you're figuring this out right now, happy to talk through it — DM me."

Never: "CLICK HERE TO SCHEDULE A DEMO" or any hard-sell variant.

---

## Voice Checklist for LinkedIn

Before posting, verify:

- [ ] Hook is specific and takes a position — not a question that could apply to any company
- [ ] No line is longer than 3 sentences
- [ ] No hollow words: "exciting", "innovative", "game-changing", "rapidly evolving"
- [ ] No emojis
- [ ] The post reads like it came from someone who has done this work — not a content marketer
- [ ] There is a named concept, specific number, or real-world observation somewhere in the body
- [ ] The CTA asks for something reasonable — not a sales commitment

---

## Post Themes for the Current Phase

Four recurring angles aligned to the Zero Case Study Playbook:

| Theme | Example Hook | Goal |
|-------|-------------|------|
| **AI pilot failure** | "Your AI pilot failed because nobody asked the revenue question first." | Names the ICP's frustration; drives assessment tool clicks |
| **Hiring myths** | "The 'Head of AI' role is a trap for companies under $50M. Here's what to do instead." | Addresses the buy-vs-build objection |
| **Tool vs. system** | "Salesforce Agentforce is not an AI strategy. It's a feature." | Positions vs. tool-first thinking |
| **O/G/O framework** | "There are three jobs in any AI system. Most companies only fill one." | Introduces the methodology; builds IP credibility |

Rotate across themes. The ICP should see variety — diagnosis, framework, counterintuitive take, stakes — not the same angle every week.

### Claude OS Post Angle Archetypes

Beyond the core themes above, these three archetypes position Olytic's Claude OS philosophy and should be woven into the weekly post rotation:

#### 1. The Salesforce Analogy

**Core insight:** Unified Salesforce suite created exponential value in the early 2000s. Unified Claude OS does the same in 2026 for knowledge work. This is historical precedent, not futurism.

**Hook patterns:**
- "Salesforce unified CRM, sales, and service in 2003. They won. Fragmented CRM point tools lost. This is happening to AI right now."
- "Everyone stacked CRM point tools before Salesforce. The winners unified. Same pattern with AI in 2026."
- "You don't build revenue operations with 5 separate tools. You build it with Salesforce. Same logic applies to AI systems."

**Body structure:**
- Opening: name the historical parallel (Salesforce early 2000s vs. AI 2026)
- Middle: why unified won in that era (single source of truth, compounding improvements, alignment)
- Application: why the same principle applies to AI systems now
- Landing: position Olytic as the company building the unified suite

**Why this works:**
- ICP decision-makers often have Salesforce experience
- The analogy is intellectually credible and specific
- It positions unified systems as a proven model, not a novel idea
- It reframes the conversation from "AI tools" to "AI infrastructure"

**Example post structure:**
```
Hook: "Salesforce unified CRM in 2003. Every competitor who stayed fragmented is gone. Same thing is happening to AI in 2026."

Paragraph 1: Why unified won in enterprise software — single source of truth, one feedback loop, compound improvements.

Paragraph 2: The AI reality now — most companies are stacking point tools. ChatGPT + this + that. Same fragmentation Salesforce solved.

Paragraph 3: What actually wins — one system, one governance layer, one feedback loop. Alignment that compounds automatically.

Landing: "The unified suite always beats the point solution stack. That's not changing with AI."

CTA: "If you're thinking about AI infrastructure for your team, the assessment takes 10 minutes: [link]"
```

#### 2. The Hats Framework

**Core insight:** Every business role is a "hat" — content strategist, GEO specialist, revenue ops expert. Olytic plugins = the platonic ideal of each hat, working in one operating system. You can't hire the perfect strategist; you can build one.

**Hook patterns:**
- "Every business needs a content strategist. You can hire one ($150K+) or build one inside your AI system. One costs money. One compounds value."
- "The platonic ideal content strategist: always available, never tired, learns your voice, improves weekly. That's not a hiring problem. That's a plugin problem."
- "You can't hire the perfect [GEO specialist / revenue ops person / researcher]. But you can build their ideal version inside a unified AI operating system."

**Body structure:**
- Opening: name the specific "hat" (content strategist, GEO specialist, whatever)
- Middle: why hiring that role is expensive, slow, and fragile
- Middle: alternative — build the platonic ideal inside a unified system (never tired, always improving, knows the company)
- Application: concrete example from that domain
- Landing: why this is infrastructure, not automation

**Why this works:**
- Reframes AI from "tool adoption" to "capabilities you can build"
- Speaks directly to resource-constrained SMBs
- Makes the philosophical leap from "AI should help us" to "AI can be the role"
- Positions plugins as roles, not features

**Example post structure:**
```
Hook: "You can't hire the perfect content strategist. But you can build one inside your AI system."

Paragraph 1: What perfect looks like — always available, knows your voice, improves weekly, never gets bored or defensive about feedback.

Paragraph 2: Why hiring fails — good people are expensive, slow to onboard, and leave. You're betting $150K+ on someone.

Paragraph 3: The alternative — one plugin, one unified system, one voice. Operates continuously. Improves based on feedback. Stays.

Landing: "The next decade of business is building the roles you can't hire and the people you can't afford."

CTA: "If this resonates, our assessment scores your team against this kind of thinking: [link]"
```

#### 3. The Alignment Dividend

**Core insight:** Every tool you add is another source of truth and another place to fix fragmentation. A unified system with shared governance (The One Ring) enforces alignment perpetually. Marketing and sales always misalign — until they operate from one source.

**Hook patterns:**
- "Your marketing says one thing. Your sales team says another. Your content is different again. The company is fragmented. Not because people are lazy. Because every tool is its own source of truth."
- "Brand drift across channels is solvable. Marketing/sales misalignment is solvable. Plugin inconsistency is solvable. Not with more alignment meetings. With one governance layer."
- "You can't fix organizational alignment with spreadsheets and Slack. You fix it with a unified system where alignment is structural."

**Body structure:**
- Opening: name the symptom (brand drift, messaging inconsistency, strategy fragmentation)
- Root cause: each tool is its own source of truth; nobody can enforce alignment across 5 systems
- Solution: unified governance layer (One Ring) that every component respects
- Example: how this works in practice (e.g., Magneto and sales messaging enforcing the same positioning)
- Landing: why compounding alignment beats yearly realignment meetings

**Why this works:**
- Addresses a real, daily pain (everyone says things differently)
- Positions alignment as a structural problem, not a people problem
- Makes the case for unified systems as governance, not just efficiency
- Speaks to CTOs, COOs, and marketing leaders who manage multiple teams

**Example post structure:**
```
Hook: "Your marketing says one thing. Your sales team says another. Your content is different. This isn't lazy. It's architecture."

Paragraph 1: The problem — when each tool is independent, each becomes its own source of truth.

Paragraph 2: What most companies do — more meetings, more alignment decks, more spreadsheets. It doesn't work because the structure is fragmented.

Paragraph 3: What actually works — one governance foundation that every plugin respects. Alignment becomes automatic, not aspirational.

Paragraph 4: The result — week over week, decisions compound. Messaging stays consistent. Brand stays clean. Competitive positioning sharpens automatically.

Landing: "You don't fix alignment with process. You fix it with architecture."

CTA: "Curious how this actually works? The O/G/O framework page has a concrete example: [link]"
```

---

## Integration Strategy

Weave these three Claude OS archetypes into the weekly post rotation:

- **Week 1-2:** Core problem themes (AI pilot failure, hiring myths, tool vs. system)
- **Week 3-4:** Claude OS angle (rotate: one Salesforce analogy post, one Hats Framework post, one Alignment Dividend post)
- **Week 5-6:** Framework and IP building (O/G/O snippet, methodology deepdive)
- Repeat

This keeps the feed varied while building philosophical thought leadership around the unified Claude OS positioning. The ICP should encounter the thesis from multiple angles — not repeated arguments, but different facets of the same core idea.

---

## What NOT to Post

- Long-form LinkedIn articles (not short-form, wrong format for the strategy)
- Reposts or commentary on other people's content without a strong original angle
- Product announcements without a problem-first frame
- Anything that reads like a press release
- Posts that require existing case studies to be credible (we don't have them yet — own that, don't fake it)

## Operating Principles

- **Discovery first:** Check existing posts and LinkedIn strategy before drafting. Don't repeat themes or angles.
- **Source of truth:** Brand voice from The One Ring takes precedence. Verify voice rules against `olytic-brand-standards`.
- **Atomic operations:** Edit specific posts or sections, not entire post archives.
- **Verify after writing:** Check every post against the voice checklist before considering it ready.
- **No hallucination:** If a post, theme, or competitor comparison doesn't exist, report "Not Found." Don't fabricate examples.
