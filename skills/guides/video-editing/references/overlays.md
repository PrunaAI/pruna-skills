# Overlays (text and logo)

Add title cards, lower-thirds, and watermarks on **finished** video. Requires re-encode on the video stream.

## Timed title card (drawtext)

Center title for first N seconds:

```bash
ffmpeg -y -i input.mp4 \
  -vf "drawtext=text='Product Launch':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,0,3)'" \
  -c:v libx264 -crf 20 -preset veryfast -c:a copy titled.mp4
```

Lower-third for a segment:

```bash
-vf "drawtext=text='Jane Doe — CEO':fontsize=32:fontcolor=white:x=40:y=h-80:enable='between(t,5,12)'"
```

Use `fontfile=/path/to/font.ttf` when the default font is wrong on the host.

## Logo watermark (PNG with alpha)

Bottom-right with padding:

```bash
ffmpeg -y -i input.mp4 -i logo.png \
  -filter_complex "overlay=main_w-overlay_w-20:main_h-overlay_h-20" \
  -c:v libx264 -crf 20 -preset veryfast -c:a copy watermarked.mp4
```

Timed watermark (first 10s only):

```bash
-filter_complex "overlay=20:20:enable='between(t,0,10)'"
```

## Semi-transparent logo

If the PNG has no alpha, fade via `format=rgba,colorchannelmixer=aa=0.7` on the logo input before overlay.

## Stack with captions

Apply overlays **before** or **after** subtitle burn depending on desired z-order:

- Captions on top → burn subs last
- Logo on top of subs → overlay after `ass=` pass (two-pass or single filter_complex chain)

## Next steps

- Side-by-side compare → [comparison-sliders.md](./comparison-sliders.md)
- Export → [export-presets.md](./export-presets.md)
