# pruna-generative-pipeline

Use when someone is unsure which production fits — need a menu for chained images, video, and audio with staged approval. Not for a single known tool call.

## Install

Copy-paste one of these.

**Skills CLI** (one skill):

```bash
npx skills add PrunaAI/pruna-skills@pruna-generative-pipeline -y
```

**Plugins CLI** (bundle + deps for workflows — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: pruna-generative-pipeline
```

Do **not** run `npx plugins add PrunaAI/pruna-skills@pruna-generative-pipeline` — plugins CLI has no `@name` filter (that’s skills only).

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install pruna-generative-pipeline@pruna-skills
```

**ClawHub / OpenClaw:**

```bash
openclaw plugins install clawhub:@pruna-ai/pruna-generative-pipeline
```

## Requirements

- `PRUNA_API_KEY` — [dashboard.pruna.ai](https://dashboard.pruna.ai/)
