"""Genesis service placeholder."""

from __future__ import annotations

from typing import Any

from app.schemas.charter import CharterSchema


async def create_company_and_charter(payload: dict[str, Any]) -> CharterSchema:
    return CharterSchema(
        mission="Mock mission",
        vision="Mock vision",
        values=["clarity"],
        okrs=[],
    )
