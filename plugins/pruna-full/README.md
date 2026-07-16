# pruna-full

All 20 Pruna skills in one plugin. Multi-scene workflows use staged approval (plan → stills → clips before paid video) via bundled generation policies, and parallel subagents per scene lane after you confirm — parent agent merges results.

## Install

Copy-paste one of these (do **not** use `npx plugins add …@pruna-full` — that `@` filter is skills-CLI only and returns “No plugins found”).

**Plugins CLI** (recommended for the full suite):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: pruna-full
```

Or install every plugin at once:

```bash
npx plugins add PrunaAI/pruna-skills -y
```

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install pruna-full@pruna-skills
```

**ClawHub / OpenClaw:**

```bash
openclaw plugins install clawhub:@pruna-ai/pruna-full
```

## Requirements

- `PRUNA_API_KEY` — [dashboard.pruna.ai](https://dashboard.pruna.ai/)
