# Workflow recipes

When a user describes an end product but not which workflow fits, use this document. Agents normally pick tools and workflows from skill frontmatter descriptions; humans use this when unsure.

**Policies:** Install `generation-diversity` for approval gates and workflow-feedback gates. Confirm plan before any `POST /v1/predictions`. The agent is the runner (curl + ffmpeg) — no Python scripts. Shared ffmpeg assembly craft (concat, captions, bed mix, export): **`video-editing`**.

## Quick one-off routing

For a single prompt with minimal intake — pick the shortest tool chain:

| Route | When | Chain |
|-------|------|-------|
| **image** | Still only | `p-image-ideogram` |
| **i2v** | Motion from a still | `p-image-ideogram` → `p-video` |
| **avatar** | Talking head | `p-image-ideogram` → `p-video-avatar` |

For multi-scene plans with approval gates, use a workflow skill (`music-video`, `narrated-multi-scene`, …). Install the full suite first: `npx skills add PrunaAI/pruna-skills@pruna -y` — see [README Quickstart](../README.md#quickstart).

## Routing table (recipe → workflow)

| Recipe | You get | Primary models | Workflow skill |
|--------|---------|----------------|----------------|
| A — Style-locked mood board | N stills, same world | `p-image` → optional `p-image-edit` | (tool chain) |
| B — Hero + variants | One anchor + edits | `p-image` → `p-image-edit` | (tool chain) |
| C — Print / pixel rescue | Higher-res master | `p-image-upscale` → optional `p-image-edit` | (tool chain) |
| D — Animate a plate | One motion clip from a still | still → `p-video` (I2V) | `image-to-video` |
| E — Audio-led cut | Video length follows VO/music | upload `audio` → `p-video` | `image-to-video` |
| F — Draft → final video | Cheap preview then hi-fi | `p-video` draft then final | `narrated-multi-scene` |
| G — Talking head | Portrait + speech | `p-image` → `p-video-avatar` | `avatar-single-scene` or `avatar-multi-scene` |
| H — Social hook stack | Short vertical beats | Several `p-video` and/or avatars | avatar / narrated workflows |
| M — Motion-transfer showcase | Same motion, new subject | `p-video-animate` | `avatar-multi-scene` |
| N — In-video replacement | Swap subjects in footage | `p-video-replace` | `p-video-replace` |
| O — AI music video | Full song + lyric-synced video | Music 2.5 → video | `music-video` |
| P — Narrated story film | Multi-scene B-roll + VO | scene anchor triple | `narrated-multi-scene` |
| Q — Visual transition reel | Motion between still pairs | start/end stills → `p-video` | `visual-transition-reel` |
| R — Educational explainer | Narrator + character dialogue | avatar triples | `interactive-explainer` |
| S — Illustrated story reel | Still story + VO or music | Ken Burns slideshow | `illustrated-story-reel` |
| T — Virtual try-on launch | Fashion vertical showcase | `p-image-try-on` + motion | `p-image-try-on` |
| U — Prompt-driven video edit | Recolor, restyle, remove/add, env, text, lighting | `p-video-edit` | `p-video-edit` |

## Recipe details (A–U)

## Recipe A — Style-locked mood board (same-style stills)

**Shine:** One style bible + repeated aspect ratio + the random seed ritual in `generation-diversity` (SSoT) makes a grid feel art-directed, not random.

**Intake:** How many panels? One subject or variations on a theme? Output aspect (`1:1` grid vs `9:16`)?

**Steps**

1. Write the **style bible** once (palette, line, era, lens).
2. Run **`p-image`** N times with the bible in every `prompt`, same `aspect_ratio`; vary only the beat (emotion, prop, angle). **Start all N jobs in parallel** (async). New ritual string per independent panel unless user locks **`api_seed`**.
3. If a panel drifts, **`p-image-edit`** that panel using the best prior panel as reference + “match reference style; change only: …”.
4. Optional **`p-image-upscale`** on selects for large boards or print.

**Refs:** `p-image`, `p-image-edit`, `p-image-upscale`

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
3. **`p-video`** with `image` + motion `prompt`; add `last_frame_image` for controlled arc. Full intake: `image-to-video`.

## Recipe E — Audio-conditioned `p-video` (single anchor)

**Shine:** Duration tracks audio automatically—ideal for VO-first social cuts.

**Intake:** Audio format? Visual story matching beats? Source: upload, `gemini-3.1-flash-tts`, or `music-2.5`?

**Steps**

1. Generate or upload audio → `/v1/files`.
2. **`p-video`** with `audio` + `prompt` (+ optional `image`, `last_frame_image`); omit `duration`.

For **full narrated story films**, use Recipe **P** (scene anchor triple in `video-prompting`) instead.

## Recipe F — Draft preview → locked final

**Shine:** Same prompt with `draft: true` burns cheap previews; rerun with `draft: false` once the client signs off.

**Intake:** Which beats need approval per scene? Lock list (prompt, `api_seed` if reproducibility matters, resolution) for finals.

**Steps**

1. **`p-video`** async with `draft: true` **for all scenes in parallel**; batch-poll until each preview is ready.
2. After approval, rerun with **`draft: false`** (and same **`api_seed`** if user locked API reproducibility).

## Recipe G — Talking-head (delegated workflows)

**Shine:** Slop-gated photoreal stills + hero plate URL + natural **`voice_script`** + human **`voice_prompt`** + per-scene dynamic **`video_prompt`**.

**Steps**

1. Build **character sheet** and **scene table** — see `avatar-multi-scene`.
2. Hero: **`p-image`** (photoreal, SSoT ritual in `generation-diversity`) → slop gate; lock plate URL.
3. Per scene: **`p-image-edit`** → slop gate — **parallel across scenes** after hero anchor is approved.
4. Hand off to `avatar-single-scene` or `avatar-multi-scene` for **`p-video-avatar`** batch.

## Recipe H — Vertical social “stack”

**Shine:** 2–5 ultra-short **avatar-only** beats with **different settings and angles** per scene.

**Intake:** Per-clip message; distinct background/angle per slot; hero plate URL; natural **`voice_script`**.

**Steps**

1. Use `avatar-multi-scene` for all-`p-video-avatar` stacks, or mix with `narrated-multi-scene` B-roll only when the user explicitly wants cutaways.
2. Assemble outside Pruna; normalize loudness between clips if mixing sources.

## Recipe M — Motion-transfer showcase (slider comparison)

**Shine:** Reuse winning motion templates with new subjects; slider MP4s for before/after.

**Intake:** Motion `.mp4` per beat; reference still per beat; alignment risks.

**Steps**

1. Full workflow: `avatar-multi-scene` — **`animate`** rows, sliders, concat.
2. Optional **`p-image-edit`** to repose each still toward its motion keyframe before animate.
3. Slider renders via ffmpeg hstack slider (see avatar-multi-scene SKILL).

## Recipe N — In-video replacement showcase (slider comparison)

**Shine:** Swap characters, outfits, products in existing footage without reshooting.

**Intake:** `replace_target` per row; `subject_in_video` + per-reference **`instruction_prompt`**; prefer **`p-video-avatar`** sources.

**Steps**

1. Full workflow: `p-video-replace` + visual variety from `generation-diversity` — sliders via ffmpeg hstack slider (see `avatar-multi-scene`).
2. **`p-image`** references → optional **`p-image-edit`** → **`p-video-replace`** → sliders → concat ± bed.

## Recipe O — AI music video

**Shine:** Full song + lyric-synced video.

**Steps:** `music-video` — lyrics → Music 2.5 → align → stills → `p-video-avatar` / `p-video` → assembly.

## Recipe P — Narrated story film (scene anchor triple)

**Shine:** **`image`** + **`last_frame_image`** + **`audio`** per scene — visual continuity and narration sync.

**Intake:** Scene table with start/end still prompts, narration lines, `frame_chain`, bed yes/no.

**Steps**

1. Full workflow: `narrated-multi-scene` — scene anchor triple in `video-prompting`.
2. Hero → parallel **`p-image-edit`** start + end stills → parallel Gemini TTS → probe each MP3 (≤ ~19s) → parallel **`p-video`** triple payloads.
3. Concat embedded VO → optional bed — layering in `audio-prompting`.

## Recipe Q — Visual transition reel

**Shine:** Multi-scene motion between two stills per beat (no VO).

**Steps:** `visual-transition-reel` — scene anchor pair in `video-prompting`.

## Recipe R — Educational explainer

**Shine:** Narrator VO + expert/character dialogue.

**Steps:** `interactive-explainer` — narrator triple + character avatar → concat ± bed (scenes + prompts live in that workflow skill).

## Recipe S — Illustrated story reel

**Shine:** Picture-book / illustrated story — still frames with Ken Burns motion, narration or music, **no p-video**. Vertical reel, **horizontal slideshow**, or square — set `defaults.aspect_ratio` (`9:16`, `16:9`, `1:1`).

**Intake:** Narration vs music? Aspect ratio and platform (Reels vs YouTube/presentations)?

**Steps:** `illustrated-story-reel` — `p-image` hero → `p-image-edit` beats → Gemini TTS per beat **or** Stable Audio / user track → ffmpeg assemble.

## Recipe T — Virtual try-on launch reel

**Shine:** Six fashion verticals in one announcement — ecommerce PDP, virtual fitting room, wholesale catalog, lookbook campaign, UGC ads, personalized outfit recommendations. Person + garment generation → **`p-image-try-on`** → motion branch (`p-video-avatar`, `p-video`, or before/after still slider) → Gemini narration on B-roll rows → concat → **Stable Audio** bed.

**Intake:** Which verticals? Motion mix (avatar vs I2V vs slider)? Cast diversity per `generation-diversity`?

**Steps:** `p-image-try-on` + persona craft in `image-prompting` + `p-video-avatar` — phased gates in `generation-diversity`.

## Recipe U — Prompt-driven video edit

**Shine:** One source clip (≤15s) + a surgical text instruction — colorways, environment variants, object add/remove, on-screen text, or lighting — without reshooting. Optional 1–4 reference images for product/accessory match.

**Intake:** Source video path; one principal change; keep-list (camera, motion, unmentioned subjects); optional refs; draft vs standard; keep audio?

**Steps**

1. Tool chain: upload source (and optional refs) → draft **`prompt`** from `video-prompting` (`p-video-edit-prompting`) → **`p-video-edit`**.
2. Preview with `draft: true` when iterating; final with `draft: false`. Identity/slot swap from required refs → **Recipe N** (`p-video-replace`). Concat / captions / sliders → `video-editing`.

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
| Full SKU creative kit | **B** + `p-image-try-on` |
| Episodic mascot channel | **G** + `avatar-multi-scene` |
| Motion swap / recast demo reel | **M** |
| Replace cast or products in footage | **N** |
| Recolor / restyle / text edit existing footage | **U** |
| Narrated multi-scene story | **P** |
| Illustrated still story (VO or music, no video) | **S** |
| Virtual try-on launch reel (fashion verticals) | **T** |

If a use case is not covered, define a new row: **intake → ordered models → handoff URLs**.
