from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "tasks"}

@router.get("")
async def list_tasks() -> list[dict[str, str]]:
    return [{"id": "task-1", "title": "Mock task", "status": "todo"}]
