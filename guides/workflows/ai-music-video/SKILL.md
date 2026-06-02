---
name: ai-music-video
description: Builds AI music videos — write lyrics with Music 2.5 section tags, generate the song on Replicate, map cut-safe line boundaries, alternate p-video-avatar performance clips and p-video B-roll synced to audio slices, then assemble with ffmpeg. When the user wants one singer throughout, lock a hero still and branch performance frames with p-image-edit plus project_seed — not fresh identity pulls per line. Use when the user wants a music video, lyric video, sung promo, or MiniMax song + Pruna video.
license: MIT
metadata:
  version: "0.0.1"
---

# AI music video (lyrics → song → synced clips)

End-to-end **music video** production:

1. **Lyrics** with [Music 2.5 structure tags](https://replicate.com/minimax/music-2.5) — cut on **line boundaries**, never mid-word ([lyrics-and-cuts.md](./lyrics-and-cuts.md))
2. **Song** — [music-2.5](../../../tools/audio/music-2.5/SKILL.md) on Replicate (`REPLICATE_API_TOKEN`)
3. **Cut map** — `parse_lyric_cuts.py` → per-line/per-section timings (refine by ear)
4. **Visual beats** — **`p-video-avatar`** (performance, lip sync to **audio slice**) + **`p-video`** B-roll via **scene anchor triple variant** (`image` + optional `last_frame_image` + **`audio`** slice) — [scene-anchor-triple.md](../../../references/scene-anchor-triple.md)
5. **Assembly** — trim clips to cut durations, concat, mux full song

**Staged generation:** [staged-generation-gate.md](../../../references/staged-generation-gate.md) — approve lyrics and stills before paid video jobs.

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
| **Beat mix** | Performance-heavy vs B-roll-heavy? Default: alternate on verses, performance on chorus |

Do **not** call Music 2.5 or Pruna video until lyrics are approved.

## Character continuity (when intended)

Ask whether performance beats should read as **one singer** or whether **recasts** are deliberate. Default assumption when the user names a single artist: **same person on every performance cut**.

| Intent | Stills | Video | Anti-pattern |
|--------|--------|-------|--------------|
| **Same singer throughout** | One approved **hero** via `p-image` (locked `project_seed`) → every performance still via **`p-image-edit`** off that URL — change only angle, setting, expression, wardrobe *delta* | Pass **`seed`: `project_seed`** on all **`p-video-avatar`** jobs; reuse `cast_descriptor` in edit prompts | Fresh unrelated **`p-image`** text prompt per line — faces drift |
| **Same singer, new locations** | Hero + edits per beat — vary **`setting_tag`**, **`camera_tag`**, **`lighting_tag`**; keep identity anchors (age, hair, face, baseline outfit) in the character sheet | Same seed lock; distinct **`video_prompt`** per cut | Grey-wall repeat or identical framing on consecutive performance lines |
| **Deliberate recasts** | Only on **broll** beats, labeled guest rows, or when the user explicitly asks — never silent identity swaps on back-to-back performance lines | N/A for lip-sync rows | Random new face mid-chorus without user approval |
| **Mascot / stylized host** | One approved mascot still → **`p-image-edit`** for pose/setting | **`p-video`** scene anchor triple: `image` + optional `last_frame_image` + song **`audio`** slice | **`p-video-avatar`** on non-human stills |

Record in the plan: `project_seed`, `cast` / `character_sheet`, approved **`hero_still`** URL, and `continuity: same_singer | recasts_ok`. Full cast-ledger patterns: [multi-scene-avatar-video](../multi-scene-avatar-video/SKILL.md) **Character sheet** and **Source portrait / hero**.

## Pipeline phases

| Phase | Models | Cost | Gate |
|-------|--------|------|------|
| **0 — Lyrics** | none | free | User approves lyric sheet + section tags |
| **A — Song** | `music-2.5` | medium | User approves MP3 |
| **B — Cut map** | local scripts | free | User approves timings (listen once) |
| **C — Stills** | `p-image` / `p-image-edit` | low | Per [staged-generation-gate.md](../../../references/staged-generation-gate.md) |
| **D — Clips** | `p-video-avatar`, `p-video` | **high** | After still approval |
| **E — Assembly** | ffmpeg | free | Review final MP4 |

```text
Lyrics + music.prompt
  → music-2.5 (song.mp3)
  → parse_lyric_cuts.py (cut_manifest.json)
  → refine start_sec/end_sec by ear
  → p-image stills per segment
  → slice_audio.py per cut → upload → p-video-avatar (performance) / p-video (broll)
  → assemble_music_video.py → music_video.mp4
```

## Step 1 — Write lyrics

Use section tags and **one phrase per line**. See [lyrics-and-cuts.md](./lyrics-and-cuts.md).

Store in plan JSON:

```json
{
  "music": {
    "prompt": "Indie pop, uplifting, warm female vocal, 92 BPM, acoustic guitar and soft synth pads"
  },
  "lyrics": "[Verse]\nFirst line here\nSecond line here\n\n[Chorus]\nHook line one\nHook line two"
}
```

**Cut rule:** every `\n` in sung text is a candidate cut point. Blank lines between sections = scene breaks.

## Step 2 — Generate song

```bash
python3 guides/workflows/ai-music-video/scripts/generate_song.py \
  --plan output/my-mv/music_video_plan.json \
  --out-dir output/my-mv
```

Or curl via [music-2.5 SKILL.md](../../../tools/audio/music-2.5/SKILL.md).

## Step 3 — Build and refine cut map

```bash
python3 guides/workflows/ai-music-video/scripts/parse_lyric_cuts.py \
  --plan output/my-mv/music_video_plan.json \
  --song output/my-mv/song.mp3 \
  --out output/my-mv/cut_manifest.json
```

Each cut entry includes:

| Field | Purpose |
|-------|---------|
| `beat_type` | `performance` → lip-sync clip · `broll` → cinematic |
| `cast.host_type` | `human` → performance uses **`p-video-avatar`** + audio slice · `mascot` → performance uses **`p-video`** + audio (preserves character; avatar model humanizes non-human stills) |
| `cast.performance_model` | Optional override: `p-video-avatar` or `p-video` for all performance beats |
| `lines` | Lyric lines in this clip — **never split a line across clips** |
| `start_sec` / `end_sec` | Trim window in the master song — **adjust by ear** |
| `clip` | Filename in `clips/` (set when clips are rendered) |

## Step 4 — Stills (`p-image` / `p-image-edit`)

One approved still per segment.

**When continuity is intended (default for one singer):**

1. Generate and gate **one hero** performance still with **`p-image`** + locked **`project_seed`**.
2. Store the approved URL as **`hero_still`** in the plan.
3. Every later performance still = **`p-image-edit`** from **`hero_still`** — *"Using attached reference as identity; change only: [angle], [setting], [expression]."*
4. Run the slop gate on hero and each edit before Phase D.

Performance still rules (hero and edits):

- **Entire face visible**, mouth open mid-word
- **Slight angle from the side** — not “facing camera” in still prompts ([p-video-replace trigger patterns](../../../guides/workflows/p-video-replace-comparison/SKILL.md) apply to portrait stills)
- Vary **`setting_tag`** per chorus pass — loft, rooftop, neon corridor — without reinventing the face

B-roll stills: environment, hands, product, abstract motion plate for I2V — no identity requirement unless the B-roll shows the singer.

Run [music-video-quality-checklist.md](../../../references/music-video-quality-checklist.md) before Phase D.

## Step 5 — Video clips

### Performance (lip-sync to song slice)

**Human host** (`cast.host_type: human`): **`p-video-avatar`** + `input.audio` — true talking-head lip sync.

**Mascot / stylized host** (`cast.host_type: mascot`): **`p-video`** + `input.image` + `input.audio` — matches [Pruna's music-video guide](https://docs.pruna.ai/en/stable/docs_pruna_endpoints/performance_models/workflows/music_to_video.html). **`p-video-avatar` humanizes non-human stills** into generic avatars; avoid it for knitted mascots, fox presenters, etc.

Override with `cast.performance_model: p-video-avatar | p-video` when needed.

```bash
python3 guides/workflows/ai-music-video/scripts/slice_audio.py \
  --song output/my-mv/song.mp3 --start 12.4 --end 16.8 \
  --out output/my-mv/audio/cut_01_2.mp3
# Upload slice → POST /v1/files → pass URL as input.audio
```

| Field | Guidance |
|-------|----------|
| `image` | Approved performance still |
| `audio` | Sliced line/section from master song — **omit `duration`** |
| `save_audio` | **`true`** — embed vocal in clip (required for audio-led cuts) |
| `video_prompt` | Unique motion per cut — push-in, arc, handheld sway |
| `resolution` | Match plan (`1080p` for final) |
| `seed` | Lock for same singer across performance clips |

### B-roll (`p-video`)

Prefer **audio-conditioned** mode — upload the same slice, motion follows length:

```json
{
  "prompt": "Slow dolly through neon city street at dusk, rain reflections, cinematic",
  "image": "https://api.pruna.ai/v1/files/STILL_ID",
  "audio": "https://api.pruna.ai/v1/files/SLICE_ID",
  "resolution": "1080p",
  "save_audio": true
}
```

Omit `duration` when `audio` is set. Runner: [`run_from_plan.py`](./scripts/run_from_plan.py) uses [`p_video_payload.py`](../_shared/scripts/p_video_payload.py).

For `[Inst]` / `[Solo]` with no vocals, use `duration` from cut map instead of audio.

**Parallelize** independent clips after confirmation — [parallel-execution.md](../../../references/parallel-execution.md).

## Step 6 — Assemble

Name clips to match cut ids (e.g. `01_2.mp4`) or set `"clip"` on each cut in the manifest.

```bash
python3 guides/workflows/ai-music-video/scripts/assemble_music_video.py \
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
| **Variety** | [visual-variety-bible.md](../../../references/visual-variety-bible.md) — distinct world per B-roll insert |

## Plan template

Copy [`templates/music-video-plan.template.json`](./templates/music-video-plan.template.json) or see [examples.md](./examples.md).

## Environment

```bash
export REPLICATE_API_TOKEN=r8_...   # music-2.5
export PRUNA_API_KEY=...          # p-image, p-video-avatar, p-video
```

Requires **`ffmpeg`** and **`ffprobe`**.

## Anti-patterns

- Generating video before lyrics + song + cut map are approved
- `voice_script` on performance beats when the real song slice should drive lip sync
- Cutting mid-word to hit a beat — always trim on line boundaries
- Same grey-wall performance still for every line
- Fresh **`p-image`** identity pull per performance line when the user wanted one singer
- Skipping **`hero_still`** + edit chain — biggest cause of face drift across a music video
- Skipping the listen pass on `start_sec` / `end_sec` after proportional allocation

## Related

| Resource | Path |
|----------|------|
| Music 2.5 tool | [music-2.5](../../../tools/audio/music-2.5/SKILL.md) |
| Lyric + cut rules | [lyrics-and-cuts.md](./lyrics-and-cuts.md) |
| Avatar API | [p-video-avatar](../../../tools/video/p-video-avatar/SKILL.md) |
| Cinematic API | [p-video](../../../tools/video/p-video/SKILL.md) |
| Scenario hub | [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md) recipe **O** |
| QA | [music-video-quality-checklist.md](../../../references/music-video-quality-checklist.md) |
