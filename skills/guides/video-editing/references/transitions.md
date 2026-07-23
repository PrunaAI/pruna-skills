# Transitions (xfade)

Crossfade between clips when hard cuts feel abrupt. Pair **video** `xfade` with **audio** `acrossfade` of the same duration.

## When to use

- Reels and montages where joins should breathe (~0.12–0.5s)
- Visual-only reels (`visual-transition-reel` style)

## When hard-cut is better

- Narrated beats with embedded VO (cuts align to speech)
- Music-video beat edits (cuts align to lyric timestamps)
- Any join where timing is already locked to audio

## Curated transition allowlist

| Name | Feel |
|------|------|
| `fade` | Default crossfade |
| `fadeblack` | Dip through black |
| `wipeleft` / `wiperight` | Directional wipe |
| `slideleft` / `slideright` | Slide |
| `dissolve` | Soft dissolve |
| `circlecrop` | Circular reveal |

Both inputs must match **resolution**, **fps**, **pixel format**, and **timebase**. Normalize first — see [assembly-concat.md](./assembly-concat.md).

## Two-clip crossfade

Offset = duration of first clip **minus** transition duration:

```bash
DUR1=$(ffprobe -v error -show_entries format=duration -of csv=p=0 clip1.mp4)
XF=0.25
OFFSET=$(echo "$DUR1 - $XF" | bc)

ffmpeg -y -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=${XF}:offset=${OFFSET}[v];[0:a][1:a]acrossfade=d=${XF}[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 20 -preset veryfast -c:a aac -b:a 192k out.mp4
```

## Chain three or more clips

Build incrementally: render `clip1+clip2` → temp → xfade with `clip3`. Automate offset math per join (each offset = cumulative duration minus overlap).

**ponytail:** manual offset chains are O(n) re-encodes; fine for ≤5 joins; for long chains prefer planning durations in a table first.

## Timing notes

- `xfade` duration range: 0–60s; reels usually **0.12–0.15s** (subtle) or **0.25–0.5s** (visible)
- Match `acrossfade` `d=` to `xfade` `duration=` for natural audio
- If second clip has no audio, map video only or generate silent audio

## Next steps

- Simple stitch → [assembly-concat.md](./assembly-concat.md)
- Export → [export-presets.md](./export-presets.md)
