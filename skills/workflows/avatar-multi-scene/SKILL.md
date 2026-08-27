---
name: avatar-multi-scene
description: Use when someone wants the same person hosting several clips — multi-segment UGC, comparison reels, or mixed speaking and animated scenes with continuity.
license: MIT
metadata:
  version: "1.0.10"
  package: pruna-skills
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## Workflow habit

In **every reply**, name `` `avatar-multi-scene` `` in backticks. Restate the user's **continuity / UGC / host / segment** goal in one line. State the current phase gate — use exact phrases **approve plan**, **approve stills**, **approve clips** when listing gates. Do **not** same-turn plan + paid video. Skip-review / burn-credits → follow `generation-diversity` **Red flags**.

## Purpose

Produce a **coherent multi-scene** piece stitched later with **ffmpeg** (Pruna does not ship a concat endpoint). Each beat is one of:

| Beat type | Model | Deliverable |
|-----------|--------|-------------|
| **`avatar`** | **`p-video-avatar`** | Talking-head clip from approved still + `voice_script` |
| **`animate`** | **`p-video-animate`** + slider render | Motion-transfer clip, usually wrapped in a **side-by-side or wipe comparison** MP4 (motion template vs animated subject) |

Mix types in one announcement reel—e.g. avatar hook → animate slider demo → avatar CTA.

Visual continuity comes from **Pruna `p-image` / `p-image-edit`** on uploaded references.

Follow this skill in **plain language** when talking to the person requesting the video. Use **natural, speakable copy** in every `voice_script`.

**Staged generation:** `generation-diversity` · `generation-diversity`

## Quick reference

| Resource | Path |
|----------|------|
| Photoreal dynamic personas | `image-prompting` |
| Cast ledger, character sheet, voice/video prompts | [prompt-templates.md](./prompt-templates.md) |
| Animate rows, sliders, alignment | [animate-beats.md](./animate-beats.md) |
| Examples | [examples.md](./examples.md) |
| Feedback discipline | `generation-diversity` |
| Slider (agent) | ffmpeg `hstack` / wipe — see **Slider comparison** below |
| Batch template | [templates/batch.template.json](./templates/batch.template.json) |

## Feedback gates (required)

| Phase | What to show | Proceed when |
|-------|--------------|--------------|
| **0 — Plan** | Scene table, read-through, cast ledger | **approve plan** |
| **A — Stills** | Hero + per-scene plates | **approve stills** |
| **B — Video** | Avatar / animate clips + sliders | **approve clips** |
| **C — Assembly** | Concat reel + optional bed | User accepts |

## Intake: ask before generating

Open intake → **`generation-diversity`** clarification intake.

**Do not** call `POST /v1/predictions` until the user has answered and you have recorded the answers (use defaults only if the user explicitly opts in):

| Topic | Questions |
|-------|-----------|
| **Goal** | What is the piece for (pitch, tutorial, trailer, episode)? Primary audience? |
| **Scope** | How many speaking scenes or beats? Approximate total runtime after assembly? |
| **Cast** | Who speaks, in what order? One character throughout or multiple? |
| **Look** | Aspect for stills and feel (`9:16` / `16:9`)? Avatar output `720p` or `1080p`? |
| **Media source** | **Generate** hero plates with `p-image` / edits vs **upload-only** references; user-owned motion templates for animate beats? |
| **Voice** | For **each named character**, pick **one** Pruna `voice` and `voice_language` and **reuse it in every scene** that character speaks. Any words that must be pronounced exactly (names, acronyms)? |
| **Style** | Agreed **style bible** line for all image prompts? |
| **Character sheet** | Per speaker: age range, wardrobe baseline, hair, skin/realism level, personality adjectives—record before hero generation (see **Character sheet** below). |
| **Scene variety** | Each scene must differ in **camera angle**, **background/setting**, and/or **energy**—no two consecutive scenes with the same framing and location unless the user asks. Plan **`visual_style_tag`**, **`setting_tag`**, **`camera_tag`**, **`lighting_tag`** per row — `generation-diversity`. |
| **Ritual seed (SSoT)** | Ritual seed at hero — generate and state a ritual string; log as **`ritual_seed`**; derive prompt axes via sum-mod. **Do not** pass ritual string to API `seed`. |
| **References** | Which files to upload; rights cleared? |
| **Beat mix** | Which scenes are **`avatar`** vs **`animate`**? All avatar, all animate, or mixed announcement? |
| **Narrated B-roll cutaways** | Optional **`p-video`** beats using scene-anchor triple (`video-prompting`) alongside avatar rows |
| **Motion templates** (animate beats) | Source `.mp4` per animate row—owned/licensed? Match pose/framing to reference still? |
| **Slider delivery** (animate beats) | Comparison MP4 only, animated-only strip, or both? Canvas default 1920×1080. |
| **Assembly** | How clips will be joined and leveled (ffmpeg plan)? |

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
4. Run animate QA from `video-prompting` on the pair before animate.

**Anti-patterns (all types):** two identical office avatar scenes back-to-back; corporate brochure **`voice_script`**; human dance template + chibi meme still without repose; serial API jobs when scenes are independent; **motion templates that prompt smile/wave only** (avatar stays silent — see below).

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

| Pattern | Structure |
|---------|-----------|
| Interleaved | avatar hook → animate demo → avatar proof → animate demo → avatar CTA |
| Slider-heavy | N **`animate`** slider rows → final **`avatar`** CTA on hero |

End product launches with a speakable **`avatar`** CTA unless the user opts out.

## Identity & ritual seed policy

Complete the ritual seed step in `generation-diversity` before hero prompt work. Log **`ritual_seed`** in manifest; reuse only on same-brief slop retry.

Character continuity = **approved hero plate URL** + cast descriptor — not API `seed`. Pass **`api_seed`** in `input` only when the user explicitly locks reproducibility.

## Natural voice (mandatory for avatar social / founder content)

**`voice_script`** = speakable dialogue (contractions, short breaths). **`voice_prompt`** = performance direction only — never marketing copy or script text.

Good/bad pairs: **[prompt-templates.md](./prompt-templates.md)**.

## Source portrait / hero (same character across styles and scenes)

For **each** recurring character:

1. Land **one** approved **source** still via **`p-image`** or upload. Run the slop gate on the hero before sign-off. Treat the approved file URL as the **identity anchor**.
2. **Every** later look—including a new background, emotion, prop, or **style variation**—should be produced with **`p-image-edit`** from **that same source URL**, plus the shared style bible and a short delta (“change only: …”).
3. **Each new scene** still starts from the same character source so faces stay one continuous role across the arc.

## Confirmation gate (mandatory)

After intake is complete:

1. Present a **read-through package**: scene order and **type** per row; full **`voice_script`** for avatar rows; motion templates + reference stills + **alignment risks** for animate rows; cast ledger; hero URL(s); chosen **`resolution`**; legal/CTA lines **verbatim** if supplied.
2. Ask clearly for approval (e.g. “Reply **approve** or **go** when this script and cast are final.”).
3. **Do not** upload binaries for generation or call **`POST /v1/predictions`** until the user **explicitly confirms**.

## How the agent runs this

Once the user confirms:

1. Upload refs → hero `p-image` → parallel per-scene `p-image-edit` → slop gates → **approve stills**.
2. Parallel **`p-video-avatar`** (avatar rows) and **`p-video-animate`** (animate rows) via curl batches (`pruna-api`).
3. For each animate row, build a **slider / comparison** MP4 with ffmpeg (below).
4. ffmpeg concat in scene order → optional bed → **approve** final.

Prefer one parallel lane per independent scene after the hero exists. Parent owns confirmation, manifest merge, and assembly.

## Core rules

1. **`p-video-avatar` `input.image`** — use an approved still URL from `/v1/files` that passed `generation-diversity` checklists.
2. Run the **slop gate** on every hero and scene still **before** any avatar job.

```text
Hero:     p-image (or upload) → slop gate → approve anchor
Scene N:  p-image-edit(anchor) → slop gate → p-video-avatar
```

## API surface (this workflow)

| Step | Model | Skill |
|------|--------|--------|
| Upload binaries | `POST /v1/files` | `pruna-api` |
| Style-locked stills | `p-image`, `p-image-edit` | `p-image`, `p-image-edit` |
| Talking clips | `p-video-avatar` | `p-video-avatar` |
| Motion transfer | **`p-video-animate`** | `p-video-animate` |
| Slider comparison | ffmpeg (below) | local |

Use **`PRUNA_API_KEY`** and the **`apikey`** header on every call. **Async + parallel by default**: batch all avatar jobs once approved stills pass slop; batch all animate jobs once motion + still URLs are ready; poll all `get_url` together.

## Parallel execution

| Phase | Parallel? |
|-------|-----------|
| Hero `p-image` → gate | Sequential |
| Per-scene `p-image-edit` | **Yes** — all scenes |
| Slop gate | **Yes** — review in parallel |
| `p-video-avatar` | **Yes** — all avatar rows |
| `p-video-animate` | **Yes** — all animate rows |
| Slider render | **Yes** — all animate rows |
| Assembly | Sequential order only |

**Rule:** Never dispatch generation before user confirmation.

## Slider comparison (animate rows)

Side-by-side (motion template | animated):

```bash
ffmpeg -y -i motion_template.mp4 -i animated.mp4 \
  -filter_complex "[0:v]scale=960:1080[l];[1:v]scale=960:1080[r];[l][r]hstack=inputs=2[v]" \
  -map "[v]" -map 1:a? -c:v libx264 -c:a aac -shortest scene_compare.mp4
```

Or present both clips and let the user’s editor build a wipe slider. Paths can follow [templates/batch.template.json](./templates/batch.template.json) (`source`, `render`, `samples[]`).

## Workflow

| Step | Action |
|------|--------|
| 1–3 | Intake → speakable script → **confirmation gate** (no API until approve) |
| 4–5 | Upload refs → **`p-image` hero** per character → slop gate |
| 6–7 | Parallel **`p-image-edit`** scene stills → slop gate each |
| 8 | Parallel **`p-video-avatar`** (cast ledger voices, unique `video_prompt` per scene) |
| 9 | Parallel **`p-video-animate`** + ffmpeg sliders — [animate-beats.md](./animate-beats.md) |
| 10 | ffmpeg concat ± optional bed — `stable-audio-2.5` |
| 11 | Manifest: paths, prediction ids, slop notes, cast snapshot |

```bash
ffmpeg -y -f concat -safe 0 -i clips.txt -c copy reel.mp4
```

Shared ffmpeg recipes (concat, bed mix, sliders, export): **`video-editing`**.

## Related

Related skills:

| Skill | Description | Install |
| --- | --- | --- |
| `avatar-single-scene` | Use when someone wants one polished host-on-camera beat — a speaking person with intake and approval gates before generation. | `npx skills add PrunaAI/pruna-skills@avatar-single-scene -y` |
| `image-to-video` | Use when someone wants one short film beat from images — a narrated scene, story moment, or cinematic B-roll with optional voiceover. | `npx skills add PrunaAI/pruna-skills@image-to-video -y` |
| `narrated-multi-scene` | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue. | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

