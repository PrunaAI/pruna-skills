# Example prompt: mixed avatar + animate announcement

Use **[multi-scene-avatar-video](../../../guides/workflows/multi-scene-avatar-video/SKILL.md)** with a scene table mixing **`avatar`** and **`animate`** rows. Model guidance: [animate-beats.md](../../../guides/workflows/multi-scene-avatar-video/animate-beats.md).

## Prompt

> Create a **P-Video-Animate** product announcement (~45–60s). Mix talking-head beats with slider comparison demos.
>
> **Eye-catching variety:** each animate slider row uses 3–4 persona stills in **different visual styles** — photoreal UGC, premium anime, claymation, Disney/Pixar 3D, cyberpunk, blockbuster film, AAA game — each with its **own background, camera angle, and lighting**. Alternate cast gender and representation across avatar rows. See [visual-variety-bible.md](../../../references/visual-variety-bible.md).
>
> Product points: motion transfer from source video onto reference image; fast inference; pricing; use cases (UGC variations, meme remixes, scene recasting, game cinematics).
>
> Animate rows: hero edit → **speaking** motion template (`p-video-avatar`) → persona stills → `p-video-animate` → slider MP4. Avatar rows: hero edit → `p-video-avatar`. End with a short CTA on the hero spokesperson.

## Example scene table

| # | Type | Beat |
|---|------|------|
| 1 | avatar | Hook — spokesperson intro |
| 2 | animate | Slider — UGC motion, 4 persona styles (photoreal · anime · clay · Disney 3D) |
| 3 | avatar | Feature / speed proof |
| 4 | animate | Slider — second motion template |
| 5 | avatar | CTA |

Or slider-heavy: rows 1–N all **`animate`**, final row **`avatar`** CTA.

## Run

Portable (installed skill or repo skill path):

```bash
export PRUNA_API_KEY="your_key"
pip install -r guides/workflows/p-video-animate-comparison/scripts/requirements.txt

python3 guides/workflows/p-video-animate-comparison/scripts/run_from_plan.py \
  --plan output/p-video-animate-announcement/announcement_plan.json \
  --out-dir output/p-video-animate-announcement \
  --phase stills
```

After reviewing stills: `--approve-stills --phase video`

Repo clone wrapper: `python3 scripts/run_p_video_animate_announcement.py --phase stills`

Config templates: [`examples/workflows/p-video-animate-comparison/`](./)

## Motion-template rule

When **`p-video-avatar`** generates a motion source for **`p-video-animate`**, **`video_prompt`** must request **speaking** — lip movement and explain gestures — not smile/wave only.
