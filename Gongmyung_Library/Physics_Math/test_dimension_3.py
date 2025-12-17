import math
import random

# 3차원 시뮬레이션: 입체(Volume)와 구조(Structure)의 형성
# 이론: 2차원 평면이 적층되어 3차원 공간을 형성하며, 깊이(Depth)를 가진다.

class Void:
    def __init__(self):
        self.time = 0

    def observe(self, energy):
        self.time += 1
        probability = 1 - math.exp(-energy * self.time)
        return random.random() < probability

class Space3D:
    def __init__(self, size):
        self.size = size
        # 3차원 복셀 그리드: [z][y][x]
        self.voxels = [[[0 for _ in range(size)] for _ in range(size)] for _ in range(size)]
        self.void_generator = Void()

    def evolve(self, energy, iterations_per_layer):
        print(f"--- 3차원 시뮬레이션 시작: {self.size}x{self.size}x{self.size} 큐브 ---")
        total_particles = 0
        
        # 각 층(Layer)마다 독립적인 2차원 시뮬레이션 수행 후 적층
        for z in range(self.size):
            layer_particles = 0
            # 각 층은 시간의 흐름을 공유하거나 독립적일 수 있음. 여기서는 독립적 사건의 적층으로 가정.
            # 하지만 Void의 시간은 계속 흐른다고 가정하면 위층으로 갈수록 존재 확률이 높아질 수 있음.
            # 여기서는 층별로 균일한 확률 분포를 보기 위해 Void 시간을 리셋하거나 유지할 수 있는데,
            # "쌓인다"는 개념을 위해 아래층부터 순차적으로 생성된다고 가정.
            
            for _ in range(iterations_per_layer):
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
                
                if self.voxels[z][y][x] == 0:
                    if self.void_generator.observe(energy):
                        self.voxels[z][y][x] = 1
                        layer_particles += 1
            
            total_particles += layer_particles
            # print(f"Layer {z}: {layer_particles} particles created.")

        print(f"--- 시뮬레이션 종료: 총 {total_particles}개의 입자 생성 ---")
        self.analyze_structure()

    def analyze_structure(self):
        # 밀도 계산
        total_volume = self.size ** 3
        active_voxels = sum(sum(sum(row) for row in layer) for layer in self.voxels)
        density = active_voxels / total_volume
        print(f"전체 밀도(Density): {density:.4f}")

        # 중심부 단면(Cross-section) 시각화 (z = size // 2)
        mid_z = self.size // 2
        print(f"\n[Cross-section at Z={mid_z}]")
        for row in self.voxels[mid_z]:
            print(' '.join(['●' if cell else '○' for cell in row]))

# 실행
# 10x10x10 크기의 우주 생성
universe = Space3D(10)
# 각 층마다 에너지 0.05로 20번의 관측 시도
universe.evolve(energy=0.05, iterations_per_layer=20)
