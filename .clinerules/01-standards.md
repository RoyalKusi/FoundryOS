# 01-standards — Flutter + Backend Standards (summarized §6–7)

- Flutter stable latest, Dart 3, M3 + Cupertino adaptive
- Feature-first clean architecture: app/(router,theme,di,bootstrap) core/(design_system,network,errors,utils,widgets) features/<feature>/{data,domain,presentation}
- Riverpod 2 codegen, AsyncNotifier, no setState beyond ephemeral
- go_router typed routes, auth redirect, deep links
- freezed + json_serializable, no dynamic in domain
- Dio interceptors (auth refresh, retry 5xx with backoff), SSE streaming, Supabase Realtime wrapped, drift offline cache, optimistic send, record (AAC 16kHz) + just_audio, file_picker chunked 25MB
- Sealed Failure, Result<T,Failure>, global error boundary, Sentry optional
- Tokens in core/design_system only, no raw hex
- a11y: semantics, VoiceOver/TalkBack, dynamic type
- Lints: very_good_analysis zero warnings
- Tests: unit notifiers/repos, widget per screen state, golden light/dark, one integration happy path
- Backend: Python 3.12 FastAPI Pydantic v2 SQLAlchemy 2 async, Alembic vs Supabase migrations ADR, app/{api,domain,services,agents,rag,llm,workers,db,core}, ruff+mypy strict, pytest ≥80% on agents/rag/services, prompts in app/agents/prompts/*.md versioned, Pydantic validation, env secrets only, OpenAPI sync ADR, JSON logs company_id/run_id/request_id, JWT RLS every table, prompt-injection defence
