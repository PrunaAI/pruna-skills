# Pruna Skills (agent notes)

Generative media skills for the [Pruna AI API](https://docs.api.pruna.ai/guides/models). Portable [Agent Skills](https://agentskills.io/specification) — Cursor, Claude Code, Copilot, Codex, and more.

## Install

```bash
export PRUNA_API_KEY="…"          # see api-setup.md
npx skills add PrunaAI/pruna-skills@p-image -y
npx plugins add PrunaAI/pruna-skills -y   # workflows / pruna-full
```

List: `npx skills add PrunaAI/pruna-skills -l` · Catalog: [skills.sh](https://skills.sh)

**Team default:** one tool (`@p-image`) → one workflow plugin (`music-video`) → full suite (`pruna-full` with staged approval + subagents after confirm). Open [README.skills.md](README.skills.md) only for the full catalog.

## Layout

| Path | Role |
|------|------|
| `tools/` `guides/` `workflows/` | Author here |
| `plugins/` | Generated install bundles — do not edit |
| `skills.catalog.json` | Skill name source of truth |

Tiers: **tools** (one API call) → `npx skills`; **guides** (no API) → `npx skills`; **workflows** → prefer `npx plugins`.

## Safety

Review skills before use in untrusted repos: [references/shared/agent-safety.md](references/shared/agent-safety.md).

## Maintainers

```bash
make bundle && make validate
```

Releases: [PUBLISHING.md](PUBLISHING.md) · Backlog: [BACKLOG.md](BACKLOG.md)
