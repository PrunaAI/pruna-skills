# Agents / MCP gate

Criteria for adding `agents/` or `.mcp.json` to this repo. **Do not implement** until a row below is met.

Skills + curl + ffmpeg + API keys remain the portable path for Cursor and cross-provider installs.

| Add when… | What to ship | Where |
|-----------|--------------|-------|
| Official Pruna MCP server exists | Single `.mcp.json` in **one** pilot skill (`p-image` or `pruna` suite) | `skills/<category>/<name>/.mcp.json` |
| Measured under-trigger on workflows | Claude activation hooks (Scott Spence pattern) | one workflow skill only |
| Product wants a selectable "Pruna Studio" agent | One `agents/*.agent.md` under `pruna` | after eval shows need |

## Explicit non-goals

- No MCP or agents copied into all 26 skills
- No Cursor dependency on MCP — any MCP is an optional enhancement for Claude/Copilot
- No agents/MCP in this repo until criteria above are recorded as met in [BACKLOG.md](BACKLOG.md)

## Cross-provider rule

Cursor users must not depend on MCP. Keep generation callable via skill body + shell + `PRUNA_API_KEY` alone.
