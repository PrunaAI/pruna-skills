---
name: multi-scene-avatar-video
description: Builds multi-scene Pruna video pieces—talking-avatar clips (p-video-avatar), motion-transfer slider beats (p-video-animate + comparison render), or mixed announcement reels—with character sheets, locked seeds, natural human voice, hero reuse via p-image-edit, alignment-aware animate prep, explicit user confirmation before any API calls, then async parallel generation per phase with subagents per scene lane where possible.
metadata:
  version: "0.0.1"
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
| **Scene variety** | Each scene must differ in **camera angle**, **background/setting**, and/or **energy**—no two consecutive scenes with the same framing and location unless the user asks. Plan **`visual_style_tag`**, **`setting_tag`**, **`camera_tag`**, **`lighting_tag`** per row; cast diversity (gender, age, ethnicity) on showcase reels — [visual-variety-bible.md](../../../references/visual-variety-bible.md). |
| **Seeds** | Pick and **lock** a project **`seed`** at hero `p-image` (or user-supplied). Record in manifest; reuse when regenerating the same hero; pass the same **`seed`** to every **`p-video-avatar`** call unless A/B testing motion. |
| **References** | Which files to upload; rights cleared? |
| **Beat mix** | Which scenes are **`avatar`** vs **`animate`**? All avatar, all animate, or mixed announcement? |
| **Motion templates** (animate beats) | Source `.mp4` per animate row—owned/licensed? Match pose/framing to reference still? |
| **Slider delivery** (animate beats) | Comparison MP4 only, animated-only strip, or both? Canvas default 1920×1080. |
| **Assembly** | How clips will be joined and leveled (tool-agnostic plan)? |

If anything material is unknown, **ask** before the first upload or prediction.

## Cast ledger (voice lock)

Maintain a small **cast table** in the manifest or brief:

| Character | Pruna `voice` | `voice_language` | Notes |
|-----------|----------------|------------------|--------|
| (example) | `Zephyr (Female)` | `English (US)` | Same voice every time this character speaks. |

**Rule:** A recurring character **never** changes voice between scenes unless the user explicitly asks for a recast. Optional per-character **`voice_prompt`** tweaks are fine; the **`voice`** preset stays fixed.

## Character sheet (identity + traits)

Before the hero still, write a **character sheet** per speaking role and keep it in the manifest. Agents use it in every image prompt and when drafting dialogue tone.

| Field | Example | Used in |
|-------|---------|---------|
| Name / role | Alex, founder spokesperson | Brief, manifest |
| Age & build | early 30s, athletic | `p-image`, `p-image-edit` |
| Face & hair | short dark hair, light stubble, brown eyes | identity anchors in image prompts |
| Realism | photorealistic documentary, not CGI | `p-image` hero prompt |
| Wardrobe baseline | black crew-neck, minimal | style bible; scene edits change setting not outfit unless scripted |
| Personality | warm, direct, founder-energy | `voice_prompt`, `voice_script` tone |
| Locked `seed` | e.g. `482901` | hero `p-image`, all `p-video-avatar` calls |

**Rule:** Scene-to-scene **style** changes (office → mountain → ISS → desk → studio) come from **`p-image-edit`** off the approved hero—never a fresh unrelated **`p-image`** that reinvents the face.

## Scene plan (dynamic beats)

Every multi-scene piece needs a **scene table** before generation. Each row has a **`type`**: `avatar` or `animate`.

### Avatar rows

| # | Type | Setting & angle | Emotion | `voice_script` (natural) | `video_prompt` (camera/motion) |
|---|------|-----------------|---------|--------------------------|--------------------------------|
| 1 | avatar | extreme close-up, dark cinematic | hook, curious | "Hey — quick question. When you're…" | slow push-in, direct eye contact |
| 3 | avatar | medium, ISS cupola | excited reveal | "So we teamed up with…" | gentle float, earth in window |
| … | avatar | **must differ from prior avatar row** | | speakable, contractions OK | positive camera grammar only |

### Animate rows

| # | Type | Motion template | Reference still | Alignment plan | `instruction_prompt` (optional) | Slider output |
|---|------|-----------------|-----------------|----------------|----------------------------------|---------------|
| 2 | animate | `ugc_hook.mp4` | hero still | match MC close-up, facing lens | "Match gestures; keep outfit from reference." | `scene02_compare.mp4` |
| 4 | animate | `dance_trend.mp4` | mascot still | **risk:** human legs on short mascot | "Upper-body motion only." | `scene04_compare.mp4` |

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
4. Run [p-video-animate-quality-checklist.md](../../../references/p-video-animate-quality-checklist.md) on the pair before animate.

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

## Seed policy

1. **Hero `p-image`:** set **`seed`** once; store in manifest as `project_seed`.
2. **Regenerate hero only:** reuse `project_seed` + same prompt unless the user resets identity.
3. **`p-image-edit`:** seed support varies—continuity comes from the **hero file URL**, not re-rolling identity.
4. **`p-video-avatar`:** pass **`seed`: `project_seed`** on every clip for reproducible motion/delivery when the API accepts it; if a scene needs a motion retry, bump seed only for that scene and note it in the manifest.

## Natural voice (mandatory for avatar social / founder content)

**`voice_script`** — write how a **real person talks**, not a press release:

- Use contractions (*it's*, *we're*, *you've*), light fillers where natural (*"Hey —"*, *"right?"*, *"Anyway —"*).
- Short sentences; one idea per breath.
- Product names spoken cleanly; acronyms spelled out or simplified unless the brand always says them as letters.

**`voice_prompt`** — performance direction for **human delivery** (never duplicate script text):

```text
Natural conversational tone — like a founder on LinkedIn, not a TV announcer.
Relaxed pacing, real pauses, slight smile when excited, honest not salesy.
```

See **`prompt-templates.md`** for good/bad pairs and per-scene **`video_prompt`** patterns.

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

1. **Write** a concrete **generation package**: phased **`curl`** steps or a small script that performs uploads, **`p-image`** / **`p-image-edit`**, parallel **`p-video-avatar`** (avatar rows), parallel **`p-video-animate`** (animate rows), **`generate_video_comparison.py`** slider renders (animate rows), and downloads—matching the approved scene table **exactly**. **Parallelize** independent lanes within each phase ([parallel-execution.md](../../../references/parallel-execution.md)).
2. **Execute** that package when execution is possible (`PRUNA_API_KEY` present, network available). Prefer **one subagent per scene lane** (still pipeline: edit → gate; or avatar: create → poll → download) launched in parallel after the hero anchor exists. Parent agent owns confirmation, manifest merge, and assembly. If the environment cannot call the API, hand the user the same script and exact commands so they can run it locally without guesswork.

The script is the contract: what runs must match what was approved.

## Core rules

1. **`p-video-avatar` `input.image`** — use an approved still URL from `/v1/files` (upload, **`p-image`**, or **`p-image-edit`** output) that passed [generation-quality-checklists.md](../../../references/generation-quality-checklists.md).
2. Run the **slop gate** on every hero and scene still **before** any avatar job.

```text
Hero:     p-image (or upload) → slop gate → approve anchor
Scene N:  p-image-edit(anchor) → slop gate → p-video-avatar
```

Use the **approved hero** as the reference for **`p-image-edit`**, not a rejected intermediate.

## API surface (this workflow)

| Step | Model | Skill |
|------|--------|--------|
| Upload binaries | `POST /v1/files` | [references/pruna-api.md](../../../references/pruna-api.md) |
| Style-locked stills | `p-image`, `p-image-edit` | [p-image](../../../tools/image/p-image/SKILL.md), [p-image-edit](../../../tools/image/p-image-edit/SKILL.md) |
| Talking clips | `p-video-avatar` | [p-video-avatar](../../../tools/video/p-video-avatar/SKILL.md) |
| Motion transfer | **`p-video-animate`** | [p-video-animate](../../../tools/video/p-video-animate/SKILL.md) |
| Slider comparison (animate rows) | [`generate_video_comparison.py`](../_shared/scripts/generate_video_comparison.py) | local; install via `./scripts/install_skill.sh multi-scene-avatar-video` |

Use **`PRUNA_API_KEY`** and the **`apikey`** header on every call. **Async + parallel by default**: batch all avatar jobs once approved stills pass slop; batch all animate jobs once motion + still URLs are ready; poll all `get_url` together. See [parallel-execution.md](../../../references/parallel-execution.md).

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

1. **Intake** — Confirm the **Intake** table above is complete; expand into a written brief (cast order, **cast ledger** with one voice per character, style bible, per-scene line ownership).

2. **Draft script (natural language)** — Write the full multi-scene script as **speakable** copy: one **`voice_script`** string per **`p-video-avatar`** call (per scene or per line—your choice, but one prediction = one clip). Keep the final CTA or legal line **verbatim** if the client supplied exact wording.

3. **Confirmation** — Share the read-through package and **wait for explicit user approval** (see **Confirmation gate**). No API calls before that.

4. **Ingest references**
   - Collect licenced or owned reference stills (concept art, turnaround, prior approved renders).
   - Upload each with `POST https://api.pruna.ai/v1/files`; store each **`urls.get`** (or `https://api.pruna.ai/v1/files/{id}`) in a manifest. These URLs are the only inputs to **`p-image-edit`**; do not rely on hotlinked third-party URLs.

5. **Lock source / hero frames (per character)** — See **Source portrait / hero**. One approved hero anchor URL per speaking character; all later looks derive from **`p-image-edit`** off that anchor unless the user resets.

6. **Per-scene reference stills (edit → gate)**
   - For each scene row: **`p-image-edit`** from the hero anchor URL — **change only:** angle, background, emotion, props.
   - **Run all scene edits in parallel** once the hero anchor URL exists.
   - Upload approved stills to `/v1/files`; record URLs as `scene_N_still` in manifest.

7. **Slop gate (every still)**
   - Run [`references/generation-quality-checklists.md`](../../../references/generation-quality-checklists.md) on each hero and scene still. Regenerate until pass **before** any avatar job.

8. **Per-scene avatar generation (avatar rows only)**
   - **Create all `p-video-avatar` jobs in parallel** (async, no `Try-Sync`) once every scene still for avatar rows passes slop. Poll all jobs together; download when complete.
   - Call **`p-video-avatar`** with JSON **`input`** using **snake_case** keys (see `prompt-templates.md` and [p-video-avatar](../../../tools/video/p-video-avatar/SKILL.md)). **`input.image`** must be the approved scene still URL from `/v1/files`.
   - Fields: `image`, `voice_script`, **`voice`** (from the **cast ledger**), `voice_language`, **`voice_prompt`**, **`video_prompt`**, `resolution`, **`seed`** (project lock).
   - **`video_prompt` must vary by scene** (close-up push-in vs 3/4 handheld vs over-shoulder vs medium studio). Match the scene table.
   - Keep **`voice_prompt`** short and non-spoken; if the model leaks it as dialogue, shorten or omit and rely on `voice` + `voice_script` only.
   - Do **not** use negations like “no subtitles / no logos” in **`video_prompt`**; keep prompts positive and shot-focused.

9. **Per-scene motion transfer (animate rows only)**
   - Upload each motion template `.mp4` and reference still to `/v1/files`.
   - Optional **`p-image-edit`** to align pose (see **Alignment prep**).
   - **Create all `p-video-animate` jobs in parallel** once each row's URLs are ready. Poll all `get_url`; download each `generation_url`.
   - Example payload:

   ```bash
   curl -X POST 'https://api.pruna.ai/v1/predictions' \
     -H 'Content-Type: application/json' \
     -H "apikey: ${PRUNA_API_KEY}" \
     -H 'Model: p-video-animate' \
     -d '{
       "input": {
         "video": "https://api.pruna.ai/v1/files/MOTION_ID",
         "image": "https://api.pruna.ai/v1/files/SUBJECT_ID",
         "resolution": "720p",
         "target_fps": "original",
         "save_audio": true,
         "instruction_prompt": "Animate the reference subject using the motion from the source video."
       }
     }'
   ```

10. **Slider comparison render (animate rows only)**

Requires `ffmpeg` and Pillow (`pip install -r guides/workflows/_shared/scripts/requirements.txt`). After portable install, use `./scripts/requirements.txt` inside the skill folder.

**Single animate row:**

```bash
python3 guides/workflows/_shared/scripts/generate_video_comparison.py \
  --source path/to/motion-template.mp4 \
  --output path/to/animated-output.mp4 \
  --render output/scene02_compare.mp4 \
  --title "P-Video-Animate · Scene 2"
```

**Multi animate row batch** — use [`batch.template.json`](../../../examples/workflows/p-video-animate-comparison/batch.template.json):

```bash
python3 guides/workflows/_shared/scripts/generate_video_comparison.py --config output/project.batch.json
```

Default slider structure:

| Beat | ~Duration | Content |
|------|-----------|---------|
| Hook | 1.5s | Full **motion template** (slider left) |
| Synced play | min(source, output) | Slider sweeps **left → right** over ~2.5s while both play |
| Hold / outro | 1.5s each | Full **animated output** |

Tune `timing` in JSON: `hook_seconds`, `slider_seconds`, `hold_output_seconds`, `outro_seconds`.

11. **Assembly (outside Pruna)**
   - Order clips to match the scene table (`avatar` MP4s and `animate` comparison MP4s interleaved as planned). Join in **your** editor or ffmpeg concat; level audio for continuity.
   - Optional **light instrumental bed** under VO: [`launch_background_music.py`](../_shared/scripts/launch_background_music.py) + [stable-audio-2.5](../../../tools/audio/stable-audio-2.5/SKILL.md) (`REPLICATE_API_TOKEN`, ~0.12 volume).

12. **Manifest**
   - For every asset: type (`avatar` | `animate`), source path, Pruna file id/URL, prediction `id`, final clip path, prompts, slop pass/fail, alignment notes (animate), **cast ledger** snapshot.

## References

- [generation-quality-checklists.md](../../../references/generation-quality-checklists.md)
- [animate-beats.md](./animate-beats.md) — `p-video-animate` in mixed reels, motion templates, alignment, sliders
- `prompt-templates.md`
- `examples.md`

## Related

- Pruna-only pipeline overview: [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md)
- One-scene avatar: [single-scene-avatar-video](../single-scene-avatar-video/SKILL.md)
- Cinematic B-roll (non-avatar): [single-scene-ai-video](../single-scene-ai-video/SKILL.md), [multi-scene-ai-video](../multi-scene-ai-video/SKILL.md)
- Still upscale slider demos: [p-image-upscale-comparison](../p-image-upscale-comparison/SKILL.md)
- Motion transfer tool: [p-video-animate](../../../tools/video/p-video-animate/SKILL.md)
