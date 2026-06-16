---
name: pruna-generative-pipeline
description: Use when the user needs the Pruna recipe/scenario menu, is unsure which workflow fits, or asks for chained P-API workflows with explicit confirmation gates.
license: MIT
metadata:
  version: "0.0.1"
---

# Pruna generative pipeline (scenario hub)

This skill is the **menu of proven chains** over the atomic tools in `tools/image` and `tools/video`. For HTTP details see [references/shared/pruna-api.md](../../../../references/shared/pruna-api.md).

Marketing and demo sites change layout and messaging often; **this repo is the source of truth** for what agents should run. When humans find a compelling flow elsewhere, **encode it here** (extend a recipe, add a row to the idea map, or add a dedicated workflow skill) after checking it against [docs.api.pruna.ai](https://docs.api.pruna.ai/guides/models)—do not send agents to browse live demos as part of execution.

**Tone:** Explain plans to the user like a producer—clear scene order, what generates first, and what they should hear or see—especially whenever **`voice_script`** or narration exists. Avoid stiff jargon in client-facing script drafts unless they ask for it.

## Quick reference

| Resource | Path |
|----------|------|
| Full recipe steps (A–R) | [recipe-catalog.md](../../../../references/workflows/recipe-catalog.md) |
| Feedback gates | [staged-generation-gate.md](../../../../references/shared/staged-generation-gate.md) · [requesting-generation-feedback](../requesting-generation-feedback/SKILL.md) |
| Parallel execution | [parallel-execution.md](../../../../references/shared/parallel-execution.md) |
| Pruna HTTP | [pruna-api.md](../../../../references/shared/pruna-api.md) |

## Intake: pick a scenario first

Ask the user which **recipe** fits (or hybrid). Capture answers before any `POST /v1/predictions`:

| Topic | Questions |
|-------|-----------|
| **Recipe** | Which row in the routing table below (or combination)? |
| **Deliverable** | Stills only, video clip(s), avatars, or mixed? |
| **Aspect / resolution** | e.g. `9:16` vs `16:9`; video default **`720p`** + **`24` fps** unless user wants `1080p`/`48` or draft preview? |
| **References** | Files to upload to `/v1/files` (URLs only in predictions)? |
| **Style lock** | One **style bible** sentence for technical consistency (aspect, no text)? Per-scene **`visual_style_tag`** for deliberate variety (anime, clay, Disney 3D, cyberpunk, etc.) — [visual-variety-bible.md](../../../../references/shared/visual-variety-bible.md) |
| **Character / scenes** | Character sheet (age, look, realism, personality)? Per-scene **angle, setting, emotion, lighting** deltas? Locked **`seed`**? Cast diversity on launch reels? |
| **Voice / cast** | For talking heads: **one Pruna `voice` per character**; **natural human `voice_script`**; **realistic conversational `voice_prompt`**; unique **`video_prompt`** per scene. |
| **Scenes** | If multiple clips: scene table with distinct backgrounds/angles (or defer to [multi-scene-ai-video](../core/narrated-multi-scene/SKILL.md) / [multi-scene-avatar-video](../core/avatar-multi-scene/SKILL.md))? |

## Confirmation and execution (all recipes)

1. **Draft** any scripts, beats, or prompts that the user must approve in **natural, human language** (spoken wording for VO; clear intent per scene otherwise).
2. **Pause** and obtain **explicit confirmation** (“approve”, “go”, “run it”) before the first upload or **`POST /v1/predictions`**. If the user revises copy or cast, re-confirm when the change matters for cost or outcome.
3. **Staged execution** — after plan approval: stills only → user approves → audio prep (TTS / song) when applicable → user approves → video → user approves clips → assembly and final audio (bed). See [staged-generation-gate.md](../../../../references/shared/staged-generation-gate.md) and [requesting-generation-feedback](../requesting-generation-feedback/SKILL.md).
4. **Write** a **runnable generation package**—script or phased API steps—that matches the approved plan **exactly**. Use **async parallel fan-out** within each phase (see [parallel-execution.md](../../../../references/shared/parallel-execution.md)); avoid serial scene-by-scene execution when lanes are independent.
5. **Execute** that package when possible (**`PRUNA_API_KEY`**, network). Prefer **subagents per scene lane** (still pipeline or avatar job) when the host supports parallel agents. If execution is not possible here, deliver the same artifact for local runs.

Deep avatar workflows already spell out cast ledgers, hero reuse, and read-throughs in [multi-scene-avatar-video](../core/avatar-multi-scene/SKILL.md) and [single-scene-avatar-video](../core/avatar-single-scene/SKILL.md); defer to those when recipe **G** or **H** involves **`p-video-avatar`**.

## Routing table

| Recipe | You get | Primary models | Deep workflow (if any) |
|--------|---------|----------------|-------------------------|
| A — **Style-locked mood board** | N stills, same world | `p-image` → optional `p-image-edit` | Stay in this skill |
| B — **Hero + variants** | One anchor + edits | `p-image` → `p-image-edit` | — |
| C — **Print / pixel rescue** | Higher-res master | `p-image-upscale` → optional `p-image-edit` | — |
| D — **Animate a plate** | One motion clip from a still | `p-image` or upload → `p-video` (I2V) | [single-scene-ai-video](../core/image-to-video/SKILL.md) |
| E — **Audio-led cut** | Video length follows VO/music | upload `audio` → `p-video` | [single-scene-ai-video](../core/image-to-video/SKILL.md) |
| F — **Draft → final video** | Cheap preview then hi-fi | `p-video` (`draft: true`) then rerun `draft: false` with locked `seed`/prompt | [multi-scene-ai-video](../core/narrated-multi-scene/SKILL.md) for many beats |
| G — **Talking head** | Portrait + speech | `p-image` / `p-image-edit` → `p-video-avatar` | [single-scene-avatar-video](../core/avatar-single-scene/SKILL.md) or [multi-scene-avatar-video](../core/avatar-multi-scene/SKILL.md) |
| H — **Social hook stack** | Short vertical beats | Several `p-video` and/or avatars | Multi-scene skills above |
| I — **UGC ad factory** | Batch hook/offer/CTA avatar ads | `p-image` / `p-image-edit` → `p-video-avatar` | [ugc-ad-factory](../ugc-ad-factory/SKILL.md) |
| J — **Product-to-story reel** | 4-6 beat narrative product reel | `p-image-edit` → `p-video` | [product-to-story-reel-builder](../product-to-story-reel-builder/SKILL.md) |
| K — **Ecommerce creative pack** | Packshots + lifestyle + motion loop; virtual try-on on model photos | `p-image-try-on` / `p-image-edit` → optional `p-image-upscale` / `p-video` | [ecommerce-creative-pack-generator](../ecommerce-creative-pack-generator/SKILL.md) · [p-image-try-on](../../../../tools/image/p-image-try-on/SKILL.md) |
| L — **Character IP engine** | Episodic continuity for mascot/cast | `p-image` / `p-image-edit` + `p-video` / `p-video-avatar` | [character-ip-content-engine](../character-ip-content-engine/SKILL.md) |
| M — **Motion-transfer showcase** | Same motion, new subject + slider before/after | motion `.mp4` + still → `p-video-animate` → slider compare MP4 | [multi-scene-avatar-video](../core/avatar-multi-scene/SKILL.md) (`animate` rows) |
| N — **In-video replacement showcase** | Swap people/products in footage + slider before/after | dynamic `p-image` refs → optional `p-video-avatar` source → `p-video-replace` → slider compare MP4 | [p-video-replace-comparison](../launches/p-video-replace-comparison/SKILL.md) |
| O — **AI music video** | Full song + lyric-synced video | lyrics → [music-2.5](../../../../tools/audio/music-2.5/SKILL.md) → cut map → `p-video-avatar` + `p-video` → assembly; hero + `p-image-edit` when one singer throughout | [ai-music-video](../verticals/music-video/SKILL.md) |
| P — **Narrated story film** | Multi-scene B-roll + VO (+ optional bed) | hero → `p-image-edit` start/end stills → `p-video` with `image` + `last_frame_image` chain → [gemini-3.1-flash-tts](../../../../tools/audio/gemini-3.1-flash-tts/SKILL.md) → concat + mux ± [stable-audio-2.5](../../../../tools/audio/stable-audio-2.5/SKILL.md) | [multi-scene-ai-video](../core/narrated-multi-scene/SKILL.md) · [audio-post-production.md](../../../../references/audio/audio-post-production.md) |
| Q — **Visual transition reel** | Multi-scene motion between two stills per beat (no VO) | `p-image` hero → `p-image-edit` start/end stills → `p-video` pair (`duration`) → selective frame chain → concat | [scene-transition-video](../core/visual-transition-reel/SKILL.md) · [scene-anchor-pair.md](../../../../references/video/scene-anchor-pair.md) |
| R — **Educational explainer** | Narrator VO + expert/character dialogue | `p-image` hero → `p-image-edit` stills → **`narrator`** triple + **`character`** avatar → concat ± bed | [interactive-explainer](../verticals/interactive-explainer/SKILL.md) · [interactive-explainer-scenes.md](../../../../references/workflows/interactive-explainer-scenes.md) |
| S — **Illustrated story reel** | Still-image story with VO or music (no video API) | `p-image` hero → `p-image-edit` beats → Gemini TTS **or** Stable Audio → ffmpeg Ken Burns + mux | [illustrated-story-reel](../verticals/illustrated-story-reel/SKILL.md) |

## Handoff rules (all recipes)

- Use **Pruna file URLs** only (`POST /v1/files` → `urls.get`) in `images`, `image`, `audio`.
- **Async + parallel by default** for `p-video`, `p-video-avatar`, and batch stills—create all jobs in the current phase together, poll all `get_url` until done ([parallel-execution.md](../../../../references/shared/parallel-execution.md)). Use **subagents** for independent scene lanes after confirmation.
- **Do not** chain the next step until the previous URL is valid and (for portraits) checklist-approved when using recipe **G**.
- **Character continuity:** One **approved source / hero** URL per recurring subject; branch new looks and styles with **`p-image-edit`** from that URL (plus style bible), not unrelated fresh **`p-image`** identity pulls—unless the user resets the character.
- **Dynamic scenes:** Multi-scene avatar pieces must vary **camera angle**, **background/setting**, **lighting**, and **`visual_style_tag`** per beat—no repetitive office-only stacks unless requested. Run [visual-variety-bible.md](../../../../references/shared/visual-variety-bible.md) checklist on launch reels.
- **Photoreal stills:** Hero via **`p-image`** (documentary/photoreal prompt) → slop gate; every **`p-image-edit`** still → slop gate before **`p-video-avatar`**.
- **Seed lock:** Record **`project_seed`** at hero generation; reuse on hero regen and all **`p-video-avatar`** calls in the project manifest.
- **Same voice for the same role:** When a character speaks in more than one clip, keep **`voice`** (and usually **`voice_language`**) identical across those clips.
- **Human delivery:** **`voice_script`** = speakable dialogue; **`voice_prompt`** = realistic performance direction (never marketing copy).

## Recipes (one-liners)

Full intake, steps, and shine lines for every letter: **[recipe-catalog.md](../../../../references/workflows/recipe-catalog.md)**.

| Recipe | One-liner |
|--------|-----------|
| **A** | N style-locked `p-image` panels ± `p-image-edit` drift fix |
| **B** | One hero → `p-image-edit` variants |
| **C** | `p-image-upscale` → `p-image-edit` |
| **D** | Still → `p-video` I2V ([image-to-video](../core/image-to-video/SKILL.md)) |
| **E** | Upload audio → `p-video` (duration follows audio) |
| **F** | `draft: true` previews → locked `draft: false` finals |
| **G** | Hero + edits → `p-video-avatar` ([avatar skills](../core/avatar-multi-scene/SKILL.md)) |
| **H** | 2–5 vertical avatar beats, distinct worlds per scene |
| **I–L** | UGC ads · product reels · ecommerce pack · character IP (dedicated workflow skills) |
| **M** | Motion template + still → `p-video-animate` + slider |
| **N** | Replace in footage + slider ([p-video-replace-comparison](../launches/p-video-replace-comparison/SKILL.md)) |
| **O** | Lyrics → song → synced clips ([music-video](../verticals/music-video/SKILL.md)) |
| **P** | Scene anchor triple + VO ([narrated-multi-scene](../core/narrated-multi-scene/SKILL.md)) |
| **Q** | Start/end still pairs, no VO ([visual-transition-reel](../core/visual-transition-reel/SKILL.md)) |
| **R** | Narrator + character dialogue ([interactive-explainer](../verticals/interactive-explainer/SKILL.md)) |

## Atomic tool index

| Model | Skill |
|-------|--------|
| `p-image` | [p-image](../../../../tools/image/p-image/SKILL.md) |
| `p-image-edit` | [p-image-edit](../../../../tools/image/p-image-edit/SKILL.md) |
| `p-image-upscale` | [p-image-upscale](../../../../tools/image/p-image-upscale/SKILL.md) |
| `p-image-try-on` | [p-image-try-on](../../../../tools/image/p-image-try-on/SKILL.md) |
| `p-video` | [p-video](../../../../tools/video/p-video/SKILL.md) |
| `p-video-avatar` | [p-video-avatar](../../../../tools/video/p-video-avatar/SKILL.md) |
| `p-video-animate` | [p-video-animate](../../../../tools/video/p-video-animate/SKILL.md) |
| `p-video-replace` | [p-video-replace](../../../../tools/video/p-video-replace/SKILL.md) |
| `stable-audio-2.5` (Replicate) | [stable-audio-2.5](../../../../tools/audio/stable-audio-2.5/SKILL.md) — launch reel bed under VO |
| `gemini-3.1-flash-tts` (Replicate) | [gemini-3.1-flash-tts](../../../../tools/audio/gemini-3.1-flash-tts/SKILL.md) — narration / voiceover |
| `music-2.5` (Replicate) | [music-2.5](../../../../tools/audio/music-2.5/SKILL.md) — full songs with vocals |

Audio layering guide: [audio-post-production.md](../../../../references/audio/audio-post-production.md) · Scene anchor triple: [scene-anchor-triple.md](../../../../references/video/scene-anchor-triple.md)

Product-positioning idea map: [recipe-catalog.md](../../../../references/workflows/recipe-catalog.md) **More ideas**.
