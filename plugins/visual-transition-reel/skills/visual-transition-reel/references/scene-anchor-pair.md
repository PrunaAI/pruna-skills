# Scene anchor pair (visual transitions)

Canonical pattern for **smooth visual transitions** with Pruna **`p-video`**: two stills bracket motion; a **`prompt`** describes what happens **between** them. No narration required.

Related: [scene-anchor-triple.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/scene-anchor-triple/SKILL.md) (pair + audio) · [p-video](../../p-video/SKILL.md) · [p-image](../../p-image/SKILL.md) · [p-image-edit](../../p-image-edit/SKILL.md)

## The pair

Each scene row supplies **two Pruna file URLs** (from `POST /v1/files`) plus a motion **`prompt`** and explicit **`duration`**:

| Anchor | `input` field | Role |
|--------|---------------|------|
| **First frame** | `image` | Opening composition |
| **Last frame** | `last_frame_image` | Closing composition the clip moves toward |
| **Transition motion** | `prompt` | Camera + action between the two plates — not a description of the stills |
| **Timing** | `duration` | 1–20s on P-API; prefer **4–5s** for clean arcs |

```json
{
  "prompt": "OPEN: hold wide. MID: slow crane down, neon signs flicker. CLOSE: settle on end pose.",
  "image": "https://api.pruna.ai/v1/files/START_ID",
  "last_frame_image": "https://api.pruna.ai/v1/files/END_ID",
  "duration": 5,
  "resolution": "720p",
  "fps": 24
}
```

**Do not** set `duration` when `audio` is also present — use [scene-anchor-triple.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/scene-anchor-triple/SKILL.md) instead.

## Stills phase (`p-image` + `p-image-edit`)

| Still | Source | Plan field |
|-------|--------|------------|
| **Hero** (optional) | [`p-image`](../../p-image/SKILL.md) text prompt | `hero_prompt` |
| **Start** | Hero + [`p-image-edit`](../../p-image-edit/SKILL.md) `edit_prompt` | `edit_prompt` |
| **End** | Start still + `p-image-edit` `last_frame_edit_prompt` | `last_frame_edit_prompt` |

Or skip generation: upload user photos → `/v1/files` → set `image_source: "upload"` with local paths in the runner manifest.

Run **hero** once, then **start stills in parallel**, then **end stills in parallel** from each start still.

### Edit prompt rules

- **Start still:** OPENING composition — what the viewer sees at beat open. Prefix with `OPENING:` or `OPEN:` when helpful.
- **End still:** CLOSING composition — clear end pose before the cut. Prefix with `CLOSING:` or `CLOSE:`.
- Keep subject identity, lighting era, and aspect ratio locked via a shared **`style_bible`** appended to every image prompt.
- Change **only** pose, camera, background beat, or prop state between start and end — not character species or art medium mid-scene.

## Video phase

After **all** start and end URLs exist for every scene row:

- **`POST /v1/predictions`** with `Model: p-video` — **parallel** when scenes are independent
- **`video_prompt`** uses OPEN → MID → CLOSE structure (motion only)
- Optional **`draft: true`** on the full chain for cheap motion approval, then rerun finals

Helper: [`p_video_payload.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/p_video_payload.py) — pass `duration`, omit `audio`.

## Frame chain (multi-scene continuity)

**Chain only when motion continues** — same location, same moment, no time jump. Use a **composed start still** (hard cut) for new beats.

| Situation | `chain_from_previous` | Join style |
|-----------|----------------------|------------|
| Continuous action (run → leap) | `true` | Short crossfade (~0.12–0.15s) after extract |
| New beat / location / pause | `false` | Hard cut — composed OPENING still |
| First scene | `false` | — |

| `frame_chain_mode` | Next scene `image` when chained | Render order |
|--------------------|---------------------------------|--------------|
| **`extract_last_frame`** | ffmpeg last frame from prior clip | **Sequential** when any scene chains |
| **`parallel_vignettes`** | each scene uses its own start still | **Parallel** — hard cuts between vignettes |
| **`planned_stills`** | prior scene end still URL | **Parallel** once all stills exist |

**Why extract?** Planned end stills often differ from the model's actual last frame → visible jump at cuts. Prefer **`extract_last_frame`** for continuous motion; use **`parallel_vignettes`** for montage reels.

```text
Scene 1: start_1 → end_1   duration=5   chain→2
Scene 2: extract(clip_1) → end_2   duration=4   hard cut→3
Scene 3: start_3 → end_3   duration=5
```

## Assembly

1. **Concat** clips in scene order via [`concat_clips.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/concat_clips.py)
2. Per-join **`crossfades`**: chain joins get ~0.12–0.15s; hard cuts get 0
3. **Normalize audio** (48 kHz stereo) when mixing clips with different native audio formats — see runner `assemble_movie` pattern
4. **Optional bed** — [stable-audio-2.5](../../stable-audio-2.5/SKILL.md) mixed under native SFX (~0.08–0.15 volume)

## Pair vs triple

| Pattern | Anchors | Duration | Workflow |
|---------|---------|----------|----------|
| **Pair** | `image` + `last_frame_image` + `prompt` | `duration` | [visual-transition-reel](../SKILL.md) |
| **Triple** | pair + `audio` | follows audio | [narrated-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/narrated-multi-scene/skills/narrated-multi-scene/SKILL.md) |

Upgrade a pair scene to triple by adding TTS → upload → `audio` and removing `duration`.

## Plan JSON shape

```json
{
  "title": "Neon alley handoff",
  "hero_prompt": "Cinematic cyberpunk alley, single subject, 16:9 one frame",
  "ritual_seed": "k7Qm2xP9",
  "frame_chain_mode": "extract_last_frame",
  "assembly": {
    "chain_crossfade_seconds": 0.15,
    "hard_cut_crossfade_seconds": 0
  },
  "defaults": {
    "resolution": "720p",
    "fps": 24,
    "aspect_ratio": "16:9",
    "duration_seconds": 5
  },
  "style_bible": "Neon magenta cyan, wet pavement reflections, cinematic 16:9",
  "scenes": [
    {
      "id": "01_alley",
      "chain_from_previous": false,
      "duration_seconds": 5,
      "edit_prompt": "OPENING: Wide alley, figure small in frame, neon kanji",
      "last_frame_edit_prompt": "CLOSING: Same alley, figure closer, hand on railing",
      "video_prompt": "OPEN: hold wide. MID: slow dolly in. CLOSE: settle on end pose."
    },
    {
      "id": "02_rooftop",
      "chain_from_previous": true,
      "duration_seconds": 4,
      "edit_prompt": "OPENING: Rooftop edge, city sprawl, figure turns toward camera",
      "last_frame_edit_prompt": "CLOSING: Same rooftop, figure mid-step toward ledge",
      "video_prompt": "OPEN: wind ripples coat. MID: figure turns. CLOSE: step forward — hold."
    }
  ]
}
```

## Intake checklist (per scene)

- [ ] `edit_prompt` — OPENING still (from hero or upload)
- [ ] `last_frame_edit_prompt` — CLOSING still (from start still)
- [ ] `video_prompt` — OPEN / MID / CLOSE **motion** between the two plates
- [ ] `duration_seconds` (or global default)
- [ ] `chain_from_previous` — only if motion truly continues from prior clip
- [ ] `resolution` / `fps` / `draft` policy

## Workflows that implement this

- [visual-transition-reel](../SKILL.md) — primary workflow
- [image-to-video](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/image-to-video/skills/image-to-video/SKILL.md) — one pair beat
- [p-video](../../p-video/SKILL.md) — API reference (visual transition mode)
- Example runner: [`run_from_plan.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/visual-transition-reel/scripts/run_from_plan.py)
