"""RAG eval — seeded demo company with 30 Q/A, recall@8 gate."""

from __future__ import annotations

# Placeholder for M7; M0 just ensures file exists and gate logic is testable
DEMO_QA_PAIRS = [
    {"question": f"Mock question {i}", "answer": f"Mock answer {i}", "chunk_id": f"c{i}"}
    for i in range(30)
]


def recall_at_k(retrieved: list[str], relevant: list[str], k: int = 8) -> float:
    if not relevant:
        return 1.0
    topk = set(retrieved[:k])
    hits = len(topk.intersection(set(relevant)))
    return hits / len(relevant)


def evaluate_mock() -> float:
    # In mock, retrieval returns perfect hits
    retrieved = [f"c{i}" for i in range(8)]
    relevant = ["c0", "c1"]
    return recall_at_k(retrieved, relevant, k=8)


def test_recall_gate() -> None:
    recall = evaluate_mock()
    assert recall >= 0.85, f"recall@8 {recall} < 0.85"
