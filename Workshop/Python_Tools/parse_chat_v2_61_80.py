import json

file_path = r'c:\Users\Owner\Desktop\2.json'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    requests = data.get('requests', [])
    
    # Process turns 61 to 80 (indices 60 to 79)
    start_index = 60
    end_index = 80
    
    print(f"Analyzing {file_path} (Turns 61-80)...")
    
    for i in range(start_index, min(end_index, len(requests))):
        req = requests[i]
        user_text = req.get("message", {}).get("text", "")
        
        # Get AI response summary
        responses = req.get('response', [])
        ai_text = ''
        for resp in responses:
            if isinstance(resp, dict) and 'value' in resp:
                ai_text += resp['value'] + ' '
        
        print(f'[{i+1}] User: {user_text[:100].replace(chr(10), " ")}...')
        # print(f'      AI: {ai_text[:50].replace(chr(10), " ")}...')
        
        if (i + 1) % 10 == 0:
            print(f"--- End of Batch {(i+1)//10} (Turns {i-8}-{i+1}) ---\n")

except Exception as e:
    print(f"Error: {e}")