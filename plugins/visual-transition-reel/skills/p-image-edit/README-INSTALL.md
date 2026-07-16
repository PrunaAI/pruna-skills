# p-image-edit

## Install

**Skills CLI** (copy-paste):

```bash
npx skills add PrunaAI/pruna-skills@p-image-edit -y
```

**Plugins CLI** (workflow bundles with deps — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: p-image-edit
```

Do **not** use `npx plugins add PrunaAI/pruna-skills@p-image-edit` — the plugins CLI has no `@name` filter (that’s skills only) and prints “No plugins found”.

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install p-image-edit@pruna-skills
```

List all skills:

```bash
npx skills add PrunaAI/pruna-skills -l
```

After install, start a **new chat**. See the [root README](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/README/SKILL.md).

## From a local clone

```bash
npx skills add .@p-image-edit -y
# or:
npx skills add ./plugins/p-image-edit/skills --skill p-image-edit -y
```
