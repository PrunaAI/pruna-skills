# Generation diversity (all models)

One checklist so **every** Pruna output — **`p-image`**, **`p-video`**, try-on, avatar, replace, animate — is as **diverse** as the brief allows. Details live in linked docs; this page is the agent shortcut.

**Not a separate “ponytail scale”.** Hair (ponytail, locs, fade, buzz cut, etc.) is one **cast** choice in the matrix below — same as age, ethnicity, or setting. Use the **full** checklist here for every generation.

## Three steps (every job)

1. **[Random seed ritual](./random-seed-ritual.md)** — pick and state a random integer **first**; assign `seed` / `project_seed` / new seed per independent panel.
2. **Diversify the scenario row** — change at least **two axes** from the previous output in the same session (cast, setting, camera, **aspect_ratio**, medium, … — unless user asked for continuity).
3. **Log** — ritual seed, axes chosen, prediction id (manifest or turn text).

## Scenario axes (rotate across outputs)

| Axis | Vary with | Applies to |
|------|-----------|------------|
| **Cast** | age, ethnicity, gender, archetype, **hairstyle** | all person/content gens |
| **Medium** | photoreal · cel anime · clay · CG 3D | `p-image`, avatar stills |
| **Setting** | unique `setting_tag` — not repeat adjacent rows | stills + video plates |
| **Camera** | `camera_tag` — low / high / profile / full-body / ECU | stills, `video_prompt` |
| **Lighting** | `lighting_tag` — golden hour · neon · overcast · practical | stills, video mood |
| **Motion** | unique `video_prompt` per clip | `p-video`, `p-video-avatar`, animate |
| **Voice** | natural `voice_script`; one `voice` preset per character | avatar, TTS-led video |
| **Seed** | new ritual per **independent** job; lock `project_seed` only inside one character chain | all seeded models |
| **Aspect ratio** | different `aspect_ratio` per independent still in a batch — see [below](#aspect-ratio-multi-example-sets) | `p-image`, `p-image-edit` |

Full style/camera/lighting ladders: [visual-variety-bible.md](./visual-variety-bible.md). Persona + try-on bar: [realistic-persona-showcase.md](./realistic-persona-showcase.md).

## Aspect ratio (multi-example sets)

When generating **two or more** stills in one session (playground grid, demo batch, mood board), give each independent output a **different** `aspect_ratio` unless the user locked a format.

**Allowed `p-image` values:** `1:1` · `16:9` · `9:16` · `4:3` · `3:4` · `3:2` · `2:3`

**How to pick:** after the [random seed ritual](./random-seed-ritual.md), choose ratio by cycling the list or index with `ritual_seed % 7` — state it in the turn (*"Aspect ratio: 16:9"*). Do **not** default every example to `9:16` or `1:1`.

| Ratio | Typical use |
|-------|-------------|
| `9:16` | vertical UGC, full-body fashion, avatar talking head |
| `16:9` | environmental wide, cinematic landscape plate |
| `3:4` | editorial portrait, try-on full-body |
| `4:3` | classic portrait, product + person |
| `1:1` | packshot grid, social tile |
| `3:2` · `2:3` | magazine / poster crops |

Match prompt framing to ratio (e.g. `16:9 horizontal wide shot`, `9:16 vertical full body`). **`p-image-try-on`** inherits plate size when `preserve_input_size: true` — diversify person plates first.

**Same character arc:** one ratio for the whole chain unless the user asks for reframes.

## By model (minimum diversity)

| Model | Besides ritual seed, always vary |
|-------|-----------------------------------|
| **`p-image`** | cast + setting + camera + **aspect_ratio** (+ medium if not photoreal brief) |
| **`p-image-edit`** | setting and/or angle delta; same identity URL |
| **`p-image-try-on`** | person plate world + garment complexity; preserve scene |
| **`p-image-upscale`** | N/A on prompt — diversify **source** stills |
| **`p-video`** | `prompt` motion grammar; start/end plates differ per scene |
| **`p-video-avatar`** | `video_prompt` + still world per scene; lock voice per character |
| **`p-video-animate`** | persona still style/setting per slider ref |
| **`p-video-replace`** | recast refs — full cast spread on showcase reels |

## When **not** to maximize diversity

- **Same character arc** — lock `project_seed`, one `voice`, hero URL; vary only setting/angle/motion per scene.
- **User asked for continuity** — match their locked seed and cast.
- **Draft → final** — same prompt + `project_seed`; change only `draft: false`.

## Anti-patterns

| Wrong | Right |
|-------|--------|
| Copy doc example seeds | [Random seed ritual](./random-seed-ritual.md) |
| White wall + MC CU on every demo | Rotate setting + camera + cast |
| One `video_prompt` for whole reel | Unique motion per scene row |
| New seed mid avatar chain | Reuse `project_seed` until recast |
| Same aspect ratio on every playground example | Rotate `1:1` · `16:9` · `9:16` · `4:3` · `3:4` · `3:2` · `2:3` per [aspect ratio rules](#aspect-ratio-multi-example-sets) |

## Related

- [generation-quality-checklists.md](./generation-quality-checklists.md) — core + model checklists
- [staged-generation-gate.md](./staged-generation-gate.md) — approval phases
