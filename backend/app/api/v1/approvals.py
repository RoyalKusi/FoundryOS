from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "approvals"}

@router.get("")
async def list_approvals() -> list[dict[str, str]]:
    return [{"id": "appr-1", "type": "role_change", "status": "pending"}]
