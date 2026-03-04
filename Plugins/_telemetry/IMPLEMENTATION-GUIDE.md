# Olytic Telemetry Implementation Guide

**Date:** March 4, 2026
**Owner:** Aulë
**Status:** Ready for Integration

---

## Overview

The telemetry framework is now fully configured and hardcoded. All plugins must implement this system to collect usage data, which feeds the compounding loop that powers Olytic's optimization engine.

---

## What Was Configured

### 1. ✅ Hardcoded Telemetry Path

**Location:** `~/.claude/telemetry/`

This path is:
- Universal across all plugins (no environment variables needed)
- Flat structure (no subdirectories per plugin)
- Where plugins write JSONL files during sessions
- Monitored by the startup process on next session start

### 2. ✅ Updated Telemetry Blueprint

**File:** `telemetry-blueprint/TELEMETRY-STANDARDS.md` (v1.1.0)

Added Section 3.5 documenting:
- The hardcoded path requirement
- Session ID generation
- File naming convention: `{plugin_name}-{session_id}.jsonl`
- Append-only behavior
- Complete lifecycle flow

### 3. ✅ Updated Plugin Telemetry Skills

**Updated Files:**
- `Plugins/gaudi/src-gaudi/skills/plugin-telemetry/SKILL.md` (v0.2.0)
- `Plugins/aule/src-aule/skills/plugin-telemetry/SKILL.md` (v0.2.0)

Both now include:
- Frontmatter with `telemetry_path: "~/.claude/telemetry/"`
- Session ID requirement declaration
- Step-by-step instructions for writing logs to the hardcoded path

### 4. ✅ Startup Script (startup.py)

**Location:** `Plugins/_telemetry/startup.py`

Functionality:
- Runs automatically on Claude Cowork session start (via SessionStart hook)
- Reads all .jsonl files from `~/.claude/telemetry/`
- Loads Supabase credentials from `~/Olytic Setup/.env`
- Sends events to Supabase telemetry_events table
- Deletes local files after successful transmission
- Logs all activity to `~/.claude/telemetry.log`

### 5. ✅ SessionStart Hook Configuration

**Location:** `Plugins/_telemetry/hooks/hooks.json`

Declares:
- Hook name: `telemetry-startup`
- Trigger: SessionStart (automatic when Claude launches)
- Script: Points to `startup.py`
- Retry logic: Up to 2 retries if transmission fails
- Timeout: 30 seconds

### 6. ✅ Credential Template

**Location:** `Plugins/_telemetry/.env.example`

Template showing:
- `SUPABASE_URL` — Project URL
- `SUPABASE_API_KEY` — Service role or anon key

**Storage:** Real credentials stored in `~/Olytic Setup/.env` (not in git)

---

## How Plugins Implement This

### Step 1: Generate/Retrieve Session ID

At the start of each Claude session, plugins must generate a unique session ID:

```python
import os
import secrets

session_id = os.environ.get('CLAUDE_SESSION_ID')
if not session_id:
    session_id = f"sess_{secrets.token_hex(8)}"
    # Store for this session
    os.environ['CLAUDE_SESSION_ID'] = session_id
```

### Step 2: Write Telemetry Events

When an event occurs (skill invoked, decision made, violation detected, etc.), write JSONL to the staging folder:

```python
import json
from pathlib import Path
from datetime import datetime, timezone

telemetry_dir = Path.home() / '.claude' / 'telemetry'
telemetry_dir.mkdir(parents=True, exist_ok=True)

# Construct filename
filename = telemetry_dir / f"{plugin_name}-{session_id}.jsonl"

# Build event object
event = {
    "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
    "event": "skill_invoke",
    "plugin": "gaudi",
    "plugin_version": "0.2.0",
    "component": "data-modeling",
    "trigger": "user asked to design the schema"
}

# Append to file (JSONL format — one object per line)
with open(filename, 'a') as f:
    f.write(json.dumps(event, separators=(',', ':')) + '\n')
```

### Step 3: The Startup Process Handles the Rest

On next Claude session start:
1. SessionStart hook fires → calls startup.py
2. startup.py reads `~/.claude/telemetry/*.jsonl`
3. Parses all JSONL events
4. Authenticates to Supabase with credentials from `~/Olytic Setup/.env`
5. POSTs events to the `telemetry_events` table
6. Deletes local files after successful transmission
7. Logs activity to `~/.claude/telemetry.log`

**Result:** Telemetry automatically flows to Supabase without any manual intervention.

---

## File Structure

```
~/.claude/
├── telemetry/                    # Staging folder (created)
│   ├── aule-sess_abc123.jsonl   # Session 1
│   ├── gaudi-sess_abc123.jsonl  # Session 1
│   └── ...
└── telemetry.log                 # Startup logs

Plugins/
└── _telemetry/
    ├── TELEMETRY-FRAMEWORK.md
    ├── IMPLEMENTATION-GUIDE.md   # This file
    ├── startup.py                # Session startup script
    ├── .env.example              # Credential template
    └── hooks/
        └── hooks.json            # SessionStart hook config

telemetry-blueprint/
└── TELEMETRY-STANDARDS.md (v1.1.0)  # Updated with path

Plugins/gaudi/src-gaudi/skills/plugin-telemetry/
└── SKILL.md (v0.2.0)             # Updated with path

Plugins/aule/src-aule/skills/plugin-telemetry/
└── SKILL.md (v0.2.0)             # Updated with path
```

---

## Credentials Setup (One-Time)

**Action Required:** Copy the actual Supabase credentials to the desktop:

```bash
# On your computer (replace with actual values)
~/Olytic Setup/.env

SUPABASE_URL=https://your-actual-project.supabase.co
SUPABASE_API_KEY=sb_your_actual_api_key_here
```

This file is:
- ✅ Used by startup.py to authenticate
- ❌ NOT in git (add to .gitignore if needed)
- ✅ In a location separate from the working folder (for security)

---

## Testing the Flow

### Test 1: Verify telemetry directory exists

```bash
ls -la ~/.claude/telemetry/
# Should exist and be empty
```

### Test 2: Manually create a test telemetry file

```bash
cat >> ~/.claude/telemetry/test-telemetry-sess_test123.jsonl << 'EOF'
{"timestamp":"2026-03-04T10:00:00Z","event":"skill_invoke","plugin":"test","plugin_version":"0.1.0","component":"test","trigger":"test event"}
EOF
```

### Test 3: Run the startup script manually

```bash
python3 ~/path/to/Plugins/_telemetry/startup.py
```

Should output:
- "Credentials loaded successfully"
- "Found 1 telemetry file(s)"
- "Read 1 events"
- "Successfully sent 1 events to Supabase" (if credentials are valid)
- "Deleted test-telemetry-sess_test123.jsonl"

### Test 4: Verify logs

```bash
cat ~/.claude/telemetry.log
```

Should show startup process logs.

---

## Next Steps for Plugins

### For Existing Plugins (Gaudi, Magneto, The One Ring, Aule)

1. **Update plugin-telemetry skills** — Add telemetry path instructions (DONE for gaudi and aule)
2. **Integrate telemetry writing** — Plugins must call the telemetry writer when events occur
3. **Test with startup script** — Verify logs are created and sent

### For New Plugins Generated by Aule

1. Aule's generation template automatically includes:
   - plugin-telemetry skill with hardcoded path
   - Instructions to write to `~/.claude/telemetry/`
   - Session ID handling in the README
2. No additional configuration needed

---

## Troubleshooting

### "telemetry.log shows: Credentials not found"

**Solution:** Ensure `~/Olytic Setup/.env` exists with valid credentials:
```bash
cat ~/Olytic\ Setup/.env
```

### "startup.py doesn't delete files after transmission"

**Possible reasons:**
- File permissions issue
- Supabase transmission failed (check logs)
- File is open elsewhere

Check logs:
```bash
tail -20 ~/.claude/telemetry.log
```

### "Supabase returns 401 or 403"

**Possible reasons:**
- API key is invalid or revoked
- API key doesn't have INSERT permission on telemetry_events table
- URL is incorrect

**Solution:** Verify credentials in `~/Olytic Setup/.env` match Supabase project.

---

## Success Indicators

You'll know telemetry is working when:

✅ Files appear in `~/.claude/telemetry/` during sessions
✅ Files have JSONL content with proper event structure
✅ Startup script runs without errors (check logs)
✅ Files are deleted after startup
✅ Supabase dashboard shows new rows in telemetry_events table
✅ Session logs appear in `~/.claude/telemetry.log`

---

## Notes

- **Versioning:** Blueprint is v1.1.0, plugin-telemetry skills are v0.2.0
- **Backwards Compatibility:** Older plugins can still work; they'll just not send telemetry until updated
- **Silent by Default:** Telemetry writing doesn't appear in user-facing output
- **Violations Surface:** When plugins detect constraint violations, they DO explain to users

---

## Questions?

Refer to:
- `telemetry-blueprint/TELEMETRY-STANDARDS.md` — Canonical standard
- `Plugins/_telemetry/TELEMETRY-FRAMEWORK.md` — Architecture overview
- Plugin-telemetry skills — Event-specific implementation details
