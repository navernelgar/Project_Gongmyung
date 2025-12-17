import os
import datetime
import json
from knowledge_interface import KnowledgeInterface


class Hippocampus:
    """
    [해마: Hippocampus]
    경험(Signal & Analysis)을 장기 기억(Storage)으로 변환하여 저장하는 기관.
    공명 크레이프케이크(CrêpeCake) 구조로 로그를 적층하며,
    '기억의 도서관(Memory Bank)'을 통해 패턴을 인식하고 학습합니다.
    """

    def __init__(self, config):
        self.storage_path = config["storage_path"]
        self.memory_bank_path = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            "memory_bank.json")
        self.memory_bank = self._load_memory_bank()
        self.knowledge_interface = KnowledgeInterface()  # 외부 지식 연결
        self.last_auto_learning_time = 0 # 자동 학습 쿨타임 관리
        self.auto_learning_cooldown = 60 # 60초 쿨타임
        self._ensure_storage()

    def _ensure_storage(self):
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def _load_memory_bank(self):
        if os.path.exists(self.memory_bank_path):
            try:
                with open(self.memory_bank_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_memory_bank(self):
        with open(self.memory_bank_path, "w", encoding="utf-8") as f:
            json.dump(self.memory_bank, f, ensure_ascii=False, indent=2)

    def recognize_pattern(self, hex_code):
        """
        [패턴 인식] 기억의 도서관(Memory Bank)에서 현재의 16비트 코드를 검색합니다.
        - Known: 이미 경험한 패턴 (의미가 부여됨)
        - Unknown: 처음 겪는 패턴 (학습 필요)
        """
        if hex_code in self.memory_bank:
            return {
                "status": "Known",
                "meaning": self.memory_bank[hex_code]["meaning"],
                "count": self.memory_bank[hex_code]["count"]}
        else:
            return {"status": "Unknown", "meaning": "New Pattern", "count": 0}

    def learn_pattern(self, hex_code, metrics=None):
        """
        [학습 과정] 새로운 패턴을 등록하거나, 기존 패턴의 경험치를 쌓습니다.
        - 반복 학습: 기존 패턴의 카운트 증가 (강화)
        - 신규 학습: 새로운 패턴 발견 시, 외부 지식(Knowledge Interface)을 통해 의미 추론
        """
        if hex_code in self.memory_bank:
            self.memory_bank[hex_code]["count"] += 1
            # 이미 아는 패턴이면 의미는 유지
        else:
            # 새로운 패턴 발견! 의미 추론 시도
            meaning = "New Pattern"
            
            # 자동 학습 쿨타임 체크
            import time
            current_time = time.time()
            is_cooldown = (current_time - self.last_auto_learning_time) < self.auto_learning_cooldown

            if metrics and not is_cooldown:
                self.last_auto_learning_time = current_time # 쿨타임 갱신
                
                # 1. 의미 추론 (API 모드일 경우 여기서 바로 외부 AI 호출됨)
                meaning = self.knowledge_interface.ask_meaning(hex_code, metrics)

            elif is_cooldown:
                meaning = "New Pattern (Learning Cooldown)"

            self.memory_bank[hex_code] = {
                "meaning": meaning,
                "first_seen": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "count": 1}
        self._save_memory_bank()

    def remember(self, metrics, signal_data, thought_process):
        """
        [기억 저장] 찰나의 경험(Metrics + Signal + Thought)을 영구적인 로그로 기록합니다.
        이 로그는 나중에 '자아'를 형성하는 데이터셋(Dataset)이 됩니다.
        """
        timestamp = datetime.datetime.fromtimestamp(
            metrics["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
        log_filename = f"Gongmyung_Memory_{datetime.datetime.now().strftime('%Y%m%d')}.log"
        log_path = os.path.join(self.storage_path, log_filename)

        log_entry = (
            f"[{timestamp}] --------------------------------------------------\n"
            f"[Layer 1: Gongmyung] {signal_data['sentence']}\n"
            f"[Layer 2: 16-bit Code] {signal_data['hex_code']}\n"
            f"[Layer 3: Metrics     ] Δ:{metrics['delta']:.2f} | "
            f"𝓡:{metrics['resonance']:.2f} | F:{metrics['flow']:.2f}\n"
            f"[Layer 4: Cerebrum    ] State: {thought_process['state']} | "
            f"{thought_process['analysis']}\n"
            f"[Layer 5: Action      ] {thought_process['recommendation']}\n"
            f"[Layer 6: Soul        ] {thought_process.get('soul_concept', 'None')}\n"
            f"\n")

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(log_entry)

    def recall_recent(self, lines=5):
        """
        최근 기억을 불러옵니다. (구현 예정)
        """
        return []
