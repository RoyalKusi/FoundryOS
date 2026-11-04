-- Production RLS tightening — replaces permissive using(true) with JWT company_id check
-- A1 squad: Make app defense-in-depth, app scoping is primary
-- JWT contains company_id claim after Genesis (Supabase Auth)

-- Helper: extract company_id from JWT (supabase auth.jwt())
create or replace function current_company_id() returns uuid as $$
  select coalesce(nullif((auth.jwt() ->> 'company_id'), ''), auth.jwt() -> 'app_metadata' ->> 'company_id')::uuid;
$$ language sql stable;

-- Companies: member must belong
drop policy if exists "tenant_isolation_companies" on companies;
create policy "tenant_isolation_companies" on companies for all using (id = current_company_id()) with check (id = current_company_id());

-- Charters
drop policy if exists "tenant_isolation_charters" on charters;
create policy "tenant_isolation_charters" on charters for all using (company_id = current_company_id()) with check (company_id = current_company_id());

-- Members
drop policy if exists "tenant_isolation_members" on members;
create policy "tenant_isolation_members" on members for all using (company_id = current_company_id()) with check (company_id = current_company_id());

-- Roles
drop policy if exists "tenant_isolation_roles" on roles;
create policy "tenant_isolation_roles" on roles for all using (company_id = current_company_id()) with check (company_id = current_company_id());

-- Threads
drop policy if exists "tenant_isolation_threads" on threads;
create policy "tenant_isolation_threads" on threads for all using (company_id = current_company_id()) with check (company_id = current_company_id());

-- Documents
drop policy if exists "tenant_isolation_documents" on documents;
create policy "tenant_isolation_documents" on documents for all using (company_id = current_company_id()) with check (company_id = current_company_id());

-- Chunks
drop policy if exists "tenant_isolation_chunks" on chunks;
create policy "tenant_isolation_chunks" on chunks for all using (company_id = current_company_id()) with check (company_id = current_company_id());

-- Tasks
drop policy if exists "tenant_isolation_tasks" on tasks;
create policy "tenant_isolation_tasks" on tasks for all using (company_id = current_company_id()) with check (company_id = current_company_id());

-- Messages
drop policy if exists "tenant_isolation_messages" on messages;
create policy "tenant_isolation_messages" on messages for all using (company_id = current_company_id()) with check (company_id = current_company_id());

-- Approvals
drop policy if exists "tenant_isolation_approvals" on approvals;
create policy "tenant_isolation_approvals" on approvals for all using (company_id = current_company_id()) with check (company_id = current_company_id());

-- Agent runs — via role->company
drop policy if exists "tenant_isolation_agent_runs" on agent_runs;
create policy "tenant_isolation_agent_runs" on agent_runs for all using (exists (select 1 from roles r where r.id = agent_runs.role_id and r.company_id = current_company_id()));

-- KPI snapshots — via role
drop policy if exists "tenant_isolation_kpi_snapshots" on kpi_snapshots;
create policy "tenant_isolation_kpi_snapshots" on kpi_snapshots for all using (exists (select 1 from roles r where r.id = kpi_snapshots.role_id and r.company_id = current_company_id()));

-- Audit log
drop policy if exists "tenant_isolation_audit_log" on audit_log;
create policy "tenant_isolation_audit_log" on audit_log for all using (company_id = current_company_id()) with check (company_id = current_company_id());

-- Service role bypass for workers (supabase_service_key)
create policy "service_role_all" on companies for all using (auth.role() = 'service_role');
create policy "service_role_all_charters" on charters for all using (auth.role() = 'service_role');
create policy "service_role_all_members" on members for all using (auth.role() = 'service_role');
create policy "service_role_all_roles" on roles for all using (auth.role() = 'service_role');
create policy "service_role_all_threads" on threads for all using (auth.role() = 'service_role');
create policy "service_role_all_messages" on messages for all using (auth.role() = 'service_role');
create policy "service_role_all_tasks" on tasks for all using (auth.role() = 'service_role');
create policy "service_role_all_documents" on documents for all using (auth.role() = 'service_role');
create policy "service_role_all_chunks" on chunks for all using (auth.role() = 'service_role');
create policy "service_role_all_approvals" on approvals for all using (auth.role() = 'service_role');
