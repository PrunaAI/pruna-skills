# Workflows

```text
guides/workflows/
  _shared/scripts/
  router/              # entry — pruna-run, pruna-generative-pipeline
  core/                # scene grammar (HOW)
  verticals/           # deliverables (WHY)
  launches/            # launch / announcement / comparison reels
```

| Tier | Skills |
|------|--------|
| **Router** | `pruna-run`, `pruna-generative-pipeline`, `requesting-generation-feedback` |
| **Core** | `image-to-video`, `narrated-multi-scene`, `visual-transition-reel`, `avatar-single-scene`, `avatar-multi-scene` |
| **Verticals** | `interactive-explainer`, `music-video`, `illustrated-story-reel` |
| **Launches** | `p-image-upscale-comparison`, `p-video-animate-comparison`, `p-video-replace-comparison` |

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

Legacy install aliases — see [legacy-aliases.md](legacy-aliases.md) and `install_skill.sh` (no duplicate folders at this level).

**Human-in-the-loop:** Every workflow uses [staged-generation-gate.md](../../references/shared/staged-generation-gate.md). Per-skill commands: [workflow-feedback-gates.md](../../references/workflows/workflow-feedback-gates.md).

Install: `./scripts/install_skill.sh <folder-name>` (searches `router/`, `core/`, `verticals/`, `launches/`).
