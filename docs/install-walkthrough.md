# Install walkthrough

A step-by-step reading-version of what happens when you install the Obsidian Company Memory skill. Useful if you'd rather read than watch the Loom — or if you need to vet the procedure before running it (regulated-sector due diligence, IT review, sceptical-by-default temperament). Either is a good reason.

> **This document mirrors what the skill actually does.** The procedure the AI follows lives in [SKILL.md](../SKILL.md); this walkthrough is the human-readable description of the same nine steps. The two MUST stay in sync — if you spot a divergence, that's a bug. Email `info@absolutionlabs.com` and we'll fix it.
>
> The Loom walkthrough on [absolutionlabs.com](https://absolutionlabs.com) shows the same procedure visually, in about 7 minutes. Same content, different format.

---

## Before you begin

You will need:

- About 25 minutes of uninterrupted time. The install itself is fast (~5 min of skill activity); the rest is you reading what's there + watching the round-trip test work.
- A laptop running macOS 12+, Windows 10/11, or a recent Linux distro.
- An **empty folder** inside a cloud-synced location (Dropbox, iCloud, OneDrive, Google Drive), OR a local-only folder you're willing to back up yourself.
- Obsidian installed locally. Download from [obsidian.md/download](https://obsidian.md/download); free, no account needed. Install it, then close it — don't create a vault yet.
- One AI tool: Cowork (browser-based, easiest), Claude Code (terminal), Codex, or opencode.

You will NOT need:

- A credit card.
- A sign-up or account creation with us.
- Any prior terminal / coding experience.
- A particular operating system version beyond the minimum.

---

## Pre-flight (what the skill checks before doing anything)

When you trigger the skill ("Set up my Obsidian company memory" or equivalent), it runs three safety checks before writing a single byte to your disk. Nothing happens to your folder until all three pass.

### Check 1 — Worktree refusal

If you happen to be running this from inside a git worktree (a rare developer state — most users will never encounter it), the skill stops and asks you to relaunch from your main project folder. This prevents real work landing on an ephemeral branch that might get cleaned up later.

### Check 2 — Mount and writability

The skill confirms that:

- You've granted directory access to the target vault folder (in Cowork, this is a one-click "Allow" prompt; in Claude Code, it's the current working directory).
- The folder is writable. It probes by creating and deleting a tiny temp file. If the probe fails — typically a permissions issue or a cloud sync lock — the skill surfaces the error and stops.

### Check 3 — Skill bundle integrity

The skill verifies that all the files it needs to scaffold are present in its own installation. If the bundle is incomplete (rare; usually means an interrupted download), it stops and asks you to re-install. It does NOT try to fill in missing pieces — partial installs are a failure shape we specifically avoid.

If all three pass, you'll see the first gate.

---

## Step 1 — The compliance gate

Three checkboxes appear on screen. The skill cannot proceed unless all three are ticked. This is the first surface where you confirm — to yourself and on the record — that the install is appropriate.

```
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

**Box 2 is the one that matters most for regulated-sector users.** We don't enforce anything about your provider — we can't. But the gate makes you think about it before any data lands. If your industry has DPA requirements for the content you plan to store, check them before ticking.

If you can't honestly tick all three: **don't force-tick**. Resolve the underlying question first. The gate is not a friction tax; it's the trust signal.

---

## Step 2 — Refuse-to-scaffold gate

The skill lists the contents of the target folder. The rule is binary:

- **Empty folder** → proceed.
- **Anything else** → refuse, with a clear message.

"Anything else" includes any existing `.obsidian/` folder, any `.md` file at any depth, any non-hidden file or folder. Hidden OS metadata (`.DS_Store`, `Thumbs.db`, `desktop.ini`) is ignored.

If your folder isn't empty, the skill will not install into it — by design. There is no `--force` flag and there isn't going to be one. To install, either:

- Create a fresh empty folder, OR
- Move the existing contents elsewhere and re-run.

If you have an existing Obsidian vault and want to add this skill's structure on top of it: that's currently out of scope. Email `info@absolutionlabs.com` — we'll help with a manual migration.

---

## Step 3 — The two-question intake

The skill asks two questions, batched in a single prompt:

### Question 1 — Company name

> What is the name of the company this vault is for?

Type your company name. It must be 1–80 characters and use ordinary punctuation. The skill rejects unusual characters that could break templates (angle brackets, backticks, curly braces, control chars). Most company names — including "Acme Bros LTD", "Smith & Jones Co.", or "Anything-Hyphenated" — work fine.

This name appears in your vault's templates wherever the placeholder `{{COMPANY_NAME}}` was — `SCHEMA.md`, `CONTEXT.md`, `index.md`, `log.md`, `HOW-TO-USE-THIS.md`, and the welcome page.

### Question 2 — Sync provider

> Is this folder synced by Dropbox, iCloud, OneDrive, Google Drive, or local-only (no cloud sync)?

Pick one. This answer:

- Goes into the anonymous telemetry ping (if you don't opt out) so we can detect provider-specific failures.
- Is recorded in `_meta/scaffold-version.txt` inside your vault as a fingerprint.
- Doesn't change the install itself — every provider produces the same vault.

If you pick `local-only`, the skill adds a quiet reminder at the end about quarterly zip backups, since you don't have cloud sync versioning as a safety net.

---

## Step 4 — Date format auto-detect

You won't see this step on screen — the skill auto-detects your system locale and picks a sensible date format preference (DD/MM/YYYY for UK / EU / AU, MM/DD/YYYY for US, YYYY-MM-DD ISO for East Asia and fallback). It records the preference in `_meta/expectations.yml` for downstream tools.

Note: regardless of preference, all the YAML frontmatter dates inside vault pages use ISO `YYYY-MM-DD` — that's a technical requirement of how the lint logic works. The preference exists for tools that want it; it doesn't affect frontmatter.

---

## Step 5 — Telemetry surface

The skill renders the telemetry disclosure and an opt-out checkbox:

> This skill sends a single anonymous install ping to Absolution Labs LTD so we can detect installs that fail and fix them quickly. The ping contains: a randomly-generated UUID for this install (no link to your name, company, or vault contents), the skill version (currently `1.0.0`), your operating system family (e.g. "darwin", "win32", "linux"), the install surface (Cowork or Code), the sync provider you confirmed in Step 3, and whether the install succeeded or failed.
>
> It contains no other data. The endpoint is hosted in the EU; data is retained for 24 months and can be deleted on request by emailing `privacy@absolutionlabs.com` with the UUID shown below.
>
> Full privacy policy: [absolutionlabs.com/privacy](https://absolutionlabs.com/privacy).
>
> `[ ]` I prefer NOT to send this ping. (Default: send.)

**What we receive if you don't opt out:**

| Field | Example | Why |
|---|---|---|
| UUID | `7c2e3a14-9b8d-4f12-bc55-2e0c41d8a9b3` | Random; no link to you. The only handle to request deletion. |
| skill | `obsidian-company-memory` | Identifies which skill |
| version | `1.0.0` | Detect installs failing on a specific version |
| os | `darwin` / `win32` / `linux` | Detect installs failing on a platform |
| surface | `cowork` / `code` | Prioritise fixes by surface |
| sync_provider | `dropbox` / `icloud` / etc. | Detect installs failing on a provider |
| outcome | `attempted` / `success` / `failed` | The funnel — failures are the most useful signal |
| failure_step | `round_trip` (optional) | If failed, which step (short string, capped at 64 chars) |
| ts | `2026-06-03T12:34:56Z` | When the ping was sent (UTC) |

**Nothing else.** No IP, no email, no company name, no vault contents.

If you tick the opt-out box, no pings are sent for this install. The install proceeds identically.

You'll see your UUID at the end of the install — note it down if you might want deletion later.

---

## Step 6 — Scaffold writes

This is the main work step. About 20 files land in your folder over a few seconds. The skill writes each in a deliberate order; if any single write fails, the skill stops cleanly and tells you which file failed (it does not try to continue partway).

The files that land:

**At your vault root:**

- `SCHEMA.md` — the rulebook every AI session reads first
- `CONTEXT.md` — long-term memory for your company
- `index.md` — table of contents (always in sync)
- `log.md` — audit trail of every session
- `HOW-TO-USE-THIS.md` — the Phase 2 living guide you'll read next
- `CLAUDE.md.template` and `AGENTS.md.template` — project stubs that get used the first time you scaffold a project with `new-project-setup`

**Under `concepts/`:**

- `claude-operating-principles.md` — five starter principles for working with the AI

**Under `_meta/`:**

- `expectations.yml` — lint thresholds (editable)
- `scaffold-version.txt` — which version of the skill scaffolded this vault
- `templates/entity.md`, `concept.md`, `query.md` — page templates

**Under `.obsidian/`:**

- `app.json`, `appearance.json`, `core-plugins.json`, `community-plugins.json`, `hotkeys.json` — Obsidian's own config files, with sensible defaults

**Empty folders ready to be filled:**

- `entities/`, `comparisons/`, `queries/`, `raw/articles/`, `raw/transcripts/`, `raw/assets/`, `lint-reports/`

Every file is markdown, YAML, or JSON. No binaries. No secrets. No telemetry data inside the vault itself.

After writing, the skill re-reads each file to verify it parses cleanly. If anything is malformed, it stops before the round-trip test.

---

## Step 7 — The round-trip test

The skill creates one real wiki page so you can see the system work end-to-end. This is the proof step.

Specifically, it:

1. Creates `entities/test-welcome.md` with proper YAML frontmatter and a wikilink to `[[CONTEXT]]`.
2. Updates `index.md` to add an entry for the new page under the Entities section.
3. Verifies the initial `log.md` entry is in place.
4. Asks you to verify the result in Obsidian.

The verification has five clicks:

1. Open Obsidian → **File → Open vault** → pick your scaffolded folder.
2. In the file explorer on the left, confirm you see: `SCHEMA.md`, `CONTEXT.md`, `index.md`, `log.md`, `HOW-TO-USE-THIS.md`, and folders `entities/`, `concepts/`, `_meta/`.
3. Open `entities/test-welcome.md`. You should see a page titled "Welcome to your `<your-company-name>` vault."
4. Click the `[[CONTEXT]]` wikilink in that page. It should open `CONTEXT.md`.
5. Open `index.md`. You should see `entities/test-welcome` listed under Entities.

Reply "verified" once all five work. If one doesn't — most often a wikilinks-disabled config — see [troubleshooting.md](troubleshooting.md) § "I see SCHEMA.md but the wikilink in test-welcome.md doesn't resolve."

**Do not skip this step.** It's the difference between "the skill says it worked" and "you've seen it work."

---

## Step 8 — Phase 2 handoff

The skill confirms `HOW-TO-USE-THIS.md` is in your vault root and tells you to read it next:

> A Phase 2 living guide is in your vault root at `HOW-TO-USE-THIS.md`. It covers the weekly lint habit, the close-session protocol, how to capture knowledge mid-session, common failures, and recovery. Read it once now (about 10 minutes) and bookmark the path; revisit any time you need a reminder.

This is the canonical handoff. The install (Phase 1) is complete. Ongoing use (Phase 2) is governed by the living guide. The two are deliberately separate — the install is a one-off, the guide is the long-lived reference.

---

## Step 9 — Final message + continuation prompt

The skill prints a summary:

```
Your <company-name> vault is set up.

Vault location:     <absolute-path>
Files created:      <count>
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
info@absolutionlabs.com — replies within one business day.

Privacy
-------
absolutionlabs.com/privacy
Delete your telemetry UUID at any time by emailing privacy@absolutionlabs.com
with the UUID shown above.
```

Plus a suggested opener for your next session:

> "Mount the vault at `<vault-absolute-path>`. Read SCHEMA.md and CONTEXT.md. I want to start by capturing what `<company-name>` does and who its customers are — fill in the 'About `<company-name>`' section in CONTEXT.md and ingest it."

That opener is the lowest-friction first real use of the vault. It exercises the Ingest operation and populates the most load-bearing template field. Recommended.

---

## If anything goes wrong

The skill is designed to fail clearly, not silently. If something doesn't work:

- **Mid-install error** — the skill stops, lists which files were written successfully and which failed, and tells you to delete the folder contents and re-run. It does not try to "continue from where we left off." Partial scaffolds are not recoverable; delete-and-restart is the safe answer.
- **Round-trip test fails** — Obsidian shows something different from what the skill said it would. Walk through [docs/troubleshooting.md](troubleshooting.md) § "Round-trip verification failures" — five specific causes covered there.
- **Telemetry can't reach the endpoint** — non-blocking. Your install still works. The skill notes the failure in the final message but doesn't stall.
- **Slow file writes (>10s per file)** — usually a cloud sync provider throttling `.obsidian/` writes. Pause sync, complete the install, resume sync. Covered in [docs/troubleshooting.md](troubleshooting.md) § "Pathologically slow write".
- **You're stuck on something not covered above** — email `info@absolutionlabs.com`. Response within one business day, replied to by a human. If you're a tester, you can also WhatsApp Rob directly using the number you have for him.

---

## What this walkthrough doesn't cover

- **Ongoing use of the vault** — that's [HOW-TO-USE-THIS.md](../templates/HOW-TO-USE-THIS.md), which lands in your vault during install. Read it after install completes.
- **Forking the skill for your own variant** — [docs/customisation.md](customisation.md).
- **Upgrading or rolling back** — [docs/upgrading.md](upgrading.md).
- **Compatibility specifics for your OS / agent / sync provider** — [COMPATIBILITY.md](../COMPATIBILITY.md).
- **Why we designed each step the way we did** — [brief.md](../brief.md) Key Decisions table.

---

## Drift discipline (for maintainers)

If you're reading this as a maintainer rather than an installer:

- This file and [SKILL.md](../SKILL.md) describe the same procedure from two angles. SKILL.md is what the AI executes; this is the human-readable companion.
- When SKILL.md changes (a new step, a renamed gate, a different question), this file must change in the same commit. Otherwise users read documentation that doesn't match reality — the doc-code drift failure shape.
- The pre-release manifest lint at [scripts/lint_manifest.py](../scripts/lint_manifest.py) doesn't currently check parity between SKILL.md and this walkthrough. Adding a check is a Chunk 5 v2 candidate.

Until that lint check exists: the discipline is manual. The cost of getting it wrong is users hitting "the docs say click here, but the AI asked me something else" — which corrodes trust fast.

---

*Cross-references: [SKILL.md](../SKILL.md), [README.md](../README.md), [TESTERS.md](../TESTERS.md), [loom-script.md](../loom-script.md), [docs/troubleshooting.md](troubleshooting.md), [docs/privacy-policy.md](privacy-policy.md), [templates/HOW-TO-USE-THIS.md](../templates/HOW-TO-USE-THIS.md).*
