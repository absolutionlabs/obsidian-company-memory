# Privacy page deploy — `absolutionlabs.com/privacy`

The bundle's `docs/privacy-policy.md` is the canonical text. This file documents how to publish it to the website without drift.

---

## Two valid models

### Model A — One privacy URL covers everything Abso Labs does (recommended)

If `absolutionlabs.com/privacy` is your single privacy policy for the whole company:

1. Take the contents of `docs/privacy-policy.md` from the bundle.
2. Render it as a section of the main privacy policy under a clearly-titled heading: **"Obsidian Company Memory skill — install telemetry"**.
3. Cross-link from the main policy to this section, and from the bundle's references to the main policy URL.

Pros: one URL for prospects to bookmark; one policy for legal review (eventual); the section can be archived in place when the skill is retired.

Cons: a regulated-sector prospect reading the policy sees a longer document; they have to skim for the section about the skill.

### Model B — Per-product privacy URL

If the install-telemetry policy gets its own URL (e.g. `absolutionlabs.com/obsidian/privacy` or `/privacy/obsidian-company-memory`):

1. Render `docs/privacy-policy.md` verbatim as a standalone page.
2. Add a top-of-page link back to `/privacy` for the main policy ("for our company-wide privacy practices, see [link]").
3. Update the bundle's references (SKILL.md Step 5, plugin.json `privacy_policy_url`, README.md, loom-script.md Scene 6, TESTERS.md) to point at the per-product URL.

Pros: dedicated focused policy for the install-telemetry surface; matches what a careful regulated-sector prospect expects (per-product DPAs are normal).

Cons: drift risk between this URL and the main policy; two places to keep in sync if the company-wide posture changes.

**My recommendation: Model A.** Cheaper to operate, less drift risk. If you ship more skills with similar telemetry, each gets a section under one canonical privacy URL.

---

## Render step

The bundle's policy is markdown. Convert to the website's stack:

- **Netlify + plain markdown:** drop the file into your content folder; Netlify renders.
- **Hugo / Astro / 11ty:** import as a markdown source file; render through your normal template.
- **Plain HTML site:** `pandoc docs/privacy-policy.md -o privacy.html` and paste into your layout, OR copy-paste the body and let your editor do the markdown rendering.

The internal-notes block at the bottom of `docs/privacy-policy.md` (the 8-item internal pre-publication checklist) **must be stripped before publishing**. The block is clearly marked `## Internal notes (remove before publishing)`.

---

## Pre-publish checklist

Before publishing, walk these (from the bundle's own internal checklist):

- [ ] Effective date set at the top
- [ ] Company number + registered address filled in (placeholder `*(to be filled in)*` in the bundle)
- [ ] Internal notes section stripped
- [ ] Endpoint URL matches the live Supabase project (`https://vujwcvqiwwpncnhgxjsu.supabase.co/rest/v1/install_events`)
- [ ] Sub-processor reference is current (Supabase Inc + AWS, both EU region)
- [ ] DSAR email address (`privacy@absolutionlabs.com`) is monitored
- [ ] Cross-link from main privacy policy (Model A) OR back-link to main policy (Model B)
- [ ] DPA with Supabase verified on file
- [ ] ICO data-protection-fee register entry confirmed for Absolution Labs LTD

The original bundle's `docs/privacy-policy.md` also notes "UK GDPR lawyer review" as a pre-publish step. **Operator has explicitly deferred this for v1.** Publish as-is; queue lawyer review for before any non-EU/UK customer testimonial appears publicly.

---

## After publishing

1. Smoke-test the URL — open in an incognito browser, confirm it loads, confirm the headings match.
2. Notify the bundle: nothing actually changes in the repo. The bundle already references `absolutionlabs.com/privacy` as a literal URL.
3. Verify the SKILL.md install flow's Step 5 link works end-to-end — install the skill on a test folder, watch the telemetry surface render, click the privacy link, confirm it lands on the right page.
4. If you went with Model B (per-product URL), also update:
   - `SKILL.md` Step 5 surface text
   - `plugin.json.telemetry.privacy_policy_url`
   - `README.md` Privacy section
   - `loom-script.md` Scene 6 if the URL is verbalised
   - `TESTERS.md` reference

---

## When to revise

Revise the published policy when:

- The endpoint URL changes (custom domain `telemetry.absolutionlabs.com` is the planned change)
- A new field is added to the install telemetry schema (per the locked-fields convention in the migration — should be nullable + the 9-field disclosure table updates with the same release)
- The sub-processor stack changes (e.g. Supabase moves provider, or we add a new processor)
- Retention changes from 24 months
- The lawful basis is revisited (currently legitimate interests; alternative would be consent)
- A new regulator becomes relevant (e.g. EU residence beyond UK)

Each revision: bump the effective date at the top, add a change-log entry below the title block, do NOT retroactively apply to data already collected.

---

*The bundle's [docs/privacy-policy.md](../docs/privacy-policy.md) is the canonical source. This file is the deploy spec.*
