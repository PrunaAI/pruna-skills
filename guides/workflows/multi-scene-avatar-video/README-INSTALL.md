# Multi-scene avatar video (Pruna only)

This Cursor skill describes a **Pruna P-API–only** workflow: uploads, **`p-image` / `p-image-edit`** (and optional **`p-image-upscale`**) for style-consistent stills, **`p-video-avatar`** per scene, and your own assembly step. It does **not** depend on Scenario MCP or third-party image, TTS, or music APIs.

## Install

From a clone of this repository:

```bash
mkdir -p ~/.cursor/skills
cp -R /path/to/pruna-ai-content-generation-skills/guides/workflows/multi-scene-avatar-video ~/.cursor/skills/
```

Or install the whole repository with `npx skills add` (see repository root `README.md`). Restart Cursor or start a new chat.

## Expected path

```text
~/.cursor/skills/multi-scene-avatar-video/SKILL.md
```

## Contents

- `SKILL.md` — intake Q&A, then end-to-end Pruna-only multi-scene flow.
- `references/generation-quality-checklists.md` — shared gate for stills before avatar jobs.
- `prompt-templates.md` — Pruna models and JSON field patterns.
- `examples.md` — rhythm, QA, manifest skeleton.
