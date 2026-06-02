# Audio post-production (Pruna + Replicate)

How to choose and **layer** audio when building reels, multi-scene films, and launch videos.

**Multi-scene narrated films:** use the [scene anchor triple](./scene-anchor-triple.md) — pass TTS to **`p-video`** as `input.audio` with `image` + `last_frame_image`; do not post-mux unless re-render is impossible.

## Audio-led `p-video` (required when VO/narration exists)

When narration, TTS, or a timed audio slice is available **before** video render:

1. Upload the audio file to Pruna (`POST /v1/files`).
2. Pass `urls.get` as **`input.audio`** on **`p-video`** (or **`p-video-avatar`** for human lip-sync).
3. **Omit `duration`** — clip length follows the audio; the model syncs motion to speech.
4. Set **`save_audio`: true** so the full line is embedded in the output clip.
5. **Concat** clips in order (narration already on each clip). Optional bed mixed **under** VO in post.

**Never** generate silent `p-video` and ffmpeg-mux narration afterward unless re-render is impossible — post-mux **truncates** lines longer than the video slot (common with Gemini TTS).

Helper: [`p_video_payload.py`](../guides/workflows/_shared/scripts/p_video_payload.py) — `build_p_video_payload(...)` enforces omitting `duration` when `audio_url` is set.

| Workflow | Audio source | `p-video` fields |
|----------|--------------|------------------|
| Dog plush / story film | Gemini TTS per scene | `image` + `last_frame_image` + `audio` |
| Music video performance | Song slice per cut | `image` + `audio` |
| Music video B-roll | Song slice (optional) | `image` + `audio` or `duration` only |
| Viking narrator beats | Gemini TTS | `image` + `last_frame_image` + `audio` |

## Tool picker

| Need | Tool | Skill |
|------|------|-------|
| Cinematic clip with model-generated sound | `p-video` (`save_audio`, optional uploaded `audio`) | [p-video](../tools/video/p-video/SKILL.md) |
| Lip-sync / duration locked to VO | Upload audio → `p-video` with `audio` | [p-video](../tools/video/p-video/SKILL.md) |
| Documentary / story narrator | [Gemini 3.1 Flash TTS](https://replicate.com/google/gemini-3.1-flash-tts) | [gemini-3.1-flash-tts](../tools/audio/gemini-3.1-flash-tts/SKILL.md) |
| Light instrumental under dialogue | [Stable Audio 2.5](https://replicate.com/stability-ai/stable-audio-2.5) | [stable-audio-2.5](../tools/audio/stable-audio-2.5/SKILL.md) |
| Full song with sung vocals | [Music 2.5](https://replicate.com/minimax/music-2.5) | [music-2.5](../tools/audio/music-2.5/SKILL.md) |
| Speaking on-camera character | `p-video-avatar` | [p-video-avatar](../tools/video/p-video-avatar/SKILL.md) |

**Env:** Pruna calls need `PRUNA_API_KEY`; Replicate audio tools need `REPLICATE_API_TOKEN`. Assembly steps need **`ffmpeg`** / **`ffprobe`**.

## Layering matrix

| Stack | Primary audio | Secondary | Mix notes |
|-------|---------------|-----------|-----------|
| **Silent B-roll** | — | — | Concat video only |
| **Native `p-video` sound** | Model output | — | Keep `save_audio` default; normalize in assembly if scenes differ |
| **Narration only (fallback)** | Gemini TTS | — | Post-mux only when audio-led `p-video` is not suitable — prefer **Pipeline B** below |
| **Bed only** | Stable Audio bed | — | [`launch_background_music.py`](../guides/workflows/_shared/scripts/launch_background_music.py) |
| **Narration + bed (preferred)** | Gemini TTS → **`p-video` `audio`** | Stable Audio (quiet) | TTS uploaded to Pruna drives clip length + sync; bed mixed in post under narration (~0.08–0.15) |
| **Avatar VO + bed** | `p-video-avatar` dialogue | Stable Audio bed | Same bed pattern as replace/launch reels — bed **under** existing speech |
| **Music video** | Music 2.5 full song | — | [ai-music-video](../guides/workflows/ai-music-video/SKILL.md) |

## Recommended pipelines

### A — Narrated multi-scene B-roll (**preferred — scene anchor triple**)

```text
Phase 0 — intake: scene table with start/end still prompts + narration lines
Phase 1 — hero + p-image-edit start stills + end stills (parallel)
Phase 2 — Gemini TTS per scene (parallel) → upload each to /v1/files
Phase 3 — p-video per scene: input.image + input.last_frame_image + input.audio (parallel; omit duration)
Phase 4 — ffmpeg concat (VO embedded; frame chain via shared end/start URLs)
Phase 5 — optional Stable Audio bed under narration
```

**Scene anchor triple:** same pattern as first/last frame pairing — `audio` is the third required upload per scene row. **`p-video-avatar`:** portrait + optional `last_frame_image` + uploaded `audio`.

### A′ — Post-mux narration (fallback only)

Use only when you already have silent clips and cannot re-render. Risk: TTS longer than clip slots → cut-off VO.

```text
Phase 3 — p-video I2V without audio → concat → mux TTS in ffmpeg
```

### C — Launch / product reel (existing pattern)

```text
Phase 1 — p-video-avatar or replace reel → concat
Phase 2 — Stable Audio bed via launch_background_music.py (bed under VO, not replacing it)
```

## ffmpeg mixing (conceptual)

**Narration onto silent concat** (single VO file):

```bash
ffmpeg -y -i concat_video.mp4 -i narration.mp3 \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest output_with_vo.mp4
```

**Bed under existing narration + video** (same pattern as `launch_background_music.py`):

```text
[1:a]volume=0.12,aloop=...[bed];
[0:a][bed]amix=inputs=2:duration=first[aout]
```

Narration / avatar dialogue stays on stream `0:a`; bed is stream `1:a` at low volume.

## Intake questions (audio)

Ask before generating paid audio or video:

| Topic | Questions |
|-------|-----------|
| **Primary voice** | Narrator (Gemini TTS), on-screen avatar (`p-video-avatar`), or native `p-video` sound only? |
| **Narration scope** | Per-scene lines vs one continuous VO track? |
| **Music / bed** | None, instrumental bed only, or full song ([music-2.5](../tools/audio/music-2.5/SKILL.md))? |
| **Sync strategy** | **Preferred:** TTS → Pruna upload → **`p-video` / `p-video-avatar` with `audio`** (clip length = audio). Post-mux only as fallback. |
| **Levels** | Bed volume target (default ~0.12 under avatar VO; ~0.08–0.12 under Gemini narration)? |

## Manifest fields

```json
{
  "narration": { "enabled": true, "voice": "Sulafat", "mode": "per_scene" },
  "background_music": { "enabled": true, "volume": 0.10, "prompt": "Instrumental ... no vocals" },
  "p_video_audio": { "save_audio": true }
}
```

## Limitations (from [P-Video on Replicate](https://replicate.com/prunaai/p-video))

- Native SFX/dialogue quality varies — for premium voice realism, prefer **Gemini TTS** or **`p-video-avatar`**, then optionally mix a bed.
- Multi-speaker native audio can drift; dedicated TTS per role is safer for narration-heavy cuts.
- Extreme camera motion and complex multi-scene stories are weaker than **frame-anchored chaining** + per-scene prompts — see [p-video](../tools/video/p-video/SKILL.md) **First / last frame chaining**.

## Related

- [parallel-execution.md](./parallel-execution.md) — phased vs parallel when frames chain
- [multi-scene-ai-video](../guides/workflows/multi-scene-ai-video/SKILL.md)
- [pruna-generative-pipeline](../guides/workflows/pruna-generative-pipeline/SKILL.md)
