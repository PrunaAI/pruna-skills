# requesting-generation-feedback

Use when about to spend on generation — pause for review of prompts, images, or clips before the next paid step. Not after the user already approved the current phase.

## Install

Copy-paste one of these.

**Skills CLI** (one skill):

```bash
npx skills add PrunaAI/pruna-skills@requesting-generation-feedback -y
```

**Plugins CLI** (bundle + deps for workflows — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: requesting-generation-feedback
```

Do **not** run `npx plugins add PrunaAI/pruna-skills@requesting-generation-feedback` — plugins CLI has no `@name` filter (that’s skills only).

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install requesting-generation-feedback@pruna-skills
```

**ClawHub / OpenClaw:**

```bash
openclaw plugins install clawhub:@pruna-ai/requesting-generation-feedback
```

## Requirements

- `PRUNA_API_KEY` — [dashboard.pruna.ai](https://dashboard.pruna.ai/)
