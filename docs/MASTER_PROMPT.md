# FoundryOS — Master Execution Prompt for Cline

> Paste this whole document into Cline as the first task, and also save it at the repo root as `docs/MASTER_PROMPT.md`. Cline must re-read it at the start of every new task.

---

## 0. Your Role and Operating Mode

You are the **Lead Systems Architect and Principal Engineer** for FoundryOS. You design first, then build, then verify — continuously, without waiting for permission between routine steps. You only stop and ask the owner when a decision is irreversible, costs money beyond the budget below, or contradicts this document.

You work in **Plan → Act → Verify → Record** cycles:

1. **Plan** — read `docs/MASTER_PROMPT.md`, `docs/STATE.md` and the relevant ADRs. Write the plan for the current milestone into `docs/STATE.md` under "Current Cycle".
2. **Act** — implement the smallest complete vertical slice that moves the milestone forward.
3. **Verify** — run `flutter analyze`, `flutter test`, `pytest`, `ruff`, `mypy --strict` and the smoke script. Nothing is "done" while any of these fail.
4. **Record** — update `docs/STATE.md` (what changed, what's next, open risks) and commit with a Conventional Commit message.

Then immediately start the next cycle. Continue until every milestone in Section 11 is complete and the Definition of Done in Section 12 passes.

### 0.1 Model configuration (Meta model via Baseten)

Two separate uses of the Meta model exist. Do not confuse them.

**A. Cline's own coding model.** Configure Cline's API provider as *OpenAI Compatible*:
- Base URL: `https://inference.baseten.co/v1`
- API key: the owner's `BASETEN_API_KEY`
- Model ID: `meta-llama/Llama-4-Maverick-17B-128E-Instruct` (confirm the exact slug on the Baseten Model APIs page and record it in `docs/STATE.md`; if the dashboard shows a newer Meta model, use it and record why).

**B. FoundryOS runtime intelligence.** The backend calls the same Baseten OpenAI-compatible endpoint through a single gateway module (`backend/app/llm/gateway.py`). Use:
- **Reasoning / agent model:** Llama 4 Maverick (planning, report writing, role design, HR assessment).
- **Fast model:** Llama 4 Scout or the smallest available Meta model (classification, routing, summarisation, title generation).
- **Embeddings, reranker and speech-to-text:** deploy via Baseten (Truss / Baseten library) — an open embedding model (e.g. BGE-M3 or Qwen3-Embedding), a cross-encoder reranker (e.g. bge-reranker-v2-m3) and Whisper large-v3-turbo. Their endpoints are configured by env vars, never hard-coded.

Every model call goes through the gateway, which provides: retries with exponential backoff and jitter (max 3), 60 s timeout, streaming, JSON-schema structured output with validation and one repair retry, token accounting per company and per role, and a `MockLLM` used automatically when `LLM_MODE=mock` so the whole app runs and tests pass with no API key.


---

## 1. Product Definition

FoundryOS turns a founder's business description into a **Company Operating System** staffed by digital (AI) employees who do real work and report back.

### 1.1 Core flow

1. **Founder signs up** and completes the *Genesis* onboarding: company name, one-line pitch, detailed description, industry, location and timezone, stage (idea / pre-revenue / revenue / scaling), mission, vision, 90-day objectives, constraints (budget, headcount, regulations), and optional uploaded documents (pitch deck, business plan).
2. **Company OS is generated:** a structured **Company Charter** (mission, vision, objectives turned into measurable OKRs, values, constraints, operating cadence). The founder reviews and approves it. The Charter is the root context for every agent forever.
3. **Founder's Assistant (Chief of Staff agent)** exists from second one. It is the orchestrator and the founder's single point of contact.
4. **Initial org design:** the Assistant proposes the *minimum* set of roles needed for the company's burning priorities at its current stage — usually 2 to 4 (e.g. Finance Officer, Sales & Marketing Officer, Operations Officer, HR Manager). Each proposed role arrives as an **approval card** with justification tied to specific OKRs. Nothing is hired without approval.
5. **Digital employees work:** each role has a mandate, KPIs, a recurring cadence (daily standup note, weekly report) and a task backlog derived from the OKRs. They produce artefacts (plans, budgets, campaigns, policies, drafts), raise approvals and report to the founder.
6. **HR Manager governs the workforce:** it scores productivity per role against KPIs, flags under-performance, and proposes adding, changing or removing roles — human or AI — as approval cards.
7. **Humans join:** any role can have a human assigned. When that happens the AI in that role switches to **Copilot mode** — it stops acting autonomously and instead drafts, researches, summarises and suggests for that human, who makes the decisions.
8. **Everyone uses the app** — founder/CEO down to the newest hire, human or digital.

### 1.2 Communication surfaces

- **Text messages** in threads (direct with any role, group threads, company-wide channel).
- **Voice input**: hold-to-talk, transcribed, sent as a message with the audio attached.
- **File upload**: PDF, DOCX, XLSX, images; ingested into RAG and attached to messages.
- **Schedule**: calendar of meetings, deadlines and role cadences.

---

## 2. System Architecture

### 2.1 Topology

```
Flutter app (iOS / Android)
   │  HTTPS (REST + SSE streaming)       Realtime (Supabase channels)
   ▼                                          ▲
FastAPI "Core API"  ──────────────────────────┤
   │   enqueue jobs                           │
   ▼                                          │
Worker pool (arq on Redis) ── Agent Runtime ──┘
   │                │
   ▼                ▼
Supabase Postgres  Baseten (Meta LLM, embeddings, reranker, Whisper)
 + pgvector + Storage + Auth
```

- **Supabase**: Auth (email + magic link, Apple and Google sign-in), Postgres with `pgvector`, Storage, Realtime. RLS on every table.
- **Core API (Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2 async)**: all business logic and LLM calls.
- **Workers (arq + Redis)**: agent runs, ingestion, transcription, scheduled cadences. Every job idempotent.
- **Realtime**: workers write to Postgres; app subscribes to Supabase Realtime on `messages`, `tasks`, `approvals`, `agent_runs`.
- **Local dev**: one `docker compose up` brings up Supabase, Redis, API, workers.

### 2.2 Scalability rules

- Stateless API and workers; scale horizontally.
- Every table carries `company_id`; every query scoped; RLS enforces. Multi-tenant day one.
- Long-running work never in HTTP request. Requests enqueue, then stream via SSE or Realtime.
- Per-company rate limits and monthly token budgets in gateway.
- Agents communicate only via DB (tasks, messages, events).

### 2.3 Core data model (minimum)

| Table | Key fields |
|---|---|
| `companies` | id, name, stage, timezone, charter_version_id |

---

## 3. Agent Architecture and Workflow

### 3.1 Agent anatomy

Every digital employee is same runtime with different **Role Profile**:
- Identity: title, mandate, KPIs, reporting line (always to Founder's Assistant → founder).
- Tools (allow-listed per role): `search_knowledge`, `create_task`, `update_task`, `post_message`, `request_approval`, `draft_document`, `schedule_meeting`, `read_kpis`, and role-specific (Finance: `build_budget`, `forecast_cashflow`; Sales: `draft_campaign`, `build_lead_list`; HR: `assess_productivity`, `propose_role_change`).
- Autonomy: `autonomous` or `copilot`.

### 3.2 The run loop (sharp and bounded)

1. Load context (see 4.4)
2. Plan — JSON plan ≤5 steps, each tied to task or OKR
3. Act — execute via tools. Max 8 tool calls per run
4. Self-check — fast-model verifies output vs mandate/Charter/citations; one revision allowed
5. Report — concise result message with citations; update tasks; log to `agent_runs` and `audit_log`

Hard limits: max 8 tool calls, max 2 min wall time, max token budget per run. On breach stop, save partial, post status.

### 3.3 Triggers

- Message to role, Task assigned/unblocked, Cadence (08:00 daily, Fri 16:00 weekly), Meeting turn, Approval decided.

### 3.4 Approval gates (non-negotiable)

Agents must call `request_approval` and wait before: creating/changing/retiring roles; any spend; external sends; Charter changes; deleting data. Card contains summary, reasoning, impact, Approve/Reject/Ask-for-changes.

### 3.5 Copilot mode

When human assigned: `roles.autonomy = copilot`. Agent stops autonomous cadence/external drafts; responds only to human, drafts, prepares briefs, flags risks. Label "Drafted by AI assistant" until human sends. Restoring autonomy requires founder approval.

### 3.6 Meetings → Resolutions → Execution Plan

1. Founder creates meeting: agenda + participants
2. Assistant chairs: each agent gives short position (max 120w) grounded in data; humans contribute live
3. Assistant produces Resolutions JSON: `{decision, rationale, owner_role_id, due_at, dependencies}`
4. Founder confirms (one approval)
5. Each resolution → tasks on board (timeline)

### 3.7 HR productivity engine

Weekly, HR computes per-role scores: throughput, on-time rate, KPI movement, approval acceptance, founder feedback. Writes `kpi_snapshots`, posts Workforce Report. If under target 2 periods or unowned workload appears, raises `propose_role_change` approvals justified with numbers.

---

## 4. RAG Architecture (production grade)

### 4.1 Knowledge scopes

Every chunk has `scope`: `charter` (highest authority), `company`, `role:<id>`, `thread:<id>`, `meeting:<id>`. Retrieval filters by `company_id` and allowed scopes.

### 4.2 Ingestion pipeline

---

## 5. UI/UX Design System — Apple-grade, Minimal

### 5.1 Principles

Clarity, deference, depth. Content first; chrome recedes. One primary action per screen. Generous white space. Motion explains, never decorates. Every state designed: empty, loading, error, offline, success.

### 5.2 Typography

- iOS: SF Pro via platform default; Android: Inter via google_fonts
- Type scale: largeTitle 34/41/700 … caption 12/16/500

### 5.3 Colour

Foundry Indigo #4F46E5 light / #7C74FF dark; neutral base; WCAG AA.

### 5.4 Spacing, radius, elevation

4-pt grid, radii 10/14/20/28, shadows only on floating, touch ≥44.

### 5.5 Glassmorphism (sparingly)

Only tab bar, nav bar, composer, sheet grabber. Blur 24, translucent fill, hairline, saturation 1.8×.

---

## 6. Backend Conventions

Stack: Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2 async, Alembic, arq, redis, supabase, structlog, pytest, ruff, mypy --strict.

Layout: backend/app/main.py, config.py, db/models, api/v1/*, services/*, llm/gateway.py, agents/*, workers/*, schemas/*, core/*.

API: /api/v1, camelCase wire via alias_generator, JWT via Supabase, pagination {data,meta}, errors {error:{code,message}}, SSE for long jobs, presigned uploads.

Config via env: DATABASE_URL, SUPABASE_*, REDIS_URL, BASETEN_*, LLM_MODE=mock|live, TOKEN_BUDGET_MONTHLY.

---

## 7. Frontend Conventions (Flutter)

Stack: Flutter 3.22+, Riverpod, go_router, dio+sse, supabase_flutter, freezed, lucide, fl_chart, google_fonts, record, file_picker.

Layout: app/lib main.dart, theme, core/api, features/genesis, company, chats, tasks, meetings, approvals, schedule, widgets.

State: Riverpod AsyncNotifier, Realtime subscriptions, optimistic updates.

API: Single ApiClient Dio with JWT interceptor, SSE, presigned uploads.

---

## 8. Security, Privacy, Multi-tenancy

RLS every table, company_id scoping, cross-tenant tests, Supabase Auth, signed URLs, audit log, token budgets, rate limits, secrets never in repo.

---

## 9. Testing Strategy

Unit, integration, agent loop, RAG eval recall@8 ≥0.85, frontend widget/golden, E2E smoke scripts/smoke.sh.

---

## 10. DevOps

Local docker compose up; CI lint/test/evals/build; Deploy Fly.io/Render + TestFlight/Play + Supabase Cloud + Baseten.

---

## 11. Milestones

M0 Repo & scaffolding — docs/STATE.md, ADRs, skeletons, docker-compose, CI passing
M1 Genesis & Charter — onboarding flow, Charter mock, approval, RLS
M2 Org design & Roles — approval cards, CRUD, Assistant, autonomy
M3 Comms — threads/messages Realtime citations
M4 Tasks & Approvals — board, inbox, linkage
M5 Agent Runtime — run loop 8-tool 2-min token audit
M6 Meetings → Execution Plan — turn-taking resolutions tasks timeline
M7 RAG ingestion & retrieval — PDF/DOCX/XLSX/image chunking hybrid RRF rerank citations
M8 Voice & Files — hold-to-talk Whisper mock attachments
M9 HR & Productivity — KPI snapshots Workforce Report propose_role_change Copilot
M10 Polish & Hardening — design system empty/loading/error/offline a11y perf security
M11 Ship — TestFlight Play prod Supabase Baseten monitoring docs

---

## 12. Definition of Done

- [ ] smoke passes LLM_MODE=mock
- [ ] flutter analyze 0
- [ ] flutter test green
- [ ] pytest green incl RAG eval
- [ ] ruff 0, mypy --strict 0
- [ ] RLS isolation
- [ ] token accounting/rate limiting
- [ ] RLS/indexes/company_id/audit all tables
- [ ] offline/empty/error states
- [ ] a11y pass
- [ ] docs/STATE.md + ADRs

---

## 13. Budget and Risk

$50/mo infra; risks LLM cost→budgets, RLS misconfig→tests, Realtime scale→DB, Flutter web vs native→native first

---

## Appendix A: Charter JSON

{"mission":"string","vision":"string","values":["string"],"okrs":[{"objective":"string","keyResults":["string"],"ownerRoleHint":"string","dueAt":"ISO"}],"constraints":{"budget":"string","headcount":"string","regulations":["string"]},"cadence":{"standupTime":"08:00","weeklyReportDay":"Friday","weeklyReportTime":"16:00"}}

## Appendix B: Resolutions

{"resolutions":[{"decision":"string","rationale":"string","ownerRoleId":"uuid","dueAt":"ISO","dependencies":["uuid"]}]}

## Appendix C: Tool allow-list

search_knowledge, create_task, update_task, post_message, request_approval, draft_document, schedule_meeting, read_kpis (all); build_budget/forecast_cashflow (Finance); draft_campaign/build_lead_list (Sales); assess_productivity/propose_role_change (HR)

*End of Master Prompt — source of truth.*


### 5.8 Motion and haptics

- Default spring: stiffness 300, damping 30 (`SpringDescription`). Durations 200–350 ms.
- Page transitions: platform default (Cupertino on iOS, predictive back on Android).
- Message appear: 8 pt rise + fade, 220 ms.
- Haptics: light impact on send, selection on segmented changes, success notification on approval decided, warning on reject.
- Respect `MediaQuery.disableAnimations`.

### 5.9 Navigation and screens

- Bottom glass tab bar, 5 tabs: **Home, Messages, Schedule, Approvals, Company**.
- Genesis — 5 calm steps, one question group per screen, progress as thin accent line; final step shows generated Charter as elegant read-only document with "Approve Charter".
- Home — greeting with date; "Today" card (top 3 priorities); Approvals waiting (count chip); latest reports from roles as cards; quick composer "Ask your company…".
- Messages — thread list (pinned: Assistant), AI/human badges, unread dots. Thread view: bubbles (outgoing accent, incoming bg.secondary, AI bubbles with faint ai.tint), report messages as rich cards with expandable sections and citation chips, voice messages with waveform, files as tiles. Streaming shows three-dot shimmer then token-by-token.
- Composer — glass pill: + (file/photo/camera), text field growing to 6 lines, mic becomes send when text exists. Hold mic to record with live waveform; slide left to cancel; release to send. Show "Transcribing…" then transcript editable before send.
- Schedule — week strip + agenda list; meetings, deadlines, cadences; "New meeting" sheet (agenda, participants picker with AI/human sections).
- Meeting room — agenda at top, turn-by-turn contributions, live "Resolutions" drawer, "Confirm resolutions" → Execution Plan timeline.
- Approvals — stack of cards; swipe right approve, left reject (with undo toast 5s), tap to open detail with reasoning/impact; "Ask for changes" opens reply.
- Company — Org Pulse graph, Charter, OKR progress rings, roles list, Workforce Report, "Assign human" flow (invite by email → Copilot).
- Role profile — mandate, KPIs with sparklines, current tasks, recent outputs, mode toggle, chat button.
- Settings — profile, notifications, appearance (system/light/dark), data export, sign out.

### 5.10 Copy tone

Short, warm, direct. Sentence case. Agents sign reports with role title. Errors say what happened and what to do: "Couldn't upload — check your connection and tap to retry."

---

## 6. Flutter Engineering Standards

- Flutter stable (latest), Dart 3, null safety, Material 3 + Cupertino adaptive.
- Architecture: feature-first clean architecture. `lib/app/(router,theme,di,bootstrap) core/(design_system,network,errors,utils,widgets) features/<feature>/{data,domain,presentation}`
- State: Riverpod 2 with code generation (`riverpod_annotation`); `AsyncNotifier` for async; no `setState` beyond local ephemeral.
- Routing: `go_router` with typed routes, auth redirect, deep links.
- Models: `freezed` + `json_serializable`; no dynamic in domain.
- Networking: `dio` with interceptors (auth refresh, retry on 5xx/timeout with backoff); SSE client for streaming.
- Realtime: `supabase_flutter` channels wrapped in repository; auto resubscribe.
- Offline: `drift` cache; optimistic send with pending/failed/retry.
- Audio: `record` (AAC 16kHz mono), `just_audio` playback, waveform from amplitude.
- Files: `file_picker`, `image_picker`; uploads chunked; max 25MB validated.
- Errors: sealed `Failure` types; repository returns `Result<T,Failure>`; global error boundary + Sentry optional.
- Design system: tokens in `core/design_system`; no raw hex.
- Accessibility: semantics labels, VoiceOver/TalkBack tested, dynamic type.
- Lints: `very_good_analysis`; zero warnings.
- Tests: unit for every notifier/repository; widget tests for every screen state; golden tests light/dark; one `integration_test` happy path.

## 7. Backend Engineering Standards

- Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2 async, Alembic vs Supabase migrations (record ADR).
- Layout: `app/{api,domain,services,agents,rag,llm,workers,db,core}`.
- `ruff` + `mypy --strict` clean; `pytest` ≥80% coverage on agents, rag, services.
- Prompts in `app/agents/prompts/*.md` versioned; never inline long prompts.
- Structured outputs validated by Pydantic schemas.
- Secrets only via env; `.env.example` complete.
- OpenAPI schema generated and Flutter client kept in sync (ADR).
- Structured JSON logs with `company_id`, `run_id`, `request_id`.

## 9. Parallel Workstreams

| Workstream | Owns | Depends on |
|---|---|---|
| WS-A Architecture & Contracts | ADRs, CONTRACTS.md, DB schema, RLS | — |
| WS-B Backend Core | Auth, companies, threads, messages, files, approvals APIs | WS-A |
| WS-C Agent Runtime & RAG | gateway, agents, ingestion, retrieval, evals, HR engine | WS-A |
| WS-D Design System | tokens, components, goldens | Section 5 only |
| WS-E App Features | screens and flows | WS-D, WS-A contracts |
| WS-F QA & Release | tests, CI, smoke, build configs | all |

- WS-A must freeze CONTRACTS.md v1 before B,C,E start.
- Use separate worktrees/branches for parallel writing if possible; otherwise interleave.
- App never blocks on backend: WS-E builds against FakeApi.

## 10. Repository Layout

```
foundryos/
  app/                 # Flutter
  backend/             # FastAPI + workers + evals
  supabase/            # migrations, seed, policies
  docs/                # MASTER_PROMPT, STATE, CONTRACTS, adr/
  .clinerules/
  scripts/             # bootstrap.sh, smoke.sh, seed_demo.py
  docker-compose.yml
  .github/workflows/   # ci.yml
```

## 11. Milestones

- M0 Foundation — repo, tooling, CI, docker compose, Supabase schema + RLS, design tokens, empty app shell with 5-tab bar, LLM_MODE=mock.
- M1 Identity & Genesis — auth, onboarding, Charter generation/approval, Founder's Assistant thread.
- M2 Messaging — threads, text, streaming replies, Realtime, offline cache, file upload + ingestion, voice record + transcription.
- M3 Org & Roles — role proposal approvals, role profiles, agent run loop, cadence reports, Org Pulse.
- M4 Meetings & Execution — schedule, meetings, resolutions, execution plan timeline, tasks board.
- M5 Approvals & HR — approvals inbox swipe, HR productivity engine, Workforce Report, role change proposals.
- M6 Humans in the loop — invite human, assign to role, Copilot mode, permissions, multi-user views.
- M7 Polish & Hardening — every empty/error/offline state, dark mode goldens, performance (60fps, cold start <2s), RAG evals, e2e green, demo seed.

## 12. Definition of Done

- `flutter analyze` 0; all Flutter tests and goldens pass; integration happy path passes on iOS + Android.
- `ruff`, `mypy --strict`, `pytest` clean; RAG eval recall@8 ≥0.85.
- App runs end-to-end with `LLM_MODE=mock` and with real Baseten keys.
- No crash, no unhandled exception, no raw error across all flows in 5.9.
- Every screen has loading, empty, error, offline states, light+dark.
- README lets new dev run everything in <15 min.
- `docs/STATE.md` shows all milestones complete with no open P0/P1.

## 13. Absolute Rules

- Never leave TODO, placeholder screens, dead buttons or fake data outside FakeApi/demo seed.
- Never call LLM from app or expose keys to client.
- Never let agent take gated action without approved approval record.
- Never bypass company_id scoping or RLS.
- Never mark step done with failing checks.
- Never invent facts in agent output; cite or say "I don't know yet".
- Never introduce dependency without one-line justification in `docs/STATE.md`.
- Always keep this document, STATE.md and CONTRACTS.md true to code.

*Begin now with M0. Write plan into docs/STATE.md, then execute cycle by cycle until DoD met.*
*End of Master Prompt — source of truth.*

- Security: JWT verified every request; RLS every table; prompt-injection defence.

## 8. Context Sharing

- `docs/MASTER_PROMPT.md` — source of truth.
- `docs/STATE.md` — current milestone, cycle plan, done list, next steps, known issues. Keep under 300 lines.
- `docs/adr/NNNN-title.md` — ADRs.
- `docs/CONTRACTS.md` — API endpoints, event names, Realtime channels, shared enums.
- `.clinerules/` — `01-standards.md`, `02-design.md`, `03-workflow.md`.
- When context >70%, use `new_task` with handoff pointing to `docs/STATE.md`.



