# Platform File Formats

Per-platform format specifications for Olytic plugins. Read this file when generating, packaging, or validating plugins for any target platform. Never cache — always read fresh at invocation.

---

## Overview

Olytic plugins can be deployed to multiple AI assistant platforms. Each platform has a different convention for how plugin manifests, skill files, and packaging should be structured. This reference documents the authoritative format for each supported platform.

---

## Platform 1: Claude (Anthropic) — Native Format

**File identifier:** `.claude-plugin/plugin.json`

**Plugin manifest (`plugin.json`):**
```json
{
  "name": "kebab-case-name",
  "version": "0.1.0",
  "description": "One sentence — under 120 characters.",
  "author": {
    "name": "Olytic Solutions",
    "email": "support@olyticsolutions.com"
  },
  "keywords": ["keyword1", "keyword2"],
  "hooks": "hooks/hooks.json",
  "connectors": [
    { "id": "connector-id", "required": true, "scopes": ["read:resource"] }
  ],
  "sublabel": "1-3 Word Descriptor",
  "icon": "🔧"
}
```

**Valid keys:** `name`, `version`, `description`, `author`, `keywords`, `hooks`, `connectors`, `sublabel`, `icon`. No additional keys — unrecognized keys cause upload validation failure.

**Skill files:** `SKILL.md` — Markdown with YAML frontmatter (`name`, `description`, `version`, optional `hook`). The `description` field is the activation trigger — Claude reads it to decide when to load the skill.

**Hooks:** `hooks/hooks.json` — JSON with PostToolUse, UserPromptSubmit, SessionClose, PreToolUse event types.

**Packaging:** `.zip` archive of the entire `src-[plugin-name]/` folder. The `.claude-plugin/plugin.json` must be at the archive root's `.claude-plugin/` path.

**Upload target:** Claude.ai plugin marketplace or workspace installation.

---

## Platform 2: Microsoft Copilot — MCP Format

**File identifier:** `mcp.json` or `.mcp/manifest.json`

**Plugin manifest (`mcp.json`):**
```json
{
  "schema_version": "1.0",
  "name_for_human": "Plugin Display Name",
  "name_for_model": "plugin-kebab-name",
  "description_for_human": "User-facing description.",
  "description_for_model": "Model-facing instructions for when to use this plugin.",
  "auth": {
    "type": "none"
  },
  "api": {
    "type": "openapi",
    "url": "https://api.example.com/openapi.yaml"
  }
}
```

**Key differences from Claude format:**
- Split `description_for_human` (marketing copy) vs. `description_for_model` (routing instructions)
- Requires API spec (OpenAPI YAML) — MCP plugins are API-first, not skill-file-first
- Auth field required even if `"type": "none"`
- No hooks system — event-driven behavior not supported
- Skills are exposed as API endpoints, not Markdown files

**Packaging:** Zip with `mcp.json` at root + OpenAPI spec file.

---

## Platform 3: Google Gemini Enterprise — SDK Format

**File identifier:** `gemini-plugin.yaml`

**Plugin manifest (`gemini-plugin.yaml`):**
```yaml
plugin:
  name: plugin-kebab-name
  version: "0.1.0"
  display_name: "Plugin Display Name"
  description: |
    Multi-line description supported.
    Used for both discovery and routing.
  capabilities:
    - name: capability-name
      description: "What this capability does."
      parameters:
        - name: param_name
          type: string
          required: true
          description: "Parameter description."
  authentication:
    type: api_key
    header: X-API-Key
```

**Key differences from Claude format:**
- YAML manifest (not JSON)
- Capabilities are structured function declarations with typed parameters
- Authentication is declared in the manifest (not connector declarations)
- No hook system — capabilities are invoked explicitly, not triggered by events
- No Markdown skill files — logic lives in API endpoints or inline function specs

**Packaging:** Tar.gz or zip with `gemini-plugin.yaml` at root.

---

## Platform 4: OpenAI ChatGPT — Agent Connector Format

**File identifier:** `openai-plugin.json` (legacy) or Actions schema

**Plugin manifest (Actions `openapi.yaml`):**
```yaml
openapi: "3.0.0"
info:
  title: Plugin Name
  description: Description for ChatGPT to understand when to use this plugin.
  version: "0.1.0"
servers:
  - url: https://api.example.com
paths:
  /capability:
    post:
      operationId: capability_name
      summary: "What this endpoint does."
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                input:
                  type: string
      responses:
        "200":
          description: Success response
```

**Key differences from Claude format:**
- OpenAPI spec drives everything — no separate manifest file
- Plugins are API-first: all capabilities are HTTP endpoints
- No hook system
- `operationId` becomes the function name ChatGPT calls
- Auth configured separately in ChatGPT UI, not in spec
- Description in `info.description` is the routing instruction for the model

**Packaging:** OpenAPI YAML file + server deployment. No zip required.

---

## Cross-Platform Compatibility Notes

When generating a plugin for multi-platform deployment:

1. **Start with Claude format** (native) — it's the richest and most expressive
2. **Claude skills → MCP/Actions endpoints:** Each skill becomes an API endpoint; skill description becomes `description_for_model` / `summary`
3. **Hooks have no equivalent** on other platforms — document hook behaviors in the API description instead
4. **Connectors → Auth:** Claude connector declarations map to auth configurations on other platforms
5. **Markdown frontmatter** is Claude-specific — strip YAML headers when generating for other platforms

---

## Packaging Rules (All Platforms)

| Platform | Archive Format | Manifest Location | Skills Format |
|----------|---------------|-------------------|---------------|
| Claude | `.zip` | `.claude-plugin/plugin.json` | `skills/*/SKILL.md` |
| Copilot (MCP) | `.zip` | `mcp.json` | API endpoints |
| Gemini Enterprise | `.tar.gz` or `.zip` | `gemini-plugin.yaml` | API endpoints |
| ChatGPT | N/A (deploy) | `openapi.yaml` | API endpoints |

---

## Reference Relationships

This file is read by:
- `plugin-generation/SKILL.md` — Step 4 (generating plugin.json and structure)
- `aule-plugin-repackager/SKILL.md` — when packaging for a specific target platform
- `plugin-discovery/SKILL.md` — Q8/Q9 (target platform selection)

For the plugin identity data shape, see: `olytic-core/contracts/schemas/plugin-identity-schema.json`
