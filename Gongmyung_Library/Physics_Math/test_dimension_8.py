import math

# 8차원 시뮬레이션: 텐서 미적분(Tensor Calculus)과 중력장(Gravity Field)
# 이론: 질량은 시공간을 휘게 하며, 이 곡률(Curvature)이 곧 중력이다.

class SpacetimeGrid:
    def __init__(self, size):
        self.size = size
        # 2차원 평면이지만, 각 점은 '깊이(Depth)' 값을 가짐 (z축 왜곡)
        self.grid = [[0.0] * size for _ in range(size)]

    def apply_mass(self, mx, my, mass):
        print(f"--- 질량 배치: 좌표({mx}, {my}), 질량 {mass} ---")
        # 질량에 의한 공간 왜곡 계산 (중력 퍼텐셜 우물)
        # z = -GM / r
        for y in range(self.size):
            for x in range(self.size):
                # 유클리드 거리 계산
                dist = math.sqrt((x - mx)**2 + (y - my)**2)
                
                # 특이점(Singularity) 방지 및 부드러운 곡선 처리
                # dist가 0에 가까우면 무한대로 발산하므로 최소 거리 보정
                effective_dist = math.sqrt(dist**2 + 1.0) 
                
                # 공간이 아래로 휘어짐 (음수 값 누적)
                self.grid[y][x] -= mass / effective_dist

    def render_curvature(self):
        print("\n[Spacetime Curvature Visualization]")
        # 등고선(Contour) 방식으로 시각화
        # 깊이가 깊을수록(값이 작을수록) 더 진한 문자 사용
        
        # 값의 범위 확인
        min_val = min(min(row) for row in self.grid)
        max_val = max(max(row) for row in self.grid)
        
        print(f"Min Depth: {min_val:.2f}, Max Depth: {max_val:.2f}")

        for row in self.grid:
            line = ""
            for val in row:
                # 정규화 (0.0 ~ 1.0)
                if max_val == min_val:
                    norm = 0
                else:
                    norm = (val - min_val) / (max_val - min_val)
                
                # 시각화 문자 매핑 (깊은 곳 -> 얕은 곳)
                # @ (가장 깊음/중심) -> % -> # -> * -> + -> = -> - -> . (평평함)
                if norm < 0.1: char = "@"
                elif norm < 0.2: char = "%"
                elif norm < 0.3: char = "#"
                elif norm < 0.4: char = "*"
                elif norm < 0.5: char = "+"
                elif norm < 0.6: char = "="
                elif norm < 0.7: char = "-"
                elif norm < 0.9: char = "."
                else: char = " " # 거의 평평함
                
                line += char + " "
            print(line)

    def probe_path(self, start_x, start_y, vx, vy):
        # 휘어진 공간을 지나는 입자의 경로 추적 (측지선, Geodesic)
        # 단순화: 기울기(Gradient)가 가속도로 작용
        print(f"\n--- 입자 이동 경로 추적 (Start: {start_x}, {start_y}) ---")
        
        x, y = float(start_x), float(start_y)
        path = []
        
        for t in range(15):
            path.append((round(x), round(y)))
            
            # 현재 위치의 기울기(Gradient) 계산 = 중력 가속도
            ix, iy = int(x), int(y)
            if 0 < ix < self.size-1 and 0 < iy < self.size-1:
                # x축 기울기
                gx = (self.grid[iy][ix+1] - self.grid[iy][ix-1]) / 2.0
                # y축 기울기
                gy = (self.grid[iy+1][ix] - self.grid[iy-1][ix]) / 2.0
                
                # 가속도는 기울기의 반대 방향 (낮은 곳으로)이지만, 
                # 여기서는 grid 값이 이미 음수(깊이)이므로, 값이 더 작은 쪽(더 깊은 쪽)으로 힘을 받음.
                # grid[x+1] > grid[x-1] 이면 오른쪽이 더 높음 -> 왼쪽으로 힘 받음.
                # 즉, Gradient 방향(오르막)의 반대 방향.
                
                # 더 정확히는 퍼텐셜 U = grid 값. 힘 F = -grad U.
                # gx = dU/dx. Fx = -gx.
                # 하지만 위에서 grid를 -mass/r 로 정의했으므로(음수), 
                # 중심부로 갈수록 값이 작아짐(-100 < -10).
                # 기울기는 낮은 곳에서 높은 곳으로 향함.
                # 입자는 높은 곳(0)에서 낮은 곳(-100)으로 굴러떨어져야 함.
                # 따라서 기울기(Gradient) 방향으로 가속됨 (값이 커지는 방향? 아니면 작아지는 방향?)
                
                # 예: 중심(-100), 오른쪽(-10). 기울기 = (-10 - (-100)) > 0. 양수.
                # 입자는 중심(-100) 쪽으로 가야 함(왼쪽, 음수 방향).
                # 따라서 가속도는 -Gradient.
                
                ax = gx * 5.0 # 가속도 증폭 상수
                ay = gy * 5.0
                
                vx += ax
                vy += ay
            
            x += vx
            y += vy
            
            # 경계 체크
            if not (0 <= x < self.size and 0 <= y < self.size):
                break
                
        # 경로 시각화
        print("Path:", path)
        
        # 그리드에 경로 오버레이
        print("\n[Particle Path Visualization]")
        for r in range(self.size):
            line = ""
            for c in range(self.size):
                if (c, r) in path:
                    line += "o "
                else:
                    # 배경은 단순화
                    if self.grid[r][c] < -5.0: line += ". "
                    else: line += "  "
            print(line)


# 실행
universe = SpacetimeGrid(size=20)

# 1. 질량 배치 (중력 우물 생성)
universe.apply_mass(mx=10, my=10, mass=50.0)

# 2. 공간 곡률 시각화
universe.render_curvature()

# 3. 입자 이동 (중력 렌즈 효과 / 궤도)
# (2, 5)에서 시작하여 오른쪽으로 진행하던 입자가 중력에 의해 휘어지는지 확인
universe.probe_path(start_x=2, start_y=5, vx=1.0, vy=0.0)
