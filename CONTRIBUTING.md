# Contributing

## Where to edit

| You want to… | Edit here | Then run |
|--------------|-----------|----------|
| Model API usage | `tools/<modality>/<skill>/SKILL.md` | `make bundle-skill SKILL=<name>` |
| Workflow steps | `workflows/<skill>/SKILL.md` | `make bundle-skill SKILL=<name>` |
| Shared generation policy | `references/policies/` | `make bundle` (auto-injected; do **not** list in manifests) |
| Model-specific QA / API docs | `references/{shared,image,video,audio,workflows}/` | List basename in `skill.manifest.json` `references`, then `make bundle` |
| What ships in an install | `<skill>/skill.manifest.json` | `make bundle-skill SKILL=<name>` |
| Package version | `VERSION` | `make bundle` (syncs versions) |
| Skill name list | `.maintainer/skills.catalog.json` | `make bundle` |

**Do not edit `plugins/`** — it is generated. Pre-commit rebuilds when `tools/`, `workflows/`, or `references/` change.

## Skill types

| Type | Path | Purpose |
|------|------|---------|
| **Tool** | `tools/{image,video,audio}/<name>/` | One model API per skill |
| **Workflow** | `workflows/<name>/` | End-to-end production; `tool_skills` in manifest |

Policy injection (diversity, QA, gates) is automatic at bundle time — do not author separate guide skills for it.

Authoring conventions: [SKILL-TEMPLATE.md](docs/SKILL-TEMPLATE.md). Recipe routing for humans: [WORKFLOW-RECIPES.md](docs/WORKFLOW-RECIPES.md). Publish runbook: [PUBLISHING.md](docs/PUBLISHING.md).

## Pull request checklist

1. `SKILL.md` frontmatter `name` matches the folder name ([Agent Skills spec](https://agentskills.io/specification)).
2. Skill-specific references listed by basename in `skill.manifest.json` (never policy files — injection owns those); workflow deps in `tool_skills`.
3. If adding a skill, add its name to [`.maintainer/skills.catalog.json`](.maintainer/skills.catalog.json).
4. `make bundle` and commit updated `plugins/`, `skills.sh.json`, `docs/SKILL-CATALOG.md`.
5. `make validate` for skills you touched.
6. No API keys, tokens, or generated media in the commit.

## Makefile shortcuts

```bash
make bundle              # rebuild plugins/
make bundle-skill SKILL=p-image   # same + assert that skill exists in plugins/
make verify              # check plugins/ is current + policy injection
make validate            # verify + skills-ref + clawhub + install smoke
make smoke               # install smoke only
make publish             # ClawHub dry-run
make release             # prints release usage
```
