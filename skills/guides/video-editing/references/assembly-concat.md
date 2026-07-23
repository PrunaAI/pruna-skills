# Assembly and concat

Join finished clips in order. Prefer **stream copy** when all inputs match; re-encode only when formats differ or filters are required.

## Prerequisites

- All clips reviewed and approved before concat
- Matching **resolution**, **frame rate**, and **pixel format** when using `-c copy`
- Audio: same sample rate (48 kHz stereo is a safe target) to avoid drift

## Probe first

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 clip.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,pix_fmt -of csv=p=0 clip.mp4
```

## Hard-cut concat (fastest)

Create `clips.txt` (one `file` line per clip, paths escaped or absolute):

```text
file 'scene01.mp4'
file 'scene02.mp4'
file 'scene03.mp4'
```

```bash
ffmpeg -y -f concat -safe 0 -i clips.txt -c copy reel.mp4
```

**When `-c copy` fails:** codecs, resolution, fps, or audio layout differ — normalize each clip first or use the filter concat below.

## Filter concat (re-encode, mixed inputs)

When clips differ in size or fps, scale to a common canvas before concat:

```bash
ffmpeg -y -i a.mp4 -i b.mp4 -i c.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 20 -preset veryfast -c:a aac -b:a 192k out.mp4
```

## Mux external audio onto video

Single narration track over a silent or replaceable-audio concat:

```bash
ffmpeg -y -i concat_video.mp4 -i narration.mp3 \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest output_with_vo.mp4
```

## Normalize before join (when concat fails)

Re-encode mismatched clips to a common spec:

```bash
ffmpeg -y -i in.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30" \
  -af "aresample=48000,aformat=channel_layouts=stereo" \
  -c:v libx264 -crf 20 -preset veryfast -c:a aac -b:a 192k normalized.mp4
```

## Common failures

| Symptom | Fix |
|---------|-----|
| Concat demuxer error | Mismatched streams — normalize or filter concat |
| Audio drift mid-reel | Mixed sample rates — `aresample=48000` on all clips |
| Black frame at joins | Variable fps — force `fps=30` (or target) before concat |
| `-c copy` works but A/V skew | Different timebases — re-encode with filter concat |

## Next steps

- Soft joins → [transitions.md](./transitions.md)
- Bed under existing audio → [background-music.md](./background-music.md)
- Platform export → [export-presets.md](./export-presets.md)
