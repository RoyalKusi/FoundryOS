import pytest
from app.llm.gateway import get_gateway, TokenUsage

@pytest.mark.asyncio
async def test_mock_gateway_charter() -> None:
    gw = get_gateway()
    assert gw.mode == "mock"
    result = await gw.chat(messages=[{"role": "user", "content": "hello"}], json_schema={"type": "object", "properties": {"mission": {"type": "string"}}})
    assert "content" in result
    assert "usage" in result

@pytest.mark.asyncio
async def test_mock_embedding() -> None:
    gw = get_gateway()
    vecs = await gw.embedding(["hello world"])
    assert len(vecs) == 1
    assert len(vecs[0]) == 1024
