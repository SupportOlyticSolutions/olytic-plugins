---
name: data-modeling
description: >
  This skill should be used when the user asks to "what object schema would we use",
  "design our data model", "how should we structure the metadata",
  "what normalization approach makes sense", "help me design the database",
  "what tables do we need", or needs guidance on relational schema design,
  normalization patterns, indexing strategy, or data structure decisions
  for the plugin metadata platform.
version: 0.1.0
---

# Data Modeling for the Metadata Platform

This skill provides guidance on designing the relational database schema for Olytic's plugin metadata platform — the foundational architecture that captures usage, outcomes, and sentiment data from client plugins.

## Strategic Context

Before starting data model design, consider:

- **Outcome attribution is the core differentiator.** Every table design must support the distinction between activity signals (plugin was used) and impact signals (plugin helped achieve a business outcome). The schema must naturally encode this separation.
- **Data must be CRM-linkable.** The model must enable connection to client CRM systems via `client_id` and `org_id` so that plugin outcomes can be attributed to business results (deals closed, revenue generated, pipeline velocity, etc.).
- **The data is the product.** This isn't operational telemetry — it's a commercial asset. Schema design directly impacts what buyers will pay for. Structure for commercial value, not just operational convenience.
- **Supabase MVP, but future-proof.** Design for PostgreSQL/Supabase initially, but assume the platform will eventually work with competing storage systems. Avoid Supabase-specific patterns that don't generalize.
- **Sentiment and qualitative signals matter.** The schema must capture both quantitative metrics (invocation count, execution time) and qualitative signals (user sentiment, feedback). This combination is what creates market value.

## Core Schema Principles

### 1. Outcome Attribution Architecture

The fundamental problem the metadata platform solves is **connecting activity to outcomes**. Structure your schema around this:

**Activity layer** (what the plugin did):
- Plugin invocations (when did the user call the plugin, how long did it take, what did they ask for?)
- Feature usage within plugins (which capabilities were used, in what order, how often?)
- Plugin modifications (when was the plugin updated, what changed, did usage patterns shift?)

**Outcome layer** (what the business achieved):
- Business result capture (did the user create a document, send an email, close a deal, generate content?)
- Outcome attribution (which plugin usage directly enabled which business result?)
- Impact measurement (speed improvement, quality improvement, revenue impact, time saved?)

**Connection layer** (linking activity to outcomes):
- `outcome_id` references to activities that enabled it
- Timestamp pairs (activity happened at T1, outcome at T2, delta = latency)
- Attribution confidence scores (how certain is this connection?)

### 2. Client & Segmentation Linkage

Every record must be traceable back to the client organization and their market segment:

```
client_org
├── org_id (primary key)
├── client_id (linkable to CRM)
├── client_name
├── industry (e.g., "marketing agency", "consulting")
├── company_size_band (e.g., "20-50", "51-100")
├── geographic_region
├── crm_system (e.g., "hubspot", "salesforce")
└── crm_org_id (for CRM linkage)

plugin_deployment
├── deployment_id (primary key)
├── org_id (foreign key to client_org)
├── plugin_id (what plugin is deployed)
├── plugin_type (e.g., "doer", "optimizer")
├── deployment_date
└── deployment_status (active, archived, paused)
```

This structure enables queries like: "For healthcare companies 20-50 employees, which plugin types drive the most outcomes?" or "What's the outcome-to-activity ratio by industry?"

### 3. Dual-Layer Telemetry Design

**Structured activity events:**

```
plugin_activity_event
├── event_id (primary key)
├── deployment_id (which plugin instance)
├── org_id (which client)
├── event_type (invocation, feature_usage, error, modification)
├── event_timestamp
├── duration_ms
├── token_count (LLM tokens consumed)
├── user_category (e.g., "marketer", "sales_rep", "exec")
├── feature_used (which specific feature/command in the plugin)
├── prompt_hash (anonymized version of what the user asked)
└── error_code (if applicable)
```

**Unstructured outcome capture:**

```
plugin_outcome
├── outcome_id (primary key)
├── org_id
├── outcome_type (content_created, email_sent, deal_progressed, decision_made, time_saved)
├── outcome_value_type (qualitative, quantitative_time, quantitative_revenue)
├── outcome_description (user's description of what happened)
├── user_sentiment (positive, neutral, negative)
├── sentiment_comment (e.g., "that was helpful", "missed the mark")
├── related_activity_ids (foreign keys to plugin_activity_event records that enabled this)
├── outcome_timestamp
└── crm_record_link (optional: link to deal, contact, or activity in client CRM)
```

This dual-layer approach captures both the precise metrics (structured activity) and the human context (unstructured outcomes and sentiment).

### 4. Commercial Value Maximization

Design the schema to answer the highest-value buyer questions:

**"Which plugins work best for which company types?"**
- Requires: plugin_type + outcome by industry, company_size_band, geographic_region
- Schema support: Explicit segment columns in both activity and outcome tables; foreign keys to client_org

**"What's the ROI of this plugin type?"**
- Requires: Time spent (duration_ms, token_count) vs. business outcomes (deals closed, content created, time saved)
- Schema support: Outcome_value_type field that distinguishes quantitative revenue from qualitative impact

**"Which specific features within a plugin drive the most outcomes?"**
- Requires: Feature-level usage tracking + outcome attribution
- Schema support: feature_used column in activity events, related_activity_ids in outcomes

**"How fast do outcomes compound?"**
- Requires: Time series of activities and outcomes
- Schema support: Explicit timestamps on all events, outcome_timestamp vs. activity_timestamp for latency calculation

### 5. Anonymization & Consent Architecture

Privacy is a commercial concern, not just a compliance concern. Clients must trust the platform.

```
consent_log
├── consent_id (primary key)
├── org_id
├── data_category (e.g., "activity_tracking", "crm_linkage", "outcome_attribution")
├── consent_granted (boolean)
├── consent_timestamp
├── consent_version (which privacy policy version did they consent to?)
├── opt_out_categories (e.g., ["revenue_outcomes"])
└── consent_expiry (annual renewal)

anonymization_policy
├── policy_id
├── org_id
├── pii_masking_enabled (boolean)
├── prompt_hash_algorithm (which hashing function for user prompts?)
├── crm_field_sensitivity (which CRM fields are sensitive and should be dropped?)
└── policy_effective_date
```

**Anonymization execution:**
- User prompts → hashed (not reversible, but consistent for deduplication)
- CRM contact records → field-level filtering (drop emails, phone numbers; keep job title, industry)
- Outcomes → aggregate by type, not individual record attribution
- Sentiment comments → anonymized before storage (paraphrase, not verbatim)

### 6. Optimizer Plugin Integration

The Optimizer plugin will consume data from your metadata schema and feed back improvements. Design for that workflow:

```
optimizer_recommendation
├── recommendation_id (primary key)
├── deployment_id (which plugin to improve)
├── org_id
├── recommendation_type (prompt_update, feature_add, feature_remove, usage_pattern)
├── recommendation_basis (which data pattern triggered this)
├── recommendation_description
├── confidence_score (0.0–1.0, how confident is the Optimizer in this?)
├── recommended_at
├── accepted_at (when the client decided to implement)
├── acceptance_status (pending, accepted, rejected, implemented)
└── impact_after_implementation (how did activity/outcomes change after acceptance?)
```

This table closes the loop: Gaudi designs the schema → data flows in → Optimizer analyzes and recommends → client accepts recommendation → impact is measured → loop repeats.

## Table Relationship Map

```
client_org
    ├─→ plugin_deployment
    │       ├─→ plugin_activity_event
    │       ├─→ plugin_outcome
    │       └─→ optimizer_recommendation
    └─→ consent_log
    └─→ anonymization_policy

plugin_activity_event
    └─→ plugin_outcome (via related_activity_ids)
```

## Normalization Guidelines

**For MVP (Supabase):**
- Normalize to 3NF for activity events (remove redundancy, ensure data integrity)
- Denormalize slightly in outcome tables (include org_id, client_id, industry directly for query performance)
- Rationale: Activity events are high-volume; outcomes are lower-volume. The denormalization cost is acceptable.

**For future scale (columnar storage):**
- Consider moving to a dimensional (star schema) approach: fact tables (activity, outcomes) + dimension tables (client_org, plugins, date_ranges)
- Rationale: Columnar storage excels at aggregate queries ("total outcomes by industry"), not row-by-row lookups.

## Indexing Strategy

Create indexes to support the high-value queries:

| Index | Purpose | Columns |
|-------|---------|---------|
| Activity by org and timestamp | Fast activity retrieval for a specific client | (org_id, event_timestamp DESC) |
| Outcome by org and type | Analyze outcome patterns by org | (org_id, outcome_type, outcome_timestamp DESC) |
| Outcome attribution lookup | Link outcomes back to activities | (related_activity_ids) |
| Segment analysis | Query by industry, company size, region | (org_id) + (client_org.industry, client_org.company_size_band) |
| Optimizer recommendations by status | Track pending and accepted recommendations | (org_id, acceptance_status) |

**Note:** Avoid over-indexing. Start with these five and measure query performance before adding more.

## Common Pitfalls to Avoid

- **Conflating activity with outcome.** Activity is "the plugin was used 10 times today." Outcome is "those 10 uses resulted in 3 proposals being sent." Don't merge them — keep them separate and linked.
- **Over-normalizing for MVP.** Supabase queries are fast enough for initial use cases. Don't create 15 junction tables before you know you need them.
- **Assuming all outcomes are CRM-linkable.** Some outcomes (user created a document, said "that was helpful") aren't tied to a CRM record. Build for both.
- **Forgetting the human layer.** Quantitative data alone is weak. Sentiment ("that was helpful" vs. "you blew that") is what makes the data commercially valuable.
- **Losing consent context.** If a client opts out of outcome attribution, you must respect that in queries. Store consent explicitly, not as application logic.

## Validation Checklist

Before you finalize your schema, verify:

- **Outcome attribution is native to the design.** Can you write a single SQL query that says "show me all outcomes enabled by plugin X in org Y"? If not, rethink the structure.
- **CRM linkage is planned.** Does every outcome have a clear path to a client CRM field? (Deal ID, contact ID, activity record ID)
- **Anonymization is enforceable.** Can you anonymize a record without breaking referential integrity?
- **The Optimizer can consume it.** Can you write a query that gives the Optimizer all the context it needs to recommend improvements? (Usage patterns, outcome rates, sentiment trends)
- **Buyers will find value.** Look at your table design and ask: "Can I generate a report that answers a buyer's real question?" If the answer is no, redesign.

## Operating Principles

- **Discovery first:** Before finalizing schema, validate with the technical architect. Understand how activity will actually be captured (via Aulë telemetry hooks, via Cowork APIs, manually?) before designing the tables that receive it.
- **Source of truth:** Once schema is live and data flows in, the schema becomes authoritative. Changes to schema require coordination with the Optimizer and any dependent systems.
- **Atomic operations:** When you need to modify schema in production, make the smallest change necessary (add a column, add an index) rather than restructuring tables.
- **Verify after writing:** After any schema change, validate that existing data still conforms and that queries still perform.
- **No hallucination:** If a data field, CRM system, or integration point is not confirmed, ask rather than assuming. "Will Aulë expose plugin invocation counts via an API?" — verify before designing a table that depends on it.

## Boundaries

This skill should NOT be used for:

- Designing operational data models for Gaudi itself (like logging which decisions Gaudi made)
- Database administration tasks (backup, replication, disaster recovery)
- Client-specific schema customizations (Gaudi designs the platform template, not client variants)
- Application code design (SQL queries, ORMs, etc. — that's full-stack engineering)

If a request falls outside these boundaries, explain why and suggest the appropriate alternative.

## References

For detailed guidance on specific topics:
- **Supabase integration:** See the full-stack-engineering skill
- **Anonymization techniques:** See the data-privacy skill
- **Commercial positioning:** See the product-management skill
- **Cowork API constraints:** See the full-stack-engineering skill

---

Telemetry: This skill logs all invocations via plugin-telemetry.
