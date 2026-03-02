---
name: product-management
description: >
  This skill should be used when the user asks to "what type of data will buyers want",
  "how do we measure business impact", "design the go-to-market for the data platform",
  "what's the revenue model", "forecast commercial viability", "how do we price the data",
  or needs guidance on product strategy, revenue modeling, go-to-market, success metrics,
  and the commercial positioning of the metadata platform as a saleable product.
version: 0.1.0
---

# Product Strategy & Commercial Viability for the Data Platform

This skill provides guidance on positioning, pricing, and commercializing Olytic's plugin metadata platform — turning behavioral data into a saleable product that generates recurring revenue.

## Strategic Context

Before designing product strategy, consider:

- **The data IS the product.** This isn't a service wrap-up (though services will exist). The core value is access to proprietary intelligence about how SMBs use AI plugins. Design accordingly.
- **Multiple revenue streams, different buyers.** The platform generates revenue in at least three ways: (1) managed service optimization improvements applied to clients' plugins, (2) direct licensing of aggregated data to third-party buyers, (3) strategic intelligence to PE firms and MarTech platforms. Each stream has different packaging and pricing.
- **Data quality determines value.** If the data is generic activity metrics (plugin was used 10 times), the price will be low. If it's outcome data (plugin enabled 3 proposals to move forward faster), the price is 10x higher. Product strategy must prioritize outcome over activity.
- **Competitive window is open now.** Olytic's advantage is that it will accumulate this data as a byproduct of implementing Claude plugins. Competitors will try to copy after Olytic's success. Get to market fast, establish brand, lock in early adopters.
- **Trust is a commercial asset.** The more clients trust the platform, the better data they'll share, the higher the commercial value. Trust and revenue are directly linked.

## The Three Revenue Streams

### Stream 1: Optimization Revenue (Managed Service Improvements)

**What it is:** Olytic charges existing Claude OS Care clients to apply AI-powered optimizations to their plugins — driven by insights from the metadata platform.

**Example:** "Based on analysis of your plugin usage and industry benchmarks, we recommend adding a feature that could increase user adoption by 20%. We'll build and test it — $3K."

**Why it's valuable:**
- Low friction to sell (existing relationship, already paying for managed service)
- High margin (marginal cost is mostly Claude Cowork credits)
- Justified by data (optimization is data-driven, not guesswork)
- Stacking revenue (client pays for implementation + managed service + optimizations)

**Pricing model:**
- $1.5K – $5K per optimization (depending on feature complexity)
- Sold as "optimization projects" within the managed service retainer
- Target: 2–3 optimizations per client per year = $3K–$15K additional annual revenue per client

**Data requirements:**
- Usage patterns (which features are used, at what frequency?)
- Outcome attribution (which features drive the most outcomes?)
- Industry benchmarks (how do you compare to similar companies?)
- Sentiment analysis (user feedback about what's working and what's missing)

**Measurement:**
- Pre-optimization: baseline usage, outcome rate, sentiment
- Post-optimization: same metrics after feature is deployed
- ROI: "Feature improved outcome rate from 28% to 34%" or "Reduced time-to-complete-task by 12%"

### Stream 2: Data Licensing (Aggregated Insights)

**What it is:** Olytic licenses anonymized, aggregated data about plugin usage and outcomes to external buyers — primarily companies in the MarTech, consulting, and PE spaces.

**Example buyers:**
- **MarTech platforms** (HubSpot, Marketo, Salesforce) want to know: "Which plugins drive the most pipeline velocity for SMB marketing teams?"
- **Consulting firms** want benchmarks: "What does average plugin ROI look like for companies our size?"
- **PE firms** want portfolio intelligence: "How do portfolio companies compare on AI adoption? Which are lagging? What's the opportunity?"

**Why it's valuable:**
- Pure margin revenue (data collected as byproduct, no incremental cost)
- Recurring contracts (annual or multi-year licenses)
- Scale-friendly (one dataset sold to many buyers)
- Market window is narrow (first mover advantage in SMB AI adoption intelligence)

**Pricing model:**
- **"State of SMB AI Adoption" annual report** — $5K/year
  - Published annually (first publication at 30+ managed clients)
  - Sold as subscription to marketing leaders, agencies, consultancy firms
  - Content: "AI adoption trends, plugin performance benchmarks, outcome data by industry/size"
  - Target market: 150–200 annual subscribers → $750K–$1M annual revenue

- **"AI Plugin Performance Dataset" (Full licensing)** — $35K/year (7 licenses target)
  - Full access to anonymized platform data via API
  - Sold to PE firms, strategic acquirers, advanced consultancies
  - Content: row-level data on 50+ managed clients (aggregated, anonymized)
  - Restrictions: can't identify individual clients, can't use for competitive product
  - Target market: 5–10 licenses → $175K–$350K annual revenue (near-pure margin)

**Data requirements:**
- **Heavy outcome focus.** Activity data alone (plugin invocations) is worthless to external buyers. Outcome data (improved lead quality, faster sales cycles, content velocity) is what they'll license.
- **Segment dimension data.** Buyers need to slice by industry, company size, geographic region, role. Every row of data must be tagged with segment attributes.
- **Comparative context.** Raw numbers are meaningless. "Plugin X drove 47 outcomes" is useless. "Plugin X drove 47 outcomes; average for this segment is 32" is useful.
- **Trend and velocity data.** Buyers want to know not just absolute numbers, but how things are changing. "Adoption of X is growing 25% quarter-over-quarter" is more valuable than static snapshots.

**Measurement:**
- Units licensed (how many annual subscriptions to the report?)
- License retention rate (do buyers renew?)
- Data quality feedback (are buyers finding the data credible and actionable?)
- Impact on sales (do customers buying the report also buy consulting?)

### Stream 3: Strategic Intelligence (PE & Acquirer Intelligence)

**What it is:** Olytic sells deeply analyzed strategic intelligence to PE firms and potential acquirers.

**Example:** "Here's the detailed breakdown of how your portfolio companies compare on AI adoption. Company A is in the top 20% for outcome velocity; Company B is lagging. Here's where the opportunity is."

**Why it's valuable:**
- Highest price point ($100K–$250K per engagement)
- Defensible (only Olytic has this data)
- Natural upgrade path from managed service (serve existing clients, then sell them white-label services)
- Strategic value to acquirers (data on SMB AI adoption informs acquisition strategy)

**Pricing model:**
- $100K–$250K per "strategic intelligence engagement"
- Sold to PE firms evaluating portfolio AI adoption
- Includes: analysis, recommendations, roadmap for portfolio optimization
- Target: 2–4 engagements per year by Year 3 → $200K–$1M annual revenue

**Data requirements:**
- Benchmark data across 50+ companies (same as Stream 2)
- Custom analysis capability (ability to answer specific questions about portfolio opportunity)
- Competitive intelligence (how does your portfolio compare to other portfolios?)

**Measurement:**
- Engagements closed (how many PE firms commissioned analysis?)
- Follow-on services (do they hire Olytic to implement recommendations?)
- Lifetime value (does one engagement lead to 2–3 years of strategic retainers?)

## Competitive Positioning & Market Differentiation

**Why Olytic wins (vs. competitors):**

| Competitor | Their Advantage | Olytic's Advantage |
|------------|-----------------|-------------------|
| Generic analytics vendors (Amplitude, Mixpanel) | Established platforms, multi-product integrations | Specific to AI plugins, outcome-focused, includes optimization recommendations |
| Freelance AI consultants | Personal relationships, domain expertise | Proprietary data asset, weekly automated optimization, zero marginal cost to scale |
| Anthropic (Claude directly) | owns the platform | Independent, multi-tool support, business-context intelligence |

**Olytic's durable advantages:**
1. **Outcome attribution data** — only Olytic will have rich outcome data because it's built into the implementation and optimization loop
2. **Scope (SMB GTM)** — specific to a profitable segment; competitors trying to be everything will lose focus
3. **Compounding data asset** — early movers (15+ managed clients by Q4 2027) establish credible benchmarks; followers arrive to a mature market

## Buyer Personas & Willingness to Pay

### Buyer 1: VP of Marketing (in existing managed service client)

**Profile:** Wants to optimize their plugin investment

**Pain:** "We're using the plugin but we're not sure if we're using it optimally. Are we leaving value on the table?"

**Willingness to pay:** Medium ($2K–$5K per optimization project)

**Buying cycle:** Fast (already buying from Olytic, needs minimal justification)

**Argument:** "Here's how you compare to similar companies. We see an opportunity to improve [metric] by 20%. That's worth $100K/year in value to you."

### Buyer 2: Head of Insights (PE firm evaluating portfolio)

**Profile:** Allocating capital across portfolio companies, wants intelligence on AI adoption gaps

**Pain:** "How much value are we leaving on the table if some portfolio companies are behind on AI?"

**Willingness to pay:** High ($100K–$250K per engagement)

**Buying cycle:** Medium (quarterly investment committee meetings)

**Argument:** "Here's how your portfolio stacks up on AI adoption. Companies A and C are best-in-class. Companies D and E are 12–18 months behind. We can close that gap — here's the roadmap and ROI."

### Buyer 3: VP of Strategy (MarTech platform)

**Profile:** Wants market intelligence on how their platform is being used in the wild

**Pain:** "We know thousands of companies use our platform, but we don't know if it's driving the outcomes our customers care about."

**Willingness to pay:** Medium-high ($35K–$50K annual license)

**Buying cycle:** Long (procurement, integration into internal analytics)

**Argument:** "Here's how leading users of your platform are getting outcomes. Your market is growing 23% year-over-year in the SMB segment. Here's what's driving adoption."

## Commercial Viability Forecast

### Year 1 (Jul–Dec 2026) — Proof of Concept

**Revenue:** $0 from data/optimization (platform not yet live)
**Focus:** Win 3 implementation case studies, prove the model works

### Year 2 (2027) — Platform MVP & First Data Licensing

**Managed service clients:** 11 (conversion from Year 1 implementations)
**Optimization revenue:** ~$25K (2–3 projects per client, ~$3K each)
**Data licensing:** $0 (insufficient data volume to credibly license)
**Total:** ~$25K

### Year 3 (2028) — Threshold 1: Data becomes credible

**Managed service clients:** 26
**Optimization revenue:** ~$150K (3–4 projects per client)
**Data licensing (pilot):** ~$20K (first "State of AI Adoption" report to 4 subscribers)
**Total:** ~$170K

### Year 4 (2029) — Scale & Monetization

**Managed service clients:** 46
**Optimization revenue:** ~$300K (4 projects per client avg)
**Data licensing:** ~$600K (120 subscribers @ $5K annual report)
**Strategic intelligence:** ~$150K (2 engagements @ $75K avg)
**Total:** ~$1.05M

### Year 5 (2030) — Full Scale

**Managed service clients:** 66
**Optimization revenue:** ~$400K
**Data licensing:** ~$800K (150 subscribers + 8 full licenses @ $35K)
**Strategic intelligence:** ~$500K (4 engagements)
**Total:** ~$1.7M

**Cumulative 5-year revenue (data platform only):** ~$2.94M
**Plus managed service base revenue (from separate calculation):** ~$4M
**Total platform + managed service:** ~$6.9M

## Go-to-Market Strategy

### Phase 1: Proof (Jul 2026 – Jun 2027)

**Goal:** Win 3 case study implementations, prove the metadata platform architecture works

**Marketing:** Internal focus. Build the platform, document the process, create internal case studies.

**Sales:** Warm outreach to aligned prospects (agencies with AI maturity, consulting firms).

### Phase 2: Platform MVP (Jul 2027 – Jun 2028)

**Goal:** Launch the metadata platform with 11 managed clients; start selling optimization services

**Marketing:** "Olytic has 11 SMBs using AI plugins at scale — here's what they're learning" (benchmarking report)

**Sales:** Sell optimization projects to existing managed service clients; position as value-add to the retainer

### Phase 3: Data Licensing Beta (Jul 2028 – Dec 2028)

**Goal:** Launch "State of SMB AI Adoption" report; find first 10–15 subscribers

**Marketing:** Launch report on Olytic website; PR push ("First-of-its-kind SMB AI adoption data now available")

**Sales:** Personal outreach to MarTech, agencies, consultancies; offer pilot subscriptions at discount

### Phase 4: Full Monetization (2029+)

**Goal:** 150+ report subscribers; 5–10 full data licenses; 3–5 strategic intelligence engagements per year

**Marketing:** Annual report published every January; quarterly updates via email/LinkedIn

**Sales:** Dedicated data sales role; strategic account management for PE/acquirer relationships

## Product Roadmap

### MVP (0.1.0) — Jul 2027

- [ ] Metadata platform core (schema, collection, storage)
- [ ] Client dashboard (activity, outcomes, sentiment)
- [ ] Basic consent/privacy controls
- [ ] Optimization recommendation engine (simple heuristics)

### Phase 2 (0.2.0) — Jan 2028

- [ ] CRM linkage (HubSpot, Salesforce)
- [ ] Benchmarking dashboard (compare to peers)
- [ ] Advanced recommendations (ML-based)
- [ ] Data export (CSV, API access for advanced users)

### Phase 3 (1.0.0) — Jul 2028

- [ ] "State of SMB AI Adoption" report (published, licensed)
- [ ] White-label capability (for strategic partnerships)
- [ ] Advanced analytics (cohort analysis, retention curves)
- [ ] Predictive modeling (forecast adoption based on leading indicators)

### Phase 4 (2.0.0) — 2029+

- [ ] Multi-platform support (not just Claude Cowork)
- [ ] Custom report builder (self-service analytics)
- [ ] Real-time dashboards (streaming data, live metrics)
- [ ] AI agent for data exploration ("What drove the highest outcomes this quarter?")

## Operating Principles

- **Discovery first:** Before finalizing commercial strategy, talk to 5–10 prospective buyers in each persona. Validate that they'll actually pay for this data.
- **Source of truth:** Once you've made a pricing decision (e.g., "$35K for full data license"), don't change it without understanding impact. Consistency builds credibility.
- **Atomic operations:** Launch with the simplest viable product (annual report, $5K). Don't try to launch all three revenue streams at once.
- **Verify after writing:** When you publish a pricing model or go-to-market strategy, ask 2–3 target buyers: "Would you buy this at this price?" Adjust based on feedback.
- **No hallucination:** Don't assume buyer demand without validation. "I think PE firms will pay $100K" is a hypothesis until you talk to PE firms.

## Boundaries

This skill should NOT be used for:

- Designing the product itself (technical requirements, features) — that's solution-design
- Detailed financial modeling or venture metrics — that's CFO work
- Marketing campaign design or content strategy — that's marketing domain
- Legal terms or licensing agreements — that's counsel domain
- Pricing of the managed service (implementation + Claude OS Care) — that's separate

If a request falls outside these boundaries, explain why and suggest the appropriate alternative.

## References

For complementary guidance:
- **Commercial framing of data structure:** See data-modeling skill
- **Communicating value via UI:** See user-experience skill
- **Trust architecture that enables sharing:** See security and data-privacy skills

---

Telemetry: This skill logs all invocations via plugin-telemetry.
