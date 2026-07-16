#!/usr/bin/env python3
"""Assemble self-contained plugins/ from staged skill bundles."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GITHUB_REPO = "PrunaAI/pruna-skills"
GITHUB_TREE = f"https://github.com/{GITHUB_REPO}/tree/main"
SUITE_PLUGIN = "pruna-full"
SUITE_DESCRIPTION = (
    "Complete Pruna Skills bundle: all tool, router, core, and vertical skills in one plugin."
)
CLAWHUB_SCOPE = "pruna-ai"
REL_LINK = re.compile(r"\[([^\]]*)\]\((?!https?://|mailto:|#)([^)]+)\)")
SKILL_NAME = re.compile(r"(?:^|/)([a-z0-9][a-z0-9.-]*)/SKILL\.md")


def version() -> str:
    return (REPO / "VERSION").read_text().strip()


def read_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text()
    if not text.startswith("---"):
        return {}
    fm = text.split("---", 2)[1]
    out: dict[str, str] = {}
    for line in fm.splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def github_skill(name: str) -> str:
    return f"{GITHUB_TREE}/plugins/{name}/skills/{name}/SKILL.md"


def github_catalog_asset(path: str) -> str:
    clean = path.lstrip("./")
    if clean.startswith("references/"):
        clean = f"references/shared/{Path(clean).name}"
    elif clean.startswith("scripts/"):
        clean = f"workflows/_shared/scripts/{Path(clean).name}"
    elif "workflows/" in clean or "tools/" in clean or "guides/" in clean:
        clean = clean.lstrip("../")
        while clean.startswith("../"):
            clean = clean[3:]
    elif clean.endswith(".md") and "/" not in clean:
        clean = f"workflows/core/{Path(clean).stem}/SKILL.md"
    else:
        clean = clean.lstrip("../")
    return f"{GITHUB_TREE}/{clean}"


def rewrite_plugin_links(plugin_dir: Path, available: set[str]) -> None:
    skills_root = plugin_dir / "skills"
    if not skills_root.is_dir():
        return
    for md in skills_root.rglob("*.md"):
        text = md.read_text()

        def repl(match: re.Match[str]) -> str:
            label, target = match.group(1), match.group(2)
            path_part, _, anchor = target.partition("#")
            candidate = (md.parent / path_part).resolve()
            if candidate.exists():
                return match.group(0)
            skill_m = SKILL_NAME.search(path_part.replace("\\", "/"))
            if skill_m:
                name = skill_m.group(1)
                if name in available:
                    dest = skills_root / name / "SKILL.md"
                    href = (os_path_relpath(md.parent, dest.parent) / "SKILL.md").as_posix()
                    if anchor:
                        href += f"#{anchor}"
                    return f"[{label}]({href})"
                href = github_skill(name)
                if anchor:
                    href += f"#{anchor}"
                return f"[{label}]({href})"
            if path_part.endswith((".md", ".py", ".json", ".sh")):
                href = github_catalog_asset(path_part)
                if anchor:
                    href += f"#{anchor}"
                return f"[{label}]({href})"
            return match.group(0)

        new = REL_LINK.sub(repl, text)
        if new != text:
            md.write_text(new)


def os_path_relpath(from_dir: Path, to_dir: Path) -> Path:
    """Minimal relpath for markdown links."""
    from_parts = from_dir.parts
    to_parts = to_dir.parts
    common = 0
    for a, b in zip(from_parts, to_parts):
        if a != b:
            break
        common += 1
    ups = [".."] * (len(from_parts) - common)
    return Path(*ups, *to_parts[common:])


def write_plugin_manifest(plugin_dir: Path, name: str, description: str) -> None:
    manifest_dir = plugin_dir / ".claude-plugin"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "name": name,
        "description": description,
        "version": version(),
        "author": {"name": "Pruna AI"},
        "license": "MIT",
        "repository": f"https://github.com/{GITHUB_REPO}",
    }
    (manifest_dir / "plugin.json").write_text(json.dumps(payload, indent=2) + "\n")


def write_clawhub_package_files(
    plugin_dir: Path, name: str, description: str, bundled_skills: list[str]
) -> None:
    """ClawHub bundle-plugin publish metadata (alongside Claude .claude-plugin/)."""
    ver = version()
    skill_dirs = [f"skills/{skill}" for skill in bundled_skills]
    entry = "openclaw-entry.mjs"
    template = REPO / "scripts" / "plugin-templates" / entry
    shutil.copy2(template, plugin_dir / entry)

    openclaw_manifest = {
        "id": name,
        "name": name,
        "description": description,
        "skills": skill_dirs,
        "configSchema": {"type": "object", "additionalProperties": False, "properties": {}},
    }
    (plugin_dir / "openclaw.plugin.json").write_text(json.dumps(openclaw_manifest, indent=2) + "\n")

    install_cmd = f"openclaw plugins install clawhub:@{CLAWHUB_SCOPE}/{name}"
    readme = (
        f"# {name}\n\n"
        f"{description}\n\n"
        f"## Install\n\n"
        f"```bash\n{install_cmd}\n```\n\n"
        f"Claude Code: `/plugin install {name}@pruna-skills`\n\n"
        f"## Requirements\n\n"
        f"- `PRUNA_API_KEY` — [dashboard.pruna.ai](https://dashboard.pruna.ai/)\n"
    )
    (plugin_dir / "README.md").write_text(readme)

    package = {
        "name": f"@{CLAWHUB_SCOPE}/{name}",
        "version": ver,
        "type": "module",
        "license": "MIT",
        "description": description,
        "repository": f"https://github.com/{GITHUB_REPO}",
        "files": [".claude-plugin", "openclaw.plugin.json", "openclaw-entry.mjs", "README.md", "skills"],
        "openclaw": {
            "extensions": [f"./{entry}"],
            "compat": {"pluginApi": ">=2026.3.24-beta.2"},
            "bundledSkills": bundled_skills,
        },
    }
    (plugin_dir / "package.json").write_text(json.dumps(package, indent=2) + "\n")


def write_marketplace(plugin_meta: list[tuple[str, str]]) -> None:
    marketplace_dir = REPO / ".claude-plugin"
    marketplace_dir.mkdir(parents=True, exist_ok=True)
    ver = version()
    payload = {
        "name": "pruna-skills",
        "owner": {"name": "Pruna AI"},
        "metadata": {
            "description": "Pruna Skills — generative media agent skills for the Pruna AI API",
            "version": ver,
            "pluginRoot": "./plugins",
        },
        "plugins": [
            {
                "name": name,
                "description": desc,
                "version": ver,
                "source": f"./{name}",
            }
            for name, desc in sorted(plugin_meta)
        ],
    }
    (marketplace_dir / "marketplace.json").write_text(json.dumps(payload, indent=2) + "\n")


def emit_dep_manifests(plugin_name: str, primary_dest: Path, manifest_path: Path) -> None:
    skills_path = f"plugins/{plugin_name}/skills"
    subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "write_dep_manifests.py"),
            "--manifest",
            str(manifest_path),
            "--dest",
            str(primary_dest),
            "--skill",
            plugin_name,
            "--skills-path",
            skills_path,
        ],
        check=True,
        cwd=REPO,
    )


def build_plugin(name: str, staged: Path, plugins_root: Path) -> tuple[str, str]:
    staged_skill = staged / name
    if not (staged_skill / "SKILL.md").is_file():
        raise SystemExit(f"staging missing SKILL.md for {name}")

    manifest_path = staged_skill / "skill.manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.is_file() else {}
    deps: list[str] = list(manifest.get("tool_skills") or [])

    plugin_dir = plugins_root / name
    skills_dir = plugin_dir / "skills"
    primary_dest = skills_dir / name
    primary_dest.mkdir(parents=True, exist_ok=True)

    shutil.copytree(staged_skill, primary_dest, dirs_exist_ok=True)

    for dep in deps:
        dep_staged = staged / dep
        if not (dep_staged / "SKILL.md").is_file():
            raise SystemExit(f"{name}: tool_skills dependency {dep!r} missing from staging")
        dep_dest = skills_dir / dep
        shutil.copytree(dep_staged, dep_dest, dirs_exist_ok=True)

    available = {name, *deps}
    rewrite_plugin_links(plugin_dir, available)

    fm = read_frontmatter(primary_dest / "SKILL.md")
    description = fm.get("description", name)
    write_plugin_manifest(plugin_dir, name, description)
    write_clawhub_package_files(plugin_dir, name, description, [name, *deps])

    if deps and manifest_path.is_file():
        emit_dep_manifests(name, primary_dest, manifest_path)

    return name, description


def build_suite_plugin(staged: Path, plugins_root: Path, skill_names: list[str]) -> tuple[str, str]:
    """All-in-one plugin: every staged skill under skills/<name>/ (no per-skill dep sidecars)."""
    plugin_dir = plugins_root / SUITE_PLUGIN
    skills_dir = plugin_dir / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    for name in skill_names:
        src = staged / name
        if not (src / "SKILL.md").is_file():
            raise SystemExit(f"suite: staging missing SKILL.md for {name}")
        shutil.copytree(src, skills_dir / name, dirs_exist_ok=True)
    rewrite_plugin_links(plugin_dir, set(skill_names))
    write_plugin_manifest(plugin_dir, SUITE_PLUGIN, SUITE_DESCRIPTION)
    write_clawhub_package_files(plugin_dir, SUITE_PLUGIN, SUITE_DESCRIPTION, skill_names)
    return SUITE_PLUGIN, SUITE_DESCRIPTION


def list_staged_skills(staging: Path) -> list[str]:
    return sorted(
        d.name
        for d in staging.iterdir()
        if d.is_dir() and (d / "SKILL.md").is_file()
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--staging", type=Path, required=True, help="directory of staged skill bundles")
    args = ap.parse_args()
    staging = args.staging.resolve()
    if not staging.is_dir():
        ap.error(f"staging not found: {staging}")

    plugins_root = REPO / "plugins"
    if plugins_root.exists():
        shutil.rmtree(plugins_root)
    plugins_root.mkdir()

    plugin_meta: list[tuple[str, str]] = []
    staged_names = list_staged_skills(staging)
    for name in staged_names:
        plugin_meta.append(build_plugin(name, staging, plugins_root))
    plugin_meta.append(build_suite_plugin(staging, plugins_root, staged_names))

    write_marketplace(plugin_meta)
    print(f"Built {len(plugin_meta)} plugins ({len(staged_names)} standalone + 1 full bundle)")

    readme = plugins_root / "README.md"
    readme.write_text(
        "# Generated plugins (do not edit)\n\n"
        "Rebuilt from `tools/`, `guides/`, `workflows/` by `./scripts/bundle_all_skills.sh`.\n\n"
        "Each folder is a self-contained plugin:\n\n"
        "```text\n"
        "plugins/<name>/.claude-plugin/plugin.json\n"
        "plugins/<name>/skills/<name>/SKILL.md\n"
        "plugins/pruna-full/skills/*               # all skills in one plugin\n"
        "```\n\n"
        "**Install options:**\n"
        "- Standalone tool/router: `/plugin install p-image@pruna-skills`\n"
        "- Workflow with deps embedded: `/plugin install avatar-multi-scene@pruna-skills`\n"
        "- Everything: `/plugin install pruna-full@pruna-skills`\n"
        "- npx skills: `npx skills add ./plugins/<name>/skills --skill <name>`\n"
        "- ClawHub plugin: `clawhub package publish ./plugins/<name>`\n"
        "- ClawHub skill: `clawhub skill publish ./plugins/<name>/skills/<name>`\n"
    )


if __name__ == "__main__":
    main()
