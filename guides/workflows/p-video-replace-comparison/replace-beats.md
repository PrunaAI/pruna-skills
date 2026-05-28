# Replace beats in comparison reels

How **`p-video-replace`** fits into showcase reels built with [p-video-replace-comparison](./SKILL.md).

## What each model does

| Model | Role in a replace row |
|-------|------------------------|
| **`p-image`** | **Dynamic identity plates** — replacement people, products, mascots, props (not passive headshots) |
| **`p-image-edit`** | Optional — align wardrobe/pose to the source frame, composite props, brand lock from a hero |
| **`p-video-avatar`** | Optional — **generate source footage** when you don't have a licensed template clip |
| **`p-video-replace`** | Swap identities **into** the source video; preserves motion and audio |
| **Slider render** | Original vs replaced MP4 via [`generate_video_comparison.py`](../../../guides/workflows/_shared/scripts/generate_video_comparison.py) |

**`p-video-replace`** takes:

- **`video`** — the scene to keep (motion, camera, audio, environment)
- **`images`** — **1 to 4** reference URLs in **one** call when multiple people/objects swap together

Output keeps **scene structure from the video**, **appearance from the references**.

## Replace row pipeline

```text
Plan replace_target + subject_in_video (who / what is in the source)
  → p-image × N  (reference matched to slot: face, outfit, packshot)
  → optional p-image-edit per reference
  → source video  (upload | p-video-avatar | p-video I2V) — dynamic camera
  → p-video-replace  (video + images[] + mapped instruction_prompt)
  → slider compare MP4
  → ffmpeg concat (final reel)
  → optional background bed (Stable Audio 2.5 + launch_background_music.py)
```

## Plan schema (agent / announcement JSON)

| Field | Where | Purpose |
|-------|-------|---------|
| `replace_target` | replace row | `character` · `clothing` · `object` · `mixed` |
| `replace_mode` | replace row | `multi_job` = one image per API call + variant slider; `single_call` = up to 4 images, one output |
| `source.subject_in_video` | replace row | Plain-language list of what to swap in the source clip |
| `source.still_edit` / `video_prompt` | replace row | Plate + **continuous** motion for generated sources |
| `references[].prompt` | each ref | `p-image` look |
| `references[].instruction_prompt` | each ref | **Required** in `multi_job` — maps source slot → this reference |
| `instruction_prompt` | replace row | **Required** in `single_call` — maps all indices to screen slots |
| `visual_style_tag` | replace row | e.g. `anime_cinematic`, `clay_stop_motion`, `cyberpunk`, `photoreal_ugc` |
| `setting_tag` | replace row | Unique environment label — no duplicate adjacent scenes |
| `camera_tag` | replace row | Shot size / angle (e.g. `low_angle_mc`, `extreme_cu`) |
| `lighting_tag` | replace row | Named light mood (e.g. `neon_night`, `golden_hour`, `practical_clay`) |
| `cast_descriptor` | replace row | One-line identity: age, ethnicity, archetype for prompts |
| `background_music` | plan root | Optional post-concat instrumental bed — see below |

Runner [`run_from_plan.py`](../../../guides/workflows/p-video-replace-comparison/scripts/run_from_plan.py) calls `instruction_for_reference()` — per-reference prompt wins over row default.

### `background_music` (plan root)

After ffmpeg concat, mix a **chill instrumental bed** under avatar VO (does not replace dialogue). Requires `REPLICATE_API_TOKEN`, `ffmpeg`, `ffprobe`.

| Field | Purpose |
|-------|---------|
| `enabled` | `true` to run after assembly (or pass `--background-music` on runner) |
| `prompt` | Stable Audio style tags — e.g. *Instrumental chill lo-fi ambient, soft piano, no vocals, 85 BPM* |
| `volume` | Bed level 0–1 (default **0.12** — keep VO forward) |
| `output_name` | Final MP4 filename beside the silent concat |

Tool: [stable-audio-2.5](../../../tools/audio/stable-audio-2.5/SKILL.md) · mix: [`launch_background_music.py`](../../_shared/scripts/launch_background_music.py)

## What you can replace

**P-Video-Replace** is not only face swap. Plan explicit **`replace_target`** per row:

| Target | Source shows | Reference shows | `instruction_prompt` must say |
|--------|--------------|-----------------|-------------------------------|
| **character** | On-camera person | New identity / cast | Replace the person; keep motion and scene |
| **clothing** | Model in outfit A | Outfit B on similar body pose | Replace **only clothing**; keep face, gait, camera |
| **object** | Product / prop in scene | Hero packshot or prop still | Replace **only that object**; keep hands, table, motion |
| **mixed** | People + props + wardrobe | Refs per slot (1–4 images) | Map each reference to a specific person, garment, or object |

## Dynamic `p-image` references

Replacement stills should read clearly at swap time. Favor **energy and readability** over flat catalog poses. Match **camera energy** in source footage (tracking, orbit, whip-pan) so sliders feel alive.

| Swap type | `p-image` prompt direction |
|-----------|----------------------------|
| Person recast | Action-medium shot, face unobstructed, consistent lighting, wardrobe that fits the scene genre |
| **Clothing only** | Reference shows **same person wearing** the target outfit (talking-head rows); full-body walk rows may use full-body outfit refs — describe garments in `instruction_prompt` |
| **Product / object** | Hero packshot at **matching scale**; instruction names slot (**in hand** preferred over multi-SKU shelf); desk/chair props named by screen position |
| Mascot / stylized character | Bold silhouette; still say what replaces what in the source clip |
| Multi-person / multi-object | **One still per slot**; map left/right, shelf order, or hand-held object in `instruction_prompt` |

Lock a **style bible** across references **in one scene** so the replaced clip feels art-directed. **Across scenes**, vary worlds — see [visual-variety-bible.md](../../../references/visual-variety-bible.md).

Example person prompt:

```text
Documentary street portrait, woman mid-30s, olive skin, curly auburn hair, emerald coat,
walking stride frozen mid-step, sharp face, soft overcast light, 9:16, photoreal, no text.
```

Example product prompt:

```text
Premium skincare tube, matte white label, gold cap, studio product photography,
slight three-quarter angle, crisp typography, neutral gray backdrop, no hands.
```

## Source footage (`p-video-avatar`, `p-video` I2V, or upload)

| Source mode | Best for |
|-------------|----------|
| **`p-video-avatar`** (default) | Single-subject hooks, UGC, wardrobe talking head, in-hand SKU demos, solo cafe explainers — **`voice_script`** on source |
| **`source.plate_mode`: `p-image`** | Male knight / non-hero subjects — fresh `plate_prompt` + `plate_seed` instead of editing the female hero plate |
| **Upload** | Licensed UGC/ad masters with clear, stable swap targets |
| **`p-video` I2V** | Rare — silent B-roll only when avatar cannot frame the beat; **not** recommended for VO + replace rows |

| Field | Guidance |
|-------|----------|
| Plate still | One primary subject; show **every slot** in frame (mug on desk left, bag on chair right, tube in hand at chest) |
| **`video_prompt`** | **Continuous** but controlled — gentle dolly or subtle handheld; **mouth stays in frame** on VO rows |
| **`voice_script`** | Short, **human** lines; script words must match visible garments/props. Multi-scene reels: one **story** — each scene is the next sentence (`So you start…`, `From there…`, `Next…`, `Then…`, `So that's the arc…`), not isolated feature bullets. See `reel_narrative` in the plan. |
| **`voice_prompt`** | Conversational; add *no laugh energy* / *not performative* for explainers |
| **Lip sync for replace** | **Non-negotiable on every beat.** Speaking **`p-video-avatar`** source (`mouth clearly visible`, `clear lip movement`). Every `instruction_prompt` must include **CRITICAL: preserve exact lip sync — mouth shape, lip movement, jaw timing, and audio unchanged.** Clothing/object beats still preserve face and lips. Avoid whip-pans and big gestures during speech. |

The plate defines **framing**; references should match scale. **`p-image-edit`** can align pose or composite desk props before avatar.

### Canonical launch reel (production-tested)

Use this scene map unless the user specifies otherwise — see [`announcement_plan.json`](../../../output/p-video-replace-announcement/announcement_plan.json):

| Scene | Source pattern | Replace pattern |
|-------|----------------|-----------------|
| 1 Hook | Hero at desk + mug; VO | `multi_job`: presenter · green blazer · desk SKU |
| 2 UGC install | Creator, **creative loft** + closed laptop | `multi_job`: face · face · wardrobe — **rooftop / cafe / LED studio** per ref, varied camera |
| 3 Wardrobe | Stylist bust, VO | `multi_job`: 3 clothing-only looks |
| 4 In-game | Knight dialogue cam — fantasy swords in hand | `multi_job` + `p-video-avatar` (not streamer desk) |
| 5 Cafe | **Solo** woman, bag on chair, calm product VO | `multi_job`: face · jacket · bag (not two-shot I2V) |
| 6 Gym | **Golden template** — speaking + in-hand SKUs + shirt | `multi_job` (reuse when iterating other scenes) |
| 7 Game characters | Male reaction dorm clip (`Puck` VO) | `multi_job` — AAA soldier, fantasy ranger, cyberpunk netrunner |
| 8 CTA | Same desk pattern as hook | `multi_job`: presenter · blazer · desk SKU |

**Scene 6 pattern** (copy for new rows): one subject, product at chest height, subtle camera, per-ref `instruction_prompt` with explicit preserve-lips language.

**Multi-slot in one pass:** add a final `multi_job` reference that is a **composite** still (face + outfit + product in one image) with an instruction to apply **all** mapped changes together — see scene 2 and scene 5 in the launch plan.

**Voice / gender:** set `persona_gender` (`female` / `male`) on each replace scene and `source.voice` to the matching voice (`Zephyr (Female)` / `Puck (Male)`). Face-swap references must stay the **same gender** as the source subject — no cross-gender recasts on talking-head beats. The runner prefixes face/clothing reference `p-image` prompts from `persona_gender` and validates voice + **≥3** `references[]` per `multi_job` scene.

**Cast & style variety:** alternate gender and **`cast_descriptor`** (ethnicity, age, archetype) across scenes. **UGC/install rows:** source plate + each ref need **distinct `setting_tag`**, **`camera_tag`**, and **`lighting_tag`** — not neutral grey wall on every still. Scene 1 **persona ladder** refs each carry a different `visual_style_tag`, **`render_medium_tag`**, background, and lighting. Run [visual-variety-bible.md](../../../references/visual-variety-bible.md) checklist before generation.

**Skills-library scene 2 pattern:** source = loft + brick + window bokeh, low three-quarter handheld; refs = rooftop dusk · cafe corner · LED studio — see [`announcement_plan.json`](../../../output/skills-library-announcement/announcement_plan.json).

## Human voice (avatar hook / CTA rows)

| Do | Don't |
|----|-------|
| Short sentences you'd say out loud | "Three point five eight seconds of generation per second of video" |
| Warm, informal product share | Stiff launch-deck or announcer diction |
| One idea per beat | Feature dumps in a single `voice_script` |

Example hook: *"You hand it footage plus reference photos — it can swap faces, outfits, or products while the camera move stays put."*

**Reel voice arc (launch plan):** scripts should read as one story, not isolated spec lines.

| Scene | Role | Voice idea |
|-------|------|------------|
| 1 Hook | What shipped | Same clip — host, outfit, desk; lip sync stays |
| 2 UGC | Real ad | Face, shirt, product — same line, same lips (no composite beat) |
| 3 Wardrobe | Clothing-only | Outfit-only — same delivery |
| 4 In-game dialogue | Game trailers / NPC lines | Male knight + `Puck` — sword swaps |
| 5 Cafe | Location | Face, jacket, bag, mug — same lip sync (no composite beat) |
| 6 Gym | Lip sync | Protein, pre-workout, shirt — lips locked |
| 7 Game + Animate | Cross-sell | Character swap + P-Video-Animate line |
| 8 CTA | Close | Host or desk prop + Pruna API (2 beats, no Animate) |

Changing `voice_script` requires regenerating **`p-video-avatar`** sources (and downstream **`p-video-replace`** + compare).

## Prompt-guided mapping (required for good swaps)

Identity comes from **`images`**, but **`instruction_prompt`** must say **what in the source** maps to **what in each reference** — not a generic "replace the person."

| Layer | What to specify |
|-------|-----------------|
| **Source plate / video** | Who or what is visible (`subject_in_video`, `still_edit`) — e.g. "man in olive coat on the left" |
| **Reference `p-image` prompt** | The replacement look — wardrobe, hair, style |
| **`instruction_prompt`** | Explicit mapping: source slot → reference cues; preserve motion/audio/camera |

**Multi-job rows** (one reference per API call): put a **per-reference `instruction_prompt`** on each entry so each swap names the source subject and the reference identity.

**Single-call rows** (1–4 `images` in one job): one **`instruction_prompt`** that maps index order to screen position (left/right, shelf slots, etc.).

Example (solo cafe, `multi_job` — preferred over two-shot `single_call`):

```text
Replace only the woman's face with the reference. Keep blazer, bag on chair, cup, lip timing, and audio.
Replace only the sand linen blazer with the olive bomber from the reference — clothing only; preserve lips and audio.
Replace only the yellow crossbody on the chair with the burgundy bag from the reference — bag only; preserve face and speech.
```

## Multi-object swaps in one call (`single_call`)

Use only when the source is **silent**, simple, and slots are unambiguous (e.g. static shelf insert). For launch reels and VO rows, prefer **`multi_job`** (one image per call → variant slider).

When several targets share one silent clip:

1. Generate **one reference still per target** with **`p-image`** (up to **4**).
2. Pass all URLs in **`images`** on a **single** `p-video-replace` job.
3. One **`instruction_prompt`** maps index order to screen position (left/center/right).

For **more than four** targets, split scenes or trim subclips.

## Variant showcase (one source, many replacements)

To show **alternate identities** for the **same** slot (e.g. four mascots on one dance clip):

1. Run **`p-video-replace`** once per variant (same `video`, different single-image `images` array).
2. Build a **multi-sample** slider config — one `source`, many `samples` — see [`config.multi-sample.template.json`](../../../examples/workflows/p-video-replace-comparison/config.multi-sample.template.json).

**Reference inset (compare MP4):** compare config includes `"reference_images": [{ "reference": "references/scene01_01.jpeg", "label": "…" }, …]` so [`generate_video_comparison.py`](../../../guides/workflows/_shared/scripts/generate_video_comparison.py) draws **all** scene reference stills as **small bordered thumbnails** (labels in JSON only; not burned in) top-right on every frame. Launch runner adds every `references[]` still by default; set `reference_inset`: `"none"` on a scene to hide.

```json
{
  "source": "path/to/original-dance.mp4",
  "render": "path/to/dance-variants_compare.mp4",
  "title": "P-Video-Replace · Variant ladder",
  "source_label": "Original footage",
  "compare_mode": "single_pass_multi_slider",
  "samples": [
    { "output": "path/to/replaced_mascot_a.mp4", "output_label": "Mascot A", "beat_label": "Variant A" },
    { "output": "path/to/replaced_mascot_b.mp4", "output_label": "Mascot B", "beat_label": "Variant B" }
  ]
}
```

## Making `p-video-replace` work

| Factor | Guidance |
|--------|----------|
| Reference clarity | Face, label, garment silhouette, or prop edges readable |
| **Swap pop** | Plan `swap_visual_bible` — bold **character** identity (face, hair, wardrobe on same talent). Vivid object colors on desk props (cobalt, copper, emerald). |
| **Flash / punch** | Named gel lights, saturated wardrobe, distinct worlds per ref — [SKILL.md](./SKILL.md) **Dynamic eye-catching prompts** |
| **Story VO** | `reel_narrative` + linked `voice_script` per scene (one documentary arc, not isolated feature bullets). |
| Count | 1–4 images per call — plan slots accordingly |
| Framing | Product refs at **matching scale** to shelf/hand slot |
| Audio | `save_audio: true` when dialogue or SFX matter |
| **`instruction_prompt`** | Names **source element** + **reference element**; say what stays unchanged |
| **Visual variety** | Per scene: distinct `setting_tag`, `camera_tag`, `lighting_tag`, `visual_style_tag`; diverse cast across reel — [visual-variety-bible.md](../../../references/visual-variety-bible.md) |
| **Clothing rows** | Say *replace only clothing* — avoid accidental full identity swap unless intended |
| **Object rows** | Say *replace only [object]* — preserve hands, table, shelf reflections |

### Anti-patterns (from launch production)

- Same generic `instruction_prompt` on every variant in a `multi_job` row — **write one per reference**.
- **`single_call`** for cafe two-shot, 3-tube shelf slide, or mixed VO rows — high artifact rate; use **`multi_job`** + simpler source.
- **`p-video` I2V** for wardrobe walk, shelf SKU, or cafe dialogue — prefer **`p-video-avatar`** talking head or in-hand product.
- Pointing at counter products, busy kitchens, lens flare, gender-cross recast on gesture-heavy UGC — use **dynamic UGC locations** (loft, rooftop, cafe) + closed laptop or tube in hand + same-gender recast when possible.
- **Flat grey-wall rows** — neutral grey wall on source **and** every ref reads as one boring studio; give each ref a distinct world + camera angle.
- Flat-lay-only clothing refs on avatar bust shots — ref should show **person wearing** the outfit.
- Hook/CTA `mixed` rows that only face-swap — include real **blazer** and **desk object** beats with object-only instructions.
- Cringy laugh / comedy `video_prompt` on explainers — calm VO, `no laughter` in prompt and delivery notes.
- `voice_script` naming garments not visible in the plate (e.g. "hoodie" vs crewneck).
- Static `video_prompt` on source plates — add controlled continuous camera.
- Announcer VO or spec-sheet numbers in `voice_script` — rewrite until it sounds like a person talking.
- Same office / same medium close-up / same soft natural light on every scene — rotate settings, angles, and styles per [visual-variety-bible.md](../../../references/visual-variety-bible.md).
- Persona ladder refs that share one background or one rendering style — each ladder step needs its own world (anime alley ≠ clay living room ≠ castle garden).
- **`p-image` text triggers** — `graphic tee`, `neon signs`, `game` / `game trailer` / `HUD` / `visor`, readable screens, keyboard key grids — use plain wardrobe, film portrait wording, defocused glow, single desk object ([SKILL.md](./SKILL.md) trigger table).
- **`p-image` collage triggers** — `packshot`, `product still`, `overhead flat lay`, `comparison`, `grid`, `montage`, `side by side`, `variant grid`, **`same`** matching prior variant — use **single object, one frame, lifestyle desk detail** for object refs.
- **`p-image` laptop props** — never open laptop or screen-facing; **closed lid** only. Avoid `developer` in still prompts (use in VO only). Use **accent patch** not decal/sticker/label.
- **Persona range** — ladder hooks need **photoreal + sketch/2D + 3D animation + fictional + anthropomorphic** mix; include **accessory-only** and **wardrobe-only** rows — [SKILL.md](./SKILL.md) **Persona & subject diversity**

Run [p-video-replace-quality-checklist.md](../../../references/p-video-replace-quality-checklist.md) on inputs and outputs.

## API fields (per replace job)

- **`resolution`**: `720p` or `1080p`
- **`target_fps`**: `original` (default), `24`, or `48`
- **`seed`**: lock when retrying the same scene
- **`save_audio`**: `true` for VO-driven demos

## Mixed reels (`avatar` + `replace`)

Same pattern as animate announcements:

- Open with **`avatar`** hook explaining swaps
- Stack **`replace`** slider scenes (multi-object or variant ladder)
- Close with **`avatar`** CTA

## Parallel batching

After confirmation:

- Fan out all **`p-image`** reference jobs together
- Fan out **`p-video-replace`** per scene (independent `video` URLs)
- Fan out slider renders from [`batch.template.json`](../../../examples/workflows/p-video-replace-comparison/batch.template.json)
- Sequential ffmpeg concat for final reel
- Optional **background bed** — [stable-audio-2.5](../../../tools/audio/stable-audio-2.5/SKILL.md) at low volume under VO ([SKILL.md](./SKILL.md) **Background music**)

## Related

- Workflow skill: [SKILL.md](./SKILL.md)
- Model API: [p-video-replace](../../../tools/video/p-video-replace/SKILL.md)
- Launch background bed: [stable-audio-2.5](../../../tools/audio/stable-audio-2.5/SKILL.md)
- Motion-transfer (different job): [animate-beats.md](../multi-scene-avatar-video/animate-beats.md)
