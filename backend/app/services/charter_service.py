"""Charter service stub."""

from __future__ import annotations

from typing import Any

from app.schemas.charter import CharterSchema


async def generate_charter(payload: dict[str, Any]) -> CharterSchema:
    return CharterSchema(mission="Mock mission", vision="Mock vision", values=["clarity"], okrs=[])
