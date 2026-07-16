# recipe-catalog

Use when browsing recipe ideas for mood boards, hero images, explainers, music videos, or avatar reels and need the linked tools. For a live multi-step project, prefer the generative pipeline.

## Install

Copy-paste one of these.

**Skills CLI** (one skill):

```bash
npx skills add PrunaAI/pruna-skills@recipe-catalog -y
```

**Plugins CLI** (bundle + deps for workflows — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: recipe-catalog
```

Do **not** run `npx plugins add PrunaAI/pruna-skills@recipe-catalog` — plugins CLI has no `@name` filter (that’s skills only).

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install recipe-catalog@pruna-skills
```

**ClawHub / OpenClaw:**

```bash
openclaw plugins install clawhub:@pruna-ai/recipe-catalog
```

## Requirements

- `PRUNA_API_KEY` — [dashboard.pruna.ai](https://dashboard.pruna.ai/)
