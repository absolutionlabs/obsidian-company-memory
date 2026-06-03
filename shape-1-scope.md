# Shape 1 — Detailed Scope

*Draft v0.1. Sibling to [install-steps-and-skill-feasibility.md](install-steps-and-skill-feasibility.md). Purpose: scope the smallest credible v1 of the exportable setup skill, accounting for Cowork as the primary surface for non-technical users.*

> **Addendum 2026-06-02 (Session 2).** Sections §5 (pseudo-code procedure) and §13 (build effort estimate) were written pre-reframe — they still reference Templater, a shipped plugin bundle, git init in the vault, and first-project scaffolding. All four were cut by the SHAPE reframe captured in [brief.md](brief.md) Key Decisions #6, #7, #8, #9. **The canonical procedure is now [SKILL.md](SKILL.md) at the project root.** Treat §5 / §13 as historical context only; [brief.md](brief.md) is the source of truth for scope and [SKILL.md](SKILL.md) for the runtime procedure. The companion sections §1, §6, §7, §8, §10, §11, §12, §14 remain useful and were not invalidated by the reframe.

---

## 1. Why Cowork being the primary surface matters

Non-technical users will mostly arrive via **Cowork** (browser-based, no terminal, one-click plugin install from Settings). That's a structural constraint, not a polish detail:

| Capability | Cowork | Claude Code |
|---|---|---|
| Read/write to a folder the user grants access to | Yes | Yes |
| Run Bash inside its own sandbox | Yes | Yes (on the user's machine) |
| `curl` a file from the internet | Yes (to sandbox, then writes to mounted path) | Yes (directly to user's disk) |
| Install Obsidian on the user's local machine | **No** | Yes (`brew` / `winget` / `snap`) |
| Install Claude Code on the user's machine | **No** (and unnecessary — they're using Cowork) | Self-installs |
| Set up local launchd / Task Scheduler / cron | **No** | Yes |
| Install community plugins by writing files to the vault | Yes (via the mounted folder) | Yes |
| Write `.obsidian/*.json` configs to the vault | Yes | Yes |

The two "No" rows are the binding constraint. **Anything Shape 1 needs to do on the user's local machine that isn't "write a file inside the vault folder" is out of scope for Cowork users.** That rules out: installing Obsidian, installing any agent CLI, setting up scheduled tasks via OS schedulers.

What it does **not** rule out: scaffolding the vault, dropping community plugins into the mounted folder, writing starter files, installing future Claude Code skills (only relevant for Code users), and orchestrating the first test session. Those are 80% of the value.

The implication: **Shape 1 is a "configure + scaffold + plugin install" skill, with explicit upstream instructions (with screenshots) for the two manual steps the user does themselves: install Obsidian, and choose a sync method.** That's actually a cleaner product than trying to automate the install — fewer moving parts, fewer support tickets.

---

## 2. Target user and target outcome

**Target user.** A non-technical owner-operator of a small business who has used ChatGPT or Cowork before but has never opened a terminal. They have a Mac or Windows laptop, a Dropbox / iCloud / OneDrive account, and an Anthropic Cowork subscription.

**Target outcome (at end of Shape 1).** They have:

1. Obsidian installed locally (they did this manually, guided by the skill's preamble).
2. A vault folder inside their cloud-synced location, with the full three-layer structure scaffolded.
3. Dataview and Templater installed and enabled.
4. `SCHEMA.md`, `index.md`, `log.md`, `CONTEXT.md`, and the starter Operating Principles page in place.
5. Their first project folder with a `CLAUDE.md` stub.
6. One test entity page that they watched the skill create end-to-end, including the `index.md` update and the `log.md` entry.

**Total elapsed time from start to outcome:** ~25 minutes. Most of which is the user installing Obsidian, granting Cowork access to their cloud-sync folder, and clicking through Restricted Mode + plugin trust prompts.

**Non-goals for Shape 1** (explicitly out of scope):

- Installing Obsidian via package managers (Shape 2 territory)
- Installing Claude Code / Codex / opencode CLIs (Shape 2 territory; not needed if user stays on Cowork)
- Setting up scheduled maintenance jobs locally (Shape 3 territory)
- Provisioning a VPS for remote scheduling (Shape 3 territory)
- Multi-client `clients/<slug>/` folder layout (we ship single-company shape only; multi-tenant comes later)
- Custom schemas — user gets the canonical SCHEMA.md and can edit afterwards
- Migration from an existing Obsidian vault (separate skill, not Shape 1)

---

## 3. The user's seven-step journey

This is what the user actually does, narrated as they'd experience it. The skill's job is to make each step take seconds, with clear "do this now" prompts.

**Step 1 (user, 3 min).** Download Obsidian from [obsidian.md/download](https://obsidian.md/download). Install it. Skip the "Create your first vault" prompt — close the app for now. *(The skill's preamble tells them all of this with a screenshot.)*

**Step 2 (user, 1 min).** Decide where the vault lives. Skill recommends a cloud-synced folder (Dropbox / iCloud / OneDrive) so the vault is backed up and reachable from any device. User creates an empty folder there with the company name, e.g. `Dropbox/CompanyMemory/`.

**Step 3 (user, 1 min).** Open Cowork. Mount that folder via the directory connector. Grant access.

**Step 4 (user → skill, 5 min).** User invokes the skill: "Set up my Obsidian company memory." The skill runs:
   - Confirms the mounted directory.
   - Asks for company name and one-sentence description.
   - Asks the user to confirm three or four sensible defaults (single-company layout, English language, UK / US date format, theme preference).
   - Builds the full vault folder structure inside the mounted directory.
   - Downloads Dataview + Templater release files (in its sandbox) and writes them into `<vault>/.obsidian/plugins/`.
   - Writes the `.obsidian/*.json` config files with sensible defaults.
   - Writes `SCHEMA.md`, `index.md`, `log.md`, `CONTEXT.md`, `concepts/claude-operating-principles.md`.
   - Reports back: "Done. Now open Obsidian and do these three clicks."

**Step 5 (user, 2 min).** User opens Obsidian. Clicks **Open folder as vault**, picks the prepared folder. Obsidian loads it. Skill's report told them which three clicks come next:
   - Settings → Community plugins → Turn on community plugins.
   - Trust Dataview, trust Templater.
   - Restart Obsidian. *(Screenshot for each.)*

**Step 6 (user → skill, 5 min).** Back in Cowork. User says "Run the test." Skill:
   - Creates `entities/test-entity.md` with proper frontmatter and a `[[wikilink]]` to one of the seed pages.
   - Updates `index.md`.
   - Appends `log.md`.
   - Shows the user where to look in Obsidian to verify each thing landed.
   - User opens Obsidian, confirms it sees the new page, sees it in the index, sees the log entry.

**Step 7 (skill, 1 min).** Skill scaffolds the user's first real project folder with a `CLAUDE.md` stub pointing at the vault. Tells the user "Next time you start a session, paste this prompt to get going" with a copy-paste-ready opener.

Done. The user now has a working company memory and has personally seen the round-trip work end-to-end.

---

## 4. What the skill ships (file layout)

The skill bundle is one folder, exportable as a Cowork plugin and as a Code user-global skill from the same source.

```
obsidian-company-memory/
├── SKILL.md                         ← Cowork plugin entry / Code skill entry
├── README.md                        ← Public-facing skill description for the marketplace
├── plugin.json                      ← Cowork plugin manifest
├── manifest.yml                     ← Code skill manifest (mirror of plugin.json)
├── preamble/
│   ├── 01-install-obsidian.md       ← Pre-skill instructions: install Obsidian
│   ├── 02-pick-vault-location.md    ← Pre-skill instructions: cloud-synced folder
│   ├── 03-mount-in-cowork.md        ← Pre-skill instructions: grant access
│   └── screenshots/
│       └── (PNGs for each step)
├── templates/
│   ├── SCHEMA.md
│   ├── index.md
│   ├── log.md
│   ├── CONTEXT.md
│   ├── claude-operating-principles.md
│   ├── obsidian/
│   │   ├── app.json
│   │   ├── appearance.json
│   │   ├── core-plugins.json
│   │   ├── community-plugins.json
│   │   └── hotkeys.json
│   ├── project-stub/
│   │   ├── CLAUDE.md.template
│   │   └── AGENTS.md.template       ← For Codex / opencode users
│   └── _meta/
│       └── expectations.yml
├── plugins/                         ← Pinned community plugin releases
│   ├── dataview/
│   │   ├── main.js
│   │   ├── manifest.json
│   │   ├── styles.css
│   │   └── PINNED_VERSION
│   └── templater-obsidian/
│       ├── main.js
│       ├── manifest.json
│       ├── styles.css
│       └── PINNED_VERSION
├── scripts/
│   ├── scaffold_vault.py            ← Idempotent scaffold runner
│   ├── install_plugins.py           ← Drops the plugin files in the vault
│   ├── test_roundtrip.py            ← Runs the end-to-end smoke test
│   └── refresh_plugins.py           ← Manual command to update pinned plugins
└── docs/
    ├── customisation.md             ← How to make your own variant
    ├── upgrading.md                 ← How to refresh plugins / templates
    └── troubleshooting.md           ← Common failures + recovery
```

The two manifest files (`plugin.json` for Cowork, `manifest.yml` for Code) point at the same `SKILL.md`. The skill is identical on both surfaces; only the install path differs.

**Plugin files shipped pinned.** We ship Dataview and Templater inside the skill bundle rather than downloading them at runtime. This means:
- Zero network calls during the install. Faster, more reliable, no rate-limit risk.
- One pinned version per skill version; we update via a quarterly refresh.
- The skill works behind a corporate firewall.

Trade-off: skill bundle is ~1 MB rather than ~100 KB. Worth it.

---

## 5. The skill's actual procedure (pseudo-code)

Inside `SKILL.md`, the procedure reads roughly:

```
1. Pre-flight checks
   - Confirm directory is mounted and writable
   - Detect existing .obsidian/ — if present, ask user whether to upgrade or refuse
   - Read templates/ from skill bundle
   - Confirm skill bundle version against SKILL_VERSION constant

2. Collect inputs (one AskUserQuestion call with 3–4 questions)
   - Company name
   - One-sentence description
   - Date format (UK / US / ISO)
   - Single-company vs multi-client layout
     (Shape 1 ships single only; multi-client greyed out with "coming in v2")

3. Scaffold the vault folder structure
   - Create directories: entities/, concepts/, comparisons/, queries/, raw/{articles,transcripts,assets}/, _meta/
   - Idempotent: skip directories that already exist

4. Install community plugins
   - Create .obsidian/plugins/dataview/
   - Write main.js, manifest.json, styles.css from skill bundle's plugins/dataview/
   - Same for templater-obsidian
   - Write .obsidian/community-plugins.json with both IDs enabled

5. Write Obsidian config files
   - .obsidian/app.json, appearance.json, core-plugins.json, hotkeys.json from templates
   - DO NOT overwrite if already present (idempotent)

6. Write starter wiki files
   - SCHEMA.md with company name substituted into the header
   - index.md (empty table of contents, with frontmatter)
   - log.md (empty audit trail, with frontmatter)
   - CONTEXT.md (vault pointer with company name)
   - concepts/claude-operating-principles.md (canonical operating principles)
   - _meta/expectations.yml (lint thresholds)

7. Initialise git inside the vault (optional)
   - Code surface only: run `git init` + initial commit
   - Cowork surface: skip (sandbox can't write a .git/ on the user's disk reliably)

8. Report what was done
   - List every file created, with full paths
   - Show the three Obsidian clicks needed next, with screenshot links
   - Pause for the user to confirm they completed the clicks

9. Run the round-trip test
   - Create entities/test-welcome.md with proper frontmatter
   - Wikilink to itself (placeholder until user creates real content)
   - Update index.md with the new entry
   - Append log.md with the test entry
   - Tell user to verify in Obsidian

10. Scaffold the first project folder
    - Ask for project name
    - Create <vault-parent>/projects/<project-slug>/ with CLAUDE.md stub
    - Stub points at the vault path the user gave us

11. Hand off
    - Output the copy-paste opener for the next session
    - Output one paragraph: "Here's what to do next time"
```

Every step is idempotent — re-running the skill on an existing setup updates only what's drifted, never overwrites user edits.

---

## 6. Execution differences between Cowork and Code

| Step | Cowork | Code |
|---|---|---|
| Pre-flight | Reads from mounted dir | Reads from cwd |
| Scaffold directories | Writes via mounted dir | Writes via mounted dir or cwd |
| Install plugins | Reads from skill's `plugins/` (shipped in plugin bundle), writes to mounted vault | Same, but from `~/.claude/skills/.../plugins/` |
| Git init | Skipped | Runs locally |
| Round-trip test | Same | Same |
| Project stub | Writes to mounted projects/ | Writes to cwd's parent |

The only material difference is git init. Everything else is uniform.

---

## 7. Customisation surface (the "create your own version" answer)

A user (or another consultancy) wanting their own variant of this skill should be able to:

1. **Edit the templates.** All starter content lives in `templates/`. Want different `SCHEMA.md` rules? Different starter Operating Principles? Different `.obsidian/` defaults? Edit the files, repackage the skill, share it.

2. **Pin different community plugins.** The `plugins/` folder is the canonical place. Drop in your preferred plugins, update `community-plugins.json` template, ship.

3. **Add a custom preamble.** Want to add a "we charge a setup fee" page, or a "here's how we use this with our other consulting tools" page? Drop a markdown file in `preamble/` and reference it from `SKILL.md`.

4. **Customise the skill's questions.** The `SKILL.md` itself is editable. A consultancy could add "which of our standard templates do you want?" as a fifth question.

We ship `docs/customisation.md` walking through each of these with examples. The skill is a small bundle, not a black-box installer. That's the right shape for "exportable."

---

## 8. Build effort estimate

Honest AI-time-budget (per OP #16, calibrated for multi-block runs):

| Block | Stated AI-time | Realistic actual |
|---|---|---|
| A. Templates + screenshots authoring | 3h | ~25 min |
| B. SKILL.md procedure logic | 4h | ~30 min |
| C. Cowork plugin manifest + Code manifest mirror | 1h | ~10 min |
| D. Plugin bundle prep (download, pin, store) | 2h | ~20 min |
| E. Scripts (scaffold / install / round-trip test) | 4h | ~30 min |
| F. Docs (README, customisation, upgrading, troubleshooting) | 3h | ~25 min |
| G. End-to-end test on a clean machine | 4h | ~40 min |
| H. Packaging + submission to Cowork plugin marketplace | 2h | ~20 min |
| **Total** | **23h stated** | **~3 hours actual** |

Realistic calendar time: **one focused session** if uninterrupted. Conservatively two sessions if we discover plugin packaging edge cases.

---

## 9. Test plan

Before shipping, we run the skill against three personas:

1. **Cold Mac user.** Fresh MacBook, no Obsidian, no Cowork-history with this skill. From "I want to set this up" to "I just had my test session work" — measure elapsed time, capture friction.
2. **Cold Windows user.** Same exercise on Windows. Different cloud-sync folder defaults (OneDrive most likely). Verify path handling works without per-OS code in the skill.
3. **Existing-vault user.** Someone with an Obsidian vault already, wanting to layer this system on top without losing their existing notes. Skill should detect existing `.obsidian/` and ask permission before touching anything.

Each test produces a "first 30 minutes" capture (what the user did, where they paused, where they got stuck) that goes into a `docs/field-test-log.md` and informs Shape 2.

---

## 10. Decisions (locked 2026-06-02)

| # | Question | Decision | Effect on scope |
|---|---|---|---|
| 1 | Distribution | **Shareable via direct URL.** Free skill, not marketplace-listed. | README points at install URL; no marketplace submission step. |
| 2 | Branding | **Light-touch Absolution Labs.** Built-by attribution in README + a single line in `CONTEXT.md`, no heavier brand surfacing. | Skill name stays generic ("Obsidian Company Memory"); "by Absolution Labs" appears as a quiet footer. |
| 3 | Pricing | **Free.** No paid-support upsell embedded. | Preamble has no "if you want us to do this for you" page. |
| 4 | Multi-client | **Single-client only, permanently.** No v2 multi-client expansion. | Skill ships single-vault shape and stays there; cuts ~40% from any future build effort. |
| 5 | Scheduled lint | **Manual lint only — no scheduler.** User invokes lint as a procedure when they want it. | Cuts the per-OS scheduler block entirely. See §11 below. |

---

## 11. Lint as a manual procedure (decision #5)

Lint runs only when the user asks for it. No scheduler, no autostart, no Python-availability gating, no per-OS code paths. The lint logic still ships — it just runs in the agent's session context rather than as a background job.

**What ships:**

- The lint procedure as part of the skill bundle. User invokes it by saying "run lint on the vault" or by triggering it via a slash command like `/lint` (Code) / via the skill's runtime UI (Cowork).
- The procedure walks the vault, applies the checks defined in `SCHEMA.md` (orphan pages, broken `[[wikilinks]]`, missing frontmatter, stale pages over 30 / 90 days, CONTEXT freshness), and writes `lint-reports/YYYY-MM-DD.md` into the vault.
- The user reads the report in Obsidian and decides what to act on.

**Why this is enough.** The lint catches drift, not minute-by-minute regression. Weekly or monthly runs catch 95% of what daily runs would catch. The user's natural cadence is "I'm about to start serious work — run lint first" which lands right on the moments lint is actually useful, instead of firing into an empty inbox at 08:00 every day.

**Trade vs scheduled cron:** loses the "drift detection happens without me thinking" property. Gains: no per-OS scheduler code, no Python dependency, no "laptop asleep" failure mode, no scheduler-misfire support tickets, identical behaviour across Cowork and Code surfaces. Net win for v1.

**Documented in the preamble:** the README and the post-install "what to do next" output both surface "ask Claude to run a lint" as a recommended weekly habit. If users want it automated later, that's a Shape 2 add-on, not blocking v1.

---

## 12. The "select Cowork or Code at install" question

Short answer: **yes, sort of — but not the way it sounds.** A single skill that auto-detects and installs into the user's preferred surface isn't realistic, because Cowork plugins and Code skills are installed by different mechanisms in different places and the cloud sandbox can't reach `~/.claude/skills/` on the user's machine. But a single bundle with two install paths IS realistic and is probably what you actually want.

**Three ways to think about this:**

**Option A — Single bundle, two clearly-labelled install paths in the README.** The skill ships from one URL (a GitHub repo or single download). The README opens with:

> "Which agent do you mainly use?  
> • **Cowork** → click this install URL in Cowork's plugin settings.  
> • **Claude Code** → run this one-line install in your terminal.  
> • **Both** → do both. They share the same vault; installing one doesn't preclude the other."

The bundle contains the Cowork manifest (`plugin.json`) and the Code manifest (`SKILL.md` in the right shape) side by side. Same templates, same procedure logic, same scripts. The user picks one of two doors and the door it opens is the same room. **This is the cleanest answer.** It's honest about what the two surfaces are, and most non-technical users will pick Cowork without thinking about it.

**Option B — A "bootstrap" Cowork plugin that asks the user "Cowork or Code or both?" and installs the right pieces.** This is what the question literally asks for. The technical wall: a Cowork plugin running in the cloud cannot write to `~/.claude/skills/` on the user's local machine. It could write the Code skill into the user's mounted vault folder and tell the user "now copy this folder to `~/.claude/skills/`," but that's a manual step the user has to do anyway, and it's clunkier than just pointing them at the Code install command in the first place.

We could make Option B work by having the bootstrap plugin write a small "Code install" shell script into the vault that the user then runs in their terminal. That works mechanically but adds a layer of indirection for no real gain over Option A.

**Option C — A Code skill that auto-installs into Cowork too.** Symmetric problem in reverse. A Code skill can write files anywhere on the local machine, but it can't push a plugin into the user's Cowork environment (Cowork plugins are URL-installed via Cowork's own settings UI). Same dead-end.

**Recommendation: Option A.** Single repo, single download URL, two install commands in the README, user picks one (or both). It's honest, simple to author, simple to support, and exactly mirrors the way the rest of the agent ecosystem ships dual-surface tools today.

The skill's behaviour after install is identical on both surfaces (per §6 of this doc), so once installed there's literally no functional difference. The choice is just "which door did you walk in through."

If we want to make Option A feel more like a single experience, we can: package the README's install-method picker as an HTML landing page at `obsidian-company-memory.absolab.com/install`, with a "which agent do you use?" toggle that reveals the right install command. Five minutes of frontend work. The skill itself is unchanged.

---

## 13. Updated build effort estimate

With the dual-surface install path locked and the lint reduced to a manual procedure:

| Block | Stated AI-time | Realistic actual |
|---|---|---|
| A. Templates + screenshots authoring | 3h | ~25 min |
| B. SKILL.md procedure logic | 4h | ~30 min |
| C. Dual manifest (Cowork plugin.json + Code SKILL.md frontmatter) | 1h | ~10 min |
| D. Plugin bundle prep (Dataview + Templater pinned) | 2h | ~20 min |
| E. Scripts (scaffold / install / round-trip test) | 4h | ~30 min |
| F. Lint procedure (as part of skill, no scheduler) | 1.5h | ~15 min |
| G. Docs (README with dual-install picker, customisation, upgrading, troubleshooting) | 3h | ~25 min |
| H. End-to-end test on a clean machine | 4h | ~40 min |
| I. Optional install landing page (HTML toggle) | 1h | ~10 min |
| **Total** | **23.5h stated** | **~3 hours actual** |

One focused session. The single highest-risk block (per-OS scheduler installers) is gone, so the "two sessions if snags" caveat from the previous estimate also drops out. Realistic confidence interval narrows.

---

## 14. Further simplification candidates

A fresh pass at what's still in the scope, asking "would the user notice if this came out?" The first three are strong cuts; the rest are smaller adjustments.

### Strong cuts (recommend accepting)

**14.1 — Drop the shipped plugin bundle. Have the user install plugins from inside Obsidian.**

*Currently:* skill ships pinned copies of Dataview and Templater inside `plugins/`, writes them into the vault during setup.

*Alternative:* skill writes `community-plugins.json` listing the IDs we want enabled, then tells the user "open Settings → Community plugins → Browse, search Dataview, click Install, click Trust. Repeat for Templater." Two extra clicks per plugin. The user is already clicking "Turn on community plugins" once and trusting each plugin individually — the extra step is just one search per plugin, not a new category of work.

*Cuts:* block D entirely (20 min build), ongoing quarterly version-bump maintenance, skill bundle size, "what if the pinned version is incompatible with the user's Obsidian version?" failure mode, all "we shipped a third-party binary inside our distributable" licensing questions.

*Loses:* one click of polish. Users don't get a fully-configured Obsidian at the end of the skill — they get a 90%-configured one and finish the last 10% themselves in 60 seconds.

*Verdict:* **accept.** Net win.

**14.2 — Drop Templater entirely. Ship plain markdown templates instead.**

*Currently:* Templater is one of the two plugins we install. It's used so users can hit a hotkey and instantiate a new entity / concept page with the right frontmatter.

*Alternative:* ship a `_meta/templates/` folder containing `entity.md`, `concept.md`, `query.md` with the frontmatter already filled in. Users (and the AI) copy-paste these when creating new pages. No plugin needed.

*Cuts:* one plugin's worth of install flow (one less "Trust this plugin" click), one less plugin version to track, one less variable in "is the vault still set up correctly?"

*Loses:* Templater's hotkey-driven workflow is genuinely convenient for power users who'll create dozens of pages a week. Non-technical users mostly won't notice — they'll let Claude create pages for them and never trigger a template manually.

*Verdict:* **accept.** Dataview is load-bearing (it powers the dynamic queries that make the wiki feel like a system). Templater is convenience. Cut.

**14.3 — Ship a smaller starter Operating Principles page.**

*Currently:* the doc plan suggests shipping our full 24-principle canonical page.

*Alternative:* ship a 5-principle starter ("update records the same session, not the next one," "preserve docs by appending addendums," "trust the user over the wiki," "every page has frontmatter and at least one wikilink," "every session ends with an ingest or a logged reason it didn't"). Add a footer pointing at our full 24-principle page as inspiration for users who want to grow theirs.

*Cuts:* the noise of 24 cross-cutting rules a new user hasn't earned yet through real experience. Operating principles are most useful when they were written in response to specific incidents; a starter user has had zero incidents.

*Loses:* nothing meaningful. The principles are still discoverable from our public canonical page if they want them.

*Verdict:* **accept.** Strong cut. Reduces "what am I looking at?" cognitive load.

### Smaller adjustments (judgment calls)

**14.4 — Cut the first-project scaffolding (Step 10 in §5).**

The skill currently bootstraps the user's first project folder with a `CLAUDE.md` stub. We could leave that to the next session, where the existing `new-project-setup` skill (which we'd ship anyway as part of the bundle) handles it.

*Loses:* the "and your first project is ready to go" handoff moment. Adds one extra step to the user's next session.

*Verdict:* **trim.** The skill's job is "set up the vault." The next session's job is "start using it." Keeping those separate is cleaner.

**14.5 — Cut git init from the Code path.**

*Currently:* Code path runs `git init` inside the vault as a backup mechanism.

*Alternative:* skip. Cloud sync (Dropbox / iCloud / OneDrive) already provides version history. Git is a developer-grade feature most non-technical users won't ever use directly.

*Verdict:* **trim.** Make it an optional question ("do you want git version history? most users say no"). Default no.

**14.6 — Compress the intake to 2 questions.**

*Currently:* 3-4 questions (company name, description, date format, single-vs-multi).

*Alternative:* company name + sync location only. Date format auto-detected from system locale. Single-client is the only shape we ship (per decision #4), so don't ask.

*Verdict:* **trim.** Less to read, faster to start.

**14.7 — Cut the optional install landing page (block I).**

Already marked optional in §13. Could be cut for v1 entirely. README's two-install-command table is honest and clear; landing-page polish is for if/when the skill gets traction.

*Verdict:* **trim from v1.** Build only if user feedback shows the README confuses people.

### What we keep, with reasoning

- **Round-trip test (Step 9).** Load-bearing. Non-technical users need to see it work once before they trust it. ~30 sec of skill time, high confidence return.
- **Cloud-sync prompt.** Worth the one question. Portability and backup are real benefits.
- **`_meta/expectations.yml`.** Stays. It's where lint thresholds live; we don't want them hardcoded in `SCHEMA.md` because that breaks the "edit the rulebook, not the code" model.
- **Dual manifest (Cowork + Code).** Stays. 10 minutes of build for the "works in either surface" pitch is a fair price.

### Cumulative effect of all "accept / trim" verdicts above

| Block | Was | Now |
|---|---|---|
| A. Templates | ~25 min | ~20 min (smaller starter OP page) |
| B. SKILL.md logic | ~30 min | ~25 min (fewer steps, fewer questions) |
| C. Dual manifest | ~10 min | ~10 min |
| D. Plugin bundle | ~20 min | **cut** |
| E. Scripts | ~30 min | ~25 min (no plugin install, no project scaffold) |
| F. Lint procedure | ~15 min | ~15 min |
| G. Docs | ~25 min | ~20 min |
| H. End-to-end test | ~40 min | ~35 min |
| I. Landing page | ~10 min | **cut from v1** |
| **Realistic total** | **~3h** | **~2.5h** |

Tighter skill, less surface area, ~30 min faster build. Net win.

---

## 15. The whole project — chunks view

The project (not just the build) breaks into seven chunks. Each is shippable on its own; they sequence cleanly.

### Chunk 1 — Scope + decisions (now, mostly complete)

What it is: this scope doc, the install-feasibility doc, the user-guide draft, and Rob's locked decisions on the five open questions plus the simplification verdicts.

Status: 80% done. Remaining: lock the §14 verdicts (one yes/no from you), then chunk closes.

Output: this folder.

### Chunk 2 — Templates authoring (the content the skill ships)

What it is: the actual files the skill will drop into a user's vault. Distinct from the skill's procedure logic — this is the *what*, not the *how*.

Pieces:
- `SCHEMA.md` (single-company variant of our canonical)
- `index.md` skeleton
- `log.md` skeleton
- `CONTEXT.md` (single-company variant)
- `concepts/claude-operating-principles.md` (5-principle starter per §14.3)
- `_meta/expectations.yml` (lint thresholds)
- `_meta/templates/entity.md`, `concept.md`, `query.md` (replaces Templater per §14.2)
- `.obsidian/app.json`, `appearance.json`, `core-plugins.json`, `community-plugins.json`, `hotkeys.json` (sensible defaults)
- `CLAUDE.md` stub template (for users who want to scaffold a first project; lives in the bundle but isn't dropped automatically)
- `AGENTS.md` stub template (Codex / opencode equivalent)

Output: a `templates/` folder ready to be wrapped.

Build effort: ~20 min realistic.

### Chunk 3 — Skill procedure (the *how*)

What it is: the `SKILL.md` that defines what the agent does when invoked.

Pieces:
- Pre-flight checks (writable mounted dir, no existing `.obsidian/` unless upgrade flag)
- 2-question intake (company name + sync location)
- Vault scaffold (folders + files from chunk 2)
- `.obsidian/` config write (Obsidian closed, idempotent)
- "Three clicks you do now" handoff with screenshots
- Round-trip test
- Final report + recommended next prompt

Build effort: ~25 min realistic.

### Chunk 4 — Manifests + packaging (the distribution wrappers)

What it is: the two thin wrappers that make the skill installable.

Pieces:
- `plugin.json` (Cowork plugin manifest)
- Code skill manifest (frontmatter in `SKILL.md` per Code's convention)
- Bundle layout: single repo with both manifests pointing at the same logic
- A `README.md` with the dual-install picker (Cowork URL + Code one-liner)

Build effort: ~10 min realistic.

### Chunk 5 — The lint procedure

What it is: a small sub-procedure inside the bundle that runs `SCHEMA.md`'s lint checks on demand and writes a report into the vault.

Pieces:
- The lint logic itself (walk vault, check orphans / broken links / missing frontmatter / stale pages / CONTEXT freshness)
- Output to `lint-reports/YYYY-MM-DD.md`
- "How to invoke" docs in the README

Build effort: ~15 min realistic.

### Chunk 6 — Docs

What it is: the user-facing documentation that ships with the skill.

Pieces:
- `README.md` (the entry point — what this is, who it's for, the two install commands)
- `docs/customisation.md` (how to fork and make your own variant)
- `docs/troubleshooting.md` (common failures + recovery)
- `docs/upgrading.md` (how to refresh templates when we ship updates)
- Adapt the existing `current-setup-user-guide.md` from this folder into the bundle's long-form guide

Build effort: ~20 min realistic.

### Chunk 7 — Test, ship, announce

What it is: the cross-the-finish-line work.

Pieces:
- Three-persona test (cold Mac, cold Windows, existing-vault user) per §9
- Fix anything the tests surface
- Publish to a Github URL (skill source) + the direct-install URL for Cowork
- Light-touch announcement (LinkedIn / X / wherever) with a single screenshot and the install link
- Ship-day Slack to anyone who's expressed interest

Build effort: ~35 min realistic (mostly the testing).

### Chunk 8 — Post-ship maintenance (open-ended)

What it is: the ongoing care once it's live.

Pieces:
- Watch for "Obsidian plugin API changed and Dataview's frontmatter format moved" type drift (rare, but real)
- Field-test feedback collection (one shared doc, capture friction users report)
- Quarterly template refresh as our own canonical SCHEMA evolves
- Decide whether to graduate to Shape 2 (install automation) based on adoption signal

Effort: ongoing, low. Maybe one hour per quarter unless something major shifts.

### Chunks at a glance

| # | Chunk | Effort | Dependency |
|---|---|---|---|
| 1 | Scope + decisions | now (90% done) | — |
| 2 | Templates authoring | ~20 min | chunk 1 |
| 3 | Skill procedure | ~25 min | chunk 2 |
| 4 | Manifests + packaging | ~10 min | chunk 3 |
| 5 | Lint procedure | ~15 min | chunk 2 |
| 6 | Docs | ~20 min | chunks 2 + 3 + 4 |
| 7 | Test, ship, announce | ~35 min | chunks 2-6 |
| 8 | Maintenance | ongoing | post-ship |
| | **v1 total (chunks 2-7)** | **~2 hours** | |

Chunks 2 and 3 can run in parallel-ish (templates can be drafted while procedure is being authored, they cross-reference but don't strictly block). Chunks 4 and 5 are small wrappers around chunks 2-3. Chunk 6 needs all of them done. Chunk 7 is the gate.

The honest critical path is **Chunk 2 → Chunk 3 → Chunk 6 → Chunk 7**, which is ~100 minutes of focused work. Add chunks 4 and 5 in parallel and the total is still under 2 hours.

---

## 16. The Phase 1 / Phase 2 split

Rob's call (2026-06-02): split the deliverable into two cleanly-separated phases so the install moment is sharp and the ongoing relationship with the vault is honest about being instructions, not automation.

### Phase 1 — "Get Obsidian operational" (the skill)

The skill's entire job is to take a user from "I just installed Obsidian" to "I just had a session land something in the vault and watched it work." That's the cut.

What Phase 1 contains:
- Pre-flight + 2-question intake (company name + sync location)
- Vault scaffold (folders + starter files from chunk 2)
- `.obsidian/` config write
- "Three clicks in Obsidian" handoff with screenshots
- Round-trip test (skill creates one test entity, updates index, appends log, user verifies in Obsidian)
- Hand-off message that ends with: "you're operational — here's your Phase 2 guide for what to do from here"

Phase 1's success criterion is binary: round-trip test passes, user has confidence the system works. Phase 1 ends there.

### Phase 2 — "Living with the vault" (instructions, not a skill)

A single markdown doc that lives in the vault root (drop point: `HOW-TO-USE-THIS.md` or similar). It's the user's reference for everything that happens after Phase 1 ends. Not automation — instructions. The user reads it once after Phase 1, then revisits whenever they need a reminder.

What Phase 2 contains:

| Topic | Content shape |
|---|---|
| The weekly lint habit | "At the start of serious work each week, ask Claude to run a lint. Here's the prompt: '...'. Read the report in `lint-reports/`. Spend 5 minutes acting on anything flagged." |
| Manual ingest mid-session | "When something material happens (a decision, a price change, a brand rule), ask Claude to ingest it now rather than waiting for close. The prompt is: '...'." |
| Close-of-session protocol | "Every session ends with `/close-full`. Here's what it does and why skipping it accumulates as drift." |
| When `_summary.md` drifts | "If the rolling summary stops reflecting reality, ask Claude to rebuild it from scratch by reading `index.md` and the recently-updated pages." |
| Adding new pages by hand | "If you create a page directly in Obsidian (rather than via Claude), drop the frontmatter from `_meta/templates/entity.md` and add a one-line entry to `index.md`. Or just ask Claude to do it next session." |
| Updating `CONTEXT.md` | "When a major fact about the company changes (new product line, new ICP, new pricing tier), update `CONTEXT.md` and ask Claude to scan for stale pages that reference the old fact." |
| Backup hygiene | "Your cloud sync is your backup. Quarterly, zip the vault and save it somewhere else as a belt-and-braces. The full procedure is below." |
| What to do when something breaks | Common failures + recovery: contradiction between pages, dropbox conflict files, AI writing to the wrong place, lost work, etc. |
| When to graduate | "If you outgrow manual lint and want it automated, here's the pointer to Shape 2 (when it ships)." |

Phase 2 is a living document. Every time we learn something the user should know, it grows by a section. Doesn't require shipping a new skill version.

### Why this split is the right shape

1. **Sharp install moment.** Phase 1 has a binary success criterion (round-trip test passed). The skill doesn't have to do anything else.
2. **Honest about what Phase 2 is.** It's instructions the user follows over time, not procedures the AI runs once. Calling it a "skill" would have been a category error.
3. **Phase 2 evolves without skill versioning.** Lessons from field tests, common questions, new tips — all just edits to the markdown doc. No release process.
4. **Cleaner mental model for the user.** "Install" is one event. "Living with the vault" is everything after. The doc names match what users actually do.
5. **Cuts skill complexity further.** Anything that was "and during ongoing use, the skill also..." moves to Phase 2. Skill stays small.

### What this changes in the chunks view

Chunks 2-5 (templates, skill procedure, manifests, lint) all map to Phase 1.

Chunk 6 (docs) splits:
- README + customisation + troubleshooting + upgrading → Phase 1 install docs (live in the skill bundle)
- The Phase 2 living guide → drops into the user's vault as `HOW-TO-USE-THIS.md` during Phase 1's scaffold step

Effectively, **Phase 2 is delivered by Phase 1** — the skill drops the guide into the vault during scaffold. The user then has it forever, alongside their notes.

### Build effort breakdown by phase

| Phase | Chunks | Effort |
|---|---|---|
| **Phase 1 (the skill + immediate install docs)** | 2, 3, 4, 5, 6a | ~80 min |
| **Phase 2 (the living guide, shipped by Phase 1)** | 6b | ~20 min |
| **Test + ship** | 7 | ~35 min |
| **Total v1** | 2-7 | **~2.25 hours** |

Slight bump from §15's 2-hour estimate because the Phase 2 doc is a substantive deliverable in its own right (~600-1000 words covering the weekly habits, the close protocol, the troubleshooting playbook). Worth it: the alternative is leaving users to figure out the ongoing use themselves, which is the failure mode most "AI memory" products die from.

### What the user sees at the end of Phase 1

The skill's final message:

> Done. Your Obsidian company memory is operational.
>
> One file landed in your vault as part of setup: `HOW-TO-USE-THIS.md`. Open it in Obsidian when you have 10 minutes. It's the Phase 2 guide — how to use the vault on an ongoing basis, the weekly lint habit, the close-session protocol, common failures and recovery. Read it once, revisit whenever you need a reminder.
>
> For your next session, paste this prompt to get going:
> `[copy-paste opener]`
>
> Good luck.

Crisp. The skill ends. Phase 2 begins.

---

## 17. SHAPE-close reframe addendum (2026-06-02)

Per OP #4 (preserve documentation — append addendums, never rewrite), this section captures the deltas from the SHAPE dialogue that closed 2026-06-02. The earlier sections of this scope doc remain as the historical record of the pre-reframe scope; this addendum is the authoritative current state where it conflicts.

### What changed in SHAPE

**Project framing (largest single change).** Reframed from "free public skill seeking adoption" to **"sales/trust tool — every install is in front of a prospect, per-install quality is absolute, volume is not a metric."** Adoption / distribution / completion goals drop out of the picture. Trust-layer engineering (failure detection, professional polish, compliance gating) becomes load-bearing.

**Decision deltas vs §10 + §14:**

| Was | Now | Reason |
|---|---|---|
| Decision 2: light-touch Absolution Labs branding | **Full Absolution Labs LTD branding throughout.** All disclaimers / license / formal text use full legal name; informal copy may use "Absolution Labs". | Trust artifact must visibly bear the brand it anchors. |
| Telemetry: not in scope | **Default-on telemetry, opt-out available.** Cloudflare Worker endpoint (EU region), anonymous UUID, install + success ping. Privacy policy live at absolutionlabs.com. | Sales-tool framing demands we detect failure before the prospect tells anyone. |
| Existing-vault detection: "ask permission to upgrade" | **Refuse to scaffold if target dir has any files or `.obsidian/`.** Clear error, point user at empty folder. | Prevents data damage — the worst-case pre-mortem failure. Also closes prompt-injection blast radius. |
| Compliance disclaimer: buried in README | **First-screen compliance gate** — 3 mandatory checkboxes (data rights, sync-provider DPA, AI-provider data flow) before scaffold begins. | Regulated-sector prospects must surface concerns BEFORE writing data. |
| Support: best-effort community | **Direct support email, 1-business-day response SLA from Absolution Labs LTD.** | Branded skill in sales-tool frame demands branded support. |

**Scope additions:**

- Cloudflare Worker telemetry endpoint (EU region, rate-limited, payload-validated)
- Privacy policy at absolutionlabs.com
- COMPATIBILITY.md stating tested versions
- Version-pinned install URLs (e.g. `/install/v1.0.0`)
- SHA256 checksums of skill bundle in README
- Signed release commits
- 3-minute demo video (trust-anchor distribution asset)
- Expanded test matrix: 7 personas (cold Mac, cold Windows, Dropbox-Business, OneDrive-Business, iCloud, MDM-managed Windows, existing-vault user)
- Direct-support email + escalation runbook

**Scope removals:**

- Adoption-volume goals
- General distribution campaign (LinkedIn launch, demo blog for general audience)
- Migration from existing vault (skill refuses; separate future skill)

### Appetite delta

| | Was | Now |
|---|---|---|
| Appetite | Small | **Big** |
| Stated AI-time | ~23h | ~50-55h |
| Realistic actual | ~3h (one session) | **~7-8h (3-4 sessions)** |

The skill *behaviour* doesn't grow significantly. The **trust-layer engineering** (gating, refusing, telemetry, compliance surfacing, professional polish, expanded test matrix) is most of the added effort.

### Build estimate updated

| Block | Pre-reframe | Post-reframe |
|---|---|---|
| A. Templates authoring | ~20 min | ~25 min (now includes 5-principle starter + compliance-gate copy) |
| B. SKILL.md procedure logic | ~25 min | ~40 min (refuse-gate + compliance-gate + telemetry-call paths) |
| C. Manifests + packaging | ~10 min | ~10 min |
| D. (was plugin bundle) | cut | cut |
| E. Scripts | ~25 min | ~30 min |
| F. Lint procedure | ~15 min | ~15 min |
| G. Docs (README + customisation + troubleshooting + upgrading + COMPATIBILITY) | ~20 min | ~30 min |
| H. End-to-end test on clean machines | ~35 min | ~90 min (7 personas vs 3) |
| I. (was HTML landing page) | cut | cut |
| **NEW J. Telemetry endpoint + privacy policy** | — | ~75 min |
| **NEW K. Demo video** | — | ~45 min |
| **NEW L. Signed-release + checksum pipeline** | — | ~20 min |
| **Realistic total** | **~2.5h** | **~7h** |

### Chunks view updated

The 8-chunk view in §15 stands, with these additions/changes:

- **Chunk 2 (Templates)** — adds the 5-principle starter OP page + first-screen compliance gate copy + `HOW-TO-USE-THIS.md` Phase 2 guide
- **NEW Chunk 5b — Telemetry endpoint + privacy policy.** Sibling to Chunk 5 (lint). Can run in parallel.
- **NEW Chunk 6.5 — Demo video.** Sibling to Chunk 6 (docs). Can run in parallel once Chunk 3 has a working SKILL.md to demo.
- **Chunk 7 (Test, ship, announce)** — test matrix expands from 3 to 7 personas. Ship gate is now stricter: every Threat Map row at OK, every Fatal Pattern verified, telemetry caught at least one synthetic failure correctly.

### Why this addendum is filed here

The brief at [brief.md](brief.md) carries the canonical current state of the project (status, scope, decisions, threat map, etc.). This scope doc is the working-history of how we arrived at the current state — and per OP #4 we preserve the journey, not just the destination. Future sessions reading both docs see the path explicitly.
