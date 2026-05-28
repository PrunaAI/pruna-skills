"""Path helpers for portable workflow skill bundles."""

from __future__ import annotations

import os
from pathlib import Path


def skill_root() -> Path:
    """Skill root directory (parent of scripts/)."""
    return Path(__file__).resolve().parent.parent


def repo_root() -> Path:
    """Repository root when running from a clone (guides/workflows/_shared/scripts -> repo)."""
    return Path(__file__).resolve().parents[4]


def sibling_script(name: str) -> Path:
    return Path(__file__).resolve().parent / name


def default_template(name: str) -> Path:
    return skill_root() / "templates" / name


def default_out_dir(project_name: str) -> Path:
    env = os.environ.get("PRUNA_OUT_DIR", "").strip()
    if env:
        return Path(env)
    return Path.cwd() / "output" / project_name


def resolve_plan_path(explicit: Path | None, *, env_var: str, template_name: str, repo_fallback: Path) -> Path:
    if explicit is not None:
        return explicit
    env = os.environ.get(env_var, "").strip()
    if env:
        return Path(env)
    template = default_template(template_name)
    if template.exists():
        return template
    return repo_fallback
