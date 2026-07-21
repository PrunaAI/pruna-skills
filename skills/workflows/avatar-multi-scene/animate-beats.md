# Animate beats in multi-scene reels

How **`p-video-animate`** fits into mixed **`avatar` + `animate`** pieces built with `avatar-multi-scene`.

## What each model does

| Model | Role in an animate row |
|-------|------------------------|
| **`p-image` / `p-image-edit`** | Reference stills — motion-source portrait and persona subjects |
| **`p-video-avatar`** | Optional: generate a **motion template** (talking-head source video) when you don't have a licensed `.mp4` |
| **`p-video-animate`** | Transfer motion from source video onto reference image |
| **Slider render** | Optional comparison MP4 (motion template vs animated output) via `avatar-multi-scene` |

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

- **Style variety** (photoreal, premium anime, claymation, Disney/Pixar 3D, cyberpunk, blockbuster movie, AAA game cinematic) on one motion template shows range in slider demos — each style still needs reasonable pose/framing alignment **and** its own background, camera angle, and lighting. Record `visual_style_tag`, `setting_tag`, `camera_tag`, and `lighting_tag` per ref. See generation-diversity.md#visual-variety (`generation-diversity`).

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

Full prompt patterns: generation-diversity.md#visual-variety (`generation-diversity`).

Run `video-prompting` on inputs and outputs.

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

Requires `ffmpeg` + Pillow (`pip install -r ./scripts/requirements-comparison.txt`).

```bash
python3 ffmpeg hstack slider (see workflow SKILL) \
  --source path/to/motion-template.mp4 \
  --output path/to/animated-output.mp4 \
  --render path/to/scene_compare.mp4
```

Multi-sample / multi-scene batch mode — copy [`batch.template.json`](./templates/batch.template.json), set `source`, `render`, and per-persona `samples[].output` paths, then:

```bash
python3 ffmpeg hstack slider (see workflow SKILL) --config ./templates/batch.template.json
```

Dry-run: add `--dry-run` to validate paths before rendering.

## Assembly

Concat clips in scene-table order — avatar MP4s and animate comparison MP4s interleaved as planned. Level audio in your editor or ffmpeg.

Batch config schema: [`batch.template.json`](./templates/batch.template.json) (`scenes[]` with `source`, `render`, and `samples[]` per row).
