# Skill catalog (sources)

Authoring lives here. **`skills/`** at the repo root is the generated install tree — do not edit it by hand.

```text
catalog/
  references/          API specs, checklists, workflow docs
  tools/               one skill per model (p-image, p-video, …)
  workflows/           multi-step workflows
    _shared/scripts/   shared runners (bundled into skills)
  examples/            starter prompts and templates (mirrors workflows layout)

skills/                generated install bundles (repo root — do not edit)
scripts/               repo build tooling (bundle, install, pre-commit — not skill content)
```

Regenerate portable bundles:

```bash
./scripts/bundle_all_skills.sh
./scripts/verify_skill_bundles.sh
```

Pre-commit runs `bundle_all_skills.sh` when `catalog/` or bundle scripts change.

**Dependencies:** workflow `skill.manifest.json` → `tool_skills` only. Bundling runs `write_dep_manifests.py` → `depends:`, `apm.yml`, `pspm.json`, `skill.deps.json`. See [skill-package-managers.md](references/shared/skill-package-managers.md).

Install for agents: `npx skills add ./skills --skill <name> --agent cursor -y`

Publish to PSPM: [`PUBLISHING.md`](PUBLISHING.md) (`./scripts/publish_all_skills.sh`).

Pruna-internal launch content stays in `.mine/` (not in public `skills/` bundles).
