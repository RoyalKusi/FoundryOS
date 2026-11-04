import httpx
key='b10_VhErMdIY.1a8oMYwCiDGmSZpemFNDWSl0mXgulAMh'
base='https://inference.baseten.co/v1'
# Test Muse with better prompt and json
r=httpx.post(f'{base}/chat/completions', headers={'Authorization': f'Bearer {key}', 'Content-Type':'application/json'}, json={'model': 'meta-models/muse-spark-open-1026', 'messages': [{'role':'user','content':'Return JSON with mission and vision for a startup called FoundryOS that builds autonomous OS'}], 'temperature':0.7, 'max_tokens':300}, timeout=30)
print(r.status_code)
print(r.text[:2000])
# Try other models that might work
for model in ['deepseek-ai/DeepSeek-V4-Flash-0731', 'deepseek-ai/DeepSeek-V4.1-Flash', 'zai-org/GLM-5.2']:
    try:
        r2=httpx.post(f'{base}/chat/completions', headers={'Authorization': f'Bearer {key}', 'Content-Type':'application/json'}, json={'model': model, 'messages': [{'role':'user','content':'hi 5 words'}], 'max_tokens':20}, timeout=15)
        print(f"{model} -> {r2.status_code}: {r2.text[:200]}")
    except Exception as e:
        print(e)
