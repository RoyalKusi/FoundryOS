"""Ingestion pipeline placeholder."""

from __future__ import annotations


def structure_aware_chunking(text: str, target_tokens: int = 500, overlap: float = 0.15) -> list[str]:
    # Very naive: split on paragraphs
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    return paras or [text]


async def ingest_document(document_id: str) -> dict[str, str]:  # type: ignore[no-untyped-def]
    return {"document_id": document_id, "chunks": "0"}
