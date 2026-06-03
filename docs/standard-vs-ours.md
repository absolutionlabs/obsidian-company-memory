# Standard Obsidian + AI setups vs Obsidian Company Memory

Diff between common ways people use Obsidian alongside an AI assistant, and what this bundle ships. The point is not "ours is better" — it's "they're solving different problems; here is which one fits which need."

If you're trying to decide whether to install this skill or build your own pattern, this is the document for you.

---

## What "standard" means here

There is no single standard. Across blogs, YouTube tutorials, and the Obsidian + Claude / Obsidian + ChatGPT community, four patterns recur:

### Pattern 1 — Plain notes + manual AI prompts

You have an Obsidian vault you've used for a while. You ask Claude or ChatGPT a question by pasting context manually each time: *"Here's my notes on Customer X (paste). What's the next step?"* The AI helps; nothing is written back to the vault. No structure, no audit trail, no continuity across sessions.

**Most common shape.** Solo operators, founders, knowledge-workers who treat Obsidian as a private second brain and the AI as a search/synthesis bolt-on.

### Pattern 2 — Vault + Smart Connections (or similar plugin)

The Smart Connections community plugin embeds your vault's notes and surfaces related ones to a chat window inside Obsidian, backed by OpenAI / Claude / Gemini under the hood. You ask questions; it retrieves related notes; the AI synthesises an answer. Output usually stays in the chat — not written back as new notes.

**Solid pattern for question-answering.** Less useful for capturing new knowledge into the vault.

### Pattern 3 — Vault + Templater + custom scripts

You set up Templater with prompts that pre-fill new pages (meeting notes, daily journals, project briefs). The AI may or may not be in the loop; if it is, you usually copy AI output into the templated structure manually. Some power users build sophisticated scripts; most stop at 2-3 templates.

**Strong for personal-productivity discipline.** Higher initial setup cost; payoff scales with how much you ritualise your workflow.

### Pattern 4 — Vault + Claude Code / Cursor pointed at the folder

A developer-flavoured pattern. You `cd` into your vault folder, fire Claude Code, and ask it to make changes. The AI reads markdown, writes markdown, leaves the rest of the vault alone. No structure imposed; whatever convention you've built is what the AI follows (or doesn't, depending on session length and how clearly your conventions are encoded).

**Increasingly common.** Hits a wall when sessions don't carry forward — the next session starts cold and you re-explain your conventions, or it ignores them.

---

## What this bundle ships

A scaffolded vault with five things bolted in by design:

1. **A schema.** `SCHEMA.md` at the vault root names the three operations (Ingest / Query / Lint), defines the page format (YAML frontmatter, wikilinks), and lays out file conventions. Every AI session reads it first.
2. **A company context.** `CONTEXT.md` tells the AI what your company does, who its customers are, what its constraints are. The first thing it reads after SCHEMA.
3. **An index.** `index.md` is the lookup table. Every page on disk appears here. AI consults it to find what exists before deciding to write something new.
4. **An audit trail.** `log.md` records every Ingest, Query, and close-obsidian-project event with a date and a one-liner. Future you reads it to understand why your past self made certain calls.
5. **An operating-principles starter.** `concepts/claude-operating-principles.md` ships with 5 principles tailored to AI-assisted work; you extend over time as your team learns what to repeat and what to stop.

Plus: a procedural skill that scaffolds it in ~5 minutes, a 5-step round-trip test that verifies the system works end-to-end, an idempotency contract that refuses partial scaffolds, a compliance gate at install time, no telemetry (the skill does not phone home), and two companion skills (`open-obsidian-project` for starting projects, `close-obsidian-project` for ending sessions cleanly) that auto-install alongside the main install skill.

---

## Side-by-side comparison

| Dimension | Plain notes + AI | Smart Connections | Templater + scripts | Code/Cursor + vault | **This bundle** |
|---|---|---|---|---|---|
| Vault structure | Whatever you have | Whatever you have | Whatever you have | Whatever you have | **Scaffolded** — entities, concepts, comparisons, queries, raw, lint-reports, _meta |
| Schema document | None | None | None | None | **SCHEMA.md** — the rulebook every session reads |
| Page format | Ad-hoc | Ad-hoc | Per-template | Ad-hoc | **YAML frontmatter required**; wikilink required |
| Index / lookup | None or hand-curated | Plugin-managed embedding index | None | None | **index.md** — every page listed; lint enforces it |
| Audit trail | None | Chat history (lost on session end) | None | Git, if you set it up | **log.md** — every operation logged |
| AI session-start protocol | None | None | None | Whatever you tell it inline | **Reads SCHEMA + CONTEXT first**, every session |
| New-knowledge capture | Manual copy-paste | Output stays in chat | User fills templates | Whatever AI decides | **Ingest operation** — defined, repeatable, audited |
| Knowledge retrieval | Search + paste | Embedded-vector retrieval | Templater queries | File reads | **Query operation** — synthesised from index + pages; logged |
| Drift detection | None | None | None | None | **Lint operation** — 5 checks; manual invocation; report to disk |
| Continuity across sessions | None (cold start each time) | None (chat resets) | None | Weak (depends on session memory) | **High** — vault state is the memory; session reads it at start |
| AI follow-through on conventions | Low | Low (conventions not formalised) | Medium | Medium-low | **High** — conventions are documents the AI reads |
| Setup time | 0 (already have a vault) | ~10 min (plugin install + config) | 30-90 min (templates + scripts) | ~5 min (cd into folder) | **~25 min** (skill-driven, includes Obsidian basics) |
| Setup risk | None | Plugin config drift | Templater syntax debug | None | **Compliance gate + refuse-on-non-empty** prevents data loss |
| Multi-AI-tool support | Manual per-tool | Plugin-tied (Obsidian only) | Manual per-tool | Code/Cursor mostly | **CLAUDE.md + AGENTS.md** — works with any agent CLI that reads them |
| Telemetry / observability | None | Plugin-specific | None | None | **Opt-out, 9 anonymous fields** for install-failure detection |
| Recovery from failure | Manual (your backups) | Manual | Manual | Manual | **Cloud sync versioning + lint + scaffold-version.txt + DSAR + documented recovery drill** |
| Customisability | Total (it's your vault) | Plugin-scoped | Full (your templates) | Total | **Fork-friendly** — MIT, customisation.md guide; canonical schema with operator opt-outs |
| Vendor lock-in | None | Plugin-only | Templater-tied | None | **None** — plain markdown; uninstall = no impact on vault |

---

## Where the standard patterns are right (and ours is overkill)

### You should NOT install this bundle if:

- **You're a solo operator with a personal note vault.** You don't need an audit trail, an index, or a lint cycle. The scaffolded structure is overhead. Pattern 1 (plain notes + AI) is right for you.
- **You're using Obsidian primarily for personal knowledge management (Zettelkasten, second brain).** This bundle is shaped for company memory — facts and decisions about an organisation. Personal Zettelkasten has different conventions and you don't need a SCHEMA imposing ours.
- **You already have a working pattern that compounds.** If you've built Templater + scripts that you actively use and your team understands, the cost of migration is real and the benefit (formal SCHEMA, lint, audit trail) may not be worth it. Keep what you have.
- **You don't use an AI assistant.** The bundle is shaped around AI follow-through (CLAUDE.md, session-start protocol, AI-driven operations). Without an AI in the loop, half the value disappears.
- **Your vault has client / regulated data already in it.** The refuse-on-non-empty gate blocks installation. By design.

### Where standard patterns are particularly strong:

| Pattern | Strength | Our weakness on this axis |
|---|---|---|
| Plain notes + AI | Zero overhead; works immediately | We require ~25 min install + ongoing discipline |
| Smart Connections | Best-in-class question-answering against existing notes | We don't do embedding-based retrieval (we use structured wikilink + index) |
| Templater + scripts | Personal-productivity ritual building | We focus on AI-assisted operations, not human-typed rituals |
| Code/Cursor + vault | Lowest friction for technical users | We add the schema layer; some users find that constraining |

---

## Where this bundle is right (and the standard patterns leave gaps)

### You SHOULD install this bundle if:

- **You're building company memory** — facts and decisions about an organisation, intended to outlive any single session, person, or AI conversation.
- **You use an AI assistant** and find it forgets / repeats / drifts across sessions. The SCHEMA + CONTEXT + index + log loop fixes that by giving the AI a stable document to anchor on.
- **You have a team** (even of 2) and want shared conventions an AI can enforce. SCHEMA.md is the contract; the lint catches violations.
- **You've felt the pain of "what did we decide about X" not being findable.** The audit trail in `log.md` plus the index is precisely shaped for that.
- **You want explicit decision-trace.** Every Ingest is logged. Future you (or a future AI session, or a teammate) can read the log and understand why the vault grew the way it did.
- **Regulated-sector context.** The compliance gate at install plus a no-telemetry posture (the skill does not phone home in any version from v1.2.0 onward) covers the basics. Your own legal and regulatory due diligence still applies — the skill cannot substitute for it. Most standard patterns leave this surface entirely to you, with no compliance prompt at install time.
- **You're a consultancy / agency working with multiple clients.** The bundle ships single-company; for multi-client, the Absolution Labs Client Knowledge Base shape is the right derivative (same underlying schema, with `clients/<slug>/` routing).
- **You want recovery to be obvious if anything breaks.** The vault is plain markdown; cloud sync gives versioning; the Recovery Drill is documented; uninstalling the skill has zero impact on your vault.

### Where this bundle particularly shines:

| Failure mode of standard patterns | How this bundle addresses it |
|---|---|
| AI forgets your conventions across sessions | SCHEMA + CONTEXT + session-start protocol = AI re-reads them every time |
| New knowledge gets lost in chat | Ingest is a defined operation; output is a wiki page; logged in `log.md` |
| You can't find what you wrote 3 months ago | index.md is the lookup; wikilinks make navigation cheap; lint catches index drift |
| You can't tell what's stale | Lint check #3 (stale content) flags pages > 30 days old |
| Wikilinks point at pages that don't exist | Lint check #4 (data gaps) catches this every run |
| Two pages disagree | Lint check #1 (contradictions) flags conflicting claims |
| You can't audit what changed | log.md is the audit trail; one line per close-obsidian-project |
| You don't know if your install worked | Round-trip test verifies end-to-end; 5-step user confirmation |
| You install something that overwrites your work | Refuse-on-non-empty + worktree-refusal + skill-bundle integrity check |
| You can't tell compliance whether data leaves your machine | The vault never reaches our infra; opt-out telemetry has 9 anonymous fields disclosed at install |

---

## Migration paths

### Standard pattern → this bundle

Start a new empty folder. Install the skill. After scaffold, copy your existing notes into the appropriate scaffolded folders (`entities/`, `concepts/`, etc.). Add each copied page to `index.md`. Run a lint to catch the structural gaps. Adjust SCHEMA if your existing conventions differ — your vault, your call.

**Time:** ~25 min skill + ~30-60 min migrating notes + ~15 min cleanup lint.

### This bundle → leaner pattern

If you install this and decide it's too structured: keep the vault as a folder of markdown files; delete SCHEMA.md, index.md, log.md, and `_meta/`; uninstall the agent skill. What remains is just your markdown notes in `entities/`, `concepts/`, etc. — which you can rename or restructure however you like. Zero lock-in.

**Time:** ~5 min.

### This bundle → multi-client (consultancy / agency)

The single-company shape is permanent per key decision #4. For multi-client work, fork the bundle and add a `clients/<slug>/` routing layer following the Absolution Labs Client Knowledge Base pattern. That fork is not maintained by us; it's an operator-side decision with operator-side support.

**Time:** half-day fork + ongoing maintenance.

### This bundle → Obsidian Publish public site

The vault is markdown; Obsidian Publish reads markdown. Mechanically you can publish. Strategically: most company memory should NOT be public. If you do publish: at minimum, exclude `_meta/`, `log.md`, and any client-specific folders from the publish manifest.

**Time:** Obsidian Publish has its own setup; not covered here.

---

## What "best" depends on

| If your priority is... | Pattern that fits |
|---|---|
| Maximum simplicity, zero overhead | Plain notes + AI (Pattern 1) |
| Strong retrieval against existing notes | Smart Connections (Pattern 2) |
| Personal workflow ritual + structure | Templater + scripts (Pattern 3) |
| Developer-flavoured, vault-as-code | Code / Cursor + vault (Pattern 4) |
| Company memory + AI continuity + audit trail | **This bundle** |
| Compliance posture for regulated sector | **This bundle** |
| Multi-client agency work | **This bundle, forked + multi-client layer** |
| Pure personal knowledge management | Plain notes or Smart Connections |

None of these are wrong. They're shaped for different problems. The reason this bundle exists is the company-memory + AI-assisted-work intersection wasn't well-served by the others — and the trust artefact of "Absolution Labs ships polished, working, secure tools" needed the install moment to be high-quality.

---

## Open question: should this bundle's pattern be extracted as a general spec?

> *Operator-flagged 2026-06-03 as worth revisiting later. Not a decision yet; the question is staying open. See the project's session-persistent note for the inputs the decision will need when it gets picked up.*

There's an argument that the SCHEMA + CONTEXT + index + log + lint + AI-session-start-protocol shape is general enough to be specified independently of this bundle — call it the "Company Memory Pattern" or similar. Other tooling could implement it: Logseq variants, Notion variants, plain-folder variants without Obsidian.

We don't have plans to extract that spec. It would require maintaining a versioned standard separately from the bundle, and we don't currently have the bandwidth. If you want to write the spec yourself, the bundle's SCHEMA.md plus the procedural skill is enough to reverse-engineer it.

---

*Cross-references: [README.md](../README.md), [SKILL.md](../SKILL.md), [COMPATIBILITY.md](../COMPATIBILITY.md), [faq.md](faq.md), [customisation.md](customisation.md), [HOW-TO-USE-THIS.md](../templates/HOW-TO-USE-THIS.md).*

---

## Use at your own risk

This document is part of the Obsidian Company Memory bundle, provided "AS IS" without warranty of any kind under the MIT License. It is for general informational and educational purposes only and does not constitute professional advice. The comparisons above describe patterns we have observed; they are not endorsements of any third-party tool nor guarantees about the behaviour, security, or continued availability of any pattern described. **Read [DISCLAIMERS.md](../DISCLAIMERS.md) in full before relying on this comparison to make a tooling decision.**

*© 2026 Absolution Labs. AbsolutionLabs Ltd, registered in England and Wales (Company No. 17091663). Registered office: 15 Westbury Road, London SE20 7QL.*
