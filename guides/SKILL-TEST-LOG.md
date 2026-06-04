# Skill pressure test log

Lightweight TDD log per [writing-skills](https://github.com/anthropics/skills). Run after CSO/structure refactors.

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

## Dedupe — legacy name

| Field | Value |
|-------|-------|
| Scenario | User invokes `educational-explainer` |
| Skill | stub → `interactive-explainer` |
| Pass criteria | Agent lands on canonical content |
| Result | **PASS** — `install_skill.sh educational-explainer` → `interactive-explainer` (alias in install script, no stub folder) |
| Date | 2026-06-04 |

## Mechanical — gate enforcement

| Check | Result |
|-------|--------|
| `--phase video` without `--approve-stills` | **PASS** (SystemExit blocked) |
| `--phase assemble` without `--approve-clips` | **PASS** (SystemExit blocked) |

## Rationalization patches applied

- Discipline skill explicitly lists `--phase all` without approve flags as red flag
- CSO descriptions stripped pipeline verbs from frontmatter (30 skills)
- Legacy stubs prevent loading duplicate 1600w SKILL bodies
