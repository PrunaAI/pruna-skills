# Agent safety (data, credentials, locale)

Required before the first paid generation call (`POST /v1/predictions`, Replicate prediction, or file upload to Pruna/Replicate). Link from tool and workflow skills that transmit media.

## Privacy / external transmission

Local images, audio, scripts, and portraits are **uploaded to remote APIs** (primarily `https://api.pruna.ai/`; Replicate for TTS/song/bed/WhisperX). Uploads may include biometric-like portraits, personal voice, or copyrighted material.

- Get **explicit user acknowledgment** before the first upload or prediction in a session (or when new media is introduced).
- Do **not** use third-party likenesses or voices without the user’s confirmation that they have consent.
- Tell the user that content leaves the local environment and is processed/stored remotely per the provider’s terms.

## Credentials

- Read `PRUNA_API_KEY` / `REPLICATE_API_TOKEN` from the **host environment** only (shell / `.env` — never commit).
- **Never** embed keys in prompts, chat, manifests, plan JSON, logs, or subagent task text.
- Prefer the **parent agent** to own API calls. Do not fan credentials across parallel subagents unless the host documents isolated secret injection.
- If a key is missing, stop and use the templates in [api-credentials.md](./api-credentials.md).

## Local disk

Downloads (`curl -o …`, runners writing under an output dir) **create or overwrite** local files. Confirm the output path with the user before writing; avoid clobbering unrelated paths.

## Locale and voice

- Confirm **`voice_language`** (and voice preset) with the user before avatar/TTS jobs.
- Examples that use `English (US)` are **illustrative only** — not a silent default override of user locale.

## Related

- [api-credentials.md](./api-credentials.md) — signup + header rules
- [pruna-api.md](./pruna-api.md) — upload / poll / download
- [staged-generation-gate.md](../policies/staged-generation-gate.md) — approval phases
