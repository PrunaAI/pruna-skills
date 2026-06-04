---
name: documentary-explainer
description: Redirect — use interactive-explainer (history/biography flavor). Documentary explainers merged into guides/workflows/verticals/interactive-explainer/.
metadata:
  version: "0.0.2"
  deprecated: true
  replaces: interactive-explainer
---

# Documentary explainer (deprecated)

**Use [interactive-explainer](../verticals/interactive-explainer/SKILL.md)** with `flavor: history_biography` (or `documentary`).

Same pipeline: narrator `p-video` triples + character `p-video-avatar`. Scene patterns: [interactive-explainer-scenes.md](../../../references/workflows/interactive-explainer-scenes.md). Still-prompt trigger avoidance: [interactive-explainer/SKILL.md](../verticals/interactive-explainer/SKILL.md) **Still prompts: avoid trigger words**.

Install:

```bash
./scripts/install_skill.sh interactive-explainer
```
