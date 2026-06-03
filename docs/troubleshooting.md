# Troubleshooting

Common failure modes, what they mean, and how to recover. Organised by where in the install flow they appear.

If nothing here describes what you're seeing: email `info@absolutionlabs.com` with your OS, agent CLI, sync provider, and the exact error message. Response within one business day.

---

## Pre-install — before the skill starts

### "I pasted the install URL into Cowork and nothing happened."

The most common cause: Cowork's plugin install field rejected the URL silently because it didn't match the expected pattern (HTTPS + Absolution Labs domain).

Check:
- You copied the URL from the current install page on [absolutionlabs.com](https://absolutionlabs.com) and it's pasted with no trailing slash or extra characters.
- You're signed in to Cowork.
- You're on a Cowork plan that allows third-party plugin installs (the free tier may not).

If all three are fine: try clearing the input field and pasting again. Some browsers strip URL characters during paste-and-replace.

### "Claude Code says the install script isn't trusted."

The Code install uses `curl … | sh`. Some hardened terminal environments block piped-shell installs by default.

Options:
- Download the install script from [absolutionlabs.com](https://absolutionlabs.com) first, inspect it (it should be ~30 lines doing a `git clone` and a `mv`), then run it locally.
- Manual install: clone the source repo into `~/.claude/skills/obsidian-company-memory` (the repo URL is on the install page) and restart Claude Code.

### "The compliance checkboxes won't let me proceed."

The skill enforces all three checkboxes before any file write. If "Continue" is greyed out: one or more is unticked. Scroll back through the gate — each checkbox should show a tick when selected.

If you genuinely can't tick one of them (e.g. you're not sure the folder is yours to write to): don't force-install. Resolve the underlying question first. The checkbox gate is the trust signal, not a friction tax.

---

## During install — pre-flight refusals

### "Target folder is not empty."

The skill refuses to install into any folder containing files (key decision #14). This is the safest answer — it prevents accidental overwriting of an existing vault or unrelated work.

What to do:
- Create a new empty folder, mount it (or `cd` into it), and re-run the skill. This is the normal path.
- If you genuinely want to merge with an existing folder's contents: this skill can't help. Email `info@absolutionlabs.com` and describe what you have; we'll guide a manual migration.

The skill does NOT have a `--force` flag and won't be adding one. The refusal is the feature.

### "Pre-flight: worktree detected. Please relaunch from the main checkout."

You're running the skill from inside a git worktree (`.git/worktrees/<name>`). This produces an ephemeral CWD that strands real work on a transient branch (see Claude Operating Principle #19).

What to do: close the session, navigate to the main project checkout, and re-run from there. The skill is intentionally strict about this — silently scaffolding into a worktree has caused real data loss in our own projects.

### "Skill bundle integrity check failed: missing files."

The bundle's template files didn't all download. Most often a network blip during plugin install or `curl | sh`.

What to do: re-install. Cowork — uninstall the plugin, re-install. Code — `rm -rf ~/.claude/skills/obsidian-company-memory` then re-run the install script. The fresh download will usually succeed.

If it fails repeatedly, your network may be blocking `absolutionlabs.com` or its CDN. Check with a corporate IT team if applicable.

---

## During install — scaffold failures

### Mid-scaffold failure ("the scaffold did not complete")

The skill writes ~20 files. If any single file write fails, the skill stops and surfaces which files were written successfully and which failed. **It does NOT try to continue.**

Recover:
1. Note the path the skill reported (it will be your vault folder).
2. Delete the contents of that folder — every file, every subfolder, including `.obsidian/`. The folder should be empty.
3. Re-run the skill.
4. If it fails again with the same root cause (e.g. cloud sync throttling, permission denied), the underlying issue isn't transient. Surface to `info@absolutionlabs.com`.

The skill's design treats partial scaffolds as fundamentally untrustworthy. A re-run on a partially-written folder would conflict with the refuse-to-scaffold gate, and "force a continue" would risk a vault that looks complete but isn't.

### "Pathologically slow write" warning

If a single file write takes > 10 seconds, the skill warns and suggests pausing your cloud sync provider. Most often this happens on:

- **Dropbox for Business** with per-second write limits on `.obsidian/` folders.
- **OneDrive for Business** with strict tenant policies on hidden folders.
- **iCloud Drive** when "Optimised Storage" is evicting the folder mid-write.

Recover:
1. Pause sync (Dropbox: menu bar → Pause; OneDrive: menu bar → Pause syncing; iCloud: System Settings → iCloud → Drive → off temporarily).
2. Delete the partial scaffold (per "Mid-scaffold failure" above).
3. Re-run the skill. It should complete quickly.
4. Re-enable sync. The provider will catch up over the next minute.

### "No write access to target folder."

OS-level permissions are blocking the skill. Common causes:

- macOS: the folder is under a sandboxed path (`~/Library/CloudStorage/…`) and Cowork doesn't have Full Disk Access. Grant it in System Settings → Privacy & Security → Full Disk Access.
- Windows: the folder is under a redirected user folder (Documents / Desktop / OneDrive Known Folder Move). Choose a different folder; redirected ones cause path-rewriting drama.
- Linux: the user running Cowork / Code doesn't own the folder. `chown -R $USER:$USER /path/to/folder`.

---

## Post-scaffold — verifying the round-trip

The skill runs a 5-step verification in Obsidian. If any step fails, here's what to check.

### "I see SCHEMA.md but the wikilink in test-welcome.md doesn't resolve."

Obsidian's wikilink support is on by default but can be flipped off. Check:
- Settings → Files & Links → "Use [[Wikilinks]]" must be ON.
- The vault root must match the folder the skill scaffolded into (not a parent, not a subfolder).

If "Use [[Wikilinks]]" is off: turn it on, restart Obsidian, retry. The `.obsidian/app.json` config the skill writes sets this correctly, but a user who edited `.obsidian/` manually may have flipped it.

### "I opened the folder as a vault but Obsidian shows it as empty."

Almost always: you opened a parent folder, not the scaffolded folder. The vault must be opened at the same path the skill wrote to.

Check: in Obsidian → File → Open vault, the vault path should be your full `<vault-absolute-path>`. If it's a parent, close the vault and re-open at the correct path.

### "Obsidian says the vault is corrupt."

Very rare. Usually means a file Obsidian needs (`.obsidian/workspace.json` typically) is malformed because of an external edit.

Recover:
1. Close Obsidian.
2. Delete `.obsidian/workspace.json` only (not the whole `.obsidian/` folder).
3. Re-open Obsidian. It'll regenerate workspace state.

If the issue persists, you may have hit a Dropbox conflict file or a partial write. Check the folder for files ending in `(Dropbox conflict)` or similar; resolve by keeping one and deleting the other.

---

## Post-install — runtime issues

### "Telemetry could not be sent."

Non-blocking. The install proceeded; the success ping just didn't reach our endpoint. Common causes:

- Your firewall blocks `vujwcvqiwwpncnhgxjsu.supabase.co` (the raw Supabase project URL — a custom domain `telemetry.absolutionlabs.com` is planned but not yet deployed).
- Supabase had a brief outage.
- You're behind a corporate proxy that strips outbound POSTs.

No action needed. Your vault works. If you want us to know your install succeeded (it would help our funnel data), send a one-line email to `info@absolutionlabs.com`. Or ignore — it's genuinely opt-in for us, not just for you.

### "I want to delete my install telemetry."

Email `privacy@absolutionlabs.com` with the subject line `DSAR — Obsidian Company Memory — <your-UUID>`. The UUID was shown to you at install time in the final message. We delete all rows matching that UUID within one business day and reply confirming.

If you've lost your UUID: by design, we have no other way to identify your rows (no email, no IP, no company name in the data). The deletion right can't be exercised against rows you can't identify — but the same property means nobody else can either. That's the trade-off of true anonymisation.

### "I want to refresh my vault to the latest skill version."

See [upgrading.md](upgrading.md). Short answer: most of the time you don't need to. The vault is yours after scaffold; template updates flow into your vault only if you explicitly pull them in.

### "I started using the vault and now wikilinks I added are showing as broken."

The lint operation will tell you exactly which ones. Open a session with your AI assistant and say: "run a lint on the vault." It writes a report to `lint-reports/YYYY-MM-DD.md`.

Common causes:
- You created a page in Obsidian but forgot to add it to `index.md`. The lint flags this as "index drift".
- A page got renamed and Obsidian didn't auto-update the links. Use Obsidian's Find & Replace to fix the wikilink paths.
- A wikilink points at a page you never created. The lint surfaces these as "data gaps" — either create the page or remove the link.

### "The AI keeps writing pages that don't match SCHEMA.md."

Three things to check:
1. **Is the AI session reading SCHEMA at start?** It should be — that's the close protocol's first step. If you suspect it's skipping, paste this opener: *"Re-read SCHEMA.md and CONTEXT.md before doing any work. Confirm you've done so."*
2. **Has SCHEMA drifted?** If you edited SCHEMA without re-instructing the AI, the AI may be working off the old rules from its session memory. New session = re-reads SCHEMA = fresh.
3. **Is the AI overruling SCHEMA based on prior conversation?** Sometimes happens with long sessions. Force a re-read.

### "I want to start the vault over from scratch."

Delete the vault folder. Re-run the skill on an empty folder. You lose everything in the old vault — make sure that's what you want first. (Cloud sync version history may give you a recovery path if you change your mind.)

---

## Cloud sync conflict files

Every major sync provider creates conflict files when two devices edit the same file in close succession.

- **Dropbox:** `filename (conflicted copy 2026-06-02).md`
- **OneDrive:** `filename-<DeviceName>.md`
- **Google Drive:** `filename (1).md`
- **iCloud:** rarely creates conflicts; uses a merge UI instead

Recover:
1. Open both versions in a text editor.
2. Manually merge (or pick the more-recent one).
3. Delete the conflict file.
4. In the next AI session, run a lint to confirm the resolution didn't leave dangling wikilinks.
5. Append a line to `log.md`: "Resolved Dropbox conflict on `<path>` — kept `<which version>` because `<reason>`."

The vault is markdown. Conflict resolution is just text editing. Don't be intimidated by it.

---

## Lost / damaged vault

Worst case: you've lost the vault folder, or files inside it are unrecoverable.

Recovery options, in order:

1. **Cloud sync version history.** Dropbox / OneDrive / Google Drive all keep file history for 30+ days. Restore the folder from the provider's web UI.
2. **Local Time Machine / File History backup.** If your OS-level backup is on, the vault folder is in it.
3. **Quarterly zip backup.** If you followed the HOW-TO-USE-THIS.md backup-hygiene advice and ran a quarterly zip, restore from there.
4. **Re-scaffold + re-import.** If everything else has failed: scaffold a fresh vault, then manually re-key the facts you remember. The raw documents in `raw/` (transcripts, contracts, PDFs) are typically the hardest to recover — keep them backed up separately if they matter.

The vault is plain markdown. There is no proprietary database, no schema migration, no vendor lock-in. Recovery from any markdown source is a copy operation.

---

## Bundle download issues

The skill bundle is ~25 files; if even one is missing, the pre-flight integrity check refuses. These are the common reasons the download doesn't land cleanly.

### "The Cowork plugin URL paste did nothing visible."

Cowork's plugin install field accepts the URL silently and shows no progress indicator for the first 2-5 seconds while it resolves. If you paste-and-immediately-click-away, you may miss the success state.

What to check:
- Wait 5-10 seconds after pasting before assuming it failed.
- Open Cowork's plugin list (Settings → Plugins) — the new plugin appears there once install completes, even if no toast notification fires.
- If the plugin doesn't appear in the list after 30 seconds: the URL was probably rejected. See "URL paste did nothing" in the Pre-install section above.

### "The Claude Code install ran but `claude` doesn't see the skill."

The Code install copies the bundle to `~/.claude/skills/obsidian-company-memory/`. Code reads that directory at startup; if it was already running when you ran the install, it won't pick up the new skill until you restart.

What to do:
- Exit Code completely (close all sessions, including any in IDEs).
- Re-open Code.
- The skill should appear via its trigger phrases or `/obsidian-company-memory`.

If still not visible:
- Verify the install actually ran: `ls ~/.claude/skills/obsidian-company-memory/SKILL.md` should exist.
- Check Code's loaded-skills list: `claude --list-skills` (or your version's equivalent).
- If `SKILL.md` exists but Code doesn't list it: your Code version may pre-date user-global skills. Update Code and retry.

### "git clone fails with permission denied / SSL error / proxy error."

The canonical install URL uses HTTPS (`https://github.com/absolutionlabs/...`). Plain `git clone` should work without authentication.

If it fails:
- **Permission denied (publickey):** You're trying to clone via SSH (`git@github.com:...`) without an SSH key configured. Use the HTTPS URL instead.
- **SSL certificate problem:** Your corporate proxy is intercepting HTTPS and presenting its own cert. Either configure git to trust the proxy cert (ask IT) or download the zip from the GitHub web UI as a workaround.
- **Could not resolve host:** DNS is blocking `github.com`. Check with IT. Workaround: tether off mobile data for the install, then move the folder to your work machine.
- **fatal: unable to access ... 403:** Rate limit or geographic block. Try again in 60 seconds; if persistent, surface to `info@absolutionlabs.com`.

### "Downloaded the zip but the extracted folder structure looks wrong."

Common Windows symptom: double-clicking a `.zip` file opens it in a preview-only view, and dragging "the folder" out gives you a folder containing the zip's internal folder — i.e. nested one level deeper than expected.

What to check:
- Open the extracted folder. You should see `SKILL.md`, `README.md`, `LICENSE`, `templates/`, `docs/` at the top level.
- If instead you see ONE folder named `obsidian-company-memory-main/` or similar, descend into it — that's the actual bundle root.

What to do:
- Move the inner folder's contents up one level, OR install from the deeper level. Both work.
- For Code installs, the `~/.claude/skills/obsidian-company-memory/` folder must directly contain `SKILL.md`, not contain another folder that contains `SKILL.md`.

### "The integrity check says 'missing files' but I can see them all."

Filesystem case-sensitivity disagreement. The skill expects exact-case filenames (`SKILL.md`, not `skill.md`). Most cases:

- **Windows:** filenames are case-insensitive at the OS level, but some download tools normalise case during extraction (e.g. all-lowercase). If the bundle was zipped on Linux then extracted via a Windows tool that lowercases, the integrity check fails.
- **macOS:** the default APFS volume is case-insensitive, but some external drives are case-sensitive. The same all-lowercase-after-extraction failure mode can appear.

What to do:
- Re-download via `git clone` directly (git preserves case on the wire).
- If you must use the zip path: extract using `tar -xf bundle.zip` from a terminal rather than a GUI tool — tar preserves case more reliably than Explorer / Finder.

---

## File and folder structure confusions

The vault is plain markdown in a folder you own. Sounds simple; trips users up because of OS quirks around hidden folders and the difference between "the folder Obsidian sees" and "the folder on disk."

### "I see SCHEMA.md and the folders in Obsidian, but `.obsidian/` isn't visible."

Working as designed. `.obsidian/` is a hidden folder (leading dot) holding Obsidian's own config. Obsidian deliberately doesn't list its own config folder in its file explorer.

To see `.obsidian/` from your OS file manager:
- **macOS Finder:** press `Cmd + Shift + .` to toggle hidden file visibility.
- **Windows Explorer:** View tab → tick "Hidden items".
- **Linux file managers:** `Ctrl + H` toggles hidden-file visibility in most (Files, Nautilus, etc.).

You should rarely need to look at `.obsidian/` directly; if you do (e.g. troubleshooting plugin config), it lives at the vault root alongside SCHEMA.md.

### "I see different things in Obsidian than I see on disk."

Two real causes:

1. **Obsidian filters by file type.** It shows `.md`, `.canvas`, images, PDFs by default; not `.template`, `.txt`, `.yml`, `.json`. The `CLAUDE.md.template` and `AGENTS.md.template` files at the vault root are invisible in Obsidian's file explorer. They're on disk; the AI tool reads them at session start.
2. **`.obsidian/` is hidden** (see above).

What to check on disk to confirm everything is there:
```
<vault-root>/
├── SCHEMA.md
├── CONTEXT.md
├── index.md
├── log.md
├── HOW-TO-USE-THIS.md
├── CLAUDE.md.template
├── AGENTS.md.template
├── concepts/claude-operating-principles.md
├── entities/test-welcome.md
├── _meta/expectations.yml
├── _meta/scaffold-version.txt
├── _meta/templates/{entity,concept,query}.md
├── _meta/skill-prompts/{README,open-obsidian-project,close-obsidian-project}.md
└── .obsidian/{app,appearance,core-plugins,community-plugins,hotkeys}.json
```

Missing files = either partial scaffold (re-run on empty folder) or sync hasn't caught up yet.

### "Obsidian shows lots of files I don't recognise (`.canvas`, `workspace.json`, etc.)"

`.obsidian/workspace.json` and similar files are Obsidian's runtime state — your open tabs, sidebar widths, etc. They appear after you start using Obsidian; the skill doesn't write them. Ignore unless something specifically refers to them in troubleshooting (e.g. corrupt-workspace recovery above).

Empty `.canvas` files appear if you accidentally created one via the file menu. Safe to delete from the file explorer.

### "I moved the vault folder and the wikilinks broke."

Wikilinks are relative to the vault root, not the OS path. Moving the vault folder should NOT break links — but Obsidian may need to be told.

What to do:
1. In Obsidian: File → Open vault → "Open folder as vault" at the NEW path.
2. Close any old vault entries from Obsidian's vault list (they'll show as "missing" with the old path).
3. The wikilinks should now resolve. If they don't: in the new vault, Settings → Files & Links → "Use [[Wikilinks]]" must be ON (the scaffold sets this; manual edits may have flipped it).

### "I renamed the vault folder and now my AI session can't find SCHEMA.md."

The AI session uses an absolute path. If you renamed `~/Dropbox/MyCompany/` to `~/Dropbox/AcmeCorp/`, your AI tool still remembers the old path.

What to do:
- In your next AI session, explicitly mount the new path (Cowork: `request_directory` with the new absolute path; Code: `cd` to the new folder before invoking).
- Update `_meta/scaffold-version.txt` and `_meta/expectations.yml` if they contain hard-coded paths (they shouldn't, but check after major renames).
- The skill-prompts in `_meta/skill-prompts/` reference `{{VAULT_ABSOLUTE_PATH}}` substituted at scaffold time. If you renamed the vault, re-substitute manually with sed / Find-and-Replace on those files only.

### "The vault folder has a `(1)` or `-Copy` suffix and Obsidian opens it as a separate vault."

You triggered a duplicate via your file manager or cloud sync. The duplicated folder may have outdated content.

What to do:
1. Identify which folder is the "real" vault (check `_meta/scaffold-version.txt` for the scaffold date — the older one usually is).
2. Manually merge any newer content from the duplicate into the original.
3. Delete the duplicate.
4. Re-open the original in Obsidian; close the duplicate from Obsidian's vault list.

---

## Incompatibilities not already covered in COMPATIBILITY.md

[COMPATIBILITY.md](../COMPATIBILITY.md) lists the verified matrix. This section covers the edge cases users hit that aren't reflected in the matrix because they're environmental (corporate policy, security software, locale-specific behaviour) rather than version-specific.

### "macOS Gatekeeper / 'Obsidian is from an unidentified developer'"

Obsidian's installer is signed but some macOS configurations still prompt this on first launch (older OS, restrictive security profile).

What to do:
- Right-click the Obsidian.app in Applications → Open. Confirm the "open anyway" dialog.
- Or: System Settings → Privacy & Security → scroll to "Allow apps from" and grant Obsidian permission.
- This is about Obsidian, not the skill. Once Obsidian runs, the scaffolded vault works normally.

### "Windows Defender SmartScreen blocked the install script."

Some Windows configurations flag scripts downloaded via `curl | sh` as untrusted.

What to do:
- Click "More info" → "Run anyway" if you trust the source (the install script is open-source on GitHub; inspect before running if uncertain).
- Or: download the script directly from GitHub, inspect it (~30 lines), run it locally without piping. The script does a `git clone` + `mv` — nothing system-level.

### "Corporate proxy blocks `vujwcvqiwwpncnhgxjsu.supabase.co` (telemetry endpoint)."

Telemetry failures are non-blocking. The install proceeds and your vault works. The success ping just doesn't reach our endpoint.

What to do (if you want telemetry to land anyway):
- Ask IT to allowlist `*.supabase.co` for outbound POST (the endpoint is EU-hosted, GDPR-compliant, no PII).
- Or: send a one-line email to `info@absolutionlabs.com` confirming your install succeeded; we can manually log it for funnel data.
- Or: ignore. The vault is fully functional without telemetry.

### "Obsidian's plugin browser is blocked by corporate policy."

Dataview is strongly recommended but optional (per COMPATIBILITY.md). If your IT blocks Obsidian's plugin browser, you can:

1. **Skip Dataview entirely.** The vault works; you lose structured queries against frontmatter (the lint's threshold report will fall back to a plain-text scan).
2. **Manually install Dataview.** Download the plugin from its GitHub releases page, place `main.js`, `manifest.json`, `styles.css` in `<vault>/.obsidian/plugins/dataview/`. Enable from Obsidian's Community Plugins panel (which lists installed-but-not-marketplace plugins separately).
3. **Ask IT for an exception.** Dataview is widely-deployed in enterprise Obsidian setups; the request usually gets approved.

### "Obsidian fails to launch with 'electron / native module' error after install."

Usually a Linux distro mismatch — Obsidian's AppImage was built against a glibc version newer than your system.

What to do:
- Use Obsidian's deb / Snap / Flatpak install instead of AppImage if available.
- Or: upgrade your distro's glibc (typically requires a distro version bump).
- Or: run Obsidian via Flatpak — it bundles its own runtime.

### "iCloud Drive 'optimised storage' evicted the vault and now it's slow."

iCloud's "Optimise Storage" setting can offload rarely-accessed files to the cloud, leaving a stub on disk. Opening the vault triggers a download — first launch can be slow.

What to do:
- Finder → navigate to the vault folder → right-click → "Keep on this Mac" (or "Keep Downloaded").
- All files now stay local. iCloud still syncs changes but won't evict.

### "Dropbox Smart Sync did the same."

Same shape, different provider. Right-click the vault folder in Finder / Explorer → "Available Offline" / "Make available offline". Stays local; sync continues.

### "Locale produces unexpected date format in `expectations.yml`."

The skill auto-detects locale and writes `date_format_preference` to `_meta/expectations.yml`. If you see DD/MM when you expected MM/DD (or vice versa), the OS locale at install time was the source.

What to do:
- Edit `_meta/expectations.yml` directly. Change the `date_format_preference` line to what you want. Save.
- This is informational only — YAML frontmatter dates in pages remain ISO `YYYY-MM-DD` because the lint depends on it. The preference affects body text only.

### "I'm on a regulated Windows tenant with Microsoft Defender for Cloud Apps in front of all SaaS."

Defender for Cloud Apps may flag the Supabase telemetry POST as "shadow IT" and block it. Same answer as the proxy section above: install proceeds, telemetry fails silently. If your security team needs to allowlist: the endpoint is `vujwcvqiwwpncnhgxjsu.supabase.co` (EU-hosted, anonymous payload, public privacy policy at [absolutionlabs.com/privacy](https://absolutionlabs.com/privacy)).

### "The skill ran but my MDM-managed Windows blocks creation of `.obsidian/`."

Some Windows MDM policies forbid creation of dot-prefixed folders in user directories. The skill writes `.obsidian/` as a normal folder; the OS rejects it.

What to do:
- Install the vault outside the MDM-managed user directory (e.g. on a personal drive partition, or in `C:\Vaults\` with an exception requested from IT).
- Ask IT to grant your user account an exception for the chosen vault path.
- This is a tenant-specific block; we can't bypass it from the skill side.

---

## Escalation

If nothing here describes what you're seeing, or the recovery steps don't work:

- **Email `info@absolutionlabs.com`**. Include:
  - OS + version
  - Agent CLI (Cowork / Claude Code / Codex / opencode) + version
  - Cloud sync provider
  - Exact error message or unexpected behaviour
  - If install partially completed: contents of `_meta/scaffold-version.txt`
  - What you've already tried
- **Response SLA: one business day.** Replied to by a human at Absolution Labs (not a bot).
- **Security issues only: `security@absolutionlabs.com`** instead of `info@`. Same SLA. We won't ask you to wait for a CVE.

---

*Cross-references: [README.md](../README.md), [SKILL.md](../SKILL.md), [COMPATIBILITY.md](../COMPATIBILITY.md), [upgrading.md](upgrading.md), [templates/HOW-TO-USE-THIS.md](../templates/HOW-TO-USE-THIS.md).*

---

## Use at your own risk

This document is part of the Obsidian Company Memory bundle, provided "AS IS" without warranty of any kind under the MIT License. It is for general informational and educational purposes only and does not constitute professional advice. The recovery steps above describe approaches that have worked for us in testing; they are not guaranteed to recover any specific failure scenario, and following them may produce unintended consequences in environments we have not tested. **Read [DISCLAIMERS.md](../DISCLAIMERS.md) in full before installing, forking, or relying on anything in this repository.**

*© 2026 Absolution Labs. AbsolutionLabs Ltd, registered in England and Wales (Company No. 17091663). Registered office: 15 Westbury Road, London SE20 7QL.*
