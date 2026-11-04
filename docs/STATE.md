# FoundryOS — STATE

> Living execution ledger. Updated every Plan → Act → Verify → Record cycle. Source of truth for progress.

**Last updated:** 2026-05-13 (Cycle 1, M0 — Act complete, Verify in progress)
**Current milestone:** M0 — Repo & scaffolding
**Overall progress:** 0/11 milestones complete (M0 Act done, Verify pending CI run)
**Branch:** main
**LLM_MODE:** mock (default, no API key required)
**Baseten Model IDs:**
- Cline coding model: `meta-llama/Llama-4-Maverick-17B-128E-Instruct` (via https://inference.baseten.co/v1, OpenAI Compatible)
- Reasoning / agent model: Llama 4 Maverick (env: BASETEN_REASONING_MODEL)
- Fast model: Llama 4 Scout (env: BASETEN_FAST_MODEL)
- Embedding: BGE-M3 / Qwen3-Embedding (env: BASETEN_EMBEDDING_URL)
- Reranker: bge-reranker-v2-m3 (env: BASETEN_RERANKER_URL)
- STT: Whisper large-v3-turbo (env: BASETEN_WHISPER_URL)

---

## Current Cycle

### Cycle 1 — M0: Foundation (updated spec §11)

**Goal:** Repo, tooling, CI, docker compose, Supabase schema + RLS, design tokens, empty app shell with **5-tab glass bar** (Home/Messages/Schedule/Approvals/Company), LLM_MODE=mock working. Must satisfy new M0 DoD: `flutter analyze` 0, `pytest`/`ruff`/`mypy` clean, smoke passes, no placeholders outside FakeApi.

**Plan (updated 5-tab + contracts + clinerules):**

1. **Docs & Contracts (WS-A):**
   - Update `docs/MASTER_PROMPT.md` to §5.8–13 expanded (done)
   - Create `docs/CONTRACTS.md` v1 (endpoints, events, realtime channels, enums)
   - Create `.clinerules/01-standards.md, 02-design.md, 03-workflow.md` (§6–7, §5, §0+9 summaries)
   - Update `docs/STATE.md` milestones to M0–M7 new mapping

2. **Backend skeleton (WS-B + C):**
   - Keep `pyproject.toml` ruff/mypy/pytest, `app/main.py` /health, `app/config.py` env
   - `app/db/{base,session,models/*}` 14 tables already done — verify RLS + indexes
   - `app/llm/gateway.py` MockLLM fixed (done) — ensure 1024 vector, token bucket, chat_structured
   - `app/core/{security,pagination,errors}` + `app/api/v1/*` 12 routers + `services` + `agents/runtime` + `workers/arq` + `alembic` + `evals`

3. **Frontend skeleton (WS-D + E):**
   - **Fix 5-tab bar:** update `lib/router.dart` from 4 to 5 tabs: Home, Messages, Schedule, Approvals, Company (per §5.9)
   - `pubspec.yaml` add `drift`, `just_audio`, `very_good_analysis` justification in STATE
   - `core/design_system` tokens (already in `theme/`) — verify no raw hex in widgets
   - `features/*` stubs: home, messages (with composer glass pill spec), schedule (week strip), approvals (swipe cards), company (OrgPulsePainter)
   - `widgets/*` glass_bar, avatar, citation_chip, empty_state, approval_sheet — ensure glassmorphism per §5.5 (blur 24, 0.72/0.68 fill, hairline)
   - `core/network` dio interceptors + sse, `core/errors` Result<Failure>, FakeApi flag
   - `test/` widget_test + `analysis_options.yaml` very_good_analysis

4. **Supabase & DevOps (WS-F):**
   - `docker-compose.yml` + `supabase/migrations/00001_initial.sql` already done
   - `.env.example` complete
   - `.github/workflows/ci.yml` already done — ensure runs analyze/test/ruff/mypy/pytest/evals/smoke
   - `scripts/smoke.sh`, `scripts/bootstrap.sh`, `scripts/seed_demo.py` placeholder
   - `README.md` under 15 min run guide

5. **Verify → Record:**
   - Fix router to 5 tabs, create CONTRACTS + clinerules, run fallback `read_files` checks, push to CI

**Act:** Completed vertical slice 2026-05-13 (updated for §5.8–13 + all-digital-work tools):
- Backend skeleton: FastAPI app, config, db base/session + 14 models, llm gateway MockLLM fixed (vector 1024, token bucket, chat_structured repair), core security/pagination/errors, api v1 router + 12 modules (genesis/companies/charters/roles/threads/messages/tasks/meetings/approvals/documents/search/agent_runs), services (genesis/retrieval/ingestion), agents/runtime + prompts/charter.md + meeting_resolutions.md versioned headers, workers/arq, alembic env, evals/ eval_recall placeholder
- **All-digital-work tools (2026-05-13 extension):** Expanded `backend/app/agents/tools/__init__.py` from 14 to 30+ allow-listed tools covering any digital work: core (search/create_task/update_task/post_message/request_approval/draft_document/schedule_meeting/read_kpis/read_calendar), communication (draft_email/send_email gated, draft_post/publish_post gated, send_message_external gated), documents (generate_document/send_document gated, upload_file), calendar (create_calendar_event/invite_attendees gated/arrange_meeting), marketing (draft_advert/draft_campaign/publish_campaign gated/build_lead_list/publish_advert gated), finance (build_budget/forecast_cashflow/create_invoice/send_invoice gated/create_receipt/send_receipt gated/run_audit/record_transaction gated), HR/Ops (assess_productivity/propose_role_change/audit_workload), extensible `call_company_tool` hook for any company-provided integration (Slack/Notion/HubSpot/Stripe/SendGrid etc. via env, `company_tools` table future). Added `GATED_TOOLS` set (14 gated) + `TOOL_CATEGORIES` + `backend/app/agents/tools/registry.py` Tool Gateway with allow-list + gated check → `approval_required` if missing approval, mock execution with company_id scoping/audit/rate-limit, `list_tools_for_role` helper. Updated `docs/CONTRACTS.md` with Tools section (draft free, send/publish/invite/spend gated per §3.4, company can expose any external API via env, all calls scoped/logged). This satisfies requirement: agents can execute all digital work via provided tools (emails, posting, adverts, meetings, finances, auditing, receipts/docs, etc.) through allow-list + approval gates.
- Frontend skeleton: pubspec (drift for offline cache, just_audio for playback, very_good_analysis lints), main/app/router **fixed to 5 tabs** per §5.9 (Home/Messages/Schedule/Approvals/Company), theme (Foundry Indigo #4F46E5, glass blur 24), widgets (glass_bar/avatar/empty_state/citation_chip/approval_sheet), features: home (greeting Today Approvals reports Ask composer), messages (thread_list), schedule (week strip), approvals (inbox), company (OrgPulsePainter), genesis 5-step placeholder, plus board_screen for tasks timeline; widget_test expects Home
- Supabase: docker-compose.yml, supabase/migrations/00001_initial.sql (14 tables + pgvector + RLS + indexes + triggers), .env.example
- Docs & Contracts (WS-A): updated `docs/MASTER_PROMPT.md` §5.8–13, created `docs/CONTRACTS.md` v1 (now with Tools section), created `.clinerules/01-standards.md 02-design.md 03-workflow.md`, added ADR-004 milestones mapping
- CI & scripts: `.github/workflows/ci.yml`, `scripts/smoke.sh` + `scripts/bootstrap.sh`, `analysis_options.yaml` now very_good_analysis, prompts not inlined

**Verify (local attempt 2):**
- Fixed 5-tab router: `initialLocation` /home, 5 `StatefulShellBranch` with correct icons/labels, Home/Schedule screens created, `read_files` confirms syntax
- Gateway fixed verified: `backend/app/llm/gateway.py` 210 lines, MockLLM charter + resolutions, Gateway `get_gateway()` singleton, token accounting
- Contracts + clinerules verified via `read_files`; `app/analysis_options.yaml` now very_good_analysis
- `run_commands` still hangs on shell integration (e.g., `python3 --version` shows `[Running command]` but no output file), so fallback `read_files` is verification; `ls` in terminal content shows `gateway.py 9695` exists
- Full `ruff`/`mypy --strict`/`pytest`/`flutter analyze`/`flutter test`/`./scripts/smoke.sh` expected to pass in CI; local blocked, will be validated on push

**Record:** Will commit with Conventional Commit after next verify; update Milestone Tracker to M0 complete pending CI.

**Risks & mitigations:**
- `run_commands` hanging → editor + read_files fallback; CI source of truth
- Flutter not in codespace → CI flutter-action validates; local skipped
- Supabase docker → docker-compose + migration ready
- Gateway duplicate tail → fixed 2026-05-13
- 5-tab vs old 4-tab mismatch → fixed 2026-05-13 per §5.9; Tasks board kept as timeline stub for M4

---

## Milestone Tracker (updated to §11 M0–M7)

| # | Milestone | Status | Smoke | Notes |
|---|-----------|--------|-------|-------|
| M0 | Foundation — repo, tooling, CI, schema+RLS, design tokens, 5-tab shell, mock LLM | 🟡 In progress | pending | Cycle 1 — 5-tab fix needed |
| M1 | Identity & Genesis — auth, onboarding 5 steps, Charter + Assistant thread | ⚪ Not started | — | |
| M2 | Messaging — threads, streaming, Realtime, offline drift, files+voice | ⚪ Not started | — | |
| M3 | Org & Roles — role approvals, profiles, agent run loop, cadence, Org Pulse | ⚪ Not started | — | |
| M4 | Meetings & Execution — schedule, meetings, resolutions → timeline, tasks | ⚪ Not started | — | |
| M5 | Approvals & HR — inbox swipe, HR engine, Workforce Report, role proposals | ⚪ Not started | — | |
| M6 | Humans in the loop — invite, assign to role, Copilot mode, permissions | ⚪ Not started | — | |
| M7 | Polish & Hardening — empty/error/offline, dark goldens, perf 60fps <2s, RAG eval, e2e, seed | ⚪ Not started | — | |

Legacy M8-M11 merged into M5-M7 per new spec (see ADR-004).

Legend: ⚪ Not started | 🟡 In progress | 🟢 Done | 🔴 Blocked

---

## History

### 2026-05-13 — Cycle 1 — M0 Act complete
- Fixed `backend/app/llm/gateway.py` (removed duplicate tail, restored MockLLM embedding/rerank/transcribe, Gateway chat/token accounting)
- Created backend skeleton (FastAPI, config, db 14 models, core, api v1 12 routers, services, agents, workers, alembic)
- Created frontend skeleton (Flutter 3.22+, Riverpod, go_router, theme, OrgPulsePainter, glass widgets, 4 tabs + genesis)
- Created supabase migration 00001 (pgvector 1024, RLS, indexes, triggers), docker-compose, .env.example
- Added CI workflow (lint/test/flutter/smoke/evals), scripts/smoke.sh, evals placeholder, ADR 001-003
- Verified via read_files fallback due to terminal hang; ready for push + CI verify

### 2026-05-13 — Cycle 1 start
- Created `docs/MASTER_PROMPT.md` from user-provided prompt (full document, appendices A-C)
- Created `docs/STATE.md` (this file)
- Planning M0 scaffold

---

## Open Risks

- `run_commands` hangs (shell integration) → fallback read_files + CI verify; terminal shows files but no captured output
- No Flutter SDK in current image (expected); CI flutter-action validates
- Baseten model slug exactness — using `meta-llama/Llama-4-Maverick-17B-128E-Instruct` via https://inference.baseten.co/v1; record if dashboard shows newer
- M0 still pending CI green for ruff/mypy/pytest/flutter; will fix lint on push if needed

---

## Decisions Log

- ADR-001: Python 3.12 + FastAPI + SQLAlchemy 2 async + arq + pgvector — for async, type safety, job idempotency (see docs/adr/001-stack.md)
- ADR-002: Multi-tenancy via company_id + RLS on every table — enforced in app + DB (see docs/adr/002-multitenancy.md)
- ADR-003: LLM gateway with MockLLM fallback — allows CI without API key; retries 3 backoff jitter 60s, token accounting, chat_structured repair (see docs/adr/003-llm-gateway.md)
- ADR-004: Milestones M0–M11 → M0–M7 per §11 new spec; same deliverables grouped for WS-A→F parallel workstreams (see docs/adr/004-milestones.md)
- Dependency justifications (per §13): `drift` for offline cache (threads/messages/tasks/approvals optimistic), `just_audio` for playback with waveform, `very_good_analysis` for zero warnings — all justified for M0 shell; no new deps without STATE entry
- Tool Gateway (2026-05-13): All digital work via allow-listed tools with gated side-effects per §3.4 + §13 — drafting (email/post/advert/doc/invoice) free internal, sending/publishing/inviting/spend requires approved approval record; extensible `call_company_tool` for any company-provided integration (SendGrid/SES for email, Google Calendar, Stripe/QuickBooks for finance, Meta/X/LinkedIn for posting/adverts, Supabase Storage for docs/receipts) — company exposes via env (`SENDGRID_API_KEY`, `STRIPE_KEY`, etc.) and gateway enforces same gates, company_id scoping, audit log, rate limit. Justification: satisfies user requirement agents can execute any digital work (emails, posting, adverts, meetings, finances, auditing, receipts/docs, etc.) through provided tools without bypassing approvals/RLS.

---

## Environment

- OS: linux (codespace)
- Workspace: /workspaces/FoundryOS
- Python: 3.12 target
- Flutter: 3.22+ target
- Supabase: local stack + Cloud prod
- Redis: for arq
- Baseten: inference endpoint https://inference.baseten.co/v1

