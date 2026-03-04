# Claude Desktop Config — Fixed Versions

The `"disconnected"` error means Claude can't find `npx` because the app doesn't
inherit your Mac's PATH. Use whichever option matches your system below.

---

## Option A — Homebrew Node (most common)

```json
{
  "mcpServers": {
    "olytic-telemetry": {
      "command": "/usr/local/bin/npx",
      "args": [
        "-y",
        "@supabase/mcp-server-supabase@latest",
        "--project-ref",
        "kxnmgutidehncnafrwbu",
        "--supabase-access-token",
        "sbp_173d82e4ab04962d954bcd0412a72f07b5a142dd"
      ]
    }
  },
  "preferences": {
    "coworkWebSearchEnabled": false,
    "coworkScheduledTasksEnabled": true,
    "sidebarMode": "task"
  }
}
```

---

## Option B — Apple Silicon Homebrew (M1/M2/M3 Mac)

```json
{
  "mcpServers": {
    "olytic-telemetry": {
      "command": "/opt/homebrew/bin/npx",
      "args": [
        "-y",
        "@supabase/mcp-server-supabase@latest",
        "--project-ref",
        "kxnmgutidehncnafrwbu",
        "--supabase-access-token",
        "sbp_173d82e4ab04962d954bcd0412a72f07b5a142dd"
      ]
    }
  },
  "preferences": {
    "coworkWebSearchEnabled": false,
    "coworkScheduledTasksEnabled": true,
    "sidebarMode": "task"
  }
}
```

---

## How to find your exact path

Open Terminal and run:
```
which npx
```

Use whatever path it returns as the `"command"` value.

If `which npx` returns nothing, Node.js isn't installed. Install it from
https://nodejs.org (LTS version) then retry.
