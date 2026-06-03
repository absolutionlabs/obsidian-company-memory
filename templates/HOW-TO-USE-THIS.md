---
title: How to use this vault
created: {{TODAY}}
updated: {{TODAY}}
type: concept
tags: [guide, ongoing-use, phase-2]
---

# How to use this vault

*Read once after install. Revisit any time you need a reminder. ~10-minute read.*

This is the Phase 2 living guide for the {{COMPANY_NAME}} vault. The install skill set up the vault and verified it works. From here on, **this doc is your reference for everything that happens during ongoing use** — the weekly lint habit, the close-session protocol, what to do when something breaks, when to update what.

The vault is yours. You can edit this guide as you learn things; you can ignore parts you don't need; you can add sections that make sense for your company. It lives in your vault root so you'll see it in Obsidian's file explorer.

---

## The basic loop

You sit down to work. You open an AI session (Cowork, Claude Code, Codex, opencode — whichever you use). You describe today's task. The AI mounts the vault, reads `SCHEMA.md` and `CONTEXT.md` to refresh its rules, and does the work.

As facts surface during the session ("the supplier's lead time is 6 weeks," "we decided to drop the smaller SKU"), the AI proposes wiki updates inline. You confirm or correct. The page gets written immediately; the `updated:` date changes; `index.md` gets a new entry; `log.md` gets a session entry.

At the end of the session, you type `/close-full` (or just "let's close out"). The AI runs the close protocol, writes the audit-trail entry, and gives you a prompt for next time.

That's the whole loop. You don't curate the vault; the vault grows as a by-product.

---

## The weekly lint habit

Every week (or at the start of any serious working session) ask the AI to run a lint on the vault:

> "Run a lint on the vault. Check for orphans, broken links, stale pages, and missing frontmatter. Write the report to `lint-reports/`."

The AI walks the vault, applies the checks defined in `SCHEMA.md`, and writes `lint-reports/YYYY-MM-DD.md`. Open that file in Obsidian, spend 5 minutes acting on anything flagged, move on.

What lint catches:

- **Orphan pages** — pages with no incoming `[[wikilinks]]`. They're invisible to graph view and to the AI's lookup; effectively lost. Fix by adding a link from a related page.
- **Broken wikilinks** — `[[references]]` pointing at pages that don't exist. Either create the page, or remove the link.
- **Stale pages** — pages whose `updated:` date is older than the thresholds in `_meta/expectations.yml` (default: 90 days for most types, 30 days for `CONTEXT.md`). Review and update, or accept that they're historical.
- **Missing frontmatter** — pages without the required YAML header. Add one.
- **Index drift** — pages on disk that aren't in `index.md`. Add the missing entries.

Most weeks the report is short. The weeks it's long are the ones that needed attention.

---

## Capturing knowledge mid-session

The default behaviour is "the AI captures knowledge at close." But for important moments, capture immediately:

> "Ingest that into the vault now — I don't want to forget."

The AI runs the Ingest operation (defined in `SCHEMA.md`): writes or updates the relevant page, updates `index.md`, appends `log.md`. Takes 30 seconds.

Good moments to force an Ingest mid-session:

- A decision was made (capture the rationale, not just the outcome).
- A price changed, a supplier's terms shifted, a brand rule was clarified.
- The AI surfaced a fact you didn't realise you knew.
- Someone said something on a call that you want to keep.

Bad moments to force an Ingest:

- "We might do X, not sure yet." — captures uncertainty as certainty; wait until decided.
- Speculation, brainstorm output, half-formed ideas. — these go in a working doc, not the vault.

---

## The close-session protocol

Every session ends with `/close-full` (or "let's close out, run the close protocol"). The AI:

1. Updates any project brief if one exists.
2. Verifies at least one Ingest ran this session. If not, asks why.
3. Appends `log.md` with what happened.
4. Reports KB writes: every file touched, type of touch, one-line reason.
5. Generates a continuation prompt for next session.

The whole thing takes about 30 seconds. Skipping it leaves the session's decisions in your head but not on disk — the exact failure mode that vaults rot from.

Even a 5-minute session ends with a close. The discipline is the point.

---

## When `_summary.md` drifts (if you've added one)

The starter scaffold doesn't include a rolling summary file — they're useful but optional. If you add one (e.g. `_summary.md` at the vault root), it tends to drift from the underlying pages over time.

When you notice that drift, ask the AI:

> "Rebuild `_summary.md` from scratch by reading `index.md` and the recently-updated pages."

The AI re-reads the canonical sources and produces a fresh summary. Drift resolved.

---

## Adding pages by hand (without the AI)

You can create pages in Obsidian directly. The starter scaffold includes three templates in `_meta/templates/` — copy one, paste at the right path, fill in the frontmatter and content, save.

After you create a hand-edited page, either:

- Add a one-line entry to `index.md` yourself, or
- Ask the AI in the next session: "I added a page at [path]. Update the index and log it."

Either works. The vault doesn't care who made the change as long as the index stays in sync.

---

## Updating `CONTEXT.md`

`CONTEXT.md` tells every session what the company IS. When a major fact about the company changes — new product line, new ICP, new pricing tier, leadership change — update `CONTEXT.md` in the same session. Then ask the AI:

> "I just updated CONTEXT.md. Scan the wiki for pages that reference the old [fact] and flag them for review."

This catches stale references that would otherwise contradict the new context. The AI surfaces them; you decide what to do.

The `updated:` date on `CONTEXT.md` is tracked by the lint — if it gets older than 30 days, the lint flags it for a refresh review.

---

## Backup hygiene

Your cloud sync (Dropbox, iCloud, OneDrive, whichever you chose) is the primary backup. It gives you version history and off-machine resilience.

For belt-and-braces, quarterly: zip the whole vault folder and save it somewhere else (a thumb drive, a different cloud account, an attachment to an email to yourself). The vault is just markdown — the zip is tiny.

If you want git-level version history on top, you can initialise a git repo inside the vault and commit regularly. Most users don't need this; cloud sync's version history covers the same use cases.

---

## Common failures and recovery

**Two pages contradict each other.**
Trust the more recent one. Update both so they agree. Append a note to `log.md` recording the resolution.

**Your cloud sync created a "conflicted copy" file.**
Open both versions, manually merge the content, delete the conflict file. Tell the AI in the next session: "I resolved a Dropbox conflict — log it."

**The AI wrote something wrong to the vault.**
Fix the page directly. Run a lint to see if it cascaded anywhere. Move on. The system is designed to be edited by you.

**You accidentally edited `SCHEMA.md` and don't like the result.**
Restore from cloud sync version history. Or copy the original from the skill's templates folder if you've kept it.

**A page got deleted by accident.**
Cloud sync recovery. Or check `log.md` for when the page was last written and use that to reconstruct.

**Obsidian shows broken links everywhere after a folder rename.**
You moved or renamed a folder without Obsidian's "update links" feature. Either undo the move, or use Find-and-Replace in Obsidian to fix the link paths.

**The vault feels overwhelming and you don't know where to start.**
Open `index.md`. That's the map. Read the top few sections to orient yourself. Or ask the AI: "Summarise the current state of the vault in five sentences."

---

## When to consider going further

This is Phase 1 of the system — vault scaffold, manual lint, daily-loop discipline. That's enough for most companies indefinitely.

If you find yourself wanting more — scheduled lint at 8am every day, daily / weekly / monthly audit reports, an AI worker that consolidates the wiki in the background — that's Shape 2 territory. Not currently shipping. If demand emerges, Absolution Labs LTD will add it.

For now: the manual rhythm above is the system. Use it consistently for 30 days and you'll have a vault that's genuinely useful. Skip the discipline and the vault rots into noise.

---

## About the publisher

This vault was scaffolded by the Obsidian Company Memory skill, distributed free by Absolution Labs LTD. Absolution Labs LTD has no access to your vault contents at any point: the skill writes to your local folder via your chosen AI agent's mounted-directory access; nothing flows back. If you opted in to telemetry, the only data Absolution Labs LTD receives is anonymous install + success pings (no PII, no vault contents, no company name) — see the privacy policy at absolutionlabs.com for details.

For support: email [info@absolutionlabs.com](mailto:info@absolutionlabs.com). Response within 1 business day.

For the daily/weekly habits not covered above, ask your AI assistant directly — most of what works is naturally surfaced through use.
