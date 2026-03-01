---
name: marketplace-management
description: >
  Use this skill when the user wants to "update the marketplace", "add a plugin to
  the marketplace", "register a plugin", "update marketplace.json", "manage the
  Olytic plugin registry", or needs to stage changes to the SupportOlyticSolutions/olytic-plugins
  marketplace repository. Handles reading, diffing, and staging marketplace.json updates.
version: 0.2.0
---

# Marketplace Management — Aulë

Manage the Olytic plugin marketplace at `SupportOlyticSolutions/olytic-plugins`. This skill handles adding new plugins, updating existing entries, and staging changes for review.

**Important:** This skill stages changes for human review. It does NOT auto-merge or auto-push to main.

## Marketplace Location

- **Repository:** `SupportOlyticSolutions/olytic-plugins`
- **File:** `.claude-plugin/marketplace.json`
- **Branch:** `main` (read from), feature branch (write to)

## Marketplace Entry Schema

Each plugin entry in the `plugins` array follows this format:

```json
{
  "name": "kebab-case-plugin-name",
  "source": "./plugin-directory-name",
  "description": "One-sentence description matching plugin.json",
  "version": "0.1.0",
  "keywords": ["keyword1", "keyword2"],
  "category": "category-name"
}
```

**Category values:**
- `governance` — foundational plugins (The One Ring)
- `content` — content creation and strategy
- `sales` — sales enablement and pipeline
- `engineering` — development and technical
- `delivery` — client delivery and consulting
- `operations` — internal operations
- `meta` — plugin management tools (like Aulë)

## How to Add a New Plugin

### Step 1: Read Current Marketplace

Use `mcp__github__get_file_contents` to fetch:
- Owner: `SupportOlyticSolutions`
- Repo: `olytic-plugins`
- Path: `.claude-plugin/marketplace.json`
- Branch: `main`

Parse the JSON and note the current `plugins` array.

### Step 2: Build the New Entry

From the generated plugin's `plugin.json`, create a marketplace entry:

| plugin.json Field | Marketplace Entry Field |
|-------------------|-------------------------|
| `name` | `name` |
| `name` (same value) | `source` (prepend `./`) |
| `description` | `description` |
| `version` | `version` |
| `keywords` | `keywords` |
| (inferred from purpose) | `category` |

### Step 3: Check for Existing Entry

Search the `plugins` array for an entry with the same `name`.

- **If not found:** Add the new entry to the end of the `plugins` array.
- **If found:** Update the existing entry's `description`, `version`, `keywords`, and `category`. Preserve the `source` path.

### Step 4: Show the Diff

Present the changes to the user clearly:

**If adding:**
```
Adding to marketplace:

  + {
  +   "name": "[name]",
  +   "source": "./[name]",
  +   "description": "[description]",
  +   "version": "0.1.0",
  +   "keywords": [...],
  +   "category": "[category]"
  + }
```

**If updating:**
```
Updating marketplace entry for [name]:

  - "version": "0.1.0"
  + "version": "0.2.0"
  - "description": "[old description]"
  + "description": "[new description]"
```

### Step 5: Confirm with User

Ask: "Here's what will change in the marketplace. Should I stage this for review?"

- If yes → proceed to Step 6
- If no → ask what to change, loop back to Step 3

### Step 6: Stage the Changes

1. **Create a feature branch:**
   Use `mcp__github__create_branch` with:
   - Owner: `SupportOlyticSolutions`
   - Repo: `olytic-plugins`
   - Branch: `marketplace/add-[plugin-name]` (for new) or `marketplace/update-[plugin-name]` (for updates)
   - From: `main`

2. **Get the current file SHA:**
   The SHA from Step 1's `get_file_contents` response.

3. **Push the updated marketplace.json:**
   Use `mcp__github__create_or_update_file` with:
   - Owner: `SupportOlyticSolutions`
   - Repo: `olytic-plugins`
   - Path: `.claude-plugin/marketplace.json`
   - Branch: the feature branch from step 1
   - SHA: from step 2
   - Content: the updated JSON (pretty-printed, 2-space indent)
   - Message: `Add [plugin-name] to marketplace` or `Update [plugin-name] in marketplace`

4. **Confirm to the user:**
   "Staged on branch `marketplace/add-[plugin-name]`. You can review and merge when ready."

   Provide the branch URL: `https://github.com/SupportOlyticSolutions/olytic-plugins/tree/marketplace/add-[plugin-name]`

**Do NOT create a PR automatically** — the user may want to push additional plugin files to the same branch first.

## How to Update an Existing Plugin Version

Same process as above, but:
- In Step 3, find the existing entry by `name`
- In Step 4, show only the fields that changed
- Branch naming: `marketplace/update-[plugin-name]`
- Commit message: `Update [plugin-name] to v[version] in marketplace`

## Validation Rules

Before staging, validate:
- `name` is kebab-case
- `source` path starts with `./` and matches the plugin directory name
- `version` is valid semver
- `description` is under 120 characters
- `category` is one of the allowed values
- No duplicate `name` entries in the array (update, don't duplicate)

---
Telemetry: This skill logs all invocations via plugin-telemetry.
