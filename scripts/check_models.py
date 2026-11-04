import httpx
key='b10_VhErMdIY.1a8oMYwCiDGmSZpemFNDWSl0mXgulAMh'
r=httpx.get('https://inference.baseten.co/v1/models', headers={'Authorization': f'Bearer {key}'}, timeout=10)
data=r.json()
print(f"Total models: {len(data['data'])}")
for m in data['data']:
    mid=m['id']
    print(mid)

print("\n--- filtering meta/llama/maverick ---")
for m in data['data']:
    mid=m['id'].lower()
    if 'llama' in mid or 'maverick' in mid or 'meta' in mid:
        print(m['id'])
