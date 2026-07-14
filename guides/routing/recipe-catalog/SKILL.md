---
name: recipe-catalog
description: Use when choosing a generative pipeline — mood boards, hero variants, explainers, music videos, avatar reels, and other recipe letters A–R with linked tool and workflow skills.
license: MIT
metadata:
  version: "0.0.2"
  package: pruna-skills
  tier: guide
---

# Recipe catalog

Guideline skill for **picking the right production pattern** before calling APIs. Maps briefs to tool sequences and workflows.

## Setup

No API keys to read the catalog. See [api-setup.md](../../../api-setup.md) before running recipes.

## When to use

- User describes an end product but not which workflow fits.
- You need a structured multi-step plan (stills → edit → video → assembly).
- Comparing options (mood board vs hero variants vs full music video).

Full catalog (recipes A–R): [recipe-catalog.md](./references/recipe-catalog.md)

For interactive routing, also see [pruna-generative-pipeline](../../workflows/router/pruna-generative-pipeline/SKILL.md).

## Related skills

```bash
npx skills add PrunaAI/pruna-skills@pruna-generative-pipeline -y
npx skills add PrunaAI/pruna-skills@pruna-run -y
npx skills add PrunaAI/pruna-skills@music-video -y
```

Install as plugin: `/plugin install recipe-catalog@pruna-skills`
