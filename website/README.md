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
| `install-page.md` | Hero copy for the install landing page | `absolutionlabs.com/obsidian` (or `/install/obsidian-company-memory` — pick the slug at deploy time) |
| `privacy-page-deploy.md` | Instructions for publishing `docs/privacy-policy.md` to the website's privacy URL | `absolutionlabs.com/privacy` (or `/obsidian-privacy` if you want a per-product policy) |
| `feedback-form-spec.md` | What the feedback form should capture; tech-stack-agnostic | `absolutionlabs.com/feedback` (or replaced by mailto-only) |
| `loom-embed-snippet.md` | HTML snippet for embedding the Loom on the install page | embedded in `install-page.md` output |

---

## Deploy order (when you're ready to ship public)

1. Publish `privacy-page-deploy.md` first — the SKILL.md telemetry surface references this URL.
2. Publish `install-page.md` — links to the privacy URL from step 1.
3. Add the feedback form (or just point at `info@absolutionlabs.com` if you'd rather skip the form for v1).
4. Once the install page is live and the Loom is recorded, paste the Loom embed snippet into the install page above the install URL fold.

Order matters because each surface assumes the previous is live. The Loom in particular references the privacy URL during Scene 6.

---

## Anti-deploy: what NOT to do

- **Don't put the skill's source code on the website.** It belongs in the public GitHub repo. The website links to it, doesn't host it.
- **Don't duplicate the privacy policy text** between this folder and `docs/privacy-policy.md`. The bundle's copy is canonical; the website should render from it (or copy at deploy time with a clear "synced from bundle on X date" footer).
- **Don't gate the install URL behind a form fill.** The skill is free; gating it would break the trust framing in `brief.md` Decision #18.

---

*Maintained alongside the bundle by Absolution Labs LTD.*
