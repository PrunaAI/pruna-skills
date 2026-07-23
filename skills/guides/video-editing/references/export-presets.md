# Export presets

Final delivery pass: aspect ratio, loudness, and web-safe encoding.

## Web-safe defaults

Always include for broad playback:

```bash
-pix_fmt yuv420p -movflags +faststart
```

## Social aspect ratios (scale + pad)

Letterbox/pillarbox with black bars — keeps full frame visible:

**16:9 (YouTube, LinkedIn)**

```bash
ffmpeg -y -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,setsar=1" \
  -c:v libx264 -crf 20 -preset veryfast -c:a aac -b:a 192k -pix_fmt yuv420p -movflags +faststart youtube.mp4
```

**9:16 (Reels, TikTok, Shorts)**

```bash
-vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1"
```

**1:1 (Instagram feed)**

```bash
-vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2:black,setsar=1"
```

Use `-2` on one scale dimension when preserving aspect without forcing both axes (e.g. `scale=1080:-2`).

## Loudness normalization (EBU-ish)

After bed mix or uneven scene levels:

```bash
ffmpeg -y -i input.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11" -c:v copy -c:a aac -b:a 192k normalized.mp4
```

`-c:v copy` when video is already final; re-encode if you also scaled.

## Quality presets

| Profile | CRF | Use |
|---------|-----|-----|
| High | 18–20 | Client / launch deliverables |
| Web | 21–23 | Social upload default |
| Preview | 26–28 | Quick review links |

## Mobile-friendly (smaller file)

```bash
ffmpeg -y -i input.mp4 -c:v libx264 -preset fast -crf 28 -vf "scale=1280:-2" -c:a aac -b:a 128k mobile.mp4
```

## Order of operations

Typical final pipeline:

```text
1. Concat / transitions
2. Captions or overlays (re-encode)
3. Bed mix (often -c:v copy)
4. Aspect crop + loudnorm (this doc)
```

## Next steps

- Start of pipeline → [assembly-concat.md](./assembly-concat.md)
