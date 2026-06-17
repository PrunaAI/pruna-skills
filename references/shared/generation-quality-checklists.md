# Generation quality checklist hub

Use this as the shared quality gate across models and workflows.
Run the **Core checklist** for every generation job, then run the model-specific checklist.

Maintenance rule: keep tool/guide mapping only in this file to avoid link drift.

## Match map (tool -> checklist -> guides)

| Tool/model | Checklist | Common guides |
|------------|-----------|---------------|
| `p-image` | [`p-image-quality-checklist.md`](../image/p-image-quality-checklist.md) · persona bar: [`realistic-persona-showcase.md`](./realistic-persona-showcase.md) | [`single-scene-ai-video`](../guides/workflows/core/image-to-video/SKILL.md), [`multi-scene-ai-video`](../guides/workflows/core/narrated-multi-scene/SKILL.md), [`pruna-generative-pipeline`](../guides/workflows/router/pruna-generative-pipeline/SKILL.md) |
| `p-image-edit` | [`p-image-edit-quality-checklist.md`](../image/p-image-edit-quality-checklist.md) | [`single-scene-avatar-video`](../guides/workflows/core/avatar-single-scene/SKILL.md), [`multi-scene-avatar-video`](../guides/workflows/core/avatar-multi-scene/SKILL.md), [`pruna-generative-pipeline`](../guides/workflows/router/pruna-generative-pipeline/SKILL.md) |
| `p-image-upscale` | [`p-image-upscale-quality-checklist.md`](../image/p-image-upscale-quality-checklist.md) | [`single-scene-ai-video`](../guides/workflows/core/image-to-video/SKILL.md), [`multi-scene-ai-video`](../guides/workflows/core/narrated-multi-scene/SKILL.md), [`pruna-generative-pipeline`](../guides/workflows/router/pruna-generative-pipeline/SKILL.md), [`p-image-upscale-comparison`](../guides/workflows/launches/p-image-upscale-comparison/SKILL.md) |
| `p-image-try-on` | [`p-image-try-on-quality-checklist.md`](../image/p-image-try-on-quality-checklist.md) · showcase: [`p-image-try-on-showcase.md`](../image/p-image-try-on-showcase.md) | [`pruna-generative-pipeline`](../guides/workflows/router/pruna-generative-pipeline/SKILL.md) (ecommerce / catalog recipes) |
| `p-video` | [`p-video-quality-checklist.md`](../video/p-video-quality-checklist.md) | [`single-scene-ai-video`](../guides/workflows/core/image-to-video/SKILL.md), [`multi-scene-ai-video`](../guides/workflows/core/narrated-multi-scene/SKILL.md), [`educational-explainer`](../guides/workflows/verticals/interactive-explainer/SKILL.md), [`scene-transition-video`](../guides/workflows/core/visual-transition-reel/SKILL.md), [`pruna-generative-pipeline`](../guides/workflows/router/pruna-generative-pipeline/SKILL.md) |
| `p-video-avatar` | [`p-video-avatar-quality-checklist.md`](../video/p-video-avatar-quality-checklist.md) · persona bar: [`realistic-persona-showcase.md`](./realistic-persona-showcase.md) | [`single-scene-avatar-video`](../guides/workflows/core/avatar-single-scene/SKILL.md), [`multi-scene-avatar-video`](../guides/workflows/core/avatar-multi-scene/SKILL.md), [`educational-explainer`](../guides/workflows/verticals/interactive-explainer/SKILL.md), [`pruna-generative-pipeline`](../guides/workflows/router/pruna-generative-pipeline/SKILL.md) |
| `p-video-animate` | [`p-video-animate-quality-checklist.md`](../video/p-video-animate-quality-checklist.md) | [`multi-scene-avatar-video`](../guides/workflows/core/avatar-multi-scene/SKILL.md), [`pruna-generative-pipeline`](../guides/workflows/router/pruna-generative-pipeline/SKILL.md) |
| `p-video-replace` | [`p-video-replace-quality-checklist.md`](../video/p-video-replace-quality-checklist.md) | [`p-video-replace`](../tools/video/p-video-replace/SKILL.md), [`p-video-replace-comparison`](../guides/workflows/launches/p-video-replace-comparison/SKILL.md) |
| `music-2.5` + music video assembly | [`music-video-quality-checklist.md`](../workflows/music-video-quality-checklist.md) | [`ai-music-video`](../guides/workflows/verticals/music-video/SKILL.md), [`music-2.5`](../tools/audio/music-2.5/SKILL.md) |

## Core checklist (all models)

- **[Generation diversity](./generation-diversity.md)** — ritual seed + rotate scenario axes on **every** model (image, video, try-on, avatar, …).
- **[Random seed ritual](./random-seed-ritual.md)** — pick and state a random integer **before** every generation; never copy example seeds from docs unless user locked a seed.
- Goal and acceptance criteria are explicit (what "good" looks like is written down).
- Input assets are valid and licensed (URL/file reachable, rights cleared).
- Prompt and settings match the intended output format (`aspect_ratio`, duration, resolution, style lock). **Video default:** `720p`, `24` fps unless the brief asks for final `1080p` / `48`.
- Output contains no accidental watermarks, UI overlays, or stray text unless requested.
- Brand, legal, and safety constraints are satisfied before handoff.
- Manifest/log captures model, input fields, prediction id, output URL, and **ritual seed** for reproducibility.

## Model-specific checklists

- [`p-image-quality-checklist.md`](../image/p-image-quality-checklist.md)
- [`p-image-edit-quality-checklist.md`](../image/p-image-edit-quality-checklist.md)
- [`p-image-upscale-quality-checklist.md`](../image/p-image-upscale-quality-checklist.md)
- [`p-image-try-on-quality-checklist.md`](../image/p-image-try-on-quality-checklist.md)
- [`p-video-quality-checklist.md`](../video/p-video-quality-checklist.md)
- [`p-video-avatar-quality-checklist.md`](../video/p-video-avatar-quality-checklist.md)
- [`p-video-animate-quality-checklist.md`](../video/p-video-animate-quality-checklist.md)
- [`p-video-replace-quality-checklist.md`](../video/p-video-replace-quality-checklist.md)
- [`music-video-quality-checklist.md`](../workflows/music-video-quality-checklist.md)

## Visual variety (launch reels)

Before **any** generation, run [generation-diversity.md](./generation-diversity.md). Launch reels: also [visual-variety-bible.md](./visual-variety-bible.md) **Variety checklist**. Persona/playground bar: [realistic-persona-showcase.md](./realistic-persona-showcase.md).

For phased human review before expensive video jobs, see [staged-generation-gate.md](./staged-generation-gate.md) and the per-skill index [workflow-feedback-gates.md](../workflows/workflow-feedback-gates.md).

## Workflow note

For multi-scene projects, run these checks per scene and add a final continuity pass
(style, character identity, voice, and pacing consistency across scenes).

**Narrated cinematic B-roll:** validate [scene anchor triple](../video/scene-anchor-triple.md) inputs before `p-video` — start still, end still, uploaded narration URL per row.
