---
description: Create a new plugin from scratch with guided discovery
argument-hint: "[plugin-name] (e.g., customer-success-tracker)"
allowed-tools: ["Read", "Write", "Glob", "Bash", "mcp__github__get_file_contents", "mcp__github__create_or_update_file", "mcp__github__create_branch"]
---

Start the plugin creation process using the plugin-builder agent.

If `$ARGUMENTS` contains a plugin name, use it as the starting name (the user can refine it during discovery). If no arguments provided, begin discovery from scratch.

Steps:
1. Acknowledge the user's intent to create a plugin
2. Hand off to the plugin-builder agent for the full 6-phase workflow:
   - Discovery (7 questions)
   - Component planning
   - Generation
   - Review
   - Delivery (.plugin file)
   - Marketplace update (optional)
3. The agent manages the entire flow — do not interrupt or shortcut phases

If the user has already completed discovery separately and wants to skip to generation, they can use the plugin-generation skill directly. This command always starts from the beginning.
