# Compatibility Matrix

Tested combinations for **Obsidian Company Memory v1.0.0**. Last updated: 2026-06-02.

This skill is intentionally lightweight — markdown + YAML + JSON files only, no shipped binaries, no platform-specific code paths. Compatibility risk is therefore concentrated in two places: the agent CLI (Cowork / Claude Code / Codex / opencode) and the cloud sync provider's behaviour around the `.obsidian/` folder.

The matrix below reflects what we have tested ourselves. **"Not tested" does NOT mean "doesn't work"** — it means we haven't verified. If you successfully install on a combination we haven't tested, please [send us a one-line report](mailto:info@absolutionlabs.com?subject=Compatibility%20report%20Obsidian%20Company%20Memory) so we can add it.

---

## Operating systems

| OS | Versions tested | Status | Notes |
|---|---|---|---|
| macOS | 12 Monterey, 13 Ventura, 14 Sonoma, 15 Sequoia | ✅ Verified | All paths resolve cleanly via Cowork's mounted-directory access. |
| Windows | 10 (22H2), 11 (23H2, 24H2) | ✅ Verified | Path separator handling tested; long-path support not required. |
| Linux | Ubuntu 22.04, Ubuntu 24.04, Fedora 40, Debian 12 | ⚠️ Partial | Tested on Ubuntu; Fedora + Debian unverified but no known reason to fail. |
| ChromeOS | — | ❌ Not tested | Likely works via Linux container; unverified. |
| iOS / iPadOS | — | ❌ Not tested | Obsidian mobile + Cowork mobile both exist but the install flow assumes a desktop file picker. Out of scope for v1. |

---

## Agent CLIs

The skill is dual-surface: Cowork plugin OR Claude Code user-global skill. Other CLIs are not first-class but the scaffolded vault works fine with any agent that reads `CLAUDE.md` / `AGENTS.md`.

| Agent | Install path | Status | Notes |
|---|---|---|---|
| **Cowork** | Plugin URL install | ✅ Primary | Tested against Cowork as of 2026-06. Plugin install via shareable URL works without marketplace listing. |
| **Claude Code** | One-line `curl \| sh` into `~/.claude/skills/` | ✅ Primary | Tested on Code v0.5+. Skill loads as a user-global skill, fires on trigger phrases or `/obsidian-company-memory`. |
| **Codex** | Reads scaffolded `AGENTS.md` | ⚠️ Compatible (not first-class) | Codex doesn't have a skill mechanism, but the scaffolded vault works fine — Codex reads `AGENTS.md` at session start and follows the close protocol. |
| **opencode** | Reads scaffolded `AGENTS.md` | ⚠️ Compatible (not first-class) | Same as Codex. opencode also honours `AGENTS.md`. |
| **Other** | — | ❌ Not tested | Anything that reads `CLAUDE.md` or `AGENTS.md` should work. Anything that doesn't may need a custom session opener. |

---

## Obsidian

| Obsidian version | Status | Notes |
|---|---|---|
| 1.5.x | ✅ Minimum supported | The `.obsidian/app.json` config uses fields stable since 1.5. |
| 1.6.x – 1.9.x | ✅ Verified | All current configs work without modification. |
| < 1.5 | ❌ Unsupported | Some config fields not present; scaffold may load with defaults instead of our config. |
| Obsidian Insider builds | ⚠️ Best-effort | Pre-release builds may introduce config changes we haven't tested against; please report issues. |

---

## Community plugins (user-installed, not bundled)

The skill does NOT ship plugin binaries (deliberate cut per key decision #6). Users install plugins from inside Obsidian's plugin browser. The following are recommended; the skill works without them.

| Plugin | Recommendation | Tested with | Notes |
|---|---|---|---|
| **Dataview** | Strongly recommended | v0.5.67+ | Powers structured queries against the wiki frontmatter. The `_meta/expectations.yml` thresholds + lint queries assume Dataview is present. |
| **Templater** | Not recommended | — | Deliberately cut (key decision #7). The skill ships plain markdown templates in `_meta/templates/`; Templater is unnecessary. If you install it anyway, no conflict. |
| **Other** | Your call | — | Any community plugin you install lands in `.obsidian/plugins/` and is invisible to the skill. No conflicts expected. |

---

## Cloud sync providers

The skill writes ~20 files plus the `.obsidian/` config to your vault folder. All providers tested handle this without issue, but each has quirks worth knowing.

| Provider | Status | Notes / quirks |
|---|---|---|
| **Dropbox (personal)** | ✅ Verified | Fastest sync of the providers tested. No special handling required. |
| **Dropbox for Business** | ⚠️ Caveat | Some Business accounts apply per-second write limits to `.obsidian/`. If you see scaffold pauses > 10s, the skill surfaces a notice and suggests pausing Dropbox sync, completing the install, and resuming sync. |
| **iCloud Drive** | ✅ Verified | macOS-native. iCloud's "Optimised Storage" can evict the vault to the cloud; pin the folder locally (Finder → right-click → "Keep on this Mac") to avoid load-on-demand delays. |
| **OneDrive (personal)** | ✅ Verified | Works without modification. |
| **OneDrive for Business** | ⚠️ Caveat | Tenant-level "Known Folder Move" can rewrite paths under your feet; install into a folder you control, not `Documents` or `Desktop` which may be redirected. |
| **Google Drive (Desktop)** | ⚠️ Caveat | Sync latency is higher than Dropbox; expect 30-60s for changes to appear on other devices. Doesn't affect the install itself. |
| **Box / pCloud / Sync.com** | ❌ Not tested | Should work; please report. |
| **MEGA** | ❌ Not tested | Should work; please report. |
| **No sync (local-only)** | ✅ Verified | Vault is on local disk only. Skill surfaces a note recommending quarterly zip backups. |
| **MDM-managed Windows** | ⚠️ In test | Group policy can block `.obsidian/` writes. Tested against one MDM tenant successfully; broader testing pending Chunk 7. |

---

## Languages / locales

The skill auto-detects your system locale and sets the date-format preference accordingly (per SKILL.md Step 4). Tested locales:

| Locale | Date format used | Status |
|---|---|---|
| `en-GB` | DD/MM/YYYY | ✅ |
| `en-US` | MM/DD/YYYY | ✅ |
| `en-AU`, `en-IE`, `en-NZ`, `en-CA` | DD/MM/YYYY or MM/DD/YYYY per region | ✅ |
| `fr-*`, `de-*`, `es-*`, `it-*`, `nl-*`, `pt-*` | DD/MM/YYYY | ✅ |
| `ja-*`, `zh-*`, `ko-*` | YYYY-MM-DD | ✅ |
| Anything else | YYYY-MM-DD (ISO) fallback | ✅ |

Note: regardless of date-format preference, all YAML frontmatter dates in scaffolded files use ISO `YYYY-MM-DD` because the lint logic depends on it. The preference is informational (used by downstream tools that respect it).

---

## What "not compatible" looks like

If the skill genuinely can't run on your combination, you'll see a clear error message — not a silent half-scaffold. The skill's pre-flight refuses early and tells you which check failed:

- **Worktree detected:** ran from inside a git worktree (per OP #19). Relaunch from main checkout.
- **Skill bundle incomplete:** missing template files. Re-install from canonical URL.
- **Target folder not empty:** existing files in the vault folder. See [docs/troubleshooting.md](docs/troubleshooting.md).
- **No write access to target:** OS permissions or cloud sync lock. See [docs/troubleshooting.md](docs/troubleshooting.md).
- **Telemetry endpoint unreachable:** non-blocking; install continues.

---

## Reporting incompatibilities

If you hit an issue we haven't documented, email `info@absolutionlabs.com` with:

- Your OS + version
- Your agent CLI + version
- Your cloud sync provider
- The exact error or unexpected behaviour
- (If the install partially completed) the contents of `_meta/scaffold-version.txt` if it exists

We respond within one business day. Confirmed incompatibilities land in this file on the next quarterly refresh.

---

## Refresh cadence

This matrix is updated quarterly (next refresh: 2026-09-02). The refresh:

1. Re-runs the install on the latest Obsidian + Cowork + Claude Code versions
2. Adds any confirmed user reports from `info@absolutionlabs.com`
3. Drops support for OS / Obsidian versions that have reached EOL upstream
4. Bumps the "Last updated" line at the top of this file

If you depend on a specific combination staying tested: tell us, and we'll add it to the quarterly run.

---

*Maintained by Absolution Labs LTD. Cross-references: [README.md](README.md), [SKILL.md](SKILL.md), [docs/troubleshooting.md](docs/troubleshooting.md), [docs/upgrading.md](docs/upgrading.md).*
