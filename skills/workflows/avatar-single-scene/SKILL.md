---
name: avatar-single-scene
description: Use when someone wants one polished host-on-camera beat — a speaking person with intake and approval gates before generation.
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
| `gemini-3.1-flash-tts` | Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video. | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## Workflow habit

In **every reply**, name `` `avatar-single-scene` `` in backticks. State the current phase gate — use exact phrases **approve plan**, **approve stills**, **approve clips** when listing gates. Do **not** same-turn plan + paid video. Skip-review / burn-credits → follow `generation-diversity` **Red flags**.

## Feedback gates (required)

| Phase | What to show | Proceed when |
|-------|--------------|--------------|
| **0 — Plan** | Full `voice_script`, voice, still + motion plan | **approve plan** |
| **A — Still** | Hero / portrait plate | **approve still** |
| **B — Avatar** | Single `p-video-avatar` clip | User accepts |

## Natural language script

Write **`voice_script`** as **real dialogue**: contractions, natural rhythm, short sentences—how a person talks on camera, not a press release. See `avatar-multi-scene` for good/bad examples.

**`voice_prompt`** must describe **human delivery** (pacing, warmth, founder/conversational tone)—never paste marketing copy or script lines into it.

## Voice and image continuity

- **`voice` / `voice_language`:** Pick **one** preset pair for this clip’s speaker. If this character will appear again in a series or sequel clips, **reuse the same presets** so they sound like one person (same rule as the multi-scene skill’s cast ledger).
- **Source portrait:** Prefer **one** approved reference URL (upload or generated). If you explore alternate backgrounds or styles, branch with **`p-image-edit`** from **that same** URL plus deltas—do not reinvent the face with an unrelated **`p-image`** unless the user agrees to a new identity.

## Intake: ask before generating

Open intake → **`generation-diversity`** clarification intake.

**Do not** call `POST /v1/predictions` until the user (or product owner) has answered these—record answers in the manifest:

| Topic | Questions |
|-------|-----------|
| **Goal** | What must this one clip communicate (single CTA, greeting, demo line)? |
| **Media source** | **Upload-only** portrait vs **generate/refine** still with `p-image` / `p-image-edit` first? |
| **Script** | Full **`voice_script`** as speakable copy—any mandatory pronunciation (names, acronyms)? |
| **Voice** | Which Pruna **`voice`** and **`voice_language`**? Keep **`voice_prompt`** short (performance vibe only). |
| **Look** | `9:16` / `16:9` still? Avatar **`resolution`** `720p` or `1080p`? |
| **Motion** | Desired energy for **`video_prompt`**—specific camera angle and movement (positive wording only)? |
| **Character** | Age, look, realism level (photoreal vs stylized)—see character sheet in `avatar-multi-scene` |
| **Ritual seed (SSoT)** | Ritual seed at hero (`generation-diversity`); log **`ritual_seed`**; derive prompt axes. Identity continuity = approved plate URL. Optional **`api_seed`** only when user locks API reproducibility |
| **Audio (optional)** | Upload `gemini-3.1-flash-tts` for lip-sync via **`input.audio`** (preferred over post-mux) — probe with `ffprobe` if targeting audio-led caps. Or use native **`voice_script`**. |

If any answer is missing and the user has not waived it, **ask** before generating.

## Confirmation gate (mandatory)

After intake:

1. Show the **full `voice_script`**, chosen **`voice`** / **`voice_language`**, **`resolution`**, and a short description of the still + **`video_prompt`** plan.
2. Ask for **explicit approval** before calling the API (e.g. user replies **go** / **approved**).
3. If they edit the script, show the updated **`voice_script`** and confirm again when changes are material.

## How the agent runs this

Once confirmed:

1. Upload refs → build still with curl (`pruna-api`) → slop gate → **approve still**.
2. Optional TTS → `ffprobe` → upload as `input.audio`.
3. One async **`p-video-avatar`** job → poll → download.
4. Manifest: intake, URLs, prediction ids, confirmed script snapshot.

## Workflow (after confirmation)

1. **References** — Upload assets with `POST /v1/files`; collect Pruna file URLs.
2. **Still (if needed)** — Build one talking-head frame with **`p-image`** and/or **`p-image-edit`**. Run the slop gate before avatar.
3. **Slop gate** — `generation-diversity` checklists; fix with image models until pass.
4. **Avatar** — Call **`p-video-avatar`** with snake_case `input` (`image`, optional `last_frame_image`, **`voice_script`** *or* uploaded **`audio`**, `voice`, `voice_language`, **`voice_prompt`**, **`video_prompt`**, `resolution`, **`seed`**). Prefer uploaded **`audio`** from Gemini TTS when external narration quality matters. **Async only** (omit `Try-Sync`); poll to `succeeded`; download `generation_url`.
5. **Manifest** — Store intake answers, URLs, prediction ids, prompts, retries, confirmed script snapshot.

## Related

Related skills:

| Skill | Description | Install |
| --- | --- | --- |
| `avatar-multi-scene` | Use when someone wants the same person hosting several clips — multi-segment UGC, comparison reels, or mixed speaking and animated scenes with continuity. | `npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

