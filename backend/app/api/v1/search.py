from __future__ import annotations

from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "search"}


@router.get("")
async def search(q: str = "", company_id: str = "mock", top_k: int = 8) -> dict[str, Any]:
    from app.services.retrieval_service import reranked_search
    results = await reranked_search(q, company_id, top_k=top_k)
    return {"results": results, "query": q, "meta": {"total": len(results)}}
