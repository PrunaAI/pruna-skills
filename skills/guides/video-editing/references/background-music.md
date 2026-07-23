# Background music (bed mix)

Loop an **instrumental bed** under dialogue, avatar VO, or narration. The bed supports the voice — it must not compete with or replace it.

## Generate the bed first

Use `stable-audio-2.5` for instrumental underscore (no vocals). Bed **prompt craft** lives in `audio-prompting`.

Reuse an existing file when `"reuse_bed": true` and `launch_bed.mp3` (or project bed path) already exists — do not regenerate unless the user asks for a new prompt or seed.

## Volume targets

| Context | Bed volume (`volume=` filter) |
|---------|-------------------------------|
| Launch / promo under clear speech | **~0.20** (default) |
| Dense narration / soft VO | **~0.08–0.12** |
| Silent B-roll montage | **~0.15–0.25** (no dialogue to mask) |

Start at **0.20** for launch-style reels; duck lower if the bed fights the voice.

## Bed under existing video audio

Video stream `0` carries dialogue/VO on `0:a`. Bed is stream `1`:

```bash
ffmpeg -y -i video_with_vo.mp4 -i launch_bed.mp3 \
  -filter_complex "[1:a]volume=0.20,aloop=loop=-1:size=2e+09[bed];[0:a][bed]amix=inputs=2:duration=first:dropout_transition=0[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -shortest output.mp4
```

- `duration=first` — mix length follows the video
- `aloop` — extend short bed loops to full runtime
- `-c:v copy` when no video filters run

## Bed on silent concat (no VO track)

```bash
ffmpeg -y -i silent_reel.mp4 -i bed.mp3 \
  -filter_complex "[1:a]volume=0.15,aloop=loop=-1:size=2e+09[bed]" \
  -map 0:v -map "[bed]" -c:v copy -c:a aac -b:a 192k -shortest output.mp4
```

## Hyperframes compositions

**Embed** bed in HTML when one render is enough (`data-volume` ~0.10–0.20 vs narration) — see [combination-hyperframes.md](./combination-hyperframes.md).

**Post-mux** bed after caption burn when iterating captions or bed level: render can be VO-only; burn subs first; then `amix` with `-c:v copy` (recipe above). Prefer this path for promo reels with phrase-bar + word-accent captions.

## Anti-patterns

- Full song with vocals as a “bed” under speech — use instrumental only
- Bed louder than VO — if speech is hard to follow, drop to ~0.10
- Replacing native clip audio with bed only — keep primary dialogue on `0:a`

## Next steps

- Concat before bed → [assembly-concat.md](./assembly-concat.md)
- Loudness pass after mix → [export-presets.md](./export-presets.md)
