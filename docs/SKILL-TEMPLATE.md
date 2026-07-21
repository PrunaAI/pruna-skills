# Skill template (guides + tools + workflows)

Adapted from [agentskills.io/specification](https://agentskills.io/specification).

## Types

| Type | Location | API calls? |
|------|----------|------------|
| Guide | `skills/guides/<name>/` | No — craft / HTTP patterns |
| Tool | `skills/{image,video,audio}/<name>/` | Yes — one model operation |
| Workflow | `skills/workflows/<name>/` | Yes — agent orchestrates tools |
| Suite | `skills/suite/pruna/` | Meta — depends on all others |

## Layout

```
{name}/
├── SKILL.md
├── skill.manifest.json     # local references only (no scripts / tool_skills)
├── references/             # craft owned by this skill (guides / workflows)
└── templates/              # workflow plan JSON (optional)
```

## Frontmatter

```yaml
---
name: {folder-name}
description: Use when {triggers only}
license: MIT
metadata:
  version: "0.0.2"
  package: pruna-skills
---
```

## Cross-skill references (no outbound hyperlinks)

Markdown links may only target files **inside the same skill package** (e.g. `./references/foo.md`). Never link to another skill’s `SKILL.md`, `references/`, or to repo `docs/`.

Name other skills with backticks (`` `p-image` ``) and, in overview sections, use a **Skill | Description | Install** table. External vendor URLs (`https://…`) are fine.

Descriptions come from each skill’s frontmatter `description:` (the “use when” line). Bundle regenerates tables via `.maintainer/write_skill_cross_refs.py`.

| Section | Contents |
|---------|----------|
| **## Prerequisites** | Overview table of required skills (guides for tools; tools for workflows) |
| **## Pruna tools** / **## Related** / **## When NOT to use** | Same table shape — description = when to use that skill |
| Inline prose | `` `skill-name` `` only |
| Same-skill craft | Relative links to `./references/…` only |

Example row:

| Skill | Description | Install |
|-------|-------------|---------|
| `p-image` | Use when someone wants a fast AI image — … | `npx skills add PrunaAI/pruna-skills@p-image -y` |

Or install everything once: `npx skills add PrunaAI/pruna-skills@pruna -y`.

## Body focus

- Guides: when to use, works with, before generating reading order.
- Tools: HTTP payloads, fields, Pruna-only caveats — not restating guide craft.
- Workflows: phases, approval gates, curl/ffmpeg — agent is the runner.

## Canonical map

[`.maintainer/skills.catalog.json`](../.maintainer/skills.catalog.json) — `guides`, `tools`, `workflows`, `suite`.
