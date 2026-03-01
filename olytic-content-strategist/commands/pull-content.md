---
description: Pull a page from GitHub to review or edit
argument-hint: "[repo-name] [file-path] (e.g., olytic-site blog/post.html)"
allowed-tools: ["mcp__github__get_file_contents", "Read", "Write"]
---

Fetch a file from one of Olytic's GitHub repositories.

All repos are under the `SupportOlyticSolutions` org. Repo map:

- `olytic-site` — Main website (default for website content)
- `olytic-lab` — Lab / experimental
- `olytic-plugins` — Plugin development
- `olytic-app` — Application
- `olytic-sandbox` — Sandbox / testing

Steps:
1. Parse `$ARGUMENTS` for repo name and file path. If only a file path is given, ask which repo — suggest the most likely one based on context (default: `olytic-site` for content work)
2. Use `mcp__github__get_file_contents` with owner `SupportOlyticSolutions` and the identified repo
3. Display a summary of the page: title, approximate word count, sections found
4. Ask what the user wants to do: edit for brand compliance, rewrite a section, update content, or something else

Always load brand standards (from The One Ring) before suggesting or making any edits.
