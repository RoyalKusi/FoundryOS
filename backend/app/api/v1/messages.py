from __future__ import annotations

from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "messages"}


@router.post("")
async def post_message(payload: dict[str, Any]) -> dict[str, str]:
    return {"id": "msg-1", "body": payload.get("body", "")}


@router.get("")
async def list_messages() -> list[dict[str, str]]:
    return [{"id": "msg-1", "body": "Hello"}]
