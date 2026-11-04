import httpx, json
key='b10_VhErMdIY.1a8oMYwCiDGmSZpemFNDWSl0mXgulAMh'
base='https://inference.baseten.co/v1'
models_to_test = [
    'meta-models/muse-spark-open',
    'meta-models/muse-spark-open-1026',
    'openai/gpt-oss-120b',
    'meta-llama/Llama-4-Maverick-17B-128E-Instruct',
    'meta-llama/Llama-4-Scout-17B-16E-Instruct',
]
for model in models_to_test:
    try:
        r=httpx.post(f'{base}/chat/completions', headers={'Authorization': f'Bearer {key}', 'Content-Type':'application/json'}, json={'model': model, 'messages': [{'role':'user','content':'Say hi in 5 words'}], 'temperature':0.7, 'max_tokens':20}, timeout=20)
        print(f"{model} -> {r.status_code}: {r.text[:500]}")
    except Exception as e:
        print(f"{model} err {e}")
