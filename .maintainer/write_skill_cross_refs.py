#!/usr/bin/env python3
"""Rewrite skill cross-refs: overview tables (description + install), no SKILL.md hyperlinks.

- Regenerates skills/suite/pruna/SKILL.md overview from catalog + frontmatter descriptions
- Converts ## Prerequisites / ## Install-related / ## Pruna tools / ## Related skills
  bash-only blocks into Skill | Description | Install tables
- Strips [label](.../SKILL.md) → `skill-name` across skills/**/*.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_catalog import (  # noqa: E402
    GITHUB_REPO,
    all_primary_skills,
    description,
    guides,
    install_cmd,
    overview_table,
    strip_skill_md_links,
    tools,
    workflows,
)

REPO = Path(__file__).resolve().parents[1]
SUITE_SKILL = REPO / "skills" / "suite" / "pruna" / "SKILL.md"

NPX_RE = re.compile(rf"npx skills add {re.escape(GITHUB_REPO)}@([a-z0-9][a-z0-9.-]*)\s+-y")
SECTION_HEAD = re.compile(r"^## (.+)$", re.M)

# Sections that should be overview tables when they list installs
TABLE_SECTIONS = {
    "Prerequisites",
    "Install",
    "Pruna tools",
    "Pruna / Replicate tools",
    "Related skills",
}

# Bullet / prose sections that name skills with `name` → overview table
SKILL_MENTION_SECTIONS = {
    "When NOT to use",
    "Typical next steps",
    "Related",
    "Related skills",
}

BACKTICK_SKILL_RE = re.compile(r"`([a-z0-9][a-z0-9.-]*)`")


def extract_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    parts = text.split("---", 2)
    return "---" + parts[1] + "---", parts[2].lstrip("\n")


def names_from_npx_block(block: str) -> list[str]:
    seen: list[str] = []
    for m in NPX_RE.finditer(block):
        name = m.group(1)
        if name not in seen:
            seen.append(name)
    return seen


def names_from_backticks(body: str) -> list[str]:
    catalog = set(all_primary_skills())
    seen: list[str] = []
    for m in BACKTICK_SKILL_RE.finditer(body):
        name = m.group(1)
        if name in catalog and name not in seen and name != "pruna":
            seen.append(name)
    return seen


def rewrite_table_section(title: str, body: str) -> str | None:
    """If body lists npx installs or skill backticks, return overview table."""
    from_npx = names_from_npx_block(body)
    has_suite = "pruna" in from_npx
    names = [n for n in from_npx if n != "pruna"]

    if not names and title in SKILL_MENTION_SECTIONS:
        names = names_from_backticks(body)
        # Already a generated overview table — leave alone
        if "| Skill | Description |" in body and "| Install |" in body:
            return None

    if not names and not (title == "Install" and has_suite):
        return None

    parts: list[str] = []
    if title == "Prerequisites":
        parts.append(
            "Install and load these skills before generating (skip if already in context "
            "via `@pruna`):"
        )
        parts.append("")
    elif title in ("Pruna tools", "Pruna / Replicate tools"):
        parts.append("Matching install for every model named above. Pick what you need:")
        parts.append("")
    elif title == "Related skills":
        parts.append("Install related skills when the job needs them:")
        parts.append("")
    elif title == "When NOT to use":
        parts.append("Use a different skill instead:")
        parts.append("")
    elif title == "Typical next steps":
        parts.append("Common follow-ons after this skill:")
        parts.append("")
    elif title == "Related":
        parts.append("Related skills:")
        parts.append("")

    if names:
        parts.append(overview_table(names))
        parts.append("")

    if has_suite or title == "Prerequisites":
        parts.append(f"Or install the full suite once: `{install_cmd('pruna')}`")
        parts.append("")

    if title == "Prerequisites":
        parts.append(
            "Follow each skill's **Before generating** / craft sections — do not restate "
            "guide content here."
        )
        parts.append("")

    return "\n".join(parts).rstrip() + "\n\n"


def split_sections(body: str) -> list[tuple[str | None, str]]:
    """Return [(heading|None, content)] preserving order. First may be preamble."""
    matches = list(SECTION_HEAD.finditer(body))
    if not matches:
        return [(None, body)]
    out: list[tuple[str | None, str]] = []
    if matches[0].start() > 0:
        out.append((None, body[: matches[0].start()]))
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        out.append((title, body[start:end]))
    return out


def rewrite_skill_md(path: Path) -> bool:
    original = path.read_text()
    fm, body = extract_frontmatter(original)
    body = strip_skill_md_links(body)

    chunks: list[str] = []
    for title, content in split_sections(body):
        if title is None:
            chunks.append(content)
            continue
        rewritten = None
        if title in TABLE_SECTIONS or title in SKILL_MENTION_SECTIONS:
            rewritten = rewrite_table_section(title, content)
        chunks.append(f"## {title}\n\n")
        chunks.append(rewritten if rewritten is not None else content)

    new_body = "".join(chunks)
    # Collapse excessive blank lines
    new_body = re.sub(r"\n{3,}", "\n\n", new_body)
    new_text = (fm + "\n\n" + new_body.lstrip("\n")) if fm else new_body
    if new_text != original:
        path.write_text(new_text)
        return True
    return False


def write_suite_skill() -> None:
    """Regenerate suite overview; keep depends frontmatter from existing file."""
    existing = SUITE_SKILL.read_text()
    fm, _ = extract_frontmatter(existing)
    if not fm:
        raise SystemExit(f"missing frontmatter: {SUITE_SKILL}")

    # Ensure depends list matches catalog children (not including pruna itself)
    child_names = guides() + tools() + workflows()
    # Rebuild depends block inside frontmatter
    fm_lines = fm.strip().splitlines()
    out_fm: list[str] = []
    i = 0
    while i < len(fm_lines):
        line = fm_lines[i]
        if line.strip() == "depends:":
            out_fm.append("depends:")
            i += 1
            while i < len(fm_lines) and fm_lines[i].startswith("  - "):
                i += 1
            for name in child_names:
                out_fm.append(f"  - {name}")
            continue
        out_fm.append(line)
        i += 1
    if "depends:" not in "\n".join(out_fm):
        # insert before closing ---
        out_fm = out_fm[:-1] + ["depends:"] + [f"  - {n}" for n in child_names] + [out_fm[-1]]

    body = f"""# pruna

All Pruna generative media skills — **guides**, **tools**, and **workflows** — in one recommended install.

## Install

```bash
{install_cmd("pruna")}
```

After install, start a **new chat**. Your agent picks skills from the suite by name.

## What's included

### Guides

{overview_table(guides())}

### Tools

{overview_table(tools())}

### Workflows

{overview_table(workflows())}

## Reading order

1. `generation-diversity` — ritual seed + QA before any paid call
2. Domain craft — `image-prompting` / `video-prompting` / `audio-prompting`
3. `pruna-api` — credentials, upload/poll/download
4. The **tool** skill for the API call
5. A **workflow** skill when the job is multi-step (agent runs curl + ffmpeg)

## Requirements

- `PRUNA_API_KEY` — https://dashboard.pruna.ai/ (see docs/api-setup.md)
- `REPLICATE_API_TOKEN` when using audio tools
- `curl`, `ffmpeg` / `ffprobe` for video assembly
"""
    SUITE_SKILL.write_text("\n".join(out_fm) + "\n\n" + body)


def strip_all_reference_md() -> int:
    n = 0
    for path in (REPO / "skills").rglob("*.md"):
        if path.name == "SKILL.md":
            continue
        text = path.read_text()
        new = strip_skill_md_links(text)
        if new != text:
            path.write_text(new)
            n += 1
    return n


def main() -> None:
    write_suite_skill()
    print(f"wrote {SUITE_SKILL.relative_to(REPO)}")

    changed = 0
    for path in sorted((REPO / "skills").rglob("SKILL.md")):
        if path == SUITE_SKILL:
            continue
        if rewrite_skill_md(path):
            changed += 1
            print(f"  updated {path.relative_to(REPO)}")
    refs = strip_all_reference_md()
    print(f"updated {changed} SKILL.md files; stripped links in {refs} reference md files")


if __name__ == "__main__":
    main()
