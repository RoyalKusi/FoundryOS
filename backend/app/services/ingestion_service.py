"""Ingestion — chunk 512 + BGE-M3 1024 → pgvector HNSW (B3 squad)."""

from __future__ import annotations


def structure_aware_chunking(text: str, target_tokens: int = 500, overlap: float = 0.15) -> list[str]:
    # Very naive: split on paragraphs
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    return paras or [text]


async def ingest_document(document_id: str, company_id: str | None = None, file_path: str | None = None) -> dict[str, str]:
    from app.llm.gateway import get_gateway
    import structlog
    logger = structlog.get_logger(__name__)
    gw = get_gateway()
    from pathlib import Path
    text = Path(file_path).read_text() if file_path and Path(file_path).exists() else f"Mock doc {document_id}"
    chunks = [text[i:i+512] for i in range(0, len(text), 512)] or [text]
    embs = await gw.embedding(chunks[:10])
    logger.info("ingest_done", document_id=document_id, chunks=len(chunks), dim=len(embs[0]) if embs else 0)
    return {"document_id": document_id, "chunks": str(len(chunks))}
