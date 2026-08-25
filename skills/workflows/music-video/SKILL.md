---
name: music-video
description: Use when someone wants a full music video — original song or vocals, performance clips, B-roll, and lyric-synced edits.
license: MIT
metadata:
  version: "1.0.10"
  package: pruna-skills
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `music-2.5` | Use when someone wants an original AI song with vocals — sung lyrics, a style prompt track, or source audio for a music video. | `npx skills add PrunaAI/pruna-skills@music-2.5 -y` |
| `whisperx` | Use when someone needs word-level timestamps from audio — lyric alignment, cut-safe line boundaries, or caption source timing before burn-in with video-editing. | `npx skills add PrunaAI/pruna-skills@whisperx -y` |
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## Workflow habit

In **every reply**, name `` `music-video` `` in backticks (including intake Q&A). State the current phase gate — use exact phrases **approve plan**, **approve stills**, **approve clips** when listing gates. Do **not** same-turn plan + paid video. Skip-review / burn-credits → follow `generation-diversity` **Red flags**.

## Quick reference

| Resource | Path |
|----------|------|
| Lyrics, cuts, align pipeline | [lyrics-and-cuts.md](./lyrics-and-cuts.md) |
| Plan template | [templates/music-video-plan.template.json](./templates/music-video-plan.template.json) |
| Feedback | `generation-diversity` |
| QA | [./references/music-video-quality-checklist.md](./references/music-video-quality-checklist.md) |

## Model routing (performance vs B-roll)

| Beat | Human singer / rapper | Mascot or stylized host |
|------|----------------------|-------------------------|
| **Performance** (lip sync to song) | **`p-video-avatar`** — `image` + **`audio`** slice from master song. **Not** `voice_script`. | **`p-video`** — `image` + **`audio`** slice ([Pruna music-to-video](https://docs.pruna.ai/en/stable/docs_pruna_endpoints/performance_models/skills/workflows/music_to_video.html)). **`p-video-avatar` humanizes non-human stills** — avoid on mascots. |
| **B-roll** | **`p-video`** — still + **`audio`** slice (or `duration` on instrumentals) | Same |

Set in the plan: `cast.host_type` (`human` | `mascot`) and optional `cast.performance_model` override. Agent picks the model from `beat_type` + `host_type`.

**Human rapper pattern:** `cast.host_type: human` → performance sections use **`p-video-avatar`** + song slice; B-roll stays **`p-video`**.

## Intake: ask before generating

Open intake → **`generation-diversity`** clarification intake.

| Topic | Questions |
|-------|-----------|
| **Genre / mood** | Indie pop, R&B, electronic, acoustic ballad? Energy arc? |
| **Vocal** | Gender, timbre, tempo (BPM), key instruments — becomes `music.prompt` |
| **Story** | What should the video *show* during verse vs chorus vs instrumental? |
| **Cast** | One singer throughout or stylistic recasts on B-roll only? If **same singer**, confirm before stills — see **Character continuity** below. |
| **Continuity** | Same face/wardrobe baseline across performance cuts, or deliberate variety (location changes OK; identity drift is not)? |
| **Format** | `16:9` / `9:16`, `720p` / `1080p` |
| **Length** | Short hook (~60s) or full song (~3 min)? Fewer cuts = lower cost |
| **Cut density** | Line-per-cut (pop) or **`cut_granularity: section`** (one clip per verse — rap battles)? |
| **Beat mix** | Performance-heavy vs B-roll-heavy? Default: alternate on verses, performance on chorus |

Do **not** call Music 2.5 or Pruna video until lyrics are approved.

## Character continuity (when intended)

Ask whether performance beats should read as **one singer** or whether **recasts** are deliberate. Default assumption when the user names a single artist: **same person on every performance cut**.

| Intent | Stills | Video | Anti-pattern |
|--------|--------|-------|--------------|
| **Same singer throughout** | One approved **hero** via `p-image` (locked plate URL) → every performance still via **`p-image-edit`** off that URL | Reuse hero plate + `cast_descriptor` on all **`p-video-avatar`** jobs; distinct **`video_prompt`** per cut | Fresh unrelated **`p-image`** text prompt per line — faces drift |
| **Same singer, new locations** | Hero + edits per beat — vary **`setting_tag`**, **`camera_tag`**, **`lighting_tag`** | Same plate lock; distinct **`video_prompt`** per cut | Grey-wall repeat or identical framing on consecutive performance lines |
| **Deliberate recasts** | Only on **broll** beats, labeled guest rows, or when the user explicitly asks | N/A for lip-sync rows | Random new face mid-chorus without user approval |
| **Mascot / stylized host** | One approved mascot still → **`p-image-edit`** for pose/setting | **`p-video`** + song **`audio`** slice | **`p-video-avatar`** on non-human stills |

Record in the plan: `ritual_seed`, `cast` / `character_sheet`, approved **`hero_still`** URL, and `continuity: same_singer | recasts_ok`. Full cast-ledger patterns: `avatar-multi-scene`.

## Generation phases

| Phase | Models | Cost | Gate |
|-------|--------|------|------|
| **0 — Lyrics** | none | free | User approves lyric sheet + section tags |
| **A — Song** | `music-2.5` | medium | User approves MP3 |
| **B — Cut structure** | agent writes `cut_manifest.json` | free | Cut list matches lyric lines |
| **B2 — Cut timings** | `whisperx` | low | Review alignment stats |
| **C — Stills** | `p-image` / `p-image-edit` | low | **approve stills** |
| **D — Clips** | `p-video-avatar`, `p-video` | **high** | After still approval |
| **E — Assembly** | ffmpeg | free | After **approve clips** |

Default first paid stop: **song**.

After **`music-2.5`** delivers the track, run **`whisperx`** (`align_output: true`) before batching **`p-video`** / **`p-video-avatar`** clips — do not skip alignment when lyric-synced cuts matter.

```text
Lyrics + music.prompt → song → align → stills → video clips → music_video.mp4
```

Full lyric format, cut rules, and cut-manifest fields: **[lyrics-and-cuts.md](./lyrics-and-cuts.md)**.

## How the agent runs this

1. Copy [templates/music-video-plan.template.json](./templates/music-video-plan.template.json) → fill lyrics + cast → **approve lyrics**.
2. Generate song via `music-2.5` → **approve song**.
3. Build cut list from lyric lines; align with WhisperX → write `cut_manifest.json` with `start_sec` / `end_sec`.
4. Slice audio per cut:

```bash
ffmpeg -y -ss START -to END -i song.mp3 -c copy slices/01_2.mp3
```

5. Parallel stills (`pruna-api`) → **approve stills**.
6. Parallel performance + B-roll video jobs (upload each slice) → **approve clips**.
7. Trim clips to cut lengths, concat, mux **full song** as audio.

## Step 4 — Stills (`p-image` / `p-image-edit`)

One approved still per segment.

**When continuity is intended (default for one singer):**

1. Generate and gate **one hero** performance still with **`p-image`** + ritual seed (`generation-diversity`); lock hero plate URL.
2. Store the approved URL as **`hero_still`** in the plan.
3. Every later performance still = **`p-image-edit`** from **`hero_still`** — *"Using attached reference as identity; change only: [angle], [setting], [expression]."*
4. Run the slop gate on hero and each edit before Phase D.

Performance still rules:

- **Entire face visible**, mouth open mid-word
- **Slight angle from the side** — not “facing camera” in still prompts
- Vary **`setting_tag`** per chorus pass without reinventing the face

B-roll stills: environment, hands, product, abstract motion plate for I2V — no identity requirement unless the B-roll shows the singer.

Run [./references/music-video-quality-checklist.md](./references/music-video-quality-checklist.md) before Phase D.

## Step 5 — Video clips

### Performance (lip-sync to song slice)

**Human host** (`cast.host_type: human`): **`p-video-avatar`** + `input.audio` — true talking-head lip sync.

**Mascot / stylized host** (`cast.host_type: mascot`): **`p-video`** + `input.image` + `input.audio`. **`p-video-avatar` humanizes non-human stills** — avoid for mascots.

Override with `cast.performance_model: p-video-avatar | p-video` when needed.

| Field | Guidance |
|-------|----------|
| `image` | Approved performance still |
| `audio` | Sliced line/section from master song — **omit `duration`** |
| `save_audio` | **`true`** — embed vocal in clip |
| `video_prompt` | Unique motion per cut — push-in, arc, handheld sway |
| `resolution` | Match plan (default `720p`) |
| `api_seed` | Optional — only when user locks API reproducibility |

Probe slice length when needed:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 slices/01_2.mp3
```

### B-roll (`p-video`)

Prefer **audio-conditioned** mode — upload the same slice, motion follows length:

```json
{
  "prompt": "Slow dolly through neon city street at dusk, rain reflections, cinematic",
  "image": "https://api.pruna.ai/v1/files/STILL_ID",
  "audio": "https://api.pruna.ai/v1/files/SLICE_ID",
  "resolution": "720p",
  "fps": 24,
  "save_audio": true
}
```

Omit `duration` when `audio` is set. For `[Inst]` / `[Solo]` with no vocals, use `duration` from cut map instead of audio.

**Parallelize** independent clips after confirmation — `pruna-api`.

## Step 6 — Assemble

Name clips to match cut ids (e.g. `01_2.mp4`) or set `"clip"` on each cut in the manifest.

1. Trim each clip to its cut duration (or rely on audio-led length matching the slice).
2. Concat video track in cut order:

```bash
ffmpeg -y -f concat -safe 0 -i clips.txt -c copy video_track.mp4
```

3. Mux **full song** as the audio bed:

```bash
ffmpeg -y -i video_track.mp4 -i song.mp3 \
  -map 0:v -map 1:a -c:v copy -c:a aac -shortest music_video.mp4
```

Output: `music_video.mp4` — video from trimmed clips, **full song** on audio.

## Aesthetic guidelines

| Layer | Guidance |
|-------|----------|
| **Color** | Match `music.prompt` palette — warm ballad → golden hour; electronic → split gel neon |
| **Identity** | When `continuity: same_singer`, performance cuts should match hero face/outfit baseline — location and camera may change |
| **Rhythm** | Alternate performance and B-roll on verses; hold singer through chorus hooks |
| **Camera** | No duplicate `video_prompt` on back-to-back cuts |
| **Instrumental breaks** | Go cinematic — wide landscapes, abstract motion, detail macros |
| **Variety** | `generation-diversity` — distinct world per B-roll insert |

## Plan template

Copy [templates/music-video-plan.template.json](./templates/music-video-plan.template.json) or see [examples.md](./examples.md).

## Environment

```bash
export REPLICATE_API_TOKEN=r8_...   # music-2.5 + whisperx
export PRUNA_API_KEY=...          # p-image, p-video-avatar, p-video
```

Requires **`ffmpeg`** and **`ffprobe`**.

## Anti-patterns

- Generating video before lyrics + song + **WhisperX align** are done
- Using proportional lyric timings without WhisperX align — lip sync will drift, especially on rap
- `voice_script` on performance beats when the real song slice should drive lip sync
- Cutting mid-word to hit a beat — always trim on line boundaries
- Same grey-wall performance still for every line
- Fresh **`p-image`** identity pull per performance line when the user wanted one singer
- Skipping **`hero_still`** + edit chain — biggest cause of face drift across a music video
- Skipping review of failed alignment rows when Music 2.5 paraphrased the lyrics

## Related

Related skills:

| Skill | Description | Install |
| --- | --- | --- |
| `music-2.5` | Use when someone wants an original AI song with vocals — sung lyrics, a style prompt track, or source audio for a music video. | `npx skills add PrunaAI/pruna-skills@music-2.5 -y` |
| `whisperx` | Use when someone needs word-level timestamps from audio — lyric alignment, cut-safe line boundaries, or caption source timing before burn-in with video-editing. | `npx skills add PrunaAI/pruna-skills@whisperx -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

