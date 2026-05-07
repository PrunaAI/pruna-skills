---
name: single-scene-ai-video
description: Produces one Pruna cinematic clip (p-video) after an intake Q&A—text-to-video, image-to-video, or optional audio-conditioned—then async poll and download. Use when the user wants a single B-roll, product shot in motion, one hero video beat, or any one-off p-video without a multi-scene storyboard.
---

# Single-scene AI video (Pruna `p-video`)

One **`p-video`** prediction. See [p-video](../../../tools/video/p-video/SKILL.md) and [references/pruna-api.md](../../../references/pruna-api.md).

## Intake: ask before generating

**Do not** call `POST /v1/predictions` until these are answered and logged:

| Topic | Questions |
|-------|-----------|
| **Mode** | Text-only (`prompt` only), **image-to-video** (need upload first?), or **audio-driven** (upload duration sets clip length)? |
| **Creative** | What should happen in-frame (subject, camera, lighting, mood)? One paragraph max for `prompt`. |
| **Format** | `duration` (1–20s, ignored if audio), `resolution` (`720p` / `1080p`), `fps` (24 / 48), `aspect_ratio` if text-only (ignored when `image` is set)? |
| **Draft** | Use `draft: true` for cheaper preview or `false` for final quality? |
| **Safety / upsampling** | Client defaults for `disable_safety_filter` and `prompt_upsampling`? |
| **Repro** | Need a fixed `seed`? |
| **Delivery** | Async (recommended) or risk `Try-Sync: true` for a quick test? |

If the user has not chosen mode and duration (or audio path), **ask** before submitting.

## Workflow (after intake)

1. **Inputs** — If I2V or audio: `POST /v1/files`, use returned URLs in `input.image` or `input.audio`.
2. **Submit** — `Model: p-video`, JSON `input` per [model docs](https://docs.api.pruna.ai/guides/models/p-video). Prefer **async**; poll `get_url` until `succeeded`.
3. **Download** — Fetch `generation_url` with `apikey` header.
4. **Manifest** — Intake sheet + prediction id + final URL.

## Related

- Multi-scene `p-video` arcs: [multi-scene-ai-video](../multi-scene-ai-video/SKILL.md)
- Talking head instead: [single-scene-avatar-video](../single-scene-avatar-video/SKILL.md)
- Chain with stills/upscale: [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md)
