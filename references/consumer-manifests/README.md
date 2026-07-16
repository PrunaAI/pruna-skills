# Consumer manifests (APM and others)

Copy-paste examples for installing Pruna workflow skills with package managers other than `npx skills`.

**Full landscape:** [skill-package-managers.md](../../references/shared/skill-package-managers.md) (skills, APM, ClawHub, Agensi, Claude plugins, skills-ref).

**Preferred install:** `npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y` or `npx plugins add PrunaAI/pruna-skills -y`.  
**APM source path:** `PrunaAI/pruna-skills/plugins/<name>/skills/<name>`  
**Workflow example:** `avatar-multi-scene` (embeds `p-image`, `p-image-edit`, `p-video-avatar`, `p-video-animate` in the same plugin)

Fat workflow plugins include tool skills under `plugins/<workflow>/skills/`. The primary workflow skill also has `depends:`, `apm.yml`, and `skill.deps.json`.

## APM (`apm.yml` at project root)

```yaml
name: my-video-project
version: 1.0.0
targets:
  - cursor
  - claude
dependencies:
  apm:
    - PrunaAI/pruna-skills/plugins/avatar-multi-scene/skills/avatar-multi-scene
```

```bash
apm install
```

To pin tool skills as standalone plugins:

```yaml
dependencies:
  apm:
    - PrunaAI/pruna-skills/plugins/p-image/skills/p-image
    - PrunaAI/pruna-skills/plugins/p-image-edit/skills/p-image-edit
    - PrunaAI/pruna-skills/plugins/p-video-avatar/skills/p-video-avatar
    - PrunaAI/pruna-skills/plugins/p-video-animate/skills/p-video-animate
    - PrunaAI/pruna-skills/plugins/avatar-multi-scene/skills/avatar-multi-scene
```

## skills CLI (reference)

```bash
npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y
npx plugins add PrunaAI/pruna-skills -y   # pick avatar-multi-scene
```

## Plugin marketplace

```bash
/plugin marketplace add PrunaAI/pruna-skills
/plugin install avatar-multi-scene@pruna-skills
```

## Canonical deps (`skill.deps.json`)

```bash
cat plugins/avatar-multi-scene/skills/avatar-multi-scene/skill.deps.json | jq '.depends, .resolvers'
```

## Validate (skills-ref)

```bash
npx skills-ref validate --allow-field depends ./plugins/avatar-multi-scene/skills/avatar-multi-scene
```

## Cross-manager map

| `tool_skills` / `depends` | APM entry |
|---------------------------|-----------|
| `p-image` | `…/plugins/p-image/skills/p-image` |
| `avatar-multi-scene` | `…/plugins/avatar-multi-scene/skills/avatar-multi-scene` |

Full comparison: [skill-package-managers.md](../../references/shared/skill-package-managers.md).
