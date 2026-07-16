# Generation quality checklist hub

Use this as the shared quality gate across models and workflows.
Run the **Core checklist** for every generation job, then run the model-specific checklist.

## Who applies these checklists?

**The coding agent** — by **opening the real output files** (images, video, or audio) and reviewing them with vision. These checklists are **not** automated test scripts. There is no separate scoring service: the agent reads each item and judges pass or fail from what it sees and hears.

Typical flow:

1. **Generate or download** the asset to a local path (`stills/`, `clips/`, etc.).
2. **Inspect the file** — view the image, watch the video clip, or listen to narration when the checklist covers audio.
3. Run the **Core checklist** (below), then the **model-specific checklist** for that job.
4. **If something fails** — note which items failed, adjust prompt / settings / seed, and regenerate **only that asset** (do not advance to expensive video steps on a bad still).
5. **If it passes** — show the user the file paths (and previews when helpful). In workflows, still follow [staged-generation-gate.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/staged-generation-gate/SKILL.md): agent checklist review happens **before** you ask the user to approve stills or clips.

The user's **approve plan / approve stills / approve clips** gates are separate. Agent checklists catch obvious problems early so the user is not asked to sign off on broken outputs.

Maintenance rule: keep tool/guide mapping only in this file to avoid link drift.

## Match map (tool -> checklist -> guides)

| Tool/model | Checklist | Common guides |
|------------|-----------|---------------|
| `p-image` | [`p-image-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/image/p-image-quality-checklist.md) · persona bar: [`realistic-persona-showcase.md`](./realistic-persona-showcase.md) | [`image-to-video`](../../image-to-video/SKILL.md), [`narrated-multi-scene`](../../narrated-multi-scene/SKILL.md), [`pruna-generative-pipeline`](../../pruna-generative-pipeline/SKILL.md) |
| `p-image-edit` | [`p-image-edit-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/image/p-image-edit-quality-checklist.md) | [`avatar-single-scene`](../../avatar-single-scene/SKILL.md), [`avatar-multi-scene`](../../avatar-multi-scene/SKILL.md), [`pruna-generative-pipeline`](../../pruna-generative-pipeline/SKILL.md) |
| `p-image-upscale` | [`p-image-upscale-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/image/p-image-upscale-quality-checklist.md) | [`image-to-video`](../../image-to-video/SKILL.md), [`narrated-multi-scene`](../../narrated-multi-scene/SKILL.md), [`pruna-generative-pipeline`](../../pruna-generative-pipeline/SKILL.md), [`generate_upscale_comparison.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/generate_upscale_comparison.py) |
| `p-image-try-on` | [`p-image-try-on-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/image/p-image-try-on-quality-checklist.md) | [`pruna-generative-pipeline`](../../pruna-generative-pipeline/SKILL.md), [`p-image-try-on`](../../p-image-try-on/SKILL.md), [`realistic-persona-showcase.md`](./realistic-persona-showcase.md) |
| `p-video` | [`p-video-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/video/p-video-quality-checklist.md) | [`image-to-video`](../../image-to-video/SKILL.md), [`narrated-multi-scene`](../../narrated-multi-scene/SKILL.md), [`interactive-explainer`](../../interactive-explainer/SKILL.md), [`visual-transition-reel`](../../visual-transition-reel/SKILL.md), [`pruna-generative-pipeline`](../../pruna-generative-pipeline/SKILL.md) |
| `p-video-avatar` | [`p-video-avatar-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/video/p-video-avatar-quality-checklist.md) · persona bar: [`realistic-persona-showcase.md`](./realistic-persona-showcase.md) | [`avatar-single-scene`](../../avatar-single-scene/SKILL.md), [`avatar-multi-scene`](../../avatar-multi-scene/SKILL.md), [`interactive-explainer`](../../interactive-explainer/SKILL.md), [`pruna-generative-pipeline`](../../pruna-generative-pipeline/SKILL.md) |
| `p-video-animate` | [`p-video-animate-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/video/p-video-animate-quality-checklist.md) | [`avatar-multi-scene`](../../avatar-multi-scene/SKILL.md), [`pruna-generative-pipeline`](../../pruna-generative-pipeline/SKILL.md) |
| `p-video-replace` | [`p-video-replace-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/video/p-video-replace-quality-checklist.md) | [`p-video-replace`](../../p-video-replace/SKILL.md), [`generate_video_comparison.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/generate_video_comparison.py) |
| `music-2.5` + music video assembly | [`music-video-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/music-video-quality-checklist.md) | [`music-video`](../../music-video/SKILL.md), [`music-2.5`](../../music-2.5/SKILL.md) |

## Core checklist (all models)

- **[Generation diversity](./generation-diversity.md)** — ritual seed + rotate scenario axes on **every** model (image, video, try-on, avatar, …).
- **[Random seed ritual](./random-seed-ritual.md) (SSoT)** — generate and state a ritual string **before** every generation; derive prompt axes via sum-mod; never copy example strings from docs.
- Goal and acceptance criteria are explicit (what "good" looks like is written down).
- Input assets are valid and licensed (URL/file reachable, rights cleared).
- Prompt and settings match the intended output format (`aspect_ratio`, duration, resolution, style lock). **Video default:** `720p`, `24` fps unless the brief asks for final `1080p` / `48`.
- Output contains no accidental watermarks, UI overlays, or stray text unless requested.
- Brand, legal, and safety constraints are satisfied before handoff.
- Manifest/log captures model, input fields, prediction id, output URL, and **`ritual_seed`** for traceability.

## Model-specific checklists

- [`p-image-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/image/p-image-quality-checklist.md)
- [`p-image-edit-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/image/p-image-edit-quality-checklist.md)
- [`p-image-upscale-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/image/p-image-upscale-quality-checklist.md)
- [`p-image-try-on-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/image/p-image-try-on-quality-checklist.md)
- [`p-video-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/video/p-video-quality-checklist.md)
- [`p-video-avatar-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/video/p-video-avatar-quality-checklist.md)
- [`p-video-animate-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/video/p-video-animate-quality-checklist.md)
- [`p-video-replace-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/video/p-video-replace-quality-checklist.md)
- [`music-video-quality-checklist.md`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/music-video-quality-checklist.md)

## Visual variety (launch reels)

Before **any** generation, run [generation-diversity.md](./generation-diversity.md). Launch reels: also [visual-variety-bible.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/visual-variety-bible/SKILL.md) **Variety checklist**. Persona/playground bar: [realistic-persona-showcase.md](./realistic-persona-showcase.md).

For phased human review before expensive video jobs, see [staged-generation-gate.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/staged-generation-gate/SKILL.md) and the per-skill index [workflow-feedback-gates.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/workflow-feedback-gates.md).

## Workflow note

For multi-scene projects, run these checks per scene and add a final continuity pass
(style, character identity, voice, and pacing consistency across scenes).

**Narrated cinematic B-roll:** validate [scene anchor triple](https://github.com/PrunaAI/pruna-skills/tree/main/video/scene-anchor-triple.md) inputs before `p-video` — start still, end still, uploaded narration URL per row.
