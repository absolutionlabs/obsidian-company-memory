# How We Use Obsidian + Claude — A User Guide

*Draft v0.1. Audience: anyone setting this up for their own company who isn't a developer. Read time: ~15 minutes.*

> **Status note (2026-06-03).** This file pre-dates the SHAPE reframe (captured in our internal project brief). The content here remains broadly accurate as a user-facing description of the system, but the canonical user-facing surfaces are now:
>
> - [README.md](README.md) — public-facing entry point for anyone who has the bundle
> - [templates/HOW-TO-USE-THIS.md](templates/HOW-TO-USE-THIS.md) — the Phase 2 living guide that ships into every scaffolded vault
> - [TESTERS.md](TESTERS.md) — instructions for private-beta testers
> - [website/install-page.md](website/install-page.md) — the install landing page copy
>
> This document is retained as an internal reference for anyone reading the project history. New external-facing copy should land in one of the four canonical surfaces above, not here.

---

## TL;DR (60 seconds)

We give the business a **single folder** that acts as its long-term memory. The folder holds plain text notes, one per thing worth remembering (a person, a tool, a decision, a price, a brand rule, a meeting outcome). A free app called **Obsidian** lets a human browse, search, and edit the notes comfortably. **Claude** reads and writes the same notes directly, following a small rulebook (`SCHEMA.md`) that lives in the folder itself.

Three big ideas hold it together:

1. **It's just files.** Markdown text files on your disk. No SaaS, no database, no lock-in. If every app vanished tomorrow you'd still have the notes.
2. **A rulebook, not a vibe.** `SCHEMA.md` defines how knowledge enters (Ingest), how it's retrieved (Query), and how it's kept healthy (Lint). Every Claude session reads it first. The result is consistent capture across hundreds of sessions instead of "every session does it slightly differently."
3. **Compounding by side-effect.** You don't curate the vault. You just do your normal work, and at the end of each session Claude writes what was learned into the right place automatically. Six months in, the vault is a real asset; you never spent a day "filling it in."

**Surface-agnostic by design.** Because the vault is just markdown files on disk, any AI agent that can read and write local files can work with it. Today that includes **Claude Code** (Anthropic's CLI), **Codex** (OpenAI's coding CLI), **opencode** (the open-source equivalent), and **Hermes** (our own server-side agent that runs scheduled jobs against the same files). They all read the same `SCHEMA.md`, write to the same `index.md` and `log.md`, and produce the same Ingest / Close artifacts. There is one vault and several doors into it. If a new agent appears next year that can mount a folder, it joins the rotation without anything in the vault needing to change.

**What you actually do day to day:** open a session, describe today's work, let Claude pull the relevant notes and produce whatever the work needs, and type `/close-full` at the end. The close protocol updates the project brief, writes any new knowledge into the wiki, appends a one-line entry to `log.md`, and produces a continuation prompt you can paste into the next session. That's the whole loop.

**What keeps it healthy:** a small set of scheduled jobs (daily / weekly / monthly) that lint the vault for broken links, orphan pages, stale content, duplicates, and contradictions. They don't fix anything autonomously — they flag, so you decide. Loud on failure, quiet on success.

**What you get:** an AI that knows your business cold from session one, a dated audit trail of every decision and why, a memory that compounds rather than evaporates, and a folder you can hand to a new hire, a new agency, or take with you if you ever sell the business. The rest of this guide is the long version.

---

## 1. What this thing actually is

Imagine a really good Chief of Staff who never forgets anything. Every meeting, every decision, every "we tried that in March and it didn't work," every brand rule, every supplier quirk, every price list, every recurring task — all of it is filed away in a single, tidy cabinet. When you ask them a question, they pull the right folder, read it back to you, and remind you of the three things you said last time that contradict what you're about to do.

That's what this setup is. A single folder of plain text files on your computer that acts as your business's long-term memory, plus an AI (Claude) that reads from it and writes to it as you work. The folder is browsed with a free app called **Obsidian** so a human can read and search it comfortably. The AI is reached through **Claude Code** so it can directly read, write, and check the same files you can see.

**The folder is the system.** Not a SaaS subscription, not a cloud database, not a chatbot's hidden memory — a folder. If the apps disappeared tomorrow, you'd still have every file. You can open them in any text editor, email them, zip them up, print them. That portability is the whole point.

**Why Obsidian** rather than Notion or Google Docs? Three reasons:

1. **It's just files on your disk.** No vendor lock-in. The files are markdown (`.md`), which is plain text with light formatting. Any tool can read them, now and forever.
2. **Wiki-style linking.** You write `[[Acme Corp]]` inside a note and it becomes a clickable link to the Acme Corp page. Click it, you're there. Click the backlinks panel, you see every other page that mentions Acme. The result is a web of connected knowledge that's far more useful than a flat folder of documents.
3. **An AI can read it natively.** Claude understands markdown perfectly, can follow `[[wikilinks]]` to jump between pages, and can edit pages directly without breaking anything. The same files that make Obsidian feel pleasant for humans make it ideal as an AI's working memory.

**Why an AI with file access** rather than a plain browser chat? Plain browser chat can only read what you paste in. An AI with file access (Claude Code, Codex, opencode, or any equivalent CLI) can read your *whole folder*, run little checks, and edit files directly. It's the difference between a friend you describe a problem to over the phone, and a friend who walks into your office and pulls the relevant file off the shelf themselves.

The surface matters less than the capability. We use **Claude Code** as the default because it's the most mature today, but **Codex**, **opencode**, and our own **Hermes** server-side agent all work against the same vault. The vault doesn't know or care which one you used — it just receives reads and writes against its files, following the same rules in `SCHEMA.md`. If your team is on a different agent CLI, the vault travels with you.

---

## 2. The mental model — vault, layers, walls

Before getting into setup, three concepts make everything else click.

### The vault

In Obsidian, a "vault" is just a folder that contains a `.obsidian/` config subfolder and a bunch of markdown files. There's no installation, no database to set up — the moment you point Obsidian at a folder, it becomes a vault. You can have one vault for your business, several vaults for different parts of life, or move/copy a vault between machines just by copying the folder.

In our setup we use **one vault per company** — the company's whole memory lives in a single folder, and you mount that folder when you sit down to work.

### The three layers

Inside the vault, files fall into one of three roles. This is the architecture rule that keeps the system honest as it grows:

- **Layer 1 — Raw.** Source documents you didn't write yourself. Meeting transcripts, supplier PDFs, scraped articles, brand books, contracts. They live in `raw/` and they are *never edited*. If a transcript has a typo, the typo stays. Corrections go in a separate wiki page that links back to the raw file. The raw layer is the audit trail.

- **Layer 2 — Wiki.** Notes you (or the AI) write. Each one is a single short page about one thing — a person, a tool, a concept, a decision. They live in `entities/`, `concepts/`, `comparisons/`, and `queries/` folders. Every wiki page has a small header (called "frontmatter") that records what it is and when it was last updated, and every wiki page links to at least one other page. No orphans allowed.

- **Layer 3 — Schema.** Three small files that govern how the wiki operates: `SCHEMA.md` is the rulebook, `index.md` is the table of contents, `log.md` is the running history of what was added and why. The AI reads `SCHEMA.md` at the start of every session — it's the difference between an AI that "kind of writes notes" and an AI that follows your house rules every single time.

The analogy: Raw is a stack of original documents in a fireproof safe; Wiki is the index cards you wrote about them, cross-referenced and tagged; Schema is the librarian's rulebook. Nobody edits the documents in the safe; the cards can be updated freely; the rulebook only changes when you deliberately update it.

### The walls

Once you have more than one client, business unit, or area of concern, you need a wall between them so notes for one don't contaminate notes for another. We do this with subfolders: `clients/acme-corp/` is Acme's whole wiki-in-miniature, with its own `entities/`, `concepts/`, `raw/`, `index.md`, and `log.md`. `clients/widgets-ltd/` is the same for Widgets Ltd.

For a **single-company** setup (the version we're going to package as a skill), the wall is simpler — there's no `clients/` subfolder at all. The whole vault is the company's knowledge. The three layers (raw / wiki / schema) still apply, just at the vault root.

---

## 3. How we set it up

Five things go into the box, in this order.

### 3.1 Install Obsidian and create the vault

Obsidian is a free download from obsidian.md. Install it, open it, and the first time it asks where to put your vault, point it at the folder you want to use. We keep ours inside Dropbox so it syncs to the cloud and across machines automatically — the choice of cloud (Dropbox, OneDrive, iCloud, a NAS, nothing at all) doesn't matter to Obsidian.

The moment you point Obsidian at a folder, it creates a `.obsidian/` subfolder inside it. That hidden folder holds your settings, your enabled plugins, and your workspace layout. It is part of the vault — if you move the vault, take `.obsidian/` with it.

### 3.2 Turn on the right plugins

Obsidian ships with a set of "core plugins" you enable from settings. We turn on:

- **File explorer, search, quick switcher** — the basic browse / find experience.
- **Graph view** — a visual map of every page and its links. Useful for spotting orphan pages and clusters.
- **Backlinks, outgoing links, outline** — show you what links to the current page, what it links out to, and a navigable table of contents for long pages.
- **Tag pane** — every page can carry tags in its frontmatter; this lets you filter by tag.
- **Daily notes, templates** — for the running log files and the page templates we use when creating new entities/concepts.
- **Properties, file recovery, bookmarks** — properties shows the frontmatter as an editable form rather than raw text; file recovery is a safety net; bookmarks are pinned pages you visit often.
- **Canvas** — a free-form drawing surface for sketching architectures. Pages can be embedded in a canvas.
- **Sync** — Obsidian's own end-to-end-encrypted sync (paid). Optional if you're already using Dropbox; useful if you want a sync that doesn't go through a cloud filesystem.

We add two **community plugins** (one-click install from inside Obsidian):

- **Dataview** turns the vault into a small database. You can write a query like "show me every decision page tagged `pricing` from the last 30 days, as a table" and it renders the live result inside a normal note. This is what makes the wiki feel like a system rather than a pile of files.
- **Templater** lets you define page templates with variables. New entity? New concept page? Hit a hotkey, fill the title, and you get a skeleton with the right frontmatter already in place.

That's the entire Obsidian setup. There is no database to host, no server to run, no API key to wire up.

### 3.3 Create the starter files

Three files do most of the structural work. We create them once, at the vault root, and they govern everything that follows.

- **`SCHEMA.md`** — the rulebook. It defines what counts as a wiki page, what the frontmatter header must contain, where `raw/` files go, what an Ingest operation does, what a Query operation does, what a Lint operation does, and what the close-of-session report looks like. This is the file the AI reads first, every session, no exceptions. Tweaks to your house rules go here.

- **`index.md`** — the table of contents. Every wiki page on disk has a one-line entry here. The index is what an AI uses to find pages relevant to your question without having to read the entire vault.

- **`log.md`** — the audit trail. Each session that adds or changes anything appends one dated entry: what was created, what was updated, why. Six months later, when you ask "when did we decide to switch suppliers?", the log shows you which session, what was discussed, and which pages got written.

A fourth file, **`CONTEXT.md`**, is a short pointer at the vault root that tells the AI three things: "this is the [Company Name] vault," "read `SCHEMA.md` next," and "client-specific knowledge goes wherever in this case it just goes into this vault root since this is single-company." For multi-client setups (ours), each `clients/<slug>/CONTEXT.md` adds the per-client rules and quirks.

### 3.4 Wire up an agent (Claude Code, Codex, opencode, Hermes)

Whichever agent CLI you use, the wiring is the same. Each "project folder" you work in has a tiny stub file called `CLAUDE.md` (some tools look for `AGENTS.md` or their own equivalent; the new-project-setup skill writes whichever names your tool reads). That stub tells the agent:

1. **Mount this vault.** The literal absolute path to your Obsidian folder. The agent gets read/write access to that exact path, and nothing outside it.
2. **Read `SCHEMA.md` first.** Before doing anything else.
3. **Here's the project context** — one or two sentences about what this project is, which company it's for, where deliverables should live.

The stub is small (about 20 lines) and is generated by the `new-project-setup` skill so you never write it by hand. The skill also checks whether the company has a wiki scaffold already and creates one if not.

**Claude Code (default).** Install once. Open a terminal in any project folder, type `claude`, the session starts. Skills installed at `~/.claude/skills/` are available in every project. File edits happen directly on local disk.

**Codex.** OpenAI's coding CLI. Same shape: install, point at a project folder, the stub guides the session. Procedures from our skill stack travel as `AGENTS.md` rules rather than skills, but the underlying protocol (read `SCHEMA.md`, mount vault, run Ingest at close) is identical.

**opencode.** Open-source equivalent. Useful if your team wants a model-agnostic agent or to run a local model. Same protocol; same files.

**Hermes (server-side).** Our own VPS-based agent. Useful for scheduled tasks (the daily / weekly / monthly audits described in §3.6), for long unattended runs, and for specialist worker personas. Hermes reads the same vault over a sync (Dropbox, syncthing, or a periodic git pull) and writes the same way the CLIs do.

Result: from any of these surfaces, the agent reads the stub, mounts the vault, reads the rulebook, and is ready to work — every time, no setup ritual on your part.

### 3.5 Install the skills (the guardrails)

A **skill** in Claude Code is a named procedure the AI knows how to run. Think of skills as the difference between "I told the chef to make pasta" and "I gave the chef the recipe for our house pasta, which we know works." The skill bakes the procedure in, so the result is consistent every time.

We use a small set of skills to keep the vault healthy:

- **`new-project-setup`** — scaffolds a new project folder and its `CLAUDE.md` stub, creates client wiki folders if needed, drops a brief template.
- **`wiki-ingest`** — runs the Ingest operation from `SCHEMA.md`. Creates or updates wiki pages, updates `index.md`, appends `log.md`. This is the workhorse — every session ends with at least one ingest.
- **`close` / `close-full`** — runs the close protocol. Updates the project brief, verifies that an ingest ran, drains any pending inbox items, writes the "what was touched this session" report, generates a continuation prompt for next time.
- **`realignment`** — used when an existing project's files drift away from current standards. Re-aligns to the current schema without rewriting history.
- **`forge`** — our project-management methodology. Walks you through scoping a new piece of work in stages (Shape, Build, Ship, Sustain) so projects don't sprawl.

Skills live in `~/.claude/skills/<skill-name>/SKILL.md` on your machine, which means once installed they're available in every project, not just one. The single-company version of this whole setup ships as one bundled "Obsidian Company Memory" plugin that installs the lot in one click.

### 3.6 Add the maintenance layer (lints, crons, observability)

Once the vault is in use it needs gentle, automatic maintenance. We layer this in three steps.

- **The Lint operation** (defined in `SCHEMA.md`) checks the vault's health: orphan pages with no incoming links, broken `[[wikilinks]]`, pages missing required frontmatter, stale `CONTEXT.md` files. It can be run manually any time or scheduled.

- **A small set of scheduled tasks** ("crons") run on a server we own (called Hermes) on a daily/weekly/monthly cadence. The full list and what each does is in the cheat sheet at the end. The principle is **loud on failure, quiet on success** — if everything's healthy, you hear nothing. If something drifted, you get a single Slack message.

- **The Operating Principles file** — `concepts/claude-operating-principles.md` inside the vault — is a single page that captures the cross-cutting rules we want every Claude session to follow ("don't delegate what the tools can do," "always update records the same session, not the next one," etc.). A small sync script copies this to your machine's global Claude config (`~/.claude/CLAUDE.md`), so the rules fire on every session regardless of which project you're in. This is what we call the three-tier memory architecture: the canonical page (Tier 1) → the user-global copy (Tier 2) → the cloud-Claude pointer (Tier 3).

---

## 4. How we use it day to day

The vault sits in the background. You don't curate it, you don't open Obsidian every morning. You just work, and the vault gets richer as a byproduct.

### 4.1 Starting a session

You open Claude Code in a project folder. The AI:

1. Reads the project's `CLAUDE.md` stub.
2. Mounts the vault at the path the stub gives it.
3. Reads `SCHEMA.md` to refresh its rules.
4. Reads the project brief if there is one.
5. Reads the relevant `CONTEXT.md` (vault root or client-specific).
6. Tells you what it's loaded and asks what you want to do.

You see this happen visibly in the chat. If anything's wrong (vault not mounted, brief missing, schema stale), it surfaces immediately rather than three turns later.

### 4.2 During a session

You describe the work. Claude does it. As facts surface ("the supplier's lead time is 6 weeks," "we decided to drop the smaller SKU," "the price for the trade channel is £18"), Claude proposes wiki updates inline. You confirm or correct, and the page gets written or updated immediately. The `updated:` date in the frontmatter changes. The `[[wikilink]]` from your project brief to the supplier page is in place.

The discipline is: **capture at the moment of recognition**, not at the end. Deferring capture is how knowledge becomes stale and fragmented.

You can also ask read-only questions ("what did we decide about the trade margin in March?"). The AI runs a Query: reads `index.md`, finds the relevant pages, reads them, synthesises an answer with citations. If the answer is substantial enough to be reusable, it becomes a new page under `queries/` so the next time the same question comes up, the answer is already filed.

### 4.3 Closing a session

When you're done, you type `/close-full`. The AI runs a fixed sequence:

1. **Drain inbound channels.** Are there any backlog files, inbox queues, or messages from the wider system that should be acted on before close? Usually not. Routed automatically when there are.
2. **Update the project brief.** Move completed items to the done section. Add any new open items.
3. **Run wiki-ingest.** Confirm at least one wiki page was created or updated this session. If nothing was, that's flagged — most sessions should produce *something*.
4. **Append `log.md`.** Dated one-paragraph entry: what changed, why.
5. **Write the KB Writes Report.** A list of every file touched this session, what kind of touch (created / appended / modified), one-line reason for each. This is the audit trail.
6. **Generate the continuation prompt.** A copy-pasteable block that next session can use to pick up exactly where this one left off.

That's the protocol. Skipping it leaves the vault in a half-updated state where this session's decisions are in your head but not on disk. Running it makes the vault self-healing — every session is its own small commit to the company's long-term memory.

### 4.4 The weekly rhythm

You don't need to do anything weekly. But the system does:

- **Saturday morning**: the consolidation agent reads everything written in the past 7 days and flags duplicates, contradictions, and merge candidates. It does not edit anything — it queues things for you to review.
- **Sunday night**: the summary regenerator rewrites the rolling summary page from scratch so it doesn't drift from the underlying pages.
- **Monday morning**: a spot-check picks three random project stubs and confirms they still mount the vault correctly.

If everything's clean you get one short Slack message per week. If anything's flagged, you get a specific question with file paths and a recommended action.

---

## 5. The guardrails that keep it healthy

This is what stops the system silently rotting. Each guardrail covers a different failure mode.

| Failure mode | What stops it |
|---|---|
| AI skips the rulebook and writes notes in a free-form style | Every project's `CLAUDE.md` stub forces a read of `SCHEMA.md` before any work |
| AI invents notes that look plausible but are wrong | The "trust the user over the wiki" rule — if you say something contradicts a page, the page gets updated, not argued with |
| Notes pile up but never get cross-referenced | Every wiki page must link to at least one other; lint flags orphans |
| Two pages disagree on the same fact | Weekly consolidation agent flags it (does not auto-resolve) |
| Pages get out of date | The `updated:` date is mandatory; lint flags anything older than 30/90 days depending on the page type |
| Source documents get edited or "tidied" and lose their evidentiary value | Layer 1 raw/ rule: never edit raw files, write a wiki page that points back to them instead |
| You forget to log what was done | `/close-full` enforces the KB Writes Report at the end of every session |
| Secrets (API keys, passwords) end up in notes | Operating Principles ban persistent secrets; daily cron lint scans for plaintext token patterns |
| Cross-client information leaks | Folder walls + `CONTEXT.md` per client + lint check for forbidden cross-references |
| Session ends silently with no record | Nightly audit detects "silent closes" (sessions that didn't append `log.md`) and surfaces them |
| Backups vanish | Git inside the vault gives full file history; Dropbox is the off-machine copy; weekly zip-backup is a third belt |

There's also a softer guardrail: the **Operating Principles**. These are 24 short rules we've accumulated about how Rob and Claude work together well (apply autonomously where it's safe, finish your own tasks, don't defer what can be done today, preserve docs by appending rather than rewriting, etc.). They live as one wiki page and get copied to the global Claude config so they fire on every session. New principles get added the same way notes get added: through normal work, captured at the moment of recognition.

---

## 6. The benefits, with concrete examples

The system pays back in three ways. Each example is the kind of thing it actually catches.

### 6.1 Memory that compounds instead of evaporating

*Without it:* In April you spent 90 minutes deciding which courier service to use for a particular product line. In October you have the same conversation again from scratch because nobody wrote it down properly.

*With it:* The April session created `entities/courier-options-comparison.md` with a verdict and reasoning. October's session asks "which courier did we go with for [product line]?" The AI reads the page, gives you the answer in 5 seconds, and quotes the reasoning. The 90 minutes from April becomes a permanent asset.

### 6.2 An AI that knows your business cold

*Without it:* Every chat starts by re-explaining who you are, what you make, how you price it, who your audience is. The AI's answers are generic because it has no context.

*With it:* You sit down, the AI mounts the vault, reads the relevant context pages, and answers like a colleague who's been with the company for two years. "Given that the trade margin is 35% and the wholesaler asked for £22 a bottle, that puts retail at..." comes out naturally, because the trade margin and wholesale relationships are in the wiki.

### 6.3 An audit trail you didn't have to maintain

*Without it:* Six months after a launch you're trying to remember why a particular decision got made and can't.

*With it:* The decision is in `decisions/decision-log.md` with a date, the reasoning, the alternatives considered, the person who made the call. The `log.md` entry from that session points to the page. The git history shows the exact commit. You have a sourced, dated record without anyone ever having "kept minutes."

The hidden fourth benefit is **portability**. You can hand the whole vault to a new staff member as their onboarding pack. You can hand it to a new agency you're hiring. You can take it with you if you sell the business. It's just a folder of files.

---

## 7. The cheat sheet (one page to print and pin)

**Open a session**
> "Continuing on [project]. Here's today's task: [...]. Follow the session open protocol."

**Close a session**
> `/close-full`

**Force a wiki capture mid-session**
> "Ingest that into the wiki under [folder]."

**Ask a question against the wiki**
> "Query the wiki: [question]"

**Files at the root of every vault**
- `SCHEMA.md` — the rulebook (you maintain; AI reads)
- `index.md` — table of contents (AI maintains)
- `log.md` — audit trail (AI maintains)
- `CONTEXT.md` — vault pointer (you maintain)

**Required frontmatter on every wiki page**
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query
tags: [tag1, tag2]
sources: [raw/source-file.md]
---
```

**The three operations**
- **Ingest** — write knowledge in. Triggered every session at close, or on demand.
- **Query** — read knowledge out. Triggered any time you ask the AI a "what did we decide" question.
- **Lint** — check vault health. Runs nightly automatically, or on demand.

**The scheduled tasks (defaults)**
| Task | When | What |
|---|---|---|
| Daily digest | 08:00 daily | Healthcheck + previous 24h summary to Slack |
| Nightly audit | 23:00 daily | Integrity check, silent-close detection |
| Nightly git backup | 23:00 daily | Commits everything written that day |
| Consolidation agent | Sat 10:00 | Flags duplicates, contradictions, merge candidates |
| Summary regeneration | Sun 23:00 | Rebuilds rolling summary from scratch |
| Spot check | Mon 09:00 | 3 random project stubs verified |
| Monthly auditor | 1st of month, 09:00 | Deep audit: drift, contradictions, staleness, PII |

**Emergency procedures**
- *Claude wrote something wrong* → Edit the page, commit, move on. The system trusts you over itself.
- *A page contradicts another* → Trust the newer information, update both, the next consolidation run confirms.
- *Vault folder accidentally moved* → Re-point Obsidian and Claude Code at the new location; nothing inside the vault stores absolute paths.
- *You want a snapshot* → `git tag snapshot-YYYY-MM-DD && git push --tags`, or zip the folder.

---

## 8. Glossary

- **Vault** — the Obsidian word for "the folder of files you're working in." One vault per company in our setup.
- **Markdown** — plain text with light formatting (`# heading`, `**bold**`, `[link](url)`). Every wiki page is markdown.
- **Frontmatter** — the small YAML header at the top of every page that records what kind of page it is and when it was last updated.
- **Wikilink** — the `[[Page Name]]` syntax that creates a clickable link inside the vault. The thing that makes the vault feel like a web rather than a folder.
- **Ingest** — the operation that writes new knowledge into the vault. Run at close, or any time on demand.
- **Query** — the operation that reads knowledge out of the vault. Run when you ask a "what did we decide" style question.
- **Lint** — the operation that checks vault health. Catches orphan pages, broken links, missing frontmatter, stale pages.
- **Schema** — the rulebook (`SCHEMA.md`). Defines what an Ingest does, what frontmatter is required, what a Query produces.
- **Skill** — a named procedure Claude Code knows how to run end to end. Skills bake protocols in so the result is consistent every time.
- **CLAUDE.md stub** — the small file in each project folder that tells Claude how to mount the vault and where the rules are. Generated by the `new-project-setup` skill.
- **Operating Principles** — the page that captures cross-cutting rules for how the human and the AI work together. Copied to the global Claude config so it fires on every session.
- **Cron / scheduled task** — a small job that runs automatically on a schedule (daily, weekly, monthly). Used for audits and digests.
- **Hermes** — the small server we run that hosts the scheduled tasks and a few specialist AI workers. Not strictly required for a single-company setup, but useful once you have more than a handful of audits.

---

## 9. What this draft does not yet cover (open items for v0.2)

Most of the items previously listed here have been resolved through the SHAPE process (2026-06-02) and folded into the skill build itself. Locked project state lives in our internal project brief; the public reframe addendum is at [shape-1-scope.md](shape-1-scope.md) §17. Remaining open items for this guide:

- This guide describes how WE use the system today. It is the **reference document** the skill is based on — not the skill's user-facing material. The skill will ship its own user-facing guide (`HOW-TO-USE-THIS.md`) which inherits structure from this doc but is tuned for the non-technical-founder audience.
- The "first 30 minutes" cold-start walkthrough is no longer needed here — it lives inside the skill's Phase 1 install flow and `HOW-TO-USE-THIS.md`.
- Cron specifications were dropped in the SHAPE reframe (manual lint only). See decision #5 in the brief.

This guide remains useful as: (a) onboarding material for new collaborators joining our internal setup, (b) the reference text future updates to the skill draw from, (c) a snapshot of the canonical CKB shape circa June 2026.
