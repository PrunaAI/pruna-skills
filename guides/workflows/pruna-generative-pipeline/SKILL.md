---
name: pruna-generative-pipeline
description: Scenario hub for Pruna P-API chains—intake in plain language, natural-language scripts where there is VO or narration, optional cast ledger (one voice per recurring character), hero/source reuse via p-image-edit for continuity, mandatory explicit user confirmation before any POST /v1/predictions, then emit and run a concrete generation script or curl sequence. Links avatar and multi-scene workflows when recipes need them.
license: MIT
---

# Pruna generative pipeline (scenario hub)

This skill is the **menu of proven chains** over the atomic tools in `tools/image` and `tools/video`. For HTTP details see [references/pruna-api.md](../../../references/pruna-api.md).

Marketing and demo sites change layout and messaging often; **this repo is the source of truth** for what agents should run. When humans find a compelling flow elsewhere, **encode it here** (extend a recipe, add a row to the idea map, or add a dedicated workflow skill) after checking it against [docs.api.pruna.ai](https://docs.api.pruna.ai/guides/models)—do not send agents to browse live demos as part of execution.

**Tone:** Explain plans to the user like a producer—clear scene order, what generates first, and what they should hear or see—especially whenever **`voice_script`** or narration exists. Avoid stiff jargon in client-facing script drafts unless they ask for it.

## Intake: pick a scenario first

Ask the user which **recipe** fits (or hybrid). Capture answers before any `POST /v1/predictions`:

| Topic | Questions |
|-------|-----------|
| **Recipe** | Which row in the routing table below (or combination)? |
| **Deliverable** | Stills only, video clip(s), avatars, or mixed? |
| **Aspect / resolution** | e.g. `9:16` vs `16:9`; `720p`/`1080p` for video; draft vs final? |
| **References** | Files to upload to `/v1/files` (URLs only in predictions)? |
| **Style lock** | One **style bible** sentence reused on every prompt when consistency matters? |
| **Voice / cast** | For talking heads or recurring speakers: **one Pruna `voice` per character** across scenes; natural-language **`voice_script`** drafts as needed. |
| **Scenes** | If multiple clips: one-line intent each (or defer to [multi-scene-ai-video](../multi-scene-ai-video/SKILL.md) / [multi-scene-avatar-video](../multi-scene-avatar-video/SKILL.md))? |

## Confirmation and execution (all recipes)

1. **Draft** any scripts, beats, or prompts that the user must approve in **natural, human language** (spoken wording for VO; clear intent per scene otherwise).
2. **Pause** and obtain **explicit confirmation** (“approve”, “go”, “run it”) before the first upload or **`POST /v1/predictions`**. If the user revises copy or cast, re-confirm when the change matters for cost or outcome.
3. **Write** a **runnable generation package**—script or ordered API steps—that matches the approved plan **exactly**.
4. **Execute** that package when possible (**`PRUNA_API_KEY`**, network). If execution is not possible here, deliver the same artifact for local runs.

Deep avatar workflows already spell out cast ledgers, hero reuse, and read-throughs in [multi-scene-avatar-video](../multi-scene-avatar-video/SKILL.md) and [single-scene-avatar-video](../single-scene-avatar-video/SKILL.md); defer to those when recipe **G** or **H** involves **`p-video-avatar`**.

## Routing table

| Recipe | You get | Primary models | Deep workflow (if any) |
|--------|---------|----------------|-------------------------|
| A — **Style-locked mood board** | N stills, same world | `p-image` → optional `p-image-edit` | Stay in this skill |
| B — **Hero + variants** | One anchor + edits | `p-image` → `p-image-edit` | — |
| C — **Print / pixel rescue** | Higher-res master | `p-image-upscale` → optional `p-image-edit` | — |
| D — **Animate a plate** | One motion clip from a still | `p-image` or upload → `p-video` (I2V) | [single-scene-ai-video](../single-scene-ai-video/SKILL.md) |
| E — **Audio-led cut** | Video length follows VO/music | upload `audio` → `p-video` | [single-scene-ai-video](../single-scene-ai-video/SKILL.md) |
| F — **Draft → final video** | Cheap preview then hi-fi | `p-video` (`draft: true`) then rerun `draft: false` with locked `seed`/prompt | [multi-scene-ai-video](../multi-scene-ai-video/SKILL.md) for many beats |
| G — **Talking head** | Portrait + speech | `p-image` / `p-image-edit` → `p-video-avatar` | [single-scene-avatar-video](../single-scene-avatar-video/SKILL.md) or [multi-scene-avatar-video](../multi-scene-avatar-video/SKILL.md) |
| H — **Social hook stack** | Short vertical beats | Several `p-video` and/or avatars | Multi-scene skills above |
| I — **UGC ad factory** | Batch hook/offer/CTA avatar ads | `p-image` / `p-image-edit` → `p-video-avatar` | [ugc-ad-factory](../ugc-ad-factory/SKILL.md) |
| J — **Product-to-story reel** | 4-6 beat narrative product reel | `p-image-edit` → `p-video` | [product-to-story-reel-builder](../product-to-story-reel-builder/SKILL.md) |
| K — **Ecommerce creative pack** | Packshots + lifestyle + motion loop | `p-image-edit` → optional `p-image-upscale` / `p-video` | [ecommerce-creative-pack-generator](../ecommerce-creative-pack-generator/SKILL.md) |
| L — **Character IP engine** | Episodic continuity for mascot/cast | `p-image` / `p-image-edit` + `p-video` / `p-video-avatar` | [character-ip-content-engine](../character-ip-content-engine/SKILL.md) |

## Handoff rules (all recipes)

- Use **Pruna file URLs** only (`POST /v1/files` → `urls.get`) in `images`, `image`, `audio`.
- Prefer **async** for `p-video` and `p-video-avatar`; poll until `succeeded`.
- **Do not** chain the next step until the previous URL is valid and (for portraits) checklist-approved when using recipe **G**.
- **Character continuity:** One **approved source / hero** URL per recurring subject; branch new looks and styles with **`p-image-edit`** from that URL (plus style bible), not unrelated fresh **`p-image`** identity pulls—unless the user resets the character.
- **Same voice for the same role:** When a character speaks in more than one clip, keep **`voice`** (and usually **`voice_language`**) identical across those clips.

---

## Recipe A — Style-locked mood board (same-style stills)

**Shine:** One style bible + repeated aspect ratio + optional shared `seed` makes a grid feel art-directed, not random.

**Intake:** How many panels? One subject or variations on a theme? Output aspect (`1:1` grid vs `9:16`)?

**Steps**

1. Write the **style bible** once (palette, line, era, lens).
2. Run **`p-image`** N times with the bible in every `prompt`, same `aspect_ratio`; vary only the beat (emotion, prop, angle). Optionally fix `seed` for tighter series or vary seed for exploration.
3. If a panel drifts, **`p-image-edit`** that panel using the best prior panel as reference + “match reference style; change only: …”.
4. Optional **`p-image-upscale`** on selects for large boards or print.

**Refs:** [p-image](../../../tools/image/p-image/SKILL.md), [p-image-edit](../../../tools/image/p-image-edit/SKILL.md), [p-image-upscale](../../../tools/image/p-image-upscale/SKILL.md)

## Recipe B — Hero frame + controlled variants

**Shine:** One approved hero URL becomes the identity anchor for every `p-image-edit`—fast packaging (backgrounds, seasons, formats) without re-hitting identity from scratch.

**Intake:** What must stay fixed (face, product silhouette)? What is allowed to change per variant?

**Steps**

1. **`p-image`** or upload → one **hero** URL.
2. **`p-image-edit`** per variant: hero in `images[]`, prompt lists only deltas (e.g. “night rain”, “summer market”, “studio white sweep”).
3. Optional **`p-image-upscale`** per hero use case.

## Recipe C — Upscale-first rescue → edit

**Shine:** Upscale cleans AI mush before you edit text or logos onto packaging mockups.

**Intake:** Target MP (1–8)? `enhance_details` vs `enhance_realism` (realism can drift)?

**Steps**

1. Upload low-res → **`p-image-upscale`** with conservative `enhance_realism` unless source is synthetic.
2. **`p-image-edit`** for copy-safe layout tweaks or background replacement.

## Recipe D — Still → cinematic motion (I2V)

**Shine:** Short camera grammar (“slow push-in”, “orbit left”, “hand lifts product”) matches what **p-video** does well from a single plate.

**Intake:** Camera move, duration, `draft` for storyboard pass?

**Steps**

1. Ensure still exists (upload or **`p-image`**).
2. **`p-video`** with `image` URL + motion-only `prompt`. Follow [single-scene-ai-video](../single-scene-ai-video/SKILL.md) for full intake.

## Recipe E — Audio-conditioned `p-video`

**Shine:** Duration tracks audio automatically—ideal for VO-first social cuts.

**Intake:** Audio format (flac/mp3/wav)? Visual story that matches beats?

**Steps**

1. Upload audio → `/v1/files`.
2. **`p-video`** with `audio` + `prompt`; omit manual `duration` (ignored when audio is set per model docs).

## Recipe F — Draft preview → locked final

**Shine:** Same prompt with `draft: true` burns cheap previews; rerun with `draft: false` once the client signs off.

**Intake:** Which beats need approval per scene? Lock list (prompt, seed, resolution) for finals.

**Steps**

1. **`p-video`** async with `draft: true` per scene.
2. After approval, rerun with **`draft: false`** (and same `seed` if reproducibility matters).

## Recipe G — Talking-head (delegated workflows)

**Shine:** Slop-gated stills + Pruna TTS = predictable lip sync without external speech APIs.

**Steps**

1. Build stills with **`p-image` / `p-image-edit`** from a **locked source hero per character**; run the [generation quality checklist hub](../../../references/generation-quality-checklists.md) before **`p-video-avatar`**.
2. Hand off to [single-scene-avatar-video](../single-scene-avatar-video/SKILL.md) or [multi-scene-avatar-video](../multi-scene-avatar-video/SKILL.md) for **natural-language scripts**, **cast ledger** (one **`voice`** per recurring speaker), **confirmation**, then runnable automation or curls—those skills own **`voice_script`** wording and API timing.

## Recipe H — Vertical social “stack”

**Shine:** 2–4 ultra-short clips (hook → product → CTA) often outperform one long render for retention.

**Intake:** Per-clip message; T2V vs avatar per slot?

**Steps**

1. Use [multi-scene-ai-video](../multi-scene-ai-video/SKILL.md) for all-`p-video` stacks, or mix avatar clips via [multi-scene-avatar-video](../multi-scene-avatar-video/SKILL.md).
2. Assemble outside Pruna; normalize loudness between clips if mixing sources.

## Atomic tool index

| Model | Skill |
|-------|--------|
| `p-image` | [p-image](../../../tools/image/p-image/SKILL.md) |
| `p-image-edit` | [p-image-edit](../../../tools/image/p-image-edit/SKILL.md) |
| `p-image-upscale` | [p-image-upscale](../../../tools/image/p-image-upscale/SKILL.md) |
| `p-video` | [p-video](../../../tools/video/p-video/SKILL.md) |
| `p-video-avatar` | [p-video-avatar](../../../tools/video/p-video-avatar/SKILL.md) |

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

If a use case is not covered, define a new row: **intake → ordered models → handoff URLs**—same pattern as above.
