"""Common argparse and generation-gate dispatch for workflow plan runners."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from generation_gate import (
    apply_approve_flags,
    ensure_phase_a_allowed,
    ensure_phase_b_allowed,
    ensure_phase_song_allowed,
    load_generation_status,
    write_generation_status,
)


@dataclass
class GateRule:
    requires: str  # phase_song_approved | phase_a_approved | phase_b_approved
    approve_flag: str
    skip_flag: str


@dataclass
class PlanConfig:
    phases: tuple[str, ...]
    default_phase: str
    phase_fn: Callable[[str, argparse.Namespace], None]
    gates: dict[str, list[GateRule]] = field(default_factory=dict)
    song_phases: tuple[str, ...] = ()
    reset_after: dict[str, list[str]] = field(default_factory=dict)
    approve_only_exit: bool = True


def add_common_args(parser: argparse.ArgumentParser, *, phases: tuple[str, ...], default: str) -> None:
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--phase", choices=(*phases, "all"), default=default)
    parser.add_argument("--approve-song", action="store_true")
    parser.add_argument("--approve-stills", action="store_true")
    parser.add_argument("--approve-clips", action="store_true")
    parser.add_argument("--yes-skip-song-gate", action="store_true")
    parser.add_argument("--yes-skip-stills-gate", action="store_true")
    parser.add_argument("--yes-skip-clips-gate", action="store_true")
    parser.add_argument("--assemble-only", action="store_true")
    parser.add_argument("--only", nargs="+", metavar="ID")


def _flag_attr(flag: str) -> str:
    return flag.lstrip("-").replace("-", "_")


def _ensure_rule(out_dir: Path, args: argparse.Namespace, rule: GateRule, label: str) -> None:
    approve = getattr(args, _flag_attr(rule.approve_flag), False)
    skip = getattr(args, _flag_attr(rule.skip_flag), False)
    if rule.requires == "phase_song_approved":
        ensure_phase_song_allowed(out_dir, approve_flag=approve, skip_gate=skip, label=label)
    elif rule.requires == "phase_a_approved":
        ensure_phase_a_allowed(out_dir, approve_flag=approve, skip_gate=skip, label=label)
    elif rule.requires == "phase_b_approved":
        ensure_phase_b_allowed(out_dir, approve_flag=approve, skip_gate=skip, label=label)


def apply_phase_gates(args: argparse.Namespace, out_dir: Path, config: PlanConfig) -> None:
    run_phase = args.phase
    rules = config.gates.get(run_phase, [])
    if run_phase == "all":
        for phase_rules in config.gates.values():
            for rule in phase_rules:
                _ensure_rule(out_dir, args, rule, f"Phase {run_phase}")
        return
    for rule in rules:
        _ensure_rule(out_dir, args, rule, f"Phase {run_phase}")


def reset_status_flags(out_dir: Path, flags: list[str]) -> None:
    status = load_generation_status(out_dir)
    for flag in flags:
        status[flag] = False
    write_generation_status(out_dir, status)


def run_plan_cli(config: PlanConfig, *, extra_args: Callable[[argparse.ArgumentParser], None] | None = None) -> None:
    parser = argparse.ArgumentParser()
    add_common_args(parser, phases=config.phases, default=config.default_phase)
    if extra_args:
        extra_args(parser)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    apply_approve_flags(args, args.out_dir)
    if config.approve_only_exit and _approve_only(args):
        return

    apply_phase_gates(args, args.out_dir, config)

    phases = list(config.phases) if args.phase == "all" else [args.phase]
    for phase in phases:
        config.phase_fn(phase, args)
        for flag in config.reset_after.get(phase, []):
            reset_status_flags(args.out_dir, [flag])


def _approve_only(args: argparse.Namespace) -> bool:
    if args.only:
        return False
    flags = [args.approve_song, args.approve_stills, args.approve_clips]
    if sum(1 for f in flags if f) != 1:
        return False
    return args.phase in ("song", "stills", "video", "assemble", "cuts", "align", "tts", "render")


def load_plan(args: argparse.Namespace) -> dict[str, Any]:
    return json.loads(args.plan.read_text(encoding="utf-8"))
