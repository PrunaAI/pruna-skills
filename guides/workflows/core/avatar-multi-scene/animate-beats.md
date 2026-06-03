# Animate beats in multi-scene reels

How **`p-video-animate`** fits into mixed **`avatar` + `animate`** pieces built with [multi-scene-avatar-video](./SKILL.md).

## What each model does

| Model | Role in an animate row |
|-------|------------------------|
| **`p-image` / `p-image-edit`** | Reference stills — motion-source portrait and persona subjects |
| **`p-video-avatar`** | Optional: generate a **motion template** (talking-head source video) when you don't have a licensed `.mp4` |
| **`p-video-animate`** | Transfer motion from source video onto reference image |
| **Slider render** | Optional comparison MP4 (motion template vs animated output) via [`generate_video_comparison.py`](../../../guides/workflows/_shared/scripts/generate_video_comparison.py) |

**`p-video-animate`** takes:

- **`video`** — motion, timing, camera path, acting beats, audio source
- **`image`** — subject identity, style, wardrobe, environment look

Output keeps **motion from the video**, **appearance from the image**.

## Animate row pipeline

```text
Hero anchor (p-image)
  → motion-source still (p-image-edit)
  → motion template (p-video-avatar OR upload .mp4)
  → persona still(s) (p-image or p-image-edit)
  → p-video-animate (one job per persona)
  → optional slider compare MP4
```

## Making motion templates work

When **`p-video-avatar`** creates the source video for **`p-video-animate`**, prompt it like a **speaking** clip — not a portrait pose.

| Field | Guidance |
|-------|----------|
| Motion-source still | `mouth clearly visible ready to speak`; medium close-up; unobstructed face |
| **`video_prompt`** | `speaks directly to camera`, `clear lip movement`, explain gestures, head nods; prefix with `Camera moves continuously … never locked-off` |
| **`voice_prompt`** | Conversational delivery throughout the line — not gesture-only direction at the end |

Smile/wave/nod are fine **after** explicit speaking direction. Smile/wave **instead of** speaking produces silent templates — weak lip sync and poor slider demos.

## Making `p-video-animate` work

### Alignment (most important)

Match **shot size**, **facing direction**, and **visible limbs** between reference image and motion template.

| Pairing | Outcome |
|---------|---------|
| Same framing and pose | Best transfer |
| Same character type, slight angle difference | Good; optional repose with **`p-image-edit`** |
| Stylized / mascot / chibi on human full-body motion | Limbs and contact points often break |
| Profile motion + front-facing still | Head/shoulder artifacts |

Repose before animate when close but not exact: *"Change only: match pose and camera to reference video frame; keep identity and outfit."*

### Reference stills (personas)

- Face and mouth large enough for lip-sync when the template speaks
- **`instruction_prompt`** steers behavior without fighting source motion:

```text
Animate the reference subject using the exact motion, timing, and camera movement from the source video. Keep identity and outfit from the reference image.
```

- **Style variety** (photoreal, premium anime, claymation, Disney/Pixar 3D, cyberpunk, blockbuster movie, AAA game cinematic) on one motion template shows range in slider demos — each style still needs reasonable pose/framing alignment **and** its own background, camera angle, and lighting. Record `visual_style_tag`, `setting_tag`, `camera_tag`, and `lighting_tag` per ref. See [visual-variety-bible.md](../../../../../references/shared/visual-variety-bible.md).

### API fields

- **`resolution`**: `720p` or `1080p`
- **`target_fps`**: `original` (default), `24`, or `48`
- **`save_audio`**: `true` when the motion template has dialogue
- **`seed`**: lock per persona row when retrying

### Persona style ladder (animate slider rows)

When building eye-catching comparison reels, generate **3–4 persona stills per animate row** — each a different **`visual_style_tag`** with distinct **`setting_tag`**, **`camera_tag`**, and **`lighting_tag`**:

| Ref slot | Example style | Example setting + light |
|----------|---------------|-------------------------|
| 1 | Photoreal UGC | neutral wall, soft ring light |
| 2 | Premium anime | neon rain alley, dramatic anime key |
| 3 | Claymation | miniature living room, warm practical lamp |
| 4 | Disney / fairy-tale 3D | enchanted garden, golden hour |
| 5 (optional) | Cyberpunk | rain-slick alley, magenta-cyan edge |
| 6 (optional) | AAA game cinematic | alien canyon, volumetric sun shafts |

Full prompt patterns: [visual-variety-bible.md](../../../../../references/shared/visual-variety-bible.md).

Run [p-video-animate-quality-checklist.md](../../../../../references/video/p-video-animate-quality-checklist.md) on inputs and outputs.

## Mixed reel structures

### Interleaved avatar + animate

| # | Type | Beat |
|---|------|------|
| 1 | avatar | Hook |
| 2 | animate | Slider demo |
| 3 | avatar | Feature / proof |
| 4 | animate | Second demo |
| 5 | avatar | CTA |

### Slider-heavy + CTA close

| # | Type | Beat |
|---|------|------|
| 1–N | animate | Slider comparisons (3–4 persona variations each) |
| N+1 | avatar | CTA — return hero spokesperson, clean studio, short close |

Avatar CTA rows use **`type: avatar`** → deliver `{id}_avatar.mp4`. Animate rows → `{id}_compare.mp4` (or animated-only if no slider).

## Slider comparison (optional)

Requires `ffmpeg` + Pillow (`pip install -r guides/workflows/_shared/scripts/requirements.txt`).

```bash
python3 guides/workflows/_shared/scripts/generate_video_comparison.py \
  --source path/to/motion-template.mp4 \
  --output path/to/animated-output.mp4 \
  --render path/to/scene_compare.mp4
```

Multi-sample mode: [`examples/workflows/launches/p-video-animate-comparison/`](../../../../examples/workflows/launches/p-video-animate-comparison/)

## Assembly

Concat clips in scene-table order — avatar MP4s and animate comparison MP4s interleaved as planned. Level audio in your editor or ffmpeg.

Example plan schema and runner: [`examples/workflows/launches/p-video-animate-comparison/`](../../../../examples/workflows/launches/p-video-animate-comparison/) and [`run_from_plan.py`](../../../guides/workflows/launches/p-video-animate-comparison/scripts/run_from_plan.py).
