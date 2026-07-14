# Illustrated story reel — API reference (scoped)

APIs used by **illustrated-story-reel** only. This skill does **not** use `p-video*` models.

Credentials: [api-credentials.md](../shared/api-credentials.md)

## Pruna P-API (stills)

- Base: `https://api.pruna.ai/v1/predictions`
- Upload: `https://api.pruna.ai/v1/files`
- Header: `apikey: ${PRUNA_API_KEY}`, `Model: p-image` or `Model: p-image-edit`
- Body: `{ "input": { ... } }`
- Sync (`Try-Sync: true`) is acceptable for hero and beat stills; async + poll if jobs time out.

**Models in this workflow:**

| Model | Use |
|-------|-----|
| `p-image` | Hero anchor still |
| `p-image-edit` | Per-beat still from hero or chained prior plate |

Shared client: `scripts/pruna_api.py`

## Replicate (audio)

- Header: `Authorization: Bearer ${REPLICATE_API_TOKEN}`
- Create: `POST https://api.replicate.com/v1/models/{owner}/{name}/predictions`
- Poll `urls.get` until `succeeded`; download output URL.

**Models in this workflow:**

| Model | Use |
|-------|-----|
| `google/gemini-3.1-flash-tts` | Per-beat narration (`audio_mode: narration`) |
| `stability-ai/stable-audio-2.5` | Instrumental bed (`audio_mode: music`, no user track) |

Shared client: `scripts/replicate_api.py`

## Local assembly (ffmpeg)

Requires **`ffmpeg`** and **`ffprobe`** on PATH. The runner invokes ffmpeg with **`-y`** (overwrite output without prompt). Confirm `--out-dir` and `--output-name` before assembly.

Script: `scripts/assemble_slideshow.py` (Ken Burns segments, crossfade, audio mux).
