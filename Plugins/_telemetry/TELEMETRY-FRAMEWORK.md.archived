# Olytic Telemetry Framework

**Purpose:** Understand how plugins automatically send structured telemetry data to Supabase, driven by session start hooks and template-based schemas.

---

## Overview

The telemetry framework enables plugins to collect and transmit usage data to Supabase without manual intervention. The system is triggered automatically when Claude Cowork launches, processes any staged telemetry files, and sends them to Supabase in a standardized format.

**Key principle:** Template-driven schema ensures consistency across all plugins while allowing each plugin to define its own metrics.

---

## Architecture

### Three Components

1. **SessionStart Hooks** — Trigger telemetry startup when Claude launches
2. **Telemetry Staging** — Plugins write structured JSON files locally during sessions
3. **Automatic Transmission** — Startup script sends staged files to Supabase on session start

---

## How It Works

### Step 1: Session Initialization (SessionStart Hook)

When Claude Cowork launches, the SessionStart hook in `Plugins/_telemetry/hooks/hooks.json` fires automatically:

```json
{
  "hooks": {
    "SessionStart": {
      "invoke": "telemetry-startup",
      "description": "Check for staged telemetry files and send to Supabase"
    }
  }
}
```

No user action required. This is transparent and immediate.

### Step 2: Startup Script Execution

The telemetry startup script (`Plugins/_telemetry/startup.sh` or equivalent) performs these steps:

1. **Check for staged files** — Look in the local telemetry folder for `.json` files
2. **Read file contents** — Parse each staged telemetry file
3. **Authenticate to Supabase** — Use credentials from `.env` (not committed to git)
4. **Send to Supabase** — POST each file's data to the configured Supabase endpoint
5. **Clear local files** — Delete staged files after successful transmission
6. **Log the operation** — Record what was sent and when

### Step 3: Plugin Telemetry Collection (During Session)

During the session, plugins write telemetry events following the Aule-defined template. Each plugin's telemetry file contains:

- **session_id** — Unique identifier for this Claude session
- **plugin_id** — Which plugin generated this telemetry
- **timestamp** — When the event occurred
- **event_type** — What happened (e.g., "skill_invoked", "command_executed")
- **event_data** — Structured data about the event (varies by plugin)
- **user_context** — Session context (workspace, project, user identifier if available)

Example telemetry event:

```json
{
  "session_id": "sess_abc123xyz",
  "plugin_id": "aule",
  "timestamp": "2026-03-04T10:30:45Z",
  "event_type": "skill_generated",
  "event_data": {
    "skill_name": "aule-change-analyzer",
    "tokens_used": 1250,
    "duration_ms": 3400,
    "success": true
  },
  "user_context": {
    "workspace": "olytic-plugins",
    "project": "Aule Phase 2"
  }
}
```

---

## Local File Storage

### Directory Structure

```
Plugins/_telemetry/
├── TELEMETRY-FRAMEWORK.md       (this file)
├── hooks/
│   └── hooks.json               (SessionStart hook configuration)
├── startup.sh                    (initialization script)
├── .env.example                  (credential template - placeholders only)
├── .env                          (actual credentials - not in git)
└── staged/
    ├── aule-telemetry-sess_abc.json
    ├── magneto-telemetry-sess_abc.json
    └── gaudi-telemetry-sess_abc.json
```

### Lifecycle of a Telemetry File

1. **Creation** — Plugin writes telemetry JSON to `staged/` during the session
2. **Staging** — File remains in `staged/` until session ends or next startup
3. **Transmission** — On next session start, SessionStart hook triggers startup script
4. **Cleanup** — After successful transmission to Supabase, file is deleted from local storage
5. **Persistence** — Data now exists only in Supabase, not locally

### File Naming Convention

`{plugin-id}-telemetry-{session-id}.json`

Example: `aule-telemetry-sess_abc123xyz789.json`

---

## Template System: Aule as Source of Truth

### Where Templates Are Defined

Aule maintains telemetry schema in:

```
Plugins/aule/src-aule/skills/plugin-generation/references/telemetry-template.md
```

This file defines:
- Required fields every plugin must include
- Optional fields plugins can add
- Data types and validation rules
- Event type categories
- User context requirements

### How Plugins Use Templates

When Aule generates a new plugin, it:

1. Reads the telemetry template from references
2. Includes telemetry-writing instructions in the generated plugin's README
3. Provides a template JSON structure the plugin can use
4. Updates the template if new event types or fields are needed

When plugins write telemetry, they follow this schema exactly. This ensures:
- Consistency across all plugins
- Supabase can expect a predictable schema
- New fields can be added centrally via the template
- All plugins automatically adopt new standards

---

## Supabase Integration

### Configuration

Supabase credentials are stored in `.env` (not in version control):

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_API_KEY=sb_secret_YOUR_ACTUAL_API_KEY_HERE
```

The `.env.example` file contains only placeholders to show what variables are needed.

### Authentication

The startup script authenticates using the API key from `.env`:

```bash
curl -H "Authorization: Bearer $SUPABASE_API_KEY" \
     -H "Content-Type: application/json" \
     -d @telemetry-payload.json \
     https://$SUPABASE_URL/rest/v1/telemetry?insert=multi
```

### Data Storage

All transmitted telemetry is stored in Supabase in a `telemetry_events` table (or equivalent):

| Column | Type | Notes |
|--------|------|-------|
| id | UUID | Auto-generated primary key |
| session_id | TEXT | Unique per Claude session |
| plugin_id | TEXT | Identifies the source plugin |
| timestamp | TIMESTAMP | When the event occurred |
| event_type | TEXT | Category of event |
| event_data | JSONB | Event-specific details |
| user_context | JSONB | Session/workspace context |
| created_at | TIMESTAMP | When record was inserted |

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────┐
│ Claude Cowork Launches                          │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ SessionStart Hook    │
        │ Fires Automatically  │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────────────┐
        │ Startup Script Runs:         │
        │ 1. Find staged .json files   │
        │ 2. Read telemetry data       │
        │ 3. Authenticate to Supabase  │
        │ 4. POST data                 │
        │ 5. Delete local files        │
        └──────────┬───────────────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ Supabase Receives   │
        │ & Stores Telemetry  │
        └─────────────────────┘
                   │
    ┌──────────────┴──────────────┐
    │                             │
    ▼                             ▼
Plugin continues working    Next session starts
Writes more telemetry    (cycle repeats)
```

---

## Example: Complete Telemetry Lifecycle

### Session 1: User Works with Aule Plugin

During the Claude session:
- User invokes aule-change-analyzer skill
- Plugin detects file changes, categorizes them
- Plugin writes telemetry event to `Plugins/_telemetry/staged/aule-telemetry-sess_123.json`
- User continues working; more events accumulate in the same file
- Session ends; telemetry file remains staged locally

### Session 2: User Relaunches Claude

Claude starts:
1. SessionStart hook fires
2. Startup script finds `aule-telemetry-sess_123.json`
3. Script reads all events from that file
4. Script authenticates to Supabase (using credentials from `.env`)
5. Script sends all events to Supabase
6. Supabase stores them in the `telemetry_events` table
7. Script deletes the local file
8. Next time user works, a new telemetry file starts accumulating

---

## Security Considerations

### Credential Management

- **Real credentials are in `.env`** — This file is gitignored and never committed
- **`.env.example` has placeholders only** — Shows what variables are needed without exposing secrets
- **SessionStart hook reads from `.env`** — Credentials are loaded at runtime, not hardcoded
- **API calls use the loaded credentials** — Authentication happens transparently to the user

### Data Minimization

- Only plugin usage events are collected (no user input, no keystroke data)
- User context is limited to workspace/project identifiers
- Sensitive business logic details are not included
- Event data is structured and sanitized before transmission

### Transmission

- All data is sent over HTTPS to Supabase (encrypted in transit)
- Supabase API key is transmitted in the `Authorization` header
- Local files are deleted immediately after successful transmission

---

## Maintenance & Updates

### Adding a New Event Type

When a plugin needs to track a new kind of event:

1. Update `Plugins/aule/src-aule/skills/plugin-generation/references/telemetry-template.md`
2. Add the new event_type and required fields to the template
3. Next time Aule generates a plugin, the template is included
4. Existing plugins can manually adopt the new event type
5. The telemetry startup script automatically handles new fields (JSONB is flexible)

### Rotating Credentials

If Supabase credentials are ever compromised:

1. Rotate the API key in Supabase console
2. Update the value in `.env` (locally only)
3. No git commit needed
4. Next session start will use the new credentials
5. Old credentials stop working immediately

### Monitoring Telemetry Flow

To verify telemetry is working:

1. Check `Plugins/_telemetry/staged/` for staged files
2. Review `.env` has valid Supabase credentials
3. Verify SessionStart hook exists in `hooks.json`
4. Check Supabase dashboard for incoming `telemetry_events` records
5. Verify local files are deleted after transmission

---

## Summary

The telemetry framework is **automatic, secure, and template-driven**:

- ✅ **Automatic** — SessionStart hooks trigger on every launch, no user action
- ✅ **Secure** — Credentials in .env, only placeholders in git
- ✅ **Standardized** — Aule templates ensure consistency
- ✅ **Self-cleaning** — Local files are deleted after transmission
- ✅ **Scalable** — New plugins automatically adopt the framework

Plugins write telemetry during sessions. Next session start sends it to Supabase. No manual steps required.
