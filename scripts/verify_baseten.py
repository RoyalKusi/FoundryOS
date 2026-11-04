#!/usr/bin/env python3
"""Verify Baseten Maverick connectivity — mimics backend gateway."""
import os
import sys
import asyncio
from pathlib import Path

# Ensure backend/.env loaded
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
    load_dotenv(Path(__file__).parent.parent / "backend" / ".env")
except ImportError:
    pass

# Also load via pydantic settings
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.config import get_settings

async def test_live():
    settings = get_settings()
    # force reload from env after .env creation
    print("=== Baseten Verify ===")
    print(f"BASETEN_BASE_URL: {settings.baseten_base_url}")
    print(f"BASETEN_REASONING_MODEL: {settings.baseten_reasoning_model}")
    print(f"BASETEN_FAST_MODEL: {settings.baseten_fast_model}")
    print(f"LLM_MODE: {settings.llm_mode}")
    print(f"BASETEN_API_KEY present: {bool(settings.baseten_api_key)} len={len(settings.baseten_api_key) if settings.baseten_api_key else 0}")
    if settings.baseten_api_key:
        print(f"Key prefix: {settings.baseten_api_key[:12]}...")
    
    if settings.llm_mode != "live":
        print("WARNING: LLM_MODE != live — set LLM_MODE=live in .env for live test")
    
    if not settings.baseten_api_key:
        print("ERROR: No BASETEN_API_KEY — cannot test live")
        return False

    try:
        from app.llm.gateway import get_gateway
        gw = get_gateway()
        # Reset gateway to ensure live mode if settings changed
        gw.mode = settings.llm_mode
        if gw.mode == "live" and gw.live is None:
            from app.llm.gateway import LiveLLM
            gw.live = LiveLLM()
        
        print(f"\nGateway mode: {gw.mode}, live client: {gw.live is not None and gw.live.client is not None}")
        
        # Test chat
        print("\n--- Testing chat (Maverick) ---")
        result = await gw.chat(
            messages=[{"role": "user", "content": "Say hello in 5 words"}],
            model=settings.baseten_reasoning_model,
            temperature=0.7,
        )
        print(f"SUCCESS: {result['content'][:500]}")
        print(f"Usage: {result['usage']}")
        
        # Test structured charter generation
        print("\n--- Testing charter generation (structured JSON) ---")
        from app.services.charter_service import generate_charter
        charter = await generate_charter({"companyName": "TestCo", "pitch": "AI for founders", "industry": "SaaS"})
        print(f"Charter mission: {charter.mission}")
        print(f"Charter vision: {charter.vision}")
        print(f"Charter values: {charter.values}")
        return True
    except Exception as e:
        print(f"\nFAILED: {e}")
        import traceback
        traceback.print_exc()
        print("\n--- Diagnostics ---")
        print("Possible causes:")
        print("- API key invalid/expired (403 please check api-key)")
        print("- Baseten model slug changed — check dashboard at https://app.baseten.co")
        print("- Network blocked or base_url wrong")
        print("- Try: curl https://inference.baseten.co/v1/models -H \"Authorization: Bearer $BASETEN_API_KEY\"")
        return False

if __name__ == "__main__":
    ok = asyncio.run(test_live())
    sys.exit(0 if ok else 1)
