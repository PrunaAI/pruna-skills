# Replicate API (minimal)

Used by external tool skills (e.g. `stable-audio-2.5`, `gemini-3.1-flash-tts`).

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

Shared client: `music-video` · tool skill: `music-2.5`

## Gemini 3.1 Flash TTS

Model: `google/gemini-3.1-flash-tts`  
Required input: `text`  
Optional: `voice` (default `Kore`), `prompt` (style/scene), `language_code` (default `en-US`)

Output: audio file URL. Use for narration — upload to Pruna as part of scene anchor triple (`video-prompting`) (`input.audio` + `input.image` + `input.last_frame_image` on `p-video`). Layering with beds: `audio-prompting`
