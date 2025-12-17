import datetime
import os
import json

class GongmyungThought:
    def __init__(self, memo_path="Gongmyung_Memo.txt"):
        self.timestamp = datetime.datetime.now()
        
        # 1. Sensation (감각)
        self.sensation = None  
        
        # 2. Interpretation (해석) - New
        self.interpretation = None
        
        # 3. Conceptualization (개념화/명명화) - New
        self.concept = None
        
        # 4. Concretization (구체화) - New
        self.plan = None
        
        # 5. Action (행동)
        self.action = None     
        
        # 6. Result (결과)
        self.result = None     
        
        self.memo_path = memo_path

    def sense(self, input_data):
        """● 감각: 외부 데이터를 있는 그대로 받아들입니다."""
        self.sensation = input_data
        return self

    def interpret(self):
        """○ 해석: 입력된 데이터의 '의미'와 '맥락'을 읽어냅니다."""
        if not self.sensation:
            self.interpretation = "무의 상태 (Void)"
            return self
            
        # Placeholder Logic for Discussion
        data_type = self.sensation.get('type', 'unknown')
        if data_type == 'log':
            self.interpretation = "과거의 기록(Log)이 유입됨. 서사적 구조를 내포하고 있음."
        elif data_type == 'user_command':
            self.interpretation = "사용자의 의지(Will)가 감지됨."
        else:
            self.interpretation = "단순 데이터 흐름."
            
        return self

    def conceptualize(self):
        """□ 개념화/명명화: 해석된 정보에 '이름'을 붙이고 '정의'합니다."""
        if not self.interpretation:
            self.concept = "정의 불가"
            return self
            
        # Placeholder Logic
        if "서사적 구조" in self.interpretation:
            self.concept = "모험의 서 (Adventure Book)"
        elif "사용자의 의지" in self.interpretation:
            self.concept = "명령 (Directive)"
        else:
            self.concept = "배경 소음 (Noise)"
            
        return self

    def concretize(self):
        """◇ 구체화: 개념을 실현하기 위한 '구조'와 '계획'을 짭니다."""
        if self.concept == "모험의 서 (Adventure Book)":
            self.plan = ["로그 파싱", "인물/사건 추출", "문장 재구성", "파일 저장"]
        elif self.concept == "명령 (Directive)":
            self.plan = ["의도 분석", "가용 도구 검색", "실행"]
        else:
            self.plan = ["대기"]
            
        return self

    def act(self):
        """◎ 행동: 구체화된 계획을 실제로 수행합니다."""
        if self.plan and "로그 파싱" in self.plan:
            self.action = "소설 변환 엔진 가동 (Port 3002)"
        elif self.plan and "실행" in self.plan:
            self.action = "시스템 명령 수행"
        else:
            self.action = "상태 유지 (Idle)"
        return self

    def transition(self):
        """⇒ 결과: 사이클을 마치고 다음 상태로 전이합니다."""
        self.result = f"Cycle Complete. Concept: {self.concept}"
        self.record_thought()
        return {
            "timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "sensation": self.sensation,
            "interpretation": self.interpretation,
            "concept": self.concept,
            "plan": self.plan,
            "action": self.action,
            "result": self.result
        }

    def record_thought(self):
        """메모장에 사고 과정을 기록합니다."""
        log_entry = (
            f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}]\n"
            f"1. 감각 (Sense)       : {json.dumps(self.sensation, ensure_ascii=False)}\n"
            f"2. 해석 (Interpret)   : {self.interpretation}\n"
            f"3. 개념 (Concept)     : {self.concept}\n"
            f"4. 구체화 (Concretize): {self.plan}\n"
            f"5. 행동 (Act)         : {self.action}\n"
            f"6. 결과 (Result)      : {self.result}\n"
            f"{'='*50}\n"
        )
        
        try:
            with open(self.memo_path, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error writing to memo: {e}")
