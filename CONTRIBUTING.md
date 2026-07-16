# Contributing

## Where to edit

| You want to… | Edit here | Then run |
|--------------|-----------|----------|
| Model API usage | `tools/<modality>/<skill>/SKILL.md` | `./scripts/bundle_skill.sh <skill>` |
| Workflow steps | `workflows/**/SKILL.md` | `./scripts/bundle_skill.sh <skill>` |
| Guideline skills | `guides/**/<skill>/SKILL.md` | `./scripts/bundle_skill.sh <skill>` |
| Shared API or quality rules | `references/shared/` or `references/<modality>/` | `./scripts/bundle_all_skills.sh` |
| What ships in an install | `<skill>/skill.manifest.json` | `./scripts/bundle_skill.sh <skill>` |
| Package version | `VERSION` | `python3 scripts/sync_skill_versions.py && ./scripts/bundle_all_skills.sh` |
| Skill name list | `skills.catalog.json` | `./scripts/bundle_all_skills.sh` |

**Do not edit `plugins/`** — it is generated. Pre-commit rebuilds when `tools/`, `guides/`, or `workflows/` change.

## Skill tiers

| Tier | Path | Purpose |
|------|------|---------|
| **Tools** | `tools/{image,video,audio}/` | One model API per skill |
| **Guides** | `guides/{prompting,quality,routing}/` | Prompting, QA, routing — no paid API |
| **Workflows** | `workflows/{router,core,verticals}/` | End-to-end production pipelines |

Authoring conventions: [SKILL-TEMPLATE.md](SKILL-TEMPLATE.md). Publish runbook: [PUBLISHING.md](PUBLISHING.md). Follow-ups: [BACKLOG.md](BACKLOG.md).

## Pull request checklist

1. `SKILL.md` frontmatter `name` matches the folder name ([Agent Skills spec](https://agentskills.io/specification)).
2. References listed in `skill.manifest.json`; workflow deps in `tool_skills`.
3. If adding a skill, add its name to [`skills.catalog.json`](skills.catalog.json).
4. `./scripts/bundle_all_skills.sh` and commit updated `plugins/`, `skills.sh.json`, `README.skills.md`.
5. `make validate` (or `./scripts/validate_release.sh`) for skills you touched.
6. No API keys, tokens, or generated media in the commit.

## Makefile shortcuts

```bash
make bundle    # rebuild plugins/
make verify    # check plugins/ is current
make validate  # verify + skills-ref + clawhub + install smoke
make smoke     # install smoke only
make publish   # ClawHub dry-run
make release   # full release dry-run
```
