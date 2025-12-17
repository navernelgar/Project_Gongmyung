import json
import os
import re

def analyze_structure(content):
    lines = content.split('\n')
    total_lines = len(lines)
    
    narrative_tree = []
    code_lines = []
    
    # Heuristics for Tree Structure
    current_chapter = None
    current_section = None
    
    for i, line in enumerate(lines):
        line_content = line.strip()
        code_lines.append(line) # Keep raw line for right page
        
        if not line_content: continue

        # Level 1: Major Headers (# )
        if line_content.startswith('# '):
            node = {
                "level": 1,
                "text": line_content.replace('# ', '').strip(),
                "line_index": i + 1,
                "desc": "Chapter Start"
            }
            narrative_tree.append(node)
            current_chapter = node

        # Level 2: Sub Headers (## ) or Request Headers
        elif line_content.startswith('## '):
            node = {
                "level": 2,
                "text": line_content.replace('## ', '').strip(),
                "line_index": i + 1,
                "desc": "Section"
            }
            narrative_tree.append(node)
            current_section = node

        # Level 3: User/Assistant Markers
        elif '**User:**' in line_content or '**Assistant:**' in line_content:
            speaker = "User" if '**User:**' in line_content else "AI"
            node = {
                "level": 3,
                "text": f"{speaker} Turn",
                "line_index": i + 1,
                "desc": "Interaction"
            }
            narrative_tree.append(node)

        # Narrative Phase Detection (Fallback if no headers)
        # ... (Keep existing logic if needed, or simplify for now)

    return {
        "narrative": narrative_tree,
        "code": code_lines,
        "meta": {
            "total_lines": total_lines,
            "type": "Chat Log" if "User:" in content else "Code/Text"
        }
    }

def analyze_narrative(content):
    # Legacy function wrapper for backward compatibility
    struct = analyze_structure(content)
    return json.dumps(struct, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    file_path = r"D:\Project_Gongmyung\Gongmyung_Library\Code_AI\Reference\chat_origner\2025-12-08_chat_log.md"
    output_path = r"D:\Project_Gongmyung\Gongmyung_Library\Code_AI\analysis_result.json"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = analyze_structure(content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Structured analysis saved to: {output_path}")
    except Exception as e:
        print(f"Error: {e}")
