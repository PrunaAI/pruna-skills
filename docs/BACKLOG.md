# Backlog

Follow-ups from the skills/plugins repo review. Not blocking current releases.

## Description trigger audit

Done for v1.0.3+ follow-up: all 26 primary `description` fields rewritten (natural tone, full media breadth). Style guide: [skill-description-style.md](skill-description-style.md). Trigger / non-trigger table: [SKILL-TEST-LOG.md](SKILL-TEST-LOG.md) § Description audit. Optional later: Skill Creator harness if mis-triggers persist.

## Copilot dual manifest

Only if native Copilot install fails **on format** without it: add `.github/plugin.json` alongside `.claude-plugin/plugin.json` (Chris Ayers dual-manifest pattern). Prefer verifying with `npx plugins` / Copilot CLI smoke first.

**2026-07-16 smoke:** `npx plugins discover` lists all 27 plugins. `npx plugins add … -t github-copilot` fails with `spawnSync copilot ENOENT` / Copilot CLI not installed — **not** a dual-manifest format failure. **Re-check 2026-07-16 (post-release):** `copilot` still not on PATH. Do **not** add dual manifests until CLI smoke can distinguish format vs missing binary.

## skills.sh listing

Listing is install-telemetry-driven (no submit API). **2026-07-16:** `https://skills.sh/prunaai/pruna-skills` redirects to `www.skills.sh` and returns **500** (page not ready). Keep text link in README; add badge only when the URL resolves cleanly.

**Team bootstrap (one message):**

```bash
npx skills add PrunaAI/pruna-skills@p-image -y
npx skills add PrunaAI/pruna-skills@pruna -y          # interactive → music-video
# or: npx skills add PrunaAI/pruna-skills@pruna -y -y  # installs ALL 27
```

## Eval prompts

Add 2–4 cheap eval prompts per tier (tool / guide / workflow) beyond [SKILL-TEST-LOG.md](SKILL-TEST-LOG.md). Baseline vs improved skill comparison is optional.

## Agents / MCP in plugins

Do **not** add `agents/` or `.mcp.json` unless criteria in [agents-mcp-gate.md](agents-mcp-gate.md) are met. Skills + scripts + API keys remain the happy path.

## Optional hygiene

- Dedupe identical OpenClaw entry stubs if ClawHub ever allows manifest-only bundles
- Single shared `_shared` script copy per workflow plugin (already mostly intentional embedding)
