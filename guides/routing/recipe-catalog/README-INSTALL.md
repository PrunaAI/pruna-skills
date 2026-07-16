# recipe-catalog

## Install

**Skills CLI** (copy-paste):

```bash
npx skills add PrunaAI/pruna-skills@recipe-catalog -y
```

**Plugins CLI** (workflow bundles with deps — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: recipe-catalog
```

Do **not** use `npx plugins add PrunaAI/pruna-skills@recipe-catalog` — the plugins CLI has no `@name` filter (that’s skills only) and prints “No plugins found”.

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install recipe-catalog@pruna-skills
```

List all skills:

```bash
npx skills add PrunaAI/pruna-skills -l
```

After install, start a **new chat**. See the [root README](../../../README.md).

## From a local clone

```bash
npx skills add .@recipe-catalog -y
# or:
npx skills add ./plugins/recipe-catalog/skills --skill recipe-catalog -y
```
