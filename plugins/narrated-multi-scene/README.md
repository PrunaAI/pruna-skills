# narrated-multi-scene

Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue.

## Install

Copy-paste one of these.

**Skills CLI** (one skill):

```bash
npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y
```

**Plugins CLI** (bundle + deps for workflows — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: narrated-multi-scene
```

Do **not** run `npx plugins add PrunaAI/pruna-skills@narrated-multi-scene` — plugins CLI has no `@name` filter (that’s skills only).

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install narrated-multi-scene@pruna-skills
```

**ClawHub / OpenClaw:**

```bash
openclaw plugins install clawhub:@pruna-ai/narrated-multi-scene
```

## Requirements

- `PRUNA_API_KEY` — [dashboard.pruna.ai](https://dashboard.pruna.ai/)
