# Pruna generative pipeline — recipe catalog (A–R)

Full intake and steps for each recipe in [pruna-generative-pipeline](../../workflows/router/pruna-generative-pipeline/SKILL.md). **Confirm plan before any `POST /v1/predictions`.** Staged gates: [staged-generation-gate.md](../shared/staged-generation-gate.md).

## Recipe A — Style-locked mood board (same-style stills)

**Shine:** One style bible + repeated aspect ratio + [random seed ritual](../shared/random-seed-ritual.md) (SSoT) makes a grid feel art-directed, not random.

**Intake:** How many panels? One subject or variations on a theme? Output aspect (`1:1` grid vs `9:16`)?

**Steps**

1. Write the **style bible** once (palette, line, era, lens).
2. Run **`p-image`** N times with the bible in every `prompt`, same `aspect_ratio`; vary only the beat (emotion, prop, angle). **Start all N jobs in parallel** (async). New ritual string per independent panel unless user locks **`api_seed`**.
3. If a panel drifts, **`p-image-edit`** that panel using the best prior panel as reference + “match reference style; change only: …”.
4. Optional **`p-image-upscale`** on selects for large boards or print.

**Refs:** [p-image](../../tools/image/p-image/SKILL.md), [p-image-edit](../../tools/image/p-image-edit/SKILL.md), [p-image-upscale](../../tools/image/p-image-upscale/SKILL.md)

## Recipe B — Hero frame + controlled variants

**Shine:** One approved hero URL becomes the identity anchor for every `p-image-edit`—fast packaging without re-hitting identity from scratch.

**Intake:** What must stay fixed (face, product silhouette)? What is allowed to change per variant?

**Steps**

1. **`p-image`** or upload → one **hero** URL.
2. **`p-image-edit`** per variant: hero in `images[]`, prompt lists only deltas.
3. Optional **`p-image-upscale`** per hero use case.

## Recipe C — Upscale-first rescue → edit

**Shine:** Upscale cleans AI mush before you edit text or logos onto packaging mockups.

**Intake:** Target MP (1–128)? `enhance_details` vs `enhance_realism`?

**Steps**

1. Upload source → **`p-image-upscale`** with conservative `enhance_realism` unless source is synthetic.
2. **`p-image-edit`** for copy-safe layout tweaks or background replacement.

## Recipe D — Still → cinematic motion (I2V)

**Shine:** Short camera grammar matches what **p-video** does well from a single plate. Add **`last_frame_image`** when the beat has a known end composition.

**Intake:** Camera move, duration, `draft` for storyboard pass? End still for frame chain?

**Steps**

1. Ensure still exists (upload or **`p-image`**).
2. Optional **`p-image-edit`** for end still when chaining scenes.
3. **`p-video`** with `image` + motion `prompt`; add `last_frame_image` for controlled arc. Full intake: [image-to-video](../../workflows/core/image-to-video/SKILL.md).

## Recipe E — Audio-conditioned `p-video` (single anchor)

**Shine:** Duration tracks audio automatically—ideal for VO-first social cuts.

**Intake:** Audio format? Visual story matching beats? Source: upload, [Gemini TTS](../../tools/audio/gemini-3.1-flash-tts/SKILL.md), or [Music 2.5](../../tools/audio/music-2.5/SKILL.md)?

**Steps**

1. Generate or upload audio → `/v1/files`.
2. **`p-video`** with `audio` + `prompt` (+ optional `image`, `last_frame_image`); omit `duration`.

For **full narrated story films**, use Recipe **P** ([scene anchor triple](../video/scene-anchor-triple.md)) instead.

## Recipe F — Draft preview → locked final

**Shine:** Same prompt with `draft: true` burns cheap previews; rerun with `draft: false` once the client signs off.

**Intake:** Which beats need approval per scene? Lock list (prompt, `api_seed` if reproducibility matters, resolution) for finals.

**Steps**

1. **`p-video`** async with `draft: true` **for all scenes in parallel**; batch-poll until each preview is ready.
2. After approval, rerun with **`draft: false`** (and same **`api_seed`** if user locked API reproducibility).

## Recipe G — Talking-head (delegated workflows)

**Shine:** Slop-gated photoreal stills + hero plate URL + natural **`voice_script`** + human **`voice_prompt`** + per-scene dynamic **`video_prompt`**.

**Steps**

1. Build **character sheet** and **scene table** — see [avatar-multi-scene](../../workflows/core/avatar-multi-scene/SKILL.md).
2. Hero: **`p-image`** (photoreal, [SSoT ritual](../shared/random-seed-ritual.md)) → slop gate; lock plate URL.
3. Per scene: **`p-image-edit`** → slop gate — **parallel across scenes** after hero anchor is approved.
4. Hand off to [avatar-single-scene](../../workflows/core/avatar-single-scene/SKILL.md) or [avatar-multi-scene](../../workflows/core/avatar-multi-scene/SKILL.md) for **`p-video-avatar`** batch.

## Recipe H — Vertical social “stack”

**Shine:** 2–5 ultra-short **avatar-only** beats with **different settings and angles** per scene.

**Intake:** Per-clip message; distinct background/angle per slot; hero plate URL; natural **`voice_script`**.

**Steps**

1. Use [avatar-multi-scene](../../workflows/core/avatar-multi-scene/SKILL.md) for all-`p-video-avatar` stacks, or mix with [narrated-multi-scene](../../workflows/core/narrated-multi-scene/SKILL.md) B-roll only when the user explicitly wants cutaways.
2. Assemble outside Pruna; normalize loudness between clips if mixing sources.

## Recipe M — Motion-transfer showcase (slider comparison)

**Shine:** Reuse winning motion templates with new subjects; slider MP4s for before/after.

**Intake:** Motion `.mp4` per beat; reference still per beat; alignment risks.

**Steps**

1. Full workflow: [avatar-multi-scene](../../workflows/core/avatar-multi-scene/SKILL.md) — **`animate`** rows, sliders, concat.
2. Optional **`p-image-edit`** to repose each still toward its motion keyframe before animate.
3. Slider renders via [`generate_video_comparison.py`](../../workflows/_shared/scripts/generate_video_comparison.py).

## Recipe N — In-video replacement showcase (slider comparison)

**Shine:** Swap characters, outfits, products in existing footage without reshooting.

**Intake:** `replace_target` per row; `subject_in_video` + per-reference **`instruction_prompt`**; prefer **`p-video-avatar`** sources.

**Steps**

1. Full workflow: [p-video-replace](../../tools/video/p-video-replace/SKILL.md) + [visual-variety-bible.md](../shared/visual-variety-bible.md#prompt-patterns) — sliders via [`generate_video_comparison.py`](../../workflows/_shared/scripts/generate_video_comparison.py).
2. **`p-image`** references → optional **`p-image-edit`** → **`p-video-replace`** → sliders → concat ± bed.

## Recipe O — AI music video

**Shine:** Full song + lyric-synced video.

**Steps:** [music-video](../../workflows/verticals/music-video/SKILL.md) — lyrics → Music 2.5 → align → stills → `p-video-avatar` / `p-video` → assembly.

## Recipe P — Narrated story film (scene anchor triple)

**Shine:** **`image`** + **`last_frame_image`** + **`audio`** per scene — visual continuity and narration sync.

**Intake:** Scene table with start/end still prompts, narration lines, `frame_chain`, bed yes/no.

**Steps**

1. Full workflow: [narrated-multi-scene](../../workflows/core/narrated-multi-scene/SKILL.md) — [scene-anchor-triple.md](../video/scene-anchor-triple.md).
2. Hero → parallel **`p-image-edit`** start + end stills → parallel Gemini TTS → probe each MP3 (≤ ~19s) → parallel **`p-video`** triple payloads.
3. Concat embedded VO → optional bed — [audio-post-production.md](../audio/audio-post-production.md).

## Recipe Q — Visual transition reel

**Shine:** Multi-scene motion between two stills per beat (no VO).

**Steps:** [visual-transition-reel](../../workflows/core/visual-transition-reel/SKILL.md) — [scene-anchor-pair.md](../video/scene-anchor-pair.md).

## Recipe R — Educational explainer

**Shine:** Narrator VO + expert/character dialogue.

**Steps:** [interactive-explainer](../../workflows/verticals/interactive-explainer/SKILL.md) — narrator triple + character avatar → concat ± bed. Scenes: [interactive-explainer-scenes.md](./interactive-explainer-scenes.md). Prompts: [interactive-explainer-prompts.md](./interactive-explainer-prompts.md).

## Recipe S — Illustrated story reel

**Shine:** Picture-book / illustrated story — still frames with Ken Burns motion, narration or music, **no p-video**. Vertical reel, **horizontal slideshow**, or square — set `defaults.aspect_ratio` (`9:16`, `16:9`, `1:1`).

**Intake:** Narration vs music? Aspect ratio and platform (Reels vs YouTube/presentations)?

**Steps:** [illustrated-story-reel](../../workflows/verticals/illustrated-story-reel/SKILL.md) — `p-image` hero → `p-image-edit` beats → Gemini TTS per beat **or** Stable Audio / user track → ffmpeg assemble.

## Recipe T — Virtual try-on launch reel

**Shine:** Six fashion verticals in one announcement — ecommerce PDP, virtual fitting room, wholesale catalog, lookbook campaign, UGC ads, personalized outfit recommendations. Person + garment generation → **`p-image-try-on`** → motion branch (`p-video-avatar`, `p-video`, or before/after still slider) → Gemini narration on B-roll rows → concat → **Stable Audio** bed.

**Intake:** Which verticals? Motion mix (avatar vs I2V vs slider)? Cast diversity per [visual-variety-bible.md](../shared/visual-variety-bible.md)?

**Steps:** [p-image-try-on](../../tools/image/p-image-try-on/SKILL.md) + [realistic-persona-showcase.md](../shared/realistic-persona-showcase.md) + [p-video-avatar](../../tools/video/p-video-avatar/SKILL.md) — phased gates per [workflow-feedback-gates.md](./workflow-feedback-gates.md).

## More ideas (map to recipes)

| Idea | Map |
|------|-----|
| Fast catalog / packshots | **B** + optional **C** |
| Same character, six posts | **A** or **G** |
| Lip-sync spokesperson | **G** |
| Animate this poster | **D** |
| VO-driven ad | **E** |
| Client approval workflow | **F** |
| UGC hook testing at scale | **G** or **H** |
| Product mini-story reels | **D** or **P** |
| Full SKU creative kit | **B** + [p-image-try-on](../../tools/image/p-image-try-on/SKILL.md) |
| Episodic mascot channel | **G** + [avatar-multi-scene](../../workflows/core/avatar-multi-scene/SKILL.md) |
| Motion swap / recast demo reel | **M** |
| Replace cast or products in footage | **N** |
| Narrated multi-scene story | **P** |
| Illustrated still story (VO or music, no video) | **S** |
| Virtual try-on launch reel (fashion verticals) | **T** |

If a use case is not covered, define a new row: **intake → ordered models → handoff URLs**.

## Related

- Hub skill: [pruna-generative-pipeline/SKILL.md](../../workflows/router/pruna-generative-pipeline/SKILL.md)
- Feedback discipline: [requesting-generation-feedback/SKILL.md](../../workflows/router/requesting-generation-feedback/SKILL.md)
- API: [pruna-api.md](../shared/pruna-api.md)
