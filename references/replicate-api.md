# Replicate API (minimal)

Used by external tool skills (e.g. [stable-audio-2.5](../tools/audio/stable-audio-2.5/SKILL.md), [gemini-3.1-flash-tts](../tools/audio/gemini-3.1-flash-tts/SKILL.md)).

## Auth

```bash
export REPLICATE_API_TOKEN=r8_...
```

Header: `Authorization: Bearer ${REPLICATE_API_TOKEN}`

## Create + poll

```bash
# POST https://api.replicate.com/v1/models/{owner}/{name}/predictions
# Body: {"input": { ... }}

# Poll GET on response.urls.get until status == succeeded
# Download output URL (string or list depending on model)
```

Shared client: [`guides/workflows/_shared/scripts/replicate_api.py`](../guides/workflows/_shared/scripts/replicate_api.py)

## Stable Audio 2.5

Model: `stability-ai/stable-audio-2.5`  
Required input: `prompt`  
Optional: `duration` (1–190), `steps` (4–8), `cfg_scale`, `seed`

## Music 2.5 (MiniMax)

Model: `minimax/music-2.5`  
Required input: `lyrics` (1–3,500 chars, structure tags supported)  
Optional: `prompt` (style), `sample_rate`, `bitrate`, `audio_format` (`mp3` default)

Workflow: [ai-music-video](../guides/workflows/ai-music-video/SKILL.md) · tool skill: [music-2.5](../tools/audio/music-2.5/SKILL.md)

## Gemini 3.1 Flash TTS

Model: `google/gemini-3.1-flash-tts`  
Required input: `text`  
Optional: `voice` (default `Kore`), `prompt` (style/scene), `language_code` (default `en-US`)

Output: audio file URL. Use for narration — upload to Pruna as part of [scene anchor triple](./scene-anchor-triple.md) (`input.audio` + `input.image` + `input.last_frame_image` on `p-video`). Layering with beds: [audio-post-production.md](./audio-post-production.md)
