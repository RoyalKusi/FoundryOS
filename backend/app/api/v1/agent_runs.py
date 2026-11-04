from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

from fastapi import APIRouter

try:
    from sse_starlette.sse import EventSourceResponse
except ImportError:  # pragma: no cover
    EventSourceResponse = object  # type: ignore[misc, assignment]

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "agent_runs"}


@router.get("/{run_id}/stream")
async def stream_run(run_id: str) -> EventSourceResponse:
    async def gen() -> AsyncGenerator[dict[str, Any], None]:
        yield {"event": "start", "data": run_id}
        yield {"event": "end", "data": "done"}

    return EventSourceResponse(gen())  # type: ignore[operator]
