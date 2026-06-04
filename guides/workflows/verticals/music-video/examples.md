# AI music video examples

## Purple Pruna rap (shipped reference)

Mascot battle rapper — **`cast.host_type: mascot`** → all performance beats use **`p-video`** + song **`audio`** slices (not `p-video-avatar`).

```bash
OUT=output/verticals/music-video/purple-pruna-rap
# Final: $OUT/purple_pruna_rap.mp4
```

See [`music_video_plan.json`](../../../../output/verticals/music-video/purple-pruna-rap/music_video_plan.json) for lyrics, `project_seed`, and segment prompts.

## Human rapper (lip-sync performance)

Set **`cast.host_type: human`** in the plan. Performance sections → **`p-video-avatar`** + `input.audio` slice. B-roll → **`p-video`**. Entire face visible in stills; slight angle from the side.

## Indie pop — skills library theme

Plan template: [`templates/music-video-plan.template.json`](./templates/music-video-plan.template.json)

**Pipeline:**

```bash
OUT=output/verticals/music-video/my-music-video
mkdir -p "$OUT/clips" "$OUT/audio" "$OUT/stills"

# 1. Approve lyrics in plan → generate song → cut structure + WhisperX align
python3 guides/workflows/verticals/music-video/scripts/run_from_plan.py \
  --plan "$OUT/music_video_plan.json" --out-dir "$OUT" --phase song

python3 guides/workflows/verticals/music-video/scripts/run_from_plan.py \
  --plan "$OUT/music_video_plan.json" --out-dir "$OUT" --phase cuts

python3 guides/workflows/verticals/music-video/scripts/run_from_plan.py \
  --plan "$OUT/music_video_plan.json" --out-dir "$OUT" --phase align

# 2. Stills + clips (staged — approve stills before full --phase video)
python3 guides/workflows/verticals/music-video/scripts/run_from_plan.py \
  --plan "$OUT/music_video_plan.json" --out-dir "$OUT" --phase stills --only 01_2

python3 guides/workflows/verticals/music-video/scripts/run_from_plan.py \
  --plan "$OUT/music_video_plan.json" --out-dir "$OUT" --phase video --only 01_2

# 3. Assemble when all clips exist
python3 guides/workflows/verticals/music-video/scripts/run_from_plan.py \
  --plan "$OUT/music_video_plan.json" --out-dir "$OUT" --phase assemble
```

Or run `--phase all` after lyrics and still gates are approved. See [whisperx](../../../../tools/audio/whisperx/SKILL.md) for alignment details.

## Beat mix patterns

| Song section | Typical ratio | Visual idea |
|--------------|---------------|-------------|
| Verse | 50% performance / 50% B-roll | Singer + detail inserts |
| Chorus | 80% performance | Hero framing, push-in — reuse hero + edit for same face |
| Inst / Solo | 100% B-roll | City night, nature, abstract motion |
| Bridge | New location performance | Wardrobe or setting change via **`p-image-edit`** off hero |

## Same-singer continuity (typical)

1. Approve one performance **hero** still → set `hero_still` URL in plan.
2. Every performance segment: **`p-image-edit`** from hero — vary setting/camera, not identity.
3. All **`p-video-avatar`** calls: `"seed": project_seed` from plan.
4. B-roll may show hands, city, product — no face required.

See [SKILL.md](./SKILL.md) **Character continuity**.

## Lyric tips for this repo

- Name **concrete nouns** the B-roll can show (*notebook*, *rooftop*, *slider*) — not API jargon in every line.
- Keep chorus **identical** on repeats so you can reuse performance clips or match energy.
- Use `[Inst]` for a 4–8 bar visual break — easiest place for pure `p-video` without lip sync.

See [lyrics-and-cuts.md](./lyrics-and-cuts.md) for cut rules.
