from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.security import CurrentUser, get_current_user

router = APIRouter()


class RoleCreate(BaseModel):
    title: str
    mandate: str | None = None


class RoleOut(BaseModel):
    id: str
    title: str
    status: str


@router.get("", response_model=list[RoleOut])
async def list_roles(user: CurrentUser = Depends(get_current_user)) -> list[RoleOut]:
    return [RoleOut(id="00000000-0000-0000-0000-000000000002", title="Finance Officer", status="proposed")]


@router.post("", response_model=RoleOut)
async def create_role(payload: RoleCreate, user: CurrentUser = Depends(get_current_user)) -> RoleOut:
    return RoleOut(id="new-role-id", title=payload.title, status="proposed")


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "roles"}
