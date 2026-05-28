# Example prompt: P-Image-Upscale comparison video

Works for **any** before/after still pair—not tied to a specific campaign.

## Prompt

> I have a pre-upscale still and the matching `p-image-upscale` output. Build a before/after demo video with three zoom stops and vertical slider sweeps. Scenario: [portrait | product | landscape]. Output 1920×1080 MP4.

## Quick run (CLI, no config)

Portable (installed skill or repo skill path):

```bash
pip install -r guides/workflows/p-image-upscale-comparison/scripts/requirements.txt

python3 guides/workflows/p-image-upscale-comparison/scripts/generate_upscale_comparison.py \
  --before path/to/before.jpg \
  --after path/to/after.jpg \
  --output output/upscale-demo.mp4 \
  --preset portrait
```

## Config-based run

```bash
cp examples/workflows/p-image-upscale-comparison/config.template.json output/my-demo.config.json
# edit paths + regions, then:

python3 guides/workflows/p-image-upscale-comparison/scripts/generate_upscale_comparison.py --config output/my-demo.config.json
```

## Local test fixture (optional)

If the Tellers sample assets exist in this repo:

```bash
python3 guides/workflows/p-image-upscale-comparison/scripts/generate_upscale_comparison.py \
  --config examples/workflows/p-image-upscale-comparison/tellers-scene3.fixture.json
```
