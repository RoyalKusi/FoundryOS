"""Auth deps — Supabase JWT verification stub with company scoping."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header, HTTPException

from app.config import get_settings


class CurrentUser:
    """Minimal user extracted from Supabase JWT (or header in local/mock)."""

    def __init__(self, user_id: str, company_id: str | None, email: str | None = None) -> None:
        self.user_id = user_id
        self.company_id = company_id
        self.email = email


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    x_company_id: Annotated[str | None, Header()] = None,
) -> CurrentUser:
    """Verify Supabase JWT; in mock/local allow X-Company-Id header for testing."""
    settings = get_settings()

    # In mock mode or when no auth header, allow header-based scoping for tests/smoke
    if settings.llm_mode == "mock" or authorization is None:
        # For smoke/tests, accept X-Company-Id or default test company
        company_id = x_company_id or "00000000-0000-0000-0000-000000000001"
        user_id = "test-user-id"
        if authorization and authorization.startswith("Bearer "):
            # Real path would verify JWT via supabase-py / jose
            pass
        return CurrentUser(user_id=user_id, company_id=company_id)

    # Live path — verify JWT (simplified stub; real impl uses jose + JWKS)
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization")
    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=401, detail="Empty token")
    # TODO: verify with Supabase JWKS, extract user_id & company_id claim
    # For now, decode without verify in scaffold
    return CurrentUser(user_id="jwt-user", company_id=x_company_id)


def require_company_id(user: CurrentUser) -> str:
    if not user.company_id:
        raise HTTPException(status_code=400, detail="Company context required")
    return user.company_id


CompanyId = Annotated[str, Depends(lambda: require_company_id(Depends(get_current_user)))]  # type: ignore

