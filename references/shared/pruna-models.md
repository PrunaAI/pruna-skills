# Pruna models (index)

Pricing and limits change; confirm on the official page: [Available models](https://docs.api.pruna.ai/guides/models).

**Execution:** Multi-scene and batch runs should use **async parallel fan-out** and **subagents per independent lane** — see [parallel-execution.md](./parallel-execution.md).

## First-party Pruna models covered by this repo

| Model ID | Type | Skill folder | QA checklist |
|----------|------|----------------|--------------|
| `p-image` | Text-to-image | `tools/image/p-image` | `references/image/p-image-quality-checklist.md` |
| `p-image-edit` | Image edit / compose (1–5 images) | `tools/image/p-image-edit` | `references/image/p-image-edit-quality-checklist.md` |
| `p-image-upscale` | Upscale (target MP 1–128, optional enhance) | `tools/image/p-image-upscale` | `references/image/p-image-upscale-quality-checklist.md` |
| `p-image-try-on` | Virtual try-on (person + up to 11 garments, ≤6 recommended; optional pose ref, turbo) | `tools/image/p-image-try-on` | `references/image/p-image-try-on-quality-checklist.md` |
| `p-video` | Text / image / audio video; **first frame** (`image`) + **last frame** (`last_frame_image`) chaining | `tools/video/p-video` | `references/video/p-video-quality-checklist.md` |
| `p-video-avatar` | Talking avatar from portrait + script or audio | `tools/video/p-video-avatar` | `references/video/p-video-avatar-quality-checklist.md` |
| `p-video-animate` | Animate a still using source video motion (motion transfer) | `tools/video/p-video-animate` | `references/video/p-video-animate-quality-checklist.md` |
| `p-video-replace` | Replace people in source video using 1–4 identity images | `tools/video/p-video-replace` | `references/video/p-video-replace-quality-checklist.md` |

## External tools (Replicate)

| Tool | Type | Skill folder | Notes |
|------|------|--------------|-------|
| `stable-audio-2.5` | Text-to-music bed | `tools/audio/stable-audio-2.5` | Requires `REPLICATE_API_TOKEN`; mix via `launch_background_music.py` |
| `music-2.5` | Full song with vocals (lyrics + style) | `tools/audio/music-2.5` | Requires `REPLICATE_API_TOKEN`; [ai-music-video](../guides/workflows/verticals/music-video/SKILL.md) workflow |
| `gemini-3.1-flash-tts` | Narration / voiceover TTS | `tools/audio/gemini-3.1-flash-tts` | Requires `REPLICATE_API_TOKEN`; mux or drive `p-video` via uploaded audio — [audio-post-production.md](../audio/audio-post-production.md) |

## Related models (not duplicated as skills here)

Documented on the same models page: `p-image-lora`, trainers, `flux-*`, `wan-*`, `qwen-*`, `vace`, etc. Add a new `tools/.../<name>/SKILL.md` when you need agent guidance for another model.

## Composed workflows in this repo

| Workflow | Path |
|----------|------|
| Prompt-first fast entrypoint (auto route + direct chains) | `guides/workflows/router/pruna-run` |
| Pruna generative **scenario hub** (mood boards, packs, I2V, audio-led `p-video`, upscale chains; points to scene workflows) | `guides/workflows/router/pruna-generative-pipeline` |
| Single-scene avatar (`p-video-avatar`, intake first) | `guides/workflows/core/avatar-single-scene` |
| Multi-scene avatar (stills + `p-video-avatar` per scene, intake first) | `guides/workflows/core/avatar-multi-scene` |
| Single-scene cinematic (`p-video`, intake first) | `guides/workflows/core/image-to-video` |
| Multi-scene cinematic (`p-video` per scene, scene anchor triple) | `guides/workflows/core/narrated-multi-scene` |
| Multi-scene visual transitions (`p-image`/`p-image-edit` stills → `p-video` pair) | `guides/workflows/core/visual-transition-reel` |
| Educational explainer (narrator + character interaction) | `guides/workflows/verticals/interactive-explainer` |
| Upscale comparison demo | `guides/workflows/launches/p-image-upscale-comparison` |
| Motion-transfer showcase (`p-video-animate` + slider comparisons) | `guides/workflows/core/avatar-multi-scene` (animate rows); launch reel: `guides/workflows/launches/p-video-animate-comparison` |
| In-video replacement showcase (`p-video-replace` + slider comparisons) | `guides/workflows/launches/p-video-replace-comparison` |
| AI music video (lyrics → Music 2.5 → avatar + B-roll) | `guides/workflows/verticals/music-video` |
| Route I: UGC ad factory | `guides/workflows/ugc-ad-factory` |
| Route J: Product-to-story reel builder | `guides/workflows/product-to-story-reel-builder` |
| Route K: Ecommerce creative pack generator | `guides/workflows/ecommerce-creative-pack-generator` |
| Route L: Character IP content engine | `guides/workflows/character-ip-content-engine` |
