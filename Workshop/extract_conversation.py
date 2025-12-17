import re
import os

INPUT_FILE = r"D:\Project_Gongmyung\Gongmyung_Library\Chat_History_Full.md"
OUTPUT_FILE = r"D:\Project_Gongmyung\Gongmyung_Library\Code_AI\Reference\Conversation_Index.md"

def has_korean(text):
    # Check for Hangul Syllables or Jamo
    return bool(re.search('[\uac00-\ud7a3\u3130-\u318F]', text))

def extract_conversations():
    print(f"Scanning: {INPUT_FILE}")
    
    if not os.path.exists(INPUT_FILE):
        print("Input file not found.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    output_lines.append("# 🗣️ Conversation Index (Korean Only)\n")
    output_lines.append(f"**Source:** `{INPUT_FILE}`\n")
    output_lines.append("**Note:** Click the line number to jump to the context (requires VS Code support or manual navigation).\n\n")
    output_lines.append("---\n\n")

    current_speaker = None
    current_block = []
    start_line = 0
    
    # Simple state machine
    # 0: Looking for header
    # 1: Reading content
    
    for i, line in enumerate(lines):
        line_num = i + 1
        stripped = line.strip()
        
        # Detect Speaker Headers
        if stripped.startswith("### 👤 User"):
            # Process previous block
            if current_block and has_korean("".join(current_block)):
                content = "".join(current_block).strip()
                output_lines.append(f"### 👤 User (Line {start_line})\n")
                output_lines.append(f"{content}\n\n")
            
            current_speaker = "User"
            current_block = []
            start_line = line_num
            continue
            
        elif stripped.startswith("### 🤖 Copilot"):
            # Process previous block
            if current_block and has_korean("".join(current_block)):
                content = "".join(current_block).strip()
                output_lines.append(f"### 🤖 Copilot (Line {start_line})\n")
                output_lines.append(f"{content}\n\n")
            
            current_speaker = "Copilot"
            current_block = []
            start_line = line_num
            continue
            
        elif stripped.startswith("## 💬 Turn") or stripped.startswith("# 📁 Session"):
             # Process previous block if any (end of turn/session)
            if current_block and has_korean("".join(current_block)):
                content = "".join(current_block).strip()
                output_lines.append(f"### {current_speaker} (Line {start_line})\n")
                output_lines.append(f"{content}\n\n")
            current_block = []
            current_speaker = None
            continue

        # Accumulate content if inside a speaker block
        if current_speaker:
            # Skip purely structural markdown lines if desired, but keeping them preserves format
            current_block.append(line)

    # Process final block
    if current_block and has_korean("".join(current_block)):
        content = "".join(current_block).strip()
        output_lines.append(f"### {current_speaker} (Line {start_line})\n")
        output_lines.append(f"{content}\n\n")

    # Write output
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    print(f"Successfully generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_conversations()
