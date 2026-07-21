# Illustrated story reel — API reference (scoped)

APIs used by **illustrated-story-reel**. Optional **`p-video`** when `motion_mode: p-video`.

Credentials: [api-credentials.md](../../../guides/pruna-api/references/api-credentials.md)

## Pruna P-API (stills + optional motion)

- Base: `https://api.pruna.ai/v1/predictions`
- Upload: `https://api.pruna.ai/v1/files`
- Header: `apikey: ${PRUNA_API_KEY}`, `Model: p-image` | `p-image-edit` | `p-video`
- Body: `{ "input": { ... } }`
- Sync (`Try-Sync: true`) is acceptable for hero stills; async + poll for p-video clips.

**Models in this workflow:**

| Model | Use |
|-------|-----|
| `p-image` | Hero anchor still |
| `p-image-edit` | Per-beat still from hero or chained prior plate |
| `p-video` | Optional Mode B clip: still + narration (`save_audio: true`, omit `duration`) |

Shared clients: `scripts/pruna_api.py`, p-video skill payload fields, `scripts/story_video_clips.py`

## Replicate (audio)

- Header: `Authorization: Bearer ${REPLICATE_API_TOKEN}`
- Create: `POST https://api.replicate.com/v1/models/{owner}/{name}/predictions`
- Poll `urls.get` until `succeeded`; download output URL.

**Models in this workflow:**

| Model | Use |
|-------|-----|
| `google/gemini-3.1-flash-tts` | Per-beat narration (`audio_mode: narration`) |
| `stability-ai/stable-audio-2.5` | Instrumental bed (`audio_mode: music`, no user track) |

Shared client: pruna-api / Replicate HTTP in tool skill

## Local assembly (ffmpeg)

Requires **`ffmpeg`** and **`ffprobe`** on PATH. The agent runs ffmpeg with **`-y`** (overwrite output without prompt). Confirm out dir and output name before assembly.

- **Ken Burns:** segments + narration/bed mux — `illustrated-story-reel` **Motion + assemble**
- **p-video:** concat `clips/*.mp4` (audio embedded) — [illustrated-story-reel-p-video-motion.md](./illustrated-story-reel-p-video-motion.md)
