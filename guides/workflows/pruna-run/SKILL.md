---
name: pruna-run
description: Fast prompt-to-generation entrypoint for Pruna. Classifies incoming prompts, runs direct image/video/avatar chains, and can dispatch scenario routes I-L. Use when the user says "just run this prompt" or wants minimal setup.
license: MIT
metadata:
  version: "0.0.1"
---

# pruna-run (fast entrypoint)

Use this when the user wants immediate execution from one incoming prompt.

## What it does

- Accepts one prompt and optional overrides.
- Auto-routes to:
  - `image` (`p-image`)
  - `i2v` (`p-image -> p-video`)
  - `avatar` (`p-image -> p-video-avatar`)
  - Scenario routes `I-L` (`ugc-ad-factory`, `product-to-story-reel-builder`, `ecommerce-creative-pack-generator`, `character-ip-content-engine`)
- Writes `manifest.json` in output for reproducibility.

## Run

```bash
export PRUNA_API_KEY="your_key"
python3 scripts/pruna_run.py --prompt "launch teaser for our new product"
```

## Common commands

```bash
# Force talking avatar route (requires script)
python3 scripts/pruna_run.py \
  --route avatar \
  --prompt "friendly spokesperson portrait" \
  --voice-script "Hi, this is our new release in one sentence."

# Force image-to-video chain
python3 scripts/pruna_run.py --route i2v --prompt "cinematic desk product reveal"

# Run scenario route I directly
python3 scripts/pruna_run.py --route I --prompt "ugc hooks for trial campaign"
```

## Notes

- Set `PRUNA_API_KEY` before running.
- Prefer async for video/avatar routes; the script already polls until `succeeded`.
- Multi-scene work: use dedicated workflow skills — narrated films use [scene-anchor-triple.md](../../../references/scene-anchor-triple.md) ([multi-scene-ai-video](../multi-scene-ai-video/SKILL.md)).
