#!/usr/bin/env python3
"""Backward-compatible wrapper — canonical: guides/workflows/launches/p-video-replace-comparison/scripts/run_from_plan.py"""
import runpy
from pathlib import Path

runpy.run_path(
    str(
        Path(__file__).resolve().parents[1]
        / "guides/workflows/launches/p-video-replace-comparison/scripts/run_from_plan.py"
    ),
    run_name="__main__",
)
