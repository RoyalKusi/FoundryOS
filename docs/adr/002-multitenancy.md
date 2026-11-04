# ADR-002: Multi-tenancy via company_id + RLS

Every table carries `company_id`. Every query is scoped by `company_id` from JWT claim (`X-Company-Id` header in mock). RLS policies on every table enforce isolation; app also checks. Tests prove cross-tenant failure.

Supabase JWT contains `company_id` after Genesis. File access via signed URLs scoped to company. Audit log records every agent action.

Tradeoff: app-level scoping is primary; RLS is defense-in-depth. Migration 00001 creates permissive policies (`using (true)`) for skeleton — will tighten to `auth.jwt() ->> 'company_id'` in M1.
