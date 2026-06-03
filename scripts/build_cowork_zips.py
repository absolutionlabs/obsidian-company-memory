#!/usr/bin/env python3
"""
Build Cowork-uploadable zips for the Obsidian Company Memory bundle.

Produces three zips under release/cowork-zips/:
  - obsidian-company-memory-vX.Y.Z.zip  (SKILL.md + templates/)
  - open-obsidian-project-vX.Y.Z.zip    (SKILL.md only)
  - close-obsidian-project-vX.Y.Z.zip   (SKILL.md only)

Each zip has SKILL.md at the root and uses forward-slash path separators (the
ZIP spec requires forward slashes; PowerShell's Compress-Archive writes
backslashes, which Cowork's Upload-skill validator rejects with "Zip file
contains path with invalid characters"). This script always produces
spec-compliant zips.

Usage:
    python scripts/build_cowork_zips.py

Run from the bundle root. Writes to release/cowork-zips/. Reads the version
from the SKILL.md frontmatter of the main skill (assumes all three are pinned
to matching versions; warns if they diverge).
"""
import os
import re
import shutil
import sys
import tempfile
import zipfile

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(REPO_ROOT, "release", "cowork-zips")


def read_version(skill_md_path):
    with open(skill_md_path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^version:\s*(\S+)\s*$", line)
            if m:
                return m.group(1)
    raise SystemExit(f"FATAL: no `version:` found in {skill_md_path}")


def write_zip(zip_path, stage_dir):
    if os.path.exists(zip_path):
        os.remove(zip_path)
    file_count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(stage_dir):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, stage_dir).replace(os.sep, "/")
                zf.write(full, rel)
                file_count += 1
    return file_count


def verify_zip(zip_path):
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        if any("\\" in n for n in names):
            raise SystemExit(f"FATAL: {zip_path} contains backslash path "
                             "separators — Cowork will reject it. This script "
                             "should always emit forward slashes; check Python "
                             "version + zipfile behaviour.")
        if "SKILL.md" not in names:
            raise SystemExit(f"FATAL: {zip_path} does not contain SKILL.md at "
                             "the root — Cowork will reject it.")
        return len(names)


def build_main_skill(version):
    out = os.path.join(OUT_DIR, f"obsidian-company-memory-v{version}.zip")
    # Stage outside Dropbox to dodge sync-lock races on Windows.
    with tempfile.TemporaryDirectory() as tmp:
        stage = os.path.join(tmp, "obsidian-company-memory")
        os.makedirs(stage)
        shutil.copy(os.path.join(REPO_ROOT, "SKILL.md"),
                    os.path.join(stage, "SKILL.md"))
        shutil.copytree(os.path.join(REPO_ROOT, "templates"),
                        os.path.join(stage, "templates"))
        count = write_zip(out, stage)
    entries = verify_zip(out)
    return out, count, entries


def build_companion(name, version):
    out = os.path.join(OUT_DIR, f"{name}-v{version}.zip")
    with tempfile.TemporaryDirectory() as tmp:
        stage = os.path.join(tmp, name)
        os.makedirs(stage)
        shutil.copy(
            os.path.join(REPO_ROOT, "companion-skills", name, "SKILL.md"),
            os.path.join(stage, "SKILL.md"),
        )
        count = write_zip(out, stage)
    entries = verify_zip(out)
    return out, count, entries


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    main_version = read_version(os.path.join(REPO_ROOT, "SKILL.md"))
    open_version = read_version(
        os.path.join(REPO_ROOT, "companion-skills",
                     "open-obsidian-project", "SKILL.md"))
    close_version = read_version(
        os.path.join(REPO_ROOT, "companion-skills",
                     "close-obsidian-project", "SKILL.md"))

    versions = {main_version, open_version, close_version}
    if len(versions) > 1:
        print(f"WARN: versions diverge (main={main_version}, "
              f"open={open_version}, close={close_version}). Each zip will "
              "carry its own version; check this is deliberate before "
              "releasing.", file=sys.stderr)

    print(f"Building zips into: {OUT_DIR}")

    for label, fn in (
        ("main", lambda: build_main_skill(main_version)),
        ("open-obsidian-project", lambda: build_companion(
            "open-obsidian-project", open_version)),
        ("close-obsidian-project", lambda: build_companion(
            "close-obsidian-project", close_version)),
    ):
        path, file_count, entries = fn()
        size_kb = os.path.getsize(path) / 1024
        print(f"  {label}: {os.path.basename(path)}  "
              f"({file_count} files, {entries} zip entries, {size_kb:.1f} KB)")

    print()
    print("All zips built and verified (SKILL.md at root, forward-slash paths).")
    print("Upload each via Cowork → Skills → Upload skill, or attach to a "
          "GitHub Release:")
    print()
    print(f"  gh release create vX.Y.Z {OUT_DIR}/*.zip "
          "--repo absolutionlabs/obsidian-company-memory "
          "--notes-file release/vX.Y.Z-notes.md")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    main()
