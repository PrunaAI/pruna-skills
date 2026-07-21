#!/usr/bin/env python3
"""Load skills.catalog.json — single source of skill names for bundle/publish/docs."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO / ".maintainer" / "skills.catalog.json"
GITHUB_REPO = "PrunaAI/pruna-skills"


def load_catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text())


def guides(catalog: dict | None = None) -> list[str]:
    return list((catalog or load_catalog()).get("guides", []))


def tools(catalog: dict | None = None) -> list[str]:
    c = catalog or load_catalog()
    out: list[str] = []
    for group in c["tools"].values():
        out.extend(group)
    return out


def workflows(catalog: dict | None = None) -> list[str]:
    return list((catalog or load_catalog())["workflows"])


def suite_skills(catalog: dict | None = None) -> list[str]:
    return list((catalog or load_catalog()).get("suite", []))


def all_primary_skills(catalog: dict | None = None) -> list[str]:
    """Guides + tools + workflows + suite."""
    c = catalog or load_catalog()
    names: list[str] = []
    names.extend(guides(c))
    names.extend(tools(c))
    names.extend(workflows(c))
    names.extend(suite_skills(c))
    return names


def find_skill_dir(name: str) -> Path | None:
    for base in (
        REPO / "skills" / "guides",
        REPO / "skills" / "image",
        REPO / "skills" / "video",
        REPO / "skills" / "audio",
        REPO / "skills" / "workflows",
        REPO / "skills" / "suite",
    ):
        cand = base / name
        if (cand / "SKILL.md").is_file():
            return cand
    return None


def read_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text()
    if not text.startswith("---"):
        return {}
    block = text.split("---", 2)[1]
    out: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith(" ") and not line.startswith("-"):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


@lru_cache(maxsize=1)
def skill_descriptions() -> dict[str, str]:
    out: dict[str, str] = {}
    for name in all_primary_skills():
        skill_dir = find_skill_dir(name)
        if not skill_dir:
            continue
        fm = read_frontmatter(skill_dir / "SKILL.md")
        out[name] = fm.get("description") or f"Skill `{name}`"
    return out


def install_cmd(name: str) -> str:
    return f"npx skills add {GITHUB_REPO}@{name} -y"


def description(name: str) -> str:
    return skill_descriptions().get(name, f"Skill `{name}`")


def overview_table(names: list[str], *, include_install: bool = True) -> str:
    """Markdown table: Skill | Description | Install."""
    cols = ["Skill", "Description"]
    if include_install:
        cols.append("Install")
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    lines = [
        "| " + " | ".join(cols) + " |",
        sep,
    ]
    for name in names:
        desc = description(name).replace("|", "\\|")
        row = [f"`{name}`", desc]
        if include_install:
            row.append(f"`{install_cmd(name)}`")
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def strip_skill_md_links(text: str) -> str:
    """Turn [label](.../skill-name/SKILL.md) into `skill-name` for catalog skills."""
    names = set(all_primary_skills())

    def repl(m: re.Match[str]) -> str:
        label, path = m.group(1), m.group(2)
        base = Path(path).parent.name
        if base in names:
            return f"`{base}`"
        bare = label.replace(" SKILL.md", "").strip().strip("`")
        if bare in names:
            return f"`{bare}`"
        return m.group(0)

    return re.sub(r"\[([^\]]+)\]\(([^)]*SKILL\.md)\)", repl, text)
