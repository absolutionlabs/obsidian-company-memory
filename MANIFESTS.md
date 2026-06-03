# Manifest Mirror Contract

This skill ships from one source repo, installable on two surfaces. Each surface uses its own manifest format:

| Surface | Manifest | Format | Location |
|---|---|---|---|
| Cowork plugin | `plugin.json` | JSON | repo root |
| Claude Code skill | YAML frontmatter at the top of `SKILL.md` | YAML | repo root |

Both manifests point at the same `SKILL.md` body. The fields below MUST stay in sync — a release that updates one without the other is a release-blocker.

---

## Synced fields (both manifests must match)

| Field | `plugin.json` key | `SKILL.md` frontmatter key | Current value (v1.0.0) |
|---|---|---|---|
| Identifier / name | `id` + `name` | `name` | `obsidian-company-memory` |
| Version | `version` | `version` | `1.0.0` |
| Description | `description` | `description` | (one-paragraph; see SKILL.md) |
| License | `license` | `license` | `MIT` |
| Publisher | `publisher.name` | `publisher` | `Absolution Labs LTD` |
| Support email | `publisher.support` | `support` | `info@absolutionlabs.com` |

If you bump the version in one manifest, bump it in the other AND in `_meta/scaffold-version.txt` (written by SKILL.md Step 6.7) AND in `COMPATIBILITY.md`. All four are the canonical version surface; drift between them is a Chunk 5 lint check candidate.

---

## Surface-only fields (live in `plugin.json` only)

The Cowork plugin manifest carries additional fields that the Code skill manifest does not need, because Code surfaces resolve those concerns differently:

| Field | Why Cowork-only |
|---|---|
| `permissions.directory_access` | Cowork requires explicit per-mount grant; Code inherits CWD access |
| `permissions.network_egress.endpoints` | Cowork sandbox egress is allowlist-gated; Code does not have a sandbox |
| `surfaces` | Tells the marketplace which install paths to surface |
| `categories` / `keywords` | Marketplace discoverability metadata |
| `homepage` / `repository` / `release_signing` | Marketplace + integrity surfaces |
| `files` | Cowork plugin bundle declares which files are part of the package |
| `telemetry.endpoint` / `telemetry.anon_key` / `telemetry.endpoint_provider` / `telemetry.endpoint_region` | Telemetry config consumed by SKILL.md Steps 5 + 9.1. The anon key is public-by-design (Supabase model: security via RLS, not via key secrecy). When the telemetry endpoint moves (e.g. to a custom domain) or the anon key rotates, ONLY plugin.json changes — SKILL.md references the values by path (`plugin.json.telemetry.endpoint`, `plugin.json.telemetry.anon_key`), not by literal. |

These do not need a Code-side mirror. Code installs the whole skill directory verbatim; the agent reads `SKILL.md` and runs the procedure.

---

## Surface-only fields (live in `SKILL.md` frontmatter only)

| Field | Why Code-only |
|---|---|
| (none currently) | All Code-side metadata lives in fields that are also in `plugin.json` |

---

## What changes between v1.x releases

A patch release (e.g. `1.0.0` → `1.0.1`):

- Update both `plugin.json` `version` and `SKILL.md` `version`.
- Update `_meta/scaffold-version.txt` template inside the skill's substitution table (SKILL.md Step 6.7 writes the running version).
- Add a row to `docs/upgrading.md` describing the change.
- Bump `checksums_url` content (Chunk 7 release process — `checksums.txt` regenerated).
- Re-sign the bundle (Chunk 7 release process — see `release_signing`).

A minor release that adds a field to one manifest MUST add the equivalent to the other or document the asymmetry in this file's tables above.

---

## Pre-release manifest lint (Chunk 5 candidate)

Before public ship of any version:

1. Diff `plugin.json` `version` against `SKILL.md` `version` — must be identical.
2. Diff `plugin.json.description` against `SKILL.md` `description` — first sentence must match exactly; later sentences may diverge in framing but not in capability claims.
3. Diff `plugin.json.publisher.name` against `SKILL.md` `publisher` — must be identical (legal-name discipline per Decision #12).
4. Diff `plugin.json.license` against `SKILL.md` `license` and against the LICENSE file header — all three must match.
5. Confirm every path in `plugin.json.files` actually exists in the repo at that path.
6. Confirm `plugin.json.entry` resolves to a file that parses as valid SKILL.md (frontmatter + body).
7. Confirm `plugin.json.permissions.directory_access.writes` matches the list of writes SKILL.md Step 6 actually performs.
8. Confirm no path in `plugin.json.permissions.directory_access.writes` is missing from SKILL.md Step 6's substep list (no silent writes).
9. Confirm `plugin.json.telemetry.endpoint` is reachable (HTTP probe to the `/v1/health` equivalent — for Supabase, a GET on the project URL should return a 4xx but not a network error).
10. Confirm `plugin.json.telemetry.anon_key` parses as a valid JWT and decodes to `{"role": "anon"}`.
11. Confirm `plugin.json.permissions.network_egress.endpoints` matches `plugin.json.telemetry.endpoint` exactly.

A failure on any of these blocks the release. Codified into [`scripts/lint_manifest.py`](scripts/lint_manifest.py) — run before every public ship:

```sh
python scripts/lint_manifest.py
```

All 11 checks run in under a second; the script returns exit code 1 on any failure with detail printed.

---

## Reference

- Skill body and procedure: [SKILL.md](SKILL.md)
- Cowork plugin manifest: [plugin.json](plugin.json)
- Templates: [templates/](templates/)
- Version stamp written into every scaffolded vault: `_meta/scaffold-version.txt` (per SKILL.md Step 6.7)
- Brief and decisions: held internally; email `info@absolutionlabs.com` for specifics
- Compatibility matrix: `COMPATIBILITY.md` (Chunk 6 deliverable)

---

*Maintained by Absolution Labs LTD. Questions: `info@absolutionlabs.com`.*
