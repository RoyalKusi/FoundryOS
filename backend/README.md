# FoundryOS Backend

Core API: FastAPI + SQLAlchemy 2 async + arq + Supabase + Baseten LLM gateway.

## Quick start

```bash
cp ../.env.example .env  # or root .env.example
docker compose up          # from repo root
# API at http://localhost:8000, docs at /docs
```

## Verify

```bash
ruff check app
mypy --strict app
pytest -q
```

LLM_MODE=mock by default — no API key needed.

## Structure

- `app/main.py` — FastAPI app factory
- `app/config.py` — env via pydantic-settings
- `app/db/` — models + session
- `app/api/v1/` — route modules
- `app/llm/gateway.py` — single LLM entry point with MockLLM
- `app/agents/` — runtime + tools + profiles
- `app/workers/` — arq jobs
