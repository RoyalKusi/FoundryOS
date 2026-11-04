"""Genesis service placeholder."""

from __future__ import annotations

from app.schemas.charter import CharterSchema


async def create_company_and_charter(payload: dict) -> CharterSchema:  # type: ignore[no-untyped-def]
    return CharterSchema(
        mission="Mock mission",
        vision="Mock vision",
        values=["clarity"],
        okrs=[],
    )
