# Legacy workflow install aliases

Canonical skills live only under `router/`, `core/`, `verticals/`, and `launches/`. There are **no** duplicate folders at `guides/workflows/` root.

`./scripts/install_skill.sh <name>` accepts legacy names (see table). Portable install requires `skill.manifest.json` on the canonical skill — currently: interactive-explainer, music-video, illustrated-story-reel, visual-transition-reel, avatar-multi-scene, and all launch comparison reels.

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

Examples mirror the same tiers: `examples/workflows/{router,core,verticals,launches}/`.
