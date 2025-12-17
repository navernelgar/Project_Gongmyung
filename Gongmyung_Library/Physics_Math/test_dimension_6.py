import random
import time

# 6차원 시뮬레이션: 위상수학적 상전이(Phase Transition)와 물질화(Materialization)
# 이론: 에너지가 임계점을 넘으면 응축되어 물질(Mass)이 된다. (E = mc^2)

class Materializer:
    def __init__(self, size, critical_energy):
        self.size = size
        self.critical_energy = critical_energy
        self.energy_grid = [[0.0] * size for _ in range(size)]
        self.matter_grid = [[0] * size for _ in range(size)] # 0: 진공, 1: 물질

    def inject_energy(self, x, y, amount):
        # 에너지 주입 (에너지 보존 법칙에 따라 누적됨)
        self.energy_grid[y][x] += amount
        
        # 상전이 체크: 에너지가 임계점을 넘었는가?
        if self.energy_grid[y][x] >= self.critical_energy:
            if self.matter_grid[y][x] == 0:
                self.matter_grid[y][x] = 1 # 물질 생성!
                # 물질이 되면 에너지는 질량으로 변환되어 고정됨 (여기서는 에너지 리셋 대신 상태 변경만 표시)
                return True, self.energy_grid[y][x]
        return False, self.energy_grid[y][x]

    def render(self):
        print(f"\n[Universe State] (Critical Energy: {self.critical_energy})")
        for y in range(self.size):
            line = ""
            for x in range(self.size):
                if self.matter_grid[y][x] == 1:
                    line += "■ " # 물질 (Matter)
                else:
                    # 에너지 레벨에 따른 시각화
                    energy = self.energy_grid[y][x]
                    if energy < 10: line += "· "
                    elif energy < 30: line += "░ "
                    elif energy < 60: line += "▒ "
                    elif energy < 90: line += "▓ "
                    else: line += "█ " # 임계점 직전
            print(line)

# 실행
print("--- 6차원 시뮬레이션 시작: 에너지 응축과 물질 생성 ---")
universe = Materializer(size=10, critical_energy=100.0)

# 랜덤한 위치에 지속적으로 에너지 주입 (우주 배경 복사 또는 에너지 요동)
# 중앙 부근에 더 많은 에너지가 모이도록 설정 (중력 렌즈 효과 등 가정)

for t in range(1, 21): # 20 시간 단위 동안 진행
    print(f"\n--- Time {t} ---")
    
    # 5번의 에너지 주입 시도
    for _ in range(5):
        # 정규 분포를 사용하여 중앙(5,5)에 집중적으로 에너지 투입
        rx = int(random.gauss(5, 2))
        ry = int(random.gauss(5, 2))
        
        # 좌표 범위 제한
        rx = max(0, min(9, rx))
        ry = max(0, min(9, ry))
        
        # 에너지 주입 (랜덤 양 10~30)
        amount = random.uniform(10, 30)
        is_born, current_energy = universe.inject_energy(rx, ry, amount)
        
        if is_born:
            print(f"✨ [EVENT] 좌표 ({rx}, {ry})에서 물질 생성! (Energy: {current_energy:.2f})")
            
    universe.render()
    # time.sleep(0.5)
