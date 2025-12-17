import json

try:
    with open(r'c:\Users\Owner\Desktop\chat.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    requests = data.get('requests', [])
    
    # Process turns 101 to 200
    start_index = 100
    end_index = 200
    
    for i in range(start_index, min(end_index, len(requests))):
        req = requests[i]
        user_text = req.get("message", {}).get("text", "")
        
        print(f'[{i+1}] User: {user_text[:100].replace(chr(10), " ")}...')
        
        if (i + 1) % 10 == 0:
            print(f"--- End of Batch {(i+1)//10} (Turns {i-8}-{i+1}) ---\n")

except Exception as e:
    print(f"Error: {e}")