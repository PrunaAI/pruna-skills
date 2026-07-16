# generation-diversity

## Install

**Skills CLI** (copy-paste):

```bash
npx skills add PrunaAI/pruna-skills@generation-diversity -y
```

**Plugins CLI** (workflow bundles with deps — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: generation-diversity
```

Do **not** use `npx plugins add PrunaAI/pruna-skills@generation-diversity` — the plugins CLI has no `@name` filter (that’s skills only) and prints “No plugins found”.

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install generation-diversity@pruna-skills
```

List all skills:

```bash
npx skills add PrunaAI/pruna-skills -l
```

After install, start a **new chat**. See the [root README](../../../README.md).

## From a local clone

```bash
npx skills add .@generation-diversity -y
# or:
npx skills add ./plugins/generation-diversity/skills --skill generation-diversity -y
```
