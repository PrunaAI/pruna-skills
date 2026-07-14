# Workflows

```text
catalog/workflows/
  _shared/scripts/
  router/              # entry — pruna-run, pruna-generative-pipeline
  core/                # scene grammar (HOW)
  verticals/           # deliverables (WHY)
```

| Tier | Skills |
|------|--------|
| **Router** | `pruna-run`, `pruna-generative-pipeline`, `requesting-generation-feedback` |
| **Core** | `image-to-video`, `narrated-multi-scene`, `visual-transition-reel`, `avatar-single-scene`, `avatar-multi-scene` |
| **Verticals** | `interactive-explainer`, `music-video`, `illustrated-story-reel` |

**Pruna-internal launch reels** (comparison sliders, marketing campaigns) are in [`.mine/guides/workflows/launches/`](../../.mine/README.md).

**Do not delete the router skills** — they are the intake entrypoints, not duplicates of verticals.

### Canonical paths vs legacy install aliases

| Canonical path | Legacy install aliases |
|----------------|------------------------|
| `verticals/interactive-explainer` | `educational-explainer`, `documentary-explainer` |
| `core/narrated-multi-scene` | `multi-scene-ai-video` |
| `core/visual-transition-reel` | `scene-transition-video` |
| `verticals/music-video` | `ai-music-video` |
| `core/image-to-video` | `single-scene-ai-video` |
| `core/avatar-single-scene` | `single-scene-avatar-video` |
| `core/avatar-multi-scene` | `multi-scene-avatar-video` |

Legacy skill names — see [legacy-aliases.md](legacy-aliases.md) (canonical `name:` in frontmatter only).

**Human-in-the-loop:** Every workflow uses [staged-generation-gate.md](../../../references/shared/staged-generation-gate.md). Per-skill commands: [workflow-feedback-gates.md](../../../references/workflows/workflow-feedback-gates.md).

Install: `npx skills add ./skills --skill <folder-name> --agent cursor -y`. Pruna-internal launch skills: `bundle_skill.sh <name> --mine` (`.mine/` only).

### Portable bundles (`skills/`)

Author in `catalog/`; publish via generation:

```text
catalog/workflows/{router,core,verticals}/<skill>/   ← SKILL.md + skill.manifest.json
catalog/tools/{image,video,audio}/<skill>/           ← model tool skills
catalog/references/                                  ← shared docs (listed in manifests)
        │
        ▼  ./scripts/bundle_all_skills.sh  (also runs on pre-commit)
skills/<skill>/                                      ← flat install tree for npx skills add
```

`skill.manifest.json` declares which overlapping `catalog/references/` and `_shared/scripts/` files copy into each bundle. Check freshness: `./scripts/verify_skill_bundles.sh`.
