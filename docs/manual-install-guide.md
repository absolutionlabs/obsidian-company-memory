# Manual install guide

A by-hand installation procedure for **Obsidian Company Memory v1.2.0** without using the Cowork plugin or the Claude Code skill. Produces a vault byte-identical to the skill-installed one, plus the two companion skills (`open-obsidian-project`, `close-obsidian-project`) installed alongside.

**Estimated time:** 45–60 minutes if you follow along carefully. The skill path is ~25 minutes; manual is slower because you do the substitutions and file copies yourself.

If this guide is wrong in any specific way, email `info@absolutionlabs.com` and we'll fix it.

---

## When to use this guide (and when NOT to)

**Use this guide if any of these is true:**

- You use an AI tool other than Cowork or Claude Code (Codex, opencode, or anything else that reads `CLAUDE.md` / `AGENTS.md`) and the skill install paths don't reach you.
- You're in a regulated sector and want to inspect every file before it touches your disk.
- Your corporate proxy / firewall blocks the skill install paths (Cowork plugin URL rejected, Claude Code `curl | sh` blocked).
- You're forking the bundle and want a clean by-hand install of your variant.
- The skill failed mid-scaffold twice and you want a self-serve recovery path before emailing support.

**Do NOT use this guide if:**

- You have Cowork or Claude Code. The skill is canonical, ~20 minutes faster, and verified. Use it via the install URL on [absolutionlabs.com](https://absolutionlabs.com).
- You want to install into a folder that already has files. The skill refuses non-empty targets by design (key decision #14); this guide inherits the refusal. Use an empty folder.
- You want to "merge" the bundle with an existing vault. Out of scope; email `info@absolutionlabs.com` for a guided migration.
- You're trying to install Obsidian itself, or your agent CLI. This guide assumes both already work on your machine.

---

## Section 1 — Prerequisites

Before you start, you need:

1. **Obsidian installed locally.** Download from [obsidian.md](https://obsidian.md/download). 1.5+ required ([COMPATIBILITY.md](../COMPATIBILITY.md)).
2. **An empty folder** inside a sync provider (Dropbox / iCloud / OneDrive / Google Drive) or local-only.
3. **A terminal** (Terminal.app on macOS, Windows Terminal or PowerShell on Windows, any shell on Linux).
4. **Basic ability to edit JSON, YAML, and Markdown files** in a text editor. Notepad / TextEdit work; a real editor (VS Code, Sublime Text, Obsidian itself) is better.
5. **An AI tool that reads `CLAUDE.md` or `AGENTS.md`** at session start, with the ability to be pointed at a local folder.

If any of these is missing, resolve it before continuing.

### Quick prerequisites check

Run from your terminal:

**macOS / Linux:**

```bash
obsidian --version 2>/dev/null || echo "Obsidian not on PATH (open from Applications)"
test -d ~/path/to/your/empty-folder && echo "Folder exists" || echo "Create the folder first"
which git && echo "git OK" || echo "Install git (recommended)"
```

**Windows (PowerShell):**

```powershell
Test-Path "C:\path\to\your\empty-folder"
git --version
```

If you don't have `git`, you can use the zip download path in Section 2 instead. `git` is recommended because it preserves filename casing more reliably (see [troubleshooting.md § Bundle download issues](troubleshooting.md#bundle-download-issues)).

---

## Section 2 — Get the bundle

**Recommended: `git clone`.**

```bash
git clone https://github.com/absolutionlabs/obsidian-company-memory.git
cd obsidian-company-memory
```

You should see a top-level structure like this:

```
SKILL.md
README.md
LICENSE
DISCLAIMERS.md
COMPATIBILITY.md
MANIFESTS.md
TESTERS.md
plugin.json
companion-skills/
templates/
docs/
release/
scripts/
website/
```

If you see a single folder named `obsidian-company-memory-main/` or similar at the top, you cloned to a wrapper folder; `cd` into the wrapper folder before continuing.

**Alternative: zip download.**

If `git` isn't available or blocked:

1. Open [https://github.com/absolutionlabs/obsidian-company-memory](https://github.com/absolutionlabs/obsidian-company-memory) in a browser.
2. Click the green Code button → Download ZIP.
3. Extract with `tar -xf` on macOS / Linux, or use Windows Explorer / a tool like 7-Zip on Windows.
4. **Do NOT use Windows Explorer's preview-then-drag method** — it can nest the folder and break case-sensitivity. Use the "Extract All" button or a real extraction tool.

**Verify the bundle is complete.** From inside the bundle folder, the file count should be:

```bash
# macOS / Linux
find . -type f ! -path "./.git/*" | wc -l    # expect ~50 files

# Windows PowerShell
(Get-ChildItem -Recurse -File -Exclude .git).Count
```

If the count is dramatically off, the bundle didn't download cleanly. Re-download.

**For the rest of this guide, `$BUNDLE` refers to the bundle's root folder, and `$VAULT` refers to your target vault folder.**

---

## Section 3 — Self-check the compliance gate

The skill enforces this gate at install time with checkboxes. The manual path asks you to read each item and answer it honestly to yourself before continuing. If you can't answer YES to all three, stop.

> **1. The folder I am about to scaffold into is a folder I own or am authorised to write to. It does not contain any client data, regulated data, or personal data belonging to someone else.**
>
> If you're uncertain, stop and verify. The scaffold writes ~22 files into the folder; if it's not yours to write to, this is the wrong path.

> **2. The cloud sync provider hosting this folder (Dropbox / iCloud / OneDrive / Google Drive / local-only) is one my organisation permits for the type of content I intend to store. I have checked any applicable data processing agreement (DPA) requirements.**
>
> Regulated-sector folders: confirm the DPA covers what you're about to store. This is the box that matters most in finance / legal / healthcare.

> **3. I understand this vault will be a record of facts and decisions about my company. Absolution Labs LTD has no access to its contents at any point. The skill collects no telemetry and does not phone home at install time or afterwards.**

If any answer is NO, stop here. The skill — automated or manual — is not the right path until those answers are YES.

---

## Section 4 — Verify the target folder is empty

The refuse-to-scaffold gate applies to the manual path too. Mixing the bundle with existing files is exactly the failure shape the design prevents.

**macOS / Linux:**

```bash
ls -la "$VAULT"   # expect "total 0" plus . and ..
```

What's allowable:

- `.DS_Store` (macOS Finder metadata) — ignore.
- `Thumbs.db` (Windows Explorer thumbnails) — ignore.
- `desktop.ini` (Windows folder customisation) — ignore.

What's NOT allowable:

- Any `.md` file.
- Any `.obsidian/` folder.
- Any subfolder of any kind.
- Any file that isn't an OS hidden-metadata file.

**Windows PowerShell:**

```powershell
Get-ChildItem $VAULT -Force | Where-Object { $_.Name -notin ".DS_Store","Thumbs.db","desktop.ini" }
```

If the result is empty, the folder is good. If anything appears, **STOP**. Move whatever's there to another folder first, OR pick a different empty folder, OR delete what's there if it's truly empty cruft. Re-run the check.

---

## Section 5 — Substitution variables

This is the section that bites people. The skill ships 5 placeholders that get replaced with your values during install. **One of these has a non-obvious "do not substitute in these files" rule** (Rule 1 below). Get it wrong and the vault works but the lint flags every page as stale immediately.

### The five placeholders

| Placeholder | What it is | How to pick the value |
|---|---|---|
| `{{COMPANY_NAME}}` | Your company name as it should appear in headings, page titles, prose. | 1–80 characters. Letters, digits, spaces, hyphens, ampersands, apostrophes, periods, and corporate suffixes (LTD, Ltd, Limited, Inc, Co). NO angle brackets, braces, pipes, backslashes, backticks, or control characters. |
| `{{TODAY}}` | Today's date in ISO format. | `YYYY-MM-DD` in UTC. Example: `2026-06-03`. |
| `{{VAULT_ABSOLUTE_PATH}}` | The full path to your vault folder. | Absolute path, e.g. `/Users/jane/Dropbox/AcmeCorp` (macOS) or `C:\Users\jane\Dropbox\AcmeCorp` (Windows). |
| `{{PROJECT_NAME}}` | **Leave as literal** in `CLAUDE.md.template` and `AGENTS.md.template`. Substituted later by your `open-obsidian-project` skill. | Do not pick a value at scaffold time. |
| `{{PROJECT_DESCRIPTION}}` | Same — leave as literal. | Do not pick a value at scaffold time. |

### The three substitution-scope carve-outs (READ CAREFULLY)

Rule 1 — `templates/_meta/templates/*.md` (the per-page templates):

> **Substitute `{{COMPANY_NAME}}`. DO NOT substitute `{{TODAY}}`.**
>
> These files are USER-COPY templates. You'll clone them in Obsidian months from now to make new pages. Baking the install date into them defeats the lint's stale-page detection. Leave `{{TODAY}}` as a literal placeholder.

Rule 2 — `companion-skills/open-obsidian-project/SKILL.md` and `companion-skills/close-obsidian-project/SKILL.md`:

> **Substitute NOTHING. Copy verbatim.**
>
> The companion skills auto-install as sibling skills in your AI tool (Section 7f). They read the vault's `_meta/scaffold-version.txt` and `CONTEXT.md` at runtime to know which company / vault path they're operating against. No scaffold-time substitution required. (In v1.0.0 the equivalent files lived in `templates/_meta/skill-prompts/` and required scaffold-time substitution; v1.2.0 moved them to `companion-skills/` and removed the substitution requirement.)

Rule 3 — `templates/CLAUDE.md.template` and `templates/AGENTS.md.template`:

> **Substitute NOTHING. Copy verbatim.**
>
> All five placeholders stay literal. The user's `open-obsidian-project` skill substitutes these at first project invocation, using THAT project's date, not the vault scaffold date.

### Substitution recipes by OS

You'll do most substitutions when you copy each file in Section 7. For batch operations across many files at once, use the recipes below — but apply them carefully, respecting the carve-outs above.

**macOS (BSD sed):**

```bash
# Substitute {{COMPANY_NAME}} across a folder, in-place
find "$VAULT" -type f -name "*.md" -exec sed -i '' "s|{{COMPANY_NAME}}|Acme Corp Ltd|g" {} \;

# Substitute {{TODAY}} across a folder, in-place
find "$VAULT" -type f -name "*.md" -exec sed -i '' "s|{{TODAY}}|2026-06-03|g" {} \;
```

**Linux (GNU sed):**

```bash
find "$VAULT" -type f -name "*.md" -exec sed -i "s|{{COMPANY_NAME}}|Acme Corp Ltd|g" {} \;
find "$VAULT" -type f -name "*.md" -exec sed -i "s|{{TODAY}}|2026-06-03|g" {} \;
```

**Windows (PowerShell):**

```powershell
Get-ChildItem $VAULT -Recurse -Filter "*.md" | ForEach-Object {
    (Get-Content $_.FullName -Raw) -replace '\{\{COMPANY_NAME\}\}', 'Acme Corp Ltd' | Set-Content $_.FullName -NoNewline
}
Get-ChildItem $VAULT -Recurse -Filter "*.md" | ForEach-Object {
    (Get-Content $_.FullName -Raw) -replace '\{\{TODAY\}\}', '2026-06-03' | Set-Content $_.FullName -NoNewline
}
```

**Important:** the batch substitutions above will substitute in EVERY .md file under the vault. If you use them, you must afterwards **revert the carve-outs** — manually re-insert the literal placeholders where they should remain. See Section 12 (Common mistakes) for the specific files and the exact text to put back.

A cleaner approach: skip the batch substitution and substitute per-file as you copy in Section 7. Slower but no carve-out reversal needed.

### Pick your values now

Write these down before starting Section 7. Keep them in front of you.

```
COMPANY_NAME       = ____________________________________
TODAY              = 2026-__-__   (ISO format, UTC)
VAULT_ABSOLUTE_PATH = ____________________________________
DATE_FORMAT        = DD/MM/YYYY  /  MM/DD/YYYY  /  YYYY-MM-DD  (pick one)
SYNC_PROVIDER      = dropbox / icloud / onedrive / google-drive / local-only  (pick one)
```

`DATE_FORMAT` and `SYNC_PROVIDER` are used in `_meta/expectations.yml` and `_meta/scaffold-version.txt` only — not as substitutions in markdown.

---

## Section 6 — Create the vault folder structure

From inside `$VAULT`:

**macOS / Linux:**

```bash
cd "$VAULT"
mkdir -p entities concepts comparisons queries raw raw/articles raw/transcripts raw/assets lint-reports _meta _meta/templates .obsidian
```

**Windows PowerShell:**

```powershell
Set-Location $VAULT
"entities","concepts","comparisons","queries","raw","raw/articles","raw/transcripts","raw/assets","lint-reports","_meta","_meta/templates",".obsidian" | ForEach-Object { New-Item -ItemType Directory -Path $_ -Force | Out-Null }
```

Verify:

```bash
ls -la "$VAULT"   # should show 12 folders (10 visible + . and ..) plus the hidden .obsidian
```

`.obsidian/` is a hidden folder (leading dot). On macOS press `Cmd + Shift + .` in Finder to see it; on Windows enable "Hidden items" in Explorer's View tab.

---

## Section 7 — File-by-file copy and substitute

This is the main write step. Walk every file in order. For each, the source is in `$BUNDLE/templates/...` and the destination is in `$VAULT/...`.

For each file the column "Substitutions" tells you exactly which placeholders to replace. Apply them before saving, using your text editor's Find-and-Replace.

### 7a. `.obsidian/` config files (NO substitutions — JSON, copy verbatim)

| Source | Destination |
|---|---|
| `$BUNDLE/templates/.obsidian/app.json` | `$VAULT/.obsidian/app.json` |
| `$BUNDLE/templates/.obsidian/appearance.json` | `$VAULT/.obsidian/appearance.json` |
| `$BUNDLE/templates/.obsidian/community-plugins.json` | `$VAULT/.obsidian/community-plugins.json` |
| `$BUNDLE/templates/.obsidian/core-plugins.json` | `$VAULT/.obsidian/core-plugins.json` |
| `$BUNDLE/templates/.obsidian/hotkeys.json` | `$VAULT/.obsidian/hotkeys.json` |

**macOS / Linux:**

```bash
cp "$BUNDLE/templates/.obsidian/"*.json "$VAULT/.obsidian/"
```

**Windows PowerShell:**

```powershell
Copy-Item "$BUNDLE\templates\.obsidian\*.json" "$VAULT\.obsidian\"
```

JSON files contain no placeholders. Copy verbatim.

### 7b. Vault-root content files (substitute `{{COMPANY_NAME}}` + `{{TODAY}}`)

| Source | Destination | Substitutions |
|---|---|---|
| `$BUNDLE/templates/SCHEMA.md` | `$VAULT/SCHEMA.md` | `{{COMPANY_NAME}}`, `{{TODAY}}` |
| `$BUNDLE/templates/CONTEXT.md` | `$VAULT/CONTEXT.md` | `{{COMPANY_NAME}}`, `{{TODAY}}` |
| `$BUNDLE/templates/index.md` | `$VAULT/index.md` | `{{COMPANY_NAME}}`, `{{TODAY}}` |
| `$BUNDLE/templates/log.md` | `$VAULT/log.md` | `{{COMPANY_NAME}}`, `{{TODAY}}` |
| `$BUNDLE/templates/HOW-TO-USE-THIS.md` | `$VAULT/HOW-TO-USE-THIS.md` | `{{COMPANY_NAME}}`, `{{TODAY}}` |

For each: copy the file, open in your editor, Find-and-Replace both placeholders, save.

### 7c. Concepts page (substitute `{{TODAY}}` only)

| Source | Destination | Substitutions |
|---|---|---|
| `$BUNDLE/templates/concepts/claude-operating-principles.md` | `$VAULT/concepts/claude-operating-principles.md` | `{{TODAY}}` |

`{{COMPANY_NAME}}` doesn't appear in this file. Just substitute `{{TODAY}}`.

### 7d. `_meta/expectations.yml` (substitute `{{COMPANY_NAME}}` + `{{TODAY}}` + append `date_format_preference`)

| Source | Destination | Substitutions |
|---|---|---|
| `$BUNDLE/templates/_meta/expectations.yml` | `$VAULT/_meta/expectations.yml` | `{{COMPANY_NAME}}`, `{{TODAY}}` |

After substitution, append one new line at the bottom of the file:

```yaml
date_format_preference: DD/MM/YYYY
```

Pick the value matching your `DATE_FORMAT` choice from Section 5. (DD/MM/YYYY for en-GB / European; MM/DD/YYYY for en-US; YYYY-MM-DD for ISO / unknown.)

### 7e. Per-page templates (carve-out Rule 1 — substitute `{{COMPANY_NAME}}` only)

| Source | Destination | Substitutions |
|---|---|---|
| `$BUNDLE/templates/_meta/templates/entity.md` | `$VAULT/_meta/templates/entity.md` | **`{{COMPANY_NAME}}` only**. Leave `{{TODAY}}` as a literal placeholder. |
| `$BUNDLE/templates/_meta/templates/concept.md` | `$VAULT/_meta/templates/concept.md` | **`{{COMPANY_NAME}}` only**. Leave `{{TODAY}}` as a literal placeholder. |
| `$BUNDLE/templates/_meta/templates/query.md` | `$VAULT/_meta/templates/query.md` | **`{{COMPANY_NAME}}` only**. Leave `{{TODAY}}` as a literal placeholder. |

These files become USER-COPY templates inside the vault. When you (or your AI) clone them to make a new entity page in 3 months' time, `{{TODAY}}` should resolve to THAT day, not today. Leave it untouched.

### 7f. Companion-skill install (no substitution required — copy verbatim)

In v1.0.0 the bundle wrote three skill-prompt files into the vault at `_meta/skill-prompts/` and you (the user) manually installed them as custom skills in your AI tool. **In v1.2.0+ the companion skills auto-install alongside the main skill** as sibling skill folders in your AI tool's skill directory, with namespaced names that don't collide with other skills you might have.

For the manual install path, you copy the two companion-skill folders out of the bundle to the appropriate skill-install location for your AI tool:

| Source | Destination (Claude Code) | Substitutions |
|---|---|---|
| `$BUNDLE/companion-skills/open-obsidian-project/` (whole folder) | `~/.claude/skills/open-obsidian-project/` | **None. Copy verbatim.** |
| `$BUNDLE/companion-skills/close-obsidian-project/` (whole folder) | `~/.claude/skills/close-obsidian-project/` | **None. Copy verbatim.** |

**macOS / Linux:**

```bash
cp -r "$BUNDLE/companion-skills/open-obsidian-project" ~/.claude/skills/
cp -r "$BUNDLE/companion-skills/close-obsidian-project" ~/.claude/skills/
# Restart Claude Code so it picks up the new skills.
```

**Windows PowerShell:**

```powershell
Copy-Item -Recurse "$BUNDLE\companion-skills\open-obsidian-project" "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse "$BUNDLE\companion-skills\close-obsidian-project" "$env:USERPROFILE\.claude\skills\"
# Restart Claude Code.
```

**Collision check before copying:** if `~/.claude/skills/open-obsidian-project/` or `~/.claude/skills/close-obsidian-project/` already exists from a previous install, the `cp` will refuse or merge depending on flags. Best practice: `rm -rf` the target only if you intend to overwrite, otherwise rename your existing copy first.

The companion skills require no placeholder substitution — they read the vault's `_meta/scaffold-version.txt` and `CONTEXT.md` at runtime to know which company / vault path they're operating against. Copy verbatim.

**For Cowork / Codex / opencode**, see [companion-skills/README.md](../companion-skills/README.md) in the bundle for the surface-specific install path. The bundle path is the same; only how you register the SKILL.md with your AI tool differs.

### 7g. Project-stub templates (carve-out Rule 4 — substitute NOTHING)

| Source | Destination | Substitutions |
|---|---|---|
| `$BUNDLE/templates/CLAUDE.md.template` | `$VAULT/CLAUDE.md.template` | **None. Copy verbatim with all placeholders literal.** |
| `$BUNDLE/templates/AGENTS.md.template` | `$VAULT/AGENTS.md.template` | **None. Copy verbatim with all placeholders literal.** |

These `.template` files sit at the vault root with the `.template` suffix preserved. They are NOT instantiated; your `open-obsidian-project` skill instantiates them at first project creation. The five placeholders inside (`{{PROJECT_NAME}}`, `{{PROJECT_DESCRIPTION}}`, `{{COMPANY_NAME}}`, `{{VAULT_ABSOLUTE_PATH}}`, `{{TODAY}}`) all get substituted later, with the project's values and date, not the vault scaffold's.

### 7h. Write `_meta/scaffold-version.txt` (no template — build fresh)

Create a new file at `$VAULT/_meta/scaffold-version.txt` containing exactly:

```
skill: obsidian-company-memory
version: 1.2.0
scaffolded: 2026-06-03
date_format_preference: DD/MM/YYYY
sync_provider: dropbox
```

Substitute the three lower lines with your values:
- `scaffolded:` → your `TODAY` value
- `date_format_preference:` → DD/MM/YYYY / MM/DD/YYYY / YYYY-MM-DD
- `sync_provider:` → dropbox / icloud / onedrive / google-drive / local-only

This is the fingerprint downstream tools use to identify your install. No PII.

### 7i. Verify the write batch parses

After all files are in place, sanity-check that each parses:

**JSON (the `.obsidian/` files):**

```bash
# macOS / Linux
for f in "$VAULT/.obsidian/"*.json; do
  python3 -c "import json; json.load(open('$f'))" && echo "$f OK" || echo "$f BROKEN"
done
```

**Windows PowerShell:**

```powershell
Get-ChildItem "$VAULT\.obsidian\*.json" | ForEach-Object {
    try { Get-Content $_.FullName -Raw | ConvertFrom-Json | Out-Null; "$($_.Name) OK" }
    catch { "$($_.Name) BROKEN: $_" }
}
```

**YAML (the `_meta/expectations.yml` file):**

```bash
python3 -c "import yaml; yaml.safe_load(open('$VAULT/_meta/expectations.yml'))" && echo "OK"
```

**Markdown frontmatter** (a handful — open in Obsidian and confirm the rendered page heading shows the company name, not a literal `{{COMPANY_NAME}}`):
- `$VAULT/SCHEMA.md`
- `$VAULT/CONTEXT.md`
- `$VAULT/log.md`

If anything fails to parse, fix it before continuing.

---

## Section 8 — Round-trip test (manual version)

The skill's most important step is the round-trip test: prove the vault works end-to-end by writing one real page, updating index, appending log, and verifying everything renders in Obsidian.

### 8a. Create the test entity

Create `$VAULT/entities/test-welcome.md` with this content (substitute `<company>` and `<today>` with your values):

```markdown
---
title: Welcome to your <company> vault
created: <today>
updated: <today>
type: entity
tags: [welcome, setup]
sources: []
---

# Welcome to your <company> vault

This is the first page in your company memory. It was created automatically
during setup so you can see what a wiki page looks like and verify the system
works end-to-end.

Feel free to delete this page once you have created your first real entry —
or keep it as a marker of when the vault began.

## What just happened

1. The Obsidian Company Memory skill scaffolded your vault folder.
2. It created this page and linked it to [[CONTEXT]].
3. It updated [[index]] to include this page.
4. It appended a one-line entry to [[log]].

If you can open this page in Obsidian and click through to [[CONTEXT]] from
the wikilink, the round-trip works.

## Next

Read [[HOW-TO-USE-THIS]] for the ongoing-use guide. When you are ready to
start your first real project, run the `open-obsidian-project` skill (it ships
separately in your AI tool's skill list).
```

### 8b. Update `index.md`

Open `$VAULT/index.md` in your editor. Find the `## Entities` section. Append this line to it:

```
- [[entities/test-welcome]] — welcome page created at vault setup; safe to delete after first real page
```

Save.

### 8c. Open in Obsidian and verify (5-step check)

1. Open Obsidian → File → "Open folder as vault" → pick `$VAULT`.
2. In the file explorer on the left, you should see: `SCHEMA.md`, `CONTEXT.md`, `index.md`, `log.md`, `HOW-TO-USE-THIS.md`, and folders `entities/`, `concepts/`, `_meta/`. (Empty folders may not show depending on Obsidian's settings; that's fine.)
3. Open `entities/test-welcome.md`. The heading should read "Welcome to your `<your company name>` vault" — NOT a literal `{{COMPANY_NAME}}`.
4. Click the `[[CONTEXT]]` wikilink. It should open `CONTEXT.md`.
5. Open `index.md`. You should see `entities/test-welcome` listed under Entities.

If all five work: the round-trip passed. Continue to 8d.

If any fail: do NOT continue. See [troubleshooting.md § Post-scaffold — verifying the round-trip](troubleshooting.md#post-scaffold--verifying-the-round-trip). Most common failure is a substitution missed in step 3 (heading shows `{{COMPANY_NAME}}` literally).

### 8d. Append the second `log.md` entry

The starter `log.md` contains an initial scaffold entry. The skill's procedure appends a SECOND entry post-verification, recording that the round-trip worked.

Open `$VAULT/log.md`. Find the existing initial entry (it'll have today's date and the heading "vault setup — initial scaffold"). ABOVE that entry (newer entries go on top per the read-backwards-in-time convention), insert:

```markdown
## [<today>] vault setup — round-trip test
- Ingests: entities/test-welcome.md
- Queries: none
- Brief updated: N/A
- Notes: Round-trip test passed. User confirmed in Obsidian (manual install path).
```

Substitute `<today>` with your `TODAY` value. Save.

If the round-trip DID NOT pass: do NOT add this entry. Add a different entry naming the specific failure observed. The audit trail must be honest.

---

## Section 9 — Confirm the companion skills installed correctly

This step was already done as part of Section 7f (the companion-skill copy). What's left is verification: confirm both companion skills are visible to your AI tool and respond to invocation.

### Read [`companion-skills/README.md`](../companion-skills/README.md)

It walks the surface-by-surface install procedure for Cowork, Claude Code, Codex, and opencode. ~3 minutes to read. Useful reference if Section 7f's copy didn't land cleanly on your surface.

### Verify `open-obsidian-project` is installed

Ask your AI: *"List my available skills."* `open-obsidian-project` should appear. If you're on Code, also confirm `~/.claude/skills/open-obsidian-project/SKILL.md` exists on disk.

If it doesn't appear: re-run the copy step from Section 7f for that skill, restart your AI tool, and retry.

### Verify `close-obsidian-project` is installed

Same check. `close-obsidian-project` should appear in the skills list. If not, re-run the copy step.

If both appear and respond, you're done.

Both companion skills use the `-obsidian-project` namespace suffix so they coexist with any other "open project" or "close" skills you already have. If you already had a skill with the exact name `open-obsidian-project` or `close-obsidian-project`, the copy step in Section 7f would have collided — pick a different name for one or the other and re-run.

---

## Section 10 — Verification checklist

Before declaring the manual install complete, confirm:

```
[ ] $VAULT exists and is the absolute path you intended.
[ ] Round-trip test passed (5 Obsidian checks from § 8c).
[ ] log.md has TWO entries: initial scaffold + round-trip success.
[ ] index.md lists entities/test-welcome under Entities.
[ ] All five .obsidian/*.json files parse as valid JSON.
[ ] _meta/expectations.yml parses as valid YAML and has the date_format_preference line.
[ ] _meta/scaffold-version.txt has all six lines with your values.
[ ] CLAUDE.md.template at vault root still contains literal {{...}} placeholders (NOT substituted).
[ ] AGENTS.md.template at vault root still contains literal {{...}} placeholders (NOT substituted).
[ ] _meta/templates/{entity,concept,query}.md each contain a literal {{TODAY}} (NOT substituted).
[ ] CONTEXT.md heading shows your company name, not a literal {{COMPANY_NAME}}.
[ ] No file in the vault shows a literal {{VAULT_ABSOLUTE_PATH}} except the two .template files at the vault root.
[ ] open-obsidian-project companion skill is installed in your AI tool (verified by "list my skills" returning it).
[ ] close-obsidian-project companion skill is installed in your AI tool (same check).
```

If every box is ticked, you're done.

---

## Section 11 — Common manual-install mistakes

These are the failure modes most likely to bite a manual installer. Each links to the right recovery section.

### Mistake 1 — Forgot the carve-outs and substituted everything

You ran the batch sed/PowerShell substitution from Section 5 without reverting the carve-outs. Your `_meta/templates/*.md` files now have today's date baked in instead of `{{TODAY}}`, and your `CLAUDE.md.template` / `AGENTS.md.template` files are partially substituted.

Recovery:
1. For `_meta/templates/{entity,concept,query}.md`: open each, find your literal `TODAY` date, replace it with `{{TODAY}}`. Save.
2. For `CLAUDE.md.template` and `AGENTS.md.template` at the vault root: easiest fix is to re-copy from `$BUNDLE/templates/` verbatim — they have no substitutions at all, so just overwrite.
3. For the companion skills at `~/.claude/skills/open-obsidian-project/SKILL.md` and `~/.claude/skills/close-obsidian-project/SKILL.md`: these are copied verbatim from `$BUNDLE/companion-skills/`; if a batch substitution accidentally hit them, re-copy from the bundle.

### Mistake 2 — Heading shows `{{COMPANY_NAME}}` literally in Obsidian

You forgot to substitute in one or more files. The round-trip test in Section 8 surfaces this — the test-welcome page's heading should be your company name.

Recovery: open the affected file in your editor, Find-and-Replace `{{COMPANY_NAME}}` with your company name, save. Re-open in Obsidian to confirm.

### Mistake 3 — Wikilinks don't resolve

The `[[CONTEXT]]` wikilink in `entities/test-welcome.md` should open `CONTEXT.md` when clicked. If it doesn't:

1. Check Obsidian Settings → Files & Links → "Use [[Wikilinks]]" is ON.
2. Confirm the vault root opened in Obsidian is exactly `$VAULT` — not a parent folder.
3. Confirm `CONTEXT.md` exists at the vault root (case-sensitive: `CONTEXT.md`, not `context.md`).

### Mistake 4 — `.obsidian/` config files had `{{COMPANY_NAME}}` substituted into them

This would corrupt JSON parsing. The `.obsidian/` files contain no placeholders — they should NOT have been touched by substitution. If your batch substitution affected them, restore from the bundle:

```bash
cp "$BUNDLE/templates/.obsidian/"*.json "$VAULT/.obsidian/"
```

### Mistake 5 — Vault opened at parent folder in Obsidian

Symptom: Obsidian shows an empty file tree even though `$VAULT` has files. You opened the wrong folder.

Recovery: in Obsidian, File → Close vault. File → Open vault → pick `$VAULT` (NOT a parent or sibling folder).

### Mistake 6 — Forgot to append the second `log.md` entry

Easy mistake; the round-trip section is long. Without the second entry, your audit trail starts mid-history.

Recovery: re-read Section 8d and append. If the round-trip DIDN'T pass, append a failure entry instead — don't fake success.

---

## Section 12 — Upgrading a manually-installed vault

When a new skill version ships, your vault doesn't auto-upgrade. This is by design: vaults are yours, not ours.

See [upgrading.md](upgrading.md) for the general upgrade philosophy. The manual-install-specific differences:

1. **No `scaffold-version.txt` auto-update.** When you adopt changes from a new skill version, edit `_meta/scaffold-version.txt` yourself: bump `version` to the new value, append a line `last_refresh: YYYY-MM-DD`.
2. **No automatic file diff.** Compare the new bundle's `$BUNDLE_NEW/templates/...` against your `$VAULT/...` using `diff` (macOS / Linux) or `Compare-Object` (PowerShell). Adopt or skip each change deliberately.
3. **SCHEMA.md changes are the most important to review.** A new SCHEMA usually implies new lint behaviour, new page-format expectations, or new operation definitions. Skim the SCHEMA diff before pulling other changes.
4. **CLAUDE.md.template / AGENTS.md.template changes** affect projects you create AFTER the upgrade, not existing ones. Existing project folders keep their instantiated version.

If a version diff is too large to review by hand, the alternative is: scaffold a NEW vault using the new skill version into a separate empty folder, then migrate your content over. ~1-2 hours for a vault with 50+ pages.

---

## Section 13 — When (and whether) to switch to the skill later

If you installed manually because the skill wasn't available to you, and then later your environment gains skill access (e.g. you switch from Codex to Claude Code, or your IT allowlists the Cowork plugin URL): should you reinstall via the skill?

**Short answer: no, your vault is fine.**

**Long answer:** the skill install would refuse on your existing vault (non-empty target). You'd have to delete the vault to re-scaffold, which means losing whatever you've added. The result would be functionally identical to your current vault — no upside.

When the skill path WOULD be the right call:
- You're starting over from scratch anyway (e.g. company rename + content reset).
- You're moving to a new machine and want the skill to set up the new vault from a sync-fresh state.
- You're doing parallel installs (e.g. testing the skill before recommending it to teammates) and want a clean reference vault.

In those cases: use a separate empty folder, run the skill, compare the result to your manual install. Differences should be minimal (timestamps, possibly date-format detection). Anything else points at a manual-install mistake worth investigating.

---

## Done

If you've ticked every box in Section 11, your manually-installed vault is functionally equivalent to a skill-installed one. The remaining work is the same:

1. **Read `HOW-TO-USE-THIS.md` at the vault root** (~10 minutes). Phase 2 guide.
2. **Start your first real session** with the suggested opener:
   > Mount the vault at `<your-vault-absolute-path>`. Read SCHEMA.md and CONTEXT.md. I want to start by capturing what `<company>` does and who its customers are — fill in the 'About `<company>`' section in CONTEXT.md and ingest it.
3. **Run a baseline lint** at the end of that first session by asking your AI: *"run a lint on the vault."*

---

## Feedback

This guide is generated from the skill's procedural source. If something is wrong, missing, or unclear, email `info@absolutionlabs.com` with the section number and the specific text. We update this guide as the skill version changes and as user reports surface gaps. Quarterly refresh aligned with [COMPATIBILITY.md](../COMPATIBILITY.md).

---

*Cross-references: [SKILL.md](../SKILL.md) (the canonical procedural source), [README.md](../README.md), [COMPATIBILITY.md](../COMPATIBILITY.md), [troubleshooting.md](troubleshooting.md), [faq.md](faq.md), [standard-vs-ours.md](standard-vs-ours.md), [customisation.md](customisation.md), [upgrading.md](upgrading.md), [install-walkthrough.md](install-walkthrough.md), [manual-install-guide-scope.md](manual-install-guide-scope.md).*

---

## Use at your own risk

This document is part of the Obsidian Company Memory bundle, provided "AS IS" without warranty of any kind under the MIT License. It is for general informational and educational purposes only and does not constitute professional advice. AI-generated outputs from any vault scaffolded by this skill may contain errors and must be independently verified before reliance. The manual install path in particular bypasses the skill's built-in safety checks (worktree refusal, bundle integrity, atomic rollback on mid-scaffold failure) — you accept full responsibility for following the substitution-scope carve-outs in Section 5 and Section 7 correctly. **Read [DISCLAIMERS.md](../DISCLAIMERS.md) in full before installing, forking, or relying on anything in this repository.**

*© 2026 Absolution Labs. AbsolutionLabs Ltd, registered in England and Wales (Company No. 17091663). Registered office: 15 Westbury Road, London SE20 7QL.*
