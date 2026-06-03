---
title: Skill prompts — overview
created: {{TODAY}}
updated: {{TODAY}}
type: concept
tags: [skill-prompts, setup]
---

# Skill prompts for {{COMPANY_NAME}}

This folder holds **two prompts you'll use to create custom skills in your AI tool**. The bundle ships the prompts, not the skills — because each AI tool (Cowork, Claude Code, Codex, opencode, etc.) installs custom skills differently, and your specific workflow matters more than ours does.

Five minutes once at install time; saves you hours on every session afterward.

## What's here

| File | What it does | When you use it |
|---|---|---|
| `new-project-setup.md` | Scaffolds a new project folder, points it at this vault, writes the session stub | When you start a new piece of work |
| `close-session.md` | Updates the project brief, verifies an Ingest ran, appends the log, reports KB writes, generates a continuation prompt | At the end of every working session |

Both prompts reference your vault at `{{VAULT_ABSOLUTE_PATH}}` directly. You don't need to edit anything inside them — they're ready to install as-is.

## How to install each skill

Each prompt file has its own surface-by-surface install instructions at the top. Pick your AI tool, follow the steps, restart the tool. Skill is live.

If you use more than one AI tool: install in all of them. The prompts are identical; the install path is the only thing that differs.

## What to do if you change AI tools

The skills you install in one tool don't transfer to another. If you start using a new AI tool, re-install the same prompts there using the new tool's mechanism. The prompts themselves don't change.

## Updating the prompts later

If a new version of the Obsidian Company Memory skill ships an updated prompt, you'll see the updated text in your vault (after running the update procedure in `docs/upgrading.md`). To pick up the change in your AI tool, re-install the skill — same install procedure, just overwrites the previous version.

## A note on the design

We could have shipped pre-built skills directly. We didn't. Reasons:

1. **No one-size-fits-all skill installer.** Cowork and Claude Code use different mechanisms; the next AI tool will use something else again.
2. **Your customisations belong to you.** Once you install these, they're yours to modify. We don't want to be in your tool's skill folder.
3. **You learn what a skill is by building one.** Five minutes to create a skill from a prompt teaches you more about your AI tool than reading the docs would.

The folder structure is the rendering layer. The prompts are the product.

---

*Maintained by Absolution Labs LTD. Questions: `info@absolutionlabs.com`.*
