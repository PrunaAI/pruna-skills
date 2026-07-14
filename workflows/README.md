# Workflows

```text
workflows/
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

**Human-in-the-loop:** Every workflow uses [staged-generation-gate.md](../../../references/shared/staged-generation-gate.md). Per-skill commands: [workflow-feedback-gates.md](../../../references/workflows/workflow-feedback-gates.md).

Install: `npx skills add ./plugins/<name>/skills --skill <folder-name> --agent cursor -y` or `/plugin install <name>@pruna-skills`. Pruna-internal launch skills: `bundle_skill.sh <name> --mine` (`.mine/` only).

### Generated plugins (`plugins/`)

Author in `tools/`, `guides/`, or `workflows/`; publish via generation:

```text
workflows/{router,core,verticals}/<skill>/   ← SKILL.md + skill.manifest.json
tools/{image,video,audio}/<skill>/           ← model tool skills
references/                                  ← shared docs (listed in manifests)
        │
        ▼  ./scripts/bundle_all_skills.sh  (also runs on pre-commit)
plugins/<skill>/.claude-plugin/plugin.json
plugins/<skill>/skills/<skill>/                      ← self-contained install tree
```

Workflow plugins copy direct `tool_skills` into `plugins/<workflow>/skills/`. Check freshness: `./scripts/verify_skill_bundles.sh`.
