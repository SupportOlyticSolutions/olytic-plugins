---
name: olytic-security-policies
description: >
  This skill should be used when the user asks about "security policies",
  "data handling", "client confidentiality", "access controls", "security rules",
  "what can I share", "NDA", or needs guidance on Olytic Solutions' security
  and data protection standards.
version: 0.2.0
---

# Olytic Solutions — Security Policies

> **Trust & Operational Consistency Facet.** Security policies are how Olytic maintains the trust of clients, partners, and the market. Our embedded model means clients give us deep access to their systems and data — handling that responsibly isn't optional. Every rule here exists to protect that trust.

## Data Classification

| Classification | Description | Examples | Handling |
|---------------|-------------|----------|----------|
| **Public** | Intentionally published content | Website pages, blog posts, social media | No restrictions on sharing |
| **Internal** | For Olytic employees only | Strategy docs, OKRs, internal processes | Do not share outside Olytic |
| **Confidential** | Sensitive business information | Client data, pricing models, financials | Share only with authorized personnel |
| **Restricted** | Highest sensitivity | Credentials, API keys, client PII | Encrypted storage, need-to-know only |

## Client Data Rules

- **Never include client names, data, or details in any external content** without explicit written permission
- **Client work product belongs to the client** unless otherwise specified in the SOW
- **Anonymize all examples** used in content, proposals, or presentations — change names, numbers, and identifying details
- **Do not store client credentials** in any plugin, document, or shared resource

## AI Tool Usage

- **Never paste client data into public AI tools** without client consent
- **Use Olytic's configured AI systems** (plugins, Claude, etc.) for client work — these operate within controlled environments
- **Review AI-generated outputs** before sending to clients — the human is always the final quality gate (Governor principle)
- **Do not train external AI models on client data**

## Access Controls

- **GitHub repos:** Access granted per role. Do not share repo access with non-employees.
- **Client systems:** Access only as needed for active engagements. Revoke upon engagement completion.
- **Internal tools:** Use company accounts, not personal accounts.

## Credential Management

- **Never hardcode credentials** in files, plugins, or scripts
- **Use environment variables** for API keys and tokens
- **Rotate credentials** when team members leave or roles change
- **Report suspected credential exposure** immediately

## Communication Security

- **Use company email** for all client communication
- **Do not discuss client specifics** in public channels (social media, public Slack communities, forums)
- **Encrypt sensitive attachments** when sending via email

## Incident Response

If you discover a security issue:

1. Stop the activity immediately
2. Document what happened — what was accessed, what may have been exposed, timeline
3. Notify company leadership immediately — do not wait until you have full clarity
4. Do not attempt to cover up or minimize the issue
5. Work with leadership on notification obligations (clients, affected parties)

The bar for reporting is low. If something looks wrong, say something. The cost of a false alarm is zero. The cost of a delayed response to a real incident is not.
