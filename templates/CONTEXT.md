---
title: {{COMPANY_NAME}} — Vault Context
created: {{TODAY}}
updated: {{TODAY}}
type: entity
tags: [company, context]
---

# {{COMPANY_NAME}} — Vault Context

This is the long-term memory for {{COMPANY_NAME}}. Every AI session that mounts this vault reads `SCHEMA.md` first, then this file, before doing any work.

## What this vault is

A single, durable, human-readable record of facts, decisions, patterns, and context about {{COMPANY_NAME}}. It grows as a by-product of normal AI-assisted work: every session that produces meaningful knowledge writes it here at close.

The vault is **plain markdown files on disk** — no SaaS, no database, no lock-in. Portable to any markdown editor; backed up by the user's cloud sync; readable by humans and AI alike.

## About {{COMPANY_NAME}}

*Fill this section in during your first real session. Two to four paragraphs covering: what the company does, who its customers are, what's distinctive about it, and the immediate operational priorities.*

## Write rules for sessions

- **Single-company scope.** Everything in this vault is about {{COMPANY_NAME}}. There is no cross-client routing layer.
- **Read `SCHEMA.md` first.** It governs operations.
- **Update `index.md` and `log.md` whenever a wiki page is created or modified.** Same session, not later.
- **Trust the user over the wiki.** When the user contradicts a page, update the page.
- **Run an Ingest at close.** No silent closes.

## Where things live

- `entities/` — people, tools, products, suppliers, customers, anything that is a *thing*
- `concepts/` — ideas, patterns, methodologies, strategies
- `comparisons/` — side-by-side analyses (e.g. supplier A vs supplier B)
- `queries/` — synthesised answers to questions that took real work to compose
- `raw/` — source documents (articles, transcripts, PDFs, intake forms); never edited
- `lint-reports/` — output from the Lint operation
- `_meta/` — vault configuration (lint thresholds, page templates)
- `HOW-TO-USE-THIS.md` — the living guide for how to use this vault on an ongoing basis

## Operating Principles

The starter set lives at `concepts/claude-operating-principles.md`. Add to it as the company accumulates working rules with the AI. Principles earned through real incidents are the ones worth keeping.

## Branding and ownership

This vault is {{COMPANY_NAME}}'s. The skill that scaffolded it ships from Absolution Labs LTD. Absolution Labs LTD has no access to the vault contents — see [HOW-TO-USE-THIS.md](HOW-TO-USE-THIS.md) for the full data residency note.
