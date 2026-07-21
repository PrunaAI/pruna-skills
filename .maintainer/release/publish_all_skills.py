#!/usr/bin/env python3
"""Publish skills to registries (skills-only — no plugins/).

| Target | Command | What gets published |
|--------|---------|---------------------|
| clawhub | clawhub skill publish | Skill folder under skills/{guides,image,video,audio,workflows,suite}/ |
| index | (local) | .maintainer/publish-index.json |
| github / npx | (local) | Release tag instructions — no upload API |

GitHub + npx skills / skills.sh: push `skills/` to main and tag `skills-v<VERSION>`.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GITHUB_REPO = "PrunaAI/pruna-skills"
DEFAULT_CLAWHUB_OWNER = "pruna-ai"
CLAWHUB_NPX = ["npx", "--yes", "clawhub@latest"]
INDEX_PATH = REPO / ".maintainer" / "publish-index.json"

sys.path.insert(0, str(REPO / ".maintainer"))
from skill_catalog import all_primary_skills, find_skill_dir  # noqa: E402


def cli_bin(name: str, npx: list[str]) -> list[str]:
    return [name] if shutil.which(name) else npx


def clawhub_cmd() -> list[str]:
    return cli_bin("clawhub", CLAWHUB_NPX)


def clawhub_slug(skill: str) -> str:
    return skill.replace(".", "-")


def version() -> str:
    return (REPO / "VERSION").read_text().strip()


def list_skills() -> list[str]:
    return [n for n in all_primary_skills() if find_skill_dir(n)]


def git_head() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def clawhub_authenticated() -> bool:
    try:
        proc = subprocess.run(clawhub_cmd() + ["whoami"], cwd=REPO, capture_output=True, text=True)
        return proc.returncode == 0 and bool(proc.stdout.strip())
    except FileNotFoundError:
        return False


def clawhub_ready(preview: bool) -> bool:
    if preview or os.environ.get("CLAWHUB_TOKEN") or clawhub_authenticated():
        return True
    print("  skip clawhub: CLAWHUB_TOKEN not set and not logged in (clawhub login)", file=sys.stderr)
    return False


def publish_clawhub_skill(skill: str, *, preview: bool) -> tuple[int, str]:
    if not clawhub_ready(preview):
        return 0, "not authenticated"
    owner = os.environ.get("CLAWHUB_OWNER", DEFAULT_CLAWHUB_OWNER)
    tags = os.environ.get("CLAWHUB_TAGS", "pruna,ai,generative,latest")
    slug = clawhub_slug(skill)
    skill_path = find_skill_dir(skill)
    if not skill_path:
        return 1, f"missing {skill}"
    rel = skill_path.relative_to(REPO).as_posix()
    cmd = [
        *clawhub_cmd(),
        "skill",
        "publish",
        rel,
        "--slug",
        slug,
        "--name",
        skill,
        "--owner",
        owner,
        "--tags",
        tags,
        "--version",
        version(),
        "--json",
    ]
    if preview:
        cmd.append("--dry-run")
    commit = git_head()
    if commit:
        cmd += [
            "--source-repo",
            GITHUB_REPO,
            "--source-commit",
            commit,
            "--source-path",
            rel,
        ]
    label = " ".join(cmd)
    print(f"  {'[preview] ' if preview else ''}{label}")
    proc = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    if proc.stdout.strip():
        print(f"    {proc.stdout.strip()}")
    if proc.returncode != 0:
        err = proc.stderr.strip() or proc.stdout.strip() or f"exit {proc.returncode}"
        if not preview and any(
            s in err for s in ("already exists", "unchanged", "already synced", "Rate limit")
        ):
            print(f"  skip ({err.splitlines()[0]})")
            return 0, err
        print(f"  error: {err}", file=sys.stderr)
        return proc.returncode, err
    return 0, ""


def write_publish_index() -> Path:
    ver = version()
    owner = os.environ.get("CLAWHUB_OWNER", DEFAULT_CLAWHUB_OWNER)
    skills = list_skills()
    payload = {
        "version": ver,
        "package": "pruna-skills",
        "repository": f"https://github.com/{GITHUB_REPO}",
        "gitTag": f"skills-v{ver}",
        "skills": [
            {
                "name": name,
                "skillPath": find_skill_dir(name).relative_to(REPO).as_posix(),  # type: ignore[union-attr]
                "clawhubSkill": f"@{owner}/{clawhub_slug(name)}",
                "npxInstall": f"npx skills add {GITHUB_REPO}@{name} -y",
            }
            for name in skills
        ],
        "registries": {
            "github": {
                "method": "git tag + push",
                "tag": f"skills-v{ver}",
                "note": "No upload API — consumers install from GitHub paths after push",
            },
            "npx": {
                "method": "npx skills add (GitHub source)",
                "listAll": f"npx skills add {GITHUB_REPO} -l",
                "installSkill": f"npx skills add {GITHUB_REPO}@<name> -y",
                "recommended": f"npx skills add {GITHUB_REPO}@pruna -y",
                "skillsSh": "https://skills.sh — listing via install telemetry after first install",
            },
            "clawhubSkills": {
                "method": "clawhub skill publish",
                "owner": owner,
                "install": f"clawhub install @{owner}/<slug>",
                "publish": "./.maintainer/release/publish_all_skills.sh --execute --target clawhub",
            },
        },
    }
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(payload, indent=2) + "\n")
    return INDEX_PATH


def print_github_npx_instructions() -> None:
    ver = version()
    tag = f"skills-v{ver}"
    print("\nGitHub / npx skills (no registry upload):")
    print("  1. Push skills/ to main")
    print(f"  2. git tag {tag} && git push origin {tag}")
    print(f"  3. Consumers: npx skills add {GITHUB_REPO}@pruna -y")
    print(f"     Or one skill: npx skills add {GITHUB_REPO}@<name> -y")
    print(f"     Or list all: npx skills add {GITHUB_REPO} -l")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--target",
        default="clawhub,index",
        help="comma-separated: clawhub, index, github, npx",
    )
    ap.add_argument("--skill", action="append", help="limit clawhub to skill name(s)")
    ap.add_argument("--execute", action="store_true", help="run publishes (default: dry-run)")
    ap.add_argument("--skip-verify", action="store_true", help="skip bundle freshness check")
    args = ap.parse_args()
    dry_run = not args.execute
    targets = {t.strip() for t in args.target.split(",") if t.strip()}
    if "clawhub" in targets:
        targets.add("clawhub-skills")

    if not args.skip_verify:
        verify = subprocess.run([str(REPO / ".maintainer/verify_skill_bundles.sh")], cwd=REPO)
        if verify.returncode != 0:
            return verify.returncode

    skills = args.skill or list_skills()
    failures = 0

    if "index" in targets or dry_run:
        path = write_publish_index()
        print(f"Wrote {path.relative_to(REPO)}")

    if dry_run:
        print(f"\nDry run (pass --execute to publish). VERSION={version()}\n")

    if "clawhub-skills" in targets:
        owner = os.environ.get("CLAWHUB_OWNER", DEFAULT_CLAWHUB_OWNER)
        print(f"ClawHub skills (@{owner}/<slug>):")
        for name in skills:
            print(f"-> {name}")
            rc, _ = publish_clawhub_skill(name, preview=dry_run)
            failures += rc != 0

    if "github" in targets or "npx" in targets:
        print_github_npx_instructions()

    if not dry_run and ("github" in targets or "npx" in targets or "clawhub-skills" in targets):
        print_github_npx_instructions()

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
