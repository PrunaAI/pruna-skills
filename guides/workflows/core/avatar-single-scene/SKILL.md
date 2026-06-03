---
name: single-scene-avatar-video
description: One Pruna talking-head clip after intake—character sheet, locked seed, natural human voice_script and voice_prompt, source portrait via p-image or p-image-edit, explicit user confirmation before any POST /v1/predictions, then a runnable script or curl sequence to execute generation.
metadata:
  version: "0.0.1"
---

# Single-scene avatar video (Pruna only)

One approved portrait → one **`p-video-avatar`** job. Stills and QA reuse the same patterns as [multi-scene-avatar-video](../avatar-multi-scene/SKILL.md); use [generation-quality-checklists.md](../../../../../references/shared/generation-quality-checklists.md) and that folder’s **`prompt-templates.md`**.

Speak to the requester in **plain language**: explain what they will hear (full **`voice_script`**) and see (still + motion) before anything hits the API.

Atomic APIs: [p-video-avatar](../../../../tools/video/p-video-avatar/SKILL.md), [p-image](../../../../tools/image/p-image/SKILL.md), [p-image-edit](../../../../tools/image/p-image-edit/SKILL.md), [references/shared/pruna-api.md](../../../../../references/shared/pruna-api.md).

## Natural language script

Write **`voice_script`** as **real dialogue**: contractions, natural rhythm, short sentences—how a person talks on camera, not a press release. See [multi-scene-avatar-video/prompt-templates.md](../avatar-multi-scene/prompt-templates.md) for good/bad examples.

**`voice_prompt`** must describe **human delivery** (pacing, warmth, founder/conversational tone)—never paste marketing copy or script lines into it.

## Voice and image continuity

- **`voice` / `voice_language`:** Pick **one** preset pair for this clip’s speaker. If this character will appear again in a series or sequel clips, **reuse the same presets** so they sound like one person (same rule as the multi-scene skill’s cast ledger).
- **Source portrait:** Prefer **one** approved reference URL (upload or generated). If you explore alternate backgrounds or styles, branch with **`p-image-edit`** from **that same** URL plus deltas—do not reinvent the face with an unrelated **`p-image`** unless the user agrees to a new identity.

## Intake: ask before generating

**Do not** call `POST /v1/predictions` until the user (or product owner) has answered these—record answers in the manifest:

| Topic | Questions |
|-------|-----------|
| **Goal** | What must this one clip communicate (single CTA, greeting, demo line)? |
| **Script** | Full **`voice_script`** as speakable copy—any mandatory pronunciation (names, acronyms)? |
| **Voice** | Which Pruna **`voice`** and **`voice_language`**? Keep **`voice_prompt`** short (performance vibe only). |
| **Look** | `9:16` / `16:9` still? Avatar **`resolution`** `720p` or `1080p`? |
| **Image source** | Upload-only reference, or generate/refine with **`p-image`** / **`p-image-edit`** first? |
| **Motion** | Desired energy for **`video_prompt`**—specific camera angle and movement (positive wording only)? |
| **Character** | Age, look, realism level (photoreal vs stylized)—see character sheet in [multi-scene-avatar-video](../avatar-multi-scene/SKILL.md) |
| **Seed** | Lock **`seed`** at hero generation; pass same value to **`p-video-avatar`** |
| **Audio (optional)** | Upload [Gemini TTS](../../../../tools/audio/gemini-3.1-flash-tts/SKILL.md) for lip-sync via **`input.audio`** (preferred over post-mux) — see [scene-anchor-triple.md](../../../../../references/video/scene-anchor-triple.md) avatar variant. Or use native **`voice_script`**. |

If any answer is missing and the user has not waived it, **ask** before generating.

## Confirmation gate (mandatory)

After intake:

1. Show the **full `voice_script`**, chosen **`voice`** / **`voice_language`**, **`resolution`**, and a short description of the still + **`video_prompt`** plan.
2. Ask for **explicit approval** before calling the API (e.g. user replies **go** / **approved**).
3. If they edit the script, show the updated **`voice_script`** and confirm again when changes are material.

## Script and run package (after confirmation)

When the user confirms:

1. **Emit** a **runnable generation package**: phased **`curl`** calls or a small script (shell/Python) that uploads if needed, builds the still, runs **`p-video-avatar`** async, polls, and downloads **`generation_url`**—matching the approved script **exactly**. For multi-step prep (edit + avatar), use async and parallel phases per [parallel-execution.md](../../../../../references/shared/parallel-execution.md).
2. **Run** it when the environment allows (**`PRUNA_API_KEY`**, network). Otherwise deliver the same artifact so the user can execute locally.

## Workflow (after confirmation)

1. **References** — Upload assets with `POST /v1/files`; collect Pruna file URLs.
2. **Still (if needed)** — Build one talking-head frame with **`p-image`** (photoreal prompt + locked **`seed`**) and/or **`p-image-edit`** from a locked source. Run the slop gate before avatar.
3. **Slop gate** — Run the checklist in [generation-quality-checklists.md](../../../../../references/shared/generation-quality-checklists.md); fix with image models until pass.
4. **Avatar** — Call **`p-video-avatar`** with snake_case `input` (`image`, optional `last_frame_image`, **`voice_script`** *or* uploaded **`audio`**, `voice`, `voice_language`, **`voice_prompt`**, **`video_prompt`**, `resolution`, **`seed`**). Prefer uploaded **`audio`** from [Gemini TTS](../../../../tools/audio/gemini-3.1-flash-tts/SKILL.md) when external narration quality matters. **Async only** (omit `Try-Sync`); poll to `succeeded`; download `generation_url`.
5. **Manifest** — Store intake answers, URLs, prediction ids, prompts, retries, confirmed script snapshot.

## Related

- Multi-scene version: [multi-scene-avatar-video](../avatar-multi-scene/SKILL.md)
- Generative chain overview: [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md)
