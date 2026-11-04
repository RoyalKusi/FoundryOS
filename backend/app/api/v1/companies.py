from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.pagination import PaginationParams, PaginatedResponse, paginate
from app.core.security import get_current_user

router = APIRouter()


class CompanyOut(BaseModel):
    id: str
    name: str
    stage: str


@router.get("", response_model=PaginatedResponse[CompanyOut])
async def list_companies(p: PaginationParams = Depends(), user=Depends(get_current_user)) -> PaginatedResponse[CompanyOut]:
    # Stub: return mock company for current company_id
    data = [CompanyOut(id=user.company_id or "00000000-0000-0000-0000-000000000001", name="Demo Co", stage="idea")]
    meta = paginate(total=len(data), page=p.page, page_size=p.page_size)
    return PaginatedResponse[CompanyOut](data=data, meta=meta)


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "companies"}
