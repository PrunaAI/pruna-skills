# Pruna Skills (agent notes)

Generative media skills for the [Pruna AI API](https://docs.api.pruna.ai/guides/models). Portable [Agent Skills](https://agentskills.io/specification) — Cursor, Claude Code, Copilot, Codex, and more.

## How this works

A **skill** is a playbook your agent loads for one job. A **plugin** is the install package — workflow plugins also bring their tool deps.

- **Tools** — one paid API call → `npx skills`
- **Guides** — prompting / QA / recipes, no API → `npx skills`
- **Workflows** — full productions → prefer `npx plugins`
- **Routers** — quick one-off, pick a pipeline, or gate spend → `npx skills`

GitHub is the source of truth. [skills.sh](https://skills.sh) discovers via install telemetry. ClawHub is optional for OpenClaw. Claude marketplace is the in-repo catalog. Full onboarding: [README.md](README.md).

## Install

```bash
export PRUNA_API_KEY="…"          # see api-setup.md

npx skills add PrunaAI/pruna-skills@p-image -y
npx plugins add PrunaAI/pruna-skills
# pick music-video or pruna-full from the list
```

```bash
npx skills add PrunaAI/pruna-skills -l
npx plugins discover PrunaAI/pruna-skills
```

**Team default:** try `@p-image`, then pick `music-video`, then `pruna-full` if you want everything. Open [README.skills.md](README.skills.md) only for the full catalog.

## Layout

| Path | Role |
|------|------|
| `tools/` `guides/` `workflows/` | Author here |
| `plugins/` | Generated install bundles — do not edit |
| `skills.catalog.json` | Skill name source of truth |

## Safety

Review skills before use in untrusted repos: [references/shared/agent-safety.md](references/shared/agent-safety.md).

## Maintainers

```bash
make bundle && make validate
```

Releases: [PUBLISHING.md](PUBLISHING.md) · Backlog: [BACKLOG.md](BACKLOG.md)
