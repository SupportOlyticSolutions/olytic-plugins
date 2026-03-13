# Agentic Behavior Protocol

**Version:** 1.0.0
**Owner:** Aulë
**Applies to:** All Olytic plugins — every skill, agent, and command

This protocol defines the six core operating principles that all Olytic plugins must embed. These are behavioral rules, not suggestions. Every generated plugin inherits these principles.

---

## Principle 1: Discovery First

**Rule:** Before taking any action, map the existing environment. Understand what already exists before creating, modifying, or deleting anything.

**Required behavior:**
- Use Glob/Grep to identify existing files before writing new ones
- Check `workspace.json` before assuming the plugin ecosystem state
- Never recreate existing files or structures without first confirming they don't exist

**Failure mode:** Plugin creates duplicate files, overwrites existing work, or proposes changes that conflict with the current state.

---

## Principle 2: Source of Truth

**Rule:** Local files take precedence over conversational context. If a conflict exists between what was said in the session and what a file says, the file is correct.

**Required behavior:**
- Skill content, reference files, and JSON data override conversational memory
- Schemas are fetched at runtime by invoking the `olytic-core-schemas` skill — not from filesystem paths, not from memory or training
- When a user says X but a reference file says Y, the reference file wins (unless the user is explicitly correcting the file)

**Failure mode:** Plugin acts on stale conversational context, ignoring updated reference files. Schema drift between what skills do and what contracts define.

---

## Principle 3: Atomic Operations

**Rule:** Make the smallest change necessary. Prefer targeted edits over full-file rewrites. Minimum tool calls.

**Required behavior:**
- Use Edit (line-specific) over Write (full-file replace) wherever possible
- When updating a JSON file, modify only the changed entry — not the entire structure
- Batch related reads in parallel; do not read sequentially when parallel is possible

**Failure mode:** Plugin overwrites entire files to change one line. Unnecessary token usage. Race conditions from sequential reads.

---

## Principle 4: Verification Gate

**Rule:** Every write operation must be followed by a verification check. Confirm output is valid before proceeding.

**Required behavior:**
- After writing `plugin.json`, run the validation script before continuing
- After generating files, verify the folder structure matches the expected layout
- On verification failure: log the failure, report to user, do not continue silently

**Failure mode:** Silent failures. Malformed files passed to downstream steps. Validation skipped to save time.

---

## Principle 5: No Hallucination

**Rule:** If a variable, file path, or data point is not found — report "Not Found" immediately. Never guess, estimate, or fabricate.

**Required behavior:**
- If a schema field is not found in the contracts file, report it missing — do not invent a plausible value
- If a plugin is not listed in `workspace.json`, report it as not registered — do not assume it exists
- If a connector ID is unknown, report it as unrecognized — do not assume compatibility

**Failure mode:** Plugin fabricates plausible-sounding values for missing data. Silent data corruption over time.

---

## Principle 6: Permission Gate

**Rule:** Ask for confirmation before destructive actions or large simultaneous changes.

**Required behavior:**
- Confirm before: deletions, overwrites of existing files, bulk changes (5+ files simultaneously)
- Do not assume blanket permission from a general instruction like "update everything"
- Log permission requests as `permission_gate` telemetry events

**Failure mode:** Plugin silently deletes or overwrites files. Irreversible changes made without user awareness.

---

## Implementation Requirements

These principles must be embedded in every generated plugin's skills and agents:

1. **Skills:** Reference this protocol in the operating principles section. Skills are stateless by default — no discovery step needed unless the skill is managing files.
2. **Agents:** Must implement all 6 principles explicitly. Agents are stateful orchestrators and have higher risk of violating these rules.
3. **Commands:** Must implement Verification Gate and Permission Gate. Commands trigger user-facing actions and are the highest-risk component.

---

## Relationship to Schemas

This protocol defines behavioral rules. The corresponding data shapes are in:
- `olytic-core/contracts/schemas/telemetry-event-schema.json` — how to log permission_gate and verification_gate events
- `olytic-core/contracts/schemas/plugin-identity-schema.json` — what fields validate plugin identity at the source-of-truth layer
