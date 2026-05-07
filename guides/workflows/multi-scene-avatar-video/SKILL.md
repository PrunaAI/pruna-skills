---
name: multi-scene-avatar-video
description: Builds multi-scene talking-avatar videos on Pruna only—natural-language scripts, one locked voice per recurring character, one source hero image per character reused across styles and scenes via p-image-edit, explicit user confirmation before any API calls, then a written runnable script (automation or curl) to execute generation. Same stack as before—files, p-image, p-image-edit, optional upscale, p-video-avatar, manifest.
---

# Multi-scene avatar video (Pruna only)

## Purpose

Produce a **coherent multi-scene** talking-avatar piece where each scene is a Pruna **`p-video-avatar`** clip, stitched later in **your own editor or pipeline** (Pruna does not ship a concat endpoint in this skill set). Visual continuity comes from **Pruna `p-image` / `p-image-edit`** on uploaded references—not from other vendors’ image APIs.

Follow this skill in **plain language** when talking to the person requesting the video: explain cast, voices, and scene order the way you would in a production meeting. Use **natural, speakable copy** in every `voice_script` (real sentences, contractions where they sound right, clear emphasis—avoid stiff outline-speak unless the client wants that tone).

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
| **References** | Which files to upload; rights cleared? |
| **Assembly** | How clips will be joined and leveled (tool-agnostic plan)? |

If anything material is unknown, **ask** before the first upload or prediction.

## Cast ledger (voice lock)

Maintain a small **cast table** in the manifest or brief:

| Character | Pruna `voice` | `voice_language` | Notes |
|-----------|----------------|------------------|--------|
| (example) | `Zephyr (Female)` | `English (US)` | Same voice every time this character speaks. |

**Rule:** A recurring character **never** changes voice between scenes unless the user explicitly asks for a recast. Optional per-character **`voice_prompt`** tweaks are fine; the **`voice`** preset stays fixed.

## Source portrait / hero (same character across styles and scenes)

For **each** recurring character:

1. Land **one** approved **source** still (upload to `/v1/files` or one accepted `p-image` / `p-image-edit` result). Treat its Pruna file URL as the **identity anchor** for that character for the whole project.
2. **Every** later look—including a new background, emotion, prop, or **style variation** (e.g. “same cat, but ink-line instead of pencil”)—should be produced with **`p-image-edit`** from **that same source URL**, plus the shared style bible and a short delta (“change only: …”). Do **not** mint a fresh identity with unrelated `p-image` text prompts mid-run unless the user resets the character.
3. **Each new scene** still starts from the same character source as step 2 so faces stay one continuous role across the arc.

This keeps later scene opens and style experiments aligned with the **same** underlying portrait the user signed off on.

## Confirmation gate (mandatory)

After intake is complete and you have drafted work in **natural human language**:

1. Present a **read-through package**: scene order, full **`voice_script`** text per scene (written as real dialogue), the **cast ledger** (who speaks which lines), **which hero URL** anchors each character’s stills, chosen **`resolution`**, and any legal or CTA lines **verbatim** if supplied.
2. Ask clearly for approval (e.g. “Reply **approve** or **go** when this script and cast are final.”).
3. **Do not** upload binaries for generation, call **`POST /v1/predictions`**, or run automation until the user **explicitly confirms**.

Optional edits after feedback; repeat confirmation if the script or cast changes materially.

## Script and run package (after confirmation)

Once the user confirms:

1. **Write** a concrete **generation package**: either a **small runnable script** (shell or Python, like other automation in this repo) **or** an ordered list of **`curl`** / steps that performs uploads, **`p-image`** / **`p-image-edit`**, optional upscale, **`p-video-avatar`** (async + poll), and downloads—using the confirmed **`voice_script`** and cast ledger **exactly**.
2. **Execute** that package when execution is possible (`PRUNA_API_KEY` present, network available). If the environment cannot call the API, hand the user the same script and exact commands so they can run it locally without guesswork.

The script is the contract: what runs must match what was approved.

## Core rule

**`p-video-avatar` only runs on frames that passed** [`references/generation-quality-checklists.md`](../../../references/generation-quality-checklists.md).

## API surface (this workflow)

| Step | Model | Skill |
|------|--------|--------|
| Upload binaries | `POST /v1/files` | [references/pruna-api.md](../../../references/pruna-api.md) |
| Style-locked stills | `p-image`, `p-image-edit` | [p-image](../../../tools/image/p-image/SKILL.md), [p-image-edit](../../../tools/image/p-image-edit/SKILL.md) |
| Optional resolution pass | `p-image-upscale` | [p-image-upscale](../../../tools/image/p-image-upscale/SKILL.md) |
| Talking clips | `p-video-avatar` | [p-video-avatar](../../../tools/video/p-video-avatar/SKILL.md) |

Use **`PRUNA_API_KEY`** and the **`apikey`** header on every call. Prefer **async** predictions for avatar clips; poll until `succeeded`, then download `generation_url`.

## Workflow

1. **Intake** — Confirm the **Intake** table above is complete; expand into a written brief (cast order, **cast ledger** with one voice per character, style bible, per-scene line ownership).

2. **Draft script (natural language)** — Write the full multi-scene script as **speakable** copy: one **`voice_script`** string per **`p-video-avatar`** call (per scene or per line—your choice, but one prediction = one clip). Keep the final CTA or legal line **verbatim** if the client supplied exact wording.

3. **Confirmation** — Share the read-through package and **wait for explicit user approval** (see **Confirmation gate**). No API calls before that.

4. **Ingest references**
   - Collect licenced or owned reference stills (concept art, turnaround, prior approved renders).
   - Upload each with `POST https://api.pruna.ai/v1/files`; store each **`urls.get`** (or `https://api.pruna.ai/v1/files/{id}`) in a manifest. These URLs are the only inputs to **`p-image-edit`**; do not rely on hotlinked third-party URLs.

5. **Lock source / hero frames (per character)** — See **Source portrait / hero**. One approved anchor URL per speaking character; all later looks derive from **`p-image-edit`** off that anchor unless the user resets.

6. **Per-scene reference stills**
   - For each scene, produce **one** talking-head **image** URL from the correct character’s **source** URL + **`p-image-edit`** (pose, background, emotion, style tweak—**change only** what the beat needs). Avoid unrelated **`p-image`** text runs that reinvent the face.
   - Optional: run **`p-image-upscale`** on a still before avatar if you need more pixels for cropping or downstream tooling.

7. **Slop gate (every still)**
   - Run [`references/generation-quality-checklists.md`](../../../references/generation-quality-checklists.md) on each candidate. Regenerate with **`p-image` / `p-image-edit`** until it passes **before** any avatar job.

8. **Per-scene avatar generation**
   - For each approved still, call **`p-video-avatar`** with JSON **`input`** using **snake_case** keys (see `prompt-templates.md` and [p-video-avatar](../../../tools/video/p-video-avatar/SKILL.md)):
     - `image`, `voice_script`, **`voice`** (from the **cast ledger**—same preset every time for that character), `voice_language`, `voice_prompt`, `video_prompt`, `resolution`, optional `seed`.
   - Keep **`voice_prompt`** short and non-spoken; if the model leaks it as dialogue, shorten or omit and rely on `voice` + `voice_script` only.
   - Do **not** use negations like “no subtitles / no logos” in **`video_prompt`**; keep prompts positive and shot-focused.

9. **Assembly (outside Pruna)**
   - Order clips to match the script. Join them in **your** video editor or automation; level audio for continuity. This repo does not prescribe a vendor—only that assembly is **not** a Pruna prediction step here.

10. **Manifest**
   - For every asset: source path, Pruna file id/URL, each prediction `id`, final `generation_url`, prompts, pass/fail on slop, retries, **cast ledger** snapshot. Store enough to reproduce the cut.

## References

- [generation-quality-checklists.md](../../../references/generation-quality-checklists.md)
- `prompt-templates.md`
- `examples.md`

## Related

- Pruna-only pipeline overview: [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md)
- One-scene avatar: [single-scene-avatar-video](../single-scene-avatar-video/SKILL.md)
- Cinematic video: [single-scene-ai-video](../single-scene-ai-video/SKILL.md), [multi-scene-ai-video](../multi-scene-ai-video/SKILL.md)
