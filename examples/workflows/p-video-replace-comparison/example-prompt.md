# Example prompt: P-Video-Replace comparison announcement

Use **[p-video-replace-comparison](../../../guides/workflows/p-video-replace-comparison/SKILL.md)** with **`replace`** rows (hook/CTA are replace sliders with VO sources, not separate avatar-only clips). Pipeline: [replace-beats.md](../../../guides/workflows/p-video-replace-comparison/replace-beats.md).

## Prompt

> Build a **dynamic** P-Video-Replace launch reel (~60–90s) with slider comparisons. Show **characters**, **clothing-only**, **products/objects**, and **mixed** beats — not only face swap.
>
> **Eye-catching variety:** alternate personas, genders, ethnicities, and archetypes across scenes. Every scene gets a **unique background**, **camera angle**, and **lighting mood**. Include stylized beats — premium anime, claymation, Disney/fairy-tale 3D, cyberpunk, blockbuster movie, AAA game cinematic — especially on scene 1 **persona ladder** refs (each ref = different world + style). Run [visual-variety-bible.md](../../../references/visual-variety-bible.md) checklist before API calls.
>
> For every replace row: set **`replace_target`**, **`source.subject_in_video`**, and **explicit per-reference `instruction_prompt`** in **`multi_job`** mode. Never use a generic "replace the person" line without naming source slots and reference cues.
>
> Sources: default **`p-video-avatar`** — single subject, mouth visible, continuous but controlled camera. Prefer product **in hand** or prop **on desk/chair** over pointing-at-counter UGC, I2V shelf slides, or two-shot cafe. Clothing refs should show the **person wearing** the outfit. Object/clothing beats on VO clips must preserve lips in the instruction.
>
> Avatar VO: **human**, speakable lines — not announcer, not laughy explainer energy unless the beat is meme (scene 7).
>
> Models: dynamic **`p-image`** refs → **`p-video-avatar`** source → **`p-video-replace`** (`multi_job`) → slider MP4. Concat for final reel.
>
> **Optional delivery:** after concat, add chill **instrumental background music** under VO — Replicate [Stable Audio 2.5](https://replicate.com/stability-ai/stable-audio-2.5) via plan `background_music` or `--background-music` on the runner (~0.12 volume; no vocals).

## Example scene table (production-tested)

| # | Type | Target | Mode | Beat |
|---|------|--------|------|------|
| 1 | replace | mixed | `multi_job` | Hook — presenter · blazer · desk product (VO) |
| 2 | replace | mixed | `multi_job` | UGC — creator · tee · tube in hand |
| 3 | replace | clothing | `multi_job` | Stylist talking head — 3 outfits |
| 4 | replace | object | `multi_job` | In-game dialogue — fantasy weapon swap (`p-video-avatar`) |
| 5 | replace | mixed | `multi_job` | Solo cafe — face · jacket · bag on chair |
| 6 | replace | object | `multi_job` | Gym — SKUs + shirt (golden template) |
| 7 | replace | character | `multi_job` | Meme — 3 remixes |
| 8 | replace | mixed | `multi_job` | CTA — presenter · blazer · desk product (VO) |

## Run (after confirmation)

Portable (installed skill or repo skill path):

```bash
export PRUNA_API_KEY="your_key"
pip install -r guides/workflows/p-video-replace-comparison/scripts/requirements.txt

python3 guides/workflows/p-video-replace-comparison/scripts/run_from_plan.py \
  --plan output/p-video-replace-announcement/announcement_plan.json \
  --out-dir output/p-video-replace-announcement \
  --phase stills
```

After reviewing stills:

```bash
python3 guides/workflows/p-video-replace-comparison/scripts/run_from_plan.py \
  --plan output/p-video-replace-announcement/announcement_plan.json \
  --out-dir output/p-video-replace-announcement \
  --approve-stills --phase video
```

- Plan: [`output/p-video-replace-announcement/announcement_plan.json`](../../../output/p-video-replace-announcement/announcement_plan.json)
- Resume: add `--from-scene 3 --approve-stills --phase video`
- Assemble only: `--phase render`
- Assemble + chill bed: `--assemble-only --background-music` (requires `REPLICATE_API_TOKEN`)
- Fresh stills: `--fresh --phase stills`

Plan root may include:

```json
"background_music": {
  "enabled": true,
  "prompt": "Instrumental chill lo-fi ambient bed, soft piano and warm pads, no vocals, 85 BPM",
  "volume": 0.12,
  "output_name": "announcement_with_music.mp4"
}
```

Repo clone wrapper (backward compatible): `python3 scripts/run_p_video_replace_announcement.py --phase stills`

## Config templates

- Single swap: [`config.template.json`](./config.template.json)
- Variant ladder: [`config.multi-sample.template.json`](./config.multi-sample.template.json)
- Batch: [`batch.template.json`](./batch.template.json)
- Plan shape: [`scene-plan.template.json`](./scene-plan.template.json)

## Not this workflow

Motion-transfer → [p-video-animate-comparison](../../../guides/workflows/p-video-animate-comparison/SKILL.md).
