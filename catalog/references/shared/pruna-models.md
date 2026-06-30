# Pruna models (index)

Pricing and limits change; confirm on the official page: [Available models](https://docs.api.pruna.ai/guides/models).

**Execution:** Multi-scene and batch runs should use **async parallel fan-out** and **subagents per independent lane** — see [parallel-execution.md](./parallel-execution.md).

## First-party Pruna models covered by this repo

| Model ID | Type | Skill folder | QA checklist |
|----------|------|----------------|--------------|
| `p-image` | Text-to-image | `catalog/tools/image/p-image` | `catalog/references/image/p-image-quality-checklist.md` |
| `p-image-edit` | Image edit / compose (1–5 images) | `catalog/tools/image/p-image-edit` | `catalog/references/image/p-image-edit-quality-checklist.md` |
| `p-image-upscale` | Upscale (target MP 1–128, optional enhance) | `catalog/tools/image/p-image-upscale` | `catalog/references/image/p-image-upscale-quality-checklist.md` |
| `p-image-try-on` | Virtual try-on (person + up to 11 garments, ≤6 finals / 7–8 reliable; optional pose ref, turbo ~4) | `catalog/tools/image/p-image-try-on` | `catalog/references/image/p-image-try-on-quality-checklist.md` |
| `p-video` | Text / image / audio video; **first frame** (`image`) + **last frame** (`last_frame_image`) chaining | `catalog/tools/video/p-video` | `catalog/references/video/p-video-quality-checklist.md` |
| `p-video-avatar` | Talking avatar from portrait + script or audio | `catalog/tools/video/p-video-avatar` | `catalog/references/video/p-video-avatar-quality-checklist.md` |
| `p-video-animate` | Animate a still using source video motion (motion transfer) | `catalog/tools/video/p-video-animate` | `catalog/references/video/p-video-animate-quality-checklist.md` |
| `p-video-replace` | Replace people in source video using 1–4 identity images | `catalog/tools/video/p-video-replace` | `catalog/references/video/p-video-replace-quality-checklist.md` |

## External tools (Replicate)

| Tool | Type | Skill folder | Notes |
|------|------|--------------|-------|
| `stable-audio-2.5` | Text-to-music bed | `catalog/tools/audio/stable-audio-2.5` | Requires `REPLICATE_API_TOKEN`; mix via `launch_background_music.py` |
| `music-2.5` | Full song with vocals (lyrics + style) | `catalog/tools/audio/music-2.5` | Requires `REPLICATE_API_TOKEN`; [ai-music-video](../workflows/verticals/music-video/SKILL.md) workflow |
| `gemini-3.1-flash-tts` | Narration / voiceover TTS | `catalog/tools/audio/gemini-3.1-flash-tts` | Requires `REPLICATE_API_TOKEN`; mux or drive `p-video` via uploaded audio — [audio-post-production.md](../audio/audio-post-production.md) |

## Related models (not duplicated as skills here)

Documented on the same models page: `p-image-lora`, trainers, `flux-*`, `wan-*`, `qwen-*`, `vace`, etc. Add a new `tools/.../<name>/SKILL.md` when you need agent guidance for another model.

## Composed workflows in this repo

| Workflow | Path |
|----------|------|
| Prompt-first fast entrypoint (auto route + direct chains) | `catalog/workflows/router/pruna-run` |
| Pruna generative **scenario hub** (mood boards, packs, I2V, audio-led `p-video`, upscale chains; points to scene workflows) | `catalog/workflows/router/pruna-generative-pipeline` |
| Single-scene avatar (`p-video-avatar`, intake first) | `catalog/workflows/core/avatar-single-scene` |
| Multi-scene avatar (stills + `p-video-avatar` per scene, intake first) | `catalog/workflows/core/avatar-multi-scene` |
| Single-scene cinematic (`p-video`, intake first) | `catalog/workflows/core/image-to-video` |
| Multi-scene cinematic (`p-video` per scene, scene anchor triple) | `catalog/workflows/core/narrated-multi-scene` |
| Multi-scene visual transitions (`p-image`/`p-image-edit` stills → `p-video` pair) | `catalog/workflows/core/visual-transition-reel` |
| Educational explainer (narrator + character interaction) | `catalog/workflows/verticals/interactive-explainer` |
| Upscale comparison demo | `catalog/workflows/_shared/scripts/generate_upscale_comparison.py` |
| Motion-transfer showcase (`p-video-animate` + slider comparisons) | `catalog/workflows/core/avatar-multi-scene` (animate rows); slider script: `catalog/workflows/_shared/scripts/generate_video_comparison.py` |
| In-video replacement showcase (`p-video-replace` + slider comparisons) | `catalog/workflows/_shared/scripts/generate_video_comparison.py` |
| Virtual try-on reel (`p-image-try-on` + avatar / I2V + bed) | `p-image-try-on` tool skill + [realistic-persona-showcase.md](./realistic-persona-showcase.md) |
| AI music video (lyrics → Music 2.5 → avatar + B-roll) | `catalog/workflows/verticals/music-video` |
| Route I: UGC ad factory | `catalog/workflows/ugc-ad-factory` |
| Route J: Product-to-story reel builder | `catalog/workflows/product-to-story-reel-builder` |
| Route K: Ecommerce creative pack generator | `catalog/workflows/ecommerce-creative-pack-generator` |
| Route L: Character IP content engine | `catalog/workflows/character-ip-content-engine` |
