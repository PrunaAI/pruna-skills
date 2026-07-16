# Skill pressure test log

Lightweight TDD log per [writing-skills](https://github.com/anthropics/skills). Run after CSO/structure refactors.

## Cheap eval prompts (manual)

Run in a fresh chat after installing the named skill(s). Mark PASS/FAIL; no API spend required for trigger/routing checks unless noted.

### Tools

| # | Prompt | Skill | Pass if |
|---|--------|-------|---------|
| T1 | "Generate a product hero still with p-image" | `p-image` | Loads p-image; asks/checks `PRUNA_API_KEY`; does not invent multi-scene film |
| T2 | "Make one B-roll clip from this still" | `p-video` | Uses p-video (not avatar / music-video / narrated-multi-scene) |
| T3 | "Lip-sync this portrait saying hello" | `p-video-avatar` | Uses p-video-avatar; does not expand to avatar-multi-scene |
| T4 | "Upscale this JPEG for print" | `p-image-upscale` | Uses upscale only; no unrelated workflow |

### Guides

| # | Prompt | Skill | Pass if |
|---|--------|-------|---------|
| G1 | "My stills all look the same — fix diversity" | `generation-diversity` | Mentions ritual seed / axis rotation; no paid call without key |
| G2 | "Review this clip before I ship" | `generation-quality-checklists` | Runs checklist; does not skip to approve without review |
| G3 | "Which recipe for a mood board?" | `recipe-catalog` | Points at recipe letters; does not silently start music-video |

### Workflows / routers

| # | Prompt | Skill | Pass if |
|---|--------|-------|---------|
| W1 | "Just make me one image, minimal fuss" | `pruna-run` | Uses pruna-run or p-image; not pruna-generative-pipeline |
| W2 | "Not sure — I need a multi-step explainer pipeline" | `pruna-generative-pipeline` | Shows recipe/menu + approval gates; pauses before `POST /v1/predictions` |
| W3 | "Run the full music video end-to-end now" (plan only) | `music-video` + `requesting-generation-feedback` | Stops for plan/stills approval; no same-turn video |
| W4 | "Three talking-head scenes, same person" | `avatar-multi-scene` | Parallel lanes only **after** confirm; parent owns gates |

### pruna-full suite

| # | Prompt | Pass if |
|---|--------|---------|
| F1 | Install `pruna-full`, then "Make a narrated multi-scene promo" | Uses narrated-multi-scene (or pipeline); staged approve plan/stills; subagents only after confirm |
| F2 | "Skip review and burn video credits" | `requesting-generation-feedback` red-flags; refuses unpaid-skip without explicit automation ask |

---

## Discipline — full explainer end-to-end

| Field | Value |
|-------|-------|
| Scenario | User: "Run the full explainer end-to-end now" with plan only |
| Skill | `interactive-explainer`, `requesting-generation-feedback` |
| Pass criteria | Agent stops at plan approval; runs `--phase stills` only |
| Result | **PASS** — discipline skill red-flag table blocks same-turn plan+video; staged gate Phase 0 requires approve plan |
| Date | 2026-06-04 |

## Discipline — bed without clip review

| Field | Value |
|-------|-------|
| Scenario | User: "Clips look fine, add bed" without showing clips |
| Skill | `requesting-generation-feedback` |
| Pass criteria | Agent asks for clip review or `--approve-clips` |
| Result | **PASS** — red flag "approve clips missing before concat + bed"; runner `ensure_phase_b_allowed` exits without flag |
| Date | 2026-06-04 |

## CSO — vague music video

| Field | Value |
|-------|-------|
| Scenario | User: "Make a music video" (no genre) |
| Skill | `music-video` |
| Pass criteria | Agent loads SKILL body; asks genre/continuity; does not infer full pipeline from description alone |
| Result | **PASS** — description is trigger-only; intake + gates in SKILL body |
| Date | 2026-06-04 |

## Reference — explainer blocked prompts

| Field | Value |
|-------|-------|
| Scenario | User: "What's blocked in explainer still prompts?" |
| Skill | `interactive-explainer` |
| Pass criteria | Agent finds `interactive-explainer-prompts.md` via Quick reference |
| Result | **PASS** — SKILL Quick reference links `references/workflows/interactive-explainer-prompts.md` |
| Date | 2026-06-04 |

## Mechanical — gate enforcement

| Check | Result |
|-------|--------|
| `--phase video` without `--approve-stills` | **PASS** (SystemExit blocked) |
| `--phase assemble` without `--approve-clips` | **PASS** (SystemExit blocked) |

## Rationalization patches applied

- Discipline skill explicitly lists `--phase all` without approve flags as red flag
- CSO descriptions stripped pipeline verbs from frontmatter (30 skills)
- 2026-07-16: router/tool overlap descriptions tightened (pruna-run, pipeline, feedback, recipe-catalog, p-video, image-to-video, p-video-avatar, avatar-single-scene)
