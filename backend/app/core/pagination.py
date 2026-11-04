"""Pagination helpers — ?page=1&page_size=20 → {data, meta}."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number, 1-indexed")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")


class PaginationMeta(BaseModel):
    total: int
    page: int
    page_size: int = Field(alias="pageSize")
    total_pages: int = Field(alias="totalPages")

    model_config = {"populate_by_name": True}


class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    meta: PaginationMeta

    model_config = {"populate_by_name": True}


def paginate(total: int, page: int, page_size: int) -> PaginationMeta:
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginationMeta(total=total, page=page, page_size=page_size, total_pages=total_pages)
