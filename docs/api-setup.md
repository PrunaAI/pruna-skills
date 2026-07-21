# API setup

Skills that call paid APIs need credentials before generation.

## Environment variables

| Service | Variable | Get a key |
|---------|----------|-----------|
| **Pruna** (images, video, try-on, upscale) | `PRUNA_API_KEY` | [dashboard.pruna.ai](https://dashboard.pruna.ai/) |
| **Replicate** (Music 2.5, TTS, Stable Audio, WhisperX) | `REPLICATE_API_TOKEN` | [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens) |

```bash
export PRUNA_API_KEY="your_pruna_key"
export REPLICATE_API_TOKEN="r8_..."   # when using audio / song tools
```

## HTTP details

- Pruna uses the **`apikey`** header — see [skills/guides/pruna-api/references/pruna-api.md](../skills/guides/pruna-api/references/pruna-api.md)
- Replicate uses **`Authorization: Bearer`** — see [skills/guides/pruna-api/references/replicate-api.md](../skills/guides/pruna-api/references/replicate-api.md)

## Agent rule

If a required key is missing, do not call paid APIs. Use signup templates in [skills/guides/pruna-api/references/api-credentials.md](../skills/guides/pruna-api/references/api-credentials.md).

Guide skills (`guides/`) do not require API keys unless you combine them with a tool or workflow skill.
