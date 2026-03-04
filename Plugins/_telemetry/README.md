# Olytic Telemetry System

> **⚠ DEPRECATED — DO NOT USE**
>
> This folder (`startup.py`, `hooks/hooks.json`) represents the **retired staging-file approach** to telemetry. It is archived here for reference only. The architecture was replaced because Claude's Bash tool runs in a VM sandbox and cannot write to `~/.claude/telemetry/` on the user's Mac. Local file staging never worked.
>
> **Current architecture:** Plugins call `mcp__olytic-telemetry__log-telemetry` directly. Events are inserted into Supabase in real time. No local files, no startup script, no hooks required.

---

## Why This Approach Was Retired

The staging-file design assumed Claude could write to `~/.claude/telemetry/` on the host machine. In reality, Claude's Bash tool runs inside a Linux VM sandbox — writes go to the VM filesystem, which resets between sessions. Telemetry files were never accumulating on the Mac.

## Current Architecture

All four plugins (`gaudi`, `aule`, `magneto`, `the-one-ring`) include a `.mcp.json` that registers the `olytic-telemetry` MCP server:

```json
{
  "mcpServers": {
    "olytic-telemetry": {
      "type": "http",
      "url": "https://kxnmgutidehncnafrwbu.supabase.co/functions/v1/log-telemetry"
    }
  }
}
```

When a plugin skill logs an event, it calls `mcp__olytic-telemetry__log-telemetry` with the event JSON. The Edge Function validates and inserts the row directly into the `telemetry_events` table in Supabase. Real-time, no user setup required.

## Files in This Folder (Archived)

| File | Status |
|------|--------|
| `startup.py` | Retired — batch uploader, no longer needed |
| `hooks/hooks.json` | Retired — SessionStart hook, no longer needed |
| `.env.example` | Retained — documents what credentials are needed (still relevant for other uses) |
| `IMPLEMENTATION-GUIDE.md` | Outdated — describes the retired approach |
