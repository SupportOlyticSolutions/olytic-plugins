import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";

/**
 * log-telemetry — Olytic Telemetry Edge Function
 *
 * Design principles:
 * - No client-side JWT or service role key required
 * - Authentication via a lightweight shared static key (X-Telemetry-Key header)
 * - org_id is injected server-side and cannot be overridden by the caller
 * - Uses SUPABASE_SERVICE_ROLE_KEY env secret internally (set in Supabase dashboard)
 * - TELEMETRY_SHARED_KEY env secret set in Supabase dashboard (shared across all plugins)
 *
 * To deploy:
 *   supabase functions deploy log-telemetry --no-verify-jwt
 *
 * To set secrets in Supabase dashboard:
 *   Project Settings → Edge Functions → Secrets:
 *     TELEMETRY_SHARED_KEY = any strong random string you generate
 *     (SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are auto-injected by Supabase)
 *
 * Plugin skills send:
 *   POST https://kxnmgutidehncnafrwbu.supabase.co/functions/v1/log-telemetry
 *   X-Telemetry-Key: <TELEMETRY_SHARED_KEY>
 *   Content-Type: application/json
 *   { "timestamp", "event", "plugin", "plugin_version", "user_id", "component", "trigger", ...}
 */

const TELEMETRY_KEY = Deno.env.get("TELEMETRY_SHARED_KEY") ?? "";
const SUPABASE_URL = Deno.env.get("SUPABASE_URL") ?? "";
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";

// org_id is hardcoded server-side — clients cannot spoof it
const ORG_ID = "olytic-internal";
const DEFAULT_USER_ID = "support@olyticsolutions.com";

const REQUIRED_FIELDS = ["timestamp", "event", "plugin", "plugin_version", "component"];

Deno.serve(async (req: Request) => {
  if (req.method !== "POST") {
    return json({ error: "Method not allowed" }, 405);
  }

  // --- Auth: shared static key ---
  // If TELEMETRY_SHARED_KEY is set, enforce it. If not set (e.g. during initial setup), allow through.
  if (TELEMETRY_KEY) {
    const incomingKey = req.headers.get("X-Telemetry-Key") ?? "";
    if (incomingKey !== TELEMETRY_KEY) {
      return json({ error: "Unauthorized" }, 401);
    }
  }

  // --- Parse body ---
  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return json({ error: "Invalid JSON body" }, 400);
  }

  // --- Validate required fields ---
  for (const field of REQUIRED_FIELDS) {
    if (!body[field]) {
      return json({ error: `Missing required field: ${field}` }, 400);
    }
  }

  // --- Inject server-side fields (client cannot override) ---
  body.org_id = ORG_ID;
  if (!body.user_id) {
    body.user_id = DEFAULT_USER_ID;
  }

  // --- Insert via service role key (bypasses RLS safely, server-side only) ---
  const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);
  const { error } = await supabase.from("telemetry_events").insert([body]);

  if (error) {
    console.error("Supabase insert error:", error.message);
    return json({ error: error.message }, 500);
  }

  return json({ success: true }, 201);
});

function json(data: unknown, status: number): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", "Connection": "keep-alive" },
  });
}
