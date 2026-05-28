# Prompt + upscale tier examples

**Repo maintainer only** — not bundled in portable install. Scripts live under `examples/workflows/p-image-upscale-comparison/scripts/`.

Generate diverse `p-image` prompts and compare **32 / 64 / 128 MP** upscales side by side.

```bash
pip install -r guides/workflows/_shared/scripts/requirements.txt
export PRUNA_API_KEY="your_key"

# All 5 examples, default tiers 32,64,128
python3 examples/workflows/p-image-upscale-comparison/scripts/generate_upscale_prompt_examples.py

# Reuse existing before images, only run missing upscale tiers
python3 examples/workflows/p-image-upscale-comparison/scripts/generate_upscale_prompt_examples.py --skip-generate

# Custom tiers / subset
python3 examples/workflows/p-image-upscale-comparison/scripts/generate_upscale_prompt_examples.py --targets 32,64,128 --limit 4
```

Output: `output/p-image-upscale-comparison/prompt-examples/gallery.html`

Render long slider + zoom videos (~24s, 5 zoom stops, 128 MP after):

```bash
python3 examples/workflows/p-image-upscale-comparison/scripts/render_prompt_example_videos.py
python3 examples/workflows/p-image-upscale-comparison/scripts/render_prompt_example_videos.py --ids perfume-product --force
```

Videos: `prompt-examples/<id>/comparison_128mp.mp4`

**MP tier ladder** (5 progressive zooms, each revealing the next tier: 1× → 8× → 32× → 64× → 128×):

```bash
python3 examples/workflows/p-image-upscale-comparison/scripts/render_mp_tier_zoom_video.py --force
```

Output: `prompt-examples/<id>/mp_tier_zoom_ladder.mp4`

Each example folder contains:
- `before_p-image.jpg`
- `after_32mp.jpg` · `after_64mp.jpg` · `after_128mp.jpg`
- `tier_comparison_preview.jpg`
