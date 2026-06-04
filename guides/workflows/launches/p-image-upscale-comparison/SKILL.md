---
name: p-image-upscale-comparison
description: Builds a before/after marketing demo video for p-image-upscale—full-frame hook, multiple zoom stops, and vertical slider sweeps— from any pre/post upscale still pair. Use when showcasing upscale quality for portraits, products, landscapes, or pipeline stills.
metadata:
  version: "0.0.1"
---

# P-Image-Upscale comparison video

Turn any **before** (pre-upscale) and **after** (`p-image-upscale`) still pair into a short comparison MP4 with zoom stops and slider reveals.

**Renderer:** [`scripts/generate_upscale_comparison.py`](./scripts/generate_upscale_comparison.py) (portable) · repo wrapper: [`scripts/generate_upscale_comparison.py`](../../../scripts/generate_upscale_comparison.py)  
**Upscale API:** [p-image-upscale](../../../tools/image/p-image-upscale/SKILL.md)  
**Staged generation:** [staged-generation-gate.md](../../../references/shared/staged-generation-gate.md)  
**Quality gate:** [p-image-upscale-quality-checklist.md](../../../references/image/p-image-upscale-quality-checklist.md)

Install: `./scripts/install_skill.sh p-image-upscale-comparison`

### Maintainer recipes (repo clone only — not general options)

Gallery batch scripts live under [`examples/workflows/launches/p-image-upscale-comparison/scripts/`](../../../examples/workflows/launches/p-image-upscale-comparison/scripts/) — do not bundle in portable install.

## Intake: ask before generating

| Topic | Questions |
|-------|-----------|
| **Source pair** | Where is the **before** still (raw `p-image` / `p-image-edit` / upload)? Where is the **after** upscaled file? Same scene/subject? |
| **Target MP** | What `target` was used (typical: **4–8** social, **8–16** hero, up to **128** print)? |
| **Scenario type** | Portrait / product / landscape / generic? Drives default zoom presets. |
| **Zoom stops** | Which 2–4 regions best show the upscale win (face, logo, fabric, horizon, panel detail)? |
| **Delivery** | Output path, duration feel (default ~18–22s), resolution (default 1920×1080)? |

If the user only has a **before** image, run **`p-image-upscale`** first, pass the upscaled output through the quality checklist, then render the comparison.

## Feedback gates (required)

| Phase | What to show | Proceed when |
|-------|--------------|--------------|
| **0 — Plan** | Before/after pair, zoom regions | **approve plan** |
| **A — Upscale QA** | After still passes checklist | **approve still** |
| **B — Render** | Comparison MP4 | User accepts |

## Asset rules (critical)

- **Before** = delivery URL/file **before** upscale (or downscaled copy of the same generation).
- **After** = **`p-image-upscale`** output for that same frame.
- Both sides must represent the **same composition**. The renderer upscales the before image to match after dimensions for pixel-aligned crops.
- Pick zoom regions where blur, mush, or missing detail is obvious at 100% crop—upscale value rarely reads at full frame.

## Workflow (after intake)

1. **Confirm pair** — Run [p-image-upscale-quality-checklist.md](../../../references/image/p-image-upscale-quality-checklist.md) on the after still.
2. **Choose regions** — Start from a preset (`portrait`, `product`, `landscape`, `generic`) or define custom normalized rects (`x`, `y`, `w`, `h` in 0–1).
3. **Write config** — Copy [`config.template.json`](../../../examples/workflows/launches/p-image-upscale-comparison/config.template.json) or generate one:

   ```bash
   python3 scripts/generate_upscale_comparison.py \
     --before path/to/before.jpg \
     --after path/to/after.jpg \
     --output output/my-demo.mp4 \
     --preset portrait \
     --write-config output/my-demo.config.json \
     --dry-run
   ```

4. **Render** — Requires `ffmpeg` and Pillow (`pip install -r scripts/requirements.txt`):

   ```bash
   python3 scripts/generate_upscale_comparison.py --config output/my-demo.config.json
   ```

5. **Manifest** — Log before path, after path, upscale `target` / flags, region list, output MP4 path.

## Config schema

Paths in JSON are resolved relative to the **config file**, then the **current working directory**.

| Field | Required | Notes |
|-------|----------|-------|
| `before` | yes | Pre-upscale still |
| `after` | yes | Upscaled still |
| `output` | yes | Output `.mp4` |
| `regions` | yes* | Array of `{ label, x, y, w, h }` — omit when using `--preset` on CLI |
| `preset` | no | `portrait` · `product` · `landscape` · `generic` (CLI or JSON) |
| `before_mp` / `after_mp` | no | Badge labels; auto-estimated from pixel dimensions if omitted |
| `title` | no | Default `P-Image-Upscale` |
| `fps`, `width`, `height` | no | Default 24, 1920, 1080 |
| `timing` | no | `hook_seconds`, `zoom_seconds`, `slider_seconds`, `hold_after_seconds`, `transition_seconds`, `outro_seconds` |
| `focal_point` | no | `{ x, y, levels?, labels? }` — auto-builds progressive zoom stops |

## Region presets

| Preset | Best for | Stops |
|--------|----------|-------|
| `portrait` | Avatars, headshots, talking-head plates | eyes/skin · hair edge · clothing |
| `product` | Packshots, ecommerce | logo/label · edge · surface |
| `landscape` | Environments, B-roll stills | foreground · mid-frame · horizon |
| `generic` | Unknown / mixed | center · left · right thirds |

Override any preset stop by editing `regions` in the config after `--write-config`.

## Video structure (default timing)

| Beat | ~Duration | Content |
|------|-----------|---------|
| Hook | 2s | Full **before** frame (soft / low-res) |
| Per region | ~2.5s | Zoom in → **slider sweeps left→right** revealing **after** on the left |
| Transition | 0.6s | Pan between regions (when 2+ stops) |
| Outro | 2s | Full **after** frame + MP badge |

### Slider behavior

The vertical divider starts on the **left** (100% before, soft side) and moves **right**, progressively exposing the clearer **after** image from the left edge. Labels: **After** (revealed, left) · **Before** (remaining, right).

For progressive “Where’s Waldo” demos, set a `focal_point` instead of hand-authored regions:

```json
"focal_point": {
  "x": 0.742,
  "y": 0.356,
  "levels": 4,
  "labels": ["Forest overview", "Midground textures", "Hidden in the foliage", "Found Pruna"]
}
```

This creates four zoom stops that tighten around the focal coordinate.

## Restoration example (fake low-res → 128 MP)

Generate a photoreal master, **degrade it** (downscale + blur + heavy JPEG), upscale to **128 MP** with **`enhance_details`** + **`enhance_realism`**, then render a landscape-preset comparison:

```bash
pip install -r examples/workflows/launches/p-image-upscale-comparison/scripts/requirements.txt 2>/dev/null || pip install -r scripts/requirements.txt
export PRUNA_API_KEY="your_key"

python3 examples/workflows/launches/p-image-upscale-comparison/scripts/prepare_restoration_upscale_demo.py
```

Output: `output/launches/p-image-upscale-comparison/restoration-vacation-busy-128mp/`  
Assets: `master_p-image.jpg` · `fake_lowres_before.jpg` · `restored_after_128mp.jpg`

## Prompt examples gallery (quick before/after pairs)

Generate diverse prompt samples and compare **32 / 64 / 128 MP** upscales side by side:

```bash
python3 examples/workflows/launches/p-image-upscale-comparison/scripts/generate_upscale_prompt_examples.py
python3 examples/workflows/launches/p-image-upscale-comparison/scripts/generate_upscale_prompt_examples.py --skip-generate   # missing tiers only
```

Open `output/launches/p-image-upscale-comparison/prompt-examples/gallery.html`.

Render long slider + zoom videos (5 stops each, ~24s):

```bash
python3 examples/workflows/launches/p-image-upscale-comparison/scripts/render_prompt_example_videos.py
python3 examples/workflows/launches/p-image-upscale-comparison/scripts/render_prompt_example_videos.py --ids perfume-product --force
```

Re-run upscale only:

```bash
python3 examples/workflows/launches/p-image-upscale-comparison/scripts/prepare_restoration_upscale_demo.py --skip-generate --skip-degrade
```

Re-render video only:

```bash
python3 examples/workflows/launches/p-image-upscale-comparison/scripts/prepare_restoration_upscale_demo.py --skip-generate --skip-degrade --skip-upscale
```

## Where’s Pruna example (128 MP, nature)

Generate a **photoreal layered nature scene** (foreground · midground · background depth), hide a tiny **Pruna** marker in the foliage, upscale to **128 MP** with **`enhance_details`** + **`enhance_realism`**, then render four progressive zooms:

```bash
pip install -r scripts/requirements.txt
export PRUNA_API_KEY="your_key"

python3 examples/workflows/launches/p-image-upscale-comparison/scripts/prepare_waldo_upscale_demo.py
```

Output directory: `output/launches/p-image-upscale-comparison/nature-pruna-128mp/`  
Re-render only (assets already present):

```bash
python3 examples/workflows/launches/p-image-upscale-comparison/scripts/prepare_waldo_upscale_demo.py --skip-generate --skip-upscale
```

## CLI quick path (no config file)

```bash
python3 scripts/generate_upscale_comparison.py \
  --before assets/before.jpg \
  --after assets/after.jpg \
  --output output/upscale-demo.mp4 \
  --preset product
```

## Related

- Upscale model: [p-image-upscale](../../../tools/image/p-image-upscale/SKILL.md)
- Avatar / motion video (no upscale step): [multi-scene-avatar-video](../core/avatar-multi-scene/SKILL.md)
- Example fixture (optional): [tellers-scene3.fixture.json](../../../examples/workflows/launches/p-image-upscale-comparison/tellers-scene3.fixture.json)
