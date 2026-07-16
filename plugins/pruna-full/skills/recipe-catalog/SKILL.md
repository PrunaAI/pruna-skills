---
name: recipe-catalog
description: Use when browsing recipe ideas for mood boards, hero images, explainers, music videos, or avatar reels and need the linked tools. For a live multi-step project, prefer the generative pipeline.
license: MIT
metadata:
  version: "1.0.4"
  package: pruna-skills
  tier: guide
---

# Recipe catalog

Guideline skill for **picking the right production pattern** before calling APIs. Maps briefs to tool sequences and workflows.

## Setup

No API keys to read the catalog. See [api-setup.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/api-setup/SKILL.md) before running recipes.

## When to use

- User describes an end product but not which workflow fits.
- You need a structured multi-step plan (stills → edit → video → assembly).
- Comparing options (mood board vs hero variants vs full music video).

Full catalog (recipes A–R): [recipe-catalog.md](./references/recipe-catalog.md)

For interactive routing, also see [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md).

## Related skills

```bash
npx skills add PrunaAI/pruna-skills@pruna-generative-pipeline -y
npx skills add PrunaAI/pruna-skills@pruna-run -y
npx skills add PrunaAI/pruna-skills@music-video -y
```

Install as plugin: `/plugin install recipe-catalog@pruna-skills`
