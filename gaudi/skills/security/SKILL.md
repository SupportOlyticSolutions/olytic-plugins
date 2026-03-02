---
name: security
description: >
  Use this skill for security and trust architecture: "design trust architecture", "what security controls do we need", "how do we handle security concerns", "design the trust framework", "what compliance do we need", "what are our security requirements", "how do we protect client data", or when planning security architecture, trust layers, compliance frameworks (SOC2, GDPR), and designing security-first data governance for the metadata platform.
version: 0.1.0
---

# Security Architecture & Trust Framework

This skill provides guidance on designing security-first architecture for the plugin metadata platform — addressing client trust, compliance requirements, and building the controls that make clients feel safe sharing their data.

## Strategic Context

Before designing any security layer, consider:

- **Trust is a commercial asset.** The more clients trust the platform, the better data they'll share, the higher the commercial value. Security isn't just compliance — it's a revenue driver.
- **Clients will be nervous about data sharing.** They're giving Olytic access to plugin usage data that reveals how they use tools. Security controls and transparency are what convince them to opt in.
- **Olytic doesn't have a security team.** You're not building a bank-grade security architecture. You're building pragmatic controls that address real risks and are operationally sustainable.
- **This is Olytic's responsibility, not the vendor's.** Even though Supabase and Cowork handle some security, Olytic is the data custodian. You own the security architecture.
- **Privacy and security are tightly coupled.** Can't separate them. If data isn't secure, it can't be private. If privacy controls are weak, trust erodes.

## Security Posture & Risk Model

### Threat Model

**Who might attack or compromise the platform?**

| Threat | Actor | Intent | Method | Impact |
|--------|-------|--------|--------|--------|
| Data breach | External hacker | Steal client data or resell intelligence | Exploit unpatched vulnerability, weak auth, misconfigured DB | Catastrophic (lose all client trust) |
| Unauthorized access | Internal (Olytic employee) | Steal competitor data or sell to buyer | Query database with stolen credentials | High (client lawsuit, regulatory) |
| Malicious data injection | Compromised plugin | Insert false outcomes to artificially boost metrics | Exploit unvalidated API endpoint | Medium (data quality loss, bad recommendations) |
| Account takeover | Social engineering | Access client dashboard, export data | Phishing, credential reuse | High (client privacy breach) |
| Privacy violation | Regulatory investigation | Ensure compliance with GDPR/CCPA | Audit data handling, access controls | High (fines, reputational) |

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-----------|
| Data breach (external) | Medium | Catastrophic | Encryption, intrusion detection, incident response |
| Unauthorized internal access | Low (Olytic is small, trusted) | High | Access controls, audit logging, segregation of duties |
| Malicious data injection | Low (plugins are controlled) | Medium | Schema validation, rate limiting, anomaly detection |
| Account takeover | Medium | High | MFA, password resets, session timeouts |
| Privacy violation | Medium | High | Consent management, anonymization, data retention |

## Security Controls (By Layer)

### Layer 1: Authentication & Access Control

**Client dashboard access:**
- OAuth 2.0 (SSO via client's identity provider, or Supabase Auth)
- Multi-factor authentication (MFA) required for admin accounts
- Session timeout (15 minutes of inactivity)
- Password policy (12+ characters, complexity requirements)

**API access (for data subscribers):**
- API keys with individual rate limits
- Key rotation required every 90 days
- IP allowlisting (restrict API calls to known IP ranges)
- Scoped permissions (API key can read data but not modify)

**Internal Olytic access:**
- GitHub-based access (SSO via GitHub)
- All database access via IAM roles, not shared passwords
- Separation of duties (one person writes code, another deploys)
- Time-limited access (can request elevated permissions, expires after 8 hours)

**Detection:**
- Log all authentication events (login, logout, failed attempts, MFA challenges)
- Alert on suspicious patterns (10+ failed logins from same IP)
- Monitor API key usage (alert if key suddenly requests 10x normal volume)

### Layer 2: Data Encryption

**Data at rest (in Supabase):**
- Supabase provides encryption by default (AES-256)
- Additional application-layer encryption for sensitive fields (PII, CRM identifiers)
- Encryption keys stored in AWS Secrets Manager (managed by Supabase)

**Data in transit:**
- All API endpoints use HTTPS (TLS 1.2+)
- Internal communication between services uses mTLS (mutual TLS certificates)

**Backup encryption:**
- Supabase backups are encrypted
- Retention policy: 30-day backup retention, automatic purge after 30 days
- Encryption keys for backups stored separately from backup data

**Encryption key management:**
- Keys rotated annually (recommended by security best practices)
- Old keys retained for decryption of archived data
- Key rotation doesn't require application downtime

### Layer 3: Data Isolation & Row-Level Security (RLS)

**Multi-tenant isolation (clients can't see each other's data):**
```
-- Every data table has org_id
ALTER TABLE plugin_activity_event ENABLE ROW LEVEL SECURITY;

-- Policy: A user can only see rows for their org
CREATE POLICY org_isolation ON plugin_activity_event
  AS RESTRICTIVE
  USING (org_id = (SELECT org_id FROM client_users WHERE user_id = auth.uid()));
```

**Role-based access:**
- Admin role: full read/write access to org data
- Analyst role: read-only access to activity, outcomes, sentiment
- Viewer role: read-only access to aggregated dashboards only
- No direct database access (all queries go through API with RLS enforcement)

**Verification:**
- Unit tests that verify a user can't query another org's data
- Regular audits (monthly query review)

### Layer 4: Audit Logging

Every action that touches data must be logged:

```
audit_log
├── timestamp (when)
├── user_id (who)
├── action (what: SELECT, INSERT, UPDATE, DELETE)
├── table_name (which table)
├── record_id (which specific row)
├── org_id (which client)
├── ip_address (where from)
├── user_agent (what client)
└── success (did it work?)
```

**What triggers an audit log entry:**
- Login/logout
- API key creation or rotation
- Data query (if querying another org's data)
- Data modification (insert, update, delete)
- Consent change (client opts in/out of data sharing)
- Data export (client downloads raw data)
- User role change (promote to admin, etc.)

**Access to audit logs:**
- Only Olytic ops/security team can read audit logs
- Clients can request a copy of their audit logs (GDPR subject access request)
- Audit logs are immutable (can't be modified, only appended)

### Layer 5: Network Security

**Supabase network isolation:**
- Direct database connections only from Olytic servers (no public internet access)
- API endpoint requires authentication (no anonymous access)
- DDoS protection via Cloudflare (or similar)
- WAF (Web Application Firewall) rules to block common attacks

**Plugin-to-platform communication:**
- Plugins send data to Olytic API via HTTPS
- API validates all incoming data (schema, size limits, rate limits)
- Failed requests logged and alerted on

**Third-party integrations (CRM, BI tools):**
- OAuth for any third-party integration (CRM connector, BI tool)
- Scoped permissions (CRM connector can only read deal/contact records, not modify)
- Regular audit of active integrations (quarterly review)

### Layer 6: Application-Level Defenses

**Input validation:**
- All API inputs validated against schema (reject invalid data, log anomalies)
- SQL injection prevention (use parameterized queries, ORM)
- XSS prevention (sanitize all user-generated content in UI)

**Rate limiting:**
- API rate limits (1000 requests/minute per API key)
- Per-user limits (prevent one user from monopolizing resources)
- Graceful degradation (queue requests when limit exceeded, don't fail)

**Error handling:**
- Don't expose sensitive information in error messages
- Log detailed errors internally; show generic messages to users
- Example: user sees "Error: Invalid request", ops sees "SQL error: column 'email' doesn't exist"

## Compliance Framework

### SOC 2 Type II

**What it means:** Olytic has documented and tested controls for security, availability, and confidentiality of client data.

**What Olytic needs:**
- [ ] Documented information security policy
- [ ] Access control policy (who can access what data, how)
- [ ] Incident response plan (what do we do if there's a breach?)
- [ ] Change management policy (how do we safely deploy changes?)
- [ ] Audit logs for all access and changes
- [ ] Annual independent audit (hire Big 4 firm to test controls)

**Effort:** ~40 hours of documentation + $10K–$30K for annual audit

**Timeline:** Can be ready in 3–4 months if starting from scratch

**Why it matters:** Enterprise customers often require SOC 2 compliance from vendors. It's a commercial gating item.

### GDPR (General Data Protection Regulation)

**What it means:** If any European clients share data, that data is subject to GDPR rules.

**Key obligations:**
- **Consent:** Client must explicitly consent to data sharing (not just implied)
- **Data subject rights:** Individuals referenced in data have the right to access, modify, delete their data
- **Data processing agreement (DPA):** Contract between Olytic and client that defines data handling
- **Right to deletion:** If a user says "delete my data," Olytic must comply

**What Olytic needs:**
- [ ] Consent forms (explicit checkbox: "I agree to share plugin usage data with Olytic")
- [ ] Data processing agreement (template for client to sign)
- [ ] Deletion capability (ability to purge a user's records from the system)
- [ ] Breach notification process (notify affected users within 72 hours of discovery)

**Effort:** ~20 hours of template creation + coordination with counsel

**Timeline:** Can be ready in 2 weeks

**Why it matters:** Olytic needs to be able to say "we handle GDPR-covered data correctly." This unlocks European clients.

### CCPA (California Consumer Privacy Act)

**Similar to GDPR but less onerous:**
- Residents of California have right to know what data is collected
- Right to delete their personal data
- Right to opt out of data "sales" (sharing with third parties)

**What Olytic needs:**
- [ ] Privacy policy update (disclose data collection and third-party sharing)
- [ ] Opt-out mechanism (users can request not to have their data licensed)
- [ ] Consumer request process (fulfill deletion requests within 45 days)

**Effort:** ~10 hours

**Timeline:** Can be ready in 1 week

**Why it matters:** Protects Olytic from liability if California-based clients or individuals are affected.

## Trust Architecture (Product-Level Design)

Beyond compliance controls, design the product itself to build trust:

### 1. Transparency Dashboard

Every client sees:
- Exactly what data Olytic has collected about their organization
- How much data (number of events, outcomes, sentiment entries)
- Who has accessed their data (download audit log)
- What they've consented to share and what they've opted out of

**Design principle:** Clients never wonder what data Olytic has. It's all visible.

### 2. Granular Consent

Clients don't do binary "opt in" or "opt out." Instead:

```
Consent Configuration
├── ✓ Activity tracking (plugin invocations, feature usage)
├── ✓ Outcome attribution (linking activities to business results)
├── ✗ CRM linkage (don't connect to our Salesforce)
├── ✓ Sentiment capture (user feedback)
├── ✗ Third-party data sharing (don't sell/license our data)
└── ✓ Benchmarking (compare us to peer companies)
```

**Design principle:** Control at the data-category level. Clients decide what they're comfortable sharing.

### 3. Anonymization Guarantees

Clients want to know: "If Olytic licenses aggregated data to a third party, can they identify my company?"

**Guarantee:** "No. Aggregated reports show data across 50+ companies. Individual companies are never identifiable. We also apply k-anonymity (any data point appears in at least 5 companies) before licensing."

**Implementation:**
- Verify k-anonymity before publishing any aggregated report
- Implement and test anonymization in code (automated verification)
- Show clients the anonymization process (demystify it)

### 4. Deletion Capability

Clients need to know: "If we want Olytic to delete our data, can you actually do it?"

**Guarantee:** "Yes. You can request deletion any time. We'll purge all your data within 30 days. You'll see it removed from your dashboard immediately."

**Implementation:**
- Soft delete (mark rows as deleted, don't actually remove until 90 days later)
- Cascading delete (delete org record, which cascades to all related records)
- Verification (client can query dashboard to confirm deletion)

### 5. Incident Response Communication

If there's ever a security incident:

**Day 0:** Detect breach (unusual access pattern, failed intrusion detection alert)
**Day 0-1:** Investigate (who was affected? what data? how did they gain access?)
**Day 1:** Notify affected clients (within 24 hours of discovery)
**Day 2-7:** Remediate (apply patches, reset credentials, revoke compromised keys)
**Day 7+:** Post-mortem (publish what happened and what we changed)

**Design principle:** Transparency over silence. Clients trust vendors who communicate about failures and fix them.

## Olytic-Specific Standards

Gaudi recommends that Olytic define and publish these security standards (not industry standards, but Olytic-specific):

### Standard 1: The Data Custody Principle

"Olytic holds client data in trust. Our first obligation is to the clients whose data we hold, not to Olytic's commercial interests. When there's a conflict between profitability and client privacy, privacy wins."

**Operationalizes as:** No data licensing without explicit consent. No feature that risks client privacy.

### Standard 2: The Transparency Principle

"Clients always know what data we have, who's accessing it, and how we're using it. There's no opaque data processing."

**Operationalizes as:** Consent is granular, audit logs are client-visible, anonymization is explainable.

### Standard 3: The Data Minimization Principle

"We collect only the data we need to solve the problem. We don't collect 'just in case.'"

**Operationalizes as:** Schema design asks "do we need this field?" before adding. Retention policies automatically delete old data.

### Standard 4: The Deletion Principle

"Clients own their data. If they ask for it deleted, we delete it, no exceptions."

**Operationalizes as:** Deletion is built into the schema design, not bolted on. Regular deletion tests (monthly, we actually try to delete data and verify it's gone).

## Operating Principles

- **Discovery first:** Before finalizing security architecture, talk to target buyers (especially PE firms and large SMBs). Understand what security controls they require to feel safe.
- **Source of truth:** Once you publish an Olytic security standard (e.g., "we delete data within 30 days on request"), that becomes your commitment. Design systems to meet it.
- **Atomic operations:** Implement security controls incrementally. MVP might be basic encryption + audit logging. Add MFA, DPA, SOC 2 sequentially as you scale.
- **Verify after writing:** Don't just design controls; test them. Monthly: try to exfiltrate data, verify audit logs catch it. Quarterly: conduct a mini security review.
- **No hallucination:** If security architecture depends on a feature Supabase provides (e.g., RLS), confirm it works before designing around it.

## Boundaries

This skill should NOT be used for:

- Designing operational security (how to patch systems, incident response drills, etc.) — that's DevOps/SRE
- Writing legal compliance documents or contracts — that's counsel domain
- Designing cryptographic algorithms (use industry-standard libraries, don't invent)
- Setting security policy unilaterally — this must be collaborative with technical and legal stakeholders

If a request falls outside these boundaries, explain why and suggest the appropriate alternative.

## References

For complementary guidance:
- **Data schema and consent enforcement:** See data-modeling skill
- **Privacy and anonymization techniques:** See data-privacy skill
- **User experience of trust controls:** See user-experience skill
- **Full-stack implementation:** See full-stack-engineering agent

---

Telemetry: This skill logs all invocations via plugin-telemetry.
