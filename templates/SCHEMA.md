# {{COMPANY_NAME}} — Vault Schema

The rulebook for this vault. Every AI session reads this file before doing anything else. Changing the rules means changing this file.

## 1. Architecture

The vault has three layers.

**Layer 1 — Raw.** Source documents you didn't write. Transcripts, articles, PDFs, contracts, intake forms. They live in `raw/` and are **never edited**. If a transcript has a typo, the typo stays. Corrections go in a wiki page that points back to the raw file. The raw layer is the audit trail.

**Layer 2 — Wiki.** The notes you (or the AI) write. One page per thing worth remembering: a person, a tool, a product, a decision, a pricing rule, a brand fact. Pages live in `entities/`, `concepts/`, `comparisons/`, and `queries/`. Every page has YAML frontmatter and at least one `[[wikilink]]` to another page.

**Layer 3 — Schema.** Three files govern how the vault operates: `SCHEMA.md` (this rulebook), `index.md` (table of contents), and `log.md` (audit trail of changes). Sessions read SCHEMA at start; the index is the lookup table; the log is the history.

## 2. Page format

Every wiki page uses this YAML frontmatter:

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

- `title` — human-readable page title
- `created` — date first written; never changes
- `updated` — date of last modification; must change on every edit
- `type` — one of: `entity` (a thing), `concept` (an idea), `comparison` (side-by-side analysis), `query` (synthesised answer)
- `tags` — freeform list for discovery; no controlled vocabulary
- `sources` — paths to raw files this page draws from; empty list if from session work

## 3. The three operations

### Ingest

How knowledge enters the vault. Every session that produces meaningful knowledge runs at least one Ingest before closing.

1. Capture raw source into `raw/` if the knowledge comes from an external document, transcript, or article. Skip if knowledge comes from session work.
2. Decide whether an existing page covers the topic. Update it, or create a new page.
3. Write or update wiki pages with frontmatter and at least one `[[wikilink]]`.
4. Update `index.md` — add a one-line entry for every new page.
5. Append `log.md` — one entry describing what was ingested and why.
6. Report what changed.

### Query

How knowledge is retrieved.

1. Read `index.md` to find relevant pages.
2. Read the relevant pages.
3. Synthesise an answer with citations.
4. If the answer is substantial and reusable, file it as a new page in `queries/`.
5. Append `log.md` if a new page was filed.

### Lint

How the vault stays healthy. Run on demand: ask the AI to "run a lint on the vault." Output goes to `lint-reports/YYYY-MM-DD.md`.

1. Scan for contradictions — two pages disagreeing on the same fact. Flag with file paths.
2. Find orphan pages — pages with no inbound `[[wikilinks]]`. Every page must be reachable.
3. Check for stale content — `updated` date older than thresholds in `_meta/expectations.yml`.
4. Identify data gaps — `[[wikilinks]]` pointing to pages that don't exist yet.
5. Verify index completeness — every page on disk appears in `index.md`.
6. Check CONTEXT freshness — flag if `CONTEXT.md` is older than the threshold in `_meta/expectations.yml`.
7. Report findings with file paths and recommended actions.
8. Append `log.md`.

## 4. File conventions

- **Filenames:** lowercase, hyphens, no spaces (e.g. `klaviyo-integration.md`).
- **Frontmatter:** every page has it, no exceptions.
- **Wikilinks:** every page links to at least one other page; orphans are invisible.
- **Updated date:** must change on every modification.
- **Raw files:** never modified; corrections go in wiki pages that link back.
- **Index:** every new page added to `index.md` in the same session.
- **All files live inside this vault folder.** No session creates files outside.

## 5. Close procedure

Every session ends with `/close` (or `/close-full` if the user has that skill installed). The protocol:

1. Update the project brief if one exists.
2. Verify at least one Ingest ran this session. If not, the session must record why (in `log.md`) before closing.
3. Append `log.md` with a one-line entry: what was ingested, what was queried, brief status.
4. Report KB writes: every file touched this session, what kind of touch (created / appended / modified), one-line reason.

A close without an Ingest, log entry, or KB Writes Report is a protocol violation. Sessions should fix this in the same session — never defer to next time.

## 6. The trust rule

**The user is always right over the wiki.** If the user says a wiki page is wrong, the wiki page is wrong — update it, don't argue. The wiki is a record of what was true at a given point; the user's current knowledge supersedes it.

This rule exists because the AI cannot fact-check the wiki against reality. The user can. Pages drift, decisions change, suppliers go out of business. When the user contradicts the wiki, that's signal — capture the correction immediately.

## 7. Changing the rules

This file is the rulebook. Editing it changes how every future session operates. Don't edit casually. If you find yourself wanting to bend a rule, ask: is this rule wrong, or is this one situation an exception?

- If the rule is wrong: edit the rule, commit the change, the new rule applies from now on.
- If the situation is an exception: leave the rule alone, document the exception in the relevant page's Notes section.

---

*This schema ships with the Obsidian Company Memory skill by Absolution Labs LTD. The canonical reference for how Absolution Labs LTD's own vault works lives in their Client Knowledge Base. This single-company variant strips the multi-client routing layer. You can modify this file freely to suit your company's needs.*
