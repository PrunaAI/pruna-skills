# Legacy workflow install aliases

Canonical public skills live under `router/`, `core/`, and `verticals/`. Pruna-internal launch skills live in `.mine/catalog/workflows/launches/` (install with `--mine`).

Legacy folder names map to canonical skills (see table). Install with `npx skills add --skill <canonical-name>`. Portable install requires `skill.manifest.json` on the canonical skill — currently: interactive-explainer, music-video, illustrated-story-reel, visual-transition-reel, avatar-multi-scene.

| Legacy name | Canonical skill | Path |
|-------------|-----------------|------|
| `single-scene-ai-video` | `image-to-video` | `core/image-to-video` |
| `multi-scene-ai-video` | `narrated-multi-scene` | `core/narrated-multi-scene` |
| `scene-transition-video` | `visual-transition-reel` | `core/visual-transition-reel` |
| `single-scene-avatar-video` | `avatar-single-scene` | `core/avatar-single-scene` |
| `multi-scene-avatar-video` | `avatar-multi-scene` | `core/avatar-multi-scene` |
| `educational-explainer` | `interactive-explainer` | `verticals/interactive-explainer` |
| `documentary-explainer` | `interactive-explainer` | `verticals/interactive-explainer` |
| `ai-music-video` | `music-video` | `verticals/music-video` |

Public examples: `catalog/examples/workflows/{core,verticals}/`. Launch examples: `.mine/examples/workflows/launches/`.
