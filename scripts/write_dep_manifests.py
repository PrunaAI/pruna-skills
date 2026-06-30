#!/usr/bin/env python3
"""Emit cross-package-manager dependency manifests from skill.manifest.json tool_skills."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GITHUB_REPO = "PrunaAI/pruna-ai-content-generation-skills"
SKILLS_PATH = "skills"
GIT_REF = "main"


def read_description(skill_md: Path, fallback: str) -> str:
    text = skill_md.read_text()
    m = re.search(r"^description:\s*(.+)$", text, re.M)
    return m.group(1).strip().strip('"') if m else fallback


def patch_skill_md_depends(skill_md: Path, deps: list[str]) -> None:
    if not deps:
        return
    text = skill_md.read_text()
    text = re.sub(r"^\s+prerequisite-skills:.*\n", "", text, flags=re.M)
    text = re.sub(r"^depends:\n(?:  - .+\n)*", "", text, flags=re.M)
    block = "depends:\n" + "\n".join(f"  - {d}" for d in deps) + "\n"
    text = re.sub(r"^(---\n(?:.*\n)*?)(---\n)", lambda m: m.group(1) + block + m.group(2), text, count=1)
    skill_md.write_text(text)


def apm_path(skill: str) -> str:
    return f"{GITHUB_REPO}/{SKILLS_PATH}/{skill}"


def pspm_key(skill: str) -> str:
    return f"github:{GITHUB_REPO}/{SKILLS_PATH}/{skill}"


def write_apm_yml(dest: Path, skill: str, version: str, description: str, deps: list[str]) -> None:
    lines = "\n".join(f"    - {apm_path(d)}" for d in deps)
    dest.write_text(
        f"name: {skill}\n"
        f"version: {version}\n"
        f"type: skill\n"
        f"description: {description}\n"
        f"dependencies:\n"
        f"  apm:\n{lines}\n"
    )


def write_pspm_json(dest: Path, skill: str, version: str, description: str, deps: list[str]) -> None:
    files = ["SKILL.md", "skill.manifest.json", "pspm.json", "references", "scripts", "templates"]
    if deps:
        files.extend(["skill.deps.json", "apm.yml"])
    payload: dict = {
        "$schema": "https://pspm.dev/schemas/pspm.json",
        "name": f"@pruna/{skill}",
        "version": version,
        "description": description,
        "license": "MIT",
        "files": files,
    }
    if deps:
        payload["githubDependencies"] = {pspm_key(d): GIT_REF for d in deps}
    dest.write_text(json.dumps(payload, indent=2) + "\n")


def write_skill_deps_json(
    dest: Path, skill: str, version: str, deps: list[str], *, include_resolvers: bool = True
) -> None:
    payload: dict = {
        "schemaVersion": 1,
        "skill": skill,
        "version": version,
        "repository": GITHUB_REPO,
        "skillsPath": SKILLS_PATH,
        "depends": deps,
    }
    if include_resolvers:
        payload["resolvers"] = {
            "skills": {"depends": deps},
            "apm": {"dependencies": {"apm": [apm_path(d) for d in deps]}},
            "pspm": {"githubDependencies": {pspm_key(d): GIT_REF for d in deps}},
            "openclaw": {
                "install": [f"git:{GITHUB_REPO}@{GIT_REF}"],
                "note": "Install each skill under skills/<name> from the repo tree.",
            },
        }
    dest.write_text(json.dumps(payload, indent=2) + "\n")


def emit_for_bundle(dest: Path, skill: str, manifest_path: Path, version: str) -> bool:
    """Write publish/dep manifests for a bundled skill dir. Returns True if tool_skills present."""
    manifest = json.loads(manifest_path.read_text())
    deps: list[str] = list(manifest.get("tool_skills") or [])
    skill_md = dest / "SKILL.md"
    description = read_description(skill_md, skill)
    write_pspm_json(dest / "pspm.json", skill, version, description, deps)
    if not deps:
        return False
    patch_skill_md_depends(skill_md, deps)
    write_apm_yml(dest / "apm.yml", skill, version, description, deps)
    write_skill_deps_json(dest / "skill.deps.json", skill, version, deps)
    return True


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", type=Path, help="catalog skill.manifest.json")
    ap.add_argument("--dest", type=Path, help="bundle output directory")
    ap.add_argument("--skill", help="skill name")
    args = ap.parse_args()
    version = (REPO / "VERSION").read_text().strip()

    if not args.manifest or not args.dest or not args.skill:
        ap.error("--manifest, --dest, and --skill are required")
    emit_for_bundle(args.dest, args.skill, args.manifest, version)
    print(f"publish manifests -> {args.dest}")


if __name__ == "__main__":
    main()
    # ponytail: smoke when bundles exist
    deps_file = REPO / "skills/avatar-multi-scene/skill.deps.json"
    if deps_file.is_file():
        m = json.loads(
            (REPO / "catalog/workflows/core/avatar-multi-scene/skill.manifest.json").read_text()
        )
        d = json.loads(deps_file.read_text())
        assert d["depends"] == m["tool_skills"], "avatar-multi-scene skill.deps.json drift"
        assert "skilldex" not in d.get("resolvers", {}), "skilldex resolver removed"
