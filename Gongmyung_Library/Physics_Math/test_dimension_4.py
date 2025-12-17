import math
import time
import os

# 4차원 시뮬레이션: 시간(Time)과 파동(Wave)
# 이론: 정지된 공간에 시간이 흐르면 에너지가 파동 형태로 전파된다.

class WaveSpace:
    def __init__(self, length):
        self.length = length
        self.space = [0.0] * length

    def propagate(self, t, frequency, amplitude):
        # 파동 방정식: y = A * sin(kx - wt)
        # 여기서는 k=0.5, w=frequency 로 가정
        k = 0.5
        w = frequency
        
        current_state = []
        for x in range(self.length):
            val = amplitude * math.sin(k * x - w * t)
            current_state.append(val)
        return current_state

    def render(self, state, t):
        # 아스키 아트로 파동 시각화
        # 값의 범위 -A ~ +A 를 그래프 높이로 변환
        print(f"\n[Time {t}] Wave Propagation")
        
        # 그래프 높이 (예: -1.0 ~ 1.0)
        max_height = 5
        min_height = -5
        
        # 위에서부터 아래로 스캔하며 그리기
        for h in range(max_height, min_height - 1, -1):
            line = ""
            threshold = h / 2.5 # 스케일 조정
            
            for val in state:
                # 현재 높이 h가 파동 값 val에 근접하면 표시
                if abs(val - threshold) < 0.3:
                    line += "●"
                elif h == 0:
                    line += "-" # 기준선
                else:
                    line += " "
            print(line)

# 실행
print("--- 4차원 시뮬레이션 시작: 파동의 전파 ---")
universe = WaveSpace(length=40)
frequency = 1.0
amplitude = 2.0

# 시간 t=0 부터 t=10 까지 파동의 변화 관측
for t in range(11):
    state = universe.propagate(t, frequency, amplitude)
    universe.render(state, t)
    # time.sleep(0.2) # 실제 애니메이션 효과를 원하면 주석 해제
