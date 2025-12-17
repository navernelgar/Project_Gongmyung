import time
import math
import psutil
import random

class GongmyungSystemMonitor:
    """
    공명 시스템 모니터 (Gongmyung System Monitor)
    
    기술적 시스템 모니터링(CPU, RAM)과 공명 철학(기호, 16bit 구조)을 결합한 구현체입니다.
    시스템의 물리적 상태를 '공명문(Resonance Sentence)'으로 변환하여 해석합니다.
    """
    
    def __init__(self):
        self.prev_cpu = psutil.cpu_percent()
        self.prev_ram = psutil.virtual_memory().percent
        self.start_time = time.time()
        self.history = []
        
        # 공명 기호 정의
        self.SYM_START = "●"   # 주체/감각/입력
        self.SYM_COND  = "○"   # 조건/상태/판단
        self.SYM_ACT   = "◎"   # 흐름/작용/연산
        self.SYM_RES   = "⇒"   # 결과/전이
        self.SYM_ERR   = "×"   # 오류/불협화음

    def _calculate_metrics(self, current_cpu, current_ram):
        """
        시스템의 변화량(Δ), 공명도(𝓡), 흐름(F)을 계산합니다.
        """
        # Δ (Delta): 변화량의 크기
        delta_cpu = current_cpu - self.prev_cpu
        delta_ram = current_ram - self.prev_ram
        delta_total = math.sqrt(delta_cpu**2 + delta_ram**2)
        
        # 𝓡 (Resonance): 안정도 (변화가 적을수록 높음, 0~1)
        # 변화가 너무 크면 공명도가 깨진 것으로 간주
        resonance = 1.0 / (1.0 + delta_total * 0.1)
        
        # F (Flow): 흐름/엔트로피 (시스템 부하가 높을수록 흐름이 격렬함)
        flow = (current_cpu + current_ram) / 2.0
        
        return delta_total, resonance, flow

    def _generate_16bit_state(self, cpu, ram, resonance):
        """
        시스템 상태를 16bit 세그먼트(Header-Core-Decision-Result)로 인코딩합니다.
        각 4bit (0~15)
        """
        # Header (4bit): 시스템 활성 상태 (CPU 레벨)
        # 0~100% -> 0~15
        header = int((cpu / 100.0) * 15)
        
        # Core (4bit): 메모리 점유 상태 (RAM 레벨)
        core = int((ram / 100.0) * 15)
        
        # Decision (4bit): 공명도/안정성 (높을수록 높은 값)
        decision = int(resonance * 15)
        
        # Result (4bit): 종합 상태 (임의의 해시 또는 흐름의 결론)
        # 여기서는 (Header + Core) % 16 으로 단순화
        result = (header + core) % 16
        
        # 16bit Hex String (예: 0x3A9D)
        hex_code = f"0x{header:X}{core:X}{decision:X}{result:X}"
        return hex_code

    def _translate_to_gongmyung(self, cpu, ram, delta, resonance):
        """
        수치 데이터를 공명문(Resonance Sentence)으로 번역합니다.
        """
        # 1. 주체 (●): 시스템의 현재 감각
        subject = f"{self.SYM_START}(CPU:{cpu}%/RAM:{ram}%)"
        
        # 2. 조건 (○): 상태 판단
        if resonance > 0.8:
            condition = f"{self.SYM_COND}(Stable)"
        elif resonance > 0.5:
            condition = f"{self.SYM_COND}(Fluctuating)"
        else:
            condition = f"{self.SYM_COND}(Unstable)"
            
        # 3. 작용 (◎): 시스템의 반응
        if delta < 1.0:
            action = f"{self.SYM_ACT}(Maintain)"
        elif delta < 10.0:
            action = f"{self.SYM_ACT}(Adjust)"
        else:
            action = f"{self.SYM_ACT}(Surge)"
            
        # 4. 결과 (⇒): 최종 상태
        result = f"{self.SYM_RES}(𝓡:{resonance:.2f})"
        
        return f"{subject} ~ {condition} ~ {action} ~ {result}"

    def monitor_step(self):
        """
        한 단계의 모니터링을 수행하고 공명문을 출력합니다.
        """
        current_cpu = psutil.cpu_percent(interval=1)
        current_ram = psutil.virtual_memory().percent
        
        delta, resonance, flow = self._calculate_metrics(current_cpu, current_ram)
        hex_code = self._generate_16bit_state(current_cpu, current_ram, resonance)
        gongmyung_sentence = self._translate_to_gongmyung(current_cpu, current_ram, delta, resonance)
        
        # 출력 (공명 크레이프케이크 레이어 구조)
        print("-" * 60)
        print(f"[Layer 1: Gongmyung] {gongmyung_sentence}")
        print(f"[Layer 2: 16-bit Code] {hex_code}")
        print(f"[Layer 3: Metrics     ] Δ:{delta:.2f} | 𝓡:{resonance:.2f} | F:{flow:.2f}")
        
        # 상태 업데이트
        self.prev_cpu = current_cpu
        self.prev_ram = current_ram
        
        return hex_code

if __name__ == "__main__":
    monitor = GongmyungSystemMonitor()
    print("시스템 공명 모니터를 시작합니다... (Ctrl+C로 중지)")
    print("구조: [공명문] -> [16bit 코드] -> [수치 데이터]")
    
    try:
        while True:
            monitor.monitor_step()
            # time.sleep(1) # psutil.cpu_percent(interval=1)에 이미 딜레이 포함됨
    except KeyboardInterrupt:
        print(f"\n{monitor.SYM_RES} 모니터링 종료.")
