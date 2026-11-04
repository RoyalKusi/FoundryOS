import sys
sys.path.insert(0,'backend')
from app.config import get_settings
get_settings.cache_clear()
import app.llm.gateway
app.llm.gateway._gateway=None
from app.llm.gateway import get_gateway
import asyncio, json

async def test():
    g=get_gateway()
    print(f"Mode: {g.mode}, model: {get_settings().baseten_reasoning_model}")
    # Test simple chat with Muse
    res=await g.chat(messages=[{"role":"user","content":"Say hello in exactly 5 words, no reasoning"}], temperature=0.3)
    print("Chat result:", res['content'][:800])
    print("Usage:", res['usage'])
    # Test charter generation
    from app.services.charter_service import generate_charter
    charter=await generate_charter({"companyName":"FoundryOS","pitch":"AI OS for founders","industry":"SaaS","company_id":"test-123"})
    print("\nCharter:")
    print(f" Mission: {charter.mission}")
    print(f" Vision: {charter.vision}")
    print(f" Values: {charter.values}")
    print(json.dumps(charter.model_dump(), indent=2)[:1500])

asyncio.run(test())
