I need help troubleshooting a broken Supabase MCP connector in Claude desktop.

Please start by reading the following files so you have full context:

1. Read `~/.npm/_npx/` — list all directories in it so we can find the cached version of `@supabase/mcp-server-supabase`
2. Find and read the `package.json` inside the cached `@supabase/mcp-server-supabase` package to get the exact version installed
3. Find and read the main entrypoint (likely `dist/transports/stdio.js` or similar) and look for what CLI flags it accepts
4. Read `~/Library/Application Support/Claude/claude_desktop_config.json` so you can see the current connector config

## Background

I'm trying to connect Claude desktop to a Supabase project via the `@supabase/mcp-server-supabase` MCP server. The connector shows as "disconnected" in Claude. When I run the command manually in Terminal I get this error:

```
TypeError [ERR_PARSE_ARGS_UNKNOWN_OPTION]: Unknown option '--supabase-access-token'
```

So the `--supabase-access-token` flag is not valid for the version that got cached on my machine. I need you to:

1. Find the exact version of `@supabase/mcp-server-supabase` that is cached
2. Read the source to find the correct flag names it actually accepts
3. Give me the corrected `claude_desktop_config.json` block with the right flags
4. Confirm the correct `npx` path to use (nvm is installed at `~/.nvm`, node v20.20.0)

## Current (broken) config block

```json
"olytic-telemetry": {
  "command": "/Users/joshuakambour/.nvm/versions/node/v20.20.0/bin/npx",
  "args": [
    "-y",
    "@supabase/mcp-server-supabase@latest",
    "--project-ref",
    "kxnmgutidehncnafrwbu",
    "--supabase-access-token",
    "sbp_173d82e4ab04962d954bcd0412a72f07b5a142dd"
  ]
}
```

Please read the actual files, find the correct flags, and give me the fixed config block ready to paste.
