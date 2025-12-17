import re
import os

INPUT_FILE = r"D:\Project_Gongmyung\Gongmyung_Library\Code_AI\Reference\Conversation_Index.md"
OUTPUT_FILE = r"D:\Project_Gongmyung\Gongmyung_Library\Code_AI\Reference\Chat_Review_Pending.md"

def create_review_sheets():
    print(f"Reading: {INPUT_FILE}")
    
    if not os.path.exists(INPUT_FILE):
        print("Input file not found.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by speaker headers to identify turns
    # Regex looks for "### User" or "### Copilot"
    # We want to group roughly 10 turns (User + Copilot pairs) together
    
    # Split into blocks based on "### User" or "### 👤 User"
    # The regex matches "###" followed by optional emoji/space and "User"
    blocks = re.split(r'(?=###\s*(?:👤\s*)?User)', content)
    
    # The first block is header info, keep it
    header = blocks[0]
    conversation_blocks = blocks[1:]
    
    output_content = header + "\n"
    
    chunk_size = 10
    total_blocks = len(conversation_blocks)
    
    print(f"Total conversation turns found: {total_blocks}")
    
    for i in range(0, total_blocks, chunk_size):
        chunk = conversation_blocks[i : i + chunk_size]
        
        # Add the conversation chunk
        output_content += "".join(chunk)
        
        # Add the Review Section
        start_idx = i + 1
        end_idx = min(i + chunk_size, total_blocks)
        
        output_content += "\n" + "="*50 + "\n"
        output_content += f"## 🛑 Review Point (Turns {start_idx} ~ {end_idx})\n"
        output_content += "### 📝 AI Analysis & Annotations\n"
        output_content += "> [Write your analysis here. What happened? What did we learn? Any rules established?]\n\n"
        output_content += "="*50 + "\n\n"

    # Write output
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    print(f"Successfully generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    create_review_sheets()
