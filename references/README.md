# References

Shared specs and QA checklists, grouped like `tools/` by modality plus workflow-specific docs.

```text
references/
  shared/       # API, credentials, execution, staged gate, generation-diversity, random seed ritual, variety bible
  image/        # p-image / edit / upscale / try-on quality checklists
  video/        # p-video family checklists + scene-anchor triple/pair
  audio/        # narration + bed post-production
  workflows/    # vertical deliverable specs (explainers, music video QA)
```

**Hub:** [shared/generation-quality-checklists.md](shared/generation-quality-checklists.md) — core gate, links to every checklist, and **how agents review outputs with vision** before user approval gates.  
**Credentials:** [shared/api-credentials.md](shared/api-credentials.md) — Pruna + Replicate signup when keys are missing.

**Model index:** [shared/pruna-models.md](shared/pruna-models.md)

Portable installs copy files by **basename** into `references/` (see `scripts/bundle_skill.sh`). Marketing-only try-on docs live in [`.mine/references/image/`](../.mine/README.md).
