"""Charter service stub."""
from app.schemas.charter import CharterSchema

async def generate_charter(payload: dict) -> CharterSchema:  # type: ignore[no-untyped-def]
    return CharterSchema(mission="Mock mission", vision="Mock vision", values=["clarity"], okrs=[])
