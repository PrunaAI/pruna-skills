# Skill template (Pruna workflows + tools + guides)

Adapted from [agentskills.io/specification](https://agentskills.io/specification).

## Tiers

| Tier | Location | API calls? |
|------|----------|------------|
| Tool | `tools/{image,video,audio}/<name>/` | Yes |
| Guide | `guides/{prompting,quality,routing}/<name>/` | No |
| Workflow | `workflows/{router,core,verticals}/<name>/` | Yes (orchestrates tools) |

## Layout

```
{name}/                     # folder name MUST match frontmatter `name`
├── SKILL.md
├── skill.manifest.json     # references, scripts, tool_skills (workflows)
├── README-INSTALL.md       # install one-liners
├── references/             # bundled at publish
└── scripts/                # workflow CLIs
```

## Frontmatter

```yaml
---
name: {folder-name}
description: Use when {triggers only — NO workflow summary}
license: MIT
metadata:
  version: "0.0.2"
  package: pruna-skills
  tier: tool | guide | workflow
# Workflow only — from skill.manifest.json tool_skills:
# depends:
#   - p-image
---
```

## Setup (tools and workflows)

Link [api-setup.md](../../api-setup.md) (adjust relative path). Guide skills omit API setup unless combining with tools.

## Related Skills

Every skill should cross-reference related installs:

```bash
npx skills add PrunaAI/pruna-skills@p-image -y
npx skills add PrunaAI/pruna-skills@p-video -y
```

For workflows, list `tool_skills` from `skill.manifest.json`. Add plugin install: `/plugin install <name>@pruna-skills`.

## Body structure

See [agentskills.io](https://agentskills.io/skill-creation/best-practices). Workflows link [staged-generation-gate.md](references/shared/staged-generation-gate.md). Generation tools link [generation-diversity.md](references/shared/generation-diversity.md).

## Canonical map

See [workflows/README.md](workflows/README.md) for router/core/verticals layout.
