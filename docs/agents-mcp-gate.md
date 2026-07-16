# Agents / MCP gate

Criteria for adding `agents/` or `.mcp.json` to plugins. **Do not implement** until a row below is met.

Skills + scripts + API keys remain the portable path for Cursor and cross-provider installs.

| Add when… | What to ship | Where |
|-----------|--------------|-------|
| Official Pruna MCP server exists | Single `.mcp.json` in **one** pilot plugin (`p-image` or `pruna-run`) | `plugins/<name>/.mcp.json` |
| Measured under-trigger on workflows | Claude activation hooks (Scott Spence pattern) | one workflow plugin only |
| Product wants a selectable "Pruna Studio" agent | One `agents/*.agent.md` under `pruna-full` | after eval shows need |

## Explicit non-goals

- No MCP or agents copied into all 27 plugins
- No Cursor dependency on MCP — any MCP is an optional enhancement for Claude/Copilot
- No agents/MCP in this repo until criteria above are recorded as met in [BACKLOG.md](../BACKLOG.md)

## Cross-provider rule

Cursor users must not depend on MCP. Keep generation callable via skill body + shell scripts + `PRUNA_API_KEY` alone.
