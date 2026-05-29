# AI music video examples

## Indie pop — skills library theme

Plan template: [`templates/music-video-plan.template.json`](./templates/music-video-plan.template.json)

**Pipeline:**

```bash
OUT=output/my-music-video
mkdir -p "$OUT/clips" "$OUT/audio" "$OUT/stills"

# 1. Approve lyrics in plan → parse cuts
python3 guides/workflows/ai-music-video/scripts/parse_lyric_cuts.py \
  --plan "$OUT/music_video_plan.json" --out "$OUT/cut_manifest.json"

# 2. Generate song (Replicate music-2.5)
python3 guides/workflows/ai-music-video/scripts/generate_song.py \
  --plan "$OUT/music_video_plan.json" --out-dir "$OUT"

# 3. Re-parse with song duration
python3 guides/workflows/ai-music-video/scripts/parse_lyric_cuts.py \
  --plan "$OUT/music_video_plan.json" --song "$OUT/song.mp3" \
  --out "$OUT/cut_manifest.json"

# 4. Per cut: slice audio → p-image still → p-video-avatar (performance) or p-video (broll)
python3 guides/workflows/ai-music-video/scripts/slice_audio.py \
  --song "$OUT/song.mp3" --start 12.4 --end 16.8 \
  --out "$OUT/audio/cut_01_2.mp3"

# 5. Assemble when all clips exist
python3 guides/workflows/ai-music-video/scripts/assemble_music_video.py \
  --plan "$OUT/music_video_plan.json" --cuts "$OUT/cut_manifest.json" \
  --clips-dir "$OUT/clips" --song "$OUT/song.mp3" --out-dir "$OUT"
```

## Beat mix patterns

| Song section | Typical ratio | Visual idea |
|--------------|---------------|-------------|
| Verse | 50% performance / 50% B-roll | Singer + detail inserts |
| Chorus | 80% performance | Hero framing, push-in |
| Inst / Solo | 100% B-roll | City night, nature, abstract motion |
| Bridge | New location performance | Wardrobe or setting change |

## Lyric tips for this repo

- Name **concrete nouns** the B-roll can show (*notebook*, *rooftop*, *slider*) — not API jargon in every line.
- Keep chorus **identical** on repeats so you can reuse performance clips or match energy.
- Use `[Inst]` for a 4–8 bar visual break — easiest place for pure `p-video` without lip sync.

See [lyrics-and-cuts.md](./lyrics-and-cuts.md) for cut rules.
