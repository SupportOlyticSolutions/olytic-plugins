---
name: bi-reporting
description: >
  Use this skill for reporting and analytics design: "what should our dashboards show", "design the reporting structure", "what analytics do customers want to see", "how do we present outcomes to clients", "what metrics should we track", "design our reporting layer", "what KPIs matter", or when planning dashboard architecture, BI frameworks, client reporting cadences, and analytics that drive engagement with the metadata platform.
version: 0.1.0
---

# BI & Reporting Architecture

This skill provides guidance on designing business intelligence and reporting for the plugin metadata platform — creating the dashboards and reports that help clients understand their data and demonstrate value.

## Strategic Context

Before designing any dashboard, consider:

- **Dashboards are not just reporting — they're sales tools.** The first time a client logs in and sees "Your plugins drove 127 outcomes this month," they decide if the platform is valuable. Dashboard design directly impacts retention.
- **Different personas need different data.** A CTO cares about data freshness and system health. A marketer cares about outcomes achieved. An exec cares about ROI. One dashboard doesn't serve all.
- **Buyers use dashboards to evaluate data quality.** When you show prospective data buyers "Here's the kind of intelligence you get," they decide whether to license. Dashboards are part of your commercial positioning.
- **Simple > comprehensive.** A dashboard with 3 clear metrics clients understand beats one with 20 metrics they ignore.
- **Trends matter more than snapshots.** "Outcome rate is improving 5% week-over-week" is more useful than "This week we had 47 outcomes."

## Reporting Architecture (Layers)

### Layer 1: Real-Time Operational Dashboard

**Who uses it:** CTOs, platform leads, ops teams

**Purpose:** Health check — is the platform working? Is data flowing?

**Key metrics:**
- Data freshness: "Last event received 2 minutes ago"
- Event volume: "347 events received today" (compared to historical average)
- Plugin connections: "11 of 11 plugins reporting normally" (red if any fail)
- Error rate: "0.2% of events had errors" (with error examples)
- Data quality: "99.8% of events passed validation"

**Design:**
- Top-of-page status lights (all green = system healthy)
- One metric per card
- Trend sparkline for each metric (is this improving or degrading?)
- Alert threshold visualization ("Error rate is at 0.2% — threshold is 1%")

**Refresh cadence:** Real-time (auto-update every 30 seconds)

### Layer 2: Performance Dashboard (for clients)

**Who uses it:** Marketers, sales reps, team leads

**Purpose:** Understand plugin impact — what outcomes are we driving?

**Key sections:**

**Section 1: Monthly Overview**
- Invocation count (compared to last month, with trend)
- Outcome count (compared to last month, with trend)
- Outcome rate ("47 outcomes / 312 invocations = 15% conversion")
- Sentiment distribution ("82% positive, 14% neutral, 4% negative")

**Section 2: Outcome Breakdown**
- Stacked bar chart: outcome types (content created, proposals sent, deals progressed, decisions made, time saved)
- Most recent outcomes list (what happened in the last 24 hours)

**Section 3: Feature Usage**
- Which features are most used (bar chart, top 5)
- Feature adoption trend (are we using more features over time?)

**Section 4: Sentiment Trends**
- Positive sentiment trending (is user satisfaction improving?)
- Top positive feedback (word cloud of user comments)
- Red flags (negative feedback that needs attention)

**Design:**
- Cards are independent (can remove one without breaking layout)
- All metrics include period selector ("Show me last 30 days, 90 days, all time")
- Trends always visible (compare to previous period)
- Surprising metrics are flagged ("Positive sentiment jumped from 76% to 92%!")

**Refresh cadence:** Daily (updates at 6am UTC)

### Layer 3: Benchmarking Dashboard (unlocks at 15+ managed clients)

**Who uses it:** Marketing leaders, C-suite, investors

**Purpose:** How do we compare to peers?

**Key metrics:**
- Outcome rate percentile: "You're in the top 20% for outcome rate among similar companies"
- Feature adoption: "You use 7 of 10 features; peers average 4.2"
- Sentiment score: "Your user satisfaction is 84%; peer average is 76%"
- Growth trajectory: "Your outcome rate is growing 8% month-over-month; peer average is 5%"

**Segmentation options:**
- Filter by industry (compare to other marketing agencies)
- Filter by company size (compare to similar-sized companies)
- Filter by region (compare to companies in your region)

**Design:**
- Percentile bars (show where you rank visually)
- Segment dropdown (choose what to compare against)
- Peer band width (show the range: 25th percentile to 75th percentile)
- Explanation text ("Top 20% means you're doing something right; here's what peers in top 20% do differently")

**Refresh cadence:** Weekly (on Monday morning)

### Layer 4: Strategic Intelligence Report (for PE/acquirers)

**Who uses it:** Investment partners, strategic acquirers, executives

**Purpose:** Make investment/acquisition decisions

**Sections:**

**Section 1: Portfolio Summary**
- How many portfolio companies are on Cowork?
- Average outcome rate per company
- Breakdown by industry, size, stage
- Performance distribution (histogram of outcome rates)

**Section 2: Best Practices**
- Which portfolio companies are in the top quartile? What are they doing?
- What features do top performers use? Which are lagging?
- Specific recommendations for low performers

**Section 3: Investment Opportunity**
- Where is there untapped potential? (Which companies are underutilizing plugins?)
- Estimated ROI of optimization: "If Company D reached peer median performance, estimated +$X revenue impact"
- Resource allocation: "Invest here first to unlock value"

**Section 4: Competitive Position**
- How does this portfolio compare to other portfolios we're aware of?
- Trend: are we gaining or losing ground?

**Design:**
- Executive summary (1 page: key findings + recommendations)
- Detailed analysis (10–15 pages: tables, charts, examples)
- Appendix: raw data (for those who want to dive deep)

**Format:** PDF report (delivered quarterly or on-demand)

### Layer 5: Custom Dashboards (for advanced self-service)

**Who uses it:** Analysts, data engineers, curious users

**Purpose:** Explore data freely

**Capability:**
- Query builder: select metrics, filters, grouping
- Visualization options: line chart, bar, table, scatter, heatmap
- Drill-down: click a segment to see details
- Export: download results as CSV, embed in reports

**Design principle:** Simple for common queries, powerful for edge cases.

**Refresh cadence:** On-demand (user clicks "refresh")

## Key Metrics & Definitions

### Core Metrics (Understand These First)

| Metric | Definition | Formula | Why It Matters |
|--------|-----------|---------|----------------|
| Plugin invocation | Number of times plugin was used | COUNT(*) FROM activity_events | Measures adoption and usage frequency |
| Outcome | Business result achieved with plugin's help | COUNT(*) FROM outcomes | Measures business impact, not just activity |
| Outcome rate | Percentage of invocations that drove outcomes | outcomes / invocations | Efficiency: are we getting results per use? |
| Average time-to-outcome | Time from invocation to outcome | AVG(outcome_timestamp - invocation_timestamp) | Fast outcomes = more valuable |
| User sentiment | User feedback on plugin quality | SUM(positive) / total_feedback | Qualitative signal of satisfaction |
| Feature adoption | Percentage of available features being used | features_used / features_available | Are users exploring the full capability? |

### Derived Metrics (Build These from Core)

| Metric | Definition | Why It Matters |
|--------|-----------|----------------|
| Outcome velocity | outcomes per day (trend) | Growth signal: are outcomes increasing? |
| Stale invocations | invocations with no outcome (>7 days) | Quality signal: are some uses not generating results? |
| Sentiment trend | positive sentiment (trend) | Is the product getting better or worse? |
| Feature maturity | adoption of newest features | Adoption: do users embrace new capabilities? |
| Cohort retention | outcome rate for cohorts (by activation date) | Retention signal: do earlier users sustain results? |

### Avoid These Metrics (Misleading or Vague)

- "Plugin engagement" — too vague, doesn't distinguish between active use and accidental invocation
- "Success rate" — success by whose definition? Olytic's? The user's?
- "Monthly active users" — in a plugin context, this is almost always meaningless
- "Average session duration" — plugins don't have sessions in the traditional sense

## Dashboard Design Patterns

### Pattern 1: The Card Pattern

Each metric is a card with four elements:

```
┌─────────────────────┐
│ Outcome Rate        │ ← Metric name
│                     │
│      15%    ↗ 2%    │ ← Current value + trend (direction + magnitude)
│                     │
│ Peer avg: 12%       │ ← Context (how does it compare?)
└─────────────────────┘
```

**Benefits:**
- One metric per card (simple, focused)
- Trend visible immediately (green up arrow = good)
- Context prevents meaningless numbers (is 15% good?)

### Pattern 2: The Time-Series Pattern

Show how a metric changed over time:

```
Outcomes over time (last 90 days)

50 │     ╱╲     ╱╲
   │    ╱  ╲   ╱  ╲    ← Line chart (clear trend visible)
25 │   ╱    ╲ ╱    ╲
   │  ╱      ╱       ╲
 0 │_╱____________________
     ↑                  ↑
   30 days ago       Today

Current: 47 outcomes    Avg: 35 outcomes    Trend: +15% week-over-week
```

**Benefits:**
- Trends visible at a glance
- Anomalies stand out (spikes, dips)
- Context (current + average + trend)

### Pattern 3: The Breakdown Pattern

Show how one metric decomposes:

```
Outcomes by Type (127 total)

┌─ Content Created (51) 40%
├─ Proposals Sent (35)  28%
├─ Deals Progressed (25) 20%
├─ Decisions Made (12)  9%
└─ Time Saved (4)       3%
```

**Benefits:**
- Shows composition (where are outcomes coming from?)
- Identifies opportunity (which type is underrepresented?)

### Pattern 4: The Comparison Pattern

Show how client compares to peers:

```
Your Outcome Rate vs. Peers

You:    ████████████████████   80% percentile
Peers:  ███████████████           50% percentile
Bottom: ███                        25% percentile

You're in the top 20% for outcome rate!
```

**Benefits:**
- Competitive context (are we ahead or behind?)
- Motivation (if behind, shows room to improve)

## Reporting Cadence

| Report | Audience | Frequency | Format | Effort |
|--------|----------|-----------|--------|--------|
| Real-time operational | Ops team | Continuous | Dashboard | Auto |
| Weekly performance digest | Client team | Weekly (Mon 6am) | Email + dashboard | Auto |
| Monthly executive summary | C-suite | Monthly (1st of month) | PDF + email | Semi-auto |
| Quarterly benchmarking | Marketing + exec | Quarterly | Dashboard + PDF | Semi-auto |
| Annual state of adoption report | External buyers | Annual (Jan) | Published PDF | Manual |

## Integration Points

### Integration with CRM (for outcome attribution)

**Goal:** Connect plugin outcomes to CRM records (deals, contacts, activities)

**Data flow:**
1. Client configures CRM connection (API key or OAuth)
2. When outcome is recorded, check if it matches a CRM record (deal closed? contact created?)
3. Annotate CRM record with "influenced by plugin" tag
4. Dashboard shows "outcomes linked to $X revenue" (calculated from CRM deal amounts)

**Example:** "This plugin was used 15 times and directly contributed to 3 deals closing for a total of $250K revenue."

### Integration with BI Tools (for power users)

**Goal:** Allow clients to connect to Olytic data via standard BI tools

**Options:**
- Tableau connector (direct Supabase connection)
- Looker embed (dashboard embedded in client's Looker instance)
- Data API (client queries via API, creates own dashboards)

**Design principle:** Start with managed reports (Olytic builds what clients need). Add self-service only after learning what queries are most common.

## Data Quality Indicators

**Every dashboard should include indicators of data quality:**

- "Data last updated: 2 hours ago" — if older than 6 hours, highlight in red
- "Data completeness: 98.2%" — if <95%, alert customer
- "Events with errors: 12" — if >1%, show red warning
- "Missing outcome attribution: 3%" — expected (some outcomes can't be linked), but acknowledge it

**Principle:** Transparency about data quality builds trust.

## Operating Principles

- **Discovery first:** Before building dashboards, interview 3–5 clients and prospective buyers. What metrics matter to them? What questions do they ask?
- **Source of truth:** Once you define a metric ("outcome rate = outcomes/invocations"), use the same definition everywhere. Consistency prevents confusion.
- **Atomic operations:** Build dashboards incrementally. Start with 3 key metrics. Add more based on user feedback.
- **Verify after writing:** Show draft dashboards to real users. Do they understand what they're looking at? Can they take action based on it?
- **No hallucination:** If a dashboard assumes CRM integration exists, confirm it works before designing around it.

## Boundaries

This skill should NOT be used for:

- Marketing dashboard design (different audience, different purpose)
- Technical BI tool implementation (Tableau, Looker, etc. — that's engineering)
- SQL query writing or optimization (that's full-stack-engineering)
- Financial reporting or compliance dashboards (that's accounting/finance domain)

If a request falls outside these boundaries, explain why and suggest the appropriate alternative.

## References

For complementary guidance:
- **User experience of dashboards:** See user-experience skill
- **Data structure supporting analytics:** See data-modeling skill
- **Commercial positioning of reporting:** See product-management skill
- **API design for BI integration:** See full-stack-engineering agent

---

Telemetry: This skill logs all invocations via plugin-telemetry.
