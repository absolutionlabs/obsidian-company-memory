# Recovery Drill

Required before Gate 3 (production-touching project — telemetry endpoint + privacy infra count). Drill outcomes logged in our internal project brief's Recovery Drill Log.

The drill proves that if the worst case happens — the Supabase project is corrupted, deleted, or unreachable — you can restore it from backup without losing user data or the audit trail. If you can't, the system is fragile in a way the brief specifically marked as a Gate 3 blocker.

Run this **before public ship**, then **once per quarter** afterwards. Log every run at the bottom of this file.

---

## What you're proving

1. The current `install_events` table can be restored from a Supabase backup.
2. The schema, RLS policies, CHECK constraints, and triggers all survive the restore.
3. The DSAR audit log (`dsar_log`) is preserved.
4. The skill's bundle config doesn't need to change to talk to the restored data plane.
5. The whole restore takes less than 60 minutes from "start" to "smoke tests pass on restored project."

If any of those is false, the drill fails. Fix the underlying gap before public ship.

---

## Pre-drill setup

You need:

- A second Supabase project on the same org (this is the "restore target")
- Active Supabase Pro plan (PITR + downloadable backups are Pro features)
- The bundle's current state in a known git commit
- A tester UUID generator (any UUID v4)

Create the restore target ONCE:

```sh
# Use 1P for the DB password as we did for the live project
DBPW="$(op item create --category=password \
  --title='Supabase - Obsidian Telemetry RESTORE TARGET - DB password' \
  --vault='API Keys' --generate-password=letters,digits,40 \
  --format=json | python -c 'import json,sys; d=json.load(sys.stdin); print([f["value"] for f in d["fields"] if f["id"]=="password"][0])')"

supabase projects create obsidian-company-memory-telemetry-restore \
  --org-id gssfonwxphttcpcahams \
  --region eu-west-2 \
  --db-password "$DBPW"
```

Note the project ref. You'll use this only for drills; it stays empty between runs.

---

## The drill — step by step

### Step 1 — Seed the live project with test data

Before "destroying" the source state, plant 3 distinct rows whose UUIDs you know. These are the recoverability markers.

```sh
ANON=$(supabase projects api-keys --project-ref vujwcvqiwwpncnhgxjsu | awk '/anon/ {print $3}')

for u in "11111111-1111-4111-8111-111111111111" \
         "22222222-2222-4222-8222-222222222222" \
         "33333333-3333-4333-8333-333333333333"; do
  curl -sS -X POST \
    "https://vujwcvqiwwpncnhgxjsu.supabase.co/rest/v1/install_events" \
    -H "apikey: $ANON" -H "Authorization: Bearer $ANON" \
    -H "Content-Type: application/json" \
    -d "{\"uuid\":\"$u\",\"skill\":\"obsidian-company-memory\",\"version\":\"1.0.0\",\"os\":\"darwin\",\"surface\":\"cowork\",\"sync_provider\":\"dropbox\",\"outcome\":\"success\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}"
done
```

### Step 2 — Trigger a backup

In the Supabase dashboard:

1. Open the live project (`obsidian-company-memory-telemetry`, ref `vujwcvqiwwpncnhgxjsu`).
2. Database → Backups → "Restore from a backup" tab. Confirm scheduled daily backups are active.
3. Pick the most recent backup. Note the timestamp.

If no backups appear: Supabase Pro auto-backup may not have run yet (it runs daily; new projects wait 24h for first backup). For drills run within 24h of project creation: trigger a manual snapshot via SQL dump (Settings → Database → "Backups (manual download)").

### Step 3 — Restore the backup into the target project

Two methods, pick one:

**Method A — PITR clone (Pro feature, instant):**

In the Supabase dashboard for the restore-target project:
- Database → Backups → "Restore from another project"
- Source: `obsidian-company-memory-telemetry`
- Source timestamp: the one you noted in Step 2
- Confirm.

The restore typically takes 5-15 min for a small DB. The target project's data is overwritten.

**Method B — SQL dump + restore (always works, but slower):**

```sh
# Download the backup from Supabase dashboard as a .sql file
# Apply it to the target project:
TARGET_REF="<restore-target-ref>"
supabase link --project-ref $TARGET_REF
supabase db query --linked -f /path/to/downloaded-backup.sql
```

This restores schema + data but RLS policies must be re-applied separately (Supabase backups include policies; raw `pg_dump` doesn't).

### Step 4 — Verify schema survived

Against the restored target:

```sh
supabase db query --linked "
  SELECT
    table_name,
    (SELECT COUNT(*) FROM pg_policies WHERE schemaname='public' AND tablename=c.relname) AS policies,
    c.relrowsecurity AS rls
  FROM pg_class c
  JOIN pg_namespace n ON n.oid = c.relnamespace
  WHERE n.nspname='public' AND c.relkind='r'
  ORDER BY table_name;
"
```

**Expected:**
- `install_events` — RLS on, 1 policy (anon-INSERT)
- `dsar_log` — RLS on, 0 policies (service-role-only, intentional)

If RLS is off or policies are missing: re-apply [supabase/migrations/20260603000000_install_events.sql](../telemetry/supabase/migrations/20260603000000_install_events.sql) against the restored target.

### Step 5 — Verify data survived

```sh
supabase db query --linked "
  SELECT uuid FROM install_events
  WHERE uuid IN (
    '11111111-1111-4111-8111-111111111111',
    '22222222-2222-4222-8222-222222222222',
    '33333333-3333-4333-8333-333333333333'
  )
  ORDER BY uuid;
"
```

**Expected:** all 3 marker UUIDs present.

If fewer than 3: the backup didn't capture them (likely Step 1 ran after the backup timestamp). Re-run from Step 2 with a fresh backup taken AFTER Step 1's writes.

### Step 6 — Verify constraints survived

Smoke-test the restored target with the same 4 checks the live project passed:

```sh
RESTORED_REF="<restore-target-ref>"
RESTORED_ANON=$(supabase projects api-keys --project-ref $RESTORED_REF | awk '/anon/ {print $3}')
RESTORED_URL="https://$RESTORED_REF.supabase.co"

# (a) Valid INSERT
curl -sS -X POST "$RESTORED_URL/rest/v1/install_events" \
  -H "apikey: $RESTORED_ANON" -H "Authorization: Bearer $RESTORED_ANON" \
  -H "Content-Type: application/json" -H "Prefer: return=minimal" \
  -d '{"uuid":"44444444-4444-4444-8444-444444444444","skill":"obsidian-company-memory","version":"1.0.0","os":"darwin","surface":"cowork","sync_provider":"dropbox","outcome":"success","ts":"2026-06-03T00:00:00Z"}' \
  -w "  Insert: HTTP %{http_code}\n"

# (b) Anon SELECT blocked
curl -sS "$RESTORED_URL/rest/v1/install_events?select=uuid" \
  -H "apikey: $RESTORED_ANON" -H "Authorization: Bearer $RESTORED_ANON" \
  -w "  Select: HTTP %{http_code}\n"

# (c) Invalid enum rejected
curl -sS -X POST "$RESTORED_URL/rest/v1/install_events" \
  -H "apikey: $RESTORED_ANON" -H "Authorization: Bearer $RESTORED_ANON" \
  -H "Content-Type: application/json" \
  -d '{"uuid":"55555555-5555-4555-8555-555555555555","skill":"obsidian-company-memory","version":"1.0.0","os":"INVALID","surface":"cowork","outcome":"success","ts":"2026-06-03T00:00:00Z"}' \
  -w "  Invalid: HTTP %{http_code}\n"

# (d) Rate limit fires after 5 inserts/UUID/60s — sample with 7
for i in 1 2 3 4 5 6 7; do
  CODE=$(curl -sS -o /dev/null -X POST "$RESTORED_URL/rest/v1/install_events" \
    -H "apikey: $RESTORED_ANON" -H "Authorization: Bearer $RESTORED_ANON" \
    -H "Content-Type: application/json" \
    -d "{\"uuid\":\"66666666-6666-4666-8666-666666666666\",\"skill\":\"obsidian-company-memory\",\"version\":\"1.0.0\",\"os\":\"darwin\",\"surface\":\"cowork\",\"outcome\":\"attempted\",\"ts\":\"2026-06-03T00:00:00Z\"}" \
    -w "%{http_code}")
  echo "  RL #$i: HTTP $CODE"
done
```

**Expected:** (a) 201, (b) 200 with `[]`, (c) 400, (d) 5x 201 then 2x 400.

### Step 7 — Verify the bundle config could swap

This step doesn't change the live system — it's a paper exercise. Confirm that:

1. The bundle's `plugin.json.telemetry.endpoint` would need to change from `vujwcvqiwwpncnhgxjsu.supabase.co` to the restored project's URL.
2. The bundle's `plugin.json.telemetry.anon_key` would need to change to the restored project's anon key.
3. Both changes are file edits — no code changes required.

This proves the bundle is restoration-friendly: if you ever needed to fail over to the restore-target permanently, the change is a single commit.

### Step 8 — Clean up

Delete the rows added during the drill from BOTH projects:

```sh
# Live project
supabase link --project-ref vujwcvqiwwpncnhgxjsu
supabase db query --linked "DELETE FROM install_events WHERE uuid::text LIKE '____-1111-%' OR uuid::text LIKE '____-2222-%' OR uuid::text LIKE '____-3333-%';"

# Restore target — wipe entirely (it's a drill target, no real data)
supabase link --project-ref <restore-target-ref>
supabase db query --linked "DELETE FROM install_events; DELETE FROM dsar_log;"
```

### Step 9 — Log the drill

Append a row to the table below.

---

## Failure modes

If any step fails:

- **Backup not present** → check Supabase plan tier; Pro is required for PITR. If on Pro, file a Supabase support ticket.
- **Restore creates a different schema** → the backup didn't capture extension state or custom functions. Re-apply the migration after restore.
- **RLS policies missing post-restore** → use Method B (SQL dump) instead of Method A (PITR clone); apply migration manually.
- **Markers missing from restore** → backup timestamp was before Step 1; re-run with a fresh backup.
- **Smoke tests fail** → schema or constraint drift between live and restored; investigate using `supabase db query` against information_schema.

Document the failure mode + remediation in the log row. If a failure mode recurs across drills, file an issue against the bundle to add automation that prevents it.

---

## Drill log

| Date | Operator | Source state | Restore method | Time-to-restore | Result | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |

(Append the first row after the first run. Format example: `2026-06-15 | Rob | live project clean | Method A | 18 min | PASS | First drill; markers all present.`)

---

*This is a Gate 3 deliverable — required to pass before public ship. Quarterly cadence after that. Outcomes logged in our internal project brief's Recovery Drill Log.*
