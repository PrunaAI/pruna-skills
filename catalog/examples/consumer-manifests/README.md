# Consumer manifests (APM, PSPM, and others)

Copy-paste examples for installing Pruna workflow skills with package managers other than `npx skills`.

**Full landscape:** [skill-package-managers.md](../../references/shared/skill-package-managers.md) (skills, APM, PSPM, ClawHub, Agensi, Claude plugins, skills-ref).

**Source:** `PrunaAI/pruna-ai-content-generation-skills/skills`  
**Workflow example:** `avatar-multi-scene` (depends on `p-image`, `p-image-edit`, `p-video-avatar`, `p-video-animate`)

Bundled workflow folders under `skills/<workflow>/` include `depends:` in `SKILL.md`, plus generated `apm.yml` and `pspm.json` from `tool_skills`.

## APM (`apm.yml` at project root)

```yaml
name: my-video-project
version: 1.0.0
targets:
  - cursor
  - claude
dependencies:
  apm:
    - PrunaAI/pruna-ai-content-generation-skills/skills/avatar-multi-scene
```

```bash
apm install
```

Installing the workflow path pulls transitive tool skills when the bundle’s `apm.yml` is present. To pin only tool skills explicitly:

```yaml
dependencies:
  apm:
    - PrunaAI/pruna-ai-content-generation-skills/skills/p-image
    - PrunaAI/pruna-ai-content-generation-skills/skills/p-image-edit
    - PrunaAI/pruna-ai-content-generation-skills/skills/p-video-avatar
    - PrunaAI/pruna-ai-content-generation-skills/skills/p-video-animate
    - PrunaAI/pruna-ai-content-generation-skills/skills/avatar-multi-scene
```

## PSPM (`pspm.json` at project root)

```json
{
  "$schema": "https://pspm.dev/schemas/pspm.json",
  "name": "@user/yourname/my-video-project",
  "version": "1.0.0",
  "githubDependencies": {
    "github:PrunaAI/pruna-ai-content-generation-skills/skills/avatar-multi-scene": "main"
  }
}
```

```bash
pspm install
```

Or add from the CLI:

```bash
pspm add github:PrunaAI/pruna-ai-content-generation-skills/skills/avatar-multi-scene
```

## skills CLI (reference)

```bash
npx skills add PrunaAI/pruna-ai-content-generation-skills/skills \
  --skill avatar-multi-scene --agent cursor -y
```

Sibling deps are listed in `SKILL.md` as `depends:`.

## Canonical deps (`skill.deps.json`)

Every workflow bundle includes machine-readable deps:

```bash
cat skills/avatar-multi-scene/skill.deps.json | jq '.depends, .resolvers'
```

## Validate (skills-ref)

```bash
npx skills-ref validate --allow-field depends ./skills/avatar-multi-scene
```

## Cross-manager map

| `tool_skills` / `depends` | APM entry | PSPM `githubDependencies` key |
|---------------------------|-----------|-------------------------------|
| `p-image` | `…/skills/p-image` | `github:PrunaAI/pruna-ai-content-generation-skills/skills/p-image` |
| `avatar-multi-scene` | `…/skills/avatar-multi-scene` | `github:PrunaAI/pruna-ai-content-generation-skills/skills/avatar-multi-scene` |

Full comparison: [skill-package-managers.md](../../references/shared/skill-package-managers.md).
