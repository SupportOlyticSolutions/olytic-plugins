#!/usr/bin/env node
/**
 * generate-catalog.js
 *
 * Walks every top-level subdirectory that contains a .claude-plugin/plugin.json,
 * merges the metadata into catalog.json, and writes the result.
 *
 * Rules:
 *   - Existing catalog entries are preserved in full (useCases, rulesets, etc.).
 *   - Fields sourced from plugin.json (name, version, description, keywords)
 *     always overwrite the catalog entry so the catalog stays in sync.
 *   - Plugins present in subdirs but absent from the catalog get a stub entry.
 *   - Plugins in the catalog but with no matching subdir are left untouched
 *     (they may be legacy entries — a human should remove them deliberately).
 *   - Output is sorted: existing order is preserved, new plugins appended.
 */

const fs   = require('fs');
const path = require('path');

const ROOT         = path.resolve(__dirname, '..', '..');
const CATALOG_PATH = path.join(ROOT, 'catalog.json');

// ── 1. Discover all plugin dirs ──────────────────────────────────────────────

function discoverPlugins() {
  const plugins = [];
  const entries = fs.readdirSync(ROOT, { withFileTypes: true });

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    // skip hidden dirs and the .github folder
    if (entry.name.startsWith('.')) continue;

    const manifestPath = path.join(ROOT, entry.name, '.claude-plugin', 'plugin.json');
    if (!fs.existsSync(manifestPath)) continue;

    try {
      const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
      plugins.push({ dir: entry.name, manifest });
    } catch (err) {
      console.warn(`⚠️  Could not parse ${manifestPath}: ${err.message}`);
    }
  }

  return plugins;
}

// ── 2. Load existing catalog ──────────────────────────────────────────────────

function loadCatalog() {
  if (!fs.existsSync(CATALOG_PATH)) {
    return { version: '2.0.0', generated: '', plugins: [] };
  }
  return JSON.parse(fs.readFileSync(CATALOG_PATH, 'utf8'));
}

// ── 3. Derive category from keywords ─────────────────────────────────────────

const KEYWORD_CATEGORY_MAP = [
  [['governance', 'brand', 'policies'], 'governance'],
  [['content', 'website', 'analytics', 'seo', 'geo'], 'content'],
  [['plugin-creation', 'meta-plugin', 'marketplace'], 'meta'],
  [['data-architecture', 'metadata-platform', 'data-governance'], 'platform'],
];

function deriveCategory(keywords = []) {
  for (const [terms, category] of KEYWORD_CATEGORY_MAP) {
    if (terms.some(t => keywords.includes(t))) return category;
  }
  return 'other';
}

// ── 4. Merge ──────────────────────────────────────────────────────────────────

function merge(catalog, discovered) {
  const existingById = new Map(
    (catalog.plugins || []).map(p => [p.id, p])
  );

  const seen = new Set();
  const merged = [];

  // Pass 1: update existing entries with fresh plugin.json data
  for (const existing of catalog.plugins || []) {
    const found = discovered.find(
      d => d.manifest.name === existing.id || d.dir === existing.id
    );

    if (found) {
      const { manifest } = found;
      merged.push({
        ...existing,                          // preserve full rich data
        version:  manifest.version  || existing.version,
        keywords: manifest.keywords || existing.keywords,
        // Overwrite description only if it's a stub (starts with 'TODO')
        ...(existing.bigPicture?.startsWith('TODO') && manifest.description
          ? { bigPicture: manifest.description }
          : {}),
      });
      seen.add(manifest.name);
    } else {
      // No matching dir — keep as-is, note it
      console.log(`ℹ️  Catalog entry '${existing.id}' has no matching plugin dir — keeping as-is.`);
      merged.push(existing);
    }
  }

  // Pass 2: append stub entries for newly discovered plugins
  for (const { dir, manifest } of discovered) {
    if (seen.has(manifest.name)) continue;

    console.log(`✨ New plugin detected: '${manifest.name}' — adding stub to catalog.`);
    merged.push({
      id:          manifest.name,
      name:        toDisplayName(manifest.name),
      version:     manifest.version || '0.1.0',
      category:    deriveCategory(manifest.keywords),
      scope:       'user',
      keywords:    manifest.keywords || [],
      bigPicture:  manifest.description || 'TODO: add bigPicture',
      purpose:     'TODO: add purpose',
      useCases:    [],
      rulesets:    [],
      triggerConditions: { narrative: 'TODO', activates: [], dormant: [] },
      components:  { skills: [], commands: [], agents: [] },
      successCriteria: { narrative: 'TODO', kpis: [] },
      guardrails:  [],
      setup:       [],
    });
  }

  return merged;
}

function toDisplayName(id) {
  return id
    .split(/[-_]/)
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

// ── 5. Write ──────────────────────────────────────────────────────────────────

function main() {
  const discovered = discoverPlugins();
  console.log(`🔍 Discovered ${discovered.length} plugin(s): ${discovered.map(d => d.manifest.name).join(', ')}`);

  const catalog = loadCatalog();
  console.log(`📋 Existing catalog has ${(catalog.plugins || []).length} plugin(s).`);

  const mergedPlugins = merge(catalog, discovered);

  const output = {
    ...catalog,
    generated: new Date().toISOString(),
    plugins:   mergedPlugins,
  };

  fs.writeFileSync(CATALOG_PATH, JSON.stringify(output, null, 2) + '\n');
  console.log(`✅ catalog.json updated — ${mergedPlugins.length} plugin(s) total.`);
}

main();
