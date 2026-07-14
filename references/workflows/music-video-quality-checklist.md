# Music video quality checklist

Run at lyrics approval, after song generation, on stills, and on final assembly.

## Lyrics gate

- [ ] Section tags present (`[Verse]`, `[Chorus]`, `[Inst]`, etc.)
- [ ] **One sung phrase per line** — cuts will land on `\n` boundaries
- [ ] Chorus lyrics identical on repeats (if reusing clips)
- [ ] No tongue-twister lines unless intentional
- [ ] `music.prompt` names genre, mood, vocal, tempo, instruments

## Song gate

- [ ] Vocals intelligible; pronunciation acceptable for target language
- [ ] Section boundaries audible (verse vs chorus vs instrumental)
- [ ] Duration fits deliverable (typically 2:30–4:30 for full songs)
- [ ] MP3 downloaded and stored beside plan

## Cut map gate

- [ ] `parse_lyric_cuts.py` run with `--song` after generation
- [ ] **Listened once** — `start_sec` / `end_sec` refined; no cut mid-word
- [ ] Performance cuts cover full sung lines with ~50–150 ms tail padding
- [ ] `[Inst]` / `[Solo]` mapped to `broll` beats
- [ ] Chorus cuts prefer single performance clips per section

## Stills gate (before `p-video-*`)

- [ ] **Continuity intent captured** — `continuity: same_singer` vs deliberate recasts documented in plan
- [ ] **Hero anchor** approved for same-singer runs; performance stills derived via **`p-image-edit`** off `hero_still` (not unrelated fresh identity pulls)
- [ ] Performance: face + mouth visible, slight angle from the side
- [ ] Distinct `setting_tag` across consecutive performance clips
- [ ] B-roll stills match music mood (palette, lighting)
- [ ] No readable UI text, laptops screens, or collage trigger words — see [visual-variety-bible.md](../shared/visual-variety-bible.md#prompt-patterns) blocked still phrases where applicable

## Clip gate

- [ ] **Hero plate URL** locked on all **`p-video-avatar`** performance jobs when same-singer continuity is intended
- [ ] Performance uses **`input.audio`** slice — not mismatched `voice_script`
- [ ] Lip sync acceptable for performance segments
- [ ] B-roll motion matches audio energy
- [ ] Clip filenames match cut manifest ids

## Assembly gate

- [ ] Concat order matches cut manifest timeline
- [ ] Final MP4 muxes **full master song** (not per-clip audio fragments)
- [ ] No visible flash/jump at cut points on downbeats
- [ ] Total runtime matches song (within trim tolerance)

## Related

- [music-video SKILL](../workflows/verticals/music-video/SKILL.md)
- [lyrics-and-cuts.md](../workflows/verticals/music-video/lyrics-and-cuts.md)
- [generation-quality-checklists.md](./generation-quality-checklists.md)
