# Companion skills

Two skills that pair with the main [Obsidian Company Memory](../README.md) install skill. They handle the ongoing-use lifecycle: starting projects against your vault, and closing sessions cleanly.

| Skill | Purpose | Run when |
|---|---|---|
| [`open-obsidian-project`](open-obsidian-project/SKILL.md) | Scaffold a new project folder pointed at your vault | Start of a new project |
| [`close-obsidian-project`](close-obsidian-project/SKILL.md) | Run the session-close protocol (update brief, verify ingest, append vault log, generate continuation prompt) | End of every working session |

Both names use `-obsidian-project` as a suffix so they don't collide with any other "open project" / "close session" skills you already have for non-Obsidian work.

---

## Install

Both companions ship as separate zips on the [latest GitHub Release](https://github.com/absolutionlabs/obsidian-company-memory/releases/latest). The install paradigm is the same as the main `obsidian-company-memory` bundle: upload a zip via Cowork's Upload-skill UI, or unzip into your Code skills folder.

### Cowork

1. Download both zips from the [latest GitHub Release](https://github.com/absolutionlabs/obsidian-company-memory/releases/latest):
   - `open-obsidian-project-vX.Y.Z.zip`
   - `close-obsidian-project-vX.Y.Z.zip`
2. In Cowork: **Skills → Upload skill → drag-drop each**. Restart if Cowork prompts.
3. Confirm both appear in your skills list. Each zip is small (~4 KB) and contains only a `SKILL.md` — no extra files, no surprises.

### Claude Code

If you have a local clone of the main bundle, copy each companion folder into `~/.claude/skills/`:

```bash
cp -r ~/.claude/skills/obsidian-company-memory/companion-skills/open-obsidian-project ~/.claude/skills/
cp -r ~/.claude/skills/obsidian-company-memory/companion-skills/close-obsidian-project ~/.claude/skills/

# Restart Code; both /open-obsidian-project and /close-obsidian-project should now autocomplete.
```

If you don't have a local clone, download the same two zips from the GitHub Release and unzip each into a new folder under `~/.claude/skills/`:

```bash
mkdir -p ~/.claude/skills/open-obsidian-project
unzip ~/Downloads/open-obsidian-project-vX.Y.Z.zip -d ~/.claude/skills/open-obsidian-project/

mkdir -p ~/.claude/skills/close-obsidian-project
unzip ~/Downloads/close-obsidian-project-vX.Y.Z.zip -d ~/.claude/skills/close-obsidian-project/
```

The native `claude plugin marketplace add absolutionlabs/obsidian-company-memory` path is queued for v1.3.0 (needs `.claude-plugin/marketplace.json` at the repo root).

### Codex / opencode

These tools read `AGENTS.md` at session start; they don't have a separate skill mechanism. Two options:

1. **Inline at session start.** Download both zips from the GitHub Release, unzip each, and append the body of each `SKILL.md` to your home `~/.codex/AGENTS.md` (or equivalent) under a "Custom skills" section.
2. **Reference from your project's session stub.** When `open-obsidian-project`'s output writes `<project>/AGENTS.md`, append a line at the top pointing at the companion skills' canonical URLs so the AI knows where to find them. The session-stub template already supports this pattern.

### Any other tool

Each `SKILL.md` body is self-contained. Tell your AI: *"Run this skill"* and paste the content of the relevant `SKILL.md` file. Same outcome as a native install.

---

## Skill collision handling

Both companion skills use `obsidian-project` in their names to avoid colliding with generic "open project" / "close" / "close session" skills you may have for non-Obsidian work. If you already have a skill named exactly `open-obsidian-project` or `close-obsidian-project` — unlikely, but possible if you've forked an earlier version — the Cowork upload-skill UI surfaces a "skill already exists" error and refuses; on Claude Code the manual copy commands above will overwrite unless you rename your existing skill first.

---

## Version contract

These companion skills are versioned alongside the main bundle. The same vX.Y.Z tag on the GitHub Release ships all three (main + two companions) at matching versions, even when only one of them changed materially in a given release. If you upgrade the main bundle, re-download the companions too; manual re-upload (Cowork) or re-copy (Code) is required — there's no auto-update channel.

---

## Why two skills, not one (or three)?

**Two:** because the lifecycle has two distinct operating verbs — *start a project* and *close a session*. Both happen often enough to deserve their own skill; bundling them would force you to wade through irrelevant prompts at each invocation.

**Not one:** the Forge methodology this bundle is built on treats project-start and session-close as distinct phases. Conflating them would teach the wrong mental model.

**Not three:** earlier drafts considered a separate `start-session` skill that opens an existing project. We cut it because the natural shape is "tell the AI which project to open and what you want to do" — a one-liner the user types, not a skill invocation.

---

## Use at your own risk

These skills are part of the Obsidian Company Memory bundle, provided "AS IS" without warranty of any kind under the MIT License. They are for general informational and educational purposes only and do not constitute professional advice. AI-generated outputs from any project scaffolded or closed via these skills may contain errors and must be independently verified before reliance. **Read [DISCLAIMERS.md](../DISCLAIMERS.md) in full before installing, forking, or relying on anything in this bundle.**

*© 2026 Absolution Labs. AbsolutionLabs Ltd, registered in England and Wales (Company No. 17091663). Registered office: 15 Westbury Road, London SE20 7QL.*
