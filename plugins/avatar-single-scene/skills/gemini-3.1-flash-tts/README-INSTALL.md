# gemini-3.1-flash-tts

## Install

**Skills CLI** (copy-paste):

```bash
npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y
```

**Plugins CLI** (workflow bundles with deps — pick from the list):

```bash
npx plugins add PrunaAI/pruna-skills
# when prompted, select: gemini-3.1-flash-tts
```

Do **not** use `npx plugins add PrunaAI/pruna-skills@gemini-3.1-flash-tts` — the plugins CLI has no `@name` filter (that’s skills only) and prints “No plugins found”.

**Claude Code:**

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install gemini-3.1-flash-tts@pruna-skills
```

List all skills:

```bash
npx skills add PrunaAI/pruna-skills -l
```

After install, start a **new chat**. See the [root README](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/README/SKILL.md).

## From a local clone

```bash
npx skills add .@gemini-3.1-flash-tts -y
# or:
npx skills add ./plugins/gemini-3.1-flash-tts/skills --skill gemini-3.1-flash-tts -y
```
