---
name: music-video
description: Use when someone wants a full music video — original song or vocals, performance clips, B-roll, and lyric-synced edits.
license: MIT
metadata:
  version: "1.0.4"
---

# AI music video (lyrics → song → synced clips)

End-to-end **music video** production:

1. **Lyrics** with [Music 2.5 structure tags](https://replicate.com/minimax/music-2.5) — cut on **line boundaries**, never mid-word ([lyrics-and-cuts.md](./lyrics-and-cuts.md))
2. **Song** — [music-2.5](../../../../tools/audio/music-2.5/SKILL.md) on Replicate (`REPLICATE_API_TOKEN`)
3. **Cut map (structure)** — `parse_lyric_cuts.py` → one clip per lyric line / section
4. **Cut map (timings)** — [whisperx](../../../../tools/audio/whisperx/SKILL.md) + `align_lyric_cuts.py` → word-level `start_sec` / `end_sec` on the **rendered** song
5. **Visual beats** — model routing below — then assemble with ffmpeg
6. **Assembly** — trim clips to cut durations, concat, mux full song

**Staged generation:** [staged-generation-gate.md](../../../../../references/shared/staged-generation-gate.md) — approve lyrics and stills before paid video jobs.

## Quick reference

| Resource | Path |
|----------|------|
| Lyrics, cuts, align pipeline | [lyrics-and-cuts.md](./lyrics-and-cuts.md) |
| Runner | [`run_from_plan.py`](./scripts/run_from_plan.py) · `--phase song\|align\|stills\|video\|assemble` |
| Plan template | [`music-video-plan.template.json`](./templates/music-video-plan.template.json) |
| Feedback | [requesting-generation-feedback](../../router/requesting-generation-feedback/SKILL.md) |
| QA | [music-video-quality-checklist.md](../../../../../references/workflows/music-video-quality-checklist.md) |

## Model routing (performance vs B-roll)

| Beat | Human singer / rapper | Mascot or stylized host |
|------|----------------------|-------------------------|
| **Performance** (lip sync to song) | **[`p-video-avatar`](../../../../tools/video/p-video-avatar/SKILL.md)** — `image` + **`audio`** slice from master song. **Not** `voice_script`. | **[`p-video`](../../../../tools/video/p-video/SKILL.md)** — `image` + **`audio`** slice ([Pruna music-to-video](https://docs.pruna.ai/en/stable/docs_pruna_endpoints/performance_models/workflows/music_to_video.html)). **`p-video-avatar` humanizes non-human stills** — avoid on mascots. |
| **B-roll** | **`p-video`** — still + **`audio`** slice (or `duration` on instrumentals) | Same |

Set in the plan: `cast.host_type` (`human` | `mascot`) and optional `cast.performance_model` override. The runner ([`run_from_plan.py`](./scripts/run_from_plan.py)) picks the model from `beat_type` + `host_type`.

**Reference shipped video:** [`output/verticals/music-video/purple-pruna-rap/`](../../../../output/verticals/music-video/purple-pruna-rap/) — mascot battle rap, **`p-video`** performance + B-roll, audio-conditioned slices → `purple_pruna_rap.mp4`.

**Human rapper pattern:** `cast.host_type: human` → performance sections use **`p-video-avatar`** + song slice; B-roll stays **`p-video`**.

## Intake: ask before generating

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
| **Same singer throughout** | One approved **hero** via `p-image` (locked plate URL) → every performance still via **`p-image-edit`** off that URL — change only angle, setting, expression, wardrobe *delta* | Reuse hero plate + `cast_descriptor` on all **`p-video-avatar`** jobs; distinct **`video_prompt`** per cut | Fresh unrelated **`p-image`** text prompt per line — faces drift |
| **Same singer, new locations** | Hero + edits per beat — vary **`setting_tag`**, **`camera_tag`**, **`lighting_tag`**; keep identity anchors (age, hair, face, baseline outfit) in the character sheet | Same plate lock; distinct **`video_prompt`** per cut | Grey-wall repeat or identical framing on consecutive performance lines |
| **Deliberate recasts** | Only on **broll** beats, labeled guest rows, or when the user explicitly asks — never silent identity swaps on back-to-back performance lines | N/A for lip-sync rows | Random new face mid-chorus without user approval |
| **Mascot / stylized host** | One approved mascot still → **`p-image-edit`** for pose/setting | **`p-video`** scene anchor triple: `image` + optional `last_frame_image` + song **`audio`** slice | **`p-video-avatar`** on non-human stills |

Record in the plan: `ritual_seed`, `cast` / `character_sheet`, approved **`hero_still`** URL, and `continuity: same_singer | recasts_ok`. Full cast-ledger patterns: [avatar-multi-scene](../../core/avatar-multi-scene/SKILL.md) **Character sheet** and **Source portrait / hero**.

## Pipeline phases

| Phase | Models | Cost | Gate |
|-------|--------|------|------|
| **0 — Lyrics** | none | free | User approves lyric sheet + section tags |
| **A — Song** | `music-2.5` | medium | User approves MP3 |
| **B — Cut structure** | local scripts | free | Cut list matches lyric lines |
| **B2 — Cut timings** | [whisperx](../../../../tools/audio/whisperx/SKILL.md) | low | Review `cut_manifest.json` alignment stats |
| **C — Stills** | `p-image` / `p-image-edit` | low | Per [staged-generation-gate.md](../../../../../references/shared/staged-generation-gate.md) |
| **D — Clips** | `p-video-avatar`, `p-video` | **high** | After still approval (`--approve-stills`) |
| **E — Assembly** | ffmpeg | free | After clip approval (`--approve-clips`) |

Default runner **`--phase song`**. Phased flow:

```bash
python3 workflows/verticals/music-video/scripts/run_from_plan.py --plan PLAN --out-dir OUT --phase song
python3 ... --approve-song --phase align
python3 ... --phase stills
python3 ... --approve-stills --phase video
python3 ... --approve-clips --phase assemble
```

Index: [workflow-feedback-gates.md](../../../../../references/workflows/workflow-feedback-gates.md)

```text
Lyrics + music.prompt → song → align → stills → video clips → assemble_music_video.mp4
```

Full lyric format, cut rules, align commands, and cut-manifest fields: **[lyrics-and-cuts.md](./lyrics-and-cuts.md)**.

## Step 4 — Stills (`p-image` / `p-image-edit`)

One approved still per segment.

**When continuity is intended (default for one singer):**

1. Generate and gate **one hero** performance still with **`p-image`** + [random seed ritual](../../../references/shared/random-seed-ritual.md) (SSoT); lock hero plate URL for continuity.
2. Store the approved URL as **`hero_still`** in the plan.
3. Every later performance still = **`p-image-edit`** from **`hero_still`** — *"Using attached reference as identity; change only: [angle], [setting], [expression]."*
4. Run the slop gate on hero and each edit before Phase D.

Performance still rules (hero and edits):

- **Entire face visible**, mouth open mid-word
- **Slight angle from the side** — not “facing camera” in still prompts ([visual-variety-bible.md](../../../references/shared/visual-variety-bible.md#prompt-patterns) blocked still phrases)
- Vary **`setting_tag`** per chorus pass — loft, rooftop, neon corridor — without reinventing the face

B-roll stills: environment, hands, product, abstract motion plate for I2V — no identity requirement unless the B-roll shows the singer.

Run [music-video-quality-checklist.md](../../../../../references/workflows/music-video-quality-checklist.md) before Phase D.

## Step 5 — Video clips

### Performance (lip-sync to song slice)

**Human host** (`cast.host_type: human`): **`p-video-avatar`** + `input.audio` — true talking-head lip sync.

**Mascot / stylized host** (`cast.host_type: mascot`): **`p-video`** + `input.image` + `input.audio` — matches [Pruna's music-video guide](https://docs.pruna.ai/en/stable/docs_pruna_endpoints/performance_models/workflows/music_to_video.html). **`p-video-avatar` humanizes non-human stills** into generic avatars; avoid it for knitted mascots, fox presenters, etc.

Override with `cast.performance_model: p-video-avatar | p-video` when needed.

```bash
python3 workflows/verticals/music-video/scripts/run_from_plan.py \
  --plan output/my-mv/music_video_plan.json \
  --out-dir output/my-mv \
  --phase video --only 01_2 01_3
```

The runner calls `slice_audio.py` with `start_sec` / `end_sec` from the cut manifest (identical to `alignment.audio_slice_*`).

| Field | Guidance |
|-------|----------|
| `image` | Approved performance still |
| `audio` | Sliced line/section from master song — **omit `duration`** |
| `save_audio` | **`true`** — embed vocal in clip (required for audio-led cuts) |
| `video_prompt` | Unique motion per cut — push-in, arc, handheld sway |
| `resolution` | Match plan (default `720p`; use `1080p` when user asks for final delivery) |
| `api_seed` | Optional — only when user locks API reproducibility |

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

Omit `duration` when `audio` is set. Runner: [`run_from_plan.py`](./scripts/run_from_plan.py) uses [`p_video_payload.py`](../_shared/scripts/p_video_payload.py).

For `[Inst]` / `[Solo]` with no vocals, use `duration` from cut map instead of audio.

**Parallelize** independent clips after confirmation — [parallel-execution.md](../../../../../references/shared/parallel-execution.md).

## Step 6 — Assemble

Name clips to match cut ids (e.g. `01_2.mp4`) or set `"clip"` on each cut in the manifest.

```bash
python3 workflows/verticals/music-video/scripts/assemble_music_video.py \
  --plan output/my-mv/music_video_plan.json \
  --cuts output/my-mv/cut_manifest.json \
  --clips-dir output/my-mv/clips \
  --song output/my-mv/song.mp3 \
  --out-dir output/my-mv
```

Output: `music_video.mp4` — video track from trimmed clips, **full song** on audio.

## Aesthetic guidelines

| Layer | Guidance |
|-------|----------|
| **Color** | Match `music.prompt` palette — warm ballad → golden hour; electronic → split gel neon |
| **Identity** | When `continuity: same_singer`, performance cuts should match hero face/outfit baseline — location and camera may change |
| **Rhythm** | Alternate performance and B-roll on verses; hold singer through chorus hooks |
| **Camera** | No duplicate `video_prompt` on back-to-back cuts |
| **Instrumental breaks** | Go cinematic — wide landscapes, abstract motion, detail macros |
| **Variety** | [visual-variety-bible.md](../../../../../references/shared/visual-variety-bible.md) — distinct world per B-roll insert |

## Plan template

Copy [`templates/music-video-plan.template.json`](./templates/music-video-plan.template.json) or see [examples.md](./examples.md).

## Environment

```bash
export REPLICATE_API_TOKEN=r8_...   # music-2.5 + whisperx
export PRUNA_API_KEY=...          # p-image, p-video-avatar, p-video
```

Requires **`ffmpeg`** and **`ffprobe`**.

## Anti-patterns

- Generating video before lyrics + song + **WhisperX align** are done
- Using proportional `parse_lyric_cuts.py` timings without `--phase align` — lip sync will drift, especially on rap
- `voice_script` on performance beats when the real song slice should drive lip sync
- Cutting mid-word to hit a beat — always trim on line boundaries
- Same grey-wall performance still for every line
- Fresh **`p-image`** identity pull per performance line when the user wanted one singer
- Skipping **`hero_still`** + edit chain — biggest cause of face drift across a music video
- Skipping review of `alignment.failed` rows when Music 2.5 paraphrased the lyrics

## Related

| Resource | Path |
|----------|------|
| Lyrics + cuts + align (steps 1–3) | [lyrics-and-cuts.md](./lyrics-and-cuts.md) |
| Feedback discipline | [requesting-generation-feedback](../../router/requesting-generation-feedback/SKILL.md) |
| Music 2.5 tool | [music-2.5](../../../../tools/audio/music-2.5/SKILL.md) |
| WhisperX STT | [whisperx](../../../../tools/audio/whisperx/SKILL.md) |
| Avatar API | [p-video-avatar](../../../../tools/video/p-video-avatar/SKILL.md) |
| Cinematic API | [p-video](../../../../tools/video/p-video/SKILL.md) |
| Scenario hub | [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md) recipe **O** |
| QA | [music-video-quality-checklist.md](../../../../../references/workflows/music-video-quality-checklist.md) |
