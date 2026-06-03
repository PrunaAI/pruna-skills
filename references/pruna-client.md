# Pruna Python client (`pruna_client`)

PyPI package [pruna-client](https://pypi.org/project/pruna-client/) (v0.0.9+). Requires **Python 3.11+**.

## Install

```bash
export PRUNA_API_KEY="your_key"
uv add pruna-client   # or: uv sync (already in pyproject.toml)
uv run python scripts/pruna.py list
```

## CLIs in this repo

| Script | Purpose |
|--------|---------|
| `scripts/pruna.py` | Subcommands for every first-party model |
| `scripts/pruna_run.py` | Auto-route prompt → image / i2v / avatar chain |
| `scripts/pruna_batch.py` | Parallel async batch from JSON |

## Workflow integration

`guides/workflows/_shared/scripts/pruna_api.py` wraps the SDK with the same function names used by comparison runners (`upload_file`, `run_prediction`, …).

## Model coverage

See [pruna-models.md](./pruna-models.md). CLI `python3 scripts/pruna.py list` prints sync defaults.
