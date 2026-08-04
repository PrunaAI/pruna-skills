# Still-image prompt flow (`p-image` family)

Agent playbook for **photo generation** (`p-image`, `p-image-ideogram`) and **surgical edit** (`p-image-edit`). Full ritual, axes, and explicit structure live in [generation-diversity.md](./generation-diversity.md). Still craft (golden rules, change/keep, checklists) lives in `image-prompting` — this doc is the **pipeline glue** only.

## When to use

| Job | Tool | Start here |
|-----|------|------------|
| New photo generation | `p-image-ideogram` when photo generation needs control (text, JSON, hex/bbox, photoreal detail); else `p-image` | `p-image-ideogram` or `p-image` skill + [Generation flow](#generation-flow-p-image) |
| New photo generation (cheap / fast / bulk) | `p-image` | [Generation flow](#generation-flow-p-image) |
| Change existing photo | `p-image-edit` | [Edit flow](#edit-flow-p-image-edit) |
| Mood board / multi-panel batch | `p-image-ideogram` (×N) unless user asked cheap/fast → `p-image` | [Batch / mood board](#batch--mood-board) |
| Photo → edit → upscale → video | `p-image-ideogram` or `p-image` → `p-image-edit` → … | [Photo → edit handoff](#photo--edit-handoff) |

**Not this path:** virtual try-on → `p-image-try-on`; sharpen only → `p-image-upscale`.

## Brief lock vs free axes

**Dynamic + faithful:** diversity fills what the brief left open — it never overrides user locks.

| Lock first (user or approved plan) | Free to derive from ritual (when brief silent) |
|-----------------------------------|------------------------------------------------|
| Named subject, product, brand, species | Camera tag, lighting nuance, render category |
| Must-keep props, outfit color, readable copy | Setting texture *when* setting not specified |
| Continuity plate URL + cast descriptor | Aspect ratio (multi-example sets) |
| Edit: **change** clause + every **keep** clause | Wording spice inside the change (materials, hex, weather detail) |

**Fidelity check (before pay):** remove the user’s named subject/product/change from the prompt — if the job still “works,” the prompt is wrong. For edits, every stated **keep** must appear in the prompt string.

## Generation flow (`p-image`)

Run in order every time:

1. **Lock the brief** — list user-required facts (subject, product, format, copy-on-surface if any). Ask if anything is missing.
2. **Random seed ritual** — fresh string; state it in the turn when drafting; [sum-mod](./generation-diversity.md#ssot-axis-derivation-sum-mod) for free axes. **Do not** pass ritual string as API `seed`.
3. **Derive axes** — rotate ≥2 free axes vs the previous still in session (`aspect_ratio`, `camera_tag`, `render_category_tag`, setting materials, …). See [by model (p-image)](./generation-diversity.md#by-model-minimum-diversity).
4. **Draft explicit prompt** — name cast/creature, objects, frozen action, setting, camera/light, style tag. Follow [explicit prompt structure](./generation-diversity.md#explicit-prompt-structure-required) and `image-prompting` golden rules. **`p-image` has no upsampling** — concrete language is the whole craft.
5. **Fidelity check** — brief locks still present; no copied SKILL curl examples.
6. **Confirm** — show `prompt` + `aspect_ratio` before `POST` unless user locked wording.
7. **POST + checklist** — `pruna-api` poll/download; run `image-prompting` **p-image quality checklist** before upscale/video.

### Turn template (draft-only turn)

```text
Tool: `p-image`
Ritual seed: <fresh string>
Brief locks: <user facts>
Free axes: aspect_ratio <ratio>, camera <tag>, render <tag>, …
Draft prompt: "<explicit prompt>"
Aspect ratio: <ratio>
Fidelity: ✓ subject/product preserved
→ Confirm to POST (or edit wording)
```

### Typography

Avoid dense readable type unless the user asked for copy on a surface. When they did, follow [text & typography by model](./generation-diversity.md#text--typography-by-model).

## Edit flow (`p-image-edit`)

1. **Lock change + keeps** — `Change [X]. Keep [Y, Z, …] identical.` from user brief.
2. **Upload** — `POST /v1/files`; use `urls.get` in `input.images` (1–5 refs). Never invent file URLs.
3. **Ritual seed** — fresh string before drafting edit wording (variety in *how* you phrase the change, not *what* changes).
4. **Draft edit prompt** — surgical formula; multi-ref: `face from image 1, outfit from image 2`. See `image-prompting` **p-image-edit-prompting** reference.
5. **Fidelity check** — change clause matches ask; every keep clause present; no mood-only rewrite.
6. **Confirm** — `prompt`, refs, `aspect_ratio` (`match_input_image` when appropriate), **`turbo`** on/off (off for hard edits).
7. **POST + checklist** — `image-prompting` **p-image-edit quality checklist**.

### Turn template (edit draft)

```text
Tool: `p-image-edit`
Ritual seed: <fresh string>
Change: <user request>
Keep: <face, pose, outfit, lighting, …>
Draft prompt: "Change … Keep … identical."
Refs: image 1 = <role>
Turbo: off (hard edit) | on (default)
→ Confirm to upload + POST
```

## Batch / mood board

Independent panels (playground grid, demo batch, mood board):

- **New ritual string per panel** — one ritual for the whole board is wrong.
- **Different `aspect_ratio` per panel** when format not locked — derive from each panel’s ritual ([aspect ratio](./generation-diversity.md#aspect-ratio-multi-example-sets)).
- **Same character arc** — opposite rule: one approved photo URL, lock cast; vary only setting/angle per scene ([when not to maximize diversity](./generation-diversity.md#when-not-to-maximize-diversity)).

## Photo → edit handoff

| Step | Action |
|------|--------|
| Photo approved | Save `urls.get` from `p-image` or `p-image-ideogram` output — lock as the edit source |
| Surgical tweak | `p-image-edit` from that URL — never run photo generation again for “same person, new background” |
| Video | Edit from **upscaled** photo when the pipeline requires; upscale again after edit before `p-video*` |

Redirect to `p-image` only when the user wants a **new** subject or scene from scratch.

## Anti-patterns

| Wrong | Right |
|-------|--------|
| Copy otter/corgi curl examples from SKILL.md | Fresh ritual + brief-faithful prompt |
| `cool product vibe, neon` | Named product, materials, action, setting, camera |
| Regen new face for “change background” | `p-image-edit` on locked photo URL |
| One ritual for 4 mood-board tiles | Ritual per independent still |
| Edit prompt without keep clauses | Explicit `Keep … identical` for every user lock |
