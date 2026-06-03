# Companion skills

Two skills that pair with the main [Obsidian Company Memory](../README.md) install skill. They handle the ongoing-use lifecycle: starting projects against your vault, and closing sessions cleanly.

| Skill | Purpose | Run when |
|---|---|---|
| [`open-obsidian-project`](open-obsidian-project/SKILL.md) | Scaffold a new project folder pointed at your vault | Start of a new project |
| [`close-obsidian-project`](close-obsidian-project/SKILL.md) | Run the session-close protocol (update brief, verify ingest, append vault log, generate continuation prompt) | End of every working session |

Both names use `-obsidian-project` as a suffix so they don't collide with any other "open project" / "close session" skills you already have for non-Obsidian work.

---

## Install

### Claude Code

**Auto-install (recommended).** The main `obsidian-company-memory` install skill, when run on Claude Code, copies both companion skills to `~/.claude/skills/` as part of the install procedure. You don't need to do anything; restart Code after install and both skills will appear.

If you missed the auto-install (e.g. installed a previous version of the bundle by hand), do it manually:

```bash
# Assuming you cloned obsidian-company-memory to ~/.claude/skills/obsidian-company-memory/
cp -r ~/.claude/skills/obsidian-company-memory/companion-skills/open-obsidian-project ~/.claude/skills/
cp -r ~/.claude/skills/obsidian-company-memory/companion-skills/close-obsidian-project ~/.claude/skills/

# Restart Code; both /open-obsidian-project and /close-obsidian-project should now autocomplete.
```

### Cowork

**Multi-skill plugin (in test).** The bundle's `plugin.json` declares all three skills (main install + both companions) under one plugin. When you paste the install URL into Cowork, all three should install together. We are validating this in private beta; if Cowork's plugin system only installs the main skill, fall back to the manual path below.

**Manual fallback (if auto-install on Cowork doesn't work).** After installing the main `obsidian-company-memory` plugin, paste each of these URLs separately into Cowork's plugin install field:

```
https://raw.githubusercontent.com/absolutionlabs/obsidian-company-memory/main/companion-skills/open-obsidian-project/plugin.json

https://raw.githubusercontent.com/absolutionlabs/obsidian-company-memory/main/companion-skills/close-obsidian-project/plugin.json
```

(Standalone `plugin.json` files for each companion will be added in v1.1.1 if the multi-skill bundling doesn't carry across cleanly.)

### Codex / opencode

These tools read `AGENTS.md` at session start; they don't have a separate skill mechanism. Two options:

1. **Inline at session start.** Append a "Custom skills" section to your home `~/.codex/AGENTS.md` (or equivalent) and paste each `SKILL.md` body into it.
2. **Reference from your project's session stub.** When `open-obsidian-project`'s output writes `<project>/AGENTS.md`, append a line at the top pointing at the companion skills' canonical URLs so the AI knows where to find them. The session-stub template already supports this pattern.

### Any other tool

Each `SKILL.md` body is self-contained. Tell your AI: *"Run this skill"* and paste the content of the relevant `SKILL.md` file. Same outcome as a native install.

---

## Skill collision handling

Both companion skills use `obsidian-project` in their names to avoid colliding with generic "open project" / "close" / "close session" skills you may have for non-Obsidian work. If you already have a skill named exactly `open-obsidian-project` or `close-obsidian-project` — unlikely, but possible if you've forked an earlier version — the auto-install procedure refuses cleanly with a "skill already exists at this name" message. Move or rename your existing skill before re-running install.

---

## Version contract

These companion skills are versioned alongside the main bundle. v1.1.0 of `obsidian-company-memory` ships v1.1.0 of these two companion skills. If you upgrade the main bundle, the companions upgrade too; if you've customised your local copy of a companion skill, the auto-install detects the collision and asks you whether to overwrite (losing your edits) or skip (keeping your edits).

---

## Why two skills, not one (or three)?

**Two:** because the lifecycle has two distinct operating verbs — *start a project* and *close a session*. Both happen often enough to deserve their own skill; bundling them would force you to wade through irrelevant prompts at each invocation.

**Not one:** the Forge methodology this bundle is built on treats project-start and session-close as distinct phases. Conflating them would teach the wrong mental model.

**Not three:** earlier drafts considered a separate `start-session` skill that opens an existing project. We cut it because the natural shape is "tell the AI which project to open and what you want to do" — a one-liner the user types, not a skill invocation.

---

## Use at your own risk

These skills are part of the Obsidian Company Memory bundle, provided "AS IS" without warranty of any kind under the MIT License. They are for general informational and educational purposes only and do not constitute professional advice. AI-generated outputs from any project scaffolded or closed via these skills may contain errors and must be independently verified before reliance. **Read [DISCLAIMERS.md](../DISCLAIMERS.md) in full before installing, forking, or relying on anything in this bundle.**

*© 2026 Absolution Labs. AbsolutionLabs Ltd, registered in England and Wales (Company No. 17091663). Registered office: 15 Westbury Road, London SE20 7QL.*
