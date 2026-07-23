#!/usr/bin/env python3
"""Inject repo VERSION into skills — replaces @VERSION and syncs metadata.version."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VERSION = (REPO / "VERSION").read_text().strip()
SKILLS_ROOT = REPO / "skills"
PLACEHOLDER = "@VERSION"
TEXT_SUFFIXES = {".md", ".json", ".txt"}


def skill_files() -> list[Path]:
    if not SKILLS_ROOT.is_dir():
        return []
    return sorted(SKILLS_ROOT.rglob("SKILL.md"))


def injectable_files() -> list[Path]:
    if not SKILLS_ROOT.is_dir():
        return []
    out: list[Path] = []
    for path in SKILLS_ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            out.append(path)
    return sorted(out)


def inject_placeholders(text: str) -> str:
    if PLACEHOLDER not in text:
        return text
    return text.replace(PLACEHOLDER, VERSION)


def sync_skill_frontmatter(text: str) -> str:
    if "metadata:" not in text:
        block = f'license: MIT\nmetadata:\n  version: "{VERSION}"\n  package: pruna-skills\n'
        if re.search(r"^license:", text, re.M):
            text = re.sub(
                r"^license:.*\n",
                block,
                text,
                count=1,
            )
        else:
            text = re.sub(
                r"^(---\n.*?description:.*\n)",
                r"\1" + block,
                text,
                count=1,
                flags=re.S,
            )
        return text

    text = re.sub(r'^(\s+version:\s*)"[^"]*"', rf'\1"{VERSION}"', text, flags=re.M)
    meta = text.split("metadata:", 1)[-1].split("\n---", 1)[0]
    if "package:" not in meta:
        text = re.sub(
            rf'^(\s+version:\s*"{re.escape(VERSION)}"\s*\n)',
            rf'\1  package: pruna-skills\n',
            text,
            count=1,
            flags=re.M,
        )
    return text


def sync_file(path: Path) -> bool:
    original = path.read_text()
    text = inject_placeholders(original)
    if path.name == "SKILL.md":
        text = sync_skill_frontmatter(text)
    if text != original:
        path.write_text(text)
        return True
    return False


def frontmatter_version(path: Path) -> str | None:
    text = path.read_text()
    m = re.search(r"^metadata:\s*\n(?:\s+.+\n)*?\s+version:\s*\"([^\"]+)\"", text, re.M)
    return m.group(1) if m else None


def check() -> int:
    errors: list[str] = []
    for path in injectable_files():
        if PLACEHOLDER in path.read_text():
            errors.append(f"{path.relative_to(REPO)}: unresolved {PLACEHOLDER}")
    for path in skill_files():
        got = frontmatter_version(path)
        if got != VERSION:
            errors.append(f"{path.relative_to(REPO)}: metadata.version={got!r}, want {VERSION!r}")
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1
    print(f"VERSION={VERSION} OK ({len(skill_files())} skills, {len(injectable_files())} injectable files)")
    return 0


def use_placeholders() -> int:
    changed = 0
    for path in skill_files():
        text = path.read_text()
        new = re.sub(r'^(\s+version:\s*)"[^"]*"', rf'\1"{PLACEHOLDER}"', text, flags=re.M)
        if new != text:
            path.write_text(new)
            changed += 1
    print(f"set {PLACEHOLDER} in {changed} SKILL.md file(s)")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify VERSION injected (CI)")
    parser.add_argument(
        "--placeholders",
        action="store_true",
        help="reset metadata.version to @VERSION in all SKILL.md",
    )
    args = parser.parse_args()

    if args.check:
        raise SystemExit(check())
    if args.placeholders:
        raise SystemExit(use_placeholders())

    changed = sum(sync_file(p) for p in injectable_files())
    print(f"VERSION={VERSION} synced {changed} file(s) under skills/")


if __name__ == "__main__":
    main()
