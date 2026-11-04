from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "threads"}

@router.get("")
async def list_threads() -> list[dict[str, str]]:
    return [{"id": "thread-1", "title": "General"}]

@router.post("")
async def create_thread(payload: dict) -> dict[str, str]:  # type: ignore[no-untyped-def]
    return {"id": "new-thread", "title": payload.get("title", "Untitled")}
