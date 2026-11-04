"""Genesis service — creates company + live charter via Baseten."""

from __future__ import annotations

import json
import uuid
from typing import Any

import structlog

from app.config import get_settings
from app.llm.gateway import get_gateway
from app.schemas.charter import CharterSchema
from app.services.charter_service import generate_charter

logger = structlog.get_logger(__name__)


async def create_company_and_charter(payload: dict[str, Any]) -> CharterSchema:
    """Create company charter via live LLM; payload includes companyName, pitch, industry."""
    settings = get_settings()
    logger.info("genesis_start", payload=payload, mode=settings.llm_mode, model=settings.baseten_reasoning_model)
    # Ensure company_id for token accounting
    payload = {**payload, "company_id": payload.get("company_id") or str(uuid.uuid4())}
    charter = await generate_charter(payload)
    logger.info("genesis_complete", mission=charter.mission, mode=settings.llm_mode)
    return charter


async def handle_genesis_chat(company_payload: dict[str, Any], company_id: str | None = None) -> dict[str, Any]:
    """Helper for genesis API — returns raw charter dict via gateway chat."""
    settings = get_settings()
    gateway = get_gateway()
    messages = [
        {"role": "system", "content": "You are FoundryOS Charter Architect. Output strict JSON."},
        {"role": "user", "content": f"Generate charter for: {json.dumps(company_payload)}"},
    ]
    schema = CharterSchema.model_json_schema()
    result = await gateway.chat(messages=messages, model=settings.baseten_reasoning_model, json_schema=schema, company_id=company_id)
    return json.loads(result["content"])
