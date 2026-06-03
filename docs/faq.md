# FAQ

Question-shape help. If you have a failure or error message, [troubleshooting.md](troubleshooting.md) is the right surface. If you have a "can I" / "what if" / "why does it" question, this is the right surface.

If your question isn't here, email `info@absolutionlabs.com` — we'll answer you and add the question if it's likely to come up again.

---

## General

### What is this, in one sentence?

A skill that scaffolds an Obsidian-based company memory vault — a folder of plain markdown files structured so any AI session can read it, write to it, and stay coherent across sessions.

### Who is it for?

Founders and small-team operators who already use an AI assistant (Cowork, Claude Code, Codex, opencode) and want the AI's outputs to accumulate as durable company knowledge rather than disappearing at the end of each session.

### Is this an Obsidian plugin?

No. The skill scaffolds a vault structure that Obsidian opens; it doesn't add functionality to Obsidian itself. The plugin you'd install is the agent CLI's plugin (e.g. the Cowork plugin), which provides the skill that scaffolds the vault.

### Is this open source?

Yes, MIT-licensed. Source is on GitHub under `absolutionlabs/obsidian-company-memory`. Forks are encouraged; rename your variant per the LICENSE.

### Does this cost anything?

No. The skill is free, no upsell, no paid tier. No telemetry either — the bundle does not phone home at install time or afterwards (v1.2.0 removed the opt-out install ping that earlier versions shipped).

### Why is Absolution Labs giving this away?

It's a trust artefact for our consultancy. A polished, working, well-documented skill demonstrates how we build — better than any pitch deck. People who install it and like it sometimes become clients. People who install it and never become clients are still better off for having a working company memory.

### How long does install take?

About 25 minutes via the skill. Most of that is reading and clicking through Obsidian's own setup; the skill's portion is ~5 minutes. Manual install (if you go that route) is ~45-60 minutes.

### What do I get at the end?

A folder on your disk with: SCHEMA.md (rules), CONTEXT.md (about your company), index.md (lookup), log.md (audit trail), HOW-TO-USE-THIS.md (the living guide), an Operating Principles starter, a Welcome page, and template files your AI can read at session start. About 22 files total.

---

## Vault lifecycle

### Can I install this into a folder that already has files?

No. The skill refuses (key decision #14). Use an empty folder. The refusal is the safe answer — it prevents accidental overwriting of existing work.

### Can I install multiple vaults for multiple companies?

The skill is single-company by permanent design (key decision #4). If you genuinely run two separate companies, install two separate vaults in two separate folders. If you advise multiple clients and need a multi-client layout: use the Absolution Labs Client Knowledge Base shape instead — different artefact, not what this skill ships.

### Can I move or rename my vault folder?

Yes, but you'll need to update your AI tool's mount path. See [troubleshooting.md § "I moved the vault folder"](troubleshooting.md#i-moved-the-vault-folder-and-the-wikilinks-broke). The wikilinks survive moves; the AI's session-start path doesn't.

### Can I rename my company in the vault?

Yes. The substituted `{{COMPANY_NAME}}` appears in roughly a dozen files. Find-and-Replace across the vault (Obsidian's built-in or your editor's) handles it cleanly. Don't forget `_meta/scaffold-version.txt` and `CONTEXT.md`.

### What happens if I uninstall the skill?

Nothing happens to your vault. The skill installs into your agent CLI (Cowork plugin folder / `~/.claude/skills/`); your vault is a separate folder on your disk. Uninstalling the skill removes the install procedure from your AI tool but leaves your vault untouched.

### Can I delete my vault?

Yes, like any folder. Cloud sync version history typically lets you recover for 30+ days if you change your mind. There is no proprietary database, no vendor lock-in — the vault is plain markdown.

### Can I upgrade to a new skill version later?

See [upgrading.md](upgrading.md). Short answer: your vault doesn't auto-upgrade. New skill versions affect future scaffolds; existing vaults stay as-is unless you explicitly pull in changes (which is rare — once your vault is yours, it's yours).

### Can I start over from scratch?

Yes. Delete the vault folder, re-run the skill on an empty folder. You lose everything in the old vault. If you want to keep some pages: copy them out first, scaffold fresh, paste them back into the new structure.

---

## Data and privacy

### What does Absolution Labs see about my vault?

Nothing. The skill collects zero telemetry — no install ping, no health check, no usage data, no error reports. Your vault contents never reach our infrastructure in any version.

### Did earlier versions collect any data?

Yes. v1.0.0 and v1.1.0 shipped an opt-out 9-field anonymous install ping to an EU-hosted Supabase project (random UUID, skill version, OS family, install surface, sync provider, outcome, timestamp, optional failure step on failures). We removed it entirely in v1.2.0 because the value to us was structurally near-zero — Cowork's sandbox couldn't fire the POST so half of our data was missing by design — and the compliance overhead didn't earn the trust framing the bundle leans on. The infrastructure is being sunset; existing orphan rows contain no PII.

### Does the skill phone home for any other reason?

No. After install, there is zero network activity from the skill (it's not running — it's a one-shot scaffold). Subsequent vault use is between you, Obsidian, and your AI tool; the skill doesn't observe it.

### Is the vault encrypted?

The vault itself is plain markdown — not encrypted. Encryption lives at the cloud sync provider (Dropbox / iCloud / OneDrive / Google Drive all encrypt at rest and in transit by default) and at the OS level (FileVault / BitLocker / LUKS). If you need vault-level encryption (regulated-sector data), consider local-only sync + an encrypted disk image.

### What if I'm in a regulated sector (finance, legal, healthcare)?

The compliance gate at install Step 1 asks you to confirm three things up front. The third confirmation specifically: *Absolution Labs LTD has no access to your vault contents at any point.* If your DPA requirements still flag anything, email us before installing — we'd rather lose an install than ship a problem.

### Can my company's IT see what's in my vault?

If the vault is on a corporate-managed cloud sync (OneDrive for Business, Dropbox for Business) or a corporate-managed device: IT has the same access they have to any other file in that sync. The skill doesn't change that. If you need air-gapped: local-only sync provider, personal drive.

---

## Customisation

### Can I edit SCHEMA.md?

Yes. After scaffold, SCHEMA.md is yours. [docs/customisation.md](customisation.md) covers what's safe to edit (content), what to edit carefully (procedure), and what to leave alone (telemetry).

### Can I change the folder structure?

Yes, but the lint expects the canonical folders. If you remove or rename `entities/`, `concepts/`, etc., update the lint config in `_meta/expectations.yml` too.

### Can I add new folder types?

Yes. `decisions/`, `meetings/`, `customers/` — anything that helps you organise. Add a section to `index.md` for it. The lint reads `index.md` to know what exists, so as long as you keep `index.md` current, the structure is yours.

### Can I rebrand the skill for my company?

Yes (MIT licensed). Per the LICENSE, rename your variant so users don't confuse it with the Absolution Labs original. [docs/customisation.md](customisation.md) walks the rebrand.

### Can I change the starter Operating Principles?

Yes. They're a starter, not a doctrine. Edit `concepts/claude-operating-principles.md` to whatever shape fits your team. Five is the default for approachability; some teams grow it to 15-20 over time.

### Can I add a new question to the install intake?

In your fork, yes. The install asks two questions (company name + sync provider) by deliberate design — more questions create more friction at the trust moment. If you add (e.g.) "industry" or "team size", make it optional and explain why you're asking.

### Is there any telemetry in my fork?

No — telemetry was removed from the bundle entirely in v1.2.0. There's nothing to enable, disable, or reroute. If your fork is based on v1.0.0 or v1.1.0 and you want to remove the telemetry surface, the v1.2.0 commit `e8b3f63` → `<v1.2.0 hash>` shows exactly which fields, files, and SKILL.md sections to remove.

### Can I add Templater to my vault?

Yes, but it's not bundled (key decision #7). Install from Obsidian's plugin browser. The skill's `_meta/templates/*.md` files are plain markdown with `{{TODAY}}` placeholders; Templater can substitute them at page-creation time if you want. No conflict.

### Can I add other community plugins?

Yes. They land in `.obsidian/plugins/` and are invisible to the skill. No conflicts expected. See [COMPATIBILITY.md § Community plugins](../COMPATIBILITY.md#community-plugins-user-installed-not-bundled).

### Can I add my own AI tool's session-start file?

Yes. If you use a tool that reads (e.g.) `INSTRUCTIONS.md` rather than `CLAUDE.md` or `AGENTS.md`, add it as a template at the vault root. Our `CLAUDE.md.template` and `AGENTS.md.template` are starting points, not exhaustive.

---

## AI session behaviour

### Does the AI know about the vault automatically?

No. You point the AI at the vault at session start (Cowork: `request_directory` with the vault path; Code: `cd` to the vault). The AI reads `SCHEMA.md` and `CONTEXT.md` per its session-start protocol, then follows the scaffolded procedure.

### What happens if the AI ignores SCHEMA.md?

Three things to check, per [troubleshooting.md § "The AI keeps writing pages that don't match SCHEMA.md"](troubleshooting.md#the-ai-keeps-writing-pages-that-dont-match-schemamd). Usually a force-reread fixes it.

### Why does the AI sometimes propose changes that don't fit my vault?

LLMs work from session context plus their training. If your SCHEMA differs from typical AI memory patterns, the AI may default to its trained pattern instead of yours. The fix: at session start, re-anchor with *"Re-read SCHEMA.md and CONTEXT.md. Confirm you've done so before any work."*

### Do I need a specific AI model?

No. The vault works with any model the skill's host CLI supports (Claude Opus, Claude Sonnet, GPT-4, Gemini, etc.). Skill scaffolds the same regardless. Quality of AI follow-through varies by model; Claude Opus and Sonnet are what we test against.

### Can I use this without an AI?

Yes. The vault is plain markdown; you can write to it by hand in Obsidian. The skill, the lint, and the close-obsidian-project prompt all assume an AI as the editor — but the underlying artefact is yours regardless.

### Why does the AI keep suggesting we ingest things?

Because Ingest is the default-good action per SCHEMA's three-operation model (Ingest / Query / Lint). New information from a session usually wants to be captured. If you don't want to ingest, say so — *"don't ingest this; just answer my question"* — and the AI should comply.

### Why does the AI sometimes refuse to scaffold a project?

It's running `open-obsidian-project` and the target folder exists with content. Same shape as the skill's refuse-to-scaffold gate. The custom skill you built from `_meta/skill-prompts/open-obsidian-project.md` should refuse on non-empty target folders. If it doesn't refuse: it's misconfigured — re-read the prompt file and adjust.

### What's the difference between the skill and the custom skills I built?

This skill scaffolds the vault — one-shot, install time only.

The custom skills you built from `_meta/skill-prompts/` (`open-obsidian-project` and `close-obsidian-project`) run repeatedly — every time you start a project, every time you end a session. They live in your AI tool, not the vault.

---

## Obsidian-specific

### Do I need Obsidian to use this?

The skill produces a vault structure Obsidian opens. If you use a different markdown editor (VS Code, Logseq, etc.), the vault still works as a folder of markdown files — you just miss Obsidian's wikilink resolution and graph view.

### What Obsidian version do I need?

1.5+ (the `.obsidian/` configs use fields stable since 1.5). See [COMPATIBILITY.md § Obsidian](../COMPATIBILITY.md#obsidian).

### Why did you ship a `.obsidian/` config?

So the round-trip test works on first open. Without it, Obsidian opens with defaults that may not include wikilink rendering, which would break the verification step. The config we ship is conservative and intentionally avoids opinionated theming.

### Can I use my own theme / colors?

Yes. After scaffold, edit `.obsidian/appearance.json` or use Obsidian's Settings → Appearance UI. Your changes persist in the file; the skill never re-runs.

### Can I sync the vault between my desktop and mobile?

Yes — the vault is plain files. Use the same cloud sync provider on both devices and point Obsidian on each at the synced folder. Note: the install skill assumes desktop (it needs a file picker); after install, mobile editing works fine.

### What happens to Obsidian's workspace state across sessions?

`.obsidian/workspace.json` tracks open tabs, sidebar widths, etc. It's safe to delete (Obsidian regenerates it on next launch) and is excluded from the lint. Sync conflicts on it are common across devices; resolve by keeping the more-recent one and re-opening Obsidian.

### Can I open the vault in multiple Obsidian instances?

Not recommended. Obsidian doesn't lock files, so two instances editing the same vault can produce conflict files (see [troubleshooting.md § Cloud sync conflict files](troubleshooting.md#cloud-sync-conflict-files)). One instance at a time is the safe pattern.

### Does Obsidian's Sync (paid) work with this?

Yes. Obsidian Sync is just another sync provider from the skill's perspective — same compatibility caveats as Dropbox / OneDrive. No special configuration required.

### Does this work with Obsidian Publish?

The vault is markdown; Obsidian Publish reads markdown. Publishing the vault to a public Obsidian Publish site works mechanically — but think hard about whether you want your company memory public. Most users don't.

---

## Lint and quality

### How often should I run the lint?

[HOW-TO-USE-THIS.md](../templates/HOW-TO-USE-THIS.md) recommends weekly. The lint catches: orphan pages, broken wikilinks, stale content, index drift. Weekly is enough for most teams; daily is overkill; monthly lets too much drift accumulate.

### Will the AI run the lint automatically?

No (key decision #5 — manual invocation only). Schedulers add complexity (per-OS, sleep/wake failure modes); manual is the safer default. Ask your AI: *"run a lint on the vault."*

### What does the lint actually do?

Five checks: contradictions, orphans, stale content, data gaps (broken wikilinks), index drift. Plus a CONTEXT.md staleness check on multi-client variants. See SCHEMA.md § Lint Operation.

### Can I customise the lint thresholds?

Yes. Edit `_meta/expectations.yml`. The Dataview queries in `lint-reports/` consume the thresholds; your changes apply on next lint run.

### What happens if I never run the lint?

Nothing immediate. Drift accumulates: pages stop being linked from index, wikilinks point at deleted pages, dates fall behind. Eventually finding things gets harder. The lint's job is to catch drift before it becomes hard to fix.

---

## Practical scenarios

### My company name changed — what do I update?

In order of importance:
1. `CONTEXT.md` — the "About `<company>`" section.
2. `_meta/scaffold-version.txt` — informational, but worth updating.
3. Find-and-Replace across the vault for the old name.
4. Tell your AI in the next session, so the conversation picks up the new name.

### I want to bring an existing notes folder into this vault.

Out of scope for the skill (key decision #14). Manual path: scaffold a fresh vault in a new folder, then copy your existing markdown files into the right scaffolded folders (`entities/`, `concepts/`, etc.). Add each copied page to `index.md`. Run a lint to catch the structural gaps.

### My team is growing — can multiple people edit the vault?

Yes, via any shared cloud sync. Coordinate to avoid simultaneous edits (one person per file at a time). For larger teams, Obsidian Publish + a single-author convention works; for collaborative-edit teams, consider a git-backed setup (out of scope for the skill).

### I want to keep some pages private to me.

The vault is folder-level access. If you sync via Dropbox, anyone with the folder shared sees all of it. Two patterns: (a) put private pages in a separate vault, (b) maintain a personal vault alongside the company vault and reference it from your AI session prompts.

### I want to share specific pages with a client or vendor.

Export the page as PDF (Obsidian's File → Export to PDF), or copy the markdown text. Don't share the vault folder itself — it includes pages they shouldn't see.

### What if I want to migrate to a different memory system later?

The vault is plain markdown. Copy the folder. Open it in the new system. No lock-in. The schema (SCHEMA.md) and operating principles (concepts/) are documents the new system can either read or replace.

### What if Absolution Labs disappears tomorrow?

Your vault is on your disk; it has no dependency on Absolution Labs at runtime. The skill source is open and forkable. The telemetry endpoint disappearing means future installs fail; your existing vault keeps working forever.

---

*Cross-references: [README.md](../README.md), [SKILL.md](../SKILL.md), [COMPATIBILITY.md](../COMPATIBILITY.md), [troubleshooting.md](troubleshooting.md), [customisation.md](customisation.md), [upgrading.md](upgrading.md), [privacy-policy.md](privacy-policy.md), [standard-vs-ours.md](standard-vs-ours.md).*

---

## Use at your own risk

This document is part of the Obsidian Company Memory bundle, provided "AS IS" without warranty of any kind under the MIT License. It is for general informational and educational purposes only and does not constitute professional advice. AI-generated outputs from any vault scaffolded by this skill may contain errors and must be independently verified before reliance. **Read [DISCLAIMERS.md](../DISCLAIMERS.md) in full before installing, forking, or relying on anything in this repository.**

*© 2026 Absolution Labs. AbsolutionLabs Ltd, registered in England and Wales (Company No. 17091663). Registered office: 15 Westbury Road, London SE20 7QL.*
