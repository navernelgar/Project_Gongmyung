import json

try:
    with open(r'c:\Users\Owner\Desktop\chat.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    requests = data.get('requests', [])[:10]
    
    for i, req in enumerate(requests):
        print(f'--- Turn {i+1} ---')
        user_text = req.get("message", {}).get("text", "")
        print(f'User: {user_text[:200]}...')
        
        responses = req.get('response', [])
        ai_text = ''
        for resp in responses:
            if isinstance(resp, dict) and 'value' in resp:
                ai_text += resp['value'] + ' '
        print(f'AI: {ai_text[:200]}...')
        print('')

except Exception as e:
    print(f"Error: {e}")
