#!/usr/bin/env python3
"""Write canonical README-INSTALL.md for every primary skill (source tree)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from skill_catalog import all_primary_skills, load_catalog  # noqa: E402

GITHUB = "PrunaAI/pruna-skills"


def find_skill_dir(name: str) -> Path | None:
    for base in (REPO / "tools", REPO / "guides", REPO / "workflows"):
        for skill_md in base.rglob("SKILL.md"):
            if skill_md.parent.name == name:
                return skill_md.parent
    return None


def body(name: str) -> str:
    return f"""# {name}

## Install

```bash
npx skills add {GITHUB}@{name} -y
```

For a workflow with embedded tool dependencies, prefer:

```bash
npx plugins add {GITHUB} -y
# pick {name}
```

List all skills: `npx skills add {GITHUB} -l`

After install, start a **new chat**. See the [root README](../../../README.md).

## From a local clone

```bash
npx skills add .@{name} -y
# or:
npx skills add ./plugins/{name}/skills --skill {name} -y
```
"""


def main() -> None:
    catalog = load_catalog()
    written = 0
    for name in all_primary_skills(catalog):
        skill_dir = find_skill_dir(name)
        if skill_dir is None:
            print(f"skip {name}: source dir not found", file=sys.stderr)
            continue
        (skill_dir / "README-INSTALL.md").write_text(body(name))
        written += 1
        print(f"wrote {skill_dir.relative_to(REPO)}/README-INSTALL.md")
    print(f"README-INSTALL.md: {written} files")


if __name__ == "__main__":
    main()
