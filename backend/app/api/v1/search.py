from __future__ import annotations

from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "search"}


@router.get("")
async def search(q: str = "") -> dict[str, Any]:
    return {"results": [], "query": q}
