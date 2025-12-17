import os
import re
from datetime import datetime

# Mock AI Narrative Generation (In reality, this would call an LLM API)
def generate_narrative(logs):
    story = []
    story.append("# 🛡️ 모험가 일지: 속삭이는 숲의 하루\n")
    story.append(f"**날짜**: {datetime.now().strftime('%Y-%m-%d')}\n")
    story.append("**작성자**: 방랑 마법사 (Player)\n")
    story.append("---\n")
    
    # Context Analysis
    location = "알 수 없음"
    for line in logs:
        if "진입했습니다" in line:
            location = re.search(r"'(.*?)'", line).group(1)
            break
            
    story.append(f"오늘 나는 **{location}**으로 발걸음을 옮겼다. 숲의 공기는 차가웠지만, 모험을 시작하기엔 나쁘지 않은 날씨였다.\n")
    
    # Process Events
    for line in logs:
        time = line[:10]
        content = line[11:]
        
        if "[Chat]" in content:
            parts = content.split(':')
            if len(parts) > 1:
                speaker = parts[0].replace("[Chat] ", "").strip()
                msg = ":".join(parts[1:]).strip() # Handle colons in message
                if "[나]" in speaker:
                    story.append(f"> \"{msg}\"\n\n나는 지나가던 모험가에게 짧게 대답했다.")
                else:
                    story.append(f"숲 입구에서 `{speaker}`라는 자가 소리쳤다. \"{msg}\"")
            else:
                continue
                
        elif "[Combat]" in content:
            if "나타났습니다" in content:
                mob = re.search(r"'(.*?)'", content).group(1)
                story.append(f"\n그때였다. 수풀 사이로 **{mob}**가 거친 숨을 내쉬며 튀어나왔다.")
            elif "스킬" in content:
                skill = re.search(r"'(.*?)'", content).group(1)
                story.append(f"나는 당황하지 않고 주문을 외웠다. **{skill}**! 화염이 몬스터를 덮쳤다.")
            elif "처치" in content:
                story.append("녀석은 비명과 함께 쓰러졌다. 꽤나 싱거운 승부였다.\n")
                
        elif "[Loot]" in content:
            item = re.search(r"\[(.*?)\]", content).group(1)
            story.append(f"전리품으로 `{item}`을 챙겼다. 돈이 될지는 모르겠지만.")
            
        elif "[Move]" in content and "발견" in content:
            place = re.search(r"'(.*?)'", content).group(1)
            story.append(f"\n한참을 걷다 보니 **{place}**를 발견했다. 지동에는 나와있지 않은 곳이다. 들어가 봐도 괜찮을까?")
            
    story.append("\n---\n")
    story.append("### 📊 오늘의 성과\n")
    story.append("- **탐험 지역**: 속삭이는 숲\n")
    story.append("- **처치 몬스터**: 광폭한 멧돼지\n")
    story.append("- **획득 아이템**: 멧돼지의 송곳니\n")
    
    return "".join(story)

def main():
    log_path = "sample_game_log.txt"
    if not os.path.exists(log_path):
        print("Log file not found.")
        return

    with open(log_path, 'r', encoding='utf-8') as f:
        logs = f.readlines()
        
    narrative = generate_narrative(logs)
    
    # Save to Vault
    vault_path = r"D:\Obsidian Vault\00_Inbox\Game_Journal_Sample.md"
    with open(vault_path, 'w', encoding='utf-8') as f:
        f.write(narrative)
        
    print(f"Successfully generated journal at: {vault_path}")

if __name__ == "__main__":
    main()
