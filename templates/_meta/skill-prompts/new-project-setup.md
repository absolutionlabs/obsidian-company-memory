# New project setup — skill prompt

This file contains everything you need to create a `new-project-setup` skill in your AI tool. The skill scaffolds a project folder that points at the {{COMPANY_NAME}} vault at `{{VAULT_ABSOLUTE_PATH}}`, writes a session stub the AI reads at every project session, and (optionally) creates a project brief.

---

## How to install in your AI tool

Pick the section for your tool. The skill body (`## The skill — copy this`) is the same regardless of which tool you use.

### Claude Code

1. Create the folder `~/.claude/skills/new-project-setup/` (mkdir if it doesn't exist).
2. Inside that folder, create `SKILL.md`.
3. Copy the entire section below `## The skill — copy this` into the new `SKILL.md` file.
4. Restart Claude Code (or reload skills).
5. Verify it's loaded: in a session, type `/new-project-setup` — it should appear in the slash-command autocomplete.

### Cowork

Cowork's skill mechanism is still evolving as of v1.0.0 of this bundle. Two pragmatic options:

- **Quick path:** when you want to start a new project, paste the body of `## The skill — copy this` directly into your Cowork conversation. The AI will run it from the paste.
- **Persistent path:** package the body as a Cowork plugin per [Cowork's plugin docs](https://cowork.anthropic.com/docs/plugins). You can use this bundle's own `plugin.json` as a reference shape.

### Codex / opencode / other `AGENTS.md`-aware tools

These tools read `AGENTS.md` at session start. Two options:

- Append the body of `## The skill — copy this` to your home `~/.codex/AGENTS.md` (or equivalent) under a `## Custom skills` section. The AI will know to run it when you ask for "new project setup".
- Or invoke it directly per-session: paste the body when you want to use it.

### Any other tool

The body is self-contained. Tell your AI: *"Run this skill"* and paste the content. Same result.

---

## The skill — copy this

```markdown
---
name: new-project-setup
description: Scaffold a new project folder pointed at the {{COMPANY_NAME}} vault at {{VAULT_ABSOLUTE_PATH}}. Use when the user says "set up a new project", "start a new project", "/new-project-setup", or any close paraphrase. Creates the project folder structure, writes a session stub (CLAUDE.md or AGENTS.md) the AI reads on every future session, optionally creates a Forge-style brief, and outputs a continuation prompt for the next session.
---

# New project setup

This skill creates a new project folder that points at the {{COMPANY_NAME}} vault. Every session you run on this project will start by reading the vault's SCHEMA.md + CONTEXT.md, then the project's own brief and session stub. The result is that the AI shows up to every session with the right context loaded.

## Pre-flight

1. Confirm the {{COMPANY_NAME}} vault is mounted at `{{VAULT_ABSOLUTE_PATH}}`. If not, ask the user to mount it before continuing.
2. Read `{{VAULT_ABSOLUTE_PATH}}/SCHEMA.md` and `{{VAULT_ABSOLUTE_PATH}}/CONTEXT.md` so you know the vault's conventions.
3. Confirm the user wants to create a new project (not continue an existing one).

## Step 1 — Collect inputs

Ask the user (batch these in one prompt):

1. **Project name** — short, descriptive (e.g. "Q3 Trade Show Prep", "Klaviyo Migration", "New SKU Launch"). 3-80 chars.
2. **One-sentence description** — what this project is about, in plain English.
3. **Parent folder** — where should the project folder live? Suggest sensible defaults: a `Projects/` folder sibling to the vault, or wherever the user keeps active work.

## Step 2 — Derive the project slug

Lowercase the project name, replace spaces and underscores with hyphens, strip punctuation. Examples:

- "Q3 Trade Show Prep" → `q3-trade-show-prep`
- "Klaviyo Migration" → `klaviyo-migration`

Verify the resulting `<parent>/<slug>/` folder does NOT already exist. If it does, ask the user whether to pick a different name or use the existing folder.

## Step 3 — Create the project folder

Create the project folder at `<parent>/<slug>/`. Inside it, create these subfolders:

- `notes/` — running thoughts, meeting notes, anything not yet wiki-worthy
- `outputs/` — finished deliverables (PDFs, drafts, exported reports)
- `raw/` — source documents specific to this project (transcripts, contracts, etc.)

## Step 4 — Write the session stub

Read the template at `{{VAULT_ABSOLUTE_PATH}}/CLAUDE.md.template` (or `AGENTS.md.template` if the user's AI tool reads AGENTS.md instead).

Substitute these placeholders:

| Placeholder | Value |
|---|---|
| `{{PROJECT_NAME}}` | the project name from Step 1 |
| `{{PROJECT_DESCRIPTION}}` | the description from Step 1 |
| `{{COMPANY_NAME}}` | `{{COMPANY_NAME}}` (already substituted at vault scaffold) |
| `{{VAULT_ABSOLUTE_PATH}}` | `{{VAULT_ABSOLUTE_PATH}}` (same) |
| `{{TODAY}}` | today's date in `YYYY-MM-DD` UTC |

Write the substituted file as `<parent>/<slug>/CLAUDE.md` (or `AGENTS.md`). This is the file the AI will read at the start of every future session on this project.

## Step 5 — Optionally create a brief

Ask the user: *"Want me to scaffold a project brief? Useful for anything more involved than a one-session task."*

If yes, create `<parent>/<slug>/brief.md` with this minimal shape (the user can flesh it out later):

```
# <project-name> — Brief

**Created:** <today>
**Status:** Shape

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
| 1 | <today> | Project scaffolded. | Define scope; resolve open questions. |
```

If the user says no, skip this step. They can create a brief later by asking.

## Step 6 — Update the vault's log

In `{{VAULT_ABSOLUTE_PATH}}/log.md`, append a new entry above the existing entries:

```
## [<today>] new project — <project-name>
- Ingests: project folder scaffolded at <parent>/<slug>/
- Queries: none
- Brief updated: <yes if you created one, else N/A>
- Notes: First session on <project-name> will start with the session stub at <parent>/<slug>/CLAUDE.md
```

## Step 7 — Hand off

Tell the user:

```
Your <project-name> project is set up.

Project folder:  <parent>/<slug>/
Session stub:    <parent>/<slug>/CLAUDE.md
Brief:           <created or "you can scaffold one later by asking">
Vault log:       updated

Suggested opener for your first session on this project:

  "I'm starting work on <project-name>. Read the session stub at
   <parent>/<slug>/CLAUDE.md and the vault's SCHEMA.md and CONTEXT.md
   before doing anything else. Then we'll talk about [whatever your
   first sub-task is]."
```

## Idempotency

If the user runs this skill against an existing project folder, refuse cleanly:

> *"A project folder already exists at `<parent>/<slug>/`. To start fresh, pick a different name. To continue work on this project, just say 'I'm continuing the X project' and your AI will read the existing session stub."*

Do not overwrite existing project files.
```

---

## When you've installed it

Test it once on a throwaway project name like "test-project". Verify:

- The project folder was created at the path you specified
- `CLAUDE.md` (or `AGENTS.md`) is present in the project folder with placeholders substituted
- The vault's `log.md` got a new entry
- The AI gave you a sensible continuation prompt

If anything didn't work, the skill body is markdown — you can edit it directly in your AI tool's skill folder. Common tweaks:

- Adjust the parent-folder default in Step 1 Q3 to match where you actually keep projects
- Add or remove subfolder names in Step 3
- Change the brief template in Step 5 if you have your own preferred shape

---

*This prompt is part of the Obsidian Company Memory skill, distributed by Absolution Labs LTD. MIT-licensed; modify freely.*
