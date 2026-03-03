---
name: data-privacy
description: >
  Use this skill for privacy architecture and consent design: "how do we anonymize the data", "what's our privacy architecture", "design the consent framework", "how do we handle PII", "what data can we actually license", "GDPR compliance approach", "data minimization strategy", or when planning anonymization techniques, consent management, privacy-first data collection, and designing privacy-preserving systems for the metadata platform.
version: 0.1.0
---

# Data Privacy Architecture & Anonymization

This skill provides guidance on designing privacy-first data handling for the plugin metadata platform — understanding what data can be safely collected, shared, and licensed without violating client or individual privacy.

## Strategic Context

Before designing privacy architecture, consider:

- **Privacy enables monetization.** The more aggressive Olytic is about privacy, the more clients trust the platform, the more data they share, the more valuable the data becomes. Privacy and commercial value are aligned.
- **Olytic is the data custodian.** Even though clients own their data, Olytic is responsible for protecting it. A privacy breach is Olytic's liability, not the client's.
- **Privacy and security are inseparable.** Can't have strong privacy without strong security. See the security skill for security architecture.
- **Privacy is not just legal compliance.** It's a design philosophy. Build privacy into the system from the start, don't bolt it on at the end.
- **This is Olytic-specific, not just GDPR.** Gaudi should recommend privacy standards that go beyond minimum legal compliance and serve Olytic's commercial interests.

## Privacy Principles

### Principle 1: Consent-Before-Collection

**Clients explicitly consent to data collection BEFORE Olytic collects it.**

**Not:** "We collect everything, and clients can opt out later."

**Instead:** "For each data category, clients explicitly opt in. We only collect if they say yes."

**Categories that require explicit consent:**

| Category | What's Collected | Why Important | Default |
|----------|------------------|---------------|---------|
| Activity tracking | Plugin invocations, feature usage, error logs | Measure adoption, identify problems | Opt-in required |
| Outcome attribution | Link plugin usage to business outcomes | Measure business impact | Opt-in required |
| Sentiment capture | User feedback ("that was helpful" or "blew that one") | Improve plugins | Opt-in required |
| CRM linkage | Connect plugin usage to CRM records (deals, contacts) | Enable outcome attribution to revenue | Opt-in required |
| Benchmarking data | Include in aggregated peer comparisons | Provide competitive intelligence | Opt-in required |
| Third-party licensing | Allow Olytic to sell aggregated data to external buyers | Generate data platform revenue | Opt-in required |

**Implementation:**
- Consent form at client onboarding (checkboxes for each category)
- Ability to change consent settings at any time (in dashboard)
- Explicit confirmation for high-stakes decisions (e.g., "Allow Olytic to license your data to third parties?")
- Annual consent renewal (clients re-confirm each year)

### Principle 2: Data Minimization

**Collect only what you need. Delete what you don't use.**

**What to NOT collect:**
- Personal identifiable information (PII) of individual users (names, emails, phone numbers)
- Financial data (salary, revenue, profit margins)
- Proprietary business secrets (product plans, strategies, customer lists)
- Authentication credentials (passwords, API keys)

**What IS appropriate to collect:**
- Plugin usage metrics (how often, what features, error rates)
- User role (marketer, sales rep, exec) but not identity
- Industry and company size (for benchmarking)
- Outcomes achieved (deals progressed, content created, time saved)
- User sentiment (positive/negative/neutral) without verbatim feedback

**Implementation:**
- Schema design starts with "what do buyers actually need?" and works backward
- Automatic data deletion (activity older than 24 months is purged)
- Opting out of a data category triggers auto-deletion of that data type

### Principle 3: Purpose Limitation

**Data collected for one purpose can't be used for another without consent.**

**Example:**
- **Purpose 1:** "Collect outcome data to provide optimization recommendations to the client" ✓ Allowed (client benefits directly)
- **Purpose 2:** "Use same outcome data to license to a third-party buyer" ✗ Requires separate consent

**Implementation:**
- Consent form specifies purpose for each category
- Application logic enforces (code that says "if Purpose-1-only is set, block licensing access")
- Audit logging tracks purpose and access

### Principle 4: Transparency

**Clients understand exactly what data Olytic has and what it's doing with it.**

**Transparency mechanisms:**
- **Data inventory dashboard:** Shows exactly what data is stored about the client
- **Usage disclosure:** "This data has been queried by [Olytic team member] on [date] for [purpose]"
- **Licensing disclosure:** If data is licensed, show "Your anonymized data is included in the 'State of SMB AI Adoption' report (purchased by [buyer count] companies)"
- **Access logs:** Client can download audit log of everyone who accessed their data

**Design principle:** Surprise is bad. Transparency is trust-building.

## Anonymization Techniques

### Technique 1: Differential Privacy (Recommended for Aggregates)

**What it is:** Add statistical noise to aggregated data so individual records can't be reverse-engineered.

**Example:**
- Raw data: "Company A achieved 47 outcomes; Company B achieved 32"
- With differential privacy: "Average outcome count is 39 ± 5" (noise added)
- Can't reverse-engineer individual companies from the aggregate

**When to use:** Publishing aggregated reports (benchmarks, trends, public data)

**Implementation:**
- Use a library like `OpenDP` (differential privacy toolkit)
- Add Laplace noise to aggregate query results
- Tune epsilon (higher epsilon = less noise, more privacy risk; lower epsilon = more noise, more privacy protection)
- Recommendation: epsilon = 0.1 for public reports (strong privacy), epsilon = 1.0 for internal analysis

**Trade-off:** Slightly less accurate numbers, much stronger privacy guarantee.

### Technique 2: K-Anonymity (Recommended for Detailed Data)

**What it is:** Ensure every data point appears in at least K records, so individuals can't be singled out.

**Example:**
- Raw: "Healthcare consultant in California with 45 employees"
- Problem: There's only 1 company matching this description (identifiable)
- K-anonymity fix: Generalize to "Healthcare (broader) in West Coast (region) with 40-50 employees (band)"
- Now 5+ companies match the same profile (not identifiable)

**When to use:** Licensing detailed data to third parties (API access, raw data)

**Implementation:**
- Define quasi-identifiers (attributes that could identify: industry, size, region, plugin_type)
- Before licensing or publishing, verify K >= 5 for every combination
- Generalize or suppress outliers that don't meet K-anonymity threshold
- Example SQL check:
```
SELECT industry, company_size_band, region, COUNT(*) as count
FROM client_orgs
GROUP BY industry, company_size_band, region
HAVING COUNT(*) < 5
-- Alert ops: these combinations don't meet K-anonymity
```

**Trade-off:** Less granular data (broader categories), but impossible to identify individuals.

### Technique 3: Data Masking (For PII)

**What it is:** Replace PII with fake but consistent values.

**Example:**
- Original user name: "Sarah Johnson" → Masked: "user_42"
- Original email: "sarah@acme.com" → Masked: "user_42@company.com"
- Masked data is consistent (same person always = same user_42)

**When to use:** When data must include user-level signals but users are not customers

**Implementation:**
- Apply SHA-256 hash to user identifiers
- Prefix with domain (e.g., "user_" + hash)
- Consistently applies (same person always gets same hash)
- Not reversible (can't recover original from hash)

**Trade-off:** User-level analysis becomes less granular, but impossible to identify individuals.

### Technique 4: Tokenization (For CRM Linkage)

**What it is:** Replace sensitive values with tokens that only Olytic's system understands.

**Example:**
- Original CRM deal ID: "deal_12345" (could leak info if compromised)
- Tokenized: "tok_abc123xyz" (meaningless to external parties)
- Olytic maintains token → deal_id mapping (encrypted, access-controlled)

**When to use:** CRM linkage (linking outcomes to CRM records)

**Implementation:**
- Generate random token for each CRM link
- Store mapping in encrypted table (access-controlled)
- External parties see tokens, not original IDs
- Mapping is only accessible to Olytic staff with explicit permission

**Trade-off:** External parties can't independently verify outcome claims, but CRM data is protected.

## Consent Management System

### Consent Model

```
client_org
└── consent_profile (created at onboarding)
    ├── activity_tracking: true/false
    ├── outcome_attribution: true/false
    ├── sentiment_capture: true/false
    ├── crm_linkage: true/false
    ├── benchmarking: true/false
    ├── third_party_licensing: true/false
    └── consent_timestamp, version, renewal_date
```

### Consent Change Workflow

**Client goes to dashboard → Consent Settings → toggles a category off**

```
User clicks toggle
  ↓
Confirmation dialog: "Disabling sentiment capture will delete all existing sentiment data."
  ↓
User confirms
  ↓
Update consent_profile in database
  ↓
Trigger: Delete all sentiment_comment rows for this org
  ↓
Log audit event: "Org X disabled sentiment tracking"
  ↓
Dashboard updates: "Sentiment data deleted (purged)"
  ↓
Email to client confirming change
```

### Consent Renewal (Annual)

**Every 12 months, send clients consent renewal email:**
```
Subject: "Renew your data sharing consent with Olytic"

You're currently sharing:
☑ Activity tracking
☑ Outcome attribution
☑ Sentiment feedback
☐ CRM linkage
☑ Benchmarking
☐ Third-party licensing

Review your settings: [link]
```

**Purpose:** Prevent "consent creep" where clients forget what they consented to.

## Privacy Impact on Data Licensing

### What Data CAN Be Licensed (After Anonymization)

**Aggregated benchmarks (published reports):**
- "By industry: 47% of marketing agencies achieve outcome rate >30%"
- "By company size: 85% of 50-100 person companies use 3+ plugins"
- "Trend: plugin adoption growing 23% YoY in SMB segment"
- Fully anonymized, differentially private → Can be sold

**API access to anonymized feed:**
- Stream of events: "plugin_type=content_plugin, industry=marketing, outcome_type=content_created, sentiment=positive"
- Every record is anonymized (no org ID, no user ID, only generalized segments)
- K-anonymity >= 5 ensured before release → Can be sold

**Custom analysis (strategic engagements):**
- "Your portfolio's average outcome rate is 24%; industry average is 18%"
- Custom to one buyer, but other company details are anonymized
- Specific recommendations only shared with the buyer → Can be sold

### What Data CANNOT Be Licensed (Even After Anonymization)

**Client-specific data (even if anonymized):**
- "This consulting firm achieves 35% outcome rate" — too specific, could identify company
- "Company with 3 plugins in healthcare got 4 deals from plugin use" — too specific

**User-level data:**
- "User Sarah (user_42) used feature X 15 times" — even anonymized as user_42, violates purpose limitation

**CRM-linked outcomes:**
- "This deal ($500K) was influenced by plugin usage" — CRM data is client-specific, can't be shared

## Privacy by Design (Architecture Recommendations)

### Recommendation 1: Schema Includes Consent Enforcement

Every table has a `consent_tag` column that tracks which consent category it requires:

```
plugin_activity_event
├── org_id
├── event_id
├── consent_tag: "activity_tracking"
├── ...

plugin_outcome
├── org_id
├── outcome_id
├── consent_tag: "outcome_attribution"
├── ...

plugin_sentiment
├── org_id
├── sentiment_id
├── consent_tag: "sentiment_capture"
├── ...
```

**Benefit:** When consent changes, system automatically knows which rows to delete.

### Recommendation 2: Data Pipeline Includes Privacy Checks

Before any data leaves the system (export, API call, licensing), it passes through privacy gate:

```
Query for aggregated data
  ↓
Privacy gate: Apply anonymization rules
  ✓ Is K-anonymity >= 5?
  ✓ Is differential privacy applied?
  ✓ Are PII fields redacted?
  ↓
Safe to return: OK
↓
NOT safe: Alert ops, don't return
```

### Recommendation 3: Audit Trail for Privacy

Separately track privacy-relevant events:

```
privacy_audit_log
├── timestamp
├── event_type: "consent_change", "data_deleted", "anonymization_applied", "data_accessed"
├── org_id
├── description
├── user_id (who made the change)
├── details (what consent was changed, what data deleted, etc.)
```

## Operating Principles

- **Discovery first:** Before finalizing privacy architecture, interview 5–10 prospective data buyers. What privacy level do they require? What data CAN they not see?
- **Source of truth:** Once you publish a privacy commitment ("We delete all data within 30 days of opting out"), design systems to enforce it. Make it non-negotiable.
- **Atomic operations:** Implement privacy controls incrementally. Day 1: basic consent form. Month 1: auto-deletion on opt-out. Month 3: differential privacy on reports.
- **Verify after writing:** Don't trust anonymization theory. Test it. Try to re-identify records after applying k-anonymity. If you can do it, clients could too.
- **No hallucination:** If privacy architecture depends on a specific anonymization library or technique, test it with real data before designing around it.

## Boundaries

This skill should NOT be used for:

- Legal compliance documents or privacy policy writing (that's counsel domain)
- Cryptographic implementation (use industry-standard libraries)
- Consent UI/UX design (that's user-experience skill)
- Operational procedures for handling data deletion requests (that's ops domain)

If a request falls outside these boundaries, explain why and suggest the appropriate alternative.

## References

For complementary guidance:
- **Consent UI and transparency dashboard:** See user-experience skill
- **Security architecture that enforces privacy:** See security skill
- **Data schema design for privacy:** See data-modeling skill
- **Compliance requirements:** See security skill

---

Telemetry: This skill logs all invocations via plugin-telemetry.
