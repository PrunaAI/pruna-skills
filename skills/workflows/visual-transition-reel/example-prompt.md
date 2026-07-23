# Scene transition video

Build smooth multi-scene reels: **`p-image`** hero → **`p-image-edit`** start/end stills → **`p-video`** transition between **`image`** and **`last_frame_image`**.

## Quick start prompt

> Use the **visual-transition-reel** workflow. Three-beat cyberpunk alley reel: wide alley → stair climb (chain from prior) → rooftop hard cut. Generate hero with **p-image**, branch start/end stills with **p-image-edit**, render each beat with **p-video** using OPEN/MID/CLOSE transition prompts and 4–5s duration. Chain scene 2 from the prior last frame; hard cut before rooftop. Concat with 0.15s crossfade on chain joins. 16:9, 720p.

## Copy plan template

```bash
mkdir -p output/visual-transition-reel/my-transitions/{stills,clips}
cp skills/workflows/visual-transition-reel/templates/transition-plan.template.json \
   output/visual-transition-reel/my-transitions/plan.json
```

Edit scene `edit_prompt`, `last_frame_edit_prompt`, and `video_prompt` rows, then follow the phase table in `this skill` (agent runs curl + ffmpeg — no Python runner).

## Install

```bash
npx skills add PrunaAI/pruna-skills@visual-transition-reel -y
# or: npx skills add PrunaAI/pruna-skills@pruna -y
```

## Related

- Visual-only spec: `video-prompting`
- With narration: `narrated-multi-scene`
