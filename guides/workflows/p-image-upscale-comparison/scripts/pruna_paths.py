#!/usr/bin/env python3
"""Path helpers for portable workflow skill bundles."""

from __future__ import annotations

import os
from pathlib import Path


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def sibling_script(name: str) -> Path:
    return Path(__file__).resolve().parent / name
