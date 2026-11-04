"""Single LLM gateway — retries, token accounting, MockLLM for LLM_MODE=mock."""

from __future__ import annotations

import asyncio
import json
import random
import time
from dataclasses import dataclass, field
from typing import Any

import structlog
from pydantic import BaseModel, ValidationError

from app.config import get_settings

logger = structlog.get_logger(__name__)


@dataclass
class TokenUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0


class TokenBucket:
    def __init__(self) -> None:
        self._store: dict[str, dict[str, Any]] = {}

    def check(self, company_id: str, tokens: int = 1) -> bool:
        settings = get_settings()
        logger.debug("token_bucket_check", company_id=company_id, tokens=tokens, budget=settings.token_budget_monthly)
        return True

    def record(self, company_id: str, usage: TokenUsage) -> None:
        logger.info("token_usage", company_id=company_id, total=usage.total_tokens, cost=usage.cost_usd)


token_bucket = TokenBucket()


class MockLLM:
    async def chat(
        self,
        *,
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float = 0.7,
        json_schema: dict[str, Any] | None = None,
        stream: bool = False,
    ) -> dict[str, Any]:
        last = messages[-1]["content"].lower() if messages else ""
        if json_schema and "mission" in str(json_schema):
            return {
                "content": json.dumps(
                    {
                        "mission": "Empower founders with an autonomous OS",
                        "vision": "Every startup runs like a Fortune 500 from day one",
                        "values": ["clarity", "ownership", "velocity"],
                        "okrs": [
                            {
                                "objective": "Launch MVP",
                                "keyResults": ["Ship core flows", "Onboard 10 pilot users"],
                                "ownerRoleHint": "Operations Officer",
                                "dueAt": "2026-08-01T00:00:00Z",
                            }
                        ],
                        "constraints": {"budget": "$50/mo", "headcount": "1", "regulations": []},
                        "cadence": {"standupTime": "08:00", "weeklyReportDay": "Friday", "weeklyReportTime": "16:00"},
                    }
                ),
                "usage": TokenUsage(prompt_tokens=100, completion_tokens=150, total_tokens=250, cost_usd=0.001),
            }
        if "resolutions" in str(json_schema).lower() if json_schema else False or "resolution" in last:
            return {
                "content": json.dumps(
                    {"resolutions": [{"decision": "Mock decision", "rationale": "Mock rationale", "ownerRoleId": "00000000-0000-0000-0000-000000000001", "dueAt": "2026-08-15T00:00:00Z", "dependencies": []}]}
                ),
                "usage": TokenUsage(prompt_tokens=80, completion_tokens=60, total_tokens=140, cost_usd=0.0005),
            }
        body = f"Mock response to: {last[:200]}"
        if json_schema:
            body = json.dumps({"mock": True, "echo": last[:200]})
        return {
            "content": body,
            "usage": TokenUsage(prompt_tokens=50, completion_tokens=50, total_tokens=100, cost_usd=0.0002),
        }

    async def embedding(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * 1024 for _ in texts]

    async def rerank(self, query: str, docs: list[str]) -> list[float]:
        return [1.0 - i * 0.1 for i in range(len(docs))]

    async def transcribe(self, audio_bytes: bytes) -> str:
        return "mock transcription of audio"


class LiveLLM:
    def __init__(self) -> None:
        settings = get_settings()
        try:
            from openai import AsyncOpenAI

            self.client = AsyncOpenAI(
                api_key=settings.baseten_api_key, base_url=settings.baseten_base_url, timeout=60.0
            )
        except Exception as e:
            logger.warning("openai_init_failed", error=str(e))
            self.client = None  # type: ignore[attr-defined]

    async def _with_retries(self, coro: Any) -> Any:
        max_retries = 3
        for attempt in range(max_retries + 1):
            try:
                return await coro()
            except Exception as e:
                if attempt == max_retries:
                    raise
                backoff = (2**attempt) + random.uniform(0, 0.5)
                logger.warning("llm_retry", attempt=attempt, backoff=backoff, error=str(e))
                await asyncio.sleep(backoff)
        return None

    async def chat(self, *, messages: list[dict[str, str]], model: str | None = None, temperature: float = 0.7, json_schema: dict[str, Any] | None = None, stream: bool = False) -> dict[str, Any]:
        settings = get_settings()
        model = model or settings.baseten_reasoning_model
        if self.client is None:
            raise RuntimeError("LiveLLM client not initialized")
        kwargs: dict[str, Any] = {"model": model, "messages": messages, "temperature": temperature}
        if json_schema:
            kwargs["response_format"] = {"type": "json_object"}

        async def _call() -> dict[str, Any]:
            resp = await self.client.chat.completions.create(**kwargs)
            content = resp.choices[0].message.content or ""
            usage = getattr(resp, "usage", None)
            if usage:
                tu = TokenUsage(
                    prompt_tokens=getattr(usage, "prompt_tokens", 0),
                    completion_tokens=getattr(usage, "completion_tokens", 0),
                    total_tokens=getattr(usage, "total_tokens", 0),
                )
            else:
                tu = TokenUsage(prompt_tokens=100, completion_tokens=100, total_tokens=200)
            return {"content": content, "usage": tu}

        result = await self._with_retries(_call)
        if json_schema:
            try:
                json.loads(result["content"])
            except Exception as e:
                logger.warning("json_parse_failed", error=str(e))
                repair_messages = messages + [
                    {"role": "user", "content": f"Invalid JSON: {e}. Fix to schema {json_schema}"}
                ]
                kwargs["messages"] = repair_messages
                result = await self._with_retries(
                    lambda: self.client.chat.completions.create(**kwargs)
                )
        return result  # type: ignore[return-value]

    async def embedding(self, texts: list[str]) -> list[list[float]]:
        settings = get_settings()
        if not settings.baseten_embedding_url:
            return [[0.0] * 1024 for _ in texts]
        return [[0.0] * 1024 for _ in texts]

    async def rerank(self, query: str, docs: list[str]) -> list[float]:
        return [1.0 - i * 0.1 for i in range(len(docs))]

    async def transcribe(self, audio_bytes: bytes) -> str:
        return "mock transcription of audio via live stub"


@dataclass
class Gateway:
    mode: str = field(default_factory=lambda: get_settings().llm_mode)
    mock: MockLLM = field(default_factory=MockLLM)
    live: LiveLLM | None = None
    def __post_init__(self) -> None:
        if self.mode == "live":
            self.live = LiveLLM()
    async def chat(self, *, messages: list[dict[str, str]], model: str | None = None, temperature: float = 0.7, json_schema: dict[str, Any] | None = None, stream: bool = False, company_id: str | None = None, role_id: str | None = None) -> dict[str, Any]:
        start = time.monotonic()
        if self.mode == "mock" or self.live is None:
            result = await self.mock.chat(messages=messages, model=model, temperature=temperature, json_schema=json_schema, stream=stream)
        else:
            result = await self.live.chat(messages=messages, model=model, temperature=temperature, json_schema=json_schema, stream=stream)
        usage = result.get("usage", TokenUsage())
        assert isinstance(usage, TokenUsage)
        if company_id:
            token_bucket.record(company_id, usage)
            token_bucket.check(company_id, usage.total_tokens)
        elapsed = time.monotonic() - start
        logger.info("llm_chat", mode=self.mode, model=model, elapsed=elapsed, total_tokens=usage.total_tokens, company_id=company_id)
        return result

    async def embedding(self, texts: list[str]) -> list[list[float]]:
        if self.mode == "mock" or self.live is None:
            return await self.mock.embedding(texts)
        return await self.live.embedding(texts)

    async def rerank(self, query: str, docs: list[str]) -> list[float]:
        if self.mode == "mock" or self.live is None:
            return await self.mock.rerank(query, docs)
        assert self.live is not None
        return await self.live.rerank(query, docs)

    async def transcribe(self, audio_bytes: bytes) -> str:
        if self.mode == "mock" or self.live is None:
            return await self.mock.transcribe(audio_bytes)
        assert self.live is not None
        return await self.live.transcribe(audio_bytes)
    async def chat_structured(self, *, messages: list[dict[str, str]], schema_model: type[BaseModel], company_id: str | None = None) -> BaseModel:
        schema = schema_model.model_json_schema()
        result = await self.chat(messages=messages, json_schema=schema, company_id=company_id)
        content = result["content"]
        try:
            data = json.loads(content)
            return schema_model.model_validate(data)
        except (json.JSONDecodeError, ValidationError) as e:
            logger.warning("structured_parse_failed", error=str(e), content=content[:500])
            repair = messages + [{"role": "user", "content": f"Fix JSON, error: {e}. Output ONLY valid JSON."}]
            result2 = await self.chat(messages=repair, json_schema=schema, company_id=company_id)
            data2 = json.loads(result2["content"])
            return schema_model.model_validate(data2)

_gateway: Gateway | None = None


def get_gateway() -> Gateway:
    global _gateway
    if _gateway is None:
        _gateway = Gateway()
    return _gateway
