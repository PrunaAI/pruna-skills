# Scene anchor triple (single narrated beat → multi-scene extension)

Canonical payload pattern for **one narrated `p-video` prediction**: three uploaded anchors (`image`, `last_frame_image`, `audio`) plus a motion **`prompt`**. Use this for a **single story beat** first (`image-to-video`, `p-video`).

**Multi-scene extension** (`frame_chain`, concat, parallel batches, plan JSON with many rows) belongs only in `narrated-multi-scene` — do not treat this doc as permission for single-clip skills to orchestrate full films.

Related: [scene-anchor-pair.md](./scene-anchor-pair.md) (visual-only) · `audio-prompting` · [audio-in-video-prompting.md](./audio-in-video-prompting.md) · [prompt-dramaturgy.md](./prompt-dramaturgy.md) · [clip-chaining.md](./clip-chaining.md) · `p-video`

## The triple (one prediction)

Each beat supplies **three Pruna file URLs** (from `POST /v1/files`) plus a motion **`prompt`**:

| Anchor | `input` field | Role |
|--------|---------------|------|
| **First frame** | `image` | Opening composition |
| **Last frame** | `last_frame_image` | Closing composition |
| **Narration / VO / music slice** | `audio` | Sets **clip duration** (min(audio length, **20s** P-API max)); model syncs motion to speech or beats |

**Omit `duration`** when `audio` is set. Optional **`save_audio`: true** keeps narration on the output clip.

When audio is provided, **always** upload and pass it to `p-video` at render time. Do not generate silent clips and mux narration in ffmpeg afterward.

**20-second ceiling:** audio-led clips cannot run longer than P-API `duration` max (**20s**). Write TTS to **≤ ~19s** (probe with `ffprobe` after Gemini). Truncated VO with “audio passed” usually means the line was too long, not that `input.audio` was missing. See `gemini-3.1-flash-tts` (or `music-2.5` slice for music videos)
2. Download MP3/WAV
3. Upload to `/v1/files` → use `urls.get` as `input.audio`

**Do not** post-mux narration over silent `p-video` clips unless re-render is impossible — truncated VO is a common failure mode.

## Video phase (one beat)

When start URL, end URL, and audio URL exist:

- **`POST /v1/predictions`** with `Model: p-video` — one async job
- Poll `get_url` until done

## Multi-scene extension (narrated-multi-scene only)

The sections below apply when the user explicitly requested a **multi-scene film**. Single-clip skills must stop and hand off to `narrated-multi-scene` instead of executing them.

**Explainer interaction (preferred):** alternate **narrator** triple beats with **character** `p-video-avatar` dialogue — see `interactive-explainer` and `interactive-explainer`.

**Explainer motion & format:** dynamic `OPEN:` / `MID:` / `CLOSE:` `video_prompt` per scene; default **`720p`** + **`24` fps** — see `interactive-explainer`.

**Visual style for explainers:** keep a single `style_bible` on every `p-image` / `p-image-edit` / `p-video` prompt.

### Parallel stills / video across scenes

Run start stills **in parallel** from hero; then end stills **in parallel** from each start still. After **all** URLs exist for every scene row, `POST /v1/predictions` in a **parallel** batch. Patterns: pruna-api.md#parallel-async-multi-scene--batch (`generation-diversity`).

### Frame chain

Full decision tree: **[clip-chaining.md](./clip-chaining.md)**. Chain only when motion continues — same location, same moment, no time jump. Use a **composed start still** (hard cut) for new story beats.

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

### Scene + narration flow

Each scene row should read as one complete beat:

1. **OPEN** — `edit_prompt` / first frame matches the **opening words** of narration
2. **MID** — `video_prompt` motion develops the line
3. **CLOSE** — `last_frame_edit_prompt` holds a **clear ending pose** before the cut

Write narration to describe what is on screen at open → close. Avoid lines that reference action that hasn't happened yet or already finished.

Use `stable-audio-2.5` mixed **under** narration via `stable-audio-2.5` + ffmpeg bed mix (~0.08–0.15 volume)

### Plan JSON shape

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

Upgrade a **pair** to a **triple** by adding TTS → upload → `input.audio` and omitting `duration`. Visual-only transitions: [scene-anchor-pair.md](./scene-anchor-pair.md).

## Variants on other models

| Model | Triple analogue |
|-------|-----------------|
| **`p-video-avatar`** | `image` (portrait) + optional `last_frame_image` + **`audio`** (uploaded TTS) *or* native `voice_script` |
| **`p-video` (music video B-roll)** | `image` + **`audio`** (song slice) — `last_frame_image` optional per beat |
| **`p-video-animate`** | `image` + **`video`** (motion template) — different axis; not narration triple — use the `p-video-animate` skill |

## Workflows that implement this

- `image-to-video` — **one beat** (this skill’s default)
- `narrated-multi-scene` — primary narrated multi-scene workflow
- `visual-transition-reel` — visual pair (no VO)
- WORKFLOW-RECIPES — Recipe **P**

## Intake checklist (per beat)

- [ ] `edit_prompt` (OPENING still — matches narration open)
- [ ] `last_frame_edit_prompt` (CLOSING still — clear end pose)
- [ ] Narration line → TTS → upload URL (open/mid/close aligns with visuals)
- [ ] `video_prompt` (OPEN / MID / CLOSE motion — not duplicate narration prose)
- [ ] `resolution` / `fps` / `draft` policy
- [ ] Multi-scene only: `chain_from_previous` — only if motion truly continues from prior clip
