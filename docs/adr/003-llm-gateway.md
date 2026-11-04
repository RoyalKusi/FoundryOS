# ADR-003: LLM Gateway with MockLLM

All LLM calls go through `backend/app/llm/gateway.py`. Provides:

- Retries with exponential backoff + jitter (max 3), 60s timeout
- Streaming, JSON-schema structured output with validation + one repair retry
- Token accounting per company/role, TokenBucket rate limit (Redis-backed in prod)
- MockLLM when `LLM_MODE=mock` — deterministic charter, resolutions, embeddings, transcription — so tests + smoke pass with no API key.

Why Baseten OpenAI-compatible? Single endpoint for Maverick (reasoning) and Scout (fast), plus self-hosted embeddings/reranker/Whisper via Truss. Env-configured, never hard-coded.

Alternatives: direct OpenAI, Anthropic — rejected due to vendor lock, lack of open embeddings.
