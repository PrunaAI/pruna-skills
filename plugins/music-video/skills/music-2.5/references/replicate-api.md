# Replicate API (minimal)

Used by external tool skills (e.g. [stable-audio-2.5](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/stable-audio-2.5/skills/stable-audio-2.5/SKILL.md), [gemini-3.1-flash-tts](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/gemini-3.1-flash-tts/skills/gemini-3.1-flash-tts/SKILL.md)).

**Missing token:** agents must stop and point the user to [api-credentials.md](./api-credentials.md) — sign up at [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens) ([sign in](https://replicate.com/signin) if needed), then `export REPLICATE_API_TOKEN=r8_...`.

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

Shared client: [`workflows/_shared/scripts/replicate_api.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/replicate_api.py)

## Stable Audio 2.5

Model: `stability-ai/stable-audio-2.5`  
Required input: `prompt`  
Optional: `duration` (1–190), `steps` (4–8), `cfg_scale`, `seed`

## Music 2.5 (MiniMax)

Model: `minimax/music-2.5`  
Required input: `lyrics` (1–3,500 chars, structure tags supported)  
Optional: `prompt` (style), `sample_rate`, `bitrate`, `audio_format` (`mp3` default)

Workflow: [music-video](../../music-video/SKILL.md) · tool skill: [music-2.5](../SKILL.md)

## Gemini 3.1 Flash TTS

Model: `google/gemini-3.1-flash-tts`  
Required input: `text`  
Optional: `voice` (default `Kore`), `prompt` (style/scene), `language_code` (default `en-US`)

Output: audio file URL. Use for narration — upload to Pruna as part of [scene anchor triple](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/scene-anchor-triple/SKILL.md) (`input.audio` + `input.image` + `input.last_frame_image` on `p-video`). Layering with beds: [audio-post-production.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/audio-post-production/SKILL.md)

## p-image-ideogram (Pruna deployment)

Deployment: `prunaai/p-image-ideogram-preview`  
Endpoint: `POST https://api.replicate.com/v1/deployments/prunaai/p-image-ideogram-preview/predictions`  
Required input: `prompt`  
Optional: `mode` (`very low` · `low` · `medium` default · `high` · `very high`), `aspect_ratio`, `image_size`, `width`, `height` (when `aspect_ratio=custom`), `seed`, `output_format`, `output_quality`

Use for high-quality fast photoreal stills. Fastest drafts: [p-image](../../p-image/SKILL.md) (Pruna P-API). Tool skill: [p-image-ideogram](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/p-image-ideogram/skills/p-image-ideogram/SKILL.md)
