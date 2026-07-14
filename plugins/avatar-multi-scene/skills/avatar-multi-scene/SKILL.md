---
name: avatar-multi-scene
description: Use when the user needs multiple talking-head segments, motion-transfer comparison reels, mixed host and animate clips, or multi-scene UGC with character continuity.
license: MIT
metadata:
  version: "0.0.2"
depends:
  - p-image
  - p-image-edit
  - p-video-avatar
  - p-video-animate
---

# Multi-scene avatar & motion-transfer video (Pruna only)

## Purpose

Produce a **coherent multi-scene** piece stitched later in **your own editor or pipeline** (Pruna does not ship a concat endpoint in this skill set). Each beat is one of:

| Beat type | Model | Deliverable |
|-----------|--------|-------------|
| **`avatar`** | **`p-video-avatar`** | Talking-head clip from approved still + `voice_script` |
| **`animate`** | **`p-video-animate`** + slider render | Motion-transfer clip, usually wrapped in a **left → right slider comparison** MP4 (motion template vs animated subject) |

Mix types in one announcement reel—e.g. avatar hook → animate slider demo → avatar CTA (same pattern as the Pruna × Tellers cut, with optional **`animate`** beats between speaking scenes).

Visual continuity comes from **Pruna `p-image` / `p-image-edit`** on uploaded references—not from other vendors’ image APIs.

Follow this skill in **plain language** when talking to the person requesting the video: explain cast, voices, motion templates, and scene order the way you would in a production meeting. Use **natural, speakable copy** in every `voice_script`.

**Staged generation:** [staged-generation-gate.md](./references/staged-generation-gate.md) · [workflow-feedback-gates.md](./references/workflow-feedback-gates.md)

## Quick reference

| Resource | Path |
|----------|------|
| Photoreal dynamic personas | [realistic-persona-showcase.md](https://github.com/PrunaAI/pruna-skills/tree/main/references/shared/realistic-persona-showcase.md) |
| Cast ledger, character sheet, voice/video prompts | [prompt-templates.md](./prompt-templates.md) |
| Animate rows, sliders, alignment | [animate-beats.md](./animate-beats.md) |
| Examples | [examples.md](./examples.md) |
| Feedback discipline | [requesting-generation-feedback](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/requesting-generation-feedback/skills/requesting-generation-feedback/SKILL.md) |
| Slider script | [`generate_video_comparison.py`](./scripts/generate_video_comparison.py) |

## Feedback gates (required)

| Phase | What to show | Proceed when |
|-------|--------------|--------------|
| **0 — Plan** | Scene table, read-through, cast ledger | **approve plan** |
| **A — Stills** | Hero + per-scene plates | **approve stills** |
| **B — Video** | Avatar / animate clips + sliders | **approve clips** |
| **C — Assembly** | Concat reel + optional bed | User accepts |

## Intake: ask before generating

**Do not** call `POST /v1/predictions` until the user has answered and you have recorded the answers (use defaults only if the user explicitly opts in):

| Topic | Questions |
|-------|-----------|
| **Goal** | What is the piece for (pitch, tutorial, trailer, episode)? Primary audience? |
| **Scope** | How many speaking scenes or beats? Approximate total runtime after assembly? |
| **Cast** | Who speaks, in what order? One character throughout or multiple? |
| **Look** | Aspect for stills and feel (`9:16` / `16:9`)? Avatar output `720p` or `1080p`? |
| **Voice** | For **each named character**, pick **one** Pruna `voice` and `voice_language` and **reuse it in every scene** that character speaks. Any words that must be pronounced exactly (names, acronyms)? |
| **Style** | Agreed **style bible** line for all image prompts? |
| **Character sheet** | Per speaker: age range, wardrobe baseline, hair, skin/realism level, personality adjectives—record before hero generation (see **Character sheet** below). |
| **Scene variety** | Each scene must differ in **camera angle**, **background/setting**, and/or **energy**—no two consecutive scenes with the same framing and location unless the user asks. Plan **`visual_style_tag`**, **`setting_tag`**, **`camera_tag`**, **`lighting_tag`** per row; cast diversity (gender, age, ethnicity) on launch reels — [visual-variety-bible.md](./references/visual-variety-bible.md). |
| **Ritual seed (SSoT)** | **[Random seed ritual](https://github.com/PrunaAI/pruna-skills/tree/main/references/shared/random-seed-ritual.md)** at hero — generate and state a ritual string; log as **`ritual_seed`**; derive prompt axes via sum-mod. **Do not** pass ritual string to API `seed`. |
| **References** | Which files to upload; rights cleared? |
| **Beat mix** | Which scenes are **`avatar`** vs **`animate`**? All avatar, all animate, or mixed announcement? |
| **Narrated B-roll cutaways** | Optional **`p-video`** beats using [scene anchor triple](https://github.com/PrunaAI/pruna-skills/tree/main/references/shared/scene-anchor-triple.md) alongside avatar rows |
| **Motion templates** (animate beats) | Source `.mp4` per animate row—owned/licensed? Match pose/framing to reference still? |
| **Slider delivery** (animate beats) | Comparison MP4 only, animated-only strip, or both? Canvas default 1920×1080. |
| **Assembly** | How clips will be joined and leveled (tool-agnostic plan)? |

If anything material is unknown, **ask** before the first upload or prediction.

## Cast ledger & character sheet

Maintain a **cast table** in the manifest: one Pruna **`voice`** + **`voice_language`** per recurring character — **never** swap presets mid-story unless the user requests a recast.

Before hero generation, fill a **character sheet** per speaker (age, face, realism, wardrobe baseline, personality, **`ritual_seed`** for planning). Templates and manifest JSON: **[prompt-templates.md](./prompt-templates.md)**.

**Rule:** New locations and styles = **`p-image-edit`** off the approved hero URL — not unrelated fresh **`p-image`** identity pulls.

## Scene plan (dynamic beats)

Every piece needs a **scene table** — each row **`avatar`** or **`animate`**. Example columns and manifest JSON: **[prompt-templates.md](./prompt-templates.md)** · **[animate-beats.md](./animate-beats.md)**.

### Motion-transfer alignment (animate beats)

**P-Video-Animate** animates a reference image using motion, timing, and camera movement from a source video. The better the subject's **features, pose, framing, and proportions** align with the motion template, the better the result.

| Alignment | Typical outcome |
|-----------|-----------------|
| Same shot type, similar pose, similar scale | Clean motion transfer; slider demo reads instantly |
| Same character type, slightly different angle | Good with optional **`p-image-edit`** repose toward a template keyframe |
| Meme / cartoon / mascot on **human full-body** motion | Limbs, gait, and contact points may warp or slide |
| Tiny head / extreme proportions on **dance or arm-heavy** motion | Hands, legs, and depth cues often break |
| Reference facing camera, source subject in profile | Shoulder/head turn and occlusion artifacts |

**Rule:** Treat severe pose or proportion mismatch as a **pre-flight risk**. Repose with **`p-image-edit`** or pick a closer motion template before burning **`p-video-animate`** credits.

**Alignment prep (per animate row):**

1. Match **shot size** and **facing direction** between still and template.
2. Match **limb visibility**—if the template waves arms, the still must show arms.
3. **Repose when close but not exact** — **`p-image-edit`** from the hero anchor: *"Change only: match pose and camera to reference video frame; keep identity and outfit."*
4. Run [p-video-animate-quality-checklist.md](./references/p-video-animate-quality-checklist.md) on the pair before animate.

**Anti-patterns (all types):** two identical office avatar scenes back-to-back; corporate brochure **`voice_script`**; human dance template + chibi meme still without repose; serial API jobs when scenes are independent; **motion templates that prompt smile/wave only** (avatar stays silent — see **Motion templates for animate beats** below).

### Motion templates for animate beats

When **`p-video-avatar`** generates a **motion template** (source video for **`p-video-animate`**), treat it as a speaking beat — not a portrait pose.

| Field | Requirement |
|-------|-------------|
| Motion-source **`still_edit`** | `mouth clearly visible ready to speak` — not passive smile only |
| **`video_prompt`** | `speaks directly to camera`, `clear lip movement`, explain gestures, head nods — **before** any wave/smile close |
| **`voice_prompt`** | Delivery throughout the line — not “wave energy at the end” only |
| Camera | Prefix: `Camera moves continuously for the full clip — … never locked-off` |

Silent motion templates break slider demos and animate transfers. Prompt templates: [prompt-templates.md](./prompt-templates.md). Full animate pipeline: [animate-beats.md](./animate-beats.md).

### Mixed reels with animate rows

Combine **`avatar`** talking-head beats and **`animate`** slider demos in one scene table. Common patterns:

| Pattern | Structure |
|---------|-----------|
| Interleaved | avatar hook → animate demo → avatar proof → animate demo → avatar CTA |
| Slider-heavy | N **`animate`** slider rows → final **`avatar`** CTA on hero |

End product launches with a speakable **`avatar`** CTA unless the user opts out. See [animate-beats.md](./animate-beats.md) for model roles, alignment, and slider assembly.

## Identity & ritual seed policy

Must complete **[random seed ritual](https://github.com/PrunaAI/pruna-skills/tree/main/references/shared/random-seed-ritual.md) (SSoT)** before hero prompt work. Log **`ritual_seed`** in manifest; reuse only on same-brief slop retry.

Character continuity = **approved hero plate URL** + cast descriptor — not API `seed`. Pass **`api_seed`** in `input` only when the user explicitly locks reproducibility.

## Natural voice (mandatory for avatar social / founder content)

**`voice_script`** = speakable dialogue (contractions, short breaths). **`voice_prompt`** = performance direction only — never marketing copy or script text.

Good/bad pairs, per-scene **`video_prompt`** patterns, and shared cast voice line: **[prompt-templates.md](./prompt-templates.md)**.

## Source portrait / hero (same character across styles and scenes)

For **each** recurring character:

1. Land **one** approved **source** still via **`p-image`** (photoreal prompt + locked **`seed`**) or upload. Run the slop gate on the hero before sign-off. Treat the approved file URL as the **identity anchor**.
2. **Every** later look—including a new background, emotion, prop, or **style variation** (e.g. “same cat, but ink-line instead of pencil”)—should be produced with **`p-image-edit`** from **that same source URL**, plus the shared style bible and a short delta (“change only: …”). Do **not** mint a fresh identity with unrelated `p-image` text prompts mid-run unless the user resets the character.
3. **Each new scene** still starts from the same character source as step 2 so faces stay one continuous role across the arc.

This keeps later scene opens and style experiments aligned with the **same** underlying portrait the user signed off on.

## Confirmation gate (mandatory)

After intake is complete and you have drafted work in **natural human language**:

1. Present a **read-through package**: scene order and **type** per row; full **`voice_script`** for avatar rows; motion templates + reference stills + **alignment risks** for animate rows; cast ledger; hero URL(s); chosen **`resolution`**; legal/CTA lines **verbatim** if supplied.
2. Ask clearly for approval (e.g. “Reply **approve** or **go** when this script and cast are final.”).
3. **Do not** upload binaries for generation, call **`POST /v1/predictions`**, or run automation until the user **explicitly confirms**.

Optional edits after feedback; repeat confirmation if the script or cast changes materially.

## Script and run package (after confirmation)

Once the user confirms:

1. **Write** a concrete **generation package**: phased **`curl`** steps or a small script that performs uploads, **`p-image`** / **`p-image-edit`**, parallel **`p-video-avatar`** (avatar rows), parallel **`p-video-animate`** (animate rows), **`generate_video_comparison.py`** slider renders (animate rows), and downloads—matching the approved scene table **exactly**. **Parallelize** independent lanes within each phase ([parallel-execution.md](./references/parallel-execution.md)).
2. **Execute** that package when execution is possible (`PRUNA_API_KEY` present, network available). Prefer **one subagent per scene lane** (still pipeline: edit → gate; or avatar: create → poll → download) launched in parallel after the hero anchor exists. Parent agent owns confirmation, manifest merge, and assembly. If the environment cannot call the API, hand the user the same script and exact commands so they can run it locally without guesswork.

The script is the contract: what runs must match what was approved.

## Core rules

1. **`p-video-avatar` `input.image`** — use an approved still URL from `/v1/files` (upload, **`p-image`**, or **`p-image-edit`** output) that passed [generation-quality-checklists.md](./references/generation-quality-checklists.md).
2. Run the **slop gate** on every hero and scene still **before** any avatar job.

```text
Hero:     p-image (or upload) → slop gate → approve anchor
Scene N:  p-image-edit(anchor) → slop gate → p-video-avatar
```

Use the **approved hero** as the reference for **`p-image-edit`**, not a rejected intermediate.

## API surface (this workflow)

| Step | Model | Skill |
|------|--------|--------|
| Upload binaries | `POST /v1/files` | [pruna-api.md](./references/pruna-api.md) |
| Style-locked stills | `p-image`, `p-image-edit` | [p-image](../../../../tools/image/p-image/SKILL.md), [p-image-edit](../../../../tools/image/p-image-edit/SKILL.md) |
| Talking clips | `p-video-avatar` | [p-video-avatar](../../../../tools/video/p-video-avatar/SKILL.md) |
| Motion transfer | **`p-video-animate`** | [p-video-animate](../../../../tools/video/p-video-animate/SKILL.md) |
| Slider comparison (animate rows) | [`generate_video_comparison.py`](./scripts/generate_video_comparison.py) | local; install via `npx skills add PrunaAI/pruna-skills/plugins/avatar-multi-scene/skills --skill avatar-multi-scene --agent cursor -y` |

Use **`PRUNA_API_KEY`** and the **`apikey`** header on every call. **Async + parallel by default**: batch all avatar jobs once approved stills pass slop; batch all animate jobs once motion + still URLs are ready; poll all `get_url` together. See [parallel-execution.md](./references/parallel-execution.md).

## Parallel execution & subagents

After the **confirmation gate** and **hero anchor** are locked:

| Phase | Parallel? | Subagent split |
|-------|-----------|----------------|
| Hero `p-image` → gate | Sequential | No — identity anchor |
| Per-scene `p-image-edit` | **Yes** — all scenes | One subagent per scene still lane |
| Slop gate | **Yes** — review in parallel | Parent or per-lane subagent |
| `p-video-avatar` | **Yes** — all avatar rows | One subagent per clip (create + poll + download) |
| `p-video-animate` | **Yes** — all animate rows | One subagent per clip (create + poll + download) |
| Slider render | **Yes** — all animate rows | One subagent per comparison MP4 |
| Assembly | Sequential order only | Parent agent |

**Rule:** Never dispatch subagents before user confirmation. Parent merges all lane outputs into one manifest.

## Workflow

| Step | Action |
|------|--------|
| 1–3 | Intake → speakable script → **confirmation gate** (no API until approve) |
| 4–5 | Upload refs → **`p-image` hero** per character (locked `seed`) → slop gate |
| 6–7 | Parallel **`p-image-edit`** scene stills → slop gate each |
| 8 | Parallel **`p-video-avatar`** (cast ledger voices, unique `video_prompt` per scene) |
| 9 | Parallel **`p-video-animate`** + slider renders — [animate-beats.md](./animate-beats.md) |
| 10 | ffmpeg concat ± optional bed — [stable-audio-2.5](../../../../tools/audio/stable-audio-2.5/SKILL.md) |
| 11 | Manifest: paths, prediction ids, slop notes, cast snapshot |

Field names and curl shapes: **[prompt-templates.md](./prompt-templates.md)** · [p-video-avatar](../../../../tools/video/p-video-avatar/SKILL.md).

## References

- [generation-quality-checklists.md](./references/generation-quality-checklists.md)
- [prompt-templates.md](./prompt-templates.md) — cast ledger, character sheet, voice/video templates
- [animate-beats.md](./animate-beats.md) — `p-video-animate`, motion templates, sliders
- [requesting-generation-feedback](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/requesting-generation-feedback/skills/requesting-generation-feedback/SKILL.md)
- [examples.md](./examples.md)

## Related

- Pruna-only pipeline overview: [pruna-generative-pipeline](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/pruna-generative-pipeline/skills/pruna-generative-pipeline/SKILL.md)
- One-scene avatar: [avatar-single-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/avatar-single-scene/skills/avatar-single-scene/SKILL.md)
- Cinematic B-roll (non-avatar): [image-to-video](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/image-to-video/skills/image-to-video/SKILL.md), [narrated-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/narrated-multi-scene/skills/narrated-multi-scene/SKILL.md)
- Still upscale slider demos: [p-image-upscale-comparison](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/p-image-upscale-comparison/skills/p-image-upscale-comparison/SKILL.md)
- Motion transfer tool: [p-video-animate](../../../../tools/video/p-video-animate/SKILL.md)
