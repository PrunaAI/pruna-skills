# Skill package managers compared

How agent **skill installers**, **registries**, and **marketplaces** relate to the [Agent Skills](https://agentskills.io/specification) format, where dependencies are declared, and how this repository keeps annotations aligned across tools.

> **Scope:** This doc covers tools that **install or distribute** `SKILL.md` bundles. It does not list every agent harness (Cursor, Claude Code, Codex, …) — only the package layers on top of the open skill format.

## Taxonomy

Not everything called a “skills marketplace” is a package manager.

| Kind | Role | Examples |
|------|------|----------|
| **Specification** | Defines `SKILL.md` + folder layout | [agentskills.io](https://agentskills.io/specification) |
| **Validator** | Lint / parse; no install graph | [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) |
| **Installer CLI** | Fetch skills → agent directories | `npx skills`, `apm`, `skillpm`, `openclaw skills` |
| **Registry / index** | Discovery, stats, search | [skills.sh](https://skills.sh), ClawHub, Skilldex registry |
| **Marketplace** | Curated catalog, often zip + payment | Agensi, Claude `/plugin` marketplaces |
| **Native plugin system** | Skills + agents + hooks + MCP in one bundle | Claude Code plugins, Copilot plugins, `.claude-plugin/plugin.json` |

**Pruna repo position:** we author in ``, ship self-contained plugins in `plugins/`, and generate cross-installer dependency hints from one `tool_skills` list.

## At a glance — installers

| | **skills** | **APM** | **Skilldex** | **OpenClaw / ClawHub** |
|---|------------|---------|--------------|------------------------|
| **CLI** | `npx skills add` | `apm install` | `skillpm` / `spm` | `openclaw skills install` / `clawhub install` |
| **Project manifest** | `skills-lock.json` (optional) | `apm.yml` | `skilldex.json` | workspace `skills/` + `.clawhub/origin.json` |
| **Lockfile** | hashes in lock | `apm.lock.yaml` | install metadata in manifest | ClawHub version pins |
| **Skill unit** | `SKILL.md` folder | skill bundle, `.apm/` package, plugin | `.skill` / `SKILL.md` package | `SKILL.md` bundle |
| **Also manages** | — | prompts, instructions, MCP, LSP | **skillsets** (bundled coherent groups) | OpenClaw-only trust verify |
| **Transitive deps** | `depends:` in `SKILL.md` ([#860](https://github.com/vercel-labs/skills/issues/860)) | `dependencies.apm` in `apm.yml` | remote refs in `SKILLSET.md`; git install | registry + `git:owner/repo@ref` |
| **Registry** | skills.sh + any GitHub | any git host | Skilldex registry (metadata) | ClawHub public registry |
| **Agents** | 68+ via symlinks | Copilot, Claude, Cursor, Codex, Gemini, … | Claude Code (MCP-native) | OpenClaw (+ portable `SKILL.md`) |

### Secondary channels (not full package managers)

| Channel | What it does | Dependency story |
|---------|--------------|------------------|
| **[skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref)** | `validate`, `read-properties`, `to-prompt` | None — use `--allow-field depends` for extended frontmatter |
| **[skills.sh](https://skills.sh)** | Public index for `npx skills`; install counts | Same as skills CLI |
| **[Agensi](https://www.agensi.io/skills)** | Curated marketplace; zip download or MCP catalog | Buyer installs manually; no shared lockfile |
| **Claude Code `/plugin`** | Native plugins (skills + hooks + MCP) | `plugin.json` + marketplace; skills namespaced `plugin:skill` |
| **Git clone / copy** | Universal fallback | You own the dependency list |

## Mental model

```text
agentskills.io (SKILL.md + scripts/ references/ assets/)
        │
        ├── skills (+ skills.sh)     … GitHub install, 68+ agents, depends: siblings
        ├── APM                      … full agent stack manifest (skills + MCP + prompts)
        ├── Skilldex (skillpm)       … scoped install, validation score, skillsets
        ├── OpenClaw / ClawHub       … OpenClaw registry + git/local install
        └── Marketplaces (Agensi, Claude plugins) … discovery + bundling, varied dep models
```

- **skills** — “install this skill folder from GitHub.”
- **APM** — “reproduce the whole agent setup for the team.”
- **Skilldex** — “install with scopes + quality score; bundle related skills as a **skillset**.”
- **ClawHub** — “OpenClaw’s versioned public registry.”
- **Agensi / Claude plugins** — discovery and distribution; you (or MCP) place files in skill dirs.

## Per-tool notes

### skills (`npx skills`) + skills.sh

- **Install:** `npx skills add owner/repo --skill name --agent cursor -y`
- **Discovery:** `npx skills find`, [skills.sh](https://skills.sh)
- **Deps:** proposed top-level `depends: [sibling-names]` in `SKILL.md` (same repo)
- **Strength:** widest agent coverage, zero project manifest required
- **Gap:** cross-repo `depends` still debated ([#860](https://github.com/vercel-labs/skills/issues/860))

### APM (Microsoft)

- **Install:** `apm install owner/repo/path#ref` → writes harness dirs + lockfile
- **Deps:** `dependencies.apm` with full git paths; transitive via nested `apm.yml`
- **Strength:** one manifest for skills **and** MCP; policy + security scan
- **Drop-in:** [documented migration from `npx skills`](https://github.com/microsoft/apm)

### Skilldex (`skillpm` / `spm`)

- **Install:** `skillpm install <path|git+https://…>` at global / shared / project scope
- **Deps:** individual skills from git; **skillsets** bundle multiple skills + shared `assets/`
- **SKILLSET.md:** frontmatter includes `skills:` list for remote skill refs; embedded skills auto-discovered
- **Strength:** spec conformance **scoring**, MCP tools (`skilldex_install`, …), skillset coherence
- **vs skills.sh:** Skilldex paper explicitly compares to vercel-labs/skills — adds scoping, scoring, skillsets ([arXiv:2604.16911](https://arxiv.org/abs/2604.16911))
- **This repo:** does not generate Skilldex skillsets; use `depends:` / `apm.yml` instead

### OpenClaw + ClawHub

- **Install:** `openclaw skills install @owner/slug` or `git:owner/repo@ref` or `./local/path`
- **Registry:** ClawHub (`clawhub install`, publish, version pins, trust verify)
- **Deps:** install multiple skills explicitly; no standard `depends` in spec today
- **Strength:** versioned public registry + trust envelope for OpenClaw agents
- **Portable:** still `SKILL.md`; same bundles work outside OpenClaw via other CLIs

### Claude Code plugins (native)

- **Install:** `/plugin install name@marketplace` or `claude plugin install …`
- **Unit:** plugin = skills + agents + hooks + MCP (not skills-only)
- **Deps:** marketplace + plugin manifest; skills namespaced (`plugin-name:skill-name`)
- **When to use:** need hooks/MCP bundled with skills inside Claude Code only

### Agensi (marketplace)

- **Install:** download zip → unzip to `~/.claude/skills/` (or MCP on-demand catalog)
- **Not** a dependency resolver — commerce + security scan + discovery
- **Portable:** sells standard `SKILL.md` zips usable elsewhere

### skills-ref (validator only)

```bash
npx skills-ref validate ./plugins/p-image/skills/p-image
npx skills-ref validate --allow-field depends ./plugins/avatar-multi-scene/skills/avatar-multi-scene
```

Use `--allow-field depends` (and any harness-specific fields) until `depends` enters the base spec allowlist ([#350](https://github.com/agentskills/agentskills/pull/350)).

## Dependency annotation — layers

### 1. Agent Skills spec (portable)

Official fields: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. **No standard `depends` yet.**

### 2. skills CLI — `depends:` in `SKILL.md` (proposed)

```yaml
depends:
  - p-image
  - p-image-edit
  - p-video-avatar
  - p-video-animate
```

Sibling **names** in the same source tree. Unknown keys should be ignored by other tools.

### 3. Package-manager manifests (installer-readable)

| Tool | File | Dep format | Example |
|------|------|------------|---------|
| **skills** | `SKILL.md` | YAML list of **sibling names** | `depends: [p-image]` |
| **APM** | `apm.yml` | YAML `dependencies.apm` **full paths** | `PrunaAI/…/skills/p-image` |
| **Canonical** | `skill.deps.json` | JSON `depends` + optional `resolvers` | machine interchange |

**Rule:** short names only in `SKILL.md`. Full paths / URLs only in sidecar manifests (generated, not hand-edited).

### 4. This repo — `tool_skills` (authoring source of truth)

```json
{ "tool_skills": ["p-image", "p-image-edit", "p-video-avatar", "p-video-animate"] }
```

`make bundle` runs `.maintainer/write_dep_manifests.py` and emits:

| Output | Consumer |
|--------|----------|
| `SKILL.md` → `depends:` | `npx skills` (sibling names) |
| `apm.yml` | APM (full repo paths) |
| `skill.deps.json` | canonical JSON + `resolvers` |

**Author once:** `tool_skills` in `**/skill.manifest.json` only — do not hand-edit dep sidecars in `plugins/`.

## Install equivalents (this repository)

Preferred skills CLI form: `PrunaAI/pruna-skills@<name>`. APM still needs the full plugin skill path.

```bash
# skills CLI (default)
npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y
npx plugins add PrunaAI/pruna-skills -y   # pick avatar-multi-scene

# APM (full git path)
apm install PrunaAI/pruna-skills/plugins/avatar-multi-scene/skills/avatar-multi-scene

# Claude plugin marketplace
/plugin install avatar-multi-scene@pruna-skills
```

Copy-paste project manifests: [consumer-manifests](../../references/consumer-manifests/README.md).

## Cross-manager annotation matrix

| Concern | skills | APM | Skilldex | OpenClaw | Recommendation |
|---------|--------|-----|----------|----------|----------------|
| **Identity** | `name` in `SKILL.md` | path in `apm.yml` | package name / folder | slug from `name` or `--as` | `name` === folder name everywhere |
| **Version** | `metadata.version` | `version` in `apm.yml` | registry version | ClawHub version tag | repo [`VERSION`](../../../VERSION) at bundle time |
| **Sibling deps** | `depends: [short names]` | full `owner/repo/skills/name` | `SKILLSET.md` `skills:` | multiple installs | generate from `tool_skills` |
| **Coherent bundles** | repeated `--skill` or `depends` | transitive `apm.yml` | **skillset** + shared assets | meta-package on ClawHub | `depends:` + repeated installs |
| **Runtime reqs** | `compatibility` | — | scored in validate | — | document API keys in `compatibility` |
| **Validation** | skills-ref | apm scan (unicode) | publish checks | conformance score /100 | `openclaw skills verify` | CI: `skills-ref validate --allow-field depends` |

### Rules (avoid breakage)

1. **Short names in `depends:` only** — no GitHub paths in `SKILL.md`.
2. **Full paths in `apm.yml` only** — generated in `plugins/`, not hand-edited.
3. **Don’t encode installer logic in `metadata`** — use per-tool dep fields.
4. **Bundled `references/` are copies** — tool skills are separate installs, not `../p-image/`.
5. **Extra frontmatter is safe** — tools that don’t know `depends` should ignore it.
6. **Plugin ≠ skill** — Claude plugins namespace skills; don’t assume `/p-image` works the same as a raw install.

## When to use which

| You need… | Use |
|-----------|-----|
| Fast install to Cursor / Codex / many agents | `npx skills add` |
| Search + popularity signals | skills.sh |
| Team agent stack (skills + MCP + lockfile) | APM |
| Scoped install + quality score + skill bundles | Skilldex |
| OpenClaw agent + public versioned registry | ClawHub / `openclaw skills` |
| Paid / reviewed marketplace catalog | Agensi |
| Skills inside Claude Code with hooks/MCP | `/plugin install` |
| Validate format in CI | skills-ref |

## Ecosystem direction

Likely convergence:

1. **agentskills.io** adopts optional `depends` (sibling + optional remote).
2. **skills-ref** adds `depends` to the default allowlist.
3. **APM** read `depends` when present and map to their native dep fields.
4. **Skillsets** (Skilldex) or **meta-packages** (ClawHub) express workflow + tool skills as one install unit.

Until then: **author `tool_skills` once** in ``, bundle to `depends` + `apm.yml`.

## Links

| Tool | Docs |
|------|------|
| Agent Skills spec | [agentskills.io/specification](https://agentskills.io/specification) |
| skills-ref | [github.com/agentskills/agentskills](https://github.com/agentskills/agentskills/tree/main/skills-ref) |
| skills CLI + skills.sh | [github.com/vercel-labs/skills](https://github.com/vercel-labs/skills) · [#860 depends](https://github.com/vercel-labs/skills/issues/860) |
| APM | [microsoft.github.io/apm](https://microsoft.github.io/apm/) |
| Skilldex | [github.com/Pandemonium-Research/Skilldex](https://github.com/Pandemonium-Research/Skilldex) · [paper](https://arxiv.org/abs/2604.16911) |
| OpenClaw / ClawHub | [docs.openclaw.ai/tools/skills](https://docs.openclaw.ai/tools/skills) |
| Agensi | [agensi.io/skills](https://www.agensi.io/skills) |
| Claude plugins | [code.claude.com/docs/en/discover-plugins](https://code.claude.com/docs/en/discover-plugins) |
