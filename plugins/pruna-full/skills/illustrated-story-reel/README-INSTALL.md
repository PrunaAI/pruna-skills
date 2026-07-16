# illustrated-story-reel

## Install

**Skills CLI** (copy-paste):

```bash
npx skills add PrunaAI/pruna-skills@illustrated-story-reel -y
```

**Plugins CLI** (workflow bundles with deps — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: illustrated-story-reel
```

Do **not** use `npx plugins add PrunaAI/pruna-skills@illustrated-story-reel` — the plugins CLI has no `@name` filter (that’s skills only) and prints “No plugins found”.

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install illustrated-story-reel@pruna-skills
```

List all skills:

```bash
npx skills add PrunaAI/pruna-skills -l
```

After install, start a **new chat**. See the [root README](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/README/SKILL.md).

## From a local clone

```bash
npx skills add .@illustrated-story-reel -y
# or:
npx skills add ./plugins/illustrated-story-reel/skills --skill illustrated-story-reel -y
```
