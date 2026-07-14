# Multi-scene avatar video (Pruna only)

This Cursor skill describes a **Pruna P-API–only** workflow: uploads, **`p-image` / `p-image-edit`** for style-consistent stills, **`p-video-avatar`** per scene, and your own assembly step. It does **not** depend on Scenario MCP or third-party image, TTS, or music APIs.

## Install

```bash
npx skills add PrunaAI/pruna-skills/plugins/avatar-multi-scene/skills --skill avatar-multi-scene --agent cursor -y
```

Workflow skills declare **`depends:`** in `SKILL.md` frontmatter (`p-image`, `p-image-edit`, `p-video-avatar`, `p-video-animate`). The [skills CLI](https://www.npmjs.com/package/skills) resolves and installs those siblings from the same source.

From a local clone: `npx skills add ./plugins/avatar-multi-scene/skills --skill avatar-multi-scene --agent cursor -y`

Restart Cursor or start a new chat.

## Expected path

```text
~/.cursor/skills/avatar-multi-scene/SKILL.md
```

## Contents

- `SKILL.md` — intake Q&A, then end-to-end Pruna-only multi-scene flow.
- `references/generation-quality-checklists.md` — shared gate for stills before avatar jobs.
- `prompt-templates.md` — Pruna models and JSON field patterns.
- `examples.md` — rhythm, QA, manifest skeleton.
