# pruna-generative-pipeline

## Install

**Skills CLI** (copy-paste):

```bash
npx skills add PrunaAI/pruna-skills@pruna-generative-pipeline -y
```

**Plugins CLI** (workflow bundles with deps — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: pruna-generative-pipeline
```

Do **not** use `npx plugins add PrunaAI/pruna-skills@pruna-generative-pipeline` — the plugins CLI has no `@name` filter (that’s skills only) and prints “No plugins found”.

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install pruna-generative-pipeline@pruna-skills
```

List all skills:

```bash
npx skills add PrunaAI/pruna-skills -l
```

After install, start a **new chat**. See the [root README](../../../README.md).

## From a local clone

```bash
npx skills add .@pruna-generative-pipeline -y
# or:
npx skills add ./plugins/pruna-generative-pipeline/skills --skill pruna-generative-pipeline -y
```
