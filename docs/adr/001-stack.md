# ADR-001: Stack Choices

- **Python 3.12 + FastAPI + Pydantic v2 + SQLAlchemy 2 async** — type-safe, async, FastAPI auto-docs, pydantic-settings for config.
- **Supabase Postgres + pgvector + Realtime + Auth + Storage** — single vendor for DB, auth, realtime; pgvector for RAG.
- **arq + Redis** — lightweight async job queue, idempotent job keys, easy to scale workers.
- **Flutter Riverpod + go_router + Supabase Flutter** — modern state, typed routing, native realtime.
- **Baseten OpenAI-compatible + MockLLM** — single gateway abstraction allows CI without API key, token accounting, retries.

Alternatives considered: Celery (heavier), Prisma+Next.js (would lose Flutter native), Firebase (less SQL/RLS flexibility).
