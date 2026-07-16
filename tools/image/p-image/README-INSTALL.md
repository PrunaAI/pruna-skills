# p-image

## Install

**Skills CLI** (copy-paste):

```bash
npx skills add PrunaAI/pruna-skills@p-image -y
```

**Plugins CLI** (workflow bundles with deps — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: p-image
```

Do **not** use `npx plugins add PrunaAI/pruna-skills@p-image` — the plugins CLI has no `@name` filter (that’s skills only) and prints “No plugins found”.

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install p-image@pruna-skills
```

List all skills:

```bash
npx skills add PrunaAI/pruna-skills -l
```

After install, start a **new chat**. See the [root README](../../../README.md).

## From a local clone

```bash
npx skills add .@p-image -y
# or:
npx skills add ./plugins/p-image/skills --skill p-image -y
```
