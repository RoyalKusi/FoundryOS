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
    payload={"companyName":"FoundryOS","pitch":"AI OS for founders","industry":"SaaS","company_id":"test-123"}
    from pathlib import Path
    prompt_path=Path('backend/app/agents/prompts/charter.md')
    system_prompt=prompt_path.read_text(encoding="utf-8") if prompt_path.exists() else "Generate charter"
    user_content=f"Company payload: {json.dumps(payload)}\n\nGenerate Charter JSON with mission, vision, values, okrs, constraints, cadence."
    messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_content}]
    from app.schemas.charter import CharterSchema
    schema=CharterSchema.model_json_schema()
    result=await g.chat(messages=messages, model=get_settings().baseten_reasoning_model, temperature=0.7, json_schema=schema, company_id=payload.get("company_id"))
    print("RAW CONTENT:")
    print(result['content'])
    print("\n--- Trying parse ---")
    try:
        data=json.loads(result['content'])
        print(json.dumps(data, indent=2)[:3000])
        print("\nValues type:", type(data.get('values')), data.get('values')[:2] if data.get('values') else None)
    except Exception as e:
        print(e)

asyncio.run(test())
