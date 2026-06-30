#!/usr/bin/env python3
"""Backward-compatible wrapper — canonical: catalog/workflows/_shared/scripts/generate_upscale_comparison.py"""
import runpy
from pathlib import Path

runpy.run_path(
    str(
        Path(__file__).resolve().parents[1]
        / "catalog/workflows/_shared/scripts/generate_upscale_comparison.py"
    ),
    run_name="__main__",
)
