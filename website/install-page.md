# Install landing page — `absolutionlabs.com/obsidian`

The single canonical install surface. Drives prospects from "saw a link, considering it" → "installed and watched it work."

This file is the **copy + structure spec** for the page; render it in whatever your website stack supports (Netlify + markdown, Hugo, Astro, plain HTML — agnostic).

---

## Page structure (top to bottom)

### 1. Above-the-fold hero

**Headline** (H1):
> Obsidian Company Memory

**Subhead** (one line):
> A long-term memory for your company, scaffolded onto your machine in 25 minutes. Free. From Absolution Labs.

**Two install buttons, side by side:**

- **Cowork** — primary, large. Label: `Install in Cowork`. Click behaviour: copy install URL to clipboard + show a 3-step modal ("paste into Cowork plugin settings → approve → start session"). The install URL is the GitHub raw URL of `plugin.json` from the public repo.
- **Claude Code** — secondary, smaller. Label: `Install in Claude Code`. Click: open a modal with the `git clone` one-liner.

**Tertiary line below the buttons:**
> Don't have either tool? Just have Obsidian and a folder. [Watch the 7-min guided install first ↓](#loom)

---

### 2. Loom video block (anchor `#loom`)

Single embedded Loom, autoplay off, captioned. Embed snippet in [loom-embed-snippet.md](loom-embed-snippet.md).

Above the embed, one line of body copy:
> A walkthrough by Rob — what the skill installs, why it asks what it asks, and the round-trip test that proves it worked. Worth watching before you install if you're in a regulated sector.

---

### 3. "What it is" block (3 columns or 3 stacked cards on mobile)

| Card | Headline | Body |
|---|---|---|
| 1 | **Single-company vault** | One folder, one company, three layers: raw documents, structured wiki, schema rulebook. Same shape every AI session reads. |
| 2 | **Yours, on your machine** | Plain markdown files on your disk. Cloud sync via Dropbox / iCloud / OneDrive — your choice. We never see it. |
| 3 | **No lock-in** | MIT licensed. Fork it, modify it, distribute it. Your vault is portable to any markdown editor. |

---

### 4. "What gets installed" block

Show the same file-tree from the bundle's [README.md](../README.md) §"What gets installed". Use a monospace block. Don't shorten — the visible 20-file scaffold is part of the trust signal.

---

### 5. "What the skill does NOT install" block

Pull verbatim from the bundle's README. Eight bullet points; each one a deliberate cut with rationale. This block lands harder than the previous one for thoughtful prospects.

---

### 6. Privacy summary block

H2: **Privacy in one paragraph**

Body (verbatim from README):
> The skill writes to your local folder via your AI assistant's mounted-directory access. Nothing flows back to Absolution Labs at any point during normal use. The one exception: at install time, by default, one anonymous ping is sent to a Supabase database we operate in London. It contains a random UUID (not linked to your name, company, or vault contents), the skill version, your OS family, the install surface, the sync provider you confirmed, and whether the install succeeded or failed. No PII. You can opt out with one click at install time.

CTA below: **[Read the full privacy policy →](/privacy)**

---

### 7. Compatibility block

H2: **Tested on**

Tile grid:
- macOS 12+
- Windows 10/11
- Cowork
- Claude Code
- Codex + opencode (compatible)
- Dropbox / iCloud / OneDrive / Google Drive
- Obsidian 1.5+

Sub-line: [Full compatibility matrix →](https://github.com/absolutionlabs/obsidian-company-memory/blob/main/COMPATIBILITY.md)

---

### 8. About + support footer

Two columns:

**Left:** "About this skill"
> Built by Absolution Labs LTD because the same shape of company memory underpins every project we run with our own clients. We'd rather more companies have access to it than gate it behind a sales conversation.

**Right:** "Support + feedback"
> One email address, replied to within one business day:
> **info@absolutionlabs.com**

Below both columns:
- License: MIT — view on GitHub
- Threat model + decisions: brief.md on GitHub
- Source: github.com/absolutionlabs/obsidian-company-memory

---

## Style direction

- **Tone matches the README + the Loom script.** Calm, sales-tool-grade, no hype, no "revolutionary."
- **Typography:** the same family Absolution Labs uses for the rest of the site. If unsettled: serif body (Charter, Source Serif), sans display (Inter, Söhne).
- **Colour:** mostly Abso Labs brand. The install buttons should be the only saturated colour on the page above the fold.
- **No autoplay video.** No exit-intent popup. No cookie banner unless GDPR-required by your tracking choices (if Netlify Analytics or none — no banner needed).
- **No social login.** No email gate. No newsletter capture on this page.

---

## Mobile rules

- Hero collapses install buttons to stacked, full-width.
- Loom embed scales to 100% width, 16:9 aspect.
- 3-card "what it is" block stacks vertically.
- File tree (section 4) gets `overflow-x: scroll` rather than shrinking text below readability.

---

## Analytics

Track only what you need to decide whether to keep this surface alive:

- Page view count
- Install button click rate (Cowork vs Code)
- Loom play rate
- Bounce rate

Use Netlify's built-in analytics or Plausible. **Don't add Google Analytics, Hotjar, or anything that needs a cookie banner** — the privacy framing on the page would be undercut by the tracker stack.

---

## When to revise

Revise this page when:

- A new version of the skill ships (update version-related copy)
- The install URL changes (update the buttons + GitHub repo URL)
- The Loom is re-recorded (update the embed snippet)
- A test-matrix item produces a finding worth surfacing publicly (add to compatibility block)
- A material privacy or compliance change lands (update privacy summary verbatim from policy)

Revise on the same cadence the bundle releases — they're paired surfaces.

---

*Render this in whatever stack absolutionlabs.com runs on. The structure here is the canonical brief.*
