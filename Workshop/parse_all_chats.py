import json
import os
import glob

# Configuration
INPUT_DIR = r"d:\workspaceStorage\chat"
OUTPUT_FILE = r"D:\Project_Gongmyung\Gongmyung_Library\Chat_History_Full.md"

def parse_all_chats():
    print(f"Scanning directory: {INPUT_DIR}")
    json_files = glob.glob(os.path.join(INPUT_DIR, "*.json"))
    
    if not json_files:
        print("No JSON files found.")
        return

    print(f"Found {len(json_files)} files. Processing...")

    all_chats = []

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Use file modification time as a proxy for date if not in content
                mod_time = os.path.getmtime(file_path)
                requests = data.get('requests', [])
                if requests:
                    all_chats.append({
                        'file': os.path.basename(file_path),
                        'timestamp': mod_time,
                        'requests': requests
                    })
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    # Sort by timestamp (oldest first)
    all_chats.sort(key=lambda x: x['timestamp'])

    markdown_content = "# 📜 Project Gongmyung Full Chat History\n\n"
    markdown_content += "**Note:** Consolidated history from all workspace chat logs.\n\n"
    markdown_content += "---\n\n"

    total_turns = 0
    
    for chat_session in all_chats:
        markdown_content += f"# 📁 Session: {chat_session['file']}\n"
        markdown_content += "---\n\n"
        
        for i, req in enumerate(chat_session['requests']):
            user_msg = req.get('message', {}).get('text', '')
            if not user_msg:
                continue

            total_turns += 1
            markdown_content += f"## 💬 Turn {i+1}\n\n"
            markdown_content += f"### 👤 User\n{user_msg}\n\n"

            responses = req.get('response', [])
            ai_text_buffer = ""
            for resp in responses:
                # Handle simple value structure (found in some logs)
                if 'value' in resp and isinstance(resp['value'], str):
                    ai_text_buffer += resp['value'] + "\n\n"
                # Handle structured kind/content structure
                elif resp.get('kind') == 'markdown':
                    content = resp.get('content', {}).get('value', '')
                    if content:
                        ai_text_buffer += content + "\n\n"
            
            if ai_text_buffer:
                markdown_content += f"### 🤖 Copilot\n{ai_text_buffer}\n"
            
            markdown_content += "---\n\n"
        
        markdown_content += "\n<br>\n\n"

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Successfully generated: {OUTPUT_FILE}")
    print(f"Total Sessions: {len(all_chats)}")
    print(f"Total Turns: {total_turns}")

if __name__ == "__main__":
    parse_all_chats()
