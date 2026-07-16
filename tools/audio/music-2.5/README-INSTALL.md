# music-2.5

## Install

**Skills CLI** (copy-paste):

```bash
npx skills add PrunaAI/pruna-skills@music-2.5 -y
```

**Plugins CLI** (workflow bundles with deps — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: music-2.5
```

Do **not** use `npx plugins add PrunaAI/pruna-skills@music-2.5` — the plugins CLI has no `@name` filter (that’s skills only) and prints “No plugins found”.

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install music-2.5@pruna-skills
```

List all skills:

```bash
npx skills add PrunaAI/pruna-skills -l
```

After install, start a **new chat**. See the [root README](../../../README.md).

## From a local clone

```bash
npx skills add .@music-2.5 -y
# or:
npx skills add ./plugins/music-2.5/skills --skill music-2.5 -y
```
