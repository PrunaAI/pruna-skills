# Pruna models (index)

Pricing and limits change; confirm on the official page: [Available models](https://docs.api.pruna.ai/guides/models).

**Execution:** Multi-scene and batch runs should use **async parallel fan-out** and **subagents per independent lane** — see [pruna-api.md](./pruna-api.md#parallel-async-multi-scene--batch).

## First-party Pruna models covered by this repo

| Model ID | Type | Skill folder | QA checklist |
|----------|------|----------------|--------------|
| `p-image` | Text-to-image (good quality, extremely fast) | `skills/image/p-image` | `skills/guides/image-prompting/references/p-image-quality-checklist.md` |
| `p-image-edit` | Image edit / compose (1–5 images) | `skills/image/p-image-edit` | `skills/guides/image-prompting/references/p-image-edit-quality-checklist.md` |
| `p-image-upscale` | Upscale (target MP 1–128, optional enhance) | `skills/image/p-image-upscale` | `skills/guides/image-prompting/references/p-image-upscale-quality-checklist.md` |
| `p-image-try-on` | Virtual try-on (person + up to 11 garments, ≤6 finals / 7–8 reliable; optional pose ref, turbo ~4) | `skills/image/p-image-try-on` | `skills/guides/image-prompting/references/p-image-try-on-quality-checklist.md` |
| `p-video` | Text / image / audio video; **first frame** (`image`) + **last frame** (`last_frame_image`) chaining | `skills/video/p-video` | `skills/guides/video-prompting/references/p-video-quality-checklist.md` |
| `p-video-avatar` | Talking avatar from portrait + script or audio | `skills/video/p-video-avatar` | `skills/guides/video-prompting/references/p-video-avatar-quality-checklist.md` |
| `p-video-animate` | Animate a still using source video motion (motion transfer) | `skills/video/p-video-animate` | `skills/guides/video-prompting/references/p-video-animate-quality-checklist.md` |
| `p-video-replace` | Replace people in source video using 1–4 identity images | `skills/video/p-video-replace` | `skills/guides/video-prompting/references/p-video-replace-quality-checklist.md` |

## External tools (Replicate)

| Tool | Type | Skill folder | Notes |
|------|------|--------------|-------|
| `stable-audio-2.5` | Text-to-music bed | `skills/audio/stable-audio-2.5` | Requires `REPLICATE_API_TOKEN`; mix via stable-audio-2.5 + ffmpeg bed mix |
| `music-2.5` | Full song with vocals (lyrics + style) | `skills/audio/music-2.5` | Requires `REPLICATE_API_TOKEN`; `music-video` workflow |
| `gemini-3.1-flash-tts` | Narration / voiceover TTS | `skills/audio/gemini-3.1-flash-tts` | Requires `REPLICATE_API_TOKEN`; mux or drive `p-video` via uploaded audio — [audio-post-production.md](../../audio-prompting/references/audio-post-production.md) |

## Related models (not duplicated as skills here)

Documented on the same models page: `p-image-lora`, trainers, `flux-*`, `wan-*`, `qwen-*`, `vace`, etc. Add a new `skills/.../<name>/SKILL.md` when you need agent guidance for another model.

## Composed workflows in this repo

| Workflow | Skill path |
|----------|------------|
| Full suite install | `skills/suite/pruna` (`@pruna`) |
| Single-scene avatar (`p-video-avatar`, intake first) | `skills/workflows/avatar-single-scene` |
| Multi-scene avatar (stills + `p-video-avatar` / animate rows) | `skills/workflows/avatar-multi-scene` |
| Single-scene cinematic (`p-video`, intake first) | `skills/workflows/image-to-video` |
| Multi-scene cinematic (`p-video` + scene anchor triple) | `skills/workflows/narrated-multi-scene` |
| Multi-scene visual transitions (stills → `p-video` pair) | `skills/workflows/visual-transition-reel` |
| Educational explainer (narrator + character) | `skills/workflows/interactive-explainer` |
| Illustrated story reel (Ken Burns / gentle `p-video`) | `skills/workflows/illustrated-story-reel` |
| AI music video (lyrics → Music 2.5 → avatar + B-roll) | `skills/workflows/music-video` |
| Virtual try-on + persona bar | `p-image-try-on` + [realistic-persona-showcase.md](../../image-prompting/references/realistic-persona-showcase.md) |
| Human recipe map | [docs/WORKFLOW-RECIPES.md](../../../../docs/WORKFLOW-RECIPES.md) |
