# music-video

Use when someone wants a full music video — original song or vocals, performance clips, B-roll, and lyric-synced edits.

## Install

Copy-paste one of these.

**Skills CLI** (one skill):

```bash
npx skills add PrunaAI/pruna-skills@music-video -y
```

**Plugins CLI** (bundle + deps for workflows — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: music-video
```

Do **not** run `npx plugins add PrunaAI/pruna-skills@music-video` — plugins CLI has no `@name` filter (that’s skills only).

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install music-video@pruna-skills
```

**ClawHub / OpenClaw:**

```bash
openclaw plugins install clawhub:@pruna-ai/music-video
```

## Requirements

- `PRUNA_API_KEY` — [dashboard.pruna.ai](https://dashboard.pruna.ai/)
