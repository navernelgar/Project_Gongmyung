import math
import random

# 7차원 시뮬레이션: 군론(Group Theory)과 대칭성(Symmetry)
# 이론: 물질 입자들은 에너지 최소화를 위해 대칭적인 구조로 결합한다.

class Atom:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0

class MolecularSimulator:
    def __init__(self, num_atoms):
        self.atoms = []
        # 중앙 부근에 랜덤하게 원자 배치
        for i in range(num_atoms):
            x = random.uniform(4, 6)
            y = random.uniform(4, 6)
            self.atoms.append(Atom(i, x, y))

    def update(self):
        # 레너드-존스 포텐셜 (Lennard-Jones Potential) 유사 모델
        # 입자 간 인력과 척력을 계산하여 위치 업데이트
        dt = 0.1
        damping = 0.9 # 마찰 계수 (에너지 발산하여 안정화)

        for i, atom1 in enumerate(self.atoms):
            fx, fy = 0, 0
            for j, atom2 in enumerate(self.atoms):
                if i == j: continue
                
                dx = atom2.x - atom1.x
                dy = atom2.y - atom1.y
                dist = math.sqrt(dx**2 + dy**2)
                
                if dist < 0.1: dist = 0.1 # 0으로 나누기 방지
                
                # 힘 계산: 인력(Attraction) - 척력(Repulsion)
                # 거리가 1.0일 때 평형을 이루도록 설정
                force = (dist - 1.0) * 0.5 
                
                fx += force * (dx / dist)
                fy += force * (dy / dist)
            
            # 가속도 -> 속도 -> 위치
            atom1.vx = (atom1.vx + fx * dt) * damping
            atom1.vy = (atom1.vy + fy * dt) * damping
            
            atom1.x += atom1.vx * dt
            atom1.y += atom1.vy * dt

    def render(self):
        # 10x10 그리드에 시각화
        grid = [['·' for _ in range(10)] for _ in range(10)]
        
        for atom in self.atoms:
            gx = int(atom.x)
            gy = int(atom.y)
            if 0 <= gx < 10 and 0 <= gy < 10:
                grid[gy][gx] = '●'
        
        print("\n[Molecular Structure]")
        for row in grid:
            print(' '.join(row))
            
    def get_positions(self):
        return [(atom.x, atom.y) for atom in self.atoms]

# 실행
print("--- 7차원 시뮬레이션 시작: 대칭적 구조 형성 ---")
# 3개의 원자로 시작 (삼각형 예상)
sim = MolecularSimulator(num_atoms=3)

print("초기 상태 (Random):")
sim.render()

# 50 프레임 동안 물리 엔진 가동 (안정화)
for _ in range(50):
    sim.update()

print("최종 상태 (Stabilized):")
sim.render()

# 좌표 출력하여 대칭성 확인
positions = sim.get_positions()
print("\n최종 좌표:")
for i, pos in enumerate(positions):
    print(f"Atom {i}: ({pos[0]:.2f}, {pos[1]:.2f})")

# 거리 계산
d01 = math.sqrt((positions[0][0]-positions[1][0])**2 + (positions[0][1]-positions[1][1])**2)
d12 = math.sqrt((positions[1][0]-positions[2][0])**2 + (positions[1][1]-positions[2][1])**2)
d20 = math.sqrt((positions[2][0]-positions[0][0])**2 + (positions[2][1]-positions[0][1])**2)
print(f"\n원자 간 거리: {d01:.2f}, {d12:.2f}, {d20:.2f}")
print("결론: 거리가 거의 균일하면 정삼각형(대칭 구조)을 이룬 것이다.")
