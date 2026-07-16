# API credentials (Pruna + Replicate)

**Agent rule:** Before any `POST /v1/predictions`, Replicate prediction, or paid runner — check env vars. If a required key is **missing or empty**, **stop** and tell the user how to sign up. Do not guess, mock, or skip with placeholder keys.

## Pruna P-API

| | |
|--|--|
| **Env var** | `PRUNA_API_KEY` |
| **Header** | `apikey: ${PRUNA_API_KEY}` (not `Authorization: Bearer`) |
| **Sign up / get key** | [Pruna dashboard](https://dashboard.pruna.ai/) |
| **Docs** | [Quickstart](https://docs.api.pruna.ai/guides/quickstart) · [pruna-api.md](./pruna-api.md) |

**Used by:** all `p-image*`, `p-video*` tool skills and Pruna workflow runners.

### If `PRUNA_API_KEY` is missing — agent message template

> Pruna generation needs an API key. Sign up or sign in at **[dashboard.pruna.ai](https://dashboard.pruna.ai/)**, create an API key, then set:
>
> ```bash
> export PRUNA_API_KEY="your_key_here"
> ```
>
> Add that to your shell profile or project `.env` (never commit the key). Reply when it’s set and we can continue.

## Replicate

| | |
|--|--|
| **Env var** | `REPLICATE_API_TOKEN` |
| **Header** | `Authorization: Bearer ${REPLICATE_API_TOKEN}` |
| **Sign up / get token** | [Replicate API tokens](https://replicate.com/account/api-tokens) ([sign in](https://replicate.com/signin) first if needed) |
| **Docs** | [replicate-api.md](./replicate-api.md) |

**Used by:** `music-2.5`, `gemini-3.1-flash-tts`, `stable-audio-2.5`, `whisperx`, and workflow beds/TTS/song phases.

### If `REPLICATE_API_TOKEN` is missing — agent message template

> This step uses Replicate (song, TTS, transcription, or background bed). Create a token at **[replicate.com/account/api-tokens](https://replicate.com/account/api-tokens)**, then set:
>
> ```bash
> export REPLICATE_API_TOKEN="r8_..."
> ```
>
> Reply when it’s set and we can continue.

## Which key does this job need?

| Task | Keys required |
|------|----------------|
| `p-image`, `p-image-edit`, `p-image-upscale`, `p-image-try-on` | `PRUNA_API_KEY` |
| `p-video`, `p-video-avatar`, `p-video-animate`, `p-video-replace` | `PRUNA_API_KEY` |
| Music 2.5 song generation | `REPLICATE_API_TOKEN` |
| Gemini TTS narration | `REPLICATE_API_TOKEN` |
| Stable Audio background bed | `REPLICATE_API_TOKEN` |
| WhisperX transcription | `REPLICATE_API_TOKEN` |
| Music video / explainer (full pipeline) | **Both** — Pruna for stills/video; Replicate for song/TTS/bed as needed |

When only one key is missing, suggest **only** that provider’s signup link — not both.

## Security

- Never print full keys in chat or commit them to git.
- `.env` is gitignored; prefer env vars over hardcoding in plans or manifests.
- Never embed keys in prompts, manifests, plan JSON, logs, or **subagent task text**.
- Prefer the **parent agent** to own API calls; do not fan credentials across parallel subagents unless the host documents isolated secret injection.
- Full rules: [agent-safety.md](./agent-safety.md).
