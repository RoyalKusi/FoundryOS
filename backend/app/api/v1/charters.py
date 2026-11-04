from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "charters"}


@router.post("/{company_id}/approve")
async def approve_charter(company_id: str) -> dict[str, str]:
    return {"company_id": company_id, "status": "approved"}
