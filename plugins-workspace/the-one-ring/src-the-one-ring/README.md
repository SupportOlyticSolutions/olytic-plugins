# The One Ring

Olytic Solutions governance plugin. Installed for all employees to ensure universal alignment across brand voice, company strategy, security, and people policies.

"One Ring to rule them all" — this is the foundational plugin that every other Olytic plugin assumes is present.

## What This Plugin Enables

Before The One Ring, governance happened in documents. People had to remember to check brand standards. Strategy changes were announced but not enforced. Security rules were known but not always followed. The One Ring makes institutional knowledge operational.

With this plugin, every Olytic team member and collaborator has instant access to:

- **Always-available brand standards** — write content, ask "is this on brand?", and get an authoritative audit in seconds. No digging through old docs.
- **Strategic alignment tools** — before making a decision or taking on a client engagement, check it against current strategy, OKRs, and values in real time.
- **Consistent policy enforcement** — HR policies, security rules, and data handling standards are built into how work gets done, not something people have to think about.
- **Governance auditing** — full cross-dimensional audits of proposals, decisions, and work products ensure everything serves Olytic's mission and protects client trust.
- **Structured onboarding** — new team members get a conversational walkthrough of what Olytic is, how it operates, and what's expected — instead of drowning in a folder of PDFs.

This transforms governance from "here's what the rules are" to "here's your co-pilot for staying aligned." It's the difference between a rulebook and a system.

## Components

### Skills

- **olytic-brand-standards** — Complete brand rulebook: voice, tone, messaging pillars, ICP definition, competitive positioning, design preferences. Referenced by all role-specific plugins.
- **olytic-company-strategy** — Vision, philosophy, current strategic priorities, engagement models, and business stage context.
- **olytic-security-policies** — Data classification, client data rules, AI tool usage policies, credential management, and communication security. *[Contains placeholders — update with actual policies.]*
- **olytic-hr-policies** — Culture principles, communication norms, work hours, PTO, onboarding. *[Contains placeholders — update with actual policies.]*

### Commands

- `/brand-check [content]` — Review any content against brand standards with a scored compliance report

### Agents

- **onboarding-guide** — Conversational walkthrough for new team members, collaborators, or returning employees. Covers strategy, values, brand voice, HR norms, and security policies with depth adjusted to role.
- **brand-compliance-reviewer** — Deep multi-dimensional audit of any content (pages, emails, proposals, support responses) against all brand standards.
- **consistency-auditor** — Full governance scan of any work product or decision across all five dimensions: brand voice, strategy alignment, core values, HR norms, and security standards.

## Memory Scope & State

The One Ring operates **fresh in each conversation** — it does not maintain session state or remember past decisions across interactions. This is intentional:

- **State freshness ensures accuracy.** Each governance check reads the current skills, strategy, and policies. If something changes, the next conversation reflects the update immediately.
- **No personalized memory.** The plugin doesn't retain who you are, what decisions you've made, or patterns from your past work. Each audit is independent.
- **Stateless = always aligned.** A team member can ask the same brand compliance question today and three months from now, and the answer will be consistent with whatever the current standards are.

If you need to reference a past decision or build context across conversations, save that context in your prompt.

## Installation

This plugin should be installed at the `managed` scope for all employees:

```
claude plugin install the-one-ring --scope managed
```

Users cannot disable a managed plugin. This ensures brand and policy alignment is always active.

## How Other Plugins Use This

Role-specific plugins (content-strategist, sales, engineering, consulting-delivery) assume The One Ring is installed. They reference the brand standards and company strategy skills automatically. This means:

- Brand voice is defined once, here, and applies everywhere
- Strategy updates propagate to all teams automatically
- Policy changes take effect across the entire organization

## The One Ring as the Governance Hat

In Olytic's Hats Framework, each plugin represents a specific job-to-be-done — a "hat" someone wears at work. **The One Ring is the governance hat**: the platonic ideal of a Chief Governance Officer, brand guardian, policy enforcer, and strategic alignment keeper.

The governance hat is not a reference library. It is the constitutional layer of the Claude OS. Every other hat — the content strategist hat, the sales enablement hat, the consulting delivery hat — derives its authority, brand voice, and strategic direction from The One Ring. When The One Ring's strategy or brand standards change, every dependent plugin immediately reflects the update. This is not eventual consistency. This is instant alignment.

**The alignment dividend.** In traditional organizations, this problem is perpetual: marketing positions the product one way, sales positions it another, support uses different language. Misalignment is expensive and historically hard to close permanently. The One Ring solves this by being the single source of truth that all plugins reference. When The One Ring's strategy skill is updated, Magneto's content strategy updates. When brand voice changes, every plugin that creates external-facing content reflects the change. The alignment dividend is not one-time. It is compounding — as strategy evolves, the update propagates through the entire Claude OS automatically.

**Why managed scope.** The One Ring is the ONLY plugin installed at `managed` scope — users cannot disable it. This is not a technical accident. Governance cannot be optional. If a team member could turn off brand standards or policy enforcement, the entire system falls apart. Managed scope ensures that The One Ring is always active, always authoritative, always the constitutional foundation the other hats rely on.

**The compounding loop.** The One Ring participates in the compounding loop of the Claude OS: as strategy and brand voice evolve, The One Ring's skills are updated, and those updates immediately propagate through every dependent plugin. This is the governance dimension of the Olytic framework: Launch → Operate → Optimize → Perpetuate. At the Optimize phase, The One Ring's skills are refreshed. At the Perpetuate phase, those updates compound through the entire system. This is how governance becomes structural rather than aspirational.

## Permissions & Transparency

### Tools Accessed

- **Read** — Reads governance skill files and reference documents
- **Glob** — Locates policy files and reference materials during audits
- **Grep** — Searches content for policy violations and brand standard compliance

### Data Read/Written

- **Reads:** Internal policy documents (brand standards, strategy, HR policies, security rules), user-provided content for review
- **Writes:** None — this plugin is read-only. Audit results and recommendations are presented to the user but never persisted.

### External Services

- None — The One Ring operates entirely within the plugin ecosystem.

### Human-in-the-Loop Checkpoints

- **All governance reviews are advisory.** The plugin provides audits, recommendations, and compliance scores, but humans retain full decision authority. No action is taken automatically based on a governance audit.
- **Security flags require escalation.** If a security audit detects credential exposure, data classification violations, or client data breaches, those findings must be escalated to company leadership immediately — they are not just recommendations.
- **Strategic decisions remain with leadership.** The consistency-auditor can flag whether something aligns with current strategy, but final decisions on strategic pivots, client fit, or engagement types rest with company leadership.

## Customization

- **Brand standards:** Edit `skills/brand-standards/SKILL.md` and its references
- **Strategy:** Edit `skills/company-strategy/SKILL.md` when priorities change
- **Security:** Replace placeholder content in `skills/security-policies/SKILL.md` with actual policies
- **HR:** Replace placeholder content in `skills/hr-policies/SKILL.md` with actual policies
- **Add new agents:** Create new agent files in `agents/` for domain-specific governance (e.g., a consulting-delivery governance auditor) and register them in `plugin.json`

## Operating Principles

- **Discovery first:** Before auditing, assess what exists. Understand the context and scope before applying governance.
- **Source of truth:** Current skills and policies in this plugin take precedence over conversational context.
- **Atomic operations:** Governance checks are focused on specific dimensions, not everything at once.
- **Verification gate:** Every audit produces findings and recommendations, but no actions are taken without human approval.
- **No hallucination:** If a policy or standard cannot be found in the loaded skills, report "Not Found" — never guess or improvise governance standards.
- **Permission gate:** Security and compliance findings are treated as escalations when they involve credential exposure or client data risk.
