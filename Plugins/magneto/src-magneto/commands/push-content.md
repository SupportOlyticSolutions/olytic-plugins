---
description: Push new or updated content to GitHub
argument-hint: "[repo-name] [file-path] (e.g., olytic-site blog/new-post.html)"
allowed-tools: ["mcp__github__create_or_update_file", "mcp__github__get_file_contents", "mcp__github__create_branch", "Read"]
---

## Step 0: Fetch Latest Reference Files (Always First)

Before doing anything else, fetch the latest files from the Olytic reference folder in Google Drive:

1. Use `mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_search` with `api_query: "'1Sv3EIQ0w4J3AGCFuxR0qxPtilESFRDGQ' in parents"` and `order_by: "modifiedTime desc"` to list all files in the folder.
2. For each file returned, fetch its full contents using `mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_fetch` with the file's `uri` as the document ID. All files in this folder are Google Docs and are fully readable this way.
3. Read and internalize the fetched documents. These are the **source of truth** — they supersede any baked-in context for topics they cover.
4. If the folder is empty or inaccessible, continue normally and note to the user that the Drive reference files could not be loaded.

Do not skip this step.

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
