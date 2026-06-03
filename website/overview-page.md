# Overview page — `absolutionlabs.com/obsidian`

The canonical website surface for the Obsidian Company Memory skill. Story-led overview at the top; "get the skill" link to GitHub at the end. The actual download, install instructions, troubleshooting, and user guides all live in the GitHub repo — this page is the front door, not the bundle.

**Render this in whatever the Absolution Labs website stack supports** (Netlify + markdown, Hugo, Astro, plain HTML — agnostic). The copy below is canonical; the structure is a brief.

**Replaces:** [install-page.md](install-page.md) as the front-of-house surface. The dual install-buttons hero shape in install-page.md was an earlier draft; this page is the agreed shape from 2026-06-03 onward — overview leads, install link sits at the bottom.

---

## Page structure (top to bottom)

### 1. Hero block (above the fold)

**Headline (H1):**
> Obsidian Company Memory

**Subhead (one paragraph, calm, AL-tone):**
> A control system for AI-assisted company memory. Not a template. Built from the same patterns we use to run our own client engagements at Absolution Labs — bespoke rulebooks and prompts engineered for reliability across hundreds of AI sessions. Installs on your machine in about 25 minutes. Free. MIT-licensed. Yours after install.

**One CTA below the subhead:**
> [Watch the 7-minute guided install ↓](#loom)

No install buttons above the fold. Buttons live at the bottom, after the viewer has read what they're installing.

---

### 2. Loom video block (anchor `#loom`)

Single embedded Loom, autoplay off, captioned. Embed snippet in [loom-embed-snippet.md](loom-embed-snippet.md).

Above the embed, one line of body copy:
> A walkthrough by Rob — sixty-second "is this for you" qualifier, then the install end-to-end, then the round-trip test that proves it worked. Worth watching before you install if you're in a regulated sector.

---

### 3. What it is (single section, ~250 words, no marketing-speak)

H2: **What it is**

> Obsidian Company Memory is a folder layout and a set of prompts that turn your Obsidian vault into a working memory layer for AI sessions. Every session reads the same rulebook before doing any work. Every piece of knowledge that lands in the vault has structured metadata at the top and at least one link to another piece of knowledge. Every session ends by appending one line to an audit trail.
>
> What you're installing is not a content pack. It's a control system. The folder structure you'll see in your file manager is the rendering layer — what actually does the work is the schema document at the vault root, the company context document the AI reads at session start, the operating principles that govern how the AI behaves, and the prompt files for the two custom skills you'll build inside your AI tool after install.
>
> Once installed, you point your AI assistant — Cowork, Claude Code, Codex, opencode, anything that reads `CLAUDE.md` or `AGENTS.md` — at the vault folder. The AI follows the procedure. Your knowledge accumulates as a by-product of normal work, not as a wiki you maintain on the side.
>
> No login. No account creation. No subscription. **No telemetry** — the skill does not phone home at install time or afterwards. The vault is yours, on your disk, plain markdown, no vendor lock-in.

---

### 4. How we built it (~200 words — AL methodology surface)

H2: **How we built it**

> Same methodology we apply on paid client engagements. The build ran through fourteen working sessions in early June 2026 against our internal project framework — the *Forge Method* — which forces every project through five phases: SHAPE (define what we're not building), BUILD (ship the smallest thing), CONFIRM (prove it works), SUSTAIN (evaluate whether it's earning its keep), and TEACH (extract the patterns worth keeping).
>
> The shape phase produced eighteen explicit decisions about what this skill would NOT do — no multi-client vault layouts, no plugin bundles, no first-project scaffolding, no scheduled lint, no auto-update warnings. Each cut sharpens what the skill IS for.
>
> The threat-modelling phase covered six surfaces — secrets, privacy and data, prompt injection, attack surface, backup and rollback, and external platform configuration. Every surface has an answer recorded; none were left blank.
>
> The build phase produced the skill itself, a manifest mirror contract, and a pre-release lint that runs against every commit. The confirm phase pre-mortemed the entire pipeline and put adversarial sub-agents through it before considering it ready to ship.
>
> The work is open. The skill, templates, manifests, lint, companion skills, compatibility matrix, and full disclaimer set all live in the GitHub repo. We hold the internal project brief — design rationale, threat model, decisions log — privately, and share specifics on written request.

---

### 5. What it was based on (~250 words — the substrate)

H2: **What it was based on**

> Three substrates underpin the design.
>
> **The Absolution Labs Client Knowledge Base.** Our own internal wiki uses this exact shape — a SCHEMA document at the root that governs Ingest, Query, and Lint operations; a per-client routing layer; an audit trail spanning hundreds of sessions across multiple clients. The skill ships the single-company variant of that shape, with the multi-client routing layer cut for simplicity. We are not asking you to use a pattern we don't use ourselves.
>
> **A research pass on long-running AI memory systems.** Before SHAPE phase, we ran a multi-agent research swarm against the public literature on AI memory — the limitations of context windows, the failure modes of retrieval-augmented generation, the success patterns of Zettelkasten and PARA and other knowledge-management methodologies, the specific shape of what Anthropic and OpenAI document about session continuity. Most of what we found is published as separate concept pages in our knowledge base; the design choices here trace back to that research. The skill is not improvised.
>
> **Our own operating principles.** Twenty-four cross-cutting principles for working with AI assistants that have been built up from real incidents across our engagements — handling secrets, structuring delegation, preserving audit trails, avoiding partial-failure shapes, calibrating evaluation cadence to build velocity, and many more. Five of those principles ship as a starter set inside every vault the skill scaffolds. You extend the list as your team learns its own lessons.

---

### 6. How it helps us (~180 words — honesty about our incentive)

H2: **How it helps us**

> We use this pattern internally on every project we run. The skill is the same shape, packaged as a one-shot install for anyone who wants it. Two specific things help us when we ship this externally.
>
> First — the skill is a trust artefact. People we'd like to do paid work with often ask "what do you actually ship?" before they take a call. The skill, sitting publicly on GitHub with a guided-install Loom and a written threat model, is the answer. If you install it, see it work, and find it valuable, that's a clearer signal of fit than any sales conversation.
>
> Second — it lowers the cost of every future engagement. When a paying client is already operating an Obsidian vault of this shape, the first month of any project we run with them is faster. Less setup, less convention drift, less explaining how we work. The skill doesn't have to land in front of paying clients to earn its place — but when it does, the engagement that follows is better.
>
> No upsell embedded. No "premium tier." This is what we ship.

---

### 7. Who it's for (and who it isn't) (~200 words)

H2: **Who it's for**

Two columns side-by-side (stacked on mobile):

**Left — Built for:**
- Founders and small-team operators who already use an AI assistant and want its outputs to accumulate as durable company knowledge
- Teams of 2–50 staff, especially in regulated sectors (drinks, FMCG, professional services, healthcare adjacencies)
- Operators who've felt the pain of "what did we decide about that customer last March" and not being able to find it
- Consultancies running structured engagements with the same client across time

**Right — Not built for:**
- Personal note-taking or Zettelkasten use (you don't need a SCHEMA imposing a structure)
- Multi-client agencies wanting one vault with twenty client folders inside (different shape — [email us](mailto:info@absolutionlabs.com), we'll point you)
- Anyone who doesn't use an AI assistant at all (half the value here is AI follow-through across sessions)
- Anyone whose existing notes setup is working well enough — the migration cost is real

Below the two columns, one line:
> If you're not sure, watch the Loom first. Sixty seconds in, the qualifier will tell you whether to keep watching.

---

### 8. Get the skill (the only install CTA on the page)

H2: **Get the skill**

> The skill, the install instructions for each agent CLI, the troubleshooting guide, the FAQ, the manual install path, the customisation guide, the upgrade procedure, and the full source live on GitHub.
>
> Free. MIT-licensed. Forkable. Fork-friendly variants are encouraged — just rename them so they're not confused with the Absolution Labs original.

**Primary CTA button, large, single:**

> **Get it on GitHub →** `github.com/absolutionlabs/obsidian-company-memory`

**Below the button, three small text-links (no other CTAs above this fold):**

- [Install instructions](https://github.com/absolutionlabs/obsidian-company-memory#install)
- [Compatibility matrix](https://github.com/absolutionlabs/obsidian-company-memory/blob/main/COMPATIBILITY.md)
- [Disclaimers + caveats](https://github.com/absolutionlabs/obsidian-company-memory/blob/main/DISCLAIMERS.md)

---

### 9. Privacy summary (single short paragraph)

H2: **Privacy in one paragraph**

> The skill writes to your local folder via your AI assistant's mounted-directory access. **Nothing flows back to Absolution Labs at any point** — no install ping, no health check, no usage data, no error reports. The skill does not phone home at install time or afterwards. Your vault contents have never reached our infrastructure in any version. Earlier releases (v1.0.0 / v1.1.0) shipped a 9-field anonymous opt-out install ping; we removed it entirely in v1.2.0 because the value to us was structurally near-zero and the trust framing didn't earn the compliance overhead.

---

### 10. About + footer (compact)

Two columns:

**Left — About this skill:**
> Built by Absolution Labs because the same shape of company memory underpins every project we run with our own clients. We'd rather more companies have access to it than gate it behind a sales conversation.

**Right — Support:**
> One email address, replied to within one business day by a human:
> **info@absolutionlabs.com**

Below both columns, the Companies Act 2006 trading-disclosure line (mandatory on this page per [[entities/absolutionlabs-ltd]] § Trading-Disclosure Compliance):

> © 2026 Absolution Labs. AbsolutionLabs Ltd, registered in England and Wales (Company No. 17091663). Registered office: 15 Westbury Road, London, SE20 7QL.

---

## Style direction

- **Tone matches the Loom + the README**: calm, sales-tool-grade, no hype, no "revolutionary," no "game-changer," no exclamation marks anywhere.
- **No em dashes.** Per the operator style preference. Use commas, periods, colons, parens, semicolons, or pipes.
- **Typography:** same family as the rest of `absolutionlabs.com`. If unsettled: serif body (Charter, Source Serif), sans display (Inter, Söhne).
- **Colour:** mostly Abso Labs brand. The "Get it on GitHub" button is the only saturated colour on the page above its fold.
- **No autoplay video.** No exit-intent popup. No cookie banner unless GDPR-required by your tracking choices.
- **No social login.** No email gate. No newsletter capture on this page.
- **Two-column blocks (sections 7 and 10) stack vertically on mobile.** Loom embed scales 100% width, 16:9.

---

## Why this shape vs the previous install-page.md draft

The previous draft put install buttons above the fold. That was the right call for a "you already know what this is, here's the URL" audience. It's the wrong call for the actual audience: regulated-sector founders who haven't seen the skill before, are at most lukewarm about AI tooling, and want to read what we shipped before clicking anything.

The new shape: ten sections, story-led, single install CTA near the bottom after the viewer has read the qualifier, the methodology, the substrate, and the honesty-about-our-incentive paragraph. Conversion will be lower per-visitor by design; conversion-quality will be higher because anyone clicking through has self-selected through the qualifier.

---

## Analytics

Track only what you need to decide whether to keep this surface alive:

- Page view count
- Scroll depth (how many viewers reach section 8 / the GitHub CTA)
- Loom play rate and completion rate
- GitHub CTA click rate
- Bounce rate

Use Netlify's built-in analytics or Plausible. **Don't add Google Analytics, Hotjar, or anything that needs a cookie banner** — the privacy framing on the page would be undercut by the tracker stack.

---

## When to revise

Revise this page when:

- A new minor version of the skill ships (update version-related copy, refresh Loom embed if re-recorded)
- The GitHub repo URL changes (update the section-8 CTA + side-links)
- The Loom is re-recorded (update the embed snippet)
- A material privacy or compliance change lands (update privacy summary verbatim from policy)
- The Companies Act trading-disclosure line changes upstream (e.g. registered office moves)

Revise on the same cadence the bundle releases — they're paired surfaces.

---

*Render this in whatever stack absolutionlabs.com runs on. The structure here is the canonical brief. Cross-references: [install-page.md](install-page.md) (superseded shape, kept for history), [resources-page-card.md](resources-page-card.md), [loom-embed-snippet.md](loom-embed-snippet.md), [website/README.md](README.md), and the bundle's [README.md](../README.md) + [DISCLAIMERS.md](../DISCLAIMERS.md).*
