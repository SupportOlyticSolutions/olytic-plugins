# olytic-core

**Olytic's shared contracts library.** Install this plugin first in every org before installing any other Olytic plugin.

## What This Is

`olytic-core` is a standards dependency, not an actor. It has no skills, no agents, and no automated behavior. It exists solely to provide a stable, locally-resolvable set of contract files that all other Olytic plugins reference at runtime.

Think of it as the runtime library that every other plugin imports from.

## What's Inside

```
contracts/
├── schemas/
│   ├── telemetry-event-schema.json     ← Shape of all telemetry events
│   ├── session-summary-schema.json     ← Shape of session summaries written to vault
│   ├── vault-entry-schema.json         ← Envelope structure for vault writes
│   ├── hook-event-schema.json          ← Shape of hook event payloads
│   ├── plugin-identity-schema.json     ← Required fields for plugin.json
│   └── memory-access-schema.json       ← Shape of memory read/write requests
└── protocols/
    ├── plugin-standards.md             ← Design rules for all Olytic plugins
    └── agentic-behavior.md             ← Runtime behavior standards for all agents
```

## How Other Plugins Use It

Plugins reference contracts by name and path, resolved through this plugin at runtime:

```
Read telemetry-event-schema.json from the olytic-core plugin's contracts/schemas/ folder
```

This means: when you update a schema, update `olytic-core` and redeploy it. Every plugin
picks up the new schema on its next session — no changes to individual plugins required.

## How to Update Contracts

When Olytic publishes new contract versions to the public repository:

1. Run `/sync-contracts` — pulls latest from `github.com/olytic-solutions/olytic-contracts`
2. Review the sync report
3. Ask Aule to repackage `olytic-core`
4. Deploy the new version as an organizational plugin in your Claude org settings

All other plugins in the org will use the updated contracts on their next session.

## Source of Truth

All contracts in this plugin are mirrored from the public repository:
**`https://github.com/olytic-solutions/olytic-contracts`**

The public repo is the canonical source. This plugin holds the local copies that
installed plugins resolve against at runtime.

## Installation Order

```
1. olytic-core        ← install first, always
2. olytic-gateway     ← MCP connector (separate, installed at org level)
3. [your plugins]     ← any Olytic organizational plugins
```

Do not install other Olytic plugins before `olytic-core` is present in the org.
