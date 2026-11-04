# FoundryOS — CONTRACTS v1 (WS-A frozen)

> Source of truth for API + Realtime + shared enums. Changes require ADR and same-cycle backend+app update.

## API Base

- Prefix: `/api/v1`
- Auth: `Authorization: Bearer <Supabase JWT>`; JWT contains `company_id` claim after Genesis
- Headers: `X-Company-Id` allowed in `LLM_MODE=mock` for tests
- Pagination: `?page=1&page_size=20` → `{data: [], meta: {total, page, pageSize, totalPages}}`
- Errors: `{error: {code, message, details}}`
- Wire casing: JSON camelCase via `alias_generator`; internal snake_case
- Streaming: SSE at `/api/v1/agent_runs/{id}/stream`

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | /genesis | Create company + generate charter draft (mock LLM) |
| GET | /companies | List companies (scoped) |
| GET | /charters/{company_id} | Get charter |
| POST | /charters/{company_id}/approve | Approve charter |
| GET/POST | /roles | List/create roles |
| GET/POST | /threads | List/create threads (direct/group/channel/meeting) |
| GET/POST | /messages | List/post messages (text/voice/file/report/approval/system) |
| GET | /tasks | List tasks |
| POST | /meetings | Create meeting |
| GET | /approvals | List approvals |
| POST | /documents/upload | Upload file → enqueue ingest |
| GET | /search?q= | Hybrid search + RRF + rerank |
| GET | /agent_runs/{id}/stream | SSE stream |
| GET | /health | Health check `{status, env, llm_mode}` |

## Enums

- `stage`: idea | pre-revenue | revenue | scaling
- `member.kind`: human | ai
- `role.autonomy`: autonomous | copilot
- `role.status`: proposed | active | paused | retired
- `thread.type`: direct | group | channel | meeting
- `message.kind`: text | voice | file | report | approval | system
- `task.status`: todo | doing | done | blocked
- `task.priority`: low | medium | high | urgent
- `approval.status`: pending | approved | rejected | changes_requested
- `document.status`: pending | ready | failed
- `agent_run.status`: pending | running | completed | failed | timeout

## Realtime Channels (Supabase)

- `messages` filtered by `company_id`
- `tasks` filtered by `company_id`
- `approvals` filtered by `company_id`
- `agent_runs` filtered by `role_id`

Payload: Postgres `INSERT`/`UPDATE` via Supabase Realtime; workers write, app subscribes via `supabase_flutter` channels wrapped in repository with auto-resubscribe.

## Shared Schemas

- Charter JSON: `{mission, vision, values[], okrs[{objective, keyResults[], ownerRoleHint, dueAt}], constraints{budget,headcount,regulations[]}, cadence{standupTime, weeklyReportDay, weeklyReportTime}}`
- Resolutions: `{resolutions: [{decision, rationale, ownerRoleId, dueAt, dependencies[]}]}`

## Events

- `ingest_document` (arq job: document_id)
- `agent_run` (arq job: role_id, trigger)
- `cadence_tick` (scheduled 08:00 / Fri 16:00 local)
- `transcription` (audio_path → text)

## Tools — All Digital Work via Allow-Listed Tools

Agents execute **any digital work** (email draft/send, posting, adverts, arranging meetings, finances, auditing, sending docs/receipts, etc.) **only through company-provided tools** via `backend/app/agents/tools/registry.py` Tool Gateway.

- Allow-list per role (`TOOL_ALLOW_LIST`): `search_knowledge`, `create_task`, `update_task`, `post_message`, `request_approval`, `draft_document`, `schedule_meeting`, `read_kpis`, `read_calendar` (all); `draft_email`/`send_email`, `draft_post`/`publish_post`, `send_message_external`, `generate_document`/`send_document`, `create_calendar_event`/`invite_attendees`/`arrange_meeting`, `draft_advert`, `draft_campaign`/`publish_campaign`/`publish_advert`/`build_lead_list` (Sales & Marketing), `build_budget`/`forecast_cashflow`/`create_invoice`/`send_invoice`/`create_receipt`/`send_receipt`/`run_audit`/`record_transaction` (Finance), `assess_productivity`/`propose_role_change`/`audit_workload` (HR/Ops), plus extensible `call_company_tool` for any company integration (Slack, Notion, HubSpot, Stripe, SendGrid, etc. registered in `company_tools` table).
- **Gated tools (always require approval record before execution, §3.4):** `send_email`, `publish_post`, `send_message_external`, `send_document`, `invite_attendees`, `publish_campaign`, `publish_advert`, `send_invoice`, `send_receipt`, `record_transaction`, `call_company_tool` if external/spend/delete. Gateway returns `approval_required` if missing approval.
- Drafting is free (internal), **sending/publishing/inviting/spend is gated** — agent must call `request_approval` and wait.
- All tool calls are `company_id` scoped, audit logged, rate-limited via token bucket, and validated against allow-list at runtime. Company can expose any external API as a tool via env (e.g., `SENDGRID_API_KEY`, `STRIPE_KEY`, `SLACK_BOT_TOKEN`) — registered dynamically and enforced same gates.

## FakeApi Flag

- `APP_USE_FAKE_API=true` → app uses `FakeApi` implementing same contract; no network needed for WS-E UI development.
