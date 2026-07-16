# Generated plugins (do not edit)

Rebuilt from `tools/`, `guides/`, `workflows/` by `./scripts/bundle_all_skills.sh`.

Each folder is a self-contained plugin:

```text
plugins/<name>/.claude-plugin/plugin.json
plugins/<name>/skills/<name>/SKILL.md
plugins/pruna-full/skills/*               # all skills in one plugin
```

**Install (preferred):**
- `npx skills add PrunaAI/pruna-skills@p-image -y`
- `npx plugins add PrunaAI/pruna-skills -y` → pick a workflow or `pruna-full`

**Also:** `/plugin install <name>@pruna-skills` · ClawHub publish via `./scripts/publish_all_skills.sh`
