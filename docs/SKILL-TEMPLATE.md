# Skill template (Pruna tools + workflows)

Adapted from [agentskills.io/specification](https://agentskills.io/specification).

## Types

| Type | Location | API calls? |
|------|----------|------------|
| Tool | `tools/{image,video,audio}/<name>/` | Yes — one model operation |
| Workflow | `workflows/<name>/` | Yes — orchestrates tools |

**Policies:** Diversity, seed ritual, core QA, and (for workflows) staged gates are **injected at bundle time** from [references/policies/](../references/policies/). Do not duplicate them in `skill.manifest.json` — list only model-specific references.

## Layout

```
{name}/                     # folder name MUST match frontmatter `name`
├── SKILL.md
├── skill.manifest.json     # references, scripts, tool_skills (workflows only)
├── README-INSTALL.md       # install one-liners
└── scripts/                # workflow CLIs (optional)
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
---
```

Workflow skills: declare dependencies in `skill.manifest.json` → `tool_skills` (not frontmatter).

## Setup (tools and workflows)

Link [api-setup.md](api-setup.md). Every bundled skill gets a **Shared generation policy** section automatically.

## Related skills

Tools:

```bash
npx skills add PrunaAI/pruna-skills@p-image -y
```

Workflows — prefer plugin install (includes tool deps):

```bash
npx plugins add PrunaAI/pruna-skills
# pick music-video
```

Human recipe routing: [WORKFLOW-RECIPES.md](WORKFLOW-RECIPES.md).

## Body structure

See [agentskills.io](https://agentskills.io/skill-creation/best-practices). Focus SKILL bodies on model payloads, workflow phases, and manifests — not restating global policy.

## Canonical map

Add new skill names to [`.maintainer/skills.catalog.json`](../.maintainer/skills.catalog.json) under `tools` or `workflows`.
