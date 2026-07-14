# Generated plugins (do not edit)

Rebuilt from `tools/`, `guides/`, `workflows/` by `./scripts/bundle_all_skills.sh`.

Each folder is a self-contained plugin:

```text
plugins/<name>/.claude-plugin/plugin.json
plugins/<name>/skills/<name>/SKILL.md
plugins/pruna-full/skills/*               # all skills in one plugin
```

**Install options:**
- Standalone tool/router: `/plugin install p-image@pruna-skills`
- Workflow with deps embedded: `/plugin install avatar-multi-scene@pruna-skills`
- Everything: `/plugin install pruna-full@pruna-skills`
- npx skills: `npx skills add ./plugins/<name>/skills --skill <name>`
- ClawHub plugin: `clawhub package publish ./plugins/<name>`
- ClawHub skill: `clawhub skill publish ./plugins/<name>/skills/<name>`
