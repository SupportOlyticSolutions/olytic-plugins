# The One Ring

Olytic Solutions governance plugin. Installed for all employees to ensure universal alignment across brand voice, company strategy, security, and people policies.

"One Ring to rule them all" — this is the foundational plugin that every other Olytic plugin assumes is present.

## Components

### Skills

- **olytic-brand-standards** — Complete brand rulebook: voice, tone, messaging pillars, ICP definition, competitive positioning, design preferences. Referenced by all role-specific plugins.
- **olytic-company-strategy** — Vision, philosophy, current strategic priorities, engagement models, and business stage context.
- **olytic-security-policies** — Data classification, client data rules, AI tool usage policies, credential management, and communication security. *[Contains placeholders — update with actual policies.]*
- **olytic-hr-policies** — Culture principles, communication norms, work hours, PTO, onboarding. *[Contains placeholders — update with actual policies.]*

### Commands

- `/brand-check [content]` — Review any content against brand standards with a scored compliance report

### Agents

- **brand-compliance-reviewer** — Deep multi-dimensional audit of any content (pages, emails, proposals, support responses) against all brand standards

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

## Customization

- **Brand standards:** Edit `skills/brand-standards/SKILL.md` and its references
- **Strategy:** Edit `skills/company-strategy/SKILL.md` when priorities change
- **Security:** Replace placeholder content in `skills/security-policies/SKILL.md` with actual policies
- **HR:** Replace placeholder content in `skills/hr-policies/SKILL.md` with actual policies
