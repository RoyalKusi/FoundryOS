-- FoundryOS initial schema — 14 tables + pgvector + RLS
create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";
create extension if not exists "vector";
create extension if not exists "pg_trgm";

create or replace function set_updated_at() returns trigger as $$
begin new.updated_at = now(); return new; end; $$ language plpgsql;

create table companies (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  stage text not null default 'idea',
  timezone text not null default 'UTC',
  charter_version_id uuid,
  pitch text, description text, industry text, location text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create trigger trg_companies_updated_at before update on companies for each row execute function set_updated_at();
alter table companies enable row level security;
create policy "tenant_isolation_companies" on companies for all using (true) with check (true);

create table charters (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  version int not null default 1,
  json jsonb not null default '{}'::jsonb,
  approved_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index idx_charters_company_id on charters(company_id);
alter table charters enable row level security;
create policy "tenant_isolation_charters" on charters for all using (true) with check (true);

create table members (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  kind text not null check (kind in ('human','ai')),
  user_id text, role_id uuid, display_name text not null, avatar text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index idx_members_company_id on members(company_id);
alter table members enable row level security;
create policy "tenant_isolation_members" on members for all using (true) with check (true);

create table roles (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  title text not null, mandate text, kpis jsonb,
  autonomy text not null default 'autonomous' check (autonomy in ('autonomous','copilot')),
  status text not null default 'proposed' check (status in ('proposed','active','paused','retired')),
  human_member_id uuid references members(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index idx_roles_company_id on roles(company_id);

create table threads (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  type text not null default 'direct', title text,
  created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create index idx_threads_company_id on threads(company_id);
alter table threads enable row level security;
create policy "tenant_isolation_threads" on threads for all using (true) with check (true);

create table thread_participants (
  thread_id uuid not null references threads(id) on delete cascade,
  member_id uuid not null references members(id) on delete cascade,
  created_at timestamptz not null default now(), updated_at timestamptz not null default now(),
  primary key (thread_id, member_id)
);
alter table thread_participants enable row level security;
create policy "tenant_isolation_thread_participants" on thread_participants for all using (true) with check (true);

create table messages (
  id uuid primary key default gen_random_uuid(),
  thread_id uuid not null references threads(id) on delete cascade,
  author_member_id uuid references members(id) on delete set null,
  kind text not null default 'text', body text, attachments jsonb, citations jsonb,
  created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create index idx_messages_thread_id on messages(thread_id);
alter table messages enable row level security;
create policy "tenant_isolation_messages" on messages for all using (true) with check (true);

create table meetings (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  thread_id uuid references threads(id) on delete set null,
  agenda text, participants jsonb, status text not null default 'scheduled', resolutions jsonb,
  created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create index idx_meetings_company_id on meetings(company_id);
alter table meetings enable row level security;
create policy "tenant_isolation_meetings" on meetings for all using (true) with check (true);

create table approvals (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  type text not null, payload jsonb, requested_by uuid,
  approver_member_id uuid references members(id) on delete set null,
  status text not null default 'pending', decided_at timestamptz, rationale text,
  created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create index idx_approvals_company_id on approvals(company_id);
alter table approvals enable row level security;
create policy "tenant_isolation_approvals" on approvals for all using (true) with check (true);

create table documents (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  title text not null, storage_path text, mime_type text,
  scope text not null default 'company', status text not null default 'pending', metadata jsonb,
  created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create index idx_documents_company_id on documents(company_id);
alter table documents enable row level security;
create policy "tenant_isolation_documents" on documents for all using (true) with check (true);


create table agent_runs (
  id uuid primary key default gen_random_uuid(),
  role_id uuid not null references roles(id) on delete cascade,
  trigger text not null, status text not null default 'pending', steps jsonb, tokens int, cost float, error text,
  created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create index idx_agent_runs_role_id on agent_runs(role_id);
alter table agent_runs enable row level security;
create policy "tenant_isolation_agent_runs" on agent_runs for all using (true) with check (true);

create table kpi_snapshots (
  id uuid primary key default gen_random_uuid(),
  role_id uuid not null references roles(id) on delete cascade,
  period text not null, metrics jsonb, score float,
  created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create index idx_kpi_snapshots_role_id on kpi_snapshots(role_id);
alter table kpi_snapshots enable row level security;
create policy "tenant_isolation_kpi_snapshots" on kpi_snapshots for all using (true) with check (true);

create table audit_log (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  actor_member_id uuid, action text not null, target_type text, target_id uuid, payload_hash text, payload jsonb,
  created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create index idx_audit_log_company_id on audit_log(company_id);
alter table audit_log enable row level security;
create policy "tenant_isolation_audit_log" on audit_log for all using (true) with check (true);

create table chunks (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  document_id uuid references documents(id) on delete cascade,
  scope text not null default 'company', text text not null,
  embedding vector(1024), tsv tsvector, metadata jsonb,
  created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create index idx_chunks_company_id on chunks(company_id);
create index idx_chunks_embedding on chunks using ivfflat (embedding vector_cosine_ops) with (lists=100);
create index idx_chunks_tsv on chunks using gin(tsv);
alter table chunks enable row level security;
create policy "tenant_isolation_chunks" on chunks for all using (true) with check (true);


create table tasks (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id) on delete cascade,
  owner_role_id uuid references roles(id) on delete set null,
  title text not null, detail text, okr_ref text,
  status text not null default 'todo', priority text not null default 'medium',
  due_at timestamptz, depends_on uuid[], source text not null default 'human',
  created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create index idx_tasks_company_id on tasks(company_id);
alter table tasks enable row level security;
create policy "tenant_isolation_tasks" on tasks for all using (true) with check (true);

alter table roles enable row level security;
create policy "tenant_isolation_roles" on roles for all using (true) with check (true);
