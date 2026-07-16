---
name: generation-diversity
description: Use when outputs look generic or repetitive — apply the random seed ritual, explicit prompt structure, and scenario axis rotation before any paid generation call.
license: MIT
metadata:
  version: "1.0.2"
  package: pruna-skills
  tier: guide
---

# Generation diversity

Guideline skill for **varied, specific prompts** across all Pruna models. No API calls — read and apply before generating.

## Setup

No API keys required. For generation jobs, see [api-setup.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/api-setup/SKILL.md).

## Quick flow

1. **[Random seed ritual](./references/random-seed-ritual.md)** — always first; derive axes via sum-mod.
2. **Write an explicit prompt** — named people, props, setting, camera, style tag.
3. **Rotate at least two scenario axes** between outputs in the same session.
4. **Log** ritual string, axes, and prediction id.

Full checklist: [generation-diversity.md](./references/generation-diversity.md)

## Related skills

```bash
npx skills add PrunaAI/pruna-skills@generation-quality-checklists -y
npx skills add PrunaAI/pruna-skills@p-image -y
npx skills add PrunaAI/pruna-skills@pruna-generative-pipeline -y
```

Install as plugin: `/plugin install generation-diversity@pruna-skills`
