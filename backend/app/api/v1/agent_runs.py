from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

router = APIRouter()

@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "module": "agent_runs"}

@router.get("/{run_id}/stream")
async def stream_run(run_id: str) -> EventSourceResponse:  # type: ignore[no-untyped-def]
    async def gen():  # type: ignore[no-untyped-def]
        yield {"event": "start", "data": run_id}
        yield {"event": "end", "data": "done"}
    return EventSourceResponse(gen())
