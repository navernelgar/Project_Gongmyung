import re

class GongmyungPrism:
    """
    [공명 프리즘 (Gongmyung Prism)]
    코드의 주석(해설)을 사용자의 수준(Level)에 맞춰 변환해서 보여주는 도구입니다.
    
    Levels:
    1. Seed (씨앗/초급): "왜?"에 집중. 비유와 구조 설명. (현재 CrepeCake_Focus.html 상태)
    2. Stem (줄기/중급): "어떻게?"에 집중. 로직 흐름과 데이터 타입.
    3. Flower (꽃/고급): "무엇을?"에 집중. 핵심 기호(●/○/◎)와 성능/최적화 메모.
    """
    
    def __init__(self):
        self.levels = {
            "seed": "초급 (구조/비유)",
            "stem": "중급 (로직/흐름)",
            "flower": "고급 (기호/핵심)"
        }

    def translate_comment(self, comment_block, target_level):
        """
        주석 블록을 받아서 타겟 레벨로 변환합니다.
        (실제 구현에서는 AI나 미리 정의된 딕셔너리를 사용해야 하지만, 
         여기서는 프로토타입 로직을 보여줍니다.)
        """
        # 예시 데이터베이스
        translations = {
            "toggleLayer": {
                "seed": """
        // ● [입력] id: 사용자가 클릭한 상자의 이름표(ID)를 받아옵니다.
        // ○ [로직] document.querySelectorAll: 문서에 있는 모든 '.layer' 상자들을 다 가져옵니다.
        // [이유] 내가 누른 것만 여는 게 아니라, '안 누른 다른 상자들을 닫기 위해서' 전체를 다 검사해야 합니다.
        // ◎ [행동] classList.toggle: 맞다면 'active'라는 이름표를 붙이거나 뗍니다.""",
                
                "stem": """
        // ● Input(String id): Target Layer ID
        // ○ Logic(Loop): Iterate all .layer elements
        // ○ Logic(Condition): Check if l.id === input.id
        // ◎ Action(DOM): Toggle 'active' class based on match""",
                
                "flower": """
        // ● id -> ○ Find(.layer) -> ○ Match? -> ◎ Toggle/Remove(.active)"""
            }
        }
        
        # (이 부분은 실제 파일 파싱 로직으로 확장될 예정)
        return translations.get("toggleLayer", {}).get(target_level, comment_block)

class GongmyungTracer:
    """
    [공명 추적자 (Gongmyung Tracer)]
    실제 코드가 실행될 때, 주석(설계도)대로 움직였는지 감시합니다.
    """
    
    def compare_intent_vs_reality(self, intent_log, reality_log):
        """
        사용자의 질문: "서술한 것(주석)과 디버그(실제)가 다르면 어떻게 해?"
        답변: 그것은 '왜곡(Distortion)'입니다. 버그(Bug)의 다른 이름입니다.
        """
        discrepancies = []
        for i, (intent, real) in enumerate(zip(intent_log, reality_log)):
            if intent != real:
                discrepancies.append(f"Step {i}: 설계는 '{intent}'였으나, 실제는 '{real}'이었습니다.")
        
        return discrepancies

if __name__ == "__main__":
    prism = GongmyungPrism()
    print(f"System Ready: {prism.levels}")
