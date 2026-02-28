# Agentic Best Practices

**Goal: Maximum reasoning precision with minimal context footprint.**

These protocols apply to the Olytic Plugin Creator itself AND to every plugin it generates. They are non-negotiable.

---

## 1. Core Agentic Protocols

### Discovery First
Before proposing any action, map the existing environment. Use search, glob, or list tools to understand what already exists. Do not recreate existing files or structures.

**In the Plugin Creator:** Before generating a plugin, check if one with the same name already exists in the marketplace or working directory.

**In Generated Plugins:** Every skill and agent must instruct Claude to assess the current state before taking action. No skill should assume a blank slate.

### Source of Truth
Treat local files (Markdown, JSON, CSV) as the primary memory. If a conflict exists between chat history and a local file, the local file is correct.

**In the Plugin Creator:** Discovery output stored as structured data takes precedence over conversational memory.

**In Generated Plugins:** Skills reference their own `references/` files as authoritative. Agents reference skill content over conversational context. If a user says "our brand voice is casual" but the brand standards skill says otherwise, the skill wins.

### Atomic Operations
Perform the smallest possible change required. Use line-specific edits rather than full-file rewrites.

**In the Plugin Creator:** When updating marketplace.json, modify only the changed entry — do not rewrite the entire file structure.

**In Generated Plugins:** Commands that modify files must use targeted edits. Commands that update external systems must make the minimum necessary API calls.

### No Redundancy
Do not repeat information found in project files back to the user unless explicitly asked for a summary. Use "Reference: [filename]" instead.

**In the Plugin Creator:** When generating plugins, don't duplicate knowledge between skills. If brand standards exist in The One Ring, reference them — don't copy them.

**In Generated Plugins:** Skills should reference other skills and files rather than inlining their content. Use patterns like "For brand voice rules, see The One Ring's `olytic-brand-standards` skill."

---

## 2. Tool & Token Management

### Search Over Read
Use search tools to find specific strings and data points. Never read a file larger than 50KB in its entirety if specific information can be targeted.

**In Generated Plugins:** Commands and agents that work with large files (repos, logs, datasets) must use Grep/Glob to target specific content rather than reading entire files into context.

### Programmatic Processing
For data-heavy tasks, write and execute a local script to process the data and return only the final result to the context window.

**In Generated Plugins:** When a command involves processing large datasets (analytics, logs, metrics), instruct Claude to write a processing script rather than loading all data into the conversation.

### Batching
Consolidate multiple related tasks into a single agentic turn to reduce token overhead.

**In Generated Plugins:** Agents that perform multi-step workflows should batch related operations (e.g., read 3 files in parallel rather than sequentially) and present consolidated results.

---

## 3. Directory & Data Governance

### Active Workspace
Primary operations occur in the current working directory or designated output locations. Generated files go to predictable, consistent locations.

**In the Plugin Creator:** Generated plugins are built in the working directory, packaged from there, and delivered to outputs.

**In Generated Plugins:** Every command must specify where its output goes. No implicit file creation in unexpected locations.

### Cold Storage
Files in archive or log directories are "out of sight." Only access these when a historical lookup is explicitly required.

**In Generated Plugins:** Telemetry logs are write-only during normal operation. Only access them when the user explicitly asks to review plugin performance or history.

### Metadata Integrity
Every automated entry must include a timestamp and a "Source" tag for traceability.

**In the Plugin Creator:** Every generated file includes the plugin version and creation context.

**In Generated Plugins:** Telemetry log entries include timestamp, plugin version, component name, and source trigger. Any content pushed to external systems (GitHub, etc.) includes commit messages with author and purpose.

---

## 4. Safety & Quality Guardrails

### Verification Gate
Every write operation must be followed by a verification check to ensure the file structure remains valid.

**In the Plugin Creator:** After generating all plugin files, validate the directory structure against the expected layout before packaging.

**In Generated Plugins:** Commands that write files must verify the output (read-back check). Commands that push to external systems must confirm success. Agents must validate their output format matches the specified template.

### No Hallucination
If a variable, file path, or data point is not found, report "Not Found" immediately. Do not guess or estimate.

**In the Plugin Creator:** If discovery answers reference integrations, repos, or property IDs that can't be verified, flag them as unverified rather than assuming they're correct.

**In Generated Plugins:** Skills must instruct Claude to say "I don't have this information" rather than fabricating data. Agents must report missing data points in their output rather than filling in plausible-sounding values.

### Permission Gate
Ask for confirmation before performing any destructive actions (delete, overwrite) or making 5+ simultaneous file changes.

**In the Plugin Creator:** The plugin-builder agent confirms the component plan before generation. The marketplace updater confirms before staging changes.

**In Generated Plugins:** Every command that modifies external systems includes a confirmation step. Agents that produce large outputs present a summary before writing files. No destructive operations without explicit user approval.

---

## How to Embed in Generated Plugins

When generating a plugin, these practices are embedded in three places:

1. **In every skill body** — Add a "Operating Principles" section:
   ```markdown
   ## Operating Principles

   - **Discovery first:** Assess current state before taking action
   - **Source of truth:** Local files and skill content take precedence over conversation
   - **Atomic operations:** Make the smallest change necessary
   - **Verify after writing:** Confirm output is valid after every write operation
   - **No hallucination:** Report "Not Found" rather than guessing
   ```

2. **In every agent body** — Add to the agent's rules:
   ```markdown
   ## Rules

   - Map the environment before acting — use search/glob to understand what exists
   - Treat skill content as authoritative over conversational context
   - Batch related operations to minimize token overhead
   - Use targeted search over full-file reads for large files
   - Verify every write operation succeeded
   - Never fabricate data — report missing information explicitly
   - Confirm with the user before destructive actions or 5+ file changes
   ```

3. **In the telemetry skill** — Track compliance:
   - Log verification gate passes/failures
   - Log hallucination catches (when "Not Found" is reported)
   - Log permission gate activations (when confirmation was requested)
