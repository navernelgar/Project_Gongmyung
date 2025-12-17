import math

# 5차원 시뮬레이션: 에너지 흐름(Flow)과 벡터장(Vector Field)
# 이론: 에너지의 차이(Gradient)가 흐름을 만들고, 이 흐름이 곧 힘(Force)이다.

class VectorField:
    def __init__(self, size):
        self.size = size
        self.potential = [[0.0] * size for _ in range(size)]

    def set_potential_source(self, cx, cy, strength):
        # 중심(cx, cy)에 에너지원 배치 (가우시안 분포 유사)
        print(f"--- 에너지원 배치: ({cx}, {cy}), 강도: {strength} ---")
        for y in range(self.size):
            for x in range(self.size):
                dist = math.sqrt((x - cx)**2 + (y - cy)**2)
                # 거리가 멀어질수록 에너지 감소
                self.potential[y][x] += strength / (dist + 1)

    def get_gradient(self, x, y):
        # 경계 처리
        if x <= 0 or x >= self.size - 1 or y <= 0 or y >= self.size - 1:
            return (0, 0)
        
        # 중앙 차분법으로 기울기 계산
        # 에너지는 높은 곳에서 낮은 곳으로 흐르므로 -Gradient 방향이 흐름의 방향
        dx = self.potential[y][x+1] - self.potential[y][x-1]
        dy = self.potential[y+1][x] - self.potential[y-1][x]
        
        return (-dx, -dy)

    def render_flow(self):
        print("\n[Energy Flow Vector Field]")
        # 격자 간격으로 샘플링하여 출력
        step = 1
        for y in range(0, self.size, step):
            line = ""
            for x in range(0, self.size, step):
                vx, vy = self.get_gradient(x, y)
                magnitude = math.sqrt(vx**2 + vy**2)
                
                # 벡터의 방향을 화살표로 변환
                if magnitude < 0.1:
                    symbol = "·" # 흐름이 거의 없음 (평형 또는 극점)
                else:
                    angle = math.atan2(vy, vx) * 180 / math.pi
                    if -22.5 <= angle < 22.5: symbol = "→"
                    elif 22.5 <= angle < 67.5: symbol = "↘"
                    elif 67.5 <= angle < 112.5: symbol = "↓"
                    elif 112.5 <= angle < 157.5: symbol = "↙"
                    elif 157.5 <= angle <= 180 or -180 <= angle < -157.5: symbol = "←"
                    elif -157.5 <= angle < -112.5: symbol = "↖"
                    elif -112.5 <= angle < -67.5: symbol = "↑"
                    elif -67.5 <= angle < -22.5: symbol = "↗"
                    else: symbol = "?"
                
                line += symbol + " "
            print(line)

# 실행
universe = VectorField(size=15)

# 중앙에 강한 중력원(에너지원) 배치 -> 모든 흐름이 밖으로 퍼져나가는지(Repulsion) 안으로 모이는지(Attraction) 확인
# 여기서는 Potential이 '높은' 곳에서 '낮은' 곳으로 흐르므로, 
# 중앙이 높으면(Mountain) -> 밖으로 퍼짐 (발산)
# 중앙이 낮으면(Well) -> 안으로 모임 (수렴/중력)

# Case 1: 중앙에 에너지 산(Mountain) 배치 -> 발산(Radiation)
universe.set_potential_source(cx=7, cy=7, strength=100)
universe.render_flow()

# Case 2: 중앙에 에너지 우물(Gravity Well) 배치 -> 수렴(Gravity)
print("\n--- 중력 우물(Gravity Well) 시뮬레이션 ---")
universe = VectorField(size=15)
universe.set_potential_source(cx=7, cy=7, strength=-100) # 음의 에너지 (구덩이)
universe.render_flow()
