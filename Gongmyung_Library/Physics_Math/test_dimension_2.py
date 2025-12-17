import math
import random

# 2차원 시뮬레이션: 공간(Matrix)과 형상(Pattern)의 형성
# 이론: 존재는 위치(Address)를 가짐으로써 서로 구별되며, 모여서 형상을 이룬다.

class Void:
    def __init__(self):
        self.time = 0

    def observe(self, energy):
        self.time += 1
        probability = 1 - math.exp(-energy * self.time)
        return random.random() < probability

class Plane2D:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.void_generator = Void()

    def evolve(self, energy, iterations):
        print(f"--- 2차원 시뮬레이션 시작: {self.width}x{self.height} 공간 ---")
        count = 0
        for _ in range(iterations):
            # 랜덤한 좌표 선택
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            # 해당 좌표의 진공 상태 관측
            if self.grid[y][x] == 0:
                if self.void_generator.observe(energy):
                    self.grid[y][x] = 1
                    count += 1
        
        print(f"--- 시뮬레이션 종료: 총 {count}개의 존재 생성 ---")
        self.render()

    def render(self):
        print("\n[Current State of the Universe]")
        for row in self.grid:
            print(' '.join(['●' if cell else '○' for cell in row]))

# 실행
# 10x10 크기의 우주 생성
universe = Plane2D(10, 10)
# 에너지 0.05로 50번의 관측 시도
universe.evolve(energy=0.05, iterations=50)
