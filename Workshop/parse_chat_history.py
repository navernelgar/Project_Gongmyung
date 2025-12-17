import json
import os

# Configuration
INPUT_FILE = r"d:\workspaceStorage\chat\3a86f180-2133-43ce-be5d-c8a4e481c2ed.json"
OUTPUT_FILE = r"D:\Project_Gongmyung\Gongmyung_Library\Chat_History.md"

def parse_chat():
    print(f"Reading from: {INPUT_FILE}")
    
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: Input file not found.")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return

    requests = data.get('requests', [])
    
    markdown_content = "# 📜 Project Gongmyung Chat History\n\n"
    markdown_content += f"**Date:** {data.get('date', 'Unknown')}\n"
    markdown_content += "**Note:** This document is auto-generated for review and handover documentation.\n\n"
    markdown_content += "---\n\n"

    for i, req in enumerate(requests):
        # 1. User Request
        user_msg = req.get('message', {}).get('text', '')
        
        # Skip empty or system-like requests if needed
        if not user_msg:
            continue

        markdown_content += f"## 💬 Turn {i+1}\n\n"
        markdown_content += f"### 👤 User\n{user_msg}\n\n"

        # 2. AI Response
        responses = req.get('response', [])
        ai_text_buffer = ""
        
        for resp in responses:
            # Extract Markdown text responses
            if resp.get('kind') == 'markdown':
                content = resp.get('content', {}).get('value', '')
                if content:
                    ai_text_buffer += content + "\n\n"
            
            # Optionally extract tool calls if meaningful (e.g., terminal commands)
            # For now, let's focus on the conversation text as requested.
            # If we want to see what tools were used:
            # if resp.get('kind') == 'call':
            #     tool_name = resp.get('name')
            #     ai_text_buffer += f"*(Tool Call: {tool_name})*\n\n"

        if ai_text_buffer:
            markdown_content += f"### 🤖 Copilot\n{ai_text_buffer}\n"
        
        markdown_content += "---\n\n"

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Successfully generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    parse_chat()
