---
name: open-obsidian-project
description: Open a new project against an Obsidian Company Memory vault. Use when the user says "open a new project", "start a new Obsidian project", "/open-obsidian-project", "set up an Obsidian project", "scaffold a project against the vault", or any close paraphrase. Reads the vault's SCHEMA.md and CONTEXT.md, scaffolds a project folder structure (notes/, outputs/, raw/), writes a session-start stub (CLAUDE.md or AGENTS.md) the AI will read on every future session for that project, optionally creates a Forge-style project brief, appends an entry to the vault log, and prints a continuation prompt for the first real session on the project. Refuses if the target project folder already exists.
version: 1.1.0
license: MIT
publisher: Absolution Labs LTD
support: info@absolutionlabs.com
---

# Open Obsidian Project

This skill starts a new project against an Obsidian Company Memory vault. Every session you run on the project will start by reading the vault's SCHEMA.md + CONTEXT.md, then the project's own brief and session stub. The result: the AI shows up to every session on the project with the right context loaded, and your project knowledge accumulates as a by-product of normal work.

The skill is named `open-obsidian-project` so it can coexist with any other "new project" or "open project" skills you have for non-Obsidian work.

---

## Pre-flight

1. **Confirm the Obsidian Company Memory vault is mounted.** Ask the user for the vault's absolute path if not already known. If the user has only one such vault, the path is normally remembered from the `obsidian-company-memory` install — look for `_meta/scaffold-version.txt` at any folder the user mounts to confirm it's an OCM-shaped vault.
2. **Read the vault's `SCHEMA.md` and `CONTEXT.md`** so you know the company conventions before scaffolding.
3. **Confirm the user wants to create a NEW project** (not continue work on an existing one). If they want to continue an existing project, point them at the existing project folder's session stub and stop.

If the vault isn't mounted: ask the user to mount it via their AI tool's directory access first, then re-invoke.

---

## Step 1 — Collect inputs

Ask the user (batch in one prompt where the AI tool supports it):

1. **Project name** — short, descriptive (e.g. "Q3 Trade Show Prep", "Klaviyo Migration", "New SKU Launch"). 3–80 characters. Letters, digits, spaces, hyphens, ampersands, apostrophes.
2. **One-sentence description** — what this project is about, in plain English. Used in the brief and the session stub so future sessions land with the right framing.
3. **Parent folder** — where should the project folder live on disk? Suggest sensible defaults: a `Projects/` folder sibling to the vault, or wherever the user keeps active work. Do NOT scaffold inside the vault folder itself unless the user explicitly asks — projects live alongside the vault, not inside it.

Validation:
- Project name: 3–80 chars; reject `<`, `>`, `{`, `}`, `|`, `\`, backticks, control characters.
- Parent folder must exist and be writable.

---

## Step 2 — Derive the project slug

Lowercase the project name, replace spaces and underscores with hyphens, strip everything except `[a-z0-9-]`. Examples:

- "Q3 Trade Show Prep" → `q3-trade-show-prep`
- "Klaviyo Migration" → `klaviyo-migration`
- "Sipello — Phase 2" → `sipello-phase-2`

Verify the resulting `<parent>/<slug>/` folder does NOT already exist. If it does, refuse cleanly:

> A project folder already exists at `<parent>/<slug>/`. To start a fresh project, pick a different name. To continue work on the existing project, say "I'm continuing the X project" and I'll read its existing session stub.

Do NOT overwrite existing project files.

---

## Step 3 — Create the project folder

Create `<parent>/<slug>/` and these subfolders inside it:

- `notes/` — running thoughts, meeting notes, anything not yet wiki-worthy
- `outputs/` — finished deliverables (PDFs, drafts, exported reports)
- `raw/` — source documents specific to this project (transcripts, contracts, etc.)

---

## Step 4 — Write the session stub

Read the template the vault scaffolded at the vault root: `<vault>/CLAUDE.md.template` (if the user's AI tool reads `CLAUDE.md`) or `<vault>/AGENTS.md.template` (for Codex / opencode / similar). Most users have both — pick based on the AI tool.

Substitute these placeholders in the template:

| Placeholder | Value |
|---|---|
| `{{PROJECT_NAME}}` | the project name from Step 1 |
| `{{PROJECT_DESCRIPTION}}` | the description from Step 1 |
| `{{COMPANY_NAME}}` | read from the vault's `_meta/scaffold-version.txt` (or `CONTEXT.md`) |
| `{{VAULT_ABSOLUTE_PATH}}` | the vault's absolute path |
| `{{TODAY}}` | today's date in `YYYY-MM-DD` UTC |

Write the substituted file as `<parent>/<slug>/CLAUDE.md` (or `AGENTS.md`). This is the file the AI will read at the start of every future session on this project. Don't skip it; it's how each session re-enters with the right context.

---

## Step 5 — Optionally create a project brief

Ask: *"Want me to scaffold a project brief? Useful for anything more involved than a one-session task."*

If yes, create `<parent>/<slug>/brief.md` with this minimal Forge-shaped starter (the user can flesh it out later):

```markdown
# <project-name> — Brief

**Created:** <today>
**Status:** Shape
**Vault:** <vault-absolute-path>

## Working backwards
*(What does done look like? Who benefits? What does it unlock?)*

## Scope
**In:** *(what's included)*
**Out:** *(what's explicitly NOT included)*

## Open questions
- *(things to resolve before serious work begins)*

## Session log
| # | Date | What happened | Open items |
|---|------|---|---|
| 1 | <today> | Project scaffolded via open-obsidian-project. | Define scope; resolve open questions. |
```

If the user says no, skip this step. They can create a brief later by asking.

---

## Step 6 — Update the vault's log

Open `<vault>/log.md`. Append a new entry at the TOP (most recent first), under the format SCHEMA.md prescribes:

```
## [<today>] new project — <project-name>
- Ingests: project folder scaffolded at <parent>/<slug>/
- Queries: none
- Brief updated: <yes if you created one, else N/A>
- Notes: First session on <project-name> will start with the session stub at <parent>/<slug>/CLAUDE.md
```

---

## Step 7 — Hand off

Print:

```
Your <project-name> project is set up.

Project folder:  <parent>/<slug>/
Session stub:    <parent>/<slug>/CLAUDE.md
Brief:           <created at <path> | "you can scaffold one later by asking">
Vault log:       updated

Suggested opener for your first session on this project:

  "I'm starting work on <project-name>. Mount the vault at <vault-absolute-path>.
   Read the session stub at <parent>/<slug>/CLAUDE.md and the vault's SCHEMA.md
   and CONTEXT.md before doing anything else. Then we'll talk about [whatever
   your first sub-task is]."
```

Done. The user can paste the suggested opener into their next AI session.

---

## Idempotency contract

This skill is idempotent on empty target folders only. Running it against an existing project folder is a refusal case (Step 2). The user must pick a different name, or explicitly continue work on the existing project.

---

## Why this skill exists separately from the main `obsidian-company-memory` install skill

The install skill (run once per vault) scaffolds the vault itself. This skill (run once per project) scaffolds project folders that point at the vault. They are deliberately separate: one is install-time, one is ongoing-use. Mixing them would either bloat the install or require running the install repeatedly. Per Decision #8 in the parent bundle's design.

---

## Use at your own risk

This skill is part of the Obsidian Company Memory bundle (v1.1.0+), provided "AS IS" without warranty of any kind under the MIT License. It is for general informational and educational purposes only and does not constitute professional advice. AI-generated outputs from any project scaffolded by this skill may contain errors and must be independently verified before reliance. **Read the bundle's [DISCLAIMERS.md](https://github.com/absolutionlabs/obsidian-company-memory/blob/main/DISCLAIMERS.md) in full before installing, forking, or relying on anything from this bundle.**

*© 2026 Absolution Labs. AbsolutionLabs Ltd, registered in England and Wales (Company No. 17091663). Registered office: 15 Westbury Road, London SE20 7QL.*
