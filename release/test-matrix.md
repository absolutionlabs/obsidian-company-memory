# Test matrix — 7 personas

Before any public release, run the install against each of the 7 personas below. **Each persona is a hard gate** — a failure on any one blocks public ship. Document outcomes in `release/test-matrix-runs/<date>.md` (create the folder when first run).

The matrix maps 1:1 to the 6 assumptions + the pre-mortem failure shape captured in our internal project brief. The bundle survives this matrix or it doesn't ship.

The matrix below is current for v1.2.1+. Earlier versions (v1.0.0–v1.2.0) used a different install paradigm (URL-paste of `plugin.json`) and a 3-checkbox compliance gate; if you find yourself running the matrix against an earlier version, the install procedure and pass criteria don't match. Re-cut to the current version before running.

---

## How to run a persona

For each persona row below:

1. Read the **Setup** column. Get the environment into the described state.
2. Run the **Install procedure** column. Follow the SKILL.md flow as the persona would.
3. Compare every observation to the **Pass criteria** column.
4. Record results: every check is either `PASS` or `FAIL — <one-line reason>`.
5. If any check fails, **stop the persona run** and document the failure. Do not work around it.

A persona "passes" only when all checks in its row pass. Partial passes do not count.

---

## Persona 1 — Cold Mac, Cowork install

| | |
|---|---|
| **Setup** | A Mac (12+) with Obsidian downloaded but no vault created. A fresh Dropbox folder named `CompanyMemory-Test/` (empty). A Cowork account with no prior install of this skill. The Mac has not been used for development; assume zero terminal experience for this persona. |
| **Install procedure** | Download all three zips from the [latest GitHub Release](https://github.com/absolutionlabs/obsidian-company-memory/releases/latest). Open Cowork → Skills → Upload skill → drag-drop each zip (companions first, main last). Start a new conversation: "Set up my Obsidian company memory." Follow the prompts. |
| **Pass criteria** | (a) all three skills appear in the Cowork skills list after upload, with v1.2.1+ versions shown in the description; (b) the main skill is invoked successfully via the "Set up my Obsidian company memory" prompt; (c) compliance gate appears with a one-line passive privacy preamble + 2 checkboxes (NOT 3 — v1.2.1 cut the third); (d) refuses to scaffold into a non-empty folder when retested with `~/Downloads`; (e) 2-question intake (company name + sync provider); (f) ~20 files land in the test folder; (g) round-trip test creates `entities/test-welcome.md` + index updated + log appended; (h) Phase 2 guide handoff renders cleanly; (i) the final message names both companion skills as installed (or, if they weren't uploaded, tells the user where to get them on the GitHub Release). |
| **Why this persona matters** | This is the modal user. Failure here is failure of the v1 promise. |

---

## Persona 2 — Cold Windows, Cowork install

| | |
|---|---|
| **Setup** | Windows 10 or 11 with Obsidian downloaded but no vault. An empty folder in OneDrive (personal, not Business) named `CompanyMemory-Test\`. Cowork account, no prior install. |
| **Install procedure** | Same as Persona 1 — download the three zips from the GitHub Release, drag-drop each into Cowork → Skills → Upload skill, then invoke. |
| **Pass criteria** | All (a)–(i) from Persona 1, plus: (j) Windows path handling works (backslashes don't break wikilinks; the scaffold uses forward slashes inside vault references); (k) `app.json` config points at `raw/assets` not `raw\assets`. |
| **Why this persona matters** | Windows is half the prospect base and the most likely persona to surface path-separator bugs. |

---

## Persona 3 — Dropbox-for-Business

| | |
|---|---|
| **Setup** | macOS or Windows + Dropbox-for-Business client (NOT personal Dropbox). An empty folder inside the synced location. Confirm Dropbox is fully synced (no "Syncing..." indicator in menu bar) before starting. |
| **Install procedure** | Same as Persona 1. Watch for: scaffold pauses > 10s on any single file write (indicates Dropbox throttling). |
| **Pass criteria** | All (a)–(i), plus: (l) no individual file write blocks for > 10s; (m) post-install, every scaffolded file appears in the Dropbox web UI within 5 minutes; (n) no "conflicted copy" files generated; (o) `.obsidian/` folder syncs without "Skipping due to .ignore" warnings. |
| **Why this persona matters** | Regulated-sector prospects are disproportionately on Dropbox-for-Business; this is the hard mode for cloud sync. The brief's Threat-Map surface #6 specifically called out tenant-level controls on `.obsidian/`. |

---

## Persona 4 — OneDrive-for-Business

| | |
|---|---|
| **Setup** | Windows + OneDrive-for-Business with "Known Folder Move" either ON or OFF (test both if time permits). Empty test folder under a path the user controls — NOT `Documents/`, `Desktop/`, or `Pictures/` (those may be redirected by KFM). |
| **Install procedure** | Same as Persona 1. |
| **Pass criteria** | All (a)–(i), plus: (p) post-install vault is at the path the user picked, not silently relocated under a OneDrive-managed redirect; (q) Files-On-Demand setting respects the vault (no "Free up space" stub icons on scaffolded files); (r) tenant policy doesn't block `.obsidian/` writes (if it does, the skill surfaces the failure clearly, not silently). |
| **Why this persona matters** | OneDrive-for-Business tenants are the second-largest regulated-sector cloud surface; KFM is the most common path-rewriting failure mode the skill could hit. |

---

## Persona 5 — iCloud Drive

| | |
|---|---|
| **Setup** | macOS only. Empty folder inside `~/Library/Mobile Documents/com~apple~CloudDocs/` (the canonical iCloud path). Optimised Storage **on** for the test, then re-run with it off if the first pass fails. |
| **Install procedure** | Same as Persona 1. |
| **Pass criteria** | All (a)–(i), plus: (s) post-install, all scaffolded files have local copies (not "in cloud" ghost icons in Finder); (t) the vault opens in Obsidian without prompting to "download from iCloud"; (u) round-trip test wikilink resolves immediately, not after a download delay. |
| **Why this persona matters** | iCloud's "Optimised Storage" can evict the vault and break load-on-demand. macOS is the second platform; this combination is common among indie founders. |

---

## Persona 6 — MDM-managed Windows device

| | |
|---|---|
| **Setup** | A Windows device under an organization's MDM (Intune, Workspace ONE, or similar). Test on an actual managed device — do not simulate. Empty folder in a location the user has write access to (not a corporate-managed path). |
| **Install procedure** | Same as Persona 1. Watch for: silent file-write refusals from group policy; AppLocker blocks; restricted-execution warnings on Obsidian. |
| **Pass criteria** | All (a)–(i), plus: (v) every file write succeeds OR the skill surfaces an explicit "blocked by policy" error (no silent failures); (w) Obsidian launches; (x) the user can reach the GitHub Release page to download zips (i.e. egress to github.com isn't blocked by the proxy — if it is, that's a documented failure with a clear remediation path, not a silent break). If the MDM blocks the install entirely: that's a valid pass for the persona ONLY if the skill's error message clearly says what's blocked and recommends an action the user can take. |
| **Why this persona matters** | The brief's pre-mortem specifically called this out. Regulated-sector founders often own personal laptops but use MDM-managed work laptops. Failing silently here is the kind of incident the brief was designed to prevent. |

---

## Persona 7 — Existing-vault user

| | |
|---|---|
| **Setup** | A user who already has an Obsidian vault with real content (theirs, not synthetic). Target the install at a NEW empty folder (not at the existing vault). The existing vault must remain untouched throughout. |
| **Install procedure** | Same as Persona 1, into the new empty folder. Then, after install completes, deliberately try to re-run the install against the existing vault folder. |
| **Pass criteria** | All (a)–(i) on the new folder, plus: (y) the existing vault is untouched (verify by hash before + after, OR by `git status` if the user version-controls it); (z) the deliberate re-run against the existing vault refuses cleanly with the refuse-to-scaffold message; (aa) no path in either vault was created, modified, or deleted. |
| **Why this persona matters** | The pre-mortem's worst-case data-loss scenario. The refuse-to-scaffold gate is the structural defense; this persona is the structural test. |

---

## Persona run record template

Use this for each persona run. Save to `release/test-matrix-runs/<YYYY-MM-DD>-<persona-N>.md`:

```markdown
# Persona N — <name> — <YYYY-MM-DD>

**Tester:** <name or "Rob (operator)">
**Device:** <OS + version>
**Sync provider:** <provider>
**Skill version tested:** <semver>
**Telemetry UUID generated:** <uuid>

## Setup checklist
- [ ] Environment matches "Setup" column
- [ ] Test folder is empty (verified before install)
- [ ] Obsidian installed but no vault loaded
- [ ] Recording enabled (screen recording during install — kept until persona passes)

## Pass criteria results
(a) … PASS / FAIL — …
(b) … PASS / FAIL — …
…

## Failures (if any)
- <one paragraph per failure: what happened, what was expected, screenshots/log paths>

## Outcome
**OVERALL: PASS / FAIL**
```

---

## Gate logic

- **All 7 personas pass** → public ship is unblocked (subject to Recovery Drill + private beta gate).
- **Any persona fails** → fix the underlying issue, bump the skill version, re-run the failing persona (not the whole matrix).
- **Persona 6 (MDM) is the only one where a "clean error" counts as a pass**, because MDM policies are outside the skill's control. The skill's job there is to fail loudly, not to succeed.

---

## Time estimate

| Persona | Realistic time |
|---|---|
| 1 (Cold Mac) | 30 min |
| 2 (Cold Windows) | 30 min |
| 3 (Dropbox-for-Business) | 45 min (sync verification adds time) |
| 4 (OneDrive-for-Business) | 60 min (KFM testing both states) |
| 5 (iCloud) | 30 min |
| 6 (MDM) | 60 min (testing inside the MDM constraints) |
| 7 (Existing-vault) | 45 min (verifying the existing vault stays intact) |
| **Full matrix** | ~5 hours operator-time |

Run over 1-2 sessions. Don't compress all into one sitting — fatigue causes false PASSes.

---

*Each persona maps to a row of the brief's assumption table or pre-mortem failure shape. Failure on any row is a blocker; defer the persona's release until the underlying issue is addressed.*
