# Skill template (Pruna workflows + tools)

Adapted from [agentskills.io/specification](https://agentskills.io/specification). See also [writing-skills CSO rules](https://github.com/anthropics/skills).

## Frontmatter

```yaml
---
name: {folder-name}              # MUST match install path (see install_skill.sh)
description: Use when {triggers only — NO workflow summary, NO pipeline steps}
license: MIT                     # workflows only
metadata:
  version: "0.0.1"
---
```

**Description rules (CSO):**
- Start with `Use when…`
- Third person; triggers and symptoms only
- Max ~300 characters when possible
- Never summarize the workflow (agents skip the body if you do)

Legacy install aliases (e.g. `educational-explainer`) belong in `install_skill.sh` only — mention in stub skills, not in canonical `name:`.

## Body structure

```markdown
# {Title}

## Overview
One or two sentences: what this skill is and the core principle.

## When to Use
- Trigger / symptom bullets
- When NOT to use (1–2 bullets)

## Feedback gates
Workflows only — link [staged-generation-gate.md](../references/shared/staged-generation-gate.md) and [workflow-feedback-gates.md](../references/workflows/workflow-feedback-gates.md).

## Quick reference
Table: phases, CLI flags, or API fields. Link heavy detail to reference files.

## Workflow
Numbered steps or phased runner commands. Link out for tables longer than ~30 lines.

## Common mistakes
Anti-patterns table.

## Related
Cross-links to other skills (skill names + paths; no @ force-load).
```

## Workflow vs tool

| Type | Location | Runner |
|------|----------|--------|
| Workflow | `guides/workflows/{router,core,verticals,launches}/` | Optional `run_from_plan.py` |
| Tool | `tools/{image,video,audio}/` | None (API reference) |

## Canonical map

See [guides/workflows/README.md](workflows/README.md) for install paths and legacy aliases.
