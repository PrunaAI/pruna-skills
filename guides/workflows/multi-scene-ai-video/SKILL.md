---
name: multi-scene-ai-video
description: Produces multiple Pruna p-video clips using the scene anchor triple (image + last_frame_image + audio per scene), first/last frame chaining, Gemini TTS, optional Stable Audio beds, async parallel jobs, then assembly. Use for narrated story films, episodic B-roll, or chaptered promos.
metadata:
  version: "0.0.3"
---

# Multi-scene AI video (Pruna `p-video` only)

Each scene = one **`p-video`** job (same model, separate predictions). Assembly is **outside** Pruna (ffmpeg or your editor). No **`p-video-avatar`** in this workflow.

See [p-video](../../../tools/video/p-video/SKILL.md) (first/last frame chaining), [scene-anchor-triple.md](../../../references/scene-anchor-triple.md), [audio-post-production.md](../../../references/audio-post-production.md), and [references/pruna-api.md](../../../references/pruna-api.md).

## Intake: ask before generating

**Do not** start scene 1 until the **whole** scene plan exists in writing (manifest or table):

| Topic | Questions |
|-------|-----------|
| **Story** | Order of scenes (1…N)? What changes between scenes (location, time, emotion)? |
| **Per scene *i*** | Primary `prompt`? **First frame** (`image`), **last frame** (`last_frame_image`), **narration** (`audio` URL)? `resolution` / `fps` / `draft`? |
| **Continuity** | Per scene: **`chain_from_previous`** only when motion continues (same moment/location). Otherwise composed OPENING still + hard cut. End stills via `p-image-edit`; extract last frame when chaining. |
| **Audio** | **Scene anchor triple (preferred):** TTS → upload → **`p-video`** with `image` + `last_frame_image` + `audio`. Optional **Stable Audio** bed in post only. |
| **Global** | Default `aspect_ratio` for text-only scenes? Global `seed` policy? |
| **Runtime** | Target total duration after assembly? |
| **Assembly** | Concat order; narration mux; bed mix volume (~0.08–0.15 under VO)? |

Ask follow-ups until every scene row has enough to build `input` without guessing.

### Scene table (template — fill during intake)

| `#` | Prompt | First frame (`image`) | Last frame (`last_frame_image`) | Narration (`audio`) | Mode |
|-----|--------|----------------------|----------------------------------|---------------------|------|
| 1 | motion prompt | start still | end still → scene 2 | TTS line → upload | triple |
| 2 | | = scene 1 end | end still → scene 3 | TTS line → upload | triple |

**Mode:** `T2V` · `I2V` · `I2V+last` · **`triple`** (`image` + `last_frame_image` + `audio` — omit `duration`)

## Workflow (after intake)

### Phase 0 — Stills (parallel when independent)

1. **Hero anchor** — one approved `p-image` or upload.
2. **`p-image-edit`** per scene — **start still** (`edit_prompt`) from hero; **end still** (`last_frame_edit_prompt`) from start still. Parallel after hero exists.
3. **Frame chain (selective):** set `chain_from_previous: true` only when scene *i* continues directly from *i−1*. Use composed start still + hard cut for new beats.

### Phase 1 — Audio (parallel)

[Gemini TTS](../../../tools/audio/gemini-3.1-flash-tts/SKILL.md) per scene → upload each to `/v1/files`.

### Phase 2 — Video (parallel when all anchors ready)

**Scene anchor triple** — one `p-video` job per row:

```json
{
  "prompt": "...",
  "image": "START_URL",
  "last_frame_image": "END_URL",
  "audio": "NARRATION_URL",
  "resolution": "720p",
  "fps": 24,
  "save_audio": true
}
```

Omit `duration`. Poll all `get_url` until done; retry failed scenes only.

### Phase 3 — Review

Adjust prompt, stills, or narration; re-run **that scene only**.

### Phase 4 — Assembly

1. **Concat** clips in scene order (narration already embedded).
2. **Optional bed** — [stable-audio-2.5](../../../tools/audio/stable-audio-2.5/SKILL.md) under VO ([`launch_background_music.py`](../_shared/scripts/launch_background_music.py)).

### Phase 5 — Manifest

Scene table + all six URLs per scene (start, end, audio in/out) + prediction ids.

## Frame-chain + narration example (dog story)

```text
Scene 1: composed start,  last=play_end,   audio=vo_1   chain→2
Scene 2: extract(clip_1), last=loss_end,   audio=vo_2   hard cut→3
Scene 3: composed start,  last=search_end, audio=vo_3   chain→4
Scene 4: extract(clip_3), last=tree_end,   audio=vo_4   chain→5
Scene 5: extract(clip_4), last=reunion,   audio=vo_5
```

See [scene-anchor-triple.md](../../../references/scene-anchor-triple.md) for when to chain vs hard cut, and OPEN/MID/CLOSE prompt structure.

## Related

- Single clip: [single-scene-ai-video](../single-scene-ai-video/SKILL.md)
- Talking avatars: [multi-scene-avatar-video](../multi-scene-avatar-video/SKILL.md)
- Audio layering: [audio-post-production.md](../../../references/audio-post-production.md)
- Parallel vs phased: [parallel-execution.md](../../../references/parallel-execution.md)
- Generic chain: [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md)
