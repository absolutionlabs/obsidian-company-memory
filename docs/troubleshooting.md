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

- Your firewall blocks `telemetry.absolutionlabs.com`.
- Cloudflare had a brief outage.
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
- **Security issues only: `security@absolutionlabs.com`** instead of `support@`. Same SLA. We won't ask you to wait for a CVE.

---

*Cross-references: [README.md](../README.md), [SKILL.md](../SKILL.md), [COMPATIBILITY.md](../COMPATIBILITY.md), [upgrading.md](upgrading.md), [templates/HOW-TO-USE-THIS.md](../templates/HOW-TO-USE-THIS.md).*
