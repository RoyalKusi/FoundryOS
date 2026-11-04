"""arq worker settings."""

from __future__ import annotations

from typing import Any

from app.config import get_settings


async def ingest_document(ctx: dict[str, Any], document_id: str) -> dict[str, str]:
    return {"document_id": document_id, "status": "done"}


async def agent_run(ctx: dict[str, Any], role_id: str, trigger: str) -> dict[str, str]:
    from app.agents.runtime import run_agent, RunContext

    return await run_agent(RunContext(role_id=role_id, company_id="mock-company", trigger=trigger))


async def cadence_tick(ctx: dict[str, Any]) -> dict[str, str]:
    return {"status": "ok"}


async def transcription(ctx: dict[str, Any], audio_path: str) -> dict[str, str]:
    return {"text": "mock transcription"}

class WorkerSettings:
    redis_settings = get_settings().redis_url
    functions = [ingest_document, agent_run, cadence_tick, transcription]
    job_timeout = 120
