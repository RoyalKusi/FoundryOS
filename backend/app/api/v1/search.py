from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "search"}

@router.get("")
async def search(q: str = "") -> dict[str, list]:
    return {"results": [], "query": q}
