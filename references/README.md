# References

Shared markdown library for skill authors. **Not installable** — users never pick a “references” skill. Bundling copies selected files into each portable skill’s `references/` folder by **basename**.

Do not confuse this tree with **reference images** in API prompts (photos you upload for edit/try-on).

```text
references/
  policies/     # mandatory generation policy (auto-injected into every skill)
  shared/       # API, credentials, agent-safety, variety bible, personas
  image/        # p-image family quality checklists
  video/        # p-video family checklists + scene-anchor triple/pair
  audio/        # narration + bed post-production
  workflows/    # deliverable-specific specs (explainer scenes, music video QA)
  consumer-manifests/  # packaging metadata for external registries (not agent playbooks)
```

## Two consumption paths

| Kind | Location | How it ships |
|------|----------|--------------|
| **Policies** (mandatory) | [`policies/`](policies/) | [`inject_policies.py`](../.maintainer/inject_policies.py) copies 3 files into every Tool and 7 into every Workflow, and injects a marked **Shared generation policy** section into `SKILL.md`. Do **not** list these basenames in `skill.manifest.json`. |
| **Skill-specific refs** | `shared/`, `image/`, `video/`, `audio/`, `workflows/` | List basenames in that skill’s `skill.manifest.json` `references` array; [`install_skill.sh`](../.maintainer/install_skill.sh) copies them at bundle time. |

**Policies hub:** [policies/generation-quality-checklists.md](policies/generation-quality-checklists.md) — core gate + model checklist map.

**Credentials:** [shared/api-credentials.md](shared/api-credentials.md) — Pruna + Replicate signup when keys are missing.
