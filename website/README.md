# Website deploy artifacts — Obsidian Company Memory

Files in this folder are the **copy + spec** for the website surfaces that live on `absolutionlabs.com`. They are NOT part of the skill bundle that ships to users — they're the install funnel + privacy + feedback surfaces that the bundle's docs point at.

Two surfaces, two jobs:

| Surface | Lives in | Job |
|---|---|---|
| Bundle (everything else in this repo) | GitHub repo / install URL | The thing users install |
| Website (this folder) | `absolutionlabs.com` (Netlify) | The install funnel + trust surface that points users at the bundle |

---

## What's here

| File | Purpose | Deploys to |
|---|---|---|
| `overview-page.md` | Canonical install landing page (story-led; supersedes install-page.md) | `absolutionlabs.com/obsidian` |
| `install-page.md` | SUPERSEDED — earlier button-led shape, kept for history; do not deploy | n/a |
| `resources-page-card.md` | Card copy for the AbsoLabs resources page listing | `absolutionlabs.com/resources` (existing surface) |
| `feedback-form-spec.md` | What the feedback form would capture if/when one ships (v1 = email-only) | `absolutionlabs.com/feedback` (not deployed in v1) |
| `loom-embed-snippet.md` | HTML snippet for embedding the Loom on the install page | embedded in `overview-page.md` output once Loom is recorded |

---

## Deploy order (when you're ready to ship public)

1. Publish `overview-page.md` at `absolutionlabs.com/obsidian` (story-led, with a single "Get it on GitHub" CTA at the bottom).
2. Update `absolutionlabs.com/resources` to render the `resources-page-card.md` card (replaces the placeholder "Coming soon" entry).
3. Once the Loom is recorded, paste the Loom embed snippet into the overview page above the GitHub CTA.

No privacy page is required for this skill — v1.2.0 removed the install-telemetry surface entirely, so there is no install-time data collection to disclose.

---

## Anti-deploy: what NOT to do

- **Don't put the skill's source code on the website.** It belongs in the public GitHub repo. The website links to it, doesn't host it.
- **Don't reintroduce a privacy page for this skill.** v1.2.0 ships with no install telemetry, so a per-skill privacy policy would be misleading. If your wider AL website has a general privacy policy, the bundle inherits that posture (cookies / Netlify analytics / etc.) but the skill itself adds nothing.
- **Don't gate the install URL behind a form fill.** The skill is free; gating it would break the trust framing the bundle leans on.

---

*Maintained alongside the bundle by Absolution Labs LTD.*
