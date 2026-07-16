#!/usr/bin/env python3
"""Inject shared generation policy section + reference files into bundled skills."""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
POLICIES = REPO / "references" / "policies"
MARKER = "<!-- shared-generation-policy -->"

TOOL_FILES = [
    "random-seed-ritual.md",
    "generation-diversity.md",
    "generation-quality-checklists.md",
]
WORKFLOW_FILES = TOOL_FILES + [
    "staged-generation-gate.md",
    "approval-red-flags.md",
    "workflow-feedback-gates.md",
    "parallel-execution.md",
]

TOOL_SECTION = f"""## Shared generation policy

{MARKER}

Before any paid `POST /v1/predictions`:

1. **[Random seed ritual](./references/random-seed-ritual.md)** — always first; derive axes via sum-mod.
2. **[Generation diversity](./references/generation-diversity.md)** — explicit prompts; rotate ≥2 scenario axes per session.
3. **[Quality checklists](./references/generation-quality-checklists.md)** — open output files and judge pass/fail before advancing.
"""

WORKFLOW_EXTRA = """
4. **[Staged generation gate](./references/staged-generation-gate.md)** — plan → stills → audio → video → assembly; never skip phases in one turn.
5. **[Approval red flags](./references/approval-red-flags.md)** — pause when plan, stills, or clips were not reviewed.
6. **[Workflow feedback gates](./references/workflow-feedback-gates.md)** — runner flags and per-workflow commands.
7. **[Parallel execution](./references/parallel-execution.md)** — async fan-out within each approved phase only.
"""


def profile(manifest: dict) -> str:
    return "workflow" if manifest.get("tool_skills") else "tool"


def policy_files(kind: str) -> list[str]:
    return WORKFLOW_FILES if kind == "workflow" else TOOL_FILES


def build_section(kind: str) -> str:
    body = TOOL_SECTION
    if kind == "workflow":
        body = body.rstrip() + WORKFLOW_EXTRA
    return body + "\n"


def inject(dest: Path) -> None:
    manifest_path = dest / "skill.manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.is_file() else {}
    kind = profile(manifest)
    refs_dir = dest / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    for name in policy_files(kind):
        src = POLICIES / name
        if not src.is_file():
            raise SystemExit(f"missing policy file: {src}")
        shutil.copy2(src, refs_dir / name)

    skill_md = dest / "SKILL.md"
    text = skill_md.read_text()
    section = build_section(kind)
    if MARKER in text:
        text = re.sub(
            r"## Shared generation policy\n\n" + re.escape(MARKER) + r"[\s\S]*?(?=\n## |\Z)",
            section.rstrip() + "\n\n",
            text,
            count=1,
        )
    else:
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[0] + "---" + parts[1] + "---\n\n" + section + parts[2].lstrip("\n")
        else:
            text = section + text
    skill_md.write_text(text)


def main() -> None:
    dest = Path(sys.argv[1]).resolve()
    if not (dest / "SKILL.md").is_file():
        raise SystemExit(f"no SKILL.md in {dest}")
    inject(dest)


if __name__ == "__main__":
    main()
