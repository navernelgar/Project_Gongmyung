import urllib.request
import json
import os

file_path = r"D:\Project_Gongmyung\Gongmyung_Library\Code_AI\Reference\chat_origner\2025-12-08_chat_log.md"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    url = "http://localhost:3001/api/analyze"
    data = {
        "type": "narrative",
        "content": content
    }
    
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})

    with urllib.request.urlopen(req) as response:
        raw_response = response.read().decode('utf-8')
        print(f"Raw Response: {raw_response}")
        result = json.loads(raw_response)
        print("=== Layer 2 (Structure) ===")
        print(result.get('layer_2', 'No Layer 2'))
        print("\n=== Layer 6 (Analysis) ===")
        print(result.get('layer_6', 'No Layer 6'))

except Exception as e:
    print(f"An error occurred: {e}")
