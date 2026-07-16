# avatar-multi-scene

Use when someone wants the same person hosting several clips — multi-segment UGC, comparison reels, or mixed speaking and animated scenes with continuity.

## Install

Copy-paste one of these.

**Skills CLI** (one skill):

```bash
npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y
```

**Plugins CLI** (bundle + deps for workflows — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: avatar-multi-scene
```

Do **not** run `npx plugins add PrunaAI/pruna-skills@avatar-multi-scene` — plugins CLI has no `@name` filter (that’s skills only).

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install avatar-multi-scene@pruna-skills
```

**ClawHub / OpenClaw:**

```bash
openclaw plugins install clawhub:@pruna-ai/avatar-multi-scene
```

## Requirements

- `PRUNA_API_KEY` — [dashboard.pruna.ai](https://dashboard.pruna.ai/)
