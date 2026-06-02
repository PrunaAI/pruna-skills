# Scene anchor triple (multi-scene video)

Canonical pattern for **narrated story films** and **audio-synced B-roll** with Pruna **`p-video`**. Every workflow skill that touches multi-scene cinematic video should link here.

Related: [audio-post-production.md](./audio-post-production.md) · [parallel-execution.md](./parallel-execution.md) · [p-video](../tools/video/p-video/SKILL.md)

## The triple

Each scene row supplies **three Pruna file URLs** (from `POST /v1/files`) plus a motion **`prompt`**:

| Anchor | `input` field | Role |
|--------|---------------|------|
| **First frame** | `image` | Opening composition |
| **Last frame** | `last_frame_image` | Closing composition; becomes next scene's `image` when **`frame_chain`** is on |
| **Narration / VO / music slice** | `audio` | Sets **clip duration**; model syncs motion to speech or beats |

**Omit `duration`** when `audio` is set. Optional **`save_audio`: true** keeps narration on the output clip — **required** for narrated films so concat preserves full lines.

When audio is provided, **always** upload and pass it to `p-video` at render time. Do not generate silent clips and mux narration in ffmpeg afterward.

```json
{
  "prompt": "Dog tosses plush upward, tail wagging, motion matches narrator, warm light",
  "image": "https://api.pruna.ai/v1/files/START_ID",
  "last_frame_image": "https://api.pruna.ai/v1/files/END_ID",
  "audio": "https://api.pruna.ai/v1/files/NARRATION_ID",
  "resolution": "720p",
  "fps": 24,
  "save_audio": true
}
```

## Stills phase (`p-image-edit`)

| Still | Typical source | Plan field |
|-------|----------------|------------|
| Start | Hero + `edit_prompt` | `edit_prompt` |
| End | Start still + `last_frame_edit_prompt` | `last_frame_edit_prompt` |

Run start stills **in parallel** from hero; then end stills **in parallel** from each start still.

## Audio phase (Replicate → Pruna)

1. [Gemini 3.1 Flash TTS](../tools/audio/gemini-3.1-flash-tts/SKILL.md) per scene (or [Music 2.5](../tools/audio/music-2.5/SKILL.md) slice for music videos)
2. Download MP3/WAV
3. Upload each to `/v1/files` → use `urls.get` as `input.audio`

**Do not** post-mux narration over silent `p-video` clips unless re-render is impossible — truncated VO is a common failure mode.

## Video phase

After **all** start URLs, end URLs, and audio URLs exist for every scene row:

- **`POST /v1/predictions`** with `Model: p-video` — **parallel** batch
- Async only; poll all `get_url` until done

## Frame chain (multi-scene)

**Chain only when motion continues** — same location, same moment, no time jump. Use a **composed start still** (hard cut) for new story beats, emotional pauses, or location changes.

| Situation | `chain_from_previous` | Join style |
|-----------|----------------------|------------|
| Continuous action (toss → arc in air) | `true` | Short crossfade (~0.15s) after extract |
| New beat / pause (loss → realization) | `false` | Hard cut — composed OPENING still |
| First scene | `false` | — |

Per-scene flag in plan (overrides legacy global `frame_chain`):

```json
{ "id": "03_realization", "chain_from_previous": false, "edit_prompt": "OPENING SHOT: …" }
```

| `frame_chain_mode` | Next scene `image` when chained | Render order |
|--------------------|---------------------------------|--------------|
| **`extract_last_frame`** | ffmpeg last frame from prior clip | **Sequential** when any scene chains |
| **`planned_stills`** (legacy) | prior scene end still | Parallel |

**Why extract?** Planned end stills often differ from the model's actual last frame → visible jump at cuts.

```text
Scene 1: composed start,  last=end_1,  audio=vo_1   chain→2
Scene 2: extract(clip_1),  last=end_2,  audio=vo_2   hard cut→3
Scene 3: composed start,  last=end_3,  audio=vo_3   chain→4
```

## Scene + narration flow

Each scene row should read as one complete beat:

1. **OPEN** — `edit_prompt` / first frame matches the **opening words** of narration
2. **MID** — `video_prompt` motion develops the line
3. **CLOSE** — `last_frame_edit_prompt` holds a **clear ending pose** before the cut

Write narration to describe what is on screen at open → close. Avoid lines that reference action that hasn't happened yet or already finished.

Use [`concat_clips.py`](../guides/workflows/_shared/scripts/concat_clips.py) with per-join **`crossfades`** — chain joins get ~0.15s fade; hard cuts get 0.

## Assembly

1. **Concat** clips in scene order with optional crossfade (narration already embedded per clip)
2. **Optional bed** — [stable-audio-2.5](../tools/audio/stable-audio-2.5/SKILL.md) mixed **under** narration via [`launch_background_music.py`](../guides/workflows/_shared/scripts/launch_background_music.py) (~0.08–0.15 volume)

## Variants on other models

| Model | Triple analogue |
|-------|-----------------|
| **`p-video-avatar`** | `image` (portrait) + optional `last_frame_image` + **`audio`** (uploaded TTS) *or* native `voice_script` |
| **`p-video` (music video B-roll)** | `image` + **`audio`** (song slice) — `last_frame_image` optional per beat |
| **`p-video-animate`** | `image` + **`video`** (motion template) — different axis; not narration triple |

## Plan JSON shape

```json
{
  "frame_chain_mode": "extract_last_frame",
  "assembly": {
    "chain_crossfade_seconds": 0.15,
    "hard_cut_crossfade_seconds": 0
  },
  "narration": {
    "enabled": true,
    "voice": "Sulafat",
    "mode": "p_video_audio",
    "scene_lines": { "01_beat": "[warmly] …" }
  },
  "scenes": [
    {
      "id": "01_beat",
      "chain_from_previous": false,
      "edit_prompt": "OPENING SHOT: start still from hero…",
      "last_frame_edit_prompt": "CLOSING SHOT: end still from start…",
      "video_prompt": "OPEN: hold. MID: motion. CLOSE: settle on end pose."
    },
    {
      "id": "02_beat",
      "chain_from_previous": true,
      "edit_prompt": "…",
      "last_frame_edit_prompt": "…",
      "video_prompt": "…"
    }
  ]
}
```

## Workflows that implement this

- [multi-scene-ai-video](../guides/workflows/multi-scene-ai-video/SKILL.md) — primary workflow
- [single-scene-ai-video](../guides/workflows/single-scene-ai-video/SKILL.md) — one beat
- [pruna-generative-pipeline](../guides/workflows/pruna-generative-pipeline/SKILL.md) — Recipe **P**
- Example runner: `output/dog-plush-movie/render_audio_led.py`

## Intake checklist (per scene)

- [ ] `edit_prompt` (OPENING still — matches narration open)
- [ ] `last_frame_edit_prompt` (CLOSING still — clear end pose)
- [ ] Narration line → TTS → upload URL (open/mid/close aligns with visuals)
- [ ] `video_prompt` (OPEN / MID / CLOSE motion — not duplicate narration prose)
- [ ] `chain_from_previous` — only if motion truly continues from prior clip
- [ ] `resolution` / `fps` / `draft` policy
