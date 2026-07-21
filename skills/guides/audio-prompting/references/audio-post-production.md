# Audio post-production (Pruna + Replicate)

How to choose and **layer** audio when building reels, multi-scene films, and launch videos.

**Prompt craft (how to write):** [tts-style-prompting.md](./tts-style-prompting.md) · [music-and-bed-prompting.md](./music-and-bed-prompting.md). For in-video audio modes and talking-head VO, install and follow `video-prompting`.

**Multi-scene narrated films:** scene anchor triple lives in `video-prompting` — pass TTS to **`p-video`** as `input.audio` with `image` + `last_frame_image`; do not post-mux unless re-render is impossible. Workflow: `narrated-multi-scene`.

**Visual-only transitions (no VO):** scene anchor pair in `video-prompting` — `duration` instead of `audio`. Workflow: `visual-transition-reel`.

## Audio-led `p-video` (required when VO/narration exists)

When narration, TTS, or a timed audio slice is available **before** video render:

1. Upload the audio file to Pruna (`POST /v1/files`) — see `pruna-api`.
2. Pass `urls.get` as **`input.audio`** on **`p-video`** (or **`p-video-avatar`** for human lip-sync).
3. **Omit `duration`** — clip length follows the audio (capped at **20s** on P-API); the model syncs motion to speech.
4. Set **`save_audio`: true** so the full line is embedded in the output clip.
5. **Probe TTS length** before render — per-scene lines should be **≤ ~19s** or the API truncates the tail even when `audio` is set.
6. **Concat** clips in order (narration already on each clip). Optional bed mixed **under** VO in post.

**Never** generate silent `p-video` and ffmpeg-mux narration afterward unless re-render is impossible — post-mux **truncates** lines longer than the video slot (common with Gemini TTS).

**Over 20s?** Shorten scene copy → tighten TTS pace in `style_prompt` → split into two scene rows (each with its own triple). See `narrated-multi-scene` duration gate.

| Need | Approach | Skill |
|------|----------|-------|
| Lip-sync / duration locked to VO | Upload audio → `p-video` with `audio` | `p-video` |
| Documentary / story narrator | Gemini Flash TTS → upload → video | `gemini-3.1-flash-tts` |
| Light instrumental under dialogue | Stable Audio bed under VO | `stable-audio-2.5` |
| Full song with sung vocals | Music 2.5 track | `music-2.5` |
| Speaking on-camera character | Portrait + script / audio | `p-video-avatar` |

**Env:** Pruna calls need `PRUNA_API_KEY`; Replicate audio tools need `REPLICATE_API_TOKEN`. Assembly steps need **`ffmpeg`** / **`ffprobe`**. Credentials: `pruna-api`.

## Layering matrix

| Stack | Primary audio | Secondary | Mix notes |
|-------|---------------|-----------|-----------|
| **Silent B-roll** | — | — | Concat video only |
| **Native `p-video` sound** | Model output | — | Keep `save_audio` default; normalize in assembly if scenes differ |
| **Narration only (fallback)** | Gemini TTS | — | Post-mux only when audio-led `p-video` is not suitable — prefer **Pipeline A** below |
| **Bed only** | Stable Audio bed | — | Often with `music-video` or reel beds |

## Recommended pipelines

### A — Narrated multi-scene B-roll (**preferred — scene anchor triple**)

Use `narrated-multi-scene` + `video-prompting` (triple) + tools below.

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
Phase 2 — Stable Audio bed via stable-audio-2.5 + ffmpeg bed mix (bed under VO, not replacing it)
```

## ffmpeg mixing (conceptual)

**Narration onto silent concat** (single VO file):

```bash
ffmpeg -y -i concat_video.mp4 -i narration.mp3 \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest output_with_vo.mp4
```

**Bed under existing narration + video** (same pattern as `stable-audio-2.5` + ffmpeg bed mix):

```text
[1:a]volume=0.12,aloop=...[bed];
[0:a][bed]amix=inputs=2:duration=first[aout]
```

Narration / avatar dialogue stays on stream `0:a`; bed is stream `1:a` at low volume.

**Bed on silent concat** — loop a short generated clip to full video length (no per-assemble Stable Audio call):

```text
[1:a]volume=0.12,aloop=loop=-1:size=2e+09[bed]  →  map video + [bed], -shortest
```

Plan field `"reuse_bed": true` skips regeneration when `audio/launch_bed.mp3` exists. Delete that file (or set `reuse_bed: false`) only when you want a new prompt or seed.

## Intake questions (audio)

Ask before generating paid audio or video:

| Topic | Questions |
|-------|-----------|
| **Primary voice** | Narrator (`gemini-3.1-flash-tts`), on-screen avatar (`p-video-avatar`), or native `p-video` sound only? |
| **Narration scope** | Per-scene lines vs one continuous VO track? |
| **Music / bed** | None, instrumental bed only (`stable-audio-2.5`), or full song (`music-2.5`)? |
| **Sync strategy** | **Preferred:** TTS → Pruna upload → **`p-video` / `p-video-avatar` with `audio`** (clip length = audio). Post-mux only as fallback. |
| **Levels** | Bed volume target (default ~0.12 under avatar VO; ~0.08–0.12 under Gemini narration)? |

## Manifest fields

```json
{
  "narration": { "enabled": true, "voice": "Sulafat", "mode": "per_scene" },
  "background_music": { "enabled": true, "reuse_bed": true, "volume": 0.10, "prompt": "Instrumental ... no vocals" },
  "p_video_audio": { "save_audio": true }
}
```

## Limitations (P-Video audio)

- Native SFX/dialogue quality varies — for premium voice realism, prefer **`gemini-3.1-flash-tts`** or **`p-video-avatar`**, then optionally mix a bed.
- Multi-speaker native audio can drift; dedicated TTS per role is safer for narration-heavy cuts.
- Extreme camera motion and complex multi-scene stories are weaker than **frame-anchored chaining** + per-scene prompts — see `p-video` and `video-prompting`.

## Related skills

| Skill | When |
|-------|------|
| `video-prompting` | In-video audio modes, scene anchor pair/triple, talking-head VO craft |
| `pruna-api` | Upload / poll / parallel batches |
| `narrated-multi-scene` | Multi-scene B-roll + VO playbook |
| `visual-transition-reel` | Visual-only transitions (no VO) |
| `music-video` | Full song + lyric-synced video |
| `p-video` / `p-video-avatar` | Video API calls that consume uploaded audio |
| `gemini-3.1-flash-tts` / `stable-audio-2.5` / `music-2.5` | Paid audio generation |
