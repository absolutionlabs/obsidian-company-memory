---
name: obsidian-company-memory
description: Scaffold an Obsidian-based company-memory vault — single-company, three-layer architecture, AI-session-ready in about 25 minutes. Walks the user through a compliance gate, a 2-question intake, an idempotent vault scaffold, and a round-trip test that proves the system works end-to-end. Single source, dual install paths (Cowork plugin + Claude Code user-global skill). Triggers when the user says "set up Obsidian", "install company memory", "scaffold a vault", "set up the Absolution Labs vault", "I want a company memory system", or pastes the install URL. Hands off to `new-project-setup` for the first project; does NOT scaffold projects itself. Ships from Absolution Labs LTD.
version: 1.0.0
license: MIT
publisher: Absolution Labs LTD
support: info@absolutionlabs.com
---

# Obsidian Company Memory — Setup Skill

This skill scaffolds a working Obsidian vault for a single company, configured for AI-assisted long-term memory. The vault layout, schema, operating principles, and starter pages all come from the `templates/` folder shipped alongside this file. The procedure below is what the agent runs end-to-end.

The skill is the install moment. The Phase 2 living guide (`HOW-TO-USE-THIS.md`) ships into the vault and governs ongoing use. The skill never re-runs in production once the vault exists — re-running on an existing vault is a refusal case, not an upgrade case.

**Surface-aware.** The same SKILL.md runs on Cowork (browser, mounted-directory access) and Claude Code (local, file system). Surface differences are called out inline; both paths produce the same vault.

---

## When to invoke

Trigger the skill when the user:

- Says some variant of "set up Obsidian", "scaffold a vault", "install the company memory system", "I want a long-term memory for my company".
- Pastes an install URL pointing at this skill (the canonical install page lives on absolutionlabs.com; users may also have a versioned variant from there).
- Confirms they have an empty folder they want turned into a vault.

Do NOT invoke if:

- The user already has a vault and is asking "how do I add a page". That is Phase 2 / `HOW-TO-USE-THIS.md` territory — point them at the guide.
- The user wants to migrate an existing vault. The skill refuses non-empty target directories. A migration skill is future work (currently out of scope).
- The user wants a multi-client routing layer (`clients/<slug>/`). This skill is single-company by permanent design (key decision #4 in `brief.md`). Point them at the Absolution Labs Client Knowledge Base architecture if they need multi-client.

---

## Pre-flight (do not skip)

### Step 0a — Worktree refusal check (OP #19)

If the session is running inside a git worktree, the skill must refuse and ask the operator to relaunch from the main checkout. Worktrees produce ephemeral CWDs that strand real work on transient branches.

Run:

```
git rev-parse --git-dir 2>/dev/null
```

If the output contains `worktrees` (the path will look like `.git/worktrees/<name>`), STOP. Tell the user:

> This session is running inside a git worktree at `<path>`. Scaffolding a real vault here would strand it on a transient branch. Please relaunch this skill from the main project checkout (`<main-path>`) and try again.

Then halt. Do not proceed.

### Step 0b — Confirm the target directory is mounted and writable

- **Cowork:** the user must have granted directory access to the target vault folder via `request_directory`. If no mount is active, ask them to grant it now via Cowork's directory connector and stop until confirmed.
- **Claude Code:** the target folder must be the current working directory or an absolute path the user has explicitly named. If unclear, ask: "Which absolute path should I scaffold the vault into?"

Verify writability by attempting a no-op write (`.tmp-skill-probe` then delete). If the write fails, surface the error and stop.

### Step 0c — Verify skill-bundle integrity

Confirm the skill bundle contains the expected files:

```
SKILL.md                                       (this file)
README.md
LICENSE
COMPATIBILITY.md
templates/SCHEMA.md
templates/CONTEXT.md
templates/index.md
templates/log.md
templates/HOW-TO-USE-THIS.md
templates/concepts/claude-operating-principles.md
templates/_meta/expectations.yml
templates/_meta/templates/entity.md
templates/_meta/templates/concept.md
templates/_meta/templates/query.md
templates/.obsidian/app.json
templates/.obsidian/appearance.json
templates/.obsidian/community-plugins.json
templates/.obsidian/core-plugins.json
templates/.obsidian/hotkeys.json
templates/CLAUDE.md.template
templates/AGENTS.md.template
```

If anything is missing, the bundle is corrupt — STOP and tell the user to re-install from the canonical URL. Do not improvise replacement content.

---

## Step 1 — First-screen compliance gate (3 mandatory checkboxes)

Before any data is written, surface the compliance gate. This is a hard gate: every box must be ticked. If any is left unchecked, refuse to scaffold and explain why.

Render (verbatim shape, adapted to the surface's question UI — `AskUserQuestion` on Code, the Cowork equivalent):

```
Before this skill writes any files to your folder, please confirm three things.
These are compliance prerequisites; the skill cannot continue without all three.

[ ] 1. The folder I am about to scaffold into is a folder I own or am
       authorised to write to. It does not contain any client data, regulated
       data, or personal data belonging to someone else.

[ ] 2. The cloud sync provider hosting this folder (Dropbox / iCloud / OneDrive
       / Google Drive / local-only) is one my organisation permits for the
       type of content I intend to store. I have checked any applicable data
       processing agreement (DPA) requirements.

[ ] 3. I understand this vault will be a record of facts and decisions about
       my company. Absolution Labs LTD has no access to its contents at any
       point. If I have opted in to telemetry, only anonymous install +
       success pings are sent.
```

If all three are ticked: log to internal session memory that the gate passed, then continue. If any is unticked: refuse, surface a one-paragraph explanation of which box would be needed (no "next time" — re-run the skill when the user is ready), and exit.

**Why this gate exists.** Regulated-sector prospects (the explicit target audience per the pre-mortem in `brief.md`) need compliance concerns surfaced BEFORE any data is written. A scaffold that ran first and asked questions later would have already damaged trust by the time the gate appeared.

---

## Step 2 — Refuse-to-scaffold gate (decision #14)

List the contents of the target directory. The gate is binary:

- **Empty directory** → proceed.
- **Anything else** → REFUSE.

"Anything else" includes:

- Any existing `.obsidian/` folder.
- Any `.md` file at any depth.
- Any non-hidden file or folder of any kind.

Hidden OS metadata (`.DS_Store`, `Thumbs.db`, `desktop.ini`) is acceptable — skip those when scanning.

If refused, render:

> The target folder is not empty. This skill scaffolds into empty folders only — it never overwrites existing work or merges with an existing vault. To install: create a new empty folder, mount it (or `cd` into it), and re-run the skill. If you need to migrate an existing vault, that is currently out of scope; email `info@absolutionlabs.com` and we will help directly.

Then exit. Do not offer to "back up the existing folder" or "scaffold around" the existing files — the refusal is the safe answer.

---

## Step 3 — Two-question intake

Ask both questions in a single batched call (one `AskUserQuestion` invocation with two questions on Code; the Cowork equivalent). Do not ask sequentially — batching keeps the install moment tight.

**Question 1 — Company name.**

> What is the name of the company this vault is for?

Validation:

- Length: 1–80 characters.
- Character class: letters, digits, spaces, hyphens, ampersands, apostrophes, periods, and `LTD`/`Ltd`/`Limited`/`Inc`/`Co` suffixes allowed.
- Reject anything containing `<`, `>`, `{`, `}`, `|`, `\`, backticks, or control characters.

This name is the literal substitution for `{{COMPANY_NAME}}` everywhere in `templates/`.

**Question 2 — Confirm sync location.**

> Is this folder synced by Dropbox, iCloud, OneDrive, Google Drive, or local-only (no cloud sync)?

Multiple-choice; one answer. The answer is captured for telemetry (no PII) and for the telemetry-display step. It does not change the scaffold itself — every sync provider produces the same vault.

If "local-only", append a one-line note to the post-scaffold message reminding the user that loss of the local disk means loss of the vault, and recommend a quarterly zip backup per `HOW-TO-USE-THIS.md` § Backup hygiene.

---

## Step 4 — Auto-detect date format

Do NOT ask the user. Auto-detect from the system locale.

- **Claude Code:** read `Get-Culture` on PowerShell (Windows), `defaults read -g AppleLocale` on macOS, `locale` on Linux. Fall back to ISO if detection fails.
- **Cowork:** read the user's locale from the session context if available; fall back to ISO otherwise.

Map:

| Locale region | Date format used |
|---|---|
| en-GB, en-IE, en-AU, en-NZ, fr-*, de-*, es-*, it-*, nl-*, pt-* | DD/MM/YYYY |
| en-US, en-CA, en-PH | MM/DD/YYYY |
| ja-*, zh-*, ko-*, hu-*, lt-*, sv-* | YYYY-MM-DD (ISO) |
| anything else | YYYY-MM-DD (ISO) |

This format is stored in `_meta/expectations.yml` as `date_format_preference` (informational only — all frontmatter dates remain ISO `YYYY-MM-DD` regardless of preference, because lint logic depends on it).

---

## Step 5 — Telemetry display + opt-out

Render verbatim:

> This skill sends a single anonymous install ping to Absolution Labs LTD so we can detect installs that fail and fix them quickly. The ping contains: a randomly-generated UUID for this install (no link to your name, company, or vault contents), the skill version (currently `1.0.0`), your operating system family (e.g. "darwin", "win32", "linux"), the install surface (Cowork or Code), the sync provider you confirmed in Step 3, and whether the install succeeded or failed.
>
> It contains no other data. The endpoint is hosted in the EU; data is retained for 24 months and can be deleted on request by emailing `privacy@absolutionlabs.com` with the UUID shown below. Full privacy policy: [absolutionlabs.com/privacy](https://absolutionlabs.com/privacy).
>
> [ ] I prefer NOT to send this ping. (Default: send.)

If the user ticks the opt-out box, skip all telemetry calls for the rest of the session.

If not opted out, fire the install-attempted ping NOW (before scaffold begins) and the install-succeeded or install-failed ping at the end of Step 9. Failures are signal too.

Show the user their UUID (so they can request deletion later if they choose) in the final message.

**Telemetry implementation note.** The endpoint is the Supabase PostgREST API of an Absolution Labs project hosted in West Europe (London) — `https://vujwcvqiwwpncnhgxjsu.supabase.co/rest/v1/install_events`. The skill ships the project's public anon key in `plugin.json.telemetry.anon_key`; Postgres-level row-level security (RLS) restricts the anon role to INSERT only — anon cannot SELECT, UPDATE, or DELETE anything. CHECK constraints on every column enforce the 8-field payload schema; a Postgres trigger rate-limits to 5 inserts per 60 seconds per UUID. The anon key is public by design (Supabase's security model rests on RLS, not key secrecy). See `telemetry/` folder and `brief.md` for the full setup.

---

## Step 6 — Scaffold the vault (idempotent)

This is the main write step. Every operation is idempotent: running it on a directory that already contains the file is a no-op, never an overwrite.

Substitution variables (build once before any write):

| Placeholder | Value |
|---|---|
| `{{COMPANY_NAME}}` | from Step 3 Question 1 |
| `{{TODAY}}` | ISO date in UTC, format `YYYY-MM-DD` |
| `{{VAULT_ABSOLUTE_PATH}}` | the resolved absolute path of the target directory |
| `{{PROJECT_NAME}}` | NOT substituted at this stage (left as literal `{{PROJECT_NAME}}` in `CLAUDE.md.template` and `AGENTS.md.template` — `new-project-setup` substitutes per-project at first invocation) |
| `{{PROJECT_DESCRIPTION}}` | same — left as literal |

**Substep 6.1 — Create folder structure.**

Create the following directories under the vault root. Skip any that already exist:

```
entities/
concepts/
comparisons/
queries/
raw/
raw/articles/
raw/transcripts/
raw/assets/
lint-reports/
_meta/
_meta/templates/
.obsidian/
```

**Substep 6.2 — Write `.obsidian/` config files.**

Copy each of these from `templates/.obsidian/` to `<vault>/.obsidian/` verbatim (no substitution — JSON, not markdown):

- `app.json`
- `appearance.json`
- `core-plugins.json`
- `community-plugins.json`
- `hotkeys.json`

If any of these files already exists at the destination, STOP and refuse — this should be impossible after the Step 2 gate, but defence-in-depth catches a partially-scaffolded retry. Surface the path and exit.

**Substep 6.3 — Write the schema and context files at vault root.**

For each, read the template, substitute `{{COMPANY_NAME}}` and `{{TODAY}}`, write to the vault root:

- `SCHEMA.md` → vault root
- `CONTEXT.md` → vault root
- `index.md` → vault root
- `log.md` → vault root
- `HOW-TO-USE-THIS.md` → vault root (the Phase 2 living guide)

**Substep 6.4 — Write the concepts page.**

- `concepts/claude-operating-principles.md` → from `templates/concepts/claude-operating-principles.md`, substitute `{{TODAY}}` (no company-name substitution needed).

**Substep 6.5 — Write `_meta` files.**

- `_meta/expectations.yml` → from template; append a `date_format_preference: <detected>` line for downstream tools that want it.
- `_meta/templates/entity.md`, `concept.md`, `query.md` → from `templates/_meta/templates/`, substitute `{{TODAY}}`.

**Substep 6.6 — Write the project-stub templates (do NOT instantiate).**

These files are templates for `new-project-setup` to read when the user creates their first project. They live at the vault root with the `.template` suffix preserved:

- `CLAUDE.md.template` → vault root, leave `{{PROJECT_NAME}}`, `{{PROJECT_DESCRIPTION}}`, `{{COMPANY_NAME}}`, `{{VAULT_ABSOLUTE_PATH}}`, `{{TODAY}}` as literal placeholders for the downstream skill.
- `AGENTS.md.template` → same.

These files are NOT in `index.md` (they are not wiki pages); they sit at the root as a discoverable handoff to the next skill.

**Substep 6.7 — Write a one-line scaffold-version marker.**

Write `_meta/scaffold-version.txt` containing:

```
skill: obsidian-company-memory
version: 1.0.0
scaffolded: {{TODAY}}
date_format_preference: <detected>
sync_provider: <from Step 3 Q2>
telemetry_uuid: <UUID or "opted-out">
```

This is the fingerprint used by `docs/upgrading.md` and the lint to detect drift between vault and skill version. No PII.

**Substep 6.8 — Verify the write batch.**

Read every file just written and confirm it parses (markdown loads cleanly, JSON parses, YAML parses). If anything fails, surface which file and which error, and STOP — do not proceed to the round-trip test on a corrupt scaffold.

---

## Step 7 — Round-trip test

The skill creates one real entity page end-to-end so the user can see the system work. This is the proof step; skipping it leaves the user with a scaffolded but unverified vault.

**Substep 7.1 — Create the test entity.**

Write `entities/test-welcome.md` with substituted frontmatter and a body that includes a wikilink to `[[CONTEXT]]`:

```markdown
---
title: Welcome to your {{COMPANY_NAME}} vault
created: {{TODAY}}
updated: {{TODAY}}
type: entity
tags: [welcome, setup]
sources: []
---

# Welcome to your {{COMPANY_NAME}} vault

This is the first page in your company memory. It was created automatically
during setup so you can see what a wiki page looks like and verify the system
works end-to-end.

Feel free to delete this page once you have created your first real entry —
or keep it as a marker of when the vault began.

## What just happened

1. The Obsidian Company Memory skill scaffolded your vault folder.
2. It created this page and linked it to [[CONTEXT]].
3. It updated [[index]] to include this page.
4. It appended a one-line entry to [[log]].

If you can open this page in Obsidian and click through to [[CONTEXT]] from
the wikilink, the round-trip works.

## Next

Read [[HOW-TO-USE-THIS]] for the ongoing-use guide. When you are ready to
start your first real project, run the `new-project-setup` skill (it ships
separately in your AI tool's skill list).
```

**Substep 7.2 — Update `index.md`.**

Append under the `## Entities` section:

```
- [[entities/test-welcome]] — welcome page created at vault setup; safe to delete after first real page
```

**Substep 7.3 — Append `log.md`.**

The starter `log.md` already contains the initial scaffold entry (per `templates/log.md`). Verify it landed correctly post-substitution; if `{{TODAY}}` is still literal anywhere, fix it.

No new log entry is needed for the round-trip — the initial entry already mentions the welcome page implicitly via "round-trip test passed".

**Substep 7.4 — Tell the user to verify.**

Render:

> The vault is scaffolded and the test entity is in place. Please open Obsidian now and verify:
>
> 1. Click **Open folder as vault** and pick `<vault-absolute-path>`.
> 2. In the file explorer on the left, you should see: `SCHEMA.md`, `CONTEXT.md`, `index.md`, `log.md`, `HOW-TO-USE-THIS.md`, and folders `entities/`, `concepts/`, `_meta/` (others may be empty).
> 3. Open `entities/test-welcome.md`. You should see a page titled "Welcome to your `<company-name>` vault".
> 4. Click the `[[CONTEXT]]` wikilink in that page. It should open `CONTEXT.md`.
> 5. Open `index.md`. You should see `entities/test-welcome` listed under Entities.
>
> Reply "verified" once you have seen all five, or tell me which step did not work.

Wait for the user to confirm. If they report a problem, surface it; do not proceed to Step 9 with an unverified scaffold.

---

## Step 8 — Confirm `HOW-TO-USE-THIS.md` is in place

This step is mostly a check-and-tell — the file was already written in Substep 6.3. Confirm it exists at the vault root and the first 5 lines parse as valid YAML frontmatter. Then tell the user:

> A Phase 2 living guide is in your vault root at `HOW-TO-USE-THIS.md`. It covers the weekly lint habit, the close-session protocol, how to capture knowledge mid-session, common failures, and recovery. Read it once now (about 10 minutes) and bookmark the path; revisit any time you need a reminder.

This is the canonical handoff from "install moment" (Phase 1, this skill) to "ongoing use" (Phase 2, the guide). Reinforcing the split keeps the user from expecting the skill to do everything for them forever.

---

## Step 9 — Final message, telemetry close, handoff

**Substep 9.1 — Fire the success telemetry ping** (skip if user opted out in Step 5).

POST to: `https://vujwcvqiwwpncnhgxjsu.supabase.co/rest/v1/install_events`

Headers:

```
apikey: <plugin.json.telemetry.anon_key>
Authorization: Bearer <plugin.json.telemetry.anon_key>
Content-Type: application/json
Prefer: return=minimal
```

Body:

```json
{
  "uuid": "<UUID from Step 5>",
  "skill": "obsidian-company-memory",
  "version": "1.0.0",
  "os": "<darwin|win32|linux>",
  "surface": "<cowork|code>",
  "sync_provider": "<from Step 3 Q2>",
  "outcome": "success",
  "ts": "<ISO timestamp UTC>"
}
```

Expected response: `HTTP 201` (Created) with empty body.

If the call fails (network error, HTTP 400 from a schema-validation rejection, HTTP 429 from rate-limit), swallow silently — telemetry failure does not block the install. Log the failure to internal session state so the operator can see it on close. The same payload shape applies to the install-attempted ping (Step 5) and the install-failed ping (failure path); only the `outcome` field differs (`attempted` / `success` / `failed`).

**Substep 9.2 — Render the final message.**

```
Your <company-name> vault is set up.

Vault location:     <absolute-path>
Files created:      <count> (see list in chat above)
Round-trip test:    Passed
Phase 2 guide:      HOW-TO-USE-THIS.md at the vault root
Telemetry UUID:     <UUID or "opted out">

What to do next
---------------
1. Read HOW-TO-USE-THIS.md (about 10 minutes).
2. When you are ready to start your first real project, invoke the
   new-project-setup skill in your AI tool. It will scaffold a project
   folder pointing at this vault.
3. After your first working session, run a lint (just ask: "run a lint on
   the vault"). It will produce a baseline report you can compare against.

Feedback + support
------------------
info@absolutionlabs.com — replies within one business day. Anything that
felt clunky during setup, or did not work the way you expected: send it.

Privacy
-------
absolutionlabs.com/privacy
Delete your telemetry UUID at any time by emailing privacy@absolutionlabs.com
with the UUID shown above.
```

**Substep 9.3 — Suggest the continuation prompt for the next session.**

```
Suggested opener for your first real session:

  "Mount the vault at <vault-absolute-path>. Read SCHEMA.md and CONTEXT.md.
   I want to start by capturing what <company-name> does and who its
   customers are — fill in the 'About <company-name>' section in CONTEXT.md
   and ingest it."
```

This gives the user a frictionless first move that exercises the Ingest operation and populates the most-load-bearing template field (`CONTEXT.md` — "About {{COMPANY_NAME}}").

---

## Surface differences (Cowork vs Code)

| Step | Cowork behaviour | Code behaviour |
|---|---|---|
| 0a worktree check | N/A (no git in Cowork sandbox by default) | Run `git rev-parse --git-dir`; refuse if in worktree |
| 0b mount confirm | `request_directory` must already have fired | Working directory or explicit absolute path |
| 4 date auto-detect | Read session locale | Read OS locale via shell |
| 6 file writes | Write via mounted-directory tool | Write directly to disk |
| 9.1 telemetry | Cowork's HTTP egress | Local `curl` or HTTPS client |

The vault produced is byte-identical across surfaces. Surface differences are purely about HOW the files land; the WHAT is uniform.

---

## Failure modes and recovery

### Mid-scaffold failure

If Step 6 fails mid-write (network blip, disk full, permission revoked):

1. Do NOT attempt to "roll forward" — the partial scaffold is corrupt.
2. Surface every file that was successfully written and every file that failed.
3. Tell the user: "The scaffold did not complete. Please delete the contents of `<vault-path>` (you can verify each file against the list above) and re-run the skill. If the failure repeats, email `info@absolutionlabs.com` with the failure details."
4. Fire the `install-failed` telemetry ping (unless opted out).

Do NOT offer to "continue from where we stopped". Partial scaffolds are the failure shape from the brief's pre-mortem; the safe answer is delete-and-restart.

### Round-trip test failure

If the user reports that one of the five verification steps in Substep 7.4 did not work:

1. Walk them through diagnostic — which step, what they saw, what they expected.
2. Most common: Obsidian was opened against the wrong folder. Have them close and re-open against `<vault-absolute-path>`.
3. Next most common: wikilink-clicking is disabled. Settings → Files & Links → "Use [[Wikilinks]]" must be ON. (The `app.json` config sets this, but a user who edited it manually may have flipped it.)
4. If diagnosis fails, fire `install-failed` ping with `failure_step: round_trip`, surface support email.

### Telemetry endpoint unreachable

If the install-attempted ping in Step 5 fails to send (network, DNS, endpoint down):

1. Continue the install — telemetry failure does not block the user's vault.
2. Note in internal session state that telemetry was unreachable.
3. At final message, append a one-line note: "Telemetry could not be sent (endpoint unreachable); no impact on your vault."

### Pathologically slow file writes

If a single file write takes more than 10 seconds, assume the cloud sync provider is throttling and surface the issue. Some Dropbox-for-Business accounts apply per-second write limits to .obsidian/ folders; if detected, suggest the user pause Dropbox sync, re-run, and resume sync after the round-trip test passes.

---

## Idempotency contract

This skill is idempotent in one direction only: **on an empty directory, running it produces the same vault every time.**

It is NOT idempotent on a partially-scaffolded directory, on a directory with user edits, or on an existing vault. The Step 2 refuse-to-scaffold gate enforces this. A user wanting to re-scaffold must delete the existing contents first; a user wanting to upgrade an existing vault is handled by `docs/upgrading.md` (Chunk 6 deliverable), not by re-running this skill.

---

## What this skill does NOT do (and where the work goes instead)

| Need | Where it lives |
|---|---|
| Install Obsidian itself | User does this manually; preamble docs link `obsidian.md/download` |
| Install an agent CLI (Cowork / Code / Codex / opencode) | User installs separately; we don't bundle |
| Install Dataview / community plugins | User installs from Obsidian's browser; we don't ship plugin bundles (key decision #6) |
| Scaffold the first project folder | `new-project-setup` skill (key decision #8) |
| Initialise git in the vault | Cloud sync provides versioning; git is out of scope (key decision #9) |
| Schedule recurring lint | Out of scope; lint is manual-invocation only (key decision #5) |
| Multi-client `clients/<slug>/` layout | Permanently out of scope (key decision #4); use the AbsoLabs CKB shape for multi-client |
| Migrate an existing vault | Out of scope; refuse-to-scaffold blocks; future migration skill is potential follow-up |
| Custom SCHEMA per user | Ship one canonical SCHEMA; user can edit after scaffold; see `docs/customisation.md` |
| Auto-update warnings | Out of scope; users opt in to updates via `docs/upgrading.md` |

---

## Skill metadata for downstream tools

For agents / harnesses that introspect this file beyond the YAML frontmatter:

- **Triggers:** "set up obsidian", "scaffold a vault", "install company memory", install URL paste
- **Inputs:** target directory (mounted or CWD), 2 user-supplied answers (company name + sync provider), 3 compliance confirmations
- **Outputs:** scaffolded vault directory, 1 welcome entity, 1 install telemetry ping (opt-out)
- **Side effects:** writes ~20 files to user disk; sends 0–2 HTTPS pings to Absolution Labs telemetry endpoint
- **Idempotent:** yes, on empty directories only
- **Reversible:** yes, by deleting the vault directory (cloud sync provides version history)
- **Time-to-run:** ~5 minutes of skill time + ~20 minutes of user-side reading and Obsidian setup
- **Hard gates:** worktree refusal (OP #19), compliance gate (3 boxes), refuse-to-scaffold on non-empty directory, skill-bundle integrity check
- **Telemetry:** default-on, opt-out, anonymous UUID + 5 fields, EU-residency, 24-month retention, DSAR via UUID

---

*This skill is distributed by Absolution Labs LTD under the MIT license (see `LICENSE`). Support: `info@absolutionlabs.com`. Privacy: `https://absolutionlabs.com/privacy`. Compatibility: see `COMPATIBILITY.md` for tested Obsidian / agent / Dataview versions.*
