# avatar-single-scene

Use when someone wants one polished host-on-camera beat — a speaking person with intake and approval gates before generation.

## Install

Copy-paste one of these.

**Skills CLI** (one skill):

```bash
npx skills add PrunaAI/pruna-skills@avatar-single-scene -y
```

**Plugins CLI** (bundle + deps for workflows — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: avatar-single-scene
```

Do **not** run `npx plugins add PrunaAI/pruna-skills@avatar-single-scene` — plugins CLI has no `@name` filter (that’s skills only).

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install avatar-single-scene@pruna-skills
```

**ClawHub / OpenClaw:**

```bash
openclaw plugins install clawhub:@pruna-ai/avatar-single-scene
```

## Requirements

- `PRUNA_API_KEY` — [dashboard.pruna.ai](https://dashboard.pruna.ai/)
