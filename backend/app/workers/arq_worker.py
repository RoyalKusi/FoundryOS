"""arq worker settings."""

from app.config import get_settings

async def ingest_document(ctx: dict, document_id: str) -> dict[str, str]:  # type: ignore[no-untyped-def]
    return {"document_id": document_id, "status": "done"}

async def agent_run(ctx: dict, role_id: str, trigger: str) -> dict[str, str]:  # type: ignore[no-untyped-def]
    from app.agents.runtime import run_agent, RunContext
    return await run_agent(RunContext(role_id=role_id, company_id="mock-company", trigger=trigger))

async def cadence_tick(ctx: dict) -> dict[str, str]:  # type: ignore[no-untyped-def]
    return {"status": "ok"}

async def transcription(ctx: dict, audio_path: str) -> dict[str, str]:  # type: ignore[no-untyped-def]
    return {"text": "mock transcription"}

class WorkerSettings:
    redis_settings = get_settings().redis_url  # type: ignore[assignment]
    functions = [ingest_document, agent_run, cadence_tick, transcription]
    job_timeout = 120
