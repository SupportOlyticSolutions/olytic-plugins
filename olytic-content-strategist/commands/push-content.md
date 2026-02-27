---
description: Push new or updated content to GitHub
argument-hint: [repo-name] [file-path] (e.g., olytic-site blog/new-post.html)
allowed-tools: ["mcp__github__create_or_update_file", "mcp__github__get_file_contents", "mcp__github__create_branch", "Read"]
---

Push content to one of Olytic's GitHub repositories.

All repos are under the `SupportOlyticSolutions` org. Repo map:

- `olytic-site` — Main website (default for website content)
- `olytic-lab` — Lab / experimental
- `olytic-plugins` — Plugin development
- `olytic-app` — Application
- `olytic-sandbox` — Sandbox / testing

Steps:
1. Parse `$ARGUMENTS` for repo name and file path. If only a file path is given, ask which repo (default: `olytic-site`)
2. If the file already exists in the repo, fetch it first to get the current SHA (required for updates)
3. Confirm with the user before pushing — show a summary of what will be created or changed
4. Ask for a commit message, or suggest one based on the changes
5. For new content, suggest creating a feature branch rather than pushing directly to main
6. Push using `mcp__github__create_or_update_file` with owner `SupportOlyticSolutions`
7. Confirm success and provide the file path
