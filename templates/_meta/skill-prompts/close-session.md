# Close session — skill prompt

This file contains everything you need to create a `close-session` skill in your AI tool. The skill runs the close protocol from the {{COMPANY_NAME}} vault's `SCHEMA.md` § 5: updates the project brief, verifies a knowledge-Ingest happened this session, appends the vault log, reports what changed, and generates a continuation prompt for next time.

Run this at the end of every working session. Even a 5-minute session ends with a close. The discipline is the point.

---

## How to install in your AI tool

Pick the section for your tool. The skill body (`## The skill — copy this`) is the same regardless of which tool you use.

### Claude Code

1. Create the folder `~/.claude/skills/close-session/` (mkdir if it doesn't exist).
2. Inside that folder, create `SKILL.md`.
3. Copy the entire section below `## The skill — copy this` into the new `SKILL.md` file.
4. Restart Claude Code (or reload skills).
5. Verify it's loaded: in a session, type `/close-session` — it should appear in the slash-command autocomplete.

### Cowork

Cowork's skill mechanism is still evolving as of v1.0.0 of this bundle. Two pragmatic options:

- **Quick path:** when you want to close a session, paste the body of `## The skill — copy this` directly into your Cowork conversation. The AI will run it from the paste.
- **Persistent path:** package the body as a Cowork plugin per [Cowork's plugin docs](https://cowork.anthropic.com/docs/plugins).

### Codex / opencode / other `AGENTS.md`-aware tools

Append the body of `## The skill — copy this` to your home `~/.codex/AGENTS.md` (or equivalent) under a `## Custom skills` section. Or invoke it directly per-session by pasting the body.

### Any other tool

The body is self-contained. Tell your AI: *"Run this skill"* and paste the content. Same result.

---

## The skill — copy this

```markdown
---
name: close-session
description: Run the close protocol for a session working against the {{COMPANY_NAME}} vault at {{VAULT_ABSOLUTE_PATH}}. Use at the end of every session — even short ones. The protocol is defined in the vault's SCHEMA.md § 5; this skill executes it: updates the project brief if one exists, verifies at least one Ingest ran, appends log.md with what happened, reports KB writes, and generates a continuation prompt for next session. Triggers on "close out", "let's close this session", "/close-session", "wrap up", "end session", or any close paraphrase.
---

# Close session

This skill ends the current session by capturing what happened into the {{COMPANY_NAME}} vault so it isn't lost. Skipping the close leaves the session's decisions in someone's head but not on disk — the exact failure mode that vaults rot from.

## Pre-flight

1. Confirm the {{COMPANY_NAME}} vault is mounted at `{{VAULT_ABSOLUTE_PATH}}`. If not, ask the user where the vault is or whether they want to close without writing to it (rare; usually the answer is to mount and continue).
2. Read `{{VAULT_ABSOLUTE_PATH}}/SCHEMA.md` § 5 (Close procedure) and § 3 (the three operations: Ingest / Query / Lint) so you know the conventions.

## Step 1 — Update the project brief (if one exists)

If this session was working against a project that has a `brief.md`, locate it and update it:

- Append a row to the Session Log table at the bottom of the brief.
- Format: `| <next #> | <today> | <one-paragraph summary of what happened this session> | <comma-separated open items the next session should pick up> |`
- If a Deliverables table exists in the brief, update any rows whose status changed this session.
- Bump the brief's status line at the top if a phase changed (Shape → Build, Build → Test, Test → Ship).

If no project brief exists (e.g. this was an ad-hoc working session), skip this step. Don't manufacture a brief.

## Step 2 — Verify at least one Ingest ran

An "Ingest" is the operation defined in `SCHEMA.md` § 3 — capturing knowledge into the vault by writing or updating a wiki page, updating `index.md`, and appending `log.md`.

Walk through this session's history:

- Did any wiki page get created or updated? (Check files in `entities/`, `concepts/`, `comparisons/`, `queries/`.)
- Was `index.md` updated?
- Was `log.md` updated mid-session (separate from this close)?

If at least one Ingest happened: good, note what was ingested for Step 3.

If NO Ingest happened: this is a protocol-violation candidate. Ask the user gently: *"This session didn't ingest anything to the vault. Was there anything we discussed that's worth capturing as a wiki page before we close? If not, I'll log the reason."*

Common valid reasons to close without an Ingest:
- "This was just exploratory; nothing concrete enough to capture yet."
- "We were debugging code; the fix is in the codebase, not the vault."
- "Nothing changed; this was a status check."

Record the reason in the log entry below if no Ingest ran.

## Step 3 — Append `log.md`

Open `{{VAULT_ABSOLUTE_PATH}}/log.md`. Append a new entry at the TOP of the file (most recent first), under the format SCHEMA.md prescribes:

```
## [<today>] <project-name or "ad-hoc session"> — <one-line summary>
- Ingests: <comma-separated list of wiki pages created/updated this session, or "none — <reason>">
- Queries: <queries filed to queries/ this session, or "none">
- Brief updated: <yes / no / N/A>
- Notes: <anything else worth recording — surprising findings, decisions deferred, blockers>
```

Today's date in `YYYY-MM-DD` UTC.

## Step 4 — Report KB writes

Print a structured summary of every file you touched this session and why. Format:

```
KB writes this session:
- {{VAULT_ABSOLUTE_PATH}}/<path/to/file> — <created/appended/modified> — <one-line reason>
- ...
```

Include the vault log entry you just wrote. Include the brief update if you made one. Include any wiki pages.

This serves two purposes: it gives the user a final review surface ("did the right things land?") and it makes the audit trail explicit.

## Step 5 — Generate the continuation prompt

Generate a copy-paste-ready opener for the next session. The opener should:

- Name the project (if applicable)
- Tell the next session's AI to mount the vault at `{{VAULT_ABSOLUTE_PATH}}` and read SCHEMA + CONTEXT first
- Point at the most relevant project brief / session stub if one exists
- Name the immediate next thing the user (or AI) should do based on what was open at end-of-session

Format:

```
Suggested opener for next session
---------------------------------
"<copy-paste prompt that re-establishes context for the next session>"
```

Keep it tight (3-5 sentences). The point is for the user to paste it and get the next session's AI loaded with the right context in one shot.

## Step 6 — Close report

Print a short, structured close report:

```
Session closed.

Project:         <name or "ad-hoc">
Ingests:         <count> (or "none — <reason>")
Brief updated:   <yes / no / N/A>
Log entry:       written to {{VAULT_ABSOLUTE_PATH}}/log.md
KB writes:       <count> files touched (see list above)
Continuation:    <one-line summary of the opener above>
```

Done. The user can close the conversation.
```

---

## When you've installed it

Test it at the end of a real working session. Verify:

- The vault's `log.md` got a new entry at the top with today's date
- If you were working against a project with a brief, the brief got a new Session Log row
- You got a copy-paste continuation prompt that actually makes sense
- The close report enumerated the files you touched

If the close ran and nothing surprised you, you have the discipline in place. Use it on every session. After 30 days you'll have a vault that tells you everything that happened.

---

## Common modifications worth knowing about

The body above is the minimum-viable close. Extensions you might want to add later:

- **Inbound channel drain** — if your operation has dedicated inbox files where other AI agents file work for you (a Hermes-like multi-agent setup), add a step that reads those files and triages them at close. The Absolution Labs canonical version of this skill does this; the version you have here doesn't, because it'd be confusing for a single-agent user.
- **Cross-vault sync** — if you maintain multiple vaults, add a step that propagates relevant new wiki pages between them.
- **Telegram/Slack push** — if your team needs notification when a session closes, add a step that posts the close report to a channel.

All of these are user-side customisations. The skill is yours to edit.

---

*This prompt is part of the Obsidian Company Memory skill, distributed by Absolution Labs LTD. MIT-licensed; modify freely.*
