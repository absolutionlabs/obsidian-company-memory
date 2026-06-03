#!/usr/bin/env python3
"""
Pre-release manifest lint for the Obsidian Company Memory skill.

Implements the 11 checks documented in MANIFESTS.md § "Pre-release manifest lint".
Run from the bundle root. A failure on any check blocks the release.

Usage:
    python scripts/lint_manifest.py

Exit codes:
    0 — all checks pass
    1 — one or more checks failed (details printed)
"""

from __future__ import annotations

import base64
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Force UTF-8 on stdout so Unicode in check messages doesn't crash on Windows cmd.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

try:
    import yaml
except ImportError:
    print("error: pyyaml not installed. install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


ROOT = Path(__file__).resolve().parent.parent
RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))


# ----------------------------------------------------------------------------
# Loaders
# ----------------------------------------------------------------------------

def load_plugin_json() -> dict:
    text = (ROOT / "plugin.json").read_text(encoding="utf-8")
    # Strip the leading underscore-keyed comments (they're valid JSON; load directly)
    return json.loads(text)


def load_skill_frontmatter() -> dict:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md does not start with YAML frontmatter")
    end = text.index("\n---\n", 4)
    fm = text[4:end]
    return yaml.safe_load(fm)


def load_license_first_line() -> str:
    return (ROOT / "LICENSE").read_text(encoding="utf-8").splitlines()[0]


def load_skill_body() -> str:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    end = text.index("\n---\n", 4)
    return text[end + 5:]


# ----------------------------------------------------------------------------
# Checks
# ----------------------------------------------------------------------------

def run_checks() -> None:
    plugin = load_plugin_json()
    skill_fm = load_skill_frontmatter()
    skill_body = load_skill_body()
    license_line = load_license_first_line()

    # 1. Version match
    pj_v = plugin.get("version", "")
    sk_v = skill_fm.get("version", "")
    check(
        f"1. plugin.json.version == SKILL.md.version ({pj_v})",
        pj_v == sk_v and pj_v != "",
        f"plugin.json={pj_v!r}  SKILL.md={sk_v!r}",
    )

    # 2. Description first-sentence match
    def first_sentence(s: str) -> str:
        m = re.match(r"(.+?[.!?])(\s|$)", s.strip())
        return m.group(1) if m else s.strip()
    pj_first = first_sentence(plugin.get("description", ""))
    sk_first = first_sentence(skill_fm.get("description", ""))
    check(
        "2. description first-sentence match",
        pj_first == sk_first and pj_first != "",
        f"plugin={pj_first[:80]!r}  SKILL={sk_first[:80]!r}",
    )

    # 3. Publisher name match
    pj_pub = (plugin.get("publisher") or {}).get("name", "")
    sk_pub = skill_fm.get("publisher", "")
    check(
        f"3. publisher name match ({pj_pub!r})",
        pj_pub == sk_pub and pj_pub != "",
        f"plugin={pj_pub!r}  SKILL={sk_pub!r}",
    )

    # 4. License match across all three
    pj_lic = plugin.get("license", "")
    sk_lic = skill_fm.get("license", "")
    lic_header_ok = "MIT" in license_line
    check(
        "4. license is MIT in plugin.json + SKILL.md + LICENSE header",
        pj_lic == "MIT" and sk_lic == "MIT" and lic_header_ok,
        f"plugin={pj_lic!r}  SKILL={sk_lic!r}  LICENSE-line={license_line!r}",
    )

    # 5. Every file in plugin.json.files exists
    files = plugin.get("files", [])
    missing = [f for f in files if not (ROOT / f).exists()]
    check(
        f"5. all {len(files)} plugin.json.files paths exist",
        not missing,
        f"missing: {missing}",
    )

    # 6. plugin.json.entry resolves to SKILL.md with frontmatter
    entry = plugin.get("entry", "")
    entry_path = ROOT / entry
    entry_ok = entry_path.exists() and entry_path.read_text(encoding="utf-8").startswith("---\n")
    check(
        f"6. plugin.json.entry ({entry!r}) exists + has YAML frontmatter",
        entry_ok,
        f"entry path: {entry_path}",
    )

    # 7+8. Permissions.writes — every write declared in plugin.json appears in
    #     SKILL.md (Steps 6 + 7 — Step 6 scaffolds the main vault, Step 7 creates
    #     the round-trip welcome page). Brace-expansion patterns get expanded.
    pj_writes = set((plugin.get("permissions", {}) or {}).get("directory_access", {}).get("writes", []) or [])
    pj_basenames: set[str] = set()
    for w in pj_writes:
        base = Path(re.sub(r"^<vault>/", "", w)).name
        # Expand brace patterns like {entity,concept,query}.md
        m = re.match(r"\{([^}]+)\}\.(\w+)", base)
        if m:
            for alt in m.group(1).split(","):
                pj_basenames.add(f"{alt.strip()}.{m.group(2)}")
        elif "*" in base:
            # Glob like *.json — defer to glob comparison
            pj_basenames.add(base)
        else:
            pj_basenames.add(base)
    # Search the full SKILL.md body, not just Step 6 — round-trip test in Step 7
    # creates entities/test-welcome.md legitimately.
    sk_tokens = set(re.findall(r"[A-Za-z0-9_.-]+\.(?:md|yml|yaml|json|txt|template)", skill_body))
    missing_from_skill = sorted(
        b for b in pj_basenames
        if "*" not in b and b not in sk_tokens
    )
    check(
        f"7+8. writes parity ({len(pj_basenames)} plugin-declared writes, all should appear in SKILL.md)",
        not missing_from_skill,
        f"declared in plugin.json but not mentioned anywhere in SKILL.md: {missing_from_skill}",
    )

    # 9. Telemetry endpoint reachable
    endpoint = (plugin.get("telemetry") or {}).get("endpoint", "")
    if not endpoint:
        check("9. telemetry endpoint defined", False, "plugin.json.telemetry.endpoint missing")
    else:
        try:
            req = urllib.request.Request(endpoint, method="OPTIONS")
            with urllib.request.urlopen(req, timeout=5) as resp:
                code = resp.status
            check(f"9. telemetry endpoint reachable ({endpoint} → HTTP {code})", 200 <= code < 500)
        except urllib.error.HTTPError as e:
            # PostgREST may return 4xx on OPTIONS; that still means reachable
            check(f"9. telemetry endpoint reachable ({endpoint} → HTTP {e.code})", 200 <= e.code < 500)
        except Exception as e:
            check("9. telemetry endpoint reachability", False, f"{type(e).__name__}: {e}")

    # 10. Anon key parses as JWT with role=anon, iss=supabase, future exp,
    #     AND ref matches the endpoint hostname (defends against malicious
    #     manifest-swap where attacker forks the bundle and swaps in their
    #     own endpoint + key pair pointing at attacker infrastructure).
    anon = (plugin.get("telemetry") or {}).get("anon_key", "")
    try:
        parts = anon.split(".")
        if len(parts) != 3:
            raise ValueError(f"expected 3 JWT parts, got {len(parts)}")
        payload_b64 = parts[1] + "=" * ((4 - len(parts[1]) % 4) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        role = payload.get("role")
        iss = payload.get("iss")
        ref = payload.get("ref", "")
        exp = payload.get("exp", 0)
        from datetime import datetime, timezone
        now_ts = int(datetime.now(timezone.utc).timestamp())
        thirty_days = 30 * 24 * 60 * 60

        problems: list[str] = []
        if role != "anon":
            problems.append(f"role={role!r} expected 'anon'")
        if iss != "supabase":
            problems.append(f"iss={iss!r} expected 'supabase'")
        if exp <= now_ts:
            problems.append(f"exp={exp} is in the past")
        elif exp - now_ts < thirty_days:
            problems.append(f"exp expires in < 30 days (rotate before public ship)")

        check(
            f"10. anon_key JWT validates (role=anon, iss=supabase, exp future, ref={ref!r})",
            not problems,
            "; ".join(problems) if problems else "",
        )
    except Exception as e:
        check("10. anon_key JWT decode", False, f"{type(e).__name__}: {e}")
        ref = ""

    # 11. Network-egress endpoint matches telemetry endpoint
    egress = (
        ((plugin.get("permissions") or {}).get("network_egress") or {}).get("endpoints") or []
    )
    egress_first = egress[0] if egress else ""
    check(
        "11. permissions.network_egress.endpoints[0] == telemetry.endpoint",
        egress_first == endpoint and endpoint != "",
        f"egress={egress_first!r}  telemetry={endpoint!r}",
    )

    # 12. Endpoint hostname matches anon_key's ref claim (binds manifest to
    #     the specific Supabase project; a malicious fork that swaps the key
    #     but not the endpoint — or vice versa — fails this check).
    from urllib.parse import urlparse
    endpoint_host = urlparse(endpoint).netloc
    expected_host = f"{ref}.supabase.co" if ref else ""
    check(
        f"12. endpoint hostname matches anon_key.ref ({endpoint_host!r} == {expected_host!r})",
        bool(ref) and endpoint_host == expected_host,
        f"endpoint host={endpoint_host!r}  ref-derived={expected_host!r}",
    )


# ----------------------------------------------------------------------------
# Render
# ----------------------------------------------------------------------------

def render() -> int:
    from datetime import datetime, timezone
    print(f"MANIFEST LINT — Obsidian Company Memory ({datetime.now(timezone.utc).isoformat(timespec='seconds')})\n")
    pass_n = fail_n = 0
    for name, ok, detail in RESULTS:
        if ok:
            print(f"  PASS  {name}")
            pass_n += 1
        else:
            print(f"  FAIL  {name}")
            if detail:
                for line in detail.splitlines():
                    print(f"        {line}")
            fail_n += 1
    print(f"\nRESULT: {pass_n} / {len(RESULTS)} passed, {fail_n} failed")
    return fail_n


if __name__ == "__main__":
    try:
        run_checks()
    except Exception as e:
        print(f"script-level error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)
    sys.exit(min(render(), 1))
