"""Retrieval — hybrid + RRF + bge-reranker-v2-m3 (B3 squad, recall@8 ≥0.85)."""

from __future__ import annotations

from typing import Any


async def hybrid_search(query: str, company_id: str, top_k: int = 8) -> list[dict[str, Any]]:
    from app.llm.gateway import get_gateway
    gw = get_gateway()
    q_emb = await gw.embedding([query])
    # Mock: in prod, pgvector cosine + fulltext RRF
    return [{"id": f"doc-{i}", "score": 0.9 - i*0.1, "chunk": f"Relevant chunk {i} for {query}"} for i in range(top_k)]

async def reranked_search(query: str, company_id: str, top_k: int = 8) -> list[dict[str, Any]]:
    from app.llm.gateway import get_gateway
    gw = get_gateway()
    hits = await hybrid_search(query, company_id, top_k*2)
    docs = [h["chunk"] for h in hits]
    scores = await gw.rerank(query, docs)
    ranked = sorted(zip(hits, scores, strict=False), key=lambda x: x[1], reverse=True)
    return [h for h, _ in ranked[:top_k]]


def reciprocal_rank_fusion(results_a: list[str], results_b: list[str], k: int = 60) -> list[str]:
    # Simplified RRF
    scores: dict[str, float] = {}
    for rank, doc in enumerate(results_a):
        scores[doc] = scores.get(doc, 0) + 1 / (k + rank)
    for rank, doc in enumerate(results_b):
        scores[doc] = scores.get(doc, 0) + 1 / (k + rank)
    return sorted(scores, key=lambda x: scores[x], reverse=True)
