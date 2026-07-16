# Scene transition video

Build smooth multi-scene reels: **`p-image`** hero → **`p-image-edit`** start/end stills → **`p-video`** transition between **`image`** and **`last_frame_image`**.

## Quick start prompt

> Use the **visual-transition-reel** workflow. Three-beat cyberpunk alley reel: wide alley → stair climb (chain from prior) → rooftop hard cut. Generate hero with **p-image**, branch start/end stills with **p-image-edit**, render each beat with **p-video** using OPEN/MID/CLOSE transition prompts and 4–5s duration. Use **`extract_last_frame`** chaining on scene 2 only; hard cut before rooftop. Concat with 0.15s crossfade on chain joins. 16:9, 720p.

## Copy plan template

```bash
mkdir -p output/core/visual-transition-reel/my-transitions/{stills,clips}
cp workflows/visual-transition-reel/templates/transition-plan.template.json \
   output/core/visual-transition-reel/my-transitions/plan.json
```

Edit scene `edit_prompt`, `last_frame_edit_prompt`, and `video_prompt` rows, then:

```bash
python3 workflows/visual-transition-reel/scripts/run_from_plan.py \
  --plan output/core/visual-transition-reel/my-transitions/plan.json \
  --out-dir output/core/visual-transition-reel/my-transitions
```

## Install skill bundle

```bash
npx skills add PrunaAI/pruna-skills@visual-transition-reel -y
# or: npx plugins add PrunaAI/pruna-skills -y  # pick visual-transition-reel
```

## Related

- Visual-only spec: [scene-anchor-pair.md](./references/scene-anchor-pair.md)
- With narration: [narrated-multi-scene](../../../../workflows/narrated-multi-scene/SKILL.md)
