# Obsidian Company Memory

**Not an Obsidian template. A control system for how AI agents read, write, and stay accountable to your company's knowledge. Scaffolded onto your machine in about 25 minutes. Free, MIT-licensed, distributed by [Absolution Labs LTD](https://absolutionlabs.com).**

---

The folder structure is the rendering layer; the bespoke prompts, rulebooks, and operating principles inside it are the product. A small set of files governs how every AI session interacts with the vault: it reads `SCHEMA.md` first, follows the Ingest / Query / Lint procedure, and writes the result back to an audit trail. You run a one-off install. From then on, your company's knowledge accumulates as a by-product of normal AI-assisted work — not as a wiki you have to maintain on the side.

This skill is the install moment. It does not run again once your vault exists; ongoing use is governed by the living guide it drops at your vault root.

---

## Use at your own risk — read this before installing

The bundle is provided "AS IS" without warranty of any kind under the MIT License. It is for general informational and educational purposes only and does not constitute legal, regulatory, security, financial, or other professional advice. AI-generated outputs from any vault scaffolded by this skill may contain errors and must be independently verified before reliance. Compliance with your sector's regulatory obligations is your responsibility, not ours.

**Read [DISCLAIMERS.md](DISCLAIMERS.md) in full before installing, forking, or relying on anything in this repository.** Liability cap, statutory carve-outs (UK), indemnity (for forks), governing law, and how to serve formal notice are all set out there.

By installing the skill, you accept those terms.

---

## Install

The install is **three zip uploads in Cowork** (or three folder copies in Claude Code), then ~25 minutes — most of which is you installing Obsidian itself and granting your AI tool access to a folder.

### Cowork (recommended)

1. Go to the latest GitHub Release: [github.com/absolutionlabs/obsidian-company-memory/releases/latest](https://github.com/absolutionlabs/obsidian-company-memory/releases/latest)
2. Download three zips:
   - `open-obsidian-project-vX.Y.Z.zip` — companion: starts new projects against the vault
   - `close-obsidian-project-vX.Y.Z.zip` — companion: runs the session-close protocol
   - `obsidian-company-memory-vX.Y.Z.zip` — main install skill (~25-min vault scaffold)
3. In Cowork: open **Skills → Upload skill** and drag-drop each zip, one at a time. Suggested order: companions first (small, self-contained), main install skill last.
4. Once all three are installed, ask your AI: *"Set up Obsidian company memory"* (or paraphrase). The main skill takes it from there.

### Claude Code

Native `claude plugin marketplace add` is on the v1.3.0 roadmap. For now, clone the repo and copy the three skills into `~/.claude/skills/`:

```bash
git clone https://github.com/absolutionlabs/obsidian-company-memory.git ~/tmp/obsidian-company-memory
cp -r ~/tmp/obsidian-company-memory ~/.claude/skills/
cp -r ~/tmp/obsidian-company-memory/companion-skills/open-obsidian-project ~/.claude/skills/
cp -r ~/tmp/obsidian-company-memory/companion-skills/close-obsidian-project ~/.claude/skills/
```

Restart Code; ask your AI to *"set up Obsidian company memory"* to invoke.

### Codex / opencode / other AGENTS.md tools

Download the three zips as above, unzip each, and append the body of each `SKILL.md` to your home `~/.codex/AGENTS.md` (or equivalent) under a "Custom skills" section. The skills are written to be tool-agnostic — anything that reads `AGENTS.md` can run them.

> The install URL, version picker, and Loom walkthrough also live on the Absolution Labs website at [absolutionlabs.com](https://absolutionlabs.com).

## Before you install

### You will need

- A laptop running macOS 12+, Windows 10/11, or a recent Linux distro.
- An empty folder inside a cloud-synced location (Dropbox, iCloud, OneDrive, Google Drive), OR a local-only folder you're willing to back up yourself.
- Obsidian installed locally. Download it from [obsidian.md](https://obsidian.md/download) — free for personal and commercial use.
- One of: Cowork, Claude Code, Codex, opencode, or any other AI tool that reads `CLAUDE.md` / `AGENTS.md` and supports mounted-directory access.

### You will be asked to confirm

Above the gate, you'll see a one-line passive statement: *"This skill writes files only to your folder. Nothing is sent to Absolution Labs at install or afterwards. Full terms: DISCLAIMERS.md."* That's the privacy posture, stated for the record — you don't confirm it.

You DO confirm two things about *your* setup:

1. The folder is yours to write to (no other party's data already inside).
2. Your cloud sync provider is permitted for the content you intend to store (DPA awareness).

If you're in a regulated sector (drinks, healthcare, finance, professional services), box 2 is the one that matters — we don't enforce anything about your provider, but we surface the question before any data lands. Compliance starts at install, not at first incident.

---

## What gets installed

Inside your chosen folder, after install:

```
your-vault/
├── SCHEMA.md                    ← rulebook every AI session reads first
├── CONTEXT.md                   ← long-term memory for your company
├── index.md                     ← table of contents (always in sync)
├── log.md                       ← audit trail of every session
├── HOW-TO-USE-THIS.md           ← Phase 2 living guide (~10-min read)
├── CLAUDE.md.template           ← project-stub for open-obsidian-project
├── AGENTS.md.template           ← project-stub for Codex / opencode users
├── entities/                    ← one page per thing worth remembering
│   └── test-welcome.md          ← the round-trip test result
├── concepts/
│   └── claude-operating-principles.md
├── comparisons/                 ← side-by-side analyses (empty at start)
├── queries/                     ← synthesised answers worth keeping
├── raw/                         ← source documents (never edited)
│   ├── articles/
│   ├── transcripts/
│   └── assets/
├── lint-reports/                ← output from manual vault lint
├── _meta/
│   ├── expectations.yml         ← lint thresholds (editable)
│   ├── scaffold-version.txt     ← which version installed this vault
│   └── templates/               ← page templates (entity / concept / query)
└── .obsidian/                   ← Obsidian config (sensible defaults)
```

~20 files. All markdown / YAML / JSON. No binaries, no secrets, no telemetry inside the vault.

The two companion skills (`open-obsidian-project`, `close-obsidian-project`) ship as separate zips on the same GitHub Release — you install them via the same Upload-skill UI before (or after) the main install. They live in your AI tool's skill folder, alongside the main `obsidian-company-memory` install skill, not inside the vault. See [companion-skills/README.md](companion-skills/README.md).

## What the skill does NOT install

These are deliberate cuts. We hold the full design rationale internally; email `info@absolutionlabs.com` if you want specifics on a particular cut.

- **Obsidian itself.** You install Obsidian from `obsidian.md` separately. We tell you when.
- **Community plugins.** Dataview, Templater, etc. are installed by you from Obsidian's own plugin browser. We don't bundle third-party binaries inside our distributable.
- **An AI assistant.** Cowork, Code, Codex, opencode — you install whichever you use separately.
- **A first project.** Use the `open-obsidian-project` companion skill (installed separately from its own zip on the same GitHub Release) when you're ready to start one. Pair it with `close-obsidian-project` for session-close discipline. See [companion-skills/README.md](companion-skills/README.md) for details. Names use `-obsidian-project` namespacing so they coexist with any other "open project" / "close" skills you already have.
- **Multi-client routing.** This is single-company by permanent design. If you need multi-client, this isn't the right shape — email `info@absolutionlabs.com`.
- **A scheduled lint.** Lint is manual-invocation only: just ask your AI to "run a lint on the vault" when you want it.
- **A way to migrate an existing vault.** The skill refuses to scaffold into non-empty folders. If you have an existing vault, email `info@absolutionlabs.com` — we'll help.

## Architecture, in one paragraph

The vault has three layers. **Raw** — source documents you didn't write, in `raw/`, never edited; corrections go in linked wiki pages. **Wiki** — pages you (or the AI) write, one per thing worth remembering, in `entities/` / `concepts/` / `comparisons/` / `queries/`. Every page has YAML frontmatter and at least one `[[wikilink]]` to another page; orphans are invisible. **Schema** — `SCHEMA.md` (rulebook), `index.md` (table of contents), `log.md` (audit trail). Every AI session reads SCHEMA first, then CONTEXT, then works, then writes back. The architecture is the same shape we use inside Absolution Labs for our own knowledge base.

Full architecture detail in [templates/SCHEMA.md](templates/SCHEMA.md) and the post-install [HOW-TO-USE-THIS.md](templates/HOW-TO-USE-THIS.md).

## Privacy

The skill writes to your local folder via your AI assistant's mounted-directory access. **Nothing flows back to Absolution Labs at any point** — no install ping, no health check, no usage data, no error reports. The skill never phones home, at install time or afterwards.

Earlier releases (v1.0.0 / v1.1.0) shipped an opt-out 9-field anonymous install ping to an EU-hosted Supabase project. That surface was removed entirely in v1.2.0 — the value to us was structurally near-zero (Cowork sandbox couldn't fire the POST, so half our data was missing by design) and the compliance overhead disproportionate. The infrastructure is being sunset; orphan rows contain no PII.

## Security & integrity

- **Bundle signing + SHA256 checksums** will ship with every public release (Chunk 7 release process). They are not present on the v1.0.0 private-beta tag — when public ship lands, the current signing key and checksums file will be linked from the install page on [absolutionlabs.com](https://absolutionlabs.com).
- **Threat model** covers six surfaces (secrets, privacy + data, prompt injection, attack surface, backup + rollback, external platform config). Full text held internally; we share specifics on written request.
- **No third-party binaries shipped.** Everything in the bundle is markdown / YAML / JSON / TypeScript.

If you find a security issue: please email `security@absolutionlabs.com` rather than opening a public issue. We respond within one business day.

## Compatibility

Tested combinations + known-good versions: [COMPATIBILITY.md](COMPATIBILITY.md).

If you hit a compatibility issue we haven't documented, please send it to `info@absolutionlabs.com` — we add to the matrix quarterly.

## Documentation

- **[templates/HOW-TO-USE-THIS.md](templates/HOW-TO-USE-THIS.md)** — the Phase 2 living guide. Read this after install. ~10 minutes.
- **[docs/install-walkthrough.md](docs/install-walkthrough.md)** — step-by-step reading-version of the install procedure. Useful if you'd rather read than watch the Loom, or need to vet the procedure before running it.
- **[docs/manual-install-guide.md](docs/manual-install-guide.md)** — by-hand install procedure for users on agent CLIs the skill doesn't reach (Codex / opencode), regulated-sector users who want to inspect every file, or any user blocked by proxy / firewall from the canonical install paths. ~45-60 minute follow-along.
- **[docs/customisation.md](docs/customisation.md)** — fork your own variant; what's editable, what isn't.
- **[docs/troubleshooting.md](docs/troubleshooting.md)** — common failure modes and recovery (incl. download issues, file-structure confusions, environmental incompatibilities).
- **[docs/faq.md](docs/faq.md)** — question-shape help: "can I", "what if", "why does it". Different surface from troubleshooting (which is problem-shape).
- **[docs/standard-vs-ours.md](docs/standard-vs-ours.md)** — diff between common Obsidian + AI patterns and what this bundle ships. Read this if you're deciding whether to install.
- **[docs/upgrading.md](docs/upgrading.md)** — version pinning, rollback, manual refresh.
- **[DISCLAIMERS.md](DISCLAIMERS.md)** — full disclaimer, limitation of liability, statutory carve-outs (UK), indemnity (for forks), governing law. **Required reading before install.**
- **[MANIFESTS.md](MANIFESTS.md)** — the mirror contract between `plugin.json` (Cowork) and `SKILL.md` frontmatter (Claude Code).

## Support

- **Email:** `info@absolutionlabs.com` — replied to by a human at Absolution Labs within one business day.
- **Feedback:** same email; subject line "Feedback — Obsidian Company Memory".
- **Security issues:** `security@absolutionlabs.com`.
- **Anything else:** visit [absolutionlabs.com](https://absolutionlabs.com).

## License

MIT. See [LICENSE](LICENSE). You can fork, modify, redistribute, sell, or build on top of this — the only requirement is that the copyright notice and license text travel with the copy. If you build a commercial variant: please rename it so it isn't confused with the official Absolution Labs release.

## About Absolution Labs

[Absolution Labs LTD](https://absolutionlabs.com) builds AI-augmented operations tools for small companies, mostly in drinks and FMCG. We published this skill because the same shape of company memory underpins every project we run with our own clients, and we'd rather more companies have access to it than gate it behind a sales conversation. If you install it, see it work, and want the next thing — you know where to find us.

---

*Maintained by Absolution Labs LTD. This README, the bundle, and the operator's whole memory architecture are themselves stored in an Obsidian vault of this exact shape.*

---

*© 2026 Absolution Labs. AbsolutionLabs Ltd, registered in England and Wales (Company No. 17091663). Registered office: 15 Westbury Road, London SE20 7QL. Full disclaimers: [DISCLAIMERS.md](DISCLAIMERS.md).*
