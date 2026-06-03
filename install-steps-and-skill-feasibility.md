# Install Steps + Skill Feasibility Evaluation

*Draft v0.1. Companion to [current-setup-user-guide.md](current-setup-user-guide.md). Purpose: catalogue every step required to set up the system on a fresh machine, then evaluate whether a Claude Code skill can realistically automate it for non-technical users.*

---

## Part A — The full install / setup sequence on a fresh machine

This is what any non-technical user has to go through, end to end, to get from "I have a laptop" to "I just had my first session and something landed in the vault." I've broken it into seven phases.

### Phase 1 — Install Obsidian

| Platform | One-line install |
|---|---|
| macOS | `brew install --cask obsidian` (or download `.dmg` from [obsidian.md/download](https://obsidian.md/download)) |
| Windows | `winget install -e --id Obsidian.Obsidian` (or download `.exe` from same) |
| Linux | `snap install obsidian --classic`, AppImage from [github.com/obsidianmd/obsidian-releases](https://github.com/obsidianmd/obsidian-releases), `.deb`, or Flatpak |

No account is required for Obsidian itself. The app is free. (Obsidian Sync, the paid cross-device sync, is optional — most users either use Dropbox/iCloud/OneDrive for sync or don't sync at all.)

### Phase 2 — Create the vault

1. Open Obsidian. The first-run dialog asks "Open existing vault" or "Create new vault."
2. Choose **Create new vault**, give it a name (e.g. the company name), pick a parent folder (Dropbox folder if syncing, anywhere local if not).
3. Obsidian creates the folder and a hidden `.obsidian/` subfolder inside it. That's the vault.

Alternate path that a skill can drive: pre-build the vault folder + `.obsidian/` config on disk, then tell the user to use **Open folder as vault** instead of Create. Obsidian recognises the prepared folder and uses the config that's already there. This lets the skill ship a fully configured `.obsidian/` instead of the user having to click through setup screens.

### Phase 3 — Enable community plugins (one mandatory click)

Obsidian ships with community plugins disabled behind a feature called Restricted Mode — a deliberate security gate. To turn it off:

1. Settings → Community plugins → click **Turn on community plugins**.
2. Acknowledge the security warning.

This is the one unavoidable GUI step. A skill cannot bypass it (and shouldn't — it's a real security boundary). The skill walks the user through it with a screenshot.

Once Restricted Mode is off, a skill can install community plugins purely by dropping files on disk:

- `<vault>/.obsidian/plugins/<plugin-id>/main.js`
- `<vault>/.obsidian/plugins/<plugin-id>/manifest.json`
- `<vault>/.obsidian/plugins/<plugin-id>/styles.css` (where the plugin ships one)

Plus an entry in `<vault>/.obsidian/community-plugins.json` to mark the plugin as enabled.

The two community plugins we use:

- **Dataview** — release assets at [github.com/blacksmithgu/obsidian-dataview/releases](https://github.com/blacksmithgu/obsidian-dataview/releases)
- **Templater** — release assets at [github.com/SilentVoid13/Templater/releases](https://github.com/SilentVoid13/Templater/releases)

A skill downloads the latest release of each, drops the files into the right plugin folder, edits `community-plugins.json`. On next Obsidian launch the plugins are live.

### Phase 4 — Configure Obsidian's settings

Five JSON files inside `.obsidian/` control nearly everything:

| File | Controls |
|---|---|
| `app.json` | Link format, attachment folder, default new-file location |
| `appearance.json` | Theme, font, base text size, CSS snippets |
| `core-plugins.json` | Array of enabled built-in plugins (file-explorer, graph, backlinks, etc.) |
| `community-plugins.json` | Array of enabled community plugin IDs |
| `workspace.json` | Open tabs, pane layout |

A skill can write these directly. Caveat: write them while Obsidian is closed, because Obsidian may overwrite them on shutdown.

### Phase 5 — Drop in the starter wiki files

The skill writes these files at the vault root:

- `SCHEMA.md` — the rulebook
- `index.md` — the empty table of contents (will fill as pages are created)
- `log.md` — the empty audit trail
- `CONTEXT.md` — the per-vault pointer telling Claude what company this is and where to read rules from
- `concepts/claude-operating-principles.md` — the canonical cross-cutting rules page

And the empty folder structure:

```
<vault>/
├── SCHEMA.md
├── index.md
├── log.md
├── CONTEXT.md
├── entities/
├── concepts/
│   └── claude-operating-principles.md
├── comparisons/
├── queries/
├── raw/
│   ├── articles/
│   ├── transcripts/
│   └── assets/
└── _meta/
    └── expectations.yml
```

Trivially scriptable. The starter content is shipped with the skill itself.

### Phase 6 — Install the agent (Claude Code as default)

One of:

| Agent | One-line install |
|---|---|
| **Claude Code** (default) | macOS/Linux: `curl -fsSL https://claude.ai/install.sh \| bash` · Windows: PowerShell installer at `irm https://claude.ai/install.ps1 \| iex` · npm: `npm install -g @anthropic-ai/claude-code` |
| Codex (OpenAI) | `curl -fsSL https://chatgpt.com/codex/install.sh \| sh` (macOS/Linux) or PowerShell equivalent (Windows) |
| opencode (open source) | `curl -fsSL https://opencode.ai/install \| bash` |
| Hermes (optional, server-side) | Provisioned separately; out of scope for the laptop-only path |

After install, first run opens a browser to sign in (Claude Code → Anthropic account; Codex → OpenAI account; opencode → choice of provider). Token gets written into the agent's config. After that, every subsequent session is silent.

A skill can detect what's already installed and prompt the user to install one if nothing is present.

### Phase 7 — Install our skill stack + wire the project

Skills live at `~/.claude/skills/<skill-name>/SKILL.md` (Claude Code) or as `AGENTS.md`-driven procedures (Codex / opencode). The setup skill drops:

- `new-project-setup` — for scaffolding new projects
- `wiki-ingest` — for capturing knowledge into the vault
- `close-full` — for the close-of-session protocol
- `realignment` — for bringing older projects up to current schema

Then the skill creates the user's first project folder (with a `CLAUDE.md` stub that points at the vault) and runs one test session: write a hello-world entity page, ingest it, close, verify the page is in `index.md` and `log.md` was appended.

If that test passes the system is live.

### Phase 8 (optional) — Wire scheduled maintenance

This is where the install effort concentrates if you want the daily / weekly / monthly audits running automatically. Three real paths:

1. **Local OS-native scheduling.** Skill writes a launchd `.plist` (macOS), a Task Scheduler XML (Windows), or a crontab line (Linux). Most reliable, most code, three separate code paths. Fails if the laptop is asleep when the job is supposed to fire.
2. **Python APScheduler as a long-running user daemon.** One codebase, three autostart configurations (still three platforms). Same sleep/wake problem.
3. **Remote scheduler on a small VPS** (the "Hermes" pattern we use). One config, doesn't care if the laptop is asleep, runs in one place and syncs results back to the vault via Dropbox / git. Costs a few dollars a month for the VPS.

For a non-technical user, **option 3 is the cleanest** — but it requires the user to either rent a VPS or use a shared one. For a fully laptop-only install, option 1 is the pragmatic default and the skill should ship per-OS templates.

---

## Part B — What this means for skill feasibility

### What a skill can do entirely on its own

Everything in the table below is fully scriptable from a Claude Code skill running on the user's machine.

| Step | Mechanism |
|---|---|
| Detect OS | `uname` / `$env:OS` |
| Install Obsidian | Per-OS package manager command (brew / winget / snap / curl + AppImage) |
| Create vault folder structure | `mkdir` + `Write` tool |
| Drop starter files (SCHEMA, index, log, CONTEXT) | `Write` tool against shipped templates |
| Download + install community plugins | `curl` GitHub release zips, unzip, place files |
| Write `.obsidian/*.json` configs | `Write` tool with shipped templates |
| Install Claude Code (or Codex, opencode) | Per-OS install command |
| Install our skill files into `~/.claude/skills/` | `Write` tool |
| Create the first project folder + `CLAUDE.md` stub | Existing new-project-setup skill |
| Initialise git inside the vault | `git init` |
| Run a smoke-test session | Skill orchestrates a test ingest |

### What a skill cannot do, and what the workaround is

| Step | Why a skill can't fully automate | Workaround |
|---|---|---|
| First-run Obsidian: "trust the app" macOS Gatekeeper prompt, Windows SmartScreen prompt | OS security UI | Screenshot + 30-second explainer in the skill output. One-time per user. |
| First-run vault: clicking "Open folder as vault" | Obsidian GUI requires it (unless we write `obsidian.json` directly, which is undocumented and risky) | Skill prepares the vault folder, tells user the exact menu path to open it. One click. |
| Enabling community plugins (Restricted Mode off) | Deliberate Obsidian security gate | Screenshot + explainer. One click. |
| Per-plugin trust on first enable | Obsidian security UI | Same — one click per plugin (Dataview, Templater). |
| Agent first-run sign-in (Anthropic / OpenAI / etc.) | Browser-based OAuth | Skill triggers the agent's first invocation, user signs in in browser, control returns. |
| Cloud sync setup (Dropbox / iCloud / OneDrive) | Outside the skill's scope; user has already done it or will do separately | Skill offers a "where do you want the vault?" prompt; if Dropbox/iCloud/OneDrive are detected as available, suggests them. |
| VPS provisioning (if user chooses option 3 for scheduling) | Outside skill scope; rent or reuse | Skill outputs a one-page "how to wire a $5 VPS" guide; defers to user. |

That's a total of **4–6 one-click GUI moments**, each well-documented with a screenshot. A non-technical user can absolutely follow this — it's no harder than installing Slack and connecting it to your workspace.

### What a skill can do, but where the effort concentrates

Three areas need real engineering, not just template-writing:

1. **Cross-platform OS detection and install dispatch.** The skill has to handle macOS / Windows / Linux gracefully, with fallbacks for users who don't have Homebrew / WinGet / Snap available. ~150 lines of bash/PowerShell per platform.

2. **Plugin version pinning and updates.** Obsidian plugins update frequently. The skill needs to pin to known-working versions of Dataview and Templater and have a refresh path when those drift. ~50 lines + a "check for plugin updates" sub-command.

3. **Scheduled-task setup (if shipped).** Per-OS schedulers, as covered. ~200 lines per platform if going fully native, or ~100 lines if shipping a Python APScheduler daemon with platform-specific autostart shims. Honest assessment: this is the most expensive part of the skill by far.

---

## Part C — The skill-vs-no-skill verdict

### Headline

**Yes, the skill is viable.** Non-technical users can run it and end up with a working system. The honest scope is a "configuration + scaffolding + plugin installation + first-project bootstrapping" skill, not a "100% zero-touch install" skill — because a few security-sensitive moments (Gatekeeper, Restricted Mode, browser sign-in) are GUI by design and shouldn't be bypassed even if they could be.

### Three good shapes the skill could take, in increasing scope

**Shape 1 — "Scaffold only" skill.** Assumes the user has already installed Obsidian and an agent CLI. The skill builds the vault, drops the plugins, writes the starter files, installs our skill stack, runs the smoke test. **Scope:** ~500 lines of skill code + templates. **User effort:** 5 minutes (mostly the install of Obsidian + Claude Code before running the skill). **Verdict: easiest to ship, low-risk, high-value.** This is the right v1.

**Shape 2 — "Install + scaffold" skill.** Adds Obsidian + agent install automation across macOS / Windows / Linux. **Scope:** ~1,200 lines (the install dispatch is the bulk). **User effort:** 2 minutes (sign in to Anthropic when prompted, click the one-time GUI prompts). **Verdict: significantly more polish, useful for true non-technical users who'd struggle with `brew install`.** Worth doing as v2.

**Shape 3 — "Install + scaffold + scheduled maintenance" skill.** Adds the cron/Task-Scheduler/launchd setup for the daily/weekly/monthly audits. **Scope:** ~1,800 lines, three OS-specific autostart paths. **User effort:** the same as Shape 2 + one VPS provisioning step if they take the remote-scheduler path. **Verdict: the most complete experience, but the scheduled-tasks layer is the part most likely to drift and need maintenance.** Ship as v3 once Shape 2 has proven itself in the wild.

I'd recommend building **Shape 1 first** (3–4 day build), shipping it to a small test group, and using their feedback to decide whether Shape 2 and Shape 3 are worth the additional engineering. That's the cheapest way to find out if the "non-technical user actually adopts this" hypothesis is true before investing the bigger effort.

### What "enables people to create their own versions" actually means

This is the right question to push on. Three different definitions:

1. **"Someone can run the skill and end up with the same setup we have."** Shape 1 delivers this for a slightly-technical user (knows how to install Obsidian and run a CLI). Shape 2 delivers it for a non-technical user. Both are realistic.

2. **"Someone can customise the skill — different schema rules, different plugins, different starter content — and produce their own variant."** This is fully open to anyone who can edit markdown and JSON, because the skill ships its templates as separate files rather than hardcoding them. We'd want to document the customisation points clearly. Maybe 200 words of docs + an explicit `templates/` folder inside the skill.

3. **"Someone can rebrand and resell the skill as their own product."** Possible if we license accordingly, but probably not the intent. Worth confirming with you.

### The honest risks

- **Obsidian plugin API drift.** Dataview and Templater are community-maintained. If their file layout changes, the skill breaks. Mitigation: pin versions, run a quarterly version-bump check.
- **Agent CLI changes.** Anthropic / OpenAI / opencode all evolve their CLIs. Same risk profile as plugin drift. Mitigation: skill detects current CLI version and prompts a re-run on major version bumps.
- **The "Restricted Mode" gate is the user's first impression.** If we don't handle the screenshot + explainer well, non-technical users get scared off here. Worth investing in the UX of that one moment.
- **Scheduled tasks (if shipped) are the long-tail support burden.** Every OS update changes something. Either ship the remote-scheduler path as the recommended option, or be prepared to maintain three platform scripts indefinitely.

### Recommended next decision

Pick a shape (1, 2, or 3) for v1. My recommendation is **Shape 1**, with explicit notes in the user-facing output that point at "and here's how to install Obsidian + Claude Code first" as separate steps for users who haven't already. That gets us to a shippable skill in days rather than weeks, and proves the concept before we invest in the install automation.

If you'd rather go bigger from day one, **Shape 2** is the right target — but budget 2–3x the effort.

---

## Open items for v0.2 of this doc

- Concrete plugin version pins (Dataview, Templater) once we've decided shape.
- Per-OS install command edge cases (Linux distros without snap; Windows machines without WinGet).
- The exact `AGENTS.md` translation of our `SKILL.md` files for Codex / opencode users.
- A first cut of the skill's actual file layout (`SKILL.md`, `templates/`, scripts).
