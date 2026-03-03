---
description: Add or update a plugin in the Olytic marketplace
argument-hint: "[plugin-name] (e.g., customer-success-tracker)"
allowed-tools: ["Read", "mcp__github__get_file_contents", "mcp__github__create_or_update_file", "mcp__github__create_branch"]
---

Update the Olytic plugin marketplace to add or update a plugin entry.

This command uses the marketplace-management skill to:

1. Read the current `marketplace.json` from `SupportOlyticSolutions/olytic-plugins`
2. Find or create the entry for `$ARGUMENTS` (the plugin name)
3. If the plugin files exist locally, read `plugin.json` to populate the entry automatically
4. If the plugin files don't exist locally, ask the user for: name, description, version, category, keywords
5. Show the user what will change (diff view)
6. Ask for confirmation before staging
7. Create a feature branch and commit the updated marketplace.json
8. Provide the branch URL for review

**This command does NOT merge to main.** It only stages changes on a feature branch.

**This command is for the Olytic marketplace only.** It always targets `SupportOlyticSolutions/olytic-plugins`.
