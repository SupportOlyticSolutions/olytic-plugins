---
name: user-experience
description: >
  Use this skill for client experience and UI design: "design the client-facing dashboard", "what should the data platform UI look like", "how do we onboard clients to the platform", "design the experience for clients accessing their data", "what flows should we include", "UX for the analytics platform", or when planning client-facing UI/UX, dashboard architecture, onboarding flows, and the customer experience that builds trust in the data platform product.
version: 0.1.0
---

# User Experience Design for the Data Platform Product

This skill provides guidance on designing the client-facing experience of Olytic's data platform — how clients interact with, access, and understand the data being collected about their plugins.

## Strategic Context

Before designing any client-facing experience, consider:

- **Trust through transparency.** Clients must understand exactly what data is being collected, why, and how it will be used. The UI is your primary trust-building tool.
- **Onboarding is differentiation.** How quickly and smoothly a client gets set up determines whether they stay engaged with the platform. The onboarding flow is part of the product.
- **The dashboard is a sales tool.** When a prospective data buyer looks at your aggregated insights, they decide whether to license the data. Design dashboards that showcase the value of the platform.
- **Usability ≠ complexity.** Clients care about actionable insights and clear data, not technical sophistication. Simplicity is a feature.
- **Localization matters.** Design for different user roles: the CTO who set up the connection, the marketer who uses plugins and sees outcomes, the exec who reads the quarterly report.

## Core Design Principles

### 1. Transparency-First Onboarding

Clients must explicitly consent at every stage and understand what they're enabling.

**Recommended onboarding flow:**

| Stage | What Happens | User Action | Why It Matters |
|-------|--------------|-------------|----------------|
| 1. Data overview | "Here's what we collect and why" | Review infographic of data flow | Client understands scope before committing |
| 2. Consent by category | Granular consent for different data types | Opt in to each category separately | Client controls what's shared |
| 3. CRM linkage setup | Instructions to connect CRM for outcome attribution | Paste API key or OAuth | Client decides if outcomes can be linked to their business data |
| 4. Integration testing | "Send a test event and verify it arrives" | Trigger a test from a deployed plugin | Client sees the actual data being captured |
| 5. Access & security | Set user roles, IP allowlists, data download settings | Configure admin/viewer permissions | Client feels in control of data security |
| 6. Success confirmation | Summary of setup + link to first report | Review one dashboard showing their data | Client sees immediate value |

**Design principle:** Every step answers one question. Don't dump all settings on one page.

### 2. Role-Based Dashboard Architecture

Different personas need different information from the same data.

**CTO / Platform Lead:**
- Health dashboard: plugin connections status, data freshness, integration issues
- Data schema explorer: tables, fields, sample rows, data types
- Governance controls: consent settings, anonymization status, opt-outs
- Audit log: who accessed what data, when, for how long

**Marketer / Content Creator:**
- Performance dashboard: which of my plugins drove the most outcomes?
- Outcome breakdown: content created, campaigns launched, speed improvements
- Sentiment trends: "user feedback is increasingly positive" or "this plugin needs tuning"
- Recommendations feed: "the Optimizer suggests adding this capability"

**Executive / VP:**
- Business impact dashboard: time saved, revenue impact, content velocity
- Competitive positioning: "we're in the top quartile for adoption in our industry"
- ROI calculation: "implementation cost vs. business outcomes enabled"
- Quarterly report: trends, benchmarks, recommendations

**Design principle:** Same underlying data, different views. One API, multiple interfaces.

### 3. The Insight Hierarchy

Not all dashboards are created equal. Structure information by value and urgency.

**Tier 1 (always visible):**
- Key metric: "This plugin has driven 127 outcomes this month"
- Sentiment: "User feedback is 82% positive"
- Status: "All systems operating normally"

**Tier 2 (click to drill down):**
- Outcome breakdown by type (content created, proposals sent, deals progressed)
- Usage patterns (adoption trend, feature usage, day-of-week patterns)
- Segment comparison ("You're outperforming peers in your industry")

**Tier 3 (for deep analysis):**
- Raw data export (CSV of all activity, all outcomes)
- Custom report builder (query any combination of metrics)
- Historical trend analysis (multi-month comparisons)

**Design principle:** Show insight at a glance. Enable exploration on demand. Never default to data overload.

### 4. Outcome Attribution UI

The most valuable part of the platform is connecting activity to outcomes. Make it visible.

**Sankey diagram approach:**
- Left column: plugin invocations (stacked by type)
- Right column: business outcomes (stacked by type)
- Center: flows connecting them (user asked plugin X → outcome Y happened)
- Hover state: show latency (how long between activity and outcome)

**Alternative: outcome source analysis:**
- List outcomes in the time period
- For each outcome, show "enabled by these activities"
- Confidence score for the attribution

**Design principle:** Make the connection between activity and impact obvious and credible.

### 5. Benchmarking & Market Position

Clients want to know how they compare to peers. This is also a powerful feedback mechanism for the Optimizer.

**Benchmarking dashboard (unlocks at 15+ managed clients):**
- Segment selector: filter to companies like yours (same industry, similar size)
- Metric comparison: "Your outcome rate is 14% — peers average 11%"
- Trend comparison: "Your adoption trend is 23% month-over-month — peers average 18%"
- Feature adoption: "You use 6 of 10 available features — peers average 4.2"

**Design principle:** Benchmark only against true peers (industry, size, stage). Avoid demoralizing comparisons.

### 6. Notification & Alert System

Clients shouldn't have to log in daily to stay informed. Push key updates.

**Recommended alerts:**
- Weekly digest: "You had 312 plugin invocations, 47 outcomes, 89% positive sentiment"
- Anomalies: "Your plugin usage dropped 40% this week — investigate?"
- Recommendations: "The Optimizer recommends adding capability X (predicted +15% outcome rate)"
- New segments: "A new buyer segment is showing interest in your plugin type"

**Design principle:** Alerts drive engagement. Default to weekly frequency (not daily noise). Make unsubscribe easy.

## Critical UX Decisions

### Decision 1: Real-Time vs. Batch Data

**Option A: Real-time dashboards** — data updates instantly as events come in
- **Pros:** Feels current, supports exploration
- **Cons:** Higher platform cost, requires streaming infrastructure

**Option B: Daily batch updates** — dashboards refresh overnight
- **Pros:** Simpler, cheaper, no latency surprises
- **Cons:** Feels slightly stale, less intuitive for troubleshooting

**Recommendation for MVP:** Batch updates daily at 6am UTC. Revisit to real-time after launch if demand justifies the infrastructure.

### Decision 2: Self-Service vs. Managed Reporting

**Option A: Self-service analytics** — clients build custom reports, export CSVs, explore freely
- **Pros:** Empowers clients, reduces support burden
- **Cons:** Requires building a query builder, supporting SQL knowledge

**Option B: Managed reporting** — Olytic creates canned reports, clients receive them on schedule
- **Pros:** Higher-quality output, no support issues
- **Cons:** Less flexible, doesn't scale to custom requests

**Recommendation for MVP:** Start with managed reporting (5–10 standard reports). Offer self-service data download. Evolve to a query builder after learning what clients actually ask for.

### Decision 3: Multi-Tenant vs. White-Label

**Option A: Multi-tenant dashboard** — all clients see the same interface, branded as "Olytic Data Platform"
- **Pros:** Easier to build, maintain, and update
- **Cons:** Less control for premium clients

**Option B: White-label capability** — clients can customize dashboard branding
- **Pros:** Perceived value, enables white-label resale
- **Cons:** 2x the design/engineering work

**Recommendation for MVP:** Multi-tenant only. White-label is a future premium feature.

## Interaction Patterns to Avoid

- **Data overload on first load.** Clients should see 3–4 key metrics, not 47. Drilling down is fine; defaulting to complexity is not.
- **Technical jargon in UI.** Never show "event_id", "token_count", or "related_activity_ids" to a non-technical user. Translate to business language.
- **Misleading percentages.** "82% positive sentiment" means little without context. Always show sample size: "82% positive sentiment (based on 347 user comments)."
- **Unclear consent states.** Don't leave clients confused about what data they've opted into. Show a clear summary: "You're sharing: activity, outcomes, sentiment. Not sharing: CRM linkage."
- **Missing error states.** Design for failure (plugin connection drops, API quota exceeded). Don't leave the client wondering why data stopped updating.

## Accessibility & Design Standards

- **WCAG 2.1 AA compliance** — all dashboards must be usable by screen readers and keyboard navigation
- **Color-blind safe palettes** — use Tableau or ColorBrewer safe palettes
- **Mobile responsiveness** — design for tablet and phone; dashboards must work on any device
- **Dark mode support** — provide dark and light theme options
- **Page load performance** — aim for < 2 second dashboard load time

## Onboarding Checklist

Before launching a new client on the platform, verify:

- [ ] Client has reviewed and signed the data platform terms
- [ ] Client has completed consent flow and explicitly opted into data categories
- [ ] CRM linkage is configured (if desired by client)
- [ ] At least one test event has been collected and visible in dashboard
- [ ] Client has been assigned user roles (admin, viewer, analyst, etc.)
- [ ] Client has logged in and viewed their first dashboard
- [ ] Client has been shown how to download a data export
- [ ] Client has access to documentation and support contact
- [ ] Client has scheduled first quarterly review call

## Operating Principles

- **Discovery first:** Before designing any UI, interview 2–3 prospective users from each persona. Understand their mental models before making design assumptions.
- **Source of truth:** Once the UI design is finalized, it defines what the data must support. Build the platform to feed the UI you designed, not the other way around.
- **Atomic operations:** Make design changes incrementally. Don't redesign the entire dashboard at once.
- **Verify after writing:** Test designs with real users before engineering. Validate that they can complete key tasks (check sentiment, view outcomes, download data).
- **No hallucination:** If a UI assumes integration with a specific CRM or external system, confirm it's actually integrable before designing.

## Boundaries

This skill should NOT be used for:

- Designing Olytic's own internal tools (use other plugins for that)
- Engineering the backend that powers the dashboard (that's full-stack-engineering)
- Writing the code to implement the UI (UX design, not engineering)
- Designing the Optimizer plugin or other internal Olytic plugins
- Creating marketing collateral or pitch decks (those use different UX principles)

If a request falls outside these boundaries, explain why and suggest the appropriate alternative.

## References

For complementary guidance:
- **Data security:** See the security skill
- **Consent & privacy:** See the data-privacy skill
- **Outcome metrics:** See the product-management skill for commercial framing
- **Data structure:** See the data-modeling skill for schema design that feeds the dashboard

---

Telemetry: This skill logs all invocations via plugin-telemetry.
