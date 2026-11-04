from __future__ import annotations

from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "threads"}


@router.get("")
async def list_threads() -> list[dict[str, str]]:
    return [{"id": "thread-1", "title": "General"}]


@router.post("")
async def create_thread(payload: dict[str, Any]) -> dict[str, str]:
    return {"id": "new-thread", "title": payload.get("title", "Untitled")}
