# Lyrics and cut-safe editing

How to write lyrics for [Music 2.5](https://replicate.com/minimax/music-2.5) and map them to video clips **without cutting mid-word**.

## Golden rule

**One video cut = one complete lyric line (minimum).** Never trim a clip so a word is split across two shots.

| Safe | Unsafe |
|------|--------|
| Cut after *"Every skill a stepping stone"* | Cut between *"step-"* and *"ping"* |
| New clip at `[Chorus]` tag | Hard cut mid-line on a held note |
| B-roll over `[Inst]` with no sung words | Lip-sync clip shorter than the sung line |

## Lyric format (Music 2.5)

```text
[Intro]
(Soft piano, building)

[Verse]
We built the skills library line by line
Every workflow ready when you need it
From stills to motion, all in one place

[Pre Chorus]
And when the chorus hits you'll know

[Chorus]
Run the pipeline, watch it grow
Pruna models, let them flow
```

### Formatting rules

1. **Section tag** on its own line — `[Verse]`, `[Chorus]`, `[Bridge]`, `[Inst]`, etc.
2. **One sung phrase per line** — 2–4 lines per section reads best for melody.
3. **Blank line** between sections (`\n\n`) — natural pause; good scene boundary.
4. **Parentheticals** for ad-libs, backing vocals, or instrument directions — not cut mid-parenthetical.
5. **Keep lines speakable** — avoid tongue-twisters unless intentional; short words cut cleaner.

Full tag list: [music-2.5 SKILL.md](../../../../tools/audio/music-2.5/SKILL.md#structure-tags).

## Cut manifest (`parse_lyric_cuts.py`)

After lyrics are approved, generate a cut map:

```bash
python3 guides/workflows/verticals/music-video/scripts/parse_lyric_cuts.py \
  --plan output/my-mv/music_video_plan.json \
  --out output/my-mv/cut_manifest.json

# After song exists — proportional timing (fallback only)
python3 guides/workflows/verticals/music-video/scripts/parse_lyric_cuts.py \
  --plan output/my-mv/music_video_plan.json \
  --song output/my-mv/song.mp3 \
  --out output/my-mv/cut_manifest.json

# Preferred — WhisperX word-level alignment on the rendered song
python3 guides/workflows/verticals/music-video/scripts/run_from_plan.py \
  --plan output/my-mv/music_video_plan.json \
  --out-dir output/my-mv \
  --phase align
```

See [whisperx](../../../../tools/audio/whisperx/SKILL.md) and `align_lyric_cuts.py`.

### Default beat assignment

| Section | Default clip type | Why |
|---------|-------------------|-----|
| `[Verse]` / `[Pre Chorus]` | Alternate **performance** / **broll** per line | Variety without breaking lip sync |
| `[Chorus]` | **performance** (whole section) | Hook stays on singer |
| `[Inst]` / `[Solo]` / `[Break]` | **broll** | No lip sync — cinematic `p-video` |
| `[Intro]` / `[Outro]` | **broll** or short performance | Mood setting |

Override any cut in the plan with explicit `"beat_type": "performance" | "broll"`.

## Refining timings

**Preferred:** run `--phase align` after the song exists. [WhisperX](https://replicate.com/victor-upmeet/whisperx) transcribes the rendered MP3 with word-level timestamps; `align_lyric_cuts.py` maps each planned lyric line to a measured span.

**Fallback:** proportional allocation by character count is a rough first pass only. After generating the song:

1. Listen with the cut manifest open.
2. Adjust `start_sec` / `end_sec` on each cut so clips end **between** lines, not inside words.
3. Leave **50–150 ms** padding after the last syllable when trimming performance clips.
4. Re-run assembly — no need to regen video if only timings change.

## Mapping cuts → models

| `beat_type` | Model | Audio input |
|-------------|-------|-------------|
| **performance** (human host) | `p-video-avatar` | Song slice → `input.audio` |
| **performance** (mascot / stylized) | `p-video` | Song slice → `input.audio` — **not** avatar (humanizes non-human stills) |
| **broll** | `p-video` | Same slice or `duration` from cut map |

**Performance stills:** when the user wants one singer throughout, land **one hero** with `p-image` + locked `project_seed`, then **`p-image-edit`** every performance frame off that URL — mouth visible, statement wardrobe, varied `setting_tag` per chorus pass. Only mint a fresh identity with unrelated `p-image` prompts when recasts are deliberate (usually B-roll only).

**B-roll prompts:** match **mood + palette** of the music prompt — golden hour for warm ballads, neon for electronic, etc. See [visual-variety-bible.md](../../../../../references/shared/visual-variety-bible.md).

## Aesthetic rhythm (not just sync)

Alternate energy across the timeline:

```text
Intro (broll, wide) → Verse line (performance, medium) → Verse line (broll, detail)
→ Pre-chorus (performance, push-in) → Chorus (performance, hero angle)
→ Inst (broll, motion) → Verse 2 … → Bridge (new location) → Final chorus
```

**Camera grammar:** never repeat the same `video_prompt` on consecutive cuts — dolly, arc, crane, handheld sway ([SKILL.md](./SKILL.md) variety table).

## Anti-patterns

- **`voice_script`** on performance beats when you have the real song — use **`audio`** slice so lip sync matches the track.
- One grey-wall performance clip for every line — rotate settings per [visual-variety-bible.md](../../../../../references/shared/visual-variety-bible.md).
- New **`p-image`** identity per performance line when continuity was intended — use hero + **`p-image-edit`** instead.
- Cutting on beat without checking **syllable endings** — proportional timing can drift; always listen once.
- Lyrics that don't match section tags — model may blur section boundaries and break your cut map.

## Related

- [music-2.5](../../../../tools/audio/music-2.5/SKILL.md)
- [p-video-avatar](../../../../tools/video/p-video-avatar/SKILL.md)
- [p-video](../../../../tools/video/p-video/SKILL.md)
