# Olytic Internal Telemetry Connector — Setup Reference

## Org Details
- **Org ID:** `olytic-internal`
- **Supabase Project:** Olytic Telemetry (`kxnmgutidehncnafrwbu`)
- **Project URL:** `https://kxnmgutidehncnafrwbu.supabase.co`

---

## Org-Scoped JWT (valid until 2035-01-01)

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt4bm1ndXRpZGVobmNuYWZyd2J1Iiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJvcmdfaWQiOiJvbHl0aWMtaW50ZXJuYWwiLCJpYXQiOjE3NzI2Mzc2NDQsImV4cCI6MjA1MTIyMjQwMH0.NUvXL99EfKf6CCKpsdDreyTr70Lhf0CJ6KlKatXbycg
```

**Claims encoded in this JWT:**
- `role`: authenticated
- `org_id`: olytic-internal
- `iss`: supabase
- `ref`: kxnmgutidehncnafrwbu
- Issued: 2026-03-04 · Expires: 2035-01-01

> **Store this JWT securely.** It is the credential that authorises inserts into
> `telemetry_events` scoped to `org_id = 'olytic-internal'`. Treat it like a
> password — do not commit it to version control.

---

## Claude Desktop Config Snippet

Add this block to your `claude_desktop_config.json` under `"mcpServers"`:

```json
"olytic-telemetry": {
  "command": "npx",
  "args": [
    "-y",
    "@supabase/mcp-server-supabase@latest",
    "--read-only",
    "--project-ref", "kxnmgutidehncnafrwbu",
    "--supabase-access-token", "PASTE_YOUR_SUPABASE_PERSONAL_ACCESS_TOKEN_HERE"
  ]
}
```

> **Note on access token:** The Supabase MCP server uses your **personal access token**
> (not the service role key). Get it from:
> https://supabase.com/dashboard/account/tokens
> Create a token named "Claude Desktop – Olytic Telemetry".

The org-scoped JWT above is used **inside plugin skills** as the `Authorization: Bearer`
header when calling the Supabase REST API directly. See INSERT pattern below.

---

## Plugin INSERT Pattern (use in all telemetry SKILL.md files)

```sql
INSERT INTO telemetry_events (timestamp, event, plugin, plugin_version, org_id, user_id, component, trigger)
VALUES (NOW(), '[EVENT]', '[PLUGIN]', '[VERSION]', 'olytic-internal', '[USER_ID]', '[COMPONENT]', '[TRIGGER]');
```

The org_id `'olytic-internal'` should be hardcoded in Olytic's own plugin installs.
`user_id` remains dynamic — set to the session user's identifier at runtime.

---

## Smoke Test

Once the connector is installed, run this from any Claude session to verify:

```sql
INSERT INTO telemetry_events (timestamp, event, plugin, plugin_version, org_id, user_id, component, trigger)
VALUES (NOW(), 'skill_invoke', 'test', '0.0.0', 'olytic-internal', 'support@olyticsolutions.com', 'smoke-test', 'manual connector verification');
```

Then confirm the row landed:

```sql
SELECT id, timestamp, event, plugin, org_id, user_id, component
FROM telemetry_events
WHERE org_id = 'olytic-internal'
ORDER BY created_at DESC
LIMIT 5;
```

---

## Future Client Onboarding Pattern

For each new client org, you will:

1. Choose their org_id: `client-[shortname]` (e.g. `client-acme`)
2. Mint a new JWT using the same JWT Secret, with `"org_id": "client-[shortname]"`
3. Install their Cowork connector with their org's personal access token
4. Hardcode their `org_id` in their plugin telemetry skills

The same Supabase project handles all orgs. RLS enforces isolation — no client
can read or write another client's rows.

---

## JWT Minting Command (for future orgs)

```bash
node -e "
const crypto = require('crypto');
const header = { alg: 'HS256', typ: 'JWT' };
const now = Math.floor(Date.now() / 1000);
const payload = {
  iss: 'supabase',
  ref: 'kxnmgutidehncnafrwbu',
  role: 'authenticated',
  org_id: 'CLIENT_ORG_ID_HERE',
  iat: now,
  exp: 2051222400
};
const secret = 'YOUR_JWT_SECRET';
const b64url = (obj) => Buffer.from(JSON.stringify(obj)).toString('base64url');
const headerB64 = b64url(header);
const payloadB64 = b64url(payload);
const sig = crypto.createHmac('sha256', secret).update(headerB64+'.'+payloadB64).digest('base64url');
console.log(headerB64+'.'+payloadB64+'.'+sig);
"
```
