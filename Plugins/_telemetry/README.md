# Olytic Telemetry System

Central configuration and startup process for plugin telemetry.

## Primary Reference

**Read this first:** `telemetry-blueprint/TELEMETRY-STANDARDS.md` (v2.0.0)

This is the single authoritative source for all telemetry standards, architecture, and implementation. It consolidates both specification and architecture in one document.

## Files in This Folder

| File | Purpose |
|------|---------|
| `startup.py` | Startup script — runs on session start to send telemetry to Supabase |
| `.env.example` | Credential template — shows what environment variables are needed |
| `hooks/hooks.json` | SessionStart hook configuration — tells Claude when to run startup.py |
| `IMPLEMENTATION-GUIDE.md` | Setup and testing instructions for your machine |

## Quick Start

1. **Read:** Start with `IMPLEMENTATION-GUIDE.md`
2. **Configure:** Add real Supabase credentials to `~/Olytic Setup/.env`
3. **Verify:** Run `startup.py` manually to test
4. **Monitor:** Check `~/.claude/telemetry.log` for activity

## Key Concepts

- **Hardcoded path:** `~/.claude/telemetry/` (all plugins write here)
- **Staging:** JSONL files accumulate during the session
- **Transmission:** On next session start, startup.py reads and sends to Supabase
- **Cleanup:** Local files deleted after successful transmission

## Status

✅ Framework complete and integrated
✅ Blueprint updated (v1.1.0)
✅ Plugin skills updated (gaudi, aule)
✅ Startup script ready
✅ SessionStart hook configured

Ready for plugin integration.
