# Comparison sliders

Side-by-side **before/after** or **motion template vs animated** clips. Used in `avatar-multi-scene` animate beats and product comparison reels.

## Side-by-side (hstack)

Scale both inputs to half width, stack horizontally:

```bash
ffmpeg -y -i left.mp4 -i right.mp4 \
  -filter_complex "[0:v]scale=960:1080[l];[1:v]scale=960:1080[r];[l][r]hstack=inputs=2[v]" \
  -map "[v]" -map 1:a? -c:v libx264 -crf 20 -preset veryfast -c:a aac -shortest compare.mp4
```

Adjust `scale=W:H` to match target canvas (e.g. 1920×1080 → 960×1080 per panel).

## Labels (optional)

Add `drawtext` on each half before hstack, or burn labels in a second pass — see [overlays.md](./overlays.md).

## Vertical stack (vstack)

Portrait comparisons (before top, after bottom):

```bash
-filter_complex "[0:v]scale=1080:960[t];[1:v]scale=1080:960[b];[t][b]vstack=inputs=2[v]"
```

## Animated wipe slider

For interactive wipes, a full motion-graphic pass may be easier in [Hyperframes](./combination-hyperframes.md). For a simple static split, hstack is enough.

## Next steps

- Concat comparison clips into a reel → [assembly-concat.md](./assembly-concat.md)
- Transitions between segments → [transitions.md](./transitions.md)
