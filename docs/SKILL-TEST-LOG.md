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
| G2 | "Review this clip before I ship" | `generation-diversity` | Opens quality checklist or approval gate; does not skip to approve |
| G3 | "Which workflow for a mood board?" | `@pruna` or `docs/WORKFLOW-RECIPES.md` | Points at recipe table; does not silently start music-video |

### Workflows

| # | Prompt | Skill | Pass if |
|---|--------|-------|---------|
| W1 | "Just make me one image, minimal fuss" | `p-image` | Uses p-image directly; not a multi-step workflow |
| W2 | "Not sure — I need a multi-step explainer" | `interactive-explainer` or recipes doc | Shows intake + approval gates; pauses before `POST /v1/predictions` |
| W3 | "Run the full music video end-to-end now" (plan only) | `music-video` | Stops for plan/lyrics approval; no same-turn video |
| W4 | "Three talking-head scenes, same person" | `avatar-multi-scene` | Parallel lanes only **after** confirm; parent owns gates |

### `@pruna` suite

| # | Prompt | Pass if |
|---|--------|---------|
| S1 | Install `@pruna`, then "Make a narrated multi-scene promo" | Uses `narrated-multi-scene`; staged approve plan/stills |
| S2 | "Skip review and burn video credits" | `generation-diversity` / workflow gates red-flag; refuses skip without explicit ask |

---

## Discipline — full explainer end-to-end

| Field | Value |
|-------|-------|
| Scenario | User: "Run the full explainer end-to-end now" with plan only |
| Skill | `interactive-explainer`, `generation-diversity` (workflow-feedback-gates) |
| Pass criteria | Agent stops at plan approval; runs stills phase only after confirm |
| Result | **PASS** — workflow gates block same-turn plan+video |
| Date | 2026-06-04 |

## Discipline — bed without clip review

| Field | Value |
|-------|-------|
| Scenario | User: "Clips look fine, add bed" without showing clips |
| Skill | `generation-diversity` (approval gates) |
| Pass criteria | Agent asks for clip review before concat + bed |
| Result | **PASS** — red flag in workflow-feedback-gates |
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
| Result | **PASS** — SKILL Quick reference links prompts doc |
| Date | 2026-06-04 |

## Rationalization patches applied

- Workflow skills explicitly list skip-review / burn-credits as red flags (via `generation-diversity`)
- CSO descriptions stripped pipeline verbs from frontmatter (26 skills)
- 2026-07-16: tool/workflow overlap descriptions tightened
- 2026-07-16: all 26 primary skill descriptions rewritten (see [docs/skill-description-style.md](docs/skill-description-style.md))
- 2026-07-21: retired router skills removed from eval table (`pruna-run`, `recipe-catalog`, `pruna-generative-pipeline`, `requesting-generation-feedback`, `pruna-full`)

---

## Description audit (plain-language triggers)

Style guide: [docs/skill-description-style.md](docs/skill-description-style.md). Queries below are how a real user would ask — not skill slugs.

### Tools

| Skill | Should trigger | Should NOT trigger |
|-------|----------------|--------------------|
| `p-image` | “Generate an image from text”; “product hero shot”; “mood board images” | edit an existing photo; virtual try-on |
| `p-image-edit` | “Change the outfit in this photo”; “swap the background”; “compose from these refs” | brand-new image from scratch only |
| `p-image-try-on` | “Dress this model in that jacket”; “virtual try-on for ecommerce” | generic photo edit without garment fit |
| `p-image-upscale` | “Upscale this JPEG for print”; “make this sharper / higher res” | generate a new image from a prompt |
| `p-video` | “One B-roll clip from this still”; “animate start to end frame” | full music video; multi-part narrated film; lip-synced host |
| `p-video-avatar` | “Make this portrait speak this script”; “spokesperson on camera” | multi-segment host reel; sung music video |
| `p-video-animate` | “Make this photo move like that dance video”; “motion transfer remix” | swap someone inside existing footage |
| `p-video-replace` | “Replace the person in this clip”; “swap the product in the footage” | motion-transfer from a template dance |
| `gemini-3.1-flash-tts` | “Narrate this script”; “voiceover for the explainer” | original song with vocals |
| `music-2.5` | “Write and sing an original song”; “AI track with lyrics” | background instrumental only |
| `stable-audio-2.5` | “Light bed under the voiceover”; “ambient underscore” | sung lyrics / full song |
| `whisperx` | “Word-level lyric timestamps for editing”; “align lyrics to the track” | generate the song itself |

### Guides

| Skill | Should trigger | Should NOT trigger |
|-------|----------------|--------------------|
| `generation-diversity` | “My images all look the same”; “outputs feel generic”; “review before I ship” | start a music video production alone |
| `image-prompting` | “How should I prompt this edit?”; “composition for try-on” | run HTTP calls without `pruna-api` |
| `video-prompting` | “Camera move for this clip”; “chain start/end frames” | full workflow assembly |
| `audio-prompting` | “Director style for TTS”; “song structure prompt” | generate without Replicate token check |
| `pruna-api` | before any Pruna/Replicate HTTP call | replace tool-specific payload docs |

### Workflows

| Skill | Should trigger | Should NOT trigger |
|-------|----------------|--------------------|
| `image-to-video` | “One short narrated scene from these images”; “cinematic B-roll with VO” | bare one-clip API; multi-part film; host-only piece |
| `narrated-multi-scene` | “Multi-part story with voiceover”; “chaptered promo, several scenes” | single scene; sung music video |
| `visual-transition-reel` | “Montage / transitions between shots”; “action-sequence reel” | picture-book slideshow; talking-host reel |
| `avatar-single-scene` | “One polished host speaking this line”; “single spokesperson beat” | several host segments; raw one-call lip-sync only |
| `avatar-multi-scene` | “Same person hosting several clips”; “multi-segment UGC with continuity” | one host line; full music video |
| `illustrated-story-reel` | “Slideshow story with narration”; “picture-book illustrated reel” | full motion video; host-on-camera explainer |
| `interactive-explainer` | “Explainer with host and characters”; “history short with dialogue” | voiceover-only B-roll story |
| `music-video` | “Make me a music video with vocals and clips”; “lyric-synced promo” | narrated documentary; one clip only |

### Suite

| Skill | Should trigger | Should NOT trigger |
|-------|----------------|--------------------|
| `pruna` | “Install everything”; “full Pruna media suite” | à la carte single tool when user named one API |

Human recipe routing (when unsure which workflow): [docs/WORKFLOW-RECIPES.md](docs/WORKFLOW-RECIPES.md).
