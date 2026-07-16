---
name: generation-quality-checklists
description: Use when reviewing generated images, videos, or audio before shipping — run the quality checklists before asking for approval.
license: MIT
metadata:
  version: "1.0.4"
  package: pruna-skills
  tier: guide
---

# Generation quality checklists

Guideline skill for **agent-side QA** of generated assets. Open output files and judge pass/fail — not automated scoring.

## Setup

No API keys for the checklist itself. See [api-setup.md](../../../api-setup.md) when running generations.

## Flow

1. Generate or download the asset locally.
2. Run the **Core checklist** (diversity, seed ritual, prompt explicitness).
3. Run the **model-specific checklist** for that tool.
4. Fix and regenerate failed items before expensive video steps.
5. Follow [staged-generation-gate.md](./references/staged-generation-gate.md) for user approval gates.

Hub doc: [generation-quality-checklists.md](./references/generation-quality-checklists.md)

## Related skills

```bash
npx skills add PrunaAI/pruna-skills@generation-diversity -y
npx skills add PrunaAI/pruna-skills@requesting-generation-feedback -y
```

Install as plugin: `/plugin install generation-quality-checklists@pruna-skills`
