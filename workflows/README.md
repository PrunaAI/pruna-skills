# Workflows

Eight deliverable skills — multi-step productions with staged approval gates.

```text
workflows/
  _shared/scripts/     # shared runners (generation_gate, pruna_api, …)
  <name>/              # one folder per workflow skill
```

| Workflow | Deliverable |
|----------|-------------|
| `image-to-video` | One narrated scene or B-roll from images |
| `narrated-multi-scene` | Multi-part story with voiceover |
| `visual-transition-reel` | Montage with transitions (no VO) |
| `avatar-single-scene` | One host-on-camera beat |
| `avatar-multi-scene` | Same person hosting several clips |
| `interactive-explainer` | Explainer with host and characters |
| `music-video` | Full music video |
| `illustrated-story-reel` | Slideshow story with narration or music |

**Human-in-the-loop:** Every workflow bundle includes [staged-generation-gate.md](../references/policies/staged-generation-gate.md) and [workflow-feedback-gates.md](../references/policies/workflow-feedback-gates.md) (injected at bundle time).

**Recipe selection:** [docs/WORKFLOW-RECIPES.md](../docs/WORKFLOW-RECIPES.md) when unsure which workflow fits.

Install: `npx plugins add PrunaAI/pruna-skills` → pick workflow name, or `@skill` via `npx skills` if you already have tool deps.

```text
workflows/<skill>/SKILL.md + skill.manifest.json
        │
        ▼  make bundle
plugins/<skill>/skills/<skill>/   (+ embedded tool_skills)
```

Check freshness: `make verify`.
