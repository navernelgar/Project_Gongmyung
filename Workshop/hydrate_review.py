import json
import os
import glob
import re
from difflib import SequenceMatcher

CHAT_DIR = r"d:\workspaceStorage\chat"
INPUT_FILE = r"D:\Project_Gongmyung\Gongmyung_Library\Code_AI\Reference\Chat_Review_Pending.md"
OUTPUT_FILE = r"D:\Project_Gongmyung\Gongmyung_Library\Code_AI\Reference\Chat_Review_Hydrated.md"

def load_all_chats():
    chats = []
    files = glob.glob(os.path.join(CHAT_DIR, "*.json"))
    for fpath in files:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                requests = data.get('requests', [])
                for req in requests:
                    user_text = req.get('message', {}).get('text', '').strip()
                    
                    ai_text = ""
                    responses = req.get('response', [])
                    for resp in responses:
                        if resp.get('kind') == 'markdown':
                            val = resp.get('content', {}).get('value', '')
                            if val: ai_text += val + "\n\n"
                        elif 'value' in resp and isinstance(resp['value'], str):
                             ai_text += resp['value'] + "\n\n"
                    
                    if user_text and ai_text:
                        chats.append({'user': user_text, 'ai': ai_text})
        except Exception as e:
            print(f"Error loading {fpath}: {e}")
    return chats

def find_response(user_msg, chat_db):
    best_match = None
    best_ratio = 0.0
    
    # Normalize
    user_msg_norm = user_msg.replace(" ", "").replace("\n", "")
    
    for entry in chat_db:
        entry_norm = entry['user'].replace(" ", "").replace("\n", "")
        
        # Exact match optimization
        if user_msg_norm == entry_norm:
            return entry['ai']
            
        # Fuzzy match
        ratio = SequenceMatcher(None, user_msg_norm, entry_norm).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = entry['ai']
            
    if best_ratio > 0.85: # Threshold
        return best_match
    return None

def hydrate():
    print("Loading chat logs...")
    chat_db = load_all_chats()
    print(f"Loaded {len(chat_db)} turns.")
    
    print(f"Reading {INPUT_FILE}...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    current_user_msg = []
    capture_mode = False
    
    # Regex to identify User headers
    user_header_re = re.compile(r"^### User \(Line \d+\)")
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if user_header_re.match(line):
            # If we were capturing a previous message, process it? 
            # No, the structure is Header -> Message -> Separator/Next Header
            # But the file has "---" separators.
            
            new_lines.append(line)
            i += 1
            
            # Capture message content until "---" or next header or "## 🛑"
            msg_lines = []
            while i < len(lines):
                sub_line = lines[i]
                if sub_line.strip() == "---" or user_header_re.match(sub_line) or sub_line.startswith("## 🛑"):
                    break
                msg_lines.append(sub_line)
                i += 1
            
            # Add message lines to output
            new_lines.extend(msg_lines)
            
            # Find AI response
            user_text = "".join(msg_lines).strip()
            if user_text:
                ai_response = find_response(user_text, chat_db)
                if ai_response:
                    new_lines.append("\n### 🤖 Copilot\n")
                    new_lines.append(ai_response)
                    new_lines.append("\n")
                else:
                    # new_lines.append("\n> [AI Response Not Found]\n")
                    pass
            
            # Continue loop from current i (which is at separator or next header)
            continue
            
        else:
            new_lines.append(line)
            i += 1

    print(f"Writing to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Done.")

if __name__ == "__main__":
    hydrate()
