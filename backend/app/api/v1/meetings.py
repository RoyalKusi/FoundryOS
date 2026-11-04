from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "meetings"}

@router.post("")
async def create_meeting(payload: dict) -> dict[str, str]:  # type: ignore[no-untyped-def]
    return {"id": "meeting-1", "agenda": payload.get("agenda", "")}
