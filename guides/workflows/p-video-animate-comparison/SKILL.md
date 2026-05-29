---
name: p-video-animate-comparison
description: Motion-transfer slider renders and mixed avatar+animate announcement workflows. Use for p-video-animate slider demos, comparison MP4s, or multi-scene reels with animate beats; canonical workflow is multi-scene-avatar-video.
license: MIT
metadata:
  version: "0.0.1"
---

# P-Video-Animate comparison

**Canonical workflow:** [multi-scene-avatar-video](../multi-scene-avatar-video/SKILL.md)

Covers **slider comparison renders** and how **`p-video-animate`** fits into mixed reels.

**Visual variety:** [visual-variety-bible.md](../../../references/visual-variety-bible.md) — each animate slider row uses distinct **`visual_style_tag`** with unique backgrounds, camera angles, and lighting per persona still.

**Slider renderer:** [`scripts/generate_video_comparison.py`](./scripts/generate_video_comparison.py) · **Plan runner:** [`scripts/run_from_plan.py`](./scripts/run_from_plan.py) (default `--phase stills`)

**Staged generation:** [staged-generation-gate.md](../../../references/staged-generation-gate.md)

Install: `./scripts/install_skill.sh p-video-animate-comparison`

## Human-in-the-loop (required)

Default runner behavior is **`--phase stills`** — reference plates and motion sources only. Do not call `p-video-animate` until the user approves stills. See [staged-generation-gate.md](../../../references/staged-generation-gate.md).

| Step | Action |
|------|--------|
| 1 | Confirm scene table with user |
| 2 | Phase A: parallel `p-image` curls or [`run_from_plan.py`](./scripts/run_from_plan.py) `--phase stills` |
| 3 | User reviews stills → `--approve-stills --phase video` |
| 4 | Phase C: slider renders with [`generate_video_comparison.py`](./scripts/generate_video_comparison.py) |

## When to use

- **`animate`** scene rows — motion template vs animated subject comparison MP4s
- Mixed reels combining **`avatar`** talking heads and **`animate`** slider beats
- Batch slider renders from JSON config

## How the models fit together

See [animate-beats.md](../multi-scene-avatar-video/animate-beats.md) for the full pipeline. Summary:

1. **Motion template** — upload `.mp4` or generate with **`p-video-avatar`** (must be prompted to speak)
2. **Reference image** — persona still; style and identity come from here
3. **`p-video-animate`** — transfers motion from video onto image
4. **Slider render** — optional side-by-side comparison MP4

## Key model guidance

### `p-video-animate`

- Match pose, framing, and limb visibility between image and motion template
- Use **`instruction_prompt`** to preserve identity while following source motion
- Stylized personas (3D, claymation, anime, Disney/Pixar, cyberpunk, blockbuster film, game cinematic) work when shot size and pose align — severe proportion mismatch breaks limbs
- Plan **`visual_style_tag`**, **`setting_tag`**, **`camera_tag`**, and **`lighting_tag`** on each persona still — no two refs in a slider row should share the same world

### Motion templates (`p-video-avatar`)

- Prompt for **speaking** — lip movement, explain gestures, continuous camera
- Silent smile/wave-only templates produce weak animate results

### Mixed reel

- Interleave **`avatar`** and **`animate`** rows, or end slider-heavy reels with an **`avatar`** CTA

## Slider renderer

[`scripts/generate_video_comparison.py`](./scripts/generate_video_comparison.py)

Requires `ffmpeg` and Pillow:

```bash
pip install -r scripts/requirements.txt
```

**Single row:**

```bash
python3 scripts/generate_video_comparison.py \
  --source path/to/motion-template.mp4 \
  --output path/to/animated-output.mp4 \
  --render output/scene_compare.mp4
```

**Batch:** [`examples/workflows/p-video-animate-comparison/batch.template.json`](../../../examples/workflows/p-video-animate-comparison/batch.template.json)

## Example plan + runner

[`examples/workflows/p-video-animate-comparison/example-prompt.md`](../../../examples/workflows/p-video-animate-comparison/example-prompt.md)

Optional automation: [`scripts/run_from_plan.py`](./scripts/run_from_plan.py)

## Background music (launch reels)

After ffmpeg concat on **any** launch reel, mix a low-volume **instrumental bed** under avatar VO:

```bash
export REPLICATE_API_TOKEN=r8_...

python3 guides/workflows/_shared/scripts/launch_background_music.py \
  --video output/my-reel/final.mp4 \
  --prompt "Instrumental light electronic pop bed, soft groove and mellow synth pads, calm positive tech atmosphere, understated background music, no vocals, 94 BPM" \
  --volume 0.12 \
  --out output/my-reel/final_with_music.mp4
```

Replace-comparison plans: set `background_music` in JSON or pass `--background-music` on [`run_from_plan.py`](../p-video-replace-comparison/scripts/run_from_plan.py). Tool: [stable-audio-2.5](../../../tools/audio/stable-audio-2.5/SKILL.md).

## Related

| Topic | Location |
|-------|----------|
| In-video replacement sliders (different model) | [p-video-replace-comparison](../p-video-replace-comparison/SKILL.md) |
| Mixed avatar + animate workflow | [multi-scene-avatar-video/SKILL.md](../multi-scene-avatar-video/SKILL.md) |
| Animate beat pipeline & alignment | [animate-beats.md](../multi-scene-avatar-video/animate-beats.md) |
| Visual variety bible | [visual-variety-bible.md](../../../references/visual-variety-bible.md) |
| Model API | [p-video-animate/SKILL.md](../../../tools/video/p-video-animate/SKILL.md) |
| Prompt templates | [prompt-templates.md](../multi-scene-avatar-video/prompt-templates.md) |

## Install

```bash
cp -R guides/workflows/multi-scene-avatar-video ~/.cursor/skills/
```
