from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query
from app.core.security import CurrentUser, get_current_user
from app.core.pagination import paginate

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "threads"}


@router.get("")
async def list_threads(
    user: CurrentUser = Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> dict:
    # company_id scoped — A2 agent (skeleton returns empty, real DB in ws-b)
    data: list[dict[str, str]] = []
    return paginate(data, total=0, page=page, page_size=page_size)


@router.post("")
async def create_thread(payload: dict[str, Any], user: CurrentUser = Depends(get_current_user)) -> dict[str, str]:
    return {"id": "new-thread", "company_id": user.company_id or "00000000-0000-0000-0000-000000000001", "title": payload.get("title", "Untitled")}
