# p-image-upscale-comparison

## Install (portable bundle)

```bash
./scripts/install_skill.sh p-image-upscale-comparison
```

## Dependencies

```bash
pip install -r scripts/requirements.txt
# ffmpeg on PATH
```

## General option (slider renderer)

```bash
python3 ./scripts/generate_upscale_comparison.py --config ./templates/config.template.json
```

Curl path: generate stills via [p-image-upscale](../../../tools/image/p-image-upscale/SKILL.md), then render locally.

## Maintainer recipes (repo clone only)

Not bundled in portable install — rebuild marketing galleries from a full repo clone:

- `examples/workflows/launches/p-image-upscale-comparison/scripts/generate_upscale_prompt_examples.py`
- `examples/workflows/launches/p-image-upscale-comparison/scripts/render_prompt_example_videos.py`
- `examples/workflows/launches/p-image-upscale-comparison/scripts/render_mp_tier_zoom_video.py`
- `examples/workflows/launches/p-image-upscale-comparison/scripts/prepare_*_demo.py`
