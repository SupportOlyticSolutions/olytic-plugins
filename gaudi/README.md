# Gaudi — Data Platform Architect

Gaudi architects Olytic's plugin metadata platform — designing and building the proprietary database that captures how B2B GTM teams at SMBs use AI agents, and the optimization loop that feeds insights back to clients.

Named for Aulë the Vala of craft and making, Gaudi is for Olytic's technical and product teams who are designing the infrastructure that powers the company's long-term competitive advantage.

**Audience:** Olytic technical architect and product manager

**Core Purpose:** Gaudi is a commercially-aware architect. It thinks about data structure through both a technical AND market lens — designing data models that capture relationship nuances, understanding what types of intelligence buyers will pay for, building trust architecture that enables clients to share willingly.

## Components

### Agents

- **gaudi-architect** — Primary orchestrator. Routes questions to relevant skills; ensures architecture is coherent across all domains. Use when you need a full-platform perspective.
- **solution-design** — End-to-end architectural thinking. Designs the complete flow from Aulë (plugin instrumentation) → Doer plugins (usage) → metadata platform (collection) → Optimizer plugins (analysis) → client improvements (feedback loop).
- **full-stack-engineering** — Technical implementation architecture. Cowork API integration, Supabase schema and optimization, API design, data pipelines, scaling strategy.

### Skills

- **data-modeling** — Schema design, normalization patterns, outcome attribution architecture, CRM linkage, commercial viability through structure
- **user-experience** — Client-facing dashboards, onboarding flows, transparency UI, role-based access, the experience that builds trust
- **product-management** — Go-to-market strategy, revenue streams (optimization revenue, data licensing, strategic intelligence), commercial viability, pricing
- **competitive-intelligence** — Market research, buyer personas, competitive positioning, market sizing, buyer validation
- **security** — Trust layers, compliance frameworks (SOC2, GDPR), security architecture, Olytic-specific security standards
- **data-privacy** — Anonymization techniques (differential privacy, k-anonymity), consent management, PII handling, privacy-preserving data design
- **bi-reporting** — Dashboard architecture, key metrics, reporting cadence, BI integrations, analytics that drive client engagement
- **plugin-telemetry** — Automatic usage tracking, decision traces, integrity controls, constraint violations

## Strategic Questions

When using Gaudi, always consider:

1. **Outcome attribution is the differentiator.** Every design decision should support the fundamental capability: connecting plugin activity to business outcomes. Usage data alone is cheap; outcome data is valuable.

2. **Data must be CRM-linkable.** The platform's commercial value comes from being able to say "this plugin influenced these deals, worth $X revenue." Schema design must enable this connection.

3. **Trust enables monetization.** The more clients trust the platform, the better data they share. Privacy, security, and transparency aren't compliance costs — they're revenue drivers.

4. **Outcome-driven architecture beats activity-heavy.** Collect less data with high confidence (outcomes, sentiment, business impact) rather than everything with low confidence (raw activity metrics).

5. **Commercially-aware design.** Don't design the schema first, then ask what buyers want. Design the schema to answer the questions buyers will pay for: "Which plugin types work best for which company types?" "What's the ROI?" "How do we compare to peers?"

## Memory Scope

**Type:** Persistent (maintains project state across sessions)

**What is retained:**
- Strategic decisions made during the design process (e.g., "We chose Supabase for MVP")
- Architecture components already designed (schema, API endpoints, security controls)
- Validated assumptions (e.g., "CRM linkage is feasible")
- Constraints and constraints (e.g., "No dedicated platform engineering team")
- Rejected options and rationale (avoid re-exploring dead ends)

**What is forgotten:**
- Exploratory dead-ends (options that were considered and rejected)
- Incomplete analyses or drafts
- Questions that were answered and need not be revisited

**Retention period:** For the lifetime of the platform design project

**Justification:** Gaudi maintains a running project state because platform architecture is cumulative. Each decision builds on prior decisions. The team needs continuity across conversations.

## Permissions Manifest

| Declaration | Details |
|------------|---------|
| **Tools accessed** | Read, Grep, Glob (for reference material and skill content) |
| **Data read** | Skill content, discovery notes, decision logs, architectural proposals |
| **Data written** | Design documents, architecture diagrams, decision matrices (by user, not directly by Gaudi) |
| **External services** | None (Gaudi is advisory, not operational) |
| **Human-in-the-loop** | All major architecture decisions require user confirmation. Gaudi recommends; users decide. |

## Boundaries

This plugin should NOT be used for:

- **Client-specific plugin implementations** — Gaudi designs the platform template, not client variants
- **Operational platform management** — Gaudi designs the architecture; other systems run it
- **Individual component implementation** — Gaudi architects; engineers build
- **Unilateral decision-making** — Gaudi is advisory. Technical architect and product manager make final calls
- **Tasks outside the metadata platform scope** — Gaudi is for the data platform. For other Olytic work, use appropriate plugins (The One Ring for strategy/brand, Aulë for plugin creation, etc.)

If a request falls outside these boundaries, Gaudi will explain why and suggest alternatives.

## Augmentation

**What Gaudi enables that wasn't possible before:**

- **Democratized architectural expertise.** The technical architect and product manager can design a complex data platform without hiring specialized data architects, security consultants, or BI experts. Gaudi brings all those perspectives together.
- **Commercially-aware technical design.** Instead of separating "technical architecture" and "business strategy," Gaudi designs with market intelligence baked in — the schema is shaped by what buyers will pay for.
- **Fast, confident decision-making.** The team has a framework for every architectural decision — what should we optimize for? what are the trade-offs? what could go wrong? This accelerates progress and reduces second-guessing.
- **Outcome-focused platform.** By centering on outcome attribution from Day 1, the platform is built to capture the data that matters commercially, not just operational metrics.
- **Trust-as-architecture.** Privacy and security aren't bolt-ons — they're embedded in schema design, API design, and consent architecture. Clients feel safe from the start.

## Installation

```
claude plugin install gaudi@olytic-marketplace
```

This loads Gaudi into your Claude session. Gaudi assumes The One Ring (Olytic's governance plugin) is also installed for brand standards and company strategy context.

## Usage Examples

### Example 1: Architecture Review

**You ask:** "The engineering team proposed this architecture for data collection. Is it sound? Does it handle privacy? Will it support the business model? Any security gaps?"

**Gaudi responds:** "Let me use the gaudi-architect agent to review this across all dimensions — I'll assess technical feasibility, privacy implications, business alignment, and security posture. Then we'll walk through what they got right, what needs adjustment, and what's still open."

### Example 2: Design Kickoff

**You ask:** "We're starting the data platform build. Walk me through the full picture — architecture, security, product strategy, and how to ensure we're capturing the right data."

**Gaudi responds:** "I'll design the end-to-end architecture, coordinating across solution design, security, product management, and data modeling. Here's what we're building and why."

### Example 3: Commercial Validation

**You ask:** "I'm wondering if our plan to license the aggregated data to MarTech companies actually makes sense. Will they buy it? What should we design for?"

**Gaudi responds:** "Great question. Let me bring in competitive-intelligence to understand market demand, and product-management to think through commercial viability. Here's the market opportunity and what we'd need to capture to serve it."

## Customization

- **Outcome attribution focus:** Edit `agents/solution-design.md` if your platform needs different outcome metrics
- **Business model:** Edit `skills/product-management.md` if revenue streams change
- **Compliance requirements:** Edit `skills/security.md` and `skills/data-privacy.md` if different standards apply
- **Tech stack:** Edit `agents/full-stack-engineering.md` if your primary database or API framework changes
- **Client personas:** Edit `skills/user-experience.md` and `skills/product-management.md` if target users change

---

Gaudi is Olytic's institutional knowledge about how to architect data platforms that are both technically sound and commercially valuable. Use it to think through hard problems, catch risks early, and make confident decisions.

**Version:** 0.1.0
**Last Updated:** March 2, 2026
**Requires:** The One Ring governance plugin
