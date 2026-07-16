# Generated plugins (do not edit)

Rebuilt from `tools/` and `workflows/` by `make bundle`.

Each folder is a self-contained plugin:

```text
plugins/<name>/.claude-plugin/plugin.json
plugins/<name>/skills/<name>/SKILL.md
plugins/pruna-full/skills/*               # all skills in one plugin
```

## Install (copy-paste)

**One skill** (`@name` works here):

```bash
npx skills add PrunaAI/pruna-skills@p-image -y
```

**One plugin** (interactive — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# select e.g. music-video or pruna-full
```

**All 21 plugins:**

```bash
npx plugins add PrunaAI/pruna-skills -y
```

**Does not work** (plugins CLI has no `@` filter):

```bash
npx plugins add PrunaAI/pruna-skills@pruna-full   # → No plugins found
```

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install pruna-full@pruna-skills
```

ClawHub: `make publish`
