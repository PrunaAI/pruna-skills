# Contributing

## Where to edit

| You want to… | Edit here | Then run |
|--------------|-----------|----------|
| Model API usage | `skills/{image,video,audio}/<skill>/SKILL.md` | `make bundle` |
| Prompting craft | `skills/guides/<name>/references/` + guide `SKILL.md` | `make bundle` |
| Workflow steps | `skills/workflows/<skill>/SKILL.md` | `make bundle` |
| Workflow-local craft | `skills/workflows/<skill>/references/` | List basename in manifest, then `make bundle` |
| Package version | `VERSION` | `make bundle` |
| Skill name list | `.maintainer/skills.catalog.json` | `make bundle` |

Cross-skill reuse: **Prerequisites** + `npx skills add …@other` — do not duplicate craft files.

## Skill types

| Type | Path | Purpose |
|------|------|---------|
| **Guide** | `skills/guides/<name>/` | Craft or Pruna HTTP |
| **Tool** | `skills/{image,video,audio}/<name>/` | One API; Prerequisites → guides |
| **Workflow** | `skills/workflows/<name>/` | Playbook; Prerequisites → tools |
| **Suite** | `skills/suite/pruna/` | Umbrella |

No Python runners. No top-level `references/` or `plugins/`.

Authoring: [SKILL-TEMPLATE.md](docs/SKILL-TEMPLATE.md). Recipes: [WORKFLOW-RECIPES.md](docs/WORKFLOW-RECIPES.md). Publish: [PUBLISHING.md](docs/PUBLISHING.md).

## Pull request checklist

1. Frontmatter `name` matches folder name.
2. Tools/workflows have **## Prerequisites** with `npx skills add` lines; guides have **## Install**.
3. Guide descriptions stay vendor-neutral (except `pruna-api`).
4. New skills registered in `.maintainer/skills.catalog.json`.
5. `make bundle` and commit catalog / `skills.sh.json` / marketplace.
6. `make validate`.
7. No API keys or generated media in the commit.

## Makefile

```bash
make bundle              # versions + catalog + marketplace
make bundle-skill SKILL=p-image
make verify              # layout checks
make validate            # verify + skills-ref + smoke
make smoke
make publish             # ClawHub dry-run
```
