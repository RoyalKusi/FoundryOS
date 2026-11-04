from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "documents"}

@router.post("/upload")
async def upload_document(company_id: str = "mock") -> dict[str, str]:
    return {"id": "doc-1", "company_id": company_id, "status": "pending"}
