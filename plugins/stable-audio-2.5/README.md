# stable-audio-2.5

Use when someone wants light instrumental background music — an ambient bed under dialogue or underscore for reels and explainers.

## Install

Copy-paste one of these.

**Skills CLI** (one skill):

```bash
npx skills add PrunaAI/pruna-skills@stable-audio-2.5 -y
```

**Plugins CLI** (bundle + deps for workflows — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: stable-audio-2.5
```

Do **not** run `npx plugins add PrunaAI/pruna-skills@stable-audio-2.5` — plugins CLI has no `@name` filter (that’s skills only).

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install stable-audio-2.5@pruna-skills
```

**ClawHub / OpenClaw:**

```bash
openclaw plugins install clawhub:@pruna-ai/stable-audio-2.5
```

## Requirements

- `PRUNA_API_KEY` — [dashboard.pruna.ai](https://dashboard.pruna.ai/)
