# generation-quality-checklists

## Install

**Skills CLI** (copy-paste):

```bash
npx skills add PrunaAI/pruna-skills@generation-quality-checklists -y
```

**Plugins CLI** (workflow bundles with deps — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: generation-quality-checklists
```

Do **not** use `npx plugins add PrunaAI/pruna-skills@generation-quality-checklists` — the plugins CLI has no `@name` filter (that’s skills only) and prints “No plugins found”.

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install generation-quality-checklists@pruna-skills
```

List all skills:

```bash
npx skills add PrunaAI/pruna-skills -l
```

After install, start a **new chat**. See the [root README](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/README/SKILL.md).

## From a local clone

```bash
npx skills add .@generation-quality-checklists -y
# or:
npx skills add ./plugins/generation-quality-checklists/skills --skill generation-quality-checklists -y
```
