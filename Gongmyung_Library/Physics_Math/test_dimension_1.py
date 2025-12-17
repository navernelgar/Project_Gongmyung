import math
import random

# 1차원 시뮬레이션: 진공(0)에서 존재(1)의 탄생
# 이론: 시간의 흐름과 에너지(관측)가 확률을 높여 존재를 확정한다.

class Void:
    def __init__(self):
        self.state = 0  # 0: 무(None), 1: 유(Exist)
        self.time = 0
        self.history = []

    # 관측 시도 (에너지 투입)
    def observe(self, energy):
        self.time += 1
        
        # 존재 확률 공식: P = 1 - e^(-energy * time)
        # 시간이 지날수록, 에너지가 클수록 존재할 확률이 1에 가까워짐
        probability = 1 - math.exp(-energy * self.time)
        
        # 양자 도약 (Quantum Leap) 시뮬레이션
        random_value = random.random()
        is_materialized = random_value < probability

        if is_materialized and self.state == 0:
            self.state = 1
            print(f"[Time {self.time}] ✨ 존재 발생! (확률: {probability * 100:.4f}%, 난수: {random_value:.4f})")
        elif self.state == 0:
            print(f"[Time {self.time}] ...진공 상태 (확률: {probability * 100:.4f}%)")

        self.history.append({'time': self.time, 'probability': probability, 'state': self.state})
        return self.state

# 시뮬레이션 실행
universe = Void()
energy_input = 0.1  # 관측 에너지

print("--- 1차원 시뮬레이션 시작: 진공에서의 탄생 ---")

# 최대 50 시간 단위 동안 관측
for i in range(50):
    if universe.observe(energy_input) == 1:
        print("--- 시뮬레이션 종료: 존재 확정 ---")
        break

if universe.state == 0:
    print("--- 시뮬레이션 종료: 아직 존재하지 않음 (시간 부족) ---")
