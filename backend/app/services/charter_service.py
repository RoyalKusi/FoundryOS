"""Charter service — live Baseten via gateway, fallback mock for tests."""

from __future__ import annotations

import json
import structlog
from pathlib import Path
from typing import Any

from app.config import get_settings
from app.llm.gateway import get_gateway
from app.schemas.charter import CharterSchema

logger = structlog.get_logger(__name__)


def _load_charter_prompt() -> str:
    prompt_path = Path(__file__).parent.parent / "agents" / "prompts" / "charter.md"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    return "You are FoundryOS Charter Architect. Generate Charter JSON per schema."


async def generate_charter(payload: dict[str, Any]) -> CharterSchema:
    """Generate charter via Baseten Maverick; mock mode returns deterministic stub."""
    settings = get_settings()
    gateway = get_gateway()

    system_prompt = _load_charter_prompt()
    user_content = f"Company payload: {json.dumps(payload)}\n\nGenerate Charter JSON with mission, vision, values, okrs, constraints, cadence."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]

    # Use structured output via json_schema
    schema = CharterSchema.model_json_schema()

    try:
        result = await gateway.chat(
            messages=messages,
            model=settings.baseten_reasoning_model,
            temperature=0.7,
            json_schema=schema,
            company_id=payload.get("company_id"),
        )
        content = result["content"]
        logger.info("charter_generated", mode=settings.llm_mode, model=settings.baseten_reasoning_model, tokens=result.get("usage"))
        # Handle markdown-wrapped JSON or extra text
        if "```" in content:
            import re
            m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.DOTALL)
            if m:
                content = m.group(1)
        data = json.loads(content)
        # Normalize Muse Spark quirks: values as [{name, description}] -> ["name: description"]
        if isinstance(data.get("values"), list):
            norm_values = []
            for v in data["values"]:
                if isinstance(v, dict):
                    name = v.get("name", "")
                    desc = v.get("description", "")
                    norm_values.append(f"{name}: {desc}" if desc else name)
                elif isinstance(v, str):
                    norm_values.append(v)
            data["values"] = norm_values
        # Normalize okrs: owner -> ownerRoleHint
        if isinstance(data.get("okrs"), list):
            for okr in data["okrs"]:
                if isinstance(okr, dict) and "owner" in okr and "ownerRoleHint" not in okr:
                    okr["ownerRoleHint"] = okr.pop("owner")
        # Normalize constraints: list -> Constraints object
        if isinstance(data.get("constraints"), list):
            data["constraints"] = {"regulations": data["constraints"]}
        elif isinstance(data.get("constraints"), dict):
            # Ensure correct field names
            pass
        # Normalize cadence: ignore unknown fields, keep defaults
        if isinstance(data.get("cadence"), dict):
            # Muse returns okr_cycle, check_in etc — map to our schema or drop
            allowed = {"standupTime", "weeklyReportDay", "weeklyReportTime"}
            data["cadence"] = {k: v for k, v in data["cadence"].items() if k in allowed} or None
            if data["cadence"] == {}:
                data["cadence"] = None
        return CharterSchema.model_validate(data)
    except Exception as e:
        logger.warning("charter_generation_failed_fallback_mock", error=str(e), mode=settings.llm_mode)
        # Graceful fallback: if live fails after retries, return mock but log
        if settings.llm_mode == "live":
            logger.error("charter_live_failed_returning_fallback", error=str(e))
            # Still return mock to keep app working, but signal via values
            return CharterSchema(
                mission="Empower founders with an autonomous OS (fallback)",
                vision="Every startup runs like a Fortune 500 from day one",
                values=["clarity", "ownership", "velocity"],
                okrs=[{"objective": "Launch MVP", "keyResults": ["Ship core flows", "Onboard 10 pilots"], "ownerRoleHint": "Operations Officer"}],
            )
        return CharterSchema(mission="Mock mission", vision="Mock vision", values=["clarity"], okrs=[])
