# Backlog

Follow-ups from the skills repo review. Not blocking current releases.

## skills.sh listing

Listing is install-telemetry-driven (no submit API). **2026-07-16:** `https://skills.sh/prunaai/pruna-skills` redirects to `www.skills.sh` and returns **500** (page not ready). Keep text link in README; add badge only when the URL resolves cleanly.

## Eval prompts

Add 2–4 cheap eval prompts per tier (tool / guide / workflow) beyond [SKILL-TEST-LOG.md](SKILL-TEST-LOG.md). Baseline vs improved skill comparison is optional.

## Agents / MCP

Do **not** add `agents/` or `.mcp.json` unless criteria in [agents-mcp-gate.md](agents-mcp-gate.md) are met. Skills + curl + ffmpeg + API keys remain the happy path.

## Optional hygiene

- Dedupe identical OpenClaw entry stubs if ClawHub ever allows manifest-only bundles
- Collapse doc-examples maintainer scripts (generate + sync) if the pipeline grows further
