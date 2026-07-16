# Pruna Skills (agent notes)

Generative media skills for the [Pruna AI API](https://docs.api.pruna.ai/guides/models). Portable [Agent Skills](https://agentskills.io/specification) — Cursor, Claude Code, Copilot, Codex, and more.

## How this works

A **skill** is a playbook your agent loads for one job. A **plugin** is the install package — workflow plugins also bring their tool deps.

- **Tools** — one paid API call → `npx skills`
- **Workflows** — finished deliverables (multi-step) → prefer `npx plugins`

Shared diversity, QA, and approval rules ship inside every bundled skill via [references/policies/](references/policies/) (injected at bundle time). Humans picking recipes: [docs/WORKFLOW-RECIPES.md](docs/WORKFLOW-RECIPES.md).

GitHub is the source of truth. [skills.sh](https://skills.sh) discovers via install telemetry. ClawHub is optional for OpenClaw. Claude marketplace is the in-repo catalog. Full onboarding: [README.md](README.md).

## Install

```bash
export PRUNA_API_KEY="…" # see docs/api-setup.md

npx skills add PrunaAI/pruna-skills@p-image -y
npx plugins add PrunaAI/pruna-skills
# pick music-video or pruna-full from the list
```

```bash
npx skills add PrunaAI/pruna-skills -l
npx plugins discover PrunaAI/pruna-skills
```

**Team default:** try `@p-image`, then pick `music-video`, then `pruna-full` if you want everything. Open [docs/SKILL-CATALOG.md](docs/SKILL-CATALOG.md) only for the full catalog.

## Layout

| Path | Role |
|------|------|
| `tools/` `workflows/` | Author here |
| `references/` | Shared library — **not installable**. [`policies/`](references/policies/) auto-injected; other folders copied when listed in manifests |
| `plugins/` | Generated install bundles — do not edit |
| `.maintainer/skills.catalog.json` | Skill name source of truth (12 tools + 8 workflows) |
| `docs/SKILL-CATALOG.md` | Generated full catalog (do not edit) |

## Safety

Review skills before use in untrusted repos: [references/shared/agent-safety.md](references/shared/agent-safety.md).

## Maintainers

```bash
make bundle && make validate
```

Releases: [PUBLISHING.md](docs/PUBLISHING.md) · Backlog: [BACKLOG.md](docs/BACKLOG.md)
