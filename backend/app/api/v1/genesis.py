from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.security import CurrentUser, get_current_user

router = APIRouter()


class GenesisRequest(BaseModel):
    companyName: str
    pitch: str | None = None
    description: str | None = None
    industry: str | None = None
    stage: str = "idea"
    timezone: str = "UTC"
    mission: str | None = None
    vision: str | None = None
    objectives: list[str] | None = None


class GenesisResponse(BaseModel):
    companyId: str
    charterDraft: dict[str, Any]


@router.post("", response_model=GenesisResponse)
async def create_genesis(payload: GenesisRequest, user: CurrentUser = Depends(get_current_user)) -> GenesisResponse:
    from app.llm.gateway import get_gateway

    gateway = get_gateway()
    # Mock charter generation via gateway
    result = await gateway.chat(
        messages=[{"role": "user", "content": f"Create charter for {payload.companyName}: {payload.description}"}],
        json_schema={"type": "object", "properties": {"mission": {"type": "string"}}},
        company_id=user.company_id,
    )
    import json

    try:
        charter = json.loads(result["content"])
    except Exception:
        charter = {"mission": payload.mission or "Mock mission", "raw": result["content"]}
    return GenesisResponse(companyId=user.company_id or "mock-company", charterDraft=charter)


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "genesis"}
