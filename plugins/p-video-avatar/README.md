# p-video-avatar

Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo.

## Install

Copy-paste one of these.

**Skills CLI** (one skill):

```bash
npx skills add PrunaAI/pruna-skills@p-video-avatar -y
```

**Plugins CLI** (bundle + deps for workflows — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: p-video-avatar
```

Do **not** run `npx plugins add PrunaAI/pruna-skills@p-video-avatar` — plugins CLI has no `@name` filter (that’s skills only).

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install p-video-avatar@pruna-skills
```

**ClawHub / OpenClaw:**

```bash
openclaw plugins install clawhub:@pruna-ai/p-video-avatar
```

## Requirements

- `PRUNA_API_KEY` — [dashboard.pruna.ai](https://dashboard.pruna.ai/)
