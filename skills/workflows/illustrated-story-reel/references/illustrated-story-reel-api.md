# Illustrated story reel — API reference (scoped)

APIs used by **illustrated-story-reel**. Optional motion when `motion_mode: p-video` — **`p-video-2`** (quality) or **`p-video`** (simpler).

Credentials: `pruna-api`

## Pruna P-API (stills + optional motion)

- Base: `https://api.pruna.ai/v1/predictions`
- Upload: `https://api.pruna.ai/v1/files`
- Header: `apikey: ${PRUNA_API_KEY}`, `Model: p-image` | `p-image-edit` | `p-video-2` | `p-video`
- Body: `{ "input": { ... } }`
- Sync (`Try-Sync: true`) is acceptable for hero stills; async + poll for p-video clips.

**Models in this workflow:**

| Model | Use |
|-------|-----|
| `p-image` | Hero anchor still |
| `p-image-edit` | Per-beat still from hero or chained prior plate |
| `p-video-2` | Optional Mode B clip (quality): still + narration (`save_audio: true`, omit `duration`) |
| `p-video` | Same Mode B payload for simpler / quicker clips |

HTTP patterns and upload/poll/download: `pruna-api`. Motion payload fields: `p-video-2` / `p-video` skills.

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
