---
name: sync-contracts
trigger: "/sync-contracts"
description: >
  Pulls the latest contract files from the public olytic-contracts GitHub repository and
  updates the local copies in this plugin's contracts/ folder. Run this before repackaging
  and redeploying a new version of olytic-core to your organization.
version: 1.0.0
---

# /sync-contracts

Pulls the latest schemas and protocols from the public `olytic-solutions/olytic-contracts`
GitHub repository and updates the local copies in this plugin.

After running this command, repackage and redeploy `olytic-core` as a new organizational
plugin version. All other plugins will pick up the updated contracts on their next session
without any changes to those plugins.

## Source Repository

All contracts are hosted publicly at:
`https://github.com/olytic-solutions/olytic-contracts`

Raw file base URL:
`https://raw.githubusercontent.com/olytic-solutions/olytic-contracts/main`

## What Gets Synced

### Schemas (`contracts/schemas/`)

| File | Source Path |
|------|-------------|
| `telemetry-event-schema.json` | `schemas/telemetry-event-schema.json` |
| `session-summary-schema.json` | `schemas/session-summary-schema.json` |
| `vault-entry-schema.json` | `schemas/vault-entry-schema.json` |
| `hook-event-schema.json` | `schemas/hook-event-schema.json` |
| `plugin-identity-schema.json` | `schemas/plugin-identity-schema.json` |
| `memory-access-schema.json` | `schemas/memory-access-schema.json` |

### Protocols (`contracts/protocols/`)

| File | Source Path |
|------|-------------|
| `plugin-standards.md` | `protocols/plugin-standards.md` |
| `agentic-behavior.md` | `protocols/agentic-behavior.md` |

## Step-by-Step Protocol

**Step 1: Confirm intent.**

Tell the user:
> "I'll pull the latest contracts from `olytic-solutions/olytic-contracts` and update the
> local copies in this plugin. This will overwrite the current contract files. Proceed?"

Wait for explicit confirmation before continuing.

**Step 2: Fetch each file.**

For each file in the sync list above, fetch from:
```
https://raw.githubusercontent.com/olytic-solutions/olytic-contracts/main/[source-path]
```

Fetch all files. Do not stop on a single failure — complete the full list and report
failures at the end.

**Step 3: Validate each fetched file.**

For JSON schema files:
- Must be valid JSON (parseable)
- Must contain a `$schema` or `title` field
- Must not be empty

For Markdown protocol files:
- Must be non-empty
- Must contain a heading (`#`)

If validation fails for a file, keep the existing local copy and flag it in the report.

**Step 4: Write validated files to disk.**

Write each validated file to its local path within this plugin:
```
contracts/schemas/[filename]
contracts/protocols/[filename]
```

Overwrite existing files. Do not delete files that are not in the sync list.

**Step 5: Report results.**

Show a summary table:

| File | Status | Notes |
|------|--------|-------|
| telemetry-event-schema.json | ✓ Updated | — |
| session-summary-schema.json | ✓ Updated | — |
| plugin-standards.md | ✗ Failed | Fetch returned 404 |
| ... | | |

Then tell the user:
> "Sync complete. [N] files updated, [N] unchanged, [N] failed.
> Next steps:
> 1. Review any failed files above
> 2. Repackage this plugin: ask Aule to repackage olytic-core
> 3. Deploy the new version as an organizational plugin in your Claude org settings"

## Failure Modes

**Repository not found / network error:**
> "Could not reach `github.com/olytic-solutions/olytic-contracts`. Check that the
> repository exists and is public, then try again."
Keep all existing local files unchanged.

**Individual file 404:**
Keep the existing local copy. Flag in the report. Do not abort the rest of the sync.

**Validation failure:**
Keep the existing local copy. Flag in the report with the specific reason.

**Partial sync (some succeeded, some failed):**
Keep all successful updates. Report failures clearly. The plugin is in a mixed state —
tell the user which files are current and which are stale.

## What This Command Does NOT Do

- Does NOT repackage the plugin — that's a separate step after review
- Does NOT deploy to the org — that requires the user to upload the new version
- Does NOT modify any other plugin — only updates files within `olytic-core` itself
- Does NOT pull Aule-internal files (e.g., `aule-core-standards.md`) — those are not in the public repo
