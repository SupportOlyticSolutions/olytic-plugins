---
description: Audit and update an existing plugin to current best practices and standards
argument-hint: "[plugin-name or 'all'] (e.g., the-one-ring, olytic-content-strategist, all)"
allowed-tools: ["Read", "Write", "Glob", "Grep", "Bash", "mcp__github__get_file_contents", "mcp__github__create_or_update_file", "mcp__github__create_branch"]
---

Audit and update one or more existing plugins to match current Aulë standards — fixing upload-blocking issues, applying latest best practices (including permissions manifests, memory scope declarations, and augmentation framing), and repackaging.

Hand off to the plugin-builder agent in Update Mode. The agent manages the full update workflow:
- Audit Phase 0: Locate and inventory plugins
- Audit Phase 1: Check all files against current standards
- Audit Phase 2: Present findings before changing anything
- Audit Phase 3: Apply fixes (user chooses scope)
- Audit Phase 4: Verify all checks pass, then repackage

Steps:
1. Parse `$ARGUMENTS`:
   - If `all` or empty: Use Glob to find all `.plugin` files and plugin directories in the working folder, then hand off to the plugin-builder agent with the full list
   - If a specific name: Locate that plugin (directory or `.plugin` file) and hand off to the plugin-builder agent with that target
   - If the target is not found, report "Not Found" and list what IS available

2. Acknowledge the target(s) to the user before handing off:
   - "Auditing [plugin-name] against current standards. I'll show you what needs fixing before making any changes."
   - Or for multiple: "Auditing [N] plugins. I'll run checks on each and present findings before making any changes."

3. Hand off to the plugin-builder agent to execute the full Update Mode workflow.

**This command does not make changes without showing the audit report first.** The user always sees what will be changed and approves the scope before any files are modified.
