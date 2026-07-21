# Lyrics and cut-safe editing

How to write lyrics for [Music 2.5](https://replicate.com/minimax/music-2.5) and map them to video clips **without cutting mid-word**. Workflow skill: `music-video`.

## Pipeline (lyrics → align)

| Step | Who / skill | Output |
|------|-------------|--------|
| 1 — Lyrics | Plan JSON `music` + `lyrics` | User approves lyric sheet |
| 2 — Song | `music-2.5` | `song.mp3` — **approve song** |
| 3a — Structure | Agent builds cut list from lyric lines | `cut_manifest.json` (line boundaries) |
| 3b — Timings | `whisperx` | Word-level `start_sec` / `end_sec` — **required before video** |

Do **not** generate video until **3b** completes — proportional timings drift on rap and paraphrased vocals.

Follow [SKILL.md — How the agent runs this](./SKILL.md#how-the-agent-runs-this). No Python runner — the agent uses curl + ffmpeg.

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

Full tag list: [music-2.5 SKILL.md](../../audio/music-2.5/SKILL.md#structure-tags).

## Cut manifest

After lyrics are approved, build a cut map from lyric lines (one clip per line / section). After the song exists, align with WhisperX and write `start_sec` / `end_sec` onto each cut — never use proportional timings for video.

```bash
OUT=output/my-mv
# After song.mp3 exists — agent runs whisperx skill, then updates cut_manifest.json
```

See `whisperx` and `this skill`.

### Default beat assignment

| Section | Default clip type | Why |
|---------|-------------------|-----|
| `[Verse]` / `[Pre Chorus]` | Alternate **performance** / **broll** per line | Variety without breaking lip sync |
| `[Chorus]` | **performance** (whole section) | Hook stays on singer |
| `[Inst]` / `[Solo]` / `[Break]` | **broll** | No lip sync — cinematic `p-video` |
| `[Intro]` / `[Outro]` | **broll** or short performance | Mood setting |

Override any cut in the plan with explicit `"beat_type": "performance" | "broll"`.

## Refining timings

**Preferred:** after the song exists, run `whisperx` and map each planned lyric line to a measured span (`start_sec` / `end_sec`).

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

**Performance stills:** when the user wants one singer throughout, land **one hero** with `p-image` + [random seed ritual](../../guides/generation-diversity/references/generation-diversity.md#random-seed-ritual-mandatory-before-every-generation), then **`p-image-edit`** every performance frame off that URL — mouth visible, statement wardrobe, varied setting per chorus pass. Only mint a fresh identity with unrelated `p-image` prompts when recasts are deliberate (usually B-roll only).

**B-roll prompts:** match **mood + palette** of the music prompt — golden hour for warm ballads, neon for electronic, etc. See [generation-diversity.md#visual-variety](../../guides/generation-diversity/references/generation-diversity.md#visual-variety).

## Aesthetic rhythm (not just sync)

Alternate energy across the timeline:

```text
Intro (broll, wide) → Verse line (performance, medium) → Verse line (broll, detail)
→ Pre-chorus (performance, push-in) → Chorus (performance, hero angle)
→ Inst (broll, motion) → Verse 2 … → Bridge (new location) → Final chorus
```

**Camera grammar:** never repeat the same `video_prompt` on consecutive cuts — dolly, arc, crane, handheld sway (`this skill` variety table).

## Anti-patterns

- **`voice_script`** on performance beats when you have the real song — use **`audio`** slice so lip sync matches the track.
- One grey-wall performance clip for every line — rotate settings per [generation-diversity](../../guides/generation-diversity/references/generation-diversity.md#visual-variety).
- New **`p-image`** identity per performance line when continuity was intended — use hero + **`p-image-edit`** instead.
- Cutting on beat without checking **syllable endings** — proportional timing can drift; always listen once.
- Lyrics that don't match section tags — model may blur section boundaries and break your cut map.

## Related

- `music-2.5`
- `p-video-avatar`
- `p-video`
- `whisperx`
