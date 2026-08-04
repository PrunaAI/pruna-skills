# Pruna models (index)

Pricing and limits change; confirm on the official page: [Available models](https://docs.api.pruna.ai/guides/models).

**Execution:** Multi-scene and batch runs should use **async parallel fan-out** and **subagents per independent lane** — see [pruna-api.md](./pruna-api.md#parallel-async-multi-scene--batch).

## First-party Pruna models covered by this repo

| Model ID | Type | Tool skill | QA checklist (install guide) |
|----------|------|------------|------------------------------|
| `p-image` | Text-to-image (good quality, extremely fast; use when user asks cheap/fast) | `p-image` | `p-image-quality-checklist.md` in `image-prompting` |
| `p-image-ideogram` | Text-to-image (photoreal, typography, 1K/2K, thinking levels; default T2I when speed/cost not prioritized) | `p-image-ideogram` | `p-image-quality-checklist.md` in `image-prompting` |
| `p-image-edit` | Image edit / compose (1–5 images) | `p-image-edit` | `p-image-edit-quality-checklist.md` in `image-prompting` |
| `p-image-upscale` | Upscale (target MP 1–128, optional enhance) | `p-image-upscale` | `p-image-upscale-quality-checklist.md` in `image-prompting` |
| `p-image-try-on` | Virtual try-on (person + up to 11 garments, ≤6 finals / 7–8 reliable; optional pose ref, turbo ~4) | `p-image-try-on` | `p-image-try-on-quality-checklist.md` in `image-prompting` |
| `p-video` | Text / image / audio video; **first frame** (`image`) + **last frame** (`last_frame_image`) chaining | `p-video` | `p-video-quality-checklist.md` in `video-prompting` |
| `p-video-avatar` | Talking avatar from portrait + script or audio | `p-video-avatar` | `p-video-avatar-quality-checklist.md` in `video-prompting` |
| `p-video-animate` | Animate a still using source video motion (motion transfer) | `p-video-animate` | `p-video-animate-quality-checklist.md` in `video-prompting` |
| `p-video-replace` | Replace people in source video using 1–4 identity images | `p-video-replace` | `p-video-replace-quality-checklist.md` in `video-prompting` |

## External tools (Replicate)

| Tool | Type | Tool skill | Notes |
|------|------|------------|-------|
| `stable-audio-2.5` | Text-to-music bed | `stable-audio-2.5` | Requires `REPLICATE_API_TOKEN`; mix via ffmpeg bed mix |
| `music-2.5` | Full song with vocals (lyrics + style) | `music-2.5` | Requires `REPLICATE_API_TOKEN`; `music-video` workflow |
| `gemini-3.1-flash-tts` | Narration / voiceover TTS | `gemini-3.1-flash-tts` | Requires `REPLICATE_API_TOKEN`; mux or drive `p-video` via uploaded audio — `audio-prompting` |

## Related models (not duplicated as skills here)

Documented on the same models page: `p-image-lora`, trainers, `flux-*`, `wan-*`, `qwen-*`, `vace`, etc. Add a new tool skill when you need agent guidance for another model.

## Composed workflows in this repo

| Workflow | Skill |
|----------|-------|
| Full suite install | `pruna` |
| Single-scene avatar (`p-video-avatar`, intake first) | `avatar-single-scene` |
| Multi-scene avatar (stills + `p-video-avatar` / animate rows) | `avatar-multi-scene` |
| Single-scene cinematic (`p-video`, intake first) | `image-to-video` |
| Multi-scene cinematic (`p-video` + scene anchor triple) | `narrated-multi-scene` |
| Multi-scene visual transitions (stills → `p-video` pair) | `visual-transition-reel` |
| Educational explainer (narrator + character) | `interactive-explainer` |
| Illustrated story reel (Ken Burns / gentle `p-video`) | `illustrated-story-reel` |
| AI music video (lyrics → Music 2.5 → avatar + B-roll) | `music-video` |
| Virtual try-on + persona bar | `p-image-try-on` + `image-prompting` |
| Human recipe map | repo `docs/WORKFLOW-RECIPES.md` (not a skill) |
