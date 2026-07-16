# requesting-generation-feedback

## Install

**Skills CLI** (copy-paste):

```bash
npx skills add PrunaAI/pruna-skills@requesting-generation-feedback -y
```

**Plugins CLI** (workflow bundles with deps — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: requesting-generation-feedback
```

Do **not** use `npx plugins add PrunaAI/pruna-skills@requesting-generation-feedback` — the plugins CLI has no `@name` filter (that’s skills only) and prints “No plugins found”.

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install requesting-generation-feedback@pruna-skills
```

List all skills:

```bash
npx skills add PrunaAI/pruna-skills -l
```

After install, start a **new chat**. See the [root README](../../../README.md).

## From a local clone

```bash
npx skills add .@requesting-generation-feedback -y
# or:
npx skills add ./plugins/requesting-generation-feedback/skills --skill requesting-generation-feedback -y
```
