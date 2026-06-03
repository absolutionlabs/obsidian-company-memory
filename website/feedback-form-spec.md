# Feedback form spec

For v1 of the skill, **the feedback "form" is the email address `info@absolutionlabs.com`**. No actual form needed. This file documents the decision + what to capture if you ever decide to add one.

---

## Why not a form for v1

Three reasons:

1. **Volume is low.** This skill is a sales-tool not a mass-market product. Feedback will come in handfuls, not floods. A mailbox handles that cleanly.
2. **Forms friction the response.** Especially for the audience (regulated-sector founders). An email is conversational; a form is a survey.
3. **No PII storage to manage.** Email replies live in the mailbox you already monitor. A form would mean a database, retention rules, DSAR plumbing — all for a low-volume signal.

The README, SKILL.md final message, TESTERS.md, Loom Scene 10, and install page all point at `info@absolutionlabs.com`. That's the canonical surface.

---

## When you might add a form

Add one when:

- Feedback volume exceeds ~5/week and triage becomes a tax
- You want to bucket feedback for analytics (e.g. "% of testers who flagged the compliance gate")
- A specific tester cohort has a pattern of feedback you want to track at scale
- Anonymous feedback becomes important (some testers won't email under their own name)

Until at least two of those become true: don't add a form.

---

## If you do add one — what to capture

A minimum-viable form captures only what the email-only path captures, plus the analytical bucketing:

| Field | Required | Notes |
|---|---|---|
| Name | Optional | Email-only path has this as the sender's name |
| Email | Required if they want a reply | If unchecked, the form becomes anonymous |
| OS | Required | Bucket: macOS / Windows / Linux / Other |
| Agent CLI | Required | Bucket: Cowork / Code / Codex / opencode / Other |
| Sync provider | Required | Bucket: Dropbox / iCloud / OneDrive / Google Drive / Local-only / Other |
| Installed version | Optional | Auto-populate from referrer query string if linked from `/obsidian` |
| Overall reaction | Required | Bucket: Loved / Liked / Neutral / Disliked / Hated. NOT a numeric scale — buckets read more honestly. |
| What worked | Required | Free text, 100-char min, 2000-char max |
| What didn't work | Required | Same |
| Anything you'd want different | Optional | Free text |
| Permission to thank you publicly | Optional | Checkbox |
| Want notification when v1 ships? | Optional | Checkbox; if yes, email captured for one-time send only |

Form should fit on one screen on a laptop. Mobile: progressive disclosure is fine; multi-step is not.

---

## Don't capture

- IP address (unless legally required for spam protection — and document it if so)
- Browser fingerprint
- Time-on-page beyond "filled the form" or "didn't"
- Geographic location beyond what the user volunteers
- The contents of any other tab they have open

---

## Where the data goes

If you do build the form:

- Submissions land in the same Supabase project as the install telemetry (separate table: `feedback_submissions`)
- Same region (London)
- Same retention (24 months)
- DSAR covers both tables (the helper script extends with a UNION delete)
- Privacy policy gets a §3.5 row for the feedback data

The schema would be:

```sql
CREATE TABLE public.feedback_submissions (
  id              BIGSERIAL PRIMARY KEY,
  submitted_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  name            TEXT,
  email           TEXT,
  os              TEXT,
  agent_cli       TEXT,
  sync_provider   TEXT,
  version         TEXT,
  reaction        TEXT CHECK (reaction IN ('loved', 'liked', 'neutral', 'disliked', 'hated')),
  what_worked     TEXT NOT NULL,
  what_didnt      TEXT NOT NULL,
  what_different  TEXT,
  permit_thank    BOOLEAN DEFAULT FALSE,
  want_launch_notification BOOLEAN DEFAULT FALSE
);
ALTER TABLE public.feedback_submissions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "anon can insert feedback" ON public.feedback_submissions FOR INSERT TO anon WITH CHECK (true);
```

Same RLS pattern as `install_events`: anon INSERT only, service role for everything else.

---

## v1 decision: defer

Don't build the form for v1. Email-only is the right shape for the volume we expect. Revisit at month 3 if volume justifies it.

---

*Decision logged 2026-06-03.*
