---
title: AI Operating Principles
created: {{TODAY}}
updated: {{TODAY}}
type: concept
tags: [principles, ai, sessions]
---

# AI Operating Principles

The cross-cutting rules for how the AI works with this vault. Every session reads this page during start-up. Update this page when the company accumulates a new working rule with the AI worth remembering.

This starter set has five principles. Add to it over time as the company learns from real incidents. Principles earned through experience are the ones worth keeping; principles invented in the abstract usually aren't.

---

## 1. Update records the same session, not the next one

When the AI finds a record that is stale and the fix is in hand today, fix it in this session. "I'll come back to that next time" is how information becomes fragmented.

**Why:** Memory compounds when capture happens at the moment of recognition. Deferral is drift.

**How to apply:** Notice a brief, page, or note that no longer matches reality? Update it now. Don't add it to a backlog. The 5 minutes it costs today saves 30 minutes of re-discovery later.

---

## 2. Preserve documentation by appending addendums, never rewriting

Plans, briefs, and reference pages get shaped across multiple sessions. The AI rarely has the full strategic picture in any single session. **Never rewrite or delete existing content** — append clearly-marked addendums so the original remains as one source of truth.

**Why:** What looks like outdated content was usually deliberate at the time it was written. Rewriting destroys the reasoning. Addendums preserve it.

**How to apply:** When asked to update a doc, default to **append** with a dated header (e.g. "## Addendum — 2026-06-02, scope reframe"). Only rewrite when the user explicitly says rewrite. The original survives.

---

## 3. The user is always right over the wiki

If the user says a wiki page is wrong, the wiki page is wrong. Update it; don't argue.

**Why:** The AI cannot fact-check the wiki against reality. The user can. Wikis drift; the user's current knowledge supersedes what was recorded six months ago.

**How to apply:** When the user contradicts a wiki page, capture the correction immediately. Update the page, append the change to `log.md`, move on. Don't try to reconcile the old page with the user's new statement — just believe the user.

---

## 4. Every page has frontmatter and at least one wikilink

Pages without frontmatter are unsearchable by tag or type. Pages without `[[wikilinks]]` are orphans — invisible to graph view, backlinks, and the AI's lookup. Both forms make the vault rot.

**Why:** The vault's value comes from connection. An isolated page is barely better than a note in a random text file.

**How to apply:** Every new page gets the SCHEMA-defined frontmatter block (title, created, updated, type, tags, sources) and at least one `[[wikilink]]` to another page. If no natural link exists, link to `[[CONTEXT]]` or `[[index]]` until a better one emerges.

---

## 5. Every session ends with an Ingest, or a logged reason it didn't

Sessions that close without writing anything to the vault produce no compounding value. If a session genuinely had no knowledge to capture (reading-only, navigation-only), the AI logs that explicitly in `log.md`. Silent closes erode the discipline.

**Why:** Most sessions DO produce capturable knowledge. The session that "had nothing to write" usually had several things — and lost them because nobody checked.

**How to apply:** At close, the AI lists everything created or modified. If the list is empty, the AI surfaces this explicitly: "No KB writes this session — confirm there was nothing worth capturing?" The user confirms or names the thing that should have been written.

---

## Adding your own principles

Over time, real sessions will produce moments worth capturing here. A few examples of how new principles tend to surface:

- The AI did something surprising and the user said "no, don't do that — we need to [...]". That's a principle.
- The AI hesitated where it should have acted, or acted where it should have hesitated. That's a principle.
- A particular shape of work kept needing the same correction across sessions. That's a principle.

When you add a new principle, follow the format above: a one-sentence rule, a "Why" paragraph, a "How to apply" paragraph. The format is load-bearing — it lets the AI reason about edge cases instead of mechanically following a rule.

---

*This starter set is shipped by the Obsidian Company Memory skill from Absolution Labs LTD. Absolution Labs LTD's own internal vault has 24 principles accumulated across many months — see [their canonical page](https://github.com/Absolution-Labs/) for inspiration once you've outgrown the 5 here.*
