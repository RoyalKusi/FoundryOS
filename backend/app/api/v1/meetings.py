from __future__ import annotations

from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "meetings"}


@router.post("")
async def create_meeting(payload: dict[str, Any]) -> dict[str, str]:
    return {"id": "meeting-1", "agenda": payload.get("agenda", "")}
