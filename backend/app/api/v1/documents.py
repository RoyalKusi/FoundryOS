from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "documents"}

@router.post("/upload")
async def upload_document() -> dict[str, str]:
    return {"id": "doc-1", "status": "pending"}
