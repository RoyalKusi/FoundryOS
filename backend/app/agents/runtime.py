"""Agent runtime — plan/act/self-check/report with hard limits."""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass

from app.config import get_settings
from app.llm.gateway import get_gateway

@dataclass
class RunContext:
    role_id: str
    company_id: str
    trigger: str

async def run_agent(ctx: RunContext) -> dict[str, str]:
    settings = get_settings()
    gateway = get_gateway()
    start = time.monotonic()
    # 1. Load context (stub)
    # 2. Plan
    plan = await gateway.chat(messages=[{"role": "user", "content": f"Plan for {ctx.trigger}"}], company_id=ctx.company_id)
    # 3. Act — max 8 tool calls (stub)
    # 4. Self-check via fast model
    # 5. Report
    elapsed = time.monotonic() - start
    if elapsed > settings.max_wall_time_seconds:
        return {"status": "timeout", "plan": plan["content"]}
    return {"status": "completed", "plan": plan["content"], "elapsed": str(elapsed)}
