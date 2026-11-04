"""Retrieval service — hybrid + RRF + rerank placeholder."""

from __future__ import annotations


async def hybrid_search(query: str, company_id: str, top_k: int = 8) -> list[dict]:  # type: ignore[no-untyped-def]
    return []


def reciprocal_rank_fusion(results_a: list[str], results_b: list[str], k: int = 60) -> list[str]:  # type: ignore[no-untyped-def]
    # Simplified RRF
    scores: dict[str, float] = {}
    for rank, doc in enumerate(results_a):
        scores[doc] = scores.get(doc, 0) + 1 / (k + rank)
    for rank, doc in enumerate(results_b):
        scores[doc] = scores.get(doc, 0) + 1 / (k + rank)
    return sorted(scores, key=lambda x: scores[x], reverse=True)
