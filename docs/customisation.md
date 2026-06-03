# Customisation

How to fork this skill into your own variant — for your own company, for a consultancy you run, for a different shape of memory system that you want to ship to your own clients.

The skill is MIT-licensed. You can take it as your own starting point with no permission needed; the only requirement is that the LICENSE file travels with the copy. We'd appreciate a "based on Obsidian Company Memory by Absolution Labs LTD" line in your README, but it's not legally required.

This guide assumes you're comfortable editing markdown and JSON. You don't need to write TypeScript unless you also fork the telemetry endpoint.

---

## What's editable, and how the bundle is structured

The skill is a folder of files. Most are content; a few are procedure. Customising means editing the content; touching the procedure is more involved.

### Safe to edit freely (content layer)

These files are the vault's starter content. Editing them changes what new vaults look like; nothing structural breaks.

- `templates/SCHEMA.md` — the rulebook every AI session reads. Edit to change conventions, add new operations, change the page-format rules.
- `templates/CONTEXT.md` — the "about this company" template. Edit to change the default sections users see.
- `templates/HOW-TO-USE-THIS.md` — the Phase 2 living guide. Edit to change the daily-use rhythm you want to propose.
- `templates/concepts/claude-operating-principles.md` — the starter 5 operating principles. Edit to change which principles your variant ships.
- `templates/_meta/expectations.yml` — lint thresholds (stale-page age, required frontmatter fields, allowed page types). Edit to change defaults.
- `templates/_meta/templates/*.md` — page templates (entity, concept, query). Edit to change the default page shape users get when they create a new page.
- `templates/.obsidian/*.json` — Obsidian config defaults. Edit to change theme, attachment folder, default plugin set, etc.

After editing any of these, the next person who runs your skill gets your version verbatim. No code changes required.

### Edit with care (the procedure)

- `SKILL.md` — the procedure the AI runs at install time. The YAML frontmatter is metadata; the body is steps. Editing this changes how the install moment behaves: questions asked, gates enforced, files written, round-trip test shape.
- `plugin.json` — the Cowork plugin manifest. Edit when bundle contents change, when version bumps, when you map a different telemetry endpoint.
- `MANIFESTS.md` — the mirror contract between `SKILL.md` frontmatter and `plugin.json`. If you change one of those two, update this doc too.

Most customisations don't need procedure edits. If you're editing SKILL.md beyond changing the company-branded copy, you're effectively building a different product — at that point, consider whether you're forking or replacing.

### Generally leave alone

- `telemetry/` — the Supabase project for install telemetry (Postgres schema, RLS, rate-limit triggers, DSAR helper). Forking the telemetry means standing up your own Supabase project, applying the migration, capturing your own anon + service-role keys, and writing your own privacy policy. If you don't want telemetry, the simpler option is to delete the call from SKILL.md Step 5 + Step 9.1.
- `docs/privacy-policy.md` — only applies if you keep our telemetry. If you fork telemetry, write your own policy.
- `LICENSE` — required to travel with the copy unmodified. Don't delete this file.

---

## Common customisations

### 1. Rebrand the skill for your own company

Replace every literal `Absolution Labs LTD` with your company's full legal name; replace every `absolutionlabs.com` with your domain; replace `info@absolutionlabs.com` / `privacy@absolutionlabs.com` / `security@absolutionlabs.com` with your equivalents.

Files to touch:

- `README.md` — top-of-file branding + "About" section
- `SKILL.md` — frontmatter `publisher` field + body branding throughout
- `plugin.json` — `publisher` block
- `MANIFESTS.md` — synced-fields table
- `templates/CONTEXT.md` — "About the publisher" line
- `templates/HOW-TO-USE-THIS.md` — "About the publisher" section
- `LICENSE` — copyright line (KEEP MIT permission text identical; change only the `Copyright (c) <year> <your company>` line)
- `COMPATIBILITY.md`, `docs/*` — incidental branding

A grep for `Absolution Labs` will find them all. Most installs of this shape that I've seen do the rebrand in 15 minutes.

### 2. Change the starter Operating Principles

The skill ships with five starter principles in `templates/concepts/claude-operating-principles.md`. If your company's working style is different — different tone, different priorities, different escalation rules — replace the file.

Conventions to keep:

- Each principle has a clear name, a "Why:" paragraph, a "How to apply:" paragraph.
- Five-ish is the right number. Fewer than three feels arbitrary; more than seven feels like rules.
- Principles earned through real incidents land better than principles invented in the abstract.

If your principles diverge enough that the page reads like a different system, also update `templates/HOW-TO-USE-THIS.md` § Operating Principles to match.

### 3. Add a custom intake question

By default the skill asks two questions (company name + sync provider). If your variant needs a third — industry, team size, primary use case — add it to `SKILL.md` Step 3.

Pattern:

1. Edit `SKILL.md` Step 3 to add the new question to the batched `AskUserQuestion` call.
2. Add a new substitution placeholder (e.g. `{{INDUSTRY}}`) to the substitution table at the top of Step 6.
3. Use it in any template file (e.g. `templates/CONTEXT.md`) where you want the answer to appear.
4. Update `plugin.json` `permissions.directory_access.writes` if you're writing new files based on the answer.

Keep the question count low. Each question is a friction point; users abandon installs at the third one more than they abandon at the second.

### 4. Add a fourth folder to the wiki layer

The default vault has four wiki folders: `entities/`, `concepts/`, `comparisons/`, `queries/`. If you want a fifth (e.g. `decisions/`, `playbooks/`, `clients/`):

1. Add it to `SKILL.md` Step 6.1 (folder creation list).
2. Add a section header to `templates/index.md` so new pages of that type have a home.
3. Add a row to `templates/SCHEMA.md` § 1 Architecture and § 2 Page format.
4. Optionally add a page template at `templates/_meta/templates/<new-type>.md`.
5. Add the new type to `templates/_meta/expectations.yml` `allowed_types` and pick a stale threshold.

Keep additions deliberate. Five wiki folders is right for most shapes; ten is usually a sign that you're using folders where you should be using tags.

### 5. Change the lint thresholds

Lint thresholds live in `templates/_meta/expectations.yml`. The defaults:

```yaml
stale_thresholds:
  entity: 90       # days
  concept: 90
  comparison: 180
  query: 365
  context: 30
min_wikilinks_per_page: 1
min_incoming_wikilinks: 1
```

Edit to your taste. Tighter thresholds = more lint noise but earlier drift detection. Looser thresholds = less noise but more risk of stale content going unchallenged.

### 6. Swap the .obsidian/ defaults

`templates/.obsidian/*.json` controls Obsidian's behaviour out of the gate. Common changes:

- `app.json` — `attachmentFolderPath` controls where pasted images land; default is `raw/assets`. Change if your file convention is different.
- `appearance.json` — light vs dark theme default. Pick the one your users will expect.
- `core-plugins.json` — Obsidian's built-in plugins. Default enables a sensible set; you can prune or add.
- `community-plugins.json` — empty by default (decision #6: we don't bundle plugins). If you want to ship a recommended plugin set, list the IDs here; users still install the plugins themselves from Obsidian's browser, but enabling-on-install saves them a click.
- `hotkeys.json` — empty by default. Add custom hotkeys if your daily flow uses any.

JSON files only; no markdown substitution happens here.

### 7. Replace the install telemetry

Three options:

**(a) Remove telemetry entirely.** Edit `SKILL.md` Step 5 to skip the surface; delete `SKILL.md` Step 9.1 (success ping). Delete the `telemetry/` folder. Remove the `telemetry` block from `plugin.json`. Update `docs/privacy-policy.md` to reflect "no telemetry sent."

**(b) Point at your own endpoint.** Stand up your own Supabase project (create a project, apply the migration at `telemetry/supabase/migrations/`, capture the anon key). Edit `SKILL.md` Step 5 + Step 9.1 to point at your URL. Update `plugin.json.telemetry.endpoint` + `plugin.json.telemetry.anon_key`. Write your own privacy policy.

**(c) Keep ours.** If your variant is close enough to ours that our telemetry endpoint is fine for your use too: do nothing. Pings will go to our infrastructure and we'll see your installs in our funnel. Reach out — we may want to coordinate on what counts as a release.

Option (a) is the simplest. Option (b) is the most rigorous. Option (c) only makes sense if you're closely partnered with us.

### 8. Change the appetite from "free tool" to "paid"

The skill ships free. If your variant is paid:

- Add a `pricing` field to `plugin.json` (no schema requirement; convention).
- Update `README.md` to clearly state the price.
- Update `LICENSE` if you want a different licence than MIT (note: MIT permits selling derivative works without re-licensing, so you can sell a fork while keeping MIT — but most paid variants choose a more restrictive licence).
- Consider whether the compliance gate + refuse-to-scaffold gate are still right defaults; paid variants sometimes negotiate stricter or looser settings per client.

The skill's design doesn't assume "free." It assumes "trustworthy." Those aren't the same thing.

---

## Re-packaging your fork

Once you've edited the bundle:

1. **Bump the version** in BOTH `SKILL.md` frontmatter `version` AND `plugin.json` `version`. Use semver. Document the change in your own `CHANGELOG.md` or equivalent.
2. **Sign the bundle** if you're distributing publicly. The release-signing URL in `plugin.json.release_signing` should resolve to your own signing key.
3. **Regenerate checksums** for the public bundle and host them at your `checksums_url`.
4. **Update the install URLs** in `README.md` to point at your hosted bundle (not absolutionlabs.com).
5. **Verify the manifest mirror contract** per [MANIFESTS.md](../MANIFESTS.md) § Pre-release manifest lint. Eleven checks; runs in under a second via `python scripts/lint_manifest.py`.
6. **Test the install on a clean machine** before publishing. The "Test matrix" section of the brief lists 7 personas worth testing against; pick the ones your customer base looks like.

---

## What we'd like to know

If you fork this skill into a publicly-distributed variant, we'd love a one-line note to `info@absolutionlabs.com` letting us know it exists. We don't ask for anything in return — but knowing what people built on top of this shapes how we evolve the canonical version.

If your fork is private (internal company use only): no need to tell us.

---

## What we'll never do to your fork

- We won't try to claim authorship over your customisations.
- We won't release updates that intentionally break forks.
- We won't change the MIT license terms retroactively.
- We won't gate features behind a "join the marketplace" requirement that breaks self-hosted variants.

The shape is yours, the work is yours, the relationship with your users is yours.

---

*Cross-references: [README.md](../README.md), [SKILL.md](../SKILL.md), [MANIFESTS.md](../MANIFESTS.md), [brief.md](../brief.md).*

---

## Use at your own risk

This document is part of the Obsidian Company Memory bundle, provided "AS IS" without warranty of any kind under the MIT License. It is for general informational and educational purposes only and does not constitute professional advice. Forking the bundle, modifying it, redistributing it, or building a commercial product on top of it is permitted under the MIT License — but if you do, you indemnify Absolution Labs LTD against any claims arising from your fork or your downstream distribution (see [DISCLAIMERS.md](../DISCLAIMERS.md) § Indemnity). **Read [DISCLAIMERS.md](../DISCLAIMERS.md) in full before forking or redistributing this repository.**

*© 2026 Absolution Labs. AbsolutionLabs Ltd, registered in England and Wales (Company No. 17091663). Registered office: 15 Westbury Road, London SE20 7QL.*
