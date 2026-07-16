# avatar-multi-scene

## Install

**Skills CLI** (copy-paste):

```bash
npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y
```

**Plugins CLI** (workflow bundles with deps — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: avatar-multi-scene
```

Do **not** use `npx plugins add PrunaAI/pruna-skills@avatar-multi-scene` — the plugins CLI has no `@name` filter (that’s skills only) and prints “No plugins found”.

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install avatar-multi-scene@pruna-skills
```

List all skills:

```bash
npx skills add PrunaAI/pruna-skills -l
```

After install, start a **new chat**. See the [root README](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/README/SKILL.md).

## From a local clone

```bash
npx skills add .@avatar-multi-scene -y
# or:
npx skills add ./plugins/avatar-multi-scene/skills --skill avatar-multi-scene -y
```
