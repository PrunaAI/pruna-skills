# Scene transition video

Build smooth multi-scene reels: **`p-image`** hero → **`p-image-edit`** start/end stills → **`p-video`** transition between **`image`** and **`last_frame_image`**.

## Quick start prompt

> Use the **scene-transition-video** workflow. Three-beat cyberpunk alley reel: wide alley → stair climb (chain from prior) → rooftop hard cut. Generate hero with **p-image**, branch start/end stills with **p-image-edit**, render each beat with **p-video** using OPEN/MID/CLOSE transition prompts and 4–5s duration. Use **`extract_last_frame`** chaining on scene 2 only; hard cut before rooftop. Concat with 0.15s crossfade on chain joins. 16:9, 720p.

## Copy plan template

```bash
mkdir -p output/core/visual-transition-reel/my-transitions/{stills,clips}
cp catalog/workflows/core/visual-transition-reel/templates/transition-plan.template.json \
   output/core/visual-transition-reel/my-transitions/plan.json
```

Edit scene `edit_prompt`, `last_frame_edit_prompt`, and `video_prompt` rows, then:

```bash
python3 catalog/workflows/core/visual-transition-reel/scripts/run_from_plan.py \
  --plan output/core/visual-transition-reel/my-transitions/plan.json \
  --out-dir output/core/visual-transition-reel/my-transitions
```

## Install skill bundle

```bash
npx skills add PrunaAI/pruna-ai-content-generation-skills/skills --skill visual-transition-reel --agent cursor -y
```

## Related

- Visual-only spec: [scene-anchor-pair.md](../../../../catalog/references/video/scene-anchor-pair.md)
- With narration: [narrated-multi-scene](../../../../catalog/workflows/core/narrated-multi-scene/SKILL.md)
