from __future__ import annotations
from typing import Any
from fastapi import APIRouter, Depends
from app.core.security import CurrentUser, get_current_user

router = APIRouter()

@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "approvals"}

@router.get("")
async def list_approvals(user: CurrentUser = Depends(get_current_user)) -> dict[str, Any]:
    return {"data": [{"id": "appr-1", "company_id": user.company_id, "status": "pending", "payload": {"tool": "send_email"}}], "meta": {"total": 1, "page": 1, "pageSize": 20, "totalPages": 1}}

@router.post("/{approval_id}/approve")
async def approve(approval_id: str, user: CurrentUser = Depends(get_current_user)) -> dict[str, str]:
    return {"id": approval_id, "status": "approved"}

@router.post("/{approval_id}/reject")
async def reject(approval_id: str, user: CurrentUser = Depends(get_current_user)) -> dict[str, str]:
    return {"id": approval_id, "status": "rejected"}

@router.get("/workforce")
async def workforce(user: CurrentUser = Depends(get_current_user)) -> dict[str, Any]:
    from app.services.hr_service import workforce_report
    return await workforce_report(user.company_id or "mock")
