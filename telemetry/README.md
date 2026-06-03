# Obsidian Company Memory — Telemetry Endpoint

Direct-to-Supabase install telemetry for the [Obsidian Company Memory](../SKILL.md) skill. EU residency (West Europe / London), opt-out at runtime, anon-only-INSERT with RLS, schema-validated at the database, Postgres rate-limited.

This subfolder contains the schema, the DSAR helper, and this runbook. The endpoint itself is the Supabase project's PostgREST API — no edge function, no separate server. The Option B (direct PostgREST + RLS) architecture decision (2026-06-03) is documented internally; schema-drift mitigations are baked into the top of `supabase/migrations/20260603000000_install_events.sql`.

---

## What this records, in plain English

One row per install event (attempt, success, or failure). Each row has:

- a random UUID (no link to the user's name, email, company, or vault contents)
- the skill name + version
- the OS family (`darwin` / `win32` / `linux`)
- the install surface (`cowork` / `code`)
- the sync provider the user chose
- the outcome (`attempted` / `success` / `failed`)
- optionally, a failure-step short string (≤ 64 chars)
- the timestamp

That is the entire schema. No IP address, no email, no company name. Postgres CHECK constraints reject anything else; RLS prevents anon from reading or modifying anything.

---

## Project details

| Field | Value |
|---|---|
| Project name | `obsidian-company-memory-telemetry` |
| Project ref | `vujwcvqiwwpncnhgxjsu` |
| Region | West Europe (London / `eu-west-2`) |
| Dashboard | https://supabase.com/dashboard/project/vujwcvqiwwpncnhgxjsu |
| PostgREST base | `https://vujwcvqiwwpncnhgxjsu.supabase.co/rest/v1/` |
| DB password | `op://API Keys/Supabase - Obsidian Telemetry - DB password/password` |
| Service role key | `op://API Keys/Supabase - Obsidian Telemetry - service role/credential` |
| Anon key | Public; shipped in `plugin.json.telemetry.anon_key` |

---

## Initial setup (one-time — done 2026-06-03)

For reference if the project ever has to be rebuilt:

```sh
# 1. Create project via CLI (org-id from `supabase orgs list`)
supabase projects create obsidian-company-memory-telemetry \
  --org-id gssfonwxphttcpcahams \
  --region eu-west-2 \
  --db-password "$(op read 'op://API Keys/Supabase - Obsidian Telemetry - DB password/password')"

# 2. Link and apply schema
cd obsidian-setup-skill-test/telemetry
supabase link --project-ref vujwcvqiwwpncnhgxjsu --password "$(op read 'op://API Keys/Supabase - Obsidian Telemetry - DB password/password')"
supabase db query --linked -f supabase/migrations/20260603000000_install_events.sql

# 3. Capture the service-role key for ops
SVC=$(supabase projects api-keys --project-ref vujwcvqiwwpncnhgxjsu | awk '/service_role/ {print $3}')
op item create --category="API Credential" \
  --title="Supabase - Obsidian Telemetry - service role" \
  --vault="API Keys" "credential=$SVC"
```

---

## Smoke tests (already passed 2026-06-03)

```sh
ANON=$(supabase projects api-keys --project-ref vujwcvqiwwpncnhgxjsu | awk '/anon/ {print $3}')

# (1) Anon INSERT works
curl -sS -X POST \
  "https://vujwcvqiwwpncnhgxjsu.supabase.co/rest/v1/install_events" \
  -H "apikey: $ANON" -H "Authorization: Bearer $ANON" \
  -H "Content-Type: application/json" -H "Prefer: return=minimal" \
  -d '{"uuid":"7c2e3a14-9b8d-4f12-bc55-2e0c41d8a9b3","skill":"obsidian-company-memory","version":"1.0.0","os":"darwin","surface":"cowork","sync_provider":"dropbox","outcome":"success","ts":"2026-06-03T00:00:00Z"}'
# → HTTP 201

# (2) Anon SELECT blocked by RLS
curl -sS "https://vujwcvqiwwpncnhgxjsu.supabase.co/rest/v1/install_events?select=uuid" \
  -H "apikey: $ANON" -H "Authorization: Bearer $ANON"
# → [] (HTTP 200, empty)

# (3) Invalid enum value rejected by CHECK
curl -sS -X POST \
  "https://vujwcvqiwwpncnhgxjsu.supabase.co/rest/v1/install_events" \
  -H "apikey: $ANON" -H "Authorization: Bearer $ANON" \
  -H "Content-Type: application/json" \
  -d '{"uuid":"...","skill":"obsidian-company-memory","version":"1.0.0","os":"windows","surface":"cowork","outcome":"success","ts":"2026-06-03T00:00:00Z"}'
# → HTTP 400 with check constraint message

# (4) Rate limit fires at 6th request from same UUID within 60s
# → HTTP 400 {"code":"P0001","message":"rate_limit_exceeded"}
```

---

## Operational runbook

### Daily — health check

Supabase dashboard → Logs → API logs. Look for error-rate spike or rate-limit floods. Normal state: low traffic, mostly 201s, occasional legitimate failures.

### Weekly — install funnel review

```sh
supabase db query --linked "
  SELECT outcome, COUNT(*) AS n,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
  FROM install_events
  WHERE ts > NOW() - INTERVAL '7 days'
  GROUP BY outcome
  ORDER BY n DESC;
"
```

Healthy: `success` ≥ 95% of `attempted` (matches `brief.md` Impact Metric §1). If failure rate climbs: query `failure_step` distribution, dispatch a fix.

### Monthly — retention prune

The trigger doesn't auto-prune; run monthly via the `prune_old_install_events()` function:

```sh
supabase db query --linked "SELECT public.prune_old_install_events() AS rows_deleted;"
```

Deletes `install_events` rows older than 24 months. DSAR audit log rows are retained indefinitely per UK GDPR Article 30.

### Quarterly — SUSTAIN check (per OP #11 surface #6)

Verify the external-platform config hasn't drifted under us:

- [ ] Supabase Pro plan still active on `gssfonwxphttcpcahams` org
- [ ] Project still in `eu-west-2` (check `supabase projects list`)
- [ ] DPA with Supabase still on file
- [ ] Service role key in 1P still matches the one in the dashboard (rotation candidate every 12 months)
- [ ] Anon key in `plugin.json` still matches the live one (rotation would require a skill version bump)
- [ ] Security Advisor (Supabase Dashboard → Reports → Security Advisor) shows no new Errors

Log the audit to your normal SUSTAIN record.

---

## DSAR procedure (UK GDPR Article 15 / 17)

When a user emails `privacy@absolutionlabs.com` with their UUID:

1. **Verify the request.** Confirm the email is from a real address. Reply asking for the UUID if missing.
2. **Run the helper:**
   ```sh
   ./scripts/delete_uuid.sh <uuid> "DSAR via privacy@ inbox <date>"
   ```
3. The script:
   - Validates the UUID v4 shape.
   - Fetches the service-role key from 1P.
   - Calls `dsar_delete_uuid(uuid, requested_at, note)` Postgres function — atomic DELETE + INSERT into dsar_log in one transaction.
   - Prints suggested reply text.
4. **Reply to the requester** within one business day.

The `dsar_log` table records WHAT was deleted (UUID) and WHEN — not the deleted data itself. Article 30 record-keeping without violating Article 17.

---

## Files in this folder

| File | Purpose |
|---|---|
| `supabase/config.toml` | `supabase init` output (CLI workdir config) |
| `supabase/migrations/20260603000000_install_events.sql` | Schema, RLS, CHECK constraints, rate-limit trigger, DSAR + prune functions |
| `scripts/delete_uuid.sh` | DSAR helper (calls `dsar_delete_uuid` Postgres function via service role) |
| `README.md` | This file |
| `.gitignore` | Excludes `.temp/` (CLI internal cache) |

---

## Security & privacy posture (links to brief.md Threat-Map)

| Brief surface | This endpoint's control |
|---|---|
| #1 Secrets | Service-role key in 1P; rotated quarterly. Anon key is public by design (security via RLS). Nothing in the data path on disk. |
| #2 Privacy & data | EU residency (London) pinned at project creation. 24-month retention via monthly prune. DSAR via UUID. RLS prevents anon read. |
| #3 Prompt injection | Payload never reaches an LLM; Postgres CHECK constraints reject anything outside the 9-field schema vocabulary (8 mandatory + `failure_step` optional with [a-z0-9_:.-] charclass). |
| #4 Attack surface | RLS limits anon to INSERT only on one table; Postgres trigger rate-limits 5/60s/UUID; CHECK constraints enforce types + enums + regex. Supabase platform layers project-level rate limit + WAF. |
| #5 Backup & rollback | Supabase Pro daily PITR snapshots. Migration files in git for schema rollback. |
| #6 External platform config | Quarterly SUSTAIN check above. |

---

## Open items

- [x] Project created (2026-06-03)
- [x] Schema applied (2026-06-03)
- [x] Smoke tests passed (2026-06-03)
- [x] Service role key in 1P (2026-06-03)
- [ ] Custom domain (e.g. `telemetry.absolutionlabs.com`) — Pro tier supports it; defer until v1 public ship. Until then, the project URL in `plugin.json` is the canonical endpoint.
- [ ] First weekly funnel-review run + dashboard board
- [ ] DPA with Supabase signed copy filed
- [ ] Privacy policy at absolutionlabs.com/privacy published

---

*This endpoint is operated by Absolution Labs LTD. Code is MIT-licensed alongside the rest of the skill bundle. Questions: `info@absolutionlabs.com`. DSAR: `privacy@absolutionlabs.com`.*
