-- ============================================================================
-- Obsidian Company Memory — install telemetry schema
-- ============================================================================
--
-- Project: obsidian-company-memory-telemetry (ref vujwcvqiwwpncnhgxjsu)
-- Region:  West Europe (London, eu-west-2) — GDPR EU residency
-- Apply:   supabase db query --linked -f supabase/migrations/20260603000000_install_events.sql
--
-- ----------------------------------------------------------------------------
-- LOCKED-SCHEMA CONVENTION (per Option B decision 2026-06-03)
-- ----------------------------------------------------------------------------
-- The skill ships its public-anon-key and POSTs DIRECTLY to PostgREST. The
-- skill code in users' hands hard-codes column names. Therefore:
--
--   1. The 8 fields below are FROZEN for v1. No renames, ever.
--   2. New fields MUST be nullable with a default. Old skill versions just
--      omit them; PostgREST accepts the partial insert; downstream queries
--      treat NULL as "skill version too old to send this field."
--   3. CHECK constraints enforce the enum vocabularies declared in the
--      docs/privacy-policy.md disclosure table. Changes to either side MUST
--      land in BOTH this file and the privacy policy in the same session,
--      or the disclosure drifts from reality (Threat-Map surface #2).
--
-- The schema-drift class documented at
-- [[concepts/postgrest-schema-drift-pattern]] is bounded here by the lock,
-- not eliminated by it. If a future change requires breaking the lock,
-- expect to publish a new skill version + run a coexistence period.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Tables
-- ----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS public.install_events (
  id              BIGSERIAL PRIMARY KEY,
  uuid            UUID        NOT NULL,
  skill           TEXT        NOT NULL CHECK (skill = 'obsidian-company-memory'),
  version         TEXT        NOT NULL CHECK (version ~ '^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.-]+)?$'),
  os              TEXT        NOT NULL CHECK (os IN ('darwin', 'win32', 'linux')),
  surface         TEXT        NOT NULL CHECK (surface IN ('cowork', 'code')),
  sync_provider   TEXT                 CHECK (sync_provider IS NULL OR sync_provider IN ('dropbox', 'icloud', 'onedrive', 'google-drive', 'local-only')),
  outcome         TEXT        NOT NULL CHECK (outcome IN ('attempted', 'success', 'failed')),
  failure_step    TEXT                 CHECK (failure_step IS NULL OR length(failure_step) <= 64),
  ts              TIMESTAMPTZ NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_install_events_uuid    ON public.install_events(uuid);
CREATE INDEX IF NOT EXISTS idx_install_events_ts      ON public.install_events(ts);
CREATE INDEX IF NOT EXISTS idx_install_events_outcome ON public.install_events(outcome);
CREATE INDEX IF NOT EXISTS idx_install_events_version ON public.install_events(version);

COMMENT ON TABLE public.install_events IS
  'Anonymous install telemetry from the Obsidian Company Memory skill. '
  'Schema frozen for v1; new fields must be nullable with defaults. '
  'See docs/privacy-policy.md for the canonical disclosure of what each field captures.';


-- DSAR audit log (GDPR Article 30 record-keeping).
-- Records WHAT was deleted (UUID) and WHEN — not the deleted data itself.
CREATE TABLE IF NOT EXISTS public.dsar_log (
  id             BIGSERIAL  PRIMARY KEY,
  uuid           UUID        NOT NULL,
  requested_at   TIMESTAMPTZ NOT NULL,
  completed_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  rows_deleted   INTEGER     NOT NULL,
  operator_note  TEXT
);

COMMENT ON TABLE public.dsar_log IS
  'Audit trail of telemetry-UUID deletion requests handled under UK GDPR. '
  'Retained indefinitely per Article 30.';


-- ----------------------------------------------------------------------------
-- Row-level security
-- ----------------------------------------------------------------------------

ALTER TABLE public.install_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.dsar_log       ENABLE ROW LEVEL SECURITY;

-- install_events: anon role can INSERT, nothing else. Service role bypasses
-- RLS and can do everything for ops queries / pruning / DSAR.
CREATE POLICY "anon can insert install_events"
  ON public.install_events
  FOR INSERT
  TO anon
  WITH CHECK (true);  -- column-level CHECK constraints do the validation

-- dsar_log: no policy = anon + authenticated get deny-all. Service role only.
-- (The linter will flag this as "RLS Enabled No Policy" Info — that's the
-- correct, intentional posture per supabase-security-advisor-cleanup.md
-- § "RLS Enabled No Policy".)


-- ----------------------------------------------------------------------------
-- Rate limiting
-- ----------------------------------------------------------------------------
--
-- Postgres-side rate limit: count rows from this UUID's installs in the last
-- 60 seconds and refuse if it exceeds 5 — same envelope as the CF design
-- (5 req/min) but keyed by UUID rather than IP. UUID-keying is more honest
-- about what we're actually rate-limiting (one install can legitimately
-- send 2-3 pings: attempted, then success-or-failed; 5 covers any reasonable
-- retry pattern).
--
-- Project-level rate limiting at the Supabase platform (anon-key requests
-- per IP) provides the second layer — configurable in dashboard at
-- Settings → API → Rate Limits.

-- SECURITY DEFINER (not INVOKER): the trigger needs to SELECT from
-- install_events to count recent rows, but anon doesn't have SELECT
-- permission via RLS. SECURITY DEFINER runs the function as the table
-- owner (bypassing RLS for the COUNT). Tested 2026-06-03 — without
-- DEFINER, every anon-inserted row counts as 0 prior rows and the limit
-- never fires.
CREATE OR REPLACE FUNCTION public.enforce_install_rate_limit()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog, public
AS $$
DECLARE
  recent_count INTEGER;
BEGIN
  SELECT COUNT(*) INTO recent_count
    FROM public.install_events
    WHERE uuid = NEW.uuid
      AND created_at > NOW() - INTERVAL '60 seconds';

  IF recent_count >= 5 THEN
    RAISE EXCEPTION 'rate_limit_exceeded'
      USING HINT = 'Too many pings from this install UUID in the last 60 seconds.';
  END IF;

  RETURN NEW;
END;
$$;

-- Lock down EXECUTE per supabase-security-advisor-cleanup.md
-- § "REVOKE FROM PUBLIC trap" — revoke from anon + authenticated by name.
-- (Triggers fire regardless of EXECUTE grants; the REVOKE is hygiene.)
REVOKE EXECUTE ON FUNCTION public.enforce_install_rate_limit() FROM anon;
REVOKE EXECUTE ON FUNCTION public.enforce_install_rate_limit() FROM authenticated;

CREATE TRIGGER trg_install_events_rate_limit
  BEFORE INSERT ON public.install_events
  FOR EACH ROW
  EXECUTE FUNCTION public.enforce_install_rate_limit();


-- ----------------------------------------------------------------------------
-- DSAR helper function (called by scripts/delete_uuid.sh via service role)
-- ----------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.dsar_delete_uuid(
  target_uuid   UUID,
  requested_at  TIMESTAMPTZ,
  operator_note TEXT
) RETURNS INTEGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog, public
AS $$
DECLARE
  deleted_count INTEGER;
BEGIN
  DELETE FROM public.install_events WHERE uuid = target_uuid;
  GET DIAGNOSTICS deleted_count = ROW_COUNT;

  INSERT INTO public.dsar_log (uuid, requested_at, rows_deleted, operator_note)
    VALUES (target_uuid, requested_at, deleted_count, operator_note);

  RETURN deleted_count;
END;
$$;

-- Lock down execute — service role only. Per supabase-security-advisor-cleanup.md
-- § "REVOKE FROM PUBLIC trap", revoke from anon + authenticated explicitly.
REVOKE EXECUTE ON FUNCTION public.dsar_delete_uuid(UUID, TIMESTAMPTZ, TEXT) FROM anon;
REVOKE EXECUTE ON FUNCTION public.dsar_delete_uuid(UUID, TIMESTAMPTZ, TEXT) FROM authenticated;


-- ----------------------------------------------------------------------------
-- Retention prune helper (call monthly)
-- ----------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.prune_old_install_events()
RETURNS INTEGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog, public
AS $$
DECLARE
  deleted_count INTEGER;
BEGIN
  DELETE FROM public.install_events WHERE ts < NOW() - INTERVAL '24 months';
  GET DIAGNOSTICS deleted_count = ROW_COUNT;
  RETURN deleted_count;
END;
$$;

REVOKE EXECUTE ON FUNCTION public.prune_old_install_events() FROM anon;
REVOKE EXECUTE ON FUNCTION public.prune_old_install_events() FROM authenticated;
