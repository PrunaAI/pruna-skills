# Plan runner template

Workflow skills with `run_from_plan.py` share CLI flags and gate behavior via [`_shared/scripts/plan_runner.py`](workflows/_shared/scripts/plan_runner.py) and [`generation_gate.py`](workflows/_shared/scripts/generation_gate.py).

## skill.manifest.json — generation_phases

```json
{
  "generation_phases": {
    "default": "stills",
    "phases": ["stills", "tts", "video", "assemble"],
    "gates": {
      "tts": {
        "requires": "phase_a_approved",
        "approve_flag": "--approve-stills",
        "skip_flag": "--yes-skip-stills-gate"
      },
      "video": {
        "requires": "phase_a_approved",
        "approve_flag": "--approve-stills",
        "skip_flag": "--yes-skip-stills-gate"
      },
      "assemble": {
        "requires": "phase_b_approved",
        "approve_flag": "--approve-clips",
        "skip_flag": "--yes-skip-clips-gate"
      }
    },
    "requires_user_approval_before": ["p-video", "p-video-avatar"]
  }
}
```

Gate keys in `requires`: `phase_song_approved`, `phase_a_approved`, `phase_b_approved`.

Music-video adds `song` phase and `--approve-song` / `--yes-skip-song-gate`.

## Thin runner pattern

```python
#!/usr/bin/env python3
"""Workflow — see SKILL.md. Phased: references/shared/staged-generation-gate.md"""

from plan_runner import PlanConfig, run_plan_cli
from my_workflow_phases import run_phase

if __name__ == "__main__":
    run_plan_cli(PlanConfig(
        phases=("stills", "video", "assemble"),
        default_phase="stills",
        phase_fn=run_phase,
    ))
```

## Shared scripts (manifest `scripts.shared`)

| Script | Purpose |
|--------|---------|
| `pruna_api.py` | Upload, create, poll, download |
| `generation_gate.py` | `generation_status.json` + approve flags |
| `plan_runner.py` | Common argparse + gate dispatch |
| `stills_pipeline.py` | Hero + start/end stills batch |
| `p_video_payload.py` | Scene anchor triple payloads |
| `concat_clips.py` | ffmpeg concat |
| `launch_background_music.py` | Stable Audio bed |

**Do not fork** shared scripts into skill `scripts/` — `bundle_skill.sh` copies from `_shared/scripts/`.

## Standard CLI flags

| Flag | Purpose |
|------|---------|
| `--plan` | Plan JSON path |
| `--out-dir` | Output directory |
| `--phase` | Run one phase (default from manifest) |
| `--approve-stills` | Set `phase_a_approved` |
| `--approve-clips` | Set `phase_b_approved` |
| `--approve-song` | Set `phase_song_approved` (music-video) |
| `--yes-skip-stills-gate` | Automation bypass |
| `--yes-skip-clips-gate` | Automation bypass |
| `--assemble-only` | Concat/bed from existing clips |
| `--only ID …` | Regenerate named scenes/cuts |
