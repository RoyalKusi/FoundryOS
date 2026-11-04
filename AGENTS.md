# FoundryOS — 20 Parallel Agents Deployment
> Senior Architect full integration — frontend ↔ backend operational.

## Squads (4) — 20 Agents — Worktrees ws-b,ws-c,ws-d,ws-e + main orchestrator

**Platform A1-A4:** A1 Contracts&DB (A1 lead) v1 frozen 14 tables RLS pgvector; A2 Core API+Auth JWT company_id scoping; A3 Workers+Realtime arq SSE; A4 DevOps CI APK <15min

**Intelligence B1-B5:** B1 Gateway live Muse Spark fallback; B2 Genesis/Charter; B3 RAG ingest/retrieve recall@8; B4 Meetings/execution tool-gateway 30 tools 14 gated; B5 HR Workforce

**Experience C1-C8:** C1 Design tokens glass Indigo #4F46E5; C2 Genesis 5-step; C3 Home; C4 Messages threads/composer/streaming; C5 Schedule+Meeting; C6 Approvals swipe; C7 Company OrgPulse; C8 Role+Settings

**Integration D1-D3:** D1 Offline drift record/file_picker; D2 State Network Dio/Riverpod/Supabase FakeApi→Live; D3 QA goldens e2e perf

## Key Integration — D2 Orchestrator
- `core/network/dio_client.dart` interceptors auth refresh retry 5xx backoff
- `core/config.dart` dart-define LLM_MODE/BASENETEN_API_KEY
- Riverpod AsyncNotifier + go_router auth redirect + Supabase realtime wrappers
- Result<Failure> + Sentry + JSON logs company_id/run_id/request_id
- FakeApi flag `APP_USE_FAKE_API` never blocks backend

## Merge Protocol
- Worktrees isolated, merge only green analyze/test/ruff/mypy/pytest/smoke
- CONTRACT conflicts → A1 ADR; never LLM from app; never gated without approval

## APK
- `app/build/app/outputs/flutter-apk/app-release.apk` 53MB (mock)
- Live: `flutter build apk --release --dart-define=LLM_MODE=live --dart-define=BASETEN_API_KEY=b10_VhEr... --dart-define=BASETEN_REASONING_MODEL=meta-models/muse-spark-open-1026`
