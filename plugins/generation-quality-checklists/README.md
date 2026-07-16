# generation-quality-checklists

Use when reviewing generated images, videos, or audio before shipping — run the quality checklists before asking for approval.

## Install

Copy-paste one of these.

**Skills CLI** (one skill):

```bash
npx skills add PrunaAI/pruna-skills@generation-quality-checklists -y
```

**Plugins CLI** (bundle + deps for workflows — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: generation-quality-checklists
```

Do **not** run `npx plugins add PrunaAI/pruna-skills@generation-quality-checklists` — plugins CLI has no `@name` filter (that’s skills only).

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install generation-quality-checklists@pruna-skills
```

**ClawHub / OpenClaw:**

```bash
openclaw plugins install clawhub:@pruna-ai/generation-quality-checklists
```

## Requirements

- `PRUNA_API_KEY` — [dashboard.pruna.ai](https://dashboard.pruna.ai/)
