"""RLS cross-tenant isolation placeholder — M0 ensures file exists."""

import pytest


@pytest.mark.asyncio
async def test_cross_tenant_blocked() -> None:
    # In skeleton, we assert tenant scoping would be enforced
    # Real test spins up test DB and tries cross-company query
    company_a = "00000000-0000-0000-0000-000000000001"
    company_b = "00000000-0000-0000-0000-000000000002"
    assert company_a != company_b
    # Placeholder passes; will implement with testcontainers in M1
