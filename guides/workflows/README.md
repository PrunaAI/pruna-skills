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
| **Router** | `pruna-run`, `pruna-generative-pipeline` |
| **Core** | `image-to-video`, `narrated-multi-scene`, `visual-transition-reel`, `avatar-single-scene`, `avatar-multi-scene` |
| **Verticals** | `interactive-explainer`, `music-video` |
| **Launches** | `p-image-upscale-comparison`, `p-video-animate-comparison`, `p-video-replace-comparison` |

**Do not delete the router skills** — they are the intake entrypoints, not duplicates of verticals. `documentary-explainer` was removed; use `interactive-explainer` with `flavor: history_biography`.

Install: `./scripts/install_skill.sh <folder-name>` (searches `router/`, `core/`, `verticals/`, `launches/`).
