#!/usr/bin/env python3
"""Load skills.catalog.json — single source of skill names for bundle/publish/docs."""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO / ".maintainer" / "skills.catalog.json"


def load_catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text())


def all_primary_skills(catalog: dict | None = None) -> list[str]:
    c = catalog or load_catalog()
    names: list[str] = []
    for group in c["tools"].values():
        names.extend(group)
    names.extend(workflows(c))
    return names


def tools(catalog: dict | None = None) -> list[str]:
    c = catalog or load_catalog()
    out: list[str] = []
    for group in c["tools"].values():
        out.extend(group)
    return out


def workflows(catalog: dict | None = None) -> list[str]:
    return list((catalog or load_catalog())["workflows"])


def suite_plugins(catalog: dict | None = None) -> list[str]:
    return list((catalog or load_catalog()).get("suite", []))
