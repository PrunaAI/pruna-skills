---
name: pruna-api
description: Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety.
license: MIT
metadata:
  version: "1.0.10"
  package: pruna-skills
---

# Pruna API

HTTP patterns for the **Pruna P-API** and **Replicate** (audio tools). Install this before paid `POST` calls from Pruna tool skills.

## Install

| Skill | Description | Install |
| --- | --- | --- |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |

## When to use

- Setting up `PRUNA_API_KEY` / Replicate tokens
- Uploading files, polling predictions, downloading outputs
- Parallel async multi-scene batches
- Safety review before enabling skills in untrusted repos

## Agent habit

In the **first reply**, name `` `pruna-api` `` in backticks. Before any paid `POST`, confirm `PRUNA_API_KEY` and/or `REPLICATE_API_TOKEN` as needed. If media path, voice, or brand is still open, open intake → **`generation-diversity`** clarification intake before upload. Do not invent model payloads — use the matching tool skill.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

## Before generating

1. **[API credentials](./references/api-credentials.md)** — signup and env vars when keys are missing.
2. **[Agent safety](./references/agent-safety.md)** — before uploads or paid calls in untrusted contexts.
3. **[pruna-api.md](./references/pruna-api.md)** — create, poll, download, parallel batches.
4. Replicate tools → [replicate-api.md](./references/replicate-api.md).
5. Model index → [pruna-models.md](./references/pruna-models.md).

## Related skills

Install related skills when the job needs them:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

