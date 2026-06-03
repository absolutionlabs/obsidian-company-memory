# Upgrading

How to think about skill versions, when to refresh, and how to roll back if something breaks. Short answer: most of the time you don't need to upgrade. Your vault is yours after scaffold. Read the rest to understand why, and what the exceptions are.

---

## The two things "upgrading" could mean

People sometimes conflate these. They're different.

### 1. Upgrading your installed skill

This is the install URL / `~/.claude/skills/` artifact that scaffolds new vaults. Upgrading this changes what FUTURE installs look like; it doesn't touch any existing vault.

You'd upgrade this when:
- You want to scaffold a NEW vault and want it to use the latest templates.
- You're shipping the skill to clients (as a consultancy) and want them to get the latest.
- We've released a security fix and you want the new bundle even though you're not scaffolding anything new today.

### 2. Refreshing an existing vault

This is bringing the templates and configs IN your already-scaffolded vault up to a newer skill version's defaults.

This is **not** something the skill does for you. The vault is yours after scaffold. The skill specifically refuses to re-run on a non-empty folder (key decision #14). Refreshing an existing vault is a manual operation, documented in § Refreshing an existing vault below.

The reason for this separation: your edits to `SCHEMA.md`, `CONTEXT.md`, your operating principles, your wiki pages are sovereign. We don't want to risk overwriting them with a "helpful" auto-update.

---

## Version pinning

The install page on [absolutionlabs.com](https://absolutionlabs.com) gives you two install paths for each surface (Cowork, Code):

- A URL for the **current latest version** — convenient, but means whatever ships next could land on you without warning.
- A URL for a **specific version** (e.g. `v1.0.0`, `v1.1.0`) — reproducible, rollback-safe.

**Use the specific-version URL in production.** Pinning to `v1.0.0` (or whichever version you tested against) means:

- Your install is reproducible.
- If we release `v1.1.0` and you don't like it, you keep `v1.0.0` until you choose to move.
- If `v1.1.0` introduces a regression, you can stay on `v1.0.0` until it's fixed.

Old versions never disappear. The install page keeps every previous version selectable indefinitely; see § Version retention below.

### How to know which version you have

Two places:

1. **Your installed skill artifact:**
   - Cowork: Settings → Plugins → Obsidian Company Memory → shown next to the name.
   - Code: `cat ~/.claude/skills/obsidian-company-memory/SKILL.md | head -10` — the `version:` field in the frontmatter.

2. **Inside any vault you scaffolded:** `cat <vault>/_meta/scaffold-version.txt` — the line `version: 1.0.0` (per SKILL.md Step 6.7) records which version of the skill scaffolded that vault. This stamp does NOT auto-update when you upgrade the skill — it's a permanent record of what was installed and when.

---

## Upgrading the installed skill

### Cowork

1. Settings → Plugins → Obsidian Company Memory → uninstall.
2. Visit the install page on [absolutionlabs.com](https://absolutionlabs.com), pick the version you want, copy the install URL.
3. Paste into Cowork's plugin-install field.

The plugin is replaced in place. No vault changes occur as part of this.

### Claude Code

```sh
rm -rf ~/.claude/skills/obsidian-company-memory
# Then paste the one-line install command for the version you want
# from absolutionlabs.com — the page shows the current command.
```

Restart Code (or its harness) to pick up the new skill version.

### Verifying

After upgrading, scaffold a test vault into a throwaway folder. The new templates should land. If they don't, the old artifact is cached — clean install harder (Cowork: log out + log back in; Code: clear the skills cache per your harness's docs).

---

## Refreshing an existing vault

The skill won't do this for you. Doing it by hand is straightforward if you understand what changed between versions.

### Workflow

1. **Read the release notes** for every version between yours and the target. The install page on [absolutionlabs.com](https://absolutionlabs.com) links to per-version notes; the most recent version is at the top.

2. **Decide what you want.** Most users want one or two specific changes (a new lint rule, an updated operating principle, a `.obsidian/` config fix). You rarely want everything.

3. **Make a backup.** Zip the whole vault folder before touching anything. Cloud sync version history is also a backup, but the local zip is the one you control.

4. **Pull the change.**
   - For each file you want to refresh, copy the new version from the upgraded skill's `templates/` into your vault.
   - Pay attention to the substitution placeholders: `{{COMPANY_NAME}}` etc. in the templates must be replaced with your actual values. The original scaffold did this for you; a manual refresh requires you to do it.
   - Re-merge anything you'd customised. Use a diff tool (`diff`, `meld`, VS Code's diff view) — you'll see your edits vs the new defaults side-by-side.

5. **Re-key any references.** If the new version renames a file or moves something, the rest of your vault still points at the old path. Search-and-replace.

6. **Run a lint.** Open an AI session and say "run a lint on the vault." If anything's drifted, the lint surfaces it.

7. **Update the version stamp.** Edit `_meta/scaffold-version.txt` to record the refresh:
   ```
   version: 1.0.0
   refreshed-to: 1.1.0
   refreshed-on: 2026-09-02
   ```

   Keeping the original `version:` line means you still know which version originally scaffolded the vault. The new `refreshed-to:` + `refreshed-on:` lines tell future-you (and any operator) what you brought forward.

### When NOT to refresh

- **You only use the vault occasionally.** The longer you've gone without using the vault, the more drift; refresh after your next real working session, not before.
- **You're mid-project.** Refreshing in the middle of a build risks introducing template drift you'll attribute to your project's issues. Finish what you're on, then refresh.
- **You've extensively customised your SCHEMA / templates / principles.** A refresh might not give you anything net-new and risks losing customisation. Read the changelog first; cherry-pick.

---

## Rolling back

### Rolling back the installed skill

Code: `rm -rf ~/.claude/skills/obsidian-company-memory`, then paste the one-line install for the older version from the install page on [absolutionlabs.com](https://absolutionlabs.com).

Cowork: uninstall the current version, install from the version-pinned URL for the older version (same install page).

You can always revert to any past version we've published, because every version stays selectable on the install page forever.

### Rolling back changes to a vault

Your vault is plain markdown synced via your cloud provider's history. Roll back by:

1. **Cloud sync history.** Dropbox: web UI → right-click file → "Version history". OneDrive: web UI → file info → "Version history". Google Drive: web UI → file info → "Manage versions". iCloud: doesn't have per-file version history; use Time Machine on macOS.
2. **Quarterly zip backup.** If you took one before the change you regret: unzip into a temporary location, copy the affected file(s) back.
3. **Local OS backup.** Time Machine, File History, Backblaze, Arq — whatever you run.

The vault has no proprietary database, no migrations to undo, no schema upgrades to reverse. Rollback is file-level only.

---

## Version retention

Every published version of this skill remains selectable from the install page on [absolutionlabs.com](https://absolutionlabs.com) indefinitely. We do not retire old versions.

What you should know:

- **Older versions may stop receiving security patches.** We backport critical fixes to the most recent two minor versions only (currently: `v1.x` once we ship `v1.1.0`). If you're on `v1.0.0` six versions later, you're carrying any unpatched issues yourself.
- **Older versions may stop being compatible with newer Obsidian / agent CLIs.** If `v1.0.0`'s `.obsidian/` config uses a field deprecated in Obsidian 2.0, that's not our problem to fix on `v1.0.0` — but `v1.0.0` will still install. You'd need to migrate.
- **The compatibility matrix in [COMPATIBILITY.md](../COMPATIBILITY.md) is updated for the current version only.** Older versions' compatibility is whatever was true at their release date.

If we ever need to withdraw a published version (e.g. a critical security issue we can't patch backwards), we'll:
- Replace the version's entry on the install page with a clear "this version was withdrawn because [reason]; please install [recommended replacement]" notice.
- Email everyone we have a contact for (which is: nobody — we don't collect any contact information at install, by design).
- Post the withdrawal on the Absolution Labs site.

This is a hard-thought policy; we expect to use it never.

---

## Release cadence

The skill is not on a release schedule. Releases happen when:

- A security issue requires a fix (immediate)
- A real bug is reported and confirmed (within one to two weeks)
- A clear improvement is ready and tested (whenever)
- Quarterly compatibility refresh adds new tested combinations to [COMPATIBILITY.md](../COMPATIBILITY.md) — usually patch-version releases

No release will silently change your installed version. You upgrade when you choose to.

---

## How to know when to upgrade

We don't push notifications. The install doesn't phone home for version checks. You discover new releases the same way you'd discover anything else from Absolution Labs:

- Subscribe to the Absolution Labs newsletter at [absolutionlabs.com](https://absolutionlabs.com).
- Check the install page on [absolutionlabs.com](https://absolutionlabs.com) periodically — current version is shown.
- Email `info@absolutionlabs.com` to ask if there's a newer version than the one you're running.

This is intentional. Auto-update is convenient but also a path through which someone could ship a broken or compromised version into your environment without you noticing. The skill installs once and stays put until you choose otherwise.

---

*Cross-references: [README.md](../README.md), [SKILL.md](../SKILL.md), [COMPATIBILITY.md](../COMPATIBILITY.md), [troubleshooting.md](troubleshooting.md), [customisation.md](customisation.md).*

---

## Use at your own risk

This document is part of the Obsidian Company Memory bundle, provided "AS IS" without warranty of any kind under the MIT License. It is for general informational and educational purposes only and does not constitute professional advice. Upgrade procedures involve modifications to your vault; back up the vault folder via your cloud sync provider's version history before applying any upgrade. **Read [DISCLAIMERS.md](../DISCLAIMERS.md) in full before installing, upgrading, forking, or relying on anything in this repository.**

*© 2026 Absolution Labs. AbsolutionLabs Ltd, registered in England and Wales (Company No. 17091663). Registered office: 15 Westbury Road, London SE20 7QL.*
