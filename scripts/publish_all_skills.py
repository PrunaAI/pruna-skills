#!/usr/bin/env python3
"""Publish bundled skills to registries that support CLI publish (PSPM).

GitHub + npx skills / APM git-install: no registry upload — push tag skills-v<VERSION>.
skills.sh: appears via install telemetry after users run npx skills add.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILLS = REPO / "skills"
GITHUB_REPO = "PrunaAI/pruna-ai-content-generation-skills"
PSPM = ["npx", "--yes", "@anytio/pspm@latest"]


def version() -> str:
    return (REPO / "VERSION").read_text().strip()


def list_skills() -> list[str]:
    return sorted(
        d.name
        for d in SKILLS.iterdir()
        if d.is_dir() and not d.name.startswith("_") and (d / "SKILL.md").is_file()
    )


def run(cmd: list[str], cwd: Path, *, dry_run: bool) -> int:
    label = " ".join(cmd)
    print(f"  {'[dry-run] ' if dry_run else ''}{label}  (cwd={cwd.relative_to(REPO)})")
    if dry_run:
        return 0
    env = os.environ.copy()
    proc = subprocess.run(cmd, cwd=cwd, env=env)
    return proc.returncode


def publish_pspm(skill: str, *, dry_run: bool) -> int:
    if not dry_run and not os.environ.get("PSPM_API_KEY"):
        print("  skip pspm: PSPM_API_KEY not set", file=sys.stderr)
        return 0
    return run(
        [*PSPM, "publish", "--access", "public"],
        SKILLS / skill,
        dry_run=dry_run,
    )


def write_publish_index() -> Path:
    ver = version()
    payload = {
        "version": ver,
        "package": "pruna-ai-content-generation-skills",
        "repository": f"https://github.com/{GITHUB_REPO}",
        "skillsPath": "skills",
        "gitTag": f"skills-v{ver}",
        "skills": list_skills(),
        "registries": {
            "github": {
                "method": "git tag + push",
                "tag": f"skills-v{ver}",
                "install": f"npx skills add {GITHUB_REPO}/skills --skill <name>",
            },
            "skills.sh": {
                "method": "install telemetry (no upload API)",
                "note": "Listing follows npx skills add usage",
            },
            "apm": {
                "method": "git install (no per-skill registry upload)",
                "install": f"apm install {GITHUB_REPO}/skills/<name>",
            },
            "pspm": {
                "method": "pspm publish",
                "package": "@pruna/<name>",
                "requires": ["PSPM_API_KEY"],
            },
        },
    }
    out = SKILLS / "publish-index.json"
    out.write_text(json.dumps(payload, indent=2) + "\n")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--target",
        default="pspm",
        help="comma-separated: pspm, index",
    )
    ap.add_argument("--skill", action="append", help="limit to skill name(s)")
    ap.add_argument("--execute", action="store_true", help="run publishes (default: dry-run)")
    ap.add_argument("--skip-verify", action="store_true", help="skip bundle freshness check")
    args = ap.parse_args()
    dry_run = not args.execute
    targets = {t.strip() for t in args.target.split(",") if t.strip()}

    if not args.skip_verify:
        verify = subprocess.run([str(REPO / "scripts/verify_skill_bundles.sh")], cwd=REPO)
        if verify.returncode != 0:
            return verify.returncode

    skills = args.skill or list_skills()
    failures = 0

    if "index" in targets or dry_run:
        path = write_publish_index()
        print(f"Wrote {path.relative_to(REPO)}")

    if dry_run:
        print(f"\nDry run (pass --execute to publish). VERSION={version()}\n")

    if "pspm" in targets:
        print("PSPM (@pruna/<skill>):")
        for name in skills:
            print(f"-> {name}")
            failures += publish_pspm(name, dry_run=dry_run) != 0

    if not dry_run:
        print(f"\nGitHub / npx skills: tag and push skills-v{version()} for release marker.")
        print(f"  git tag skills-v{version()} && git push origin skills-v{version()}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
