# ADR-004: Milestones M0–M7 (updated spec §11)

- Previously M0–M11 (detailed split: Foundation, Genesis, Org, Comms, Tasks, Agent Runtime, Meetings, RAG, Voice, HR, Polish, Ship). New spec §11 consolidates to M0–M7: Foundation, Identity & Genesis, Messaging, Org & Roles, Meetings & Execution, Approvals & HR, Humans in loop, Polish & Hardening.
- Rationale: Align with parallel workstreams (WS-A→F) and reduce milestone overhead; same deliverables, grouped.
- M0 still requires: repo, tooling, CI, docker compose, Supabase schema+RLS, design tokens, empty app shell with 5-tab bar, LLM_MODE=mock — now explicitly 5 tabs (Home/Messages/Schedule/Approvals/Company) per §5.9.
- Legacy M8-M11 merged into M5-M7; tracking updated in docs/STATE.md.
- No code impact, only tracking.
