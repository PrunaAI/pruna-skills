"""Human-in-the-loop phase gates for workflow plan runners.

See references/policies/staged-generation-gate.md
"""

from __future__ import annotations

import json
from pathlib import Path


def load_generation_status(out_dir: Path) -> dict:
    status_path = out_dir / "generation_status.json"
    if not status_path.exists():
        return _default_status()
    try:
        data = json.loads(status_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return _default_status()
    if isinstance(data, list):
        return {**_default_status(), "scenes": data}
    status = _default_status()
    status.update(data)
    return status


def write_generation_status(out_dir: Path, status: dict) -> None:
    (out_dir / "generation_status.json").write_text(
        json.dumps(status, indent=2) + "\n", encoding="utf-8"
    )


def _default_status() -> dict:
    return {
        "phase_song_approved": False,
        "phase_a_approved": False,
        "phase_b_approved": False,
    }


def ensure_gate(
    out_dir: Path,
    *,
    flag: str,
    approve_flag: bool,
    skip_gate: bool,
    label: str,
    approve_cli: str,
) -> None:
    if skip_gate or approve_flag:
        return
    status = load_generation_status(out_dir)
    if status.get(flag):
        return
    raise SystemExit(
        f"{label} blocked: review outputs under {out_dir}, then re-run with "
        f"{approve_cli} or set {flag}=true in generation_status.json"
    )


def ensure_phase_song_allowed(
    out_dir: Path, *, approve_flag: bool, skip_gate: bool, label: str
) -> None:
    ensure_gate(
        out_dir,
        flag="phase_song_approved",
        approve_flag=approve_flag,
        skip_gate=skip_gate,
        label=label,
        approve_cli="--approve-song",
    )


def ensure_phase_a_allowed(
    out_dir: Path, *, approve_flag: bool, skip_gate: bool, label: str
) -> None:
    ensure_gate(
        out_dir,
        flag="phase_a_approved",
        approve_flag=approve_flag,
        skip_gate=skip_gate,
        label=label,
        approve_cli="--approve-stills",
    )


def ensure_phase_b_allowed(
    out_dir: Path, *, approve_flag: bool, skip_gate: bool, label: str
) -> None:
    ensure_gate(
        out_dir,
        flag="phase_b_approved",
        approve_flag=approve_flag,
        skip_gate=skip_gate,
        label=label,
        approve_cli="--approve-clips",
    )


def apply_approve_flags(args, out_dir: Path) -> dict:
    """Apply --approve-* CLI flags to generation_status.json; return updated status."""
    status = load_generation_status(out_dir)
    if getattr(args, "approve_song", False):
        status["phase_song_approved"] = True
        print("Marked phase_song_approved=true in generation_status.json")
    if getattr(args, "approve_stills", False):
        status["phase_a_approved"] = True
        print("Marked phase_a_approved=true in generation_status.json")
    if getattr(args, "approve_clips", False):
        status["phase_b_approved"] = True
        print("Marked phase_b_approved=true in generation_status.json")
    write_generation_status(out_dir, status)
    return status
