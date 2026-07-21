# AI music video examples

## Purple Pruna rap (shipped reference)

Mascot battle rapper — **`cast.host_type: mascot`** → all performance beats use **`p-video`** + song **`audio`** slices (not `p-video-avatar`).

```bash
OUT=output/music-video/purple-pruna-rap
# Final: $OUT/purple_pruna_rap.mp4
```

Plan JSON holds lyrics, `ritual_seed`, and segment prompts — copy from [templates/music-video-plan.template.json](./templates/music-video-plan.template.json).

## Human rapper (lip-sync performance)

Set **`cast.host_type: human`** in the plan. Performance sections → **`p-video-avatar`** + `input.audio` slice. B-roll → **`p-video`**. Entire face visible in stills; slight angle from the side.

## Indie pop — skills library theme

Plan template: [`templates/music-video-plan.template.json`](./templates/music-video-plan.template.json)

**Pipeline** (agent is the runner — follow `this skill` phase table; curl + ffmpeg, no Python scripts):

```bash
OUT=output/music-video/my-music-video
mkdir -p "$OUT/clips" "$OUT/audio" "$OUT/stills"
cp skills/workflows/music-video/templates/music-video-plan.template.json \
  "$OUT/music_video_plan.json"
```

1. Fill lyrics + `music.prompt` → **approve lyrics**
2. Generate song (`music-2.5`) → **approve song**
3. Build cut structure from lyric lines; align with `whisperx` → `cut_manifest.json`
4. Stills (`p-image` / `p-image-edit`) → **approve stills** before video
5. Performance + B-roll clips → **approve clips**
6. ffmpeg trim / concat / mux full song

See [lyrics-and-cuts.md](./lyrics-and-cuts.md) and [SKILL.md — How the agent runs this](./SKILL.md#how-the-agent-runs-this).

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
3. All **`p-video-avatar`** calls: reuse approved still plate URL; omit API `seed` unless plan sets `api_seed`.
4. B-roll may show hands, city, product — no face required.

See `this skill` **Character continuity**.

## Lyric tips for this repo

- Name **concrete nouns** the B-roll can show (*notebook*, *rooftop*, *slider*) — not API jargon in every line.
- Keep chorus **identical** on repeats so you can reuse performance clips or match energy.
- Use `[Inst]` for a 4–8 bar visual break — easiest place for pure `p-video` without lip sync.

See [lyrics-and-cuts.md](./lyrics-and-cuts.md) for cut rules.
