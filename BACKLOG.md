# Backlog

Follow-ups from the skills/plugins repo review. Not blocking current releases.

## Description trigger audit

Spot-check `SKILL.md` frontmatter `description` fields for trigger accuracy (when to fire / when not). Optional: Skill Creator–style trigger vs non-trigger query sets for the weakest descriptions.

## Copilot dual manifest

Only if native Copilot install fails without it: add `.github/plugin.json` alongside `.claude-plugin/plugin.json` (Chris Ayers dual-manifest pattern). Prefer verifying with `npx plugins` / Copilot CLI smoke first.

**2026-07-16 smoke:** `npx plugins discover` lists all 27 plugins (including updated `pruna-full` description). `npx plugins add … -t github-copilot` registers the marketplace, then fails with `spawnSync copilot ENOENT` because Copilot CLI is not installed on the smoke host — **not** a dual-manifest format failure. Re-run after `copilot` is available before adding `.github/plugin.json`.

## Eval prompts

Add 2–4 cheap eval prompts per tier (tool / guide / workflow) beyond [SKILL-TEST-LOG.md](SKILL-TEST-LOG.md). Baseline vs improved skill comparison is optional.

## Agents / MCP in plugins

Do **not** add `agents/` or `.mcp.json` unless a concrete product need appears (hosted Pruna MCP, measured activation hooks). Skills + scripts + API keys remain the happy path.

## Optional hygiene

- Dedupe identical OpenClaw entry stubs if ClawHub ever allows manifest-only bundles
- Single shared `_shared` script copy per workflow plugin (already mostly intentional embedding)
