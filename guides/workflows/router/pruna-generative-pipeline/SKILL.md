---
name: pruna-generative-pipeline
description: Scenario hub for Pruna P-API chains—including scene anchor triple narrated films (Recipe P), character sheets, hero/source reuse via p-image-edit, explicit user confirmation before any POST /v1/predictions, then async parallel fan-out.
license: MIT
metadata:
  version: "0.0.1"
---

# Pruna generative pipeline (scenario hub)

This skill is the **menu of proven chains** over the atomic tools in `tools/image` and `tools/video`. For HTTP details see [references/shared/pruna-api.md](../../../../references/shared/pruna-api.md).

Marketing and demo sites change layout and messaging often; **this repo is the source of truth** for what agents should run. When humans find a compelling flow elsewhere, **encode it here** (extend a recipe, add a row to the idea map, or add a dedicated workflow skill) after checking it against [docs.api.pruna.ai](https://docs.api.pruna.ai/guides/models)—do not send agents to browse live demos as part of execution.

**Tone:** Explain plans to the user like a producer—clear scene order, what generates first, and what they should hear or see—especially whenever **`voice_script`** or narration exists. Avoid stiff jargon in client-facing script drafts unless they ask for it.

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
3. **Staged execution** — after plan approval: stills only → user approves → audio prep (TTS / song) when applicable → user approves → video → user approves clips → assembly and final audio (bed). See [staged-generation-gate.md](../../../../references/shared/staged-generation-gate.md).
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
| K — **Ecommerce creative pack** | Packshots + lifestyle + motion loop | `p-image-edit` → optional `p-image-upscale` / `p-video` | [ecommerce-creative-pack-generator](../ecommerce-creative-pack-generator/SKILL.md) |
| L — **Character IP engine** | Episodic continuity for mascot/cast | `p-image` / `p-image-edit` + `p-video` / `p-video-avatar` | [character-ip-content-engine](../character-ip-content-engine/SKILL.md) |
| M — **Motion-transfer showcase** | Same motion, new subject + slider before/after | motion `.mp4` + still → `p-video-animate` → slider compare MP4 | [multi-scene-avatar-video](../core/avatar-multi-scene/SKILL.md) (`animate` rows) |
| N — **In-video replacement showcase** | Swap people/products in footage + slider before/after | dynamic `p-image` refs → optional `p-video-avatar` source → `p-video-replace` → slider compare MP4 | [p-video-replace-comparison](../launches/p-video-replace-comparison/SKILL.md) |
| O — **AI music video** | Full song + lyric-synced video | lyrics → [music-2.5](../../../../tools/audio/music-2.5/SKILL.md) → cut map → `p-video-avatar` + `p-video` → assembly; hero + `p-image-edit` when one singer throughout | [ai-music-video](../verticals/music-video/SKILL.md) |
| P — **Narrated story film** | Multi-scene B-roll + VO (+ optional bed) | hero → `p-image-edit` start/end stills → `p-video` with `image` + `last_frame_image` chain → [gemini-3.1-flash-tts](../../../../tools/audio/gemini-3.1-flash-tts/SKILL.md) → concat + mux ± [stable-audio-2.5](../../../../tools/audio/stable-audio-2.5/SKILL.md) | [multi-scene-ai-video](../core/narrated-multi-scene/SKILL.md) · [audio-post-production.md](../../../../references/audio/audio-post-production.md) |
| Q — **Visual transition reel** | Multi-scene motion between two stills per beat (no VO) | `p-image` hero → `p-image-edit` start/end stills → `p-video` pair (`duration`) → selective frame chain → concat | [scene-transition-video](../core/visual-transition-reel/SKILL.md) · [scene-anchor-pair.md](../../../../references/video/scene-anchor-pair.md) |
| R — **Educational explainer** | Narrator VO + expert/character dialogue | `p-image` hero → `p-image-edit` stills → **`narrator`** triple + **`character`** avatar → concat ± bed | [educational-explainer](../verticals/interactive-explainer/SKILL.md) · [educational-explainer-scenes.md](../../../../references/workflows/interactive-explainer-scenes.md) |

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

---

## Recipe A — Style-locked mood board (same-style stills)

**Shine:** One style bible + repeated aspect ratio + optional shared `seed` makes a grid feel art-directed, not random.

**Intake:** How many panels? One subject or variations on a theme? Output aspect (`1:1` grid vs `9:16`)?

**Steps**

1. Write the **style bible** once (palette, line, era, lens).
2. Run **`p-image`** N times with the bible in every `prompt`, same `aspect_ratio`; vary only the beat (emotion, prop, angle). **Start all N jobs in parallel** (async). Optionally fix `seed` for tighter series or vary seed for exploration.
3. If a panel drifts, **`p-image-edit`** that panel using the best prior panel as reference + “match reference style; change only: …”.
4. Optional **`p-image-upscale`** on selects for large boards or print.

**Refs:** [p-image](../../../../tools/image/p-image/SKILL.md), [p-image-edit](../../../../tools/image/p-image-edit/SKILL.md), [p-image-upscale](../../../../tools/image/p-image-upscale/SKILL.md)

## Recipe B — Hero frame + controlled variants

**Shine:** One approved hero URL becomes the identity anchor for every `p-image-edit`—fast packaging (backgrounds, seasons, formats) without re-hitting identity from scratch.

**Intake:** What must stay fixed (face, product silhouette)? What is allowed to change per variant?

**Steps**

1. **`p-image`** or upload → one **hero** URL.
2. **`p-image-edit`** per variant: hero in `images[]`, prompt lists only deltas (e.g. “night rain”, “summer market”, “studio white sweep”).
3. Optional **`p-image-upscale`** per hero use case.

## Recipe C — Upscale-first rescue → edit

**Shine:** Upscale cleans AI mush before you edit text or logos onto packaging mockups.

**Intake:** Target MP (1–128)? `enhance_details` vs `enhance_realism` (realism can drift)?

**Steps**

1. Upload source → **`p-image-upscale`** with conservative `enhance_realism` unless source is synthetic.
2. **`p-image-edit`** for copy-safe layout tweaks or background replacement.

## Recipe D — Still → cinematic motion (I2V)

**Shine:** Short camera grammar (“slow push-in”, “orbit left”, “hand lifts product”) matches what **p-video** does well from a single plate. Add **`last_frame_image`** when the beat has a known end composition (handoff to the next scene).

**Intake:** Camera move, duration, `draft` for storyboard pass? End still for frame chain?

**Steps**

1. Ensure still exists (upload or **`p-image`**).
2. Optional **`p-image-edit`** for end still when chaining scenes.
3. **`p-video`** with `image` + motion `prompt`; add `last_frame_image` for controlled arc. Follow [single-scene-ai-video](../core/image-to-video/SKILL.md) for full intake.

## Recipe E — Audio-conditioned `p-video` (single anchor)

**Shine:** Duration tracks audio automatically—ideal for VO-first social cuts.

**Intake:** Audio format? Visual story matching beats? Source: upload, [Gemini TTS](../../../../tools/audio/gemini-3.1-flash-tts/SKILL.md), or [Music 2.5](../../../../tools/audio/music-2.5/SKILL.md)?

**Steps**

1. Generate or upload audio → `/v1/files`.
2. **`p-video`** with `audio` + `prompt` (+ optional `image`, `last_frame_image`); omit `duration`.

For **full narrated story films**, use Recipe **P** ([scene anchor triple](../../../../references/video/scene-anchor-triple.md)) instead.

## Recipe F — Draft preview → locked final

**Shine:** Same prompt with `draft: true` burns cheap previews; rerun with `draft: false` once the client signs off.

**Intake:** Which beats need approval per scene? Lock list (prompt, seed, resolution) for finals.

**Steps**

1. **`p-video`** async with `draft: true` **for all scenes in parallel**; batch-poll until each preview is ready.
2. After approval, rerun with **`draft: false`** (and same `seed` if reproducibility matters).

## Recipe G — Talking-head (delegated workflows)

**Shine:** Slop-gated photoreal stills + locked seed + natural **`voice_script`** + human **`voice_prompt`** + per-scene dynamic **`video_prompt`** = scroll-stopping social avatar cuts without identity drift.

**Steps**

1. Build **character sheet** and **scene table** (distinct angle/setting per beat)—see [multi-scene-avatar-video](../core/avatar-multi-scene/SKILL.md).
2. Hero: **`p-image`** (photoreal, locked **`seed`**) → slop gate.
3. Per scene: **`p-image-edit`** (change only angle/background/emotion) → slop gate — **parallel across scenes** after hero anchor is approved.
4. Hand off to [single-scene-avatar-video](../core/avatar-single-scene/SKILL.md) or [multi-scene-avatar-video](../core/avatar-multi-scene/SKILL.md) for confirmation, then **`p-video-avatar`** in a **parallel batch** with shared **`seed`**, natural voice fields, and unique **`video_prompt`** per scene.

## Recipe H — Vertical social “stack”

**Shine:** 2–5 ultra-short **avatar-only** beats with **different settings and angles** per scene often outperform one long static talking-head for retention.

**Intake:** Per-clip message; distinct background/angle per slot; locked **`seed`**; natural **`voice_script`**.

**Steps**

1. Use [multi-scene-avatar-video](../core/avatar-multi-scene/SKILL.md) for all-`p-video-avatar` stacks (preferred for founder/partnership announcements), or mix with [multi-scene-ai-video](../core/narrated-multi-scene/SKILL.md) B-roll only when the user explicitly wants cutaways.
2. Assemble outside Pruna; normalize loudness between clips if mixing sources.

## Recipe M — Motion-transfer showcase (slider comparison)

**Shine:** Reuse winning motion templates with new subjects at scale; slider MP4s make before/after obvious in pitches and social.

**Intake:** Motion `.mp4` per beat; reference still per beat; alignment risks (pose, proportions, meme vs human); comparison + final reel deliverables.

**Steps**

1. Full workflow: [multi-scene-avatar-video](../core/avatar-multi-scene/SKILL.md) — scene table with **`animate`** rows, confirmation gate, parallel **`p-video-animate`**, slider renders, concat.
2. Optional **`p-image-edit`** to repose each still toward its motion keyframe before animate.
3. Render synced slider MP4s with [`generate_video_comparison.py`](../_shared/scripts/generate_video_comparison.py) (portable: `./scripts/generate_video_comparison.py` after `install_skill.sh`).

## Recipe N — In-video replacement showcase (slider comparison)

**Shine:** Swap **characters**, **outfits**, **products**, or **mixed** slots in existing footage without reshooting; slider MP4s show original vs replaced.

**Intake:** `replace_target` per row; `subject_in_video` + per-reference **`instruction_prompt`** (no generic mapping); prefer **`p-video-avatar`** sources (in-hand / desk props, single subject); default **`multi_job`**; natural avatar VO.

**Steps**

1. Full workflow: [p-video-replace-comparison](../launches/p-video-replace-comparison/SKILL.md) — production-tested 8-scene replace reel; confirmation gate; [`run_from_plan.py`](../launches/p-video-replace-comparison/scripts/run_from_plan.py) (default `--phase stills`).
2. **`p-image`** references matched to slot (face, person **wearing** outfit, hand/desk-scale packshot); **`p-image-edit`** as needed.
3. Source: **`p-video-avatar`** default (speaking, lip-safe camera); upload when licensed; avoid I2V shelf/walk/two-shot cafe for launch reels.
4. **`p-video-replace`**: **`multi_job`** (one ref + mapped prompt per slider step); `single_call` only for simple silent multi-slot clips.
5. Sliders via [`generate_video_comparison.py`](../_shared/scripts/generate_video_comparison.py); concat final reel.
6. Optional **light background music** — plan `background_music` or [`launch_background_music.py`](../_shared/scripts/launch_background_music.py) + [stable-audio-2.5](../../../../tools/audio/stable-audio-2.5/SKILL.md) (requires `REPLICATE_API_TOKEN`).

## Recipe P — Narrated story film (scene anchor triple)

**Shine:** **`image`** + **`last_frame_image`** + **`audio`** per scene — visual continuity **and** full narration sync; optional [Stable Audio](https://replicate.com/stability-ai/stable-audio-2.5) bed in post.

**Intake:** Scene table with start/end still prompts, narration lines, `frame_chain`, bed yes/no.

**Steps**

1. Full workflow: [multi-scene-ai-video](../core/narrated-multi-scene/SKILL.md) — see [scene-anchor-triple.md](../../../../references/video/scene-anchor-triple.md).
2. Hero → parallel **`p-image-edit`** start + end stills → parallel [Gemini TTS](../../../../tools/audio/gemini-3.1-flash-tts/SKILL.md) → **probe each MP3 (≤ ~19s)** → upload all → parallel **`p-video`** triple payloads (`input.audio` drives duration up to **20s** max; omit `duration`; `save_audio: true`).
3. Concat embedded VO → optional bed — [audio-post-production.md](../../../../references/audio/audio-post-production.md).

## Atomic tool index

| Model | Skill |
|-------|--------|
| `p-image` | [p-image](../../../../tools/image/p-image/SKILL.md) |
| `p-image-edit` | [p-image-edit](../../../../tools/image/p-image-edit/SKILL.md) |
| `p-image-upscale` | [p-image-upscale](../../../../tools/image/p-image-upscale/SKILL.md) |
| `p-video` | [p-video](../../../../tools/video/p-video/SKILL.md) |
| `p-video-avatar` | [p-video-avatar](../../../../tools/video/p-video-avatar/SKILL.md) |
| `p-video-animate` | [p-video-animate](../../../../tools/video/p-video-animate/SKILL.md) |
| `p-video-replace` | [p-video-replace](../../../../tools/video/p-video-replace/SKILL.md) |
| `stable-audio-2.5` (Replicate) | [stable-audio-2.5](../../../../tools/audio/stable-audio-2.5/SKILL.md) — launch reel bed under VO |
| `gemini-3.1-flash-tts` (Replicate) | [gemini-3.1-flash-tts](../../../../tools/audio/gemini-3.1-flash-tts/SKILL.md) — narration / voiceover |
| `music-2.5` (Replicate) | [music-2.5](../../../../tools/audio/music-2.5/SKILL.md) — full songs with vocals |

Audio layering guide: [audio-post-production.md](../../../../references/audio/audio-post-production.md) · Scene anchor triple: [scene-anchor-triple.md](../../../../references/video/scene-anchor-triple.md)

## More ideas (map to recipes)

| Idea from product positioning | Map |
|--------------------------------|-----|
| Fast catalog / packshots | **B** + optional **C** |
| “Same character, six posts” | **A** or **G** |
| Lip-sync spokesperson | **G** |
| “Animate this poster” | **D** |
| VO-driven ad | **E** |
| Client approval workflow | **F** |
| UGC hook testing at scale | **I** |
| Product mini-story reels | **J** |
| Full SKU creative kit | **K** |
| Episodic mascot channel | **L** |
| Motion swap / recast demo reel | **M** |
| Replace cast or products in existing footage | **N** |
| Narrated multi-scene story (scene anchor triple) | **P** |

If a use case is not covered, define a new row: **intake → ordered models → handoff URLs**—same pattern as above.
