---
name: close-obsidian-project
description: Close a working session against an Obsidian Company Memory vault project. Use at the end of every session — even short ones. Triggers on "close out the session", "close-obsidian-project", "wrap up the session", "end this session", "/close-obsidian-project", or any close paraphrase. Updates the project brief's session log if one exists, verifies at least one Ingest happened, appends a dated entry to the vault's log.md, reports every KB write made this session, generates a copy-paste continuation prompt for the next session, and prints a structured close report. Named `close-obsidian-project` (not `close-session`) so it can coexist with any other "close" or "close session" skill you may have for non-Obsidian work.
version: 1.1.0
license: MIT
publisher: Absolution Labs LTD
support: info@absolutionlabs.com
---

# Close Obsidian Project

This skill ends a working session by capturing what happened into the Obsidian Company Memory vault, so the session's decisions and discoveries don't stay trapped in conversation history. Skipping the close is how vaults rot — the work happened, but the vault doesn't know about it.

The skill is named `close-obsidian-project` so it can coexist with any other "close" or "close session" skill you have for non-Obsidian work. The skill closes a SESSION (not the project itself); the naming uses "project" for namespace uniqueness, but the operation is session-scoped.

---

## Pre-flight

1. **Confirm the Obsidian Company Memory vault is mounted.** Ask the user for the vault's absolute path if not already known. The vault path is typically remembered from the project's session stub (`CLAUDE.md` or `AGENTS.md`) — read that file if available.
2. **Read the vault's `SCHEMA.md` § 5 (Close procedure) and § 3 (the three operations: Ingest / Query / Lint)** so you know the conventions before writing.

If the vault isn't mounted: ask the user where the vault is, OR offer to close without writing to it (rare; usually the right answer is mount and continue).

---

## Step 1 — Update the project brief (if one exists)

If this session was working against a project that has a `brief.md`, locate it and update it:

- Append a row to the Session Log table at the bottom of the brief.
- Format: `| <next #> | <today> | <one-paragraph summary of what happened this session> | <comma-separated open items the next session should pick up> |`
- If a Deliverables table exists, update any rows whose status changed this session.
- Bump the brief's status line at the top if a phase changed (Shape → Build, Build → Test, Test → Ship).

If no project brief exists (e.g. ad-hoc working session): skip this step. Don't manufacture a brief.

---

## Step 2 — Verify at least one Ingest ran this session

An "Ingest" is the operation defined in the vault's `SCHEMA.md` § 3 — capturing knowledge by writing or updating a wiki page, updating `index.md`, and appending `log.md`.

Walk through this session's history:

- Did any wiki page get created or updated? Check `entities/`, `concepts/`, `comparisons/`, `queries/`.
- Was `index.md` updated to register any new page?
- Was anything else materially written that's worth surfacing?

**If at least one Ingest happened:** note what was ingested; you'll list it in Step 3.

**If NO Ingest happened:** ask the user gently:

> This session didn't ingest anything to the vault. Was there anything we discussed that's worth capturing as a wiki page before we close? If not, I'll log the reason.

Common valid reasons to close without an Ingest:
- "This was just exploratory; nothing concrete enough to capture yet."
- "We were debugging code; the fix is in the codebase, not the vault."
- "Nothing changed; this was a status check."

Record the reason in the log entry below if no Ingest ran. Honest audit trail beats forced ingests.

---

## Step 3 — Append `log.md`

Open `<vault>/log.md`. Append a new entry at the TOP of the file (most recent first), under the format SCHEMA.md prescribes:

```
## [<today>] <project-name or "ad-hoc session"> — <one-line summary>
- Ingests: <comma-separated list of wiki pages created/updated, or "none — <reason>">
- Queries: <queries filed to queries/ this session, or "none">
- Brief updated: <yes / no / N/A>
- Notes: <anything else worth recording — surprising findings, decisions deferred, blockers>
```

Use today's date in `YYYY-MM-DD` UTC.

---

## Step 4 — Report KB writes

Print a structured summary of every file you touched this session and why. Format:

```
KB writes this session:
- <vault>/<path/to/file> — <created/appended/modified> — <one-line reason>
- ...
```

Include:
- The vault log entry you just wrote.
- The brief update (if you made one in Step 1).
- Every wiki page or scaffold file touched.

This gives the user a final review surface ("did the right things land?") and makes the audit trail explicit.

---

## Step 5 — Generate the continuation prompt

Generate a copy-paste-ready opener for the next session. The opener should:

- Name the project (if applicable).
- Tell the next session's AI to mount the vault at the absolute path and read SCHEMA + CONTEXT first.
- Point at the most relevant project brief / session stub if one exists.
- Name the immediate next thing the user (or AI) should do, based on what was open at end-of-session.

Format:

```
Suggested opener for next session
---------------------------------
"<copy-paste prompt that re-establishes context for the next session>"
```

Keep it tight (3–5 sentences). The point is for the user to paste it and get the next session's AI loaded with the right context in one shot.

---

## Step 6 — Close report

Print a short, structured close report:

```
Session closed.

Project:         <name or "ad-hoc">
Ingests:         <count> (or "none — <reason>")
Brief updated:   <yes / no / N/A>
Log entry:       written to <vault>/log.md
KB writes:       <count> files touched (see list above)
Continuation:    <one-line summary of the opener above>
```

Done. The user can close the conversation.

---

## Common modifications worth knowing about

The body above is the minimum-viable close. Extensions you might want to add later (yours to edit — MIT license):

- **Inbound channel drain** — if your operation has dedicated inbox files where other AI agents file work for you (a multi-agent setup), add a step that reads those files and triages them at close. The Absolution Labs canonical version of this skill does this; the version you have here doesn't, because it'd be confusing for a single-agent user.
- **Cross-vault sync** — if you maintain multiple vaults, add a step that propagates relevant new wiki pages between them.
- **Telegram / Slack push** — if your team needs notification when a session closes, add a step that posts the close report to a channel.

All of these are user-side customisations. The skill is yours.

---

## Why this skill exists separately from the main `obsidian-company-memory` install skill

The install skill (run once per vault) scaffolds the vault itself. This skill (run at every session close) writes session results back to the vault. They are deliberately separate: install-time vs ongoing-use. Mixing them would either bloat the install or require running the install repeatedly.

---

## Use at your own risk

This skill is part of the Obsidian Company Memory bundle (v1.1.0+), provided "AS IS" without warranty of any kind under the MIT License. It is for general informational and educational purposes only and does not constitute professional advice. AI-generated outputs from any vault scaffolded by the parent bundle may contain errors and must be independently verified before reliance. **Read the bundle's [DISCLAIMERS.md](https://github.com/absolutionlabs/obsidian-company-memory/blob/main/DISCLAIMERS.md) in full before installing, forking, or relying on anything from this bundle.**

*© 2026 Absolution Labs. AbsolutionLabs Ltd, registered in England and Wales (Company No. 17091663). Registered office: 15 Westbury Road, London SE20 7QL.*
