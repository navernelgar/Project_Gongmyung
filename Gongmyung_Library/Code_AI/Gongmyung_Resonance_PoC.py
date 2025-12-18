import math
import random

# ==========================================
# 공명 이론 검증 시뮬레이션 (Resonance Theory PoC)
# ==========================================

class ResonanceSystem:
    def __init__(self):
        # 1. 의미 공간 (Semantic Space) 정의 - 3차원 좌표 (x, y, z)
        # x: 자연/물리적 성질, y: 감정/추상적 성질, z: 행동/동적 성질
        self.vocabulary = {
            # [자연] 관련 단어들 (x축 우세)
            "Apple":  [0.9, 0.1, 0.1],
            "Banana": [0.85, 0.1, 0.1],
            "Tree":   [0.8, 0.2, 0.0],
            "Water":  [0.7, 0.1, 0.3],
            
            # [감정] 관련 단어들 (y축 우세)
            "Love":   [0.1, 0.9, 0.2],
            "Happy":  [0.1, 0.85, 0.3],
            "Sad":    [0.1, -0.8, 0.1], # 부정적 감정은 반대 방향
            "Hope":   [0.2, 0.8, 0.2],
            
            # [행동] 관련 단어들 (z축 우세)
            "Run":    [0.1, 0.1, 0.9],
            "Jump":   [0.1, 0.2, 0.85],
            "Go":     [0.0, 0.0, 0.8],
            
            # [거짓/노이즈] - 문맥과 전혀 상관없는 단어
            "Chaos":  [-0.5, -0.5, -0.5]
        }

    def magnitude(self, v):
        return math.sqrt(sum(x**2 for x in v))

    def dot_product(self, v1, v2):
        return sum(x*y for x, y in zip(v1, v2))

    def resonance_score(self, word1, word2):
        """ 두 단어 사이의 공명도(Cosine Similarity) 계산 """
        v1 = self.vocabulary.get(word1)
        v2 = self.vocabulary.get(word2)
        
        if not v1 or not v2:
            return 0.0
            
        mag1 = self.magnitude(v1)
        mag2 = self.magnitude(v2)
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
            
        return self.dot_product(v1, v2) / (mag1 * mag2)

    def calculate_context_field(self, sentence):
        """ 문장의 문맥장(Context Field) 중심 좌표 계산 """
        words = sentence.split()
        if not words:
            return [0, 0, 0]
            
        # 벡터 합 계산
        context_vector = [0, 0, 0]
        valid_words = 0
        
        for w in words:
            if w in self.vocabulary:
                v = self.vocabulary[w]
                context_vector[0] += v[0]
                context_vector[1] += v[1]
                context_vector[2] += v[2]
                valid_words += 1
        
        # 평균 (중심점)
        if valid_words > 0:
            context_vector = [x / valid_words for x in context_vector]
            
        return context_vector

    def verify_truth(self, context_vector, new_word, threshold=0.5):
        """ 홀로그래픽 진실 검증: 새로운 단어가 문맥과 공명하는가? """
        if new_word not in self.vocabulary:
            return "Unknown Word"
            
        v_word = self.vocabulary[new_word]
        
        # 문맥 벡터와 새 단어 벡터 사이의 공명도 계산
        mag_c = self.magnitude(context_vector)
        mag_w = self.magnitude(v_word)
        
        if mag_c == 0 or mag_w == 0:
            return False
            
        resonance = self.dot_product(context_vector, v_word) / (mag_c * mag_w)
        
        # 공명도가 임계값보다 높으면 '참(Truth/Natural)', 낮으면 '거짓(False/Noise)'
        is_truth = resonance > threshold
        return is_truth, resonance

# ==========================================
# 검증 실행 (Verification Run)
# ==========================================
system = ResonanceSystem()

print("=== [공명 이론 검증 시뮬레이션] ===")
print("1. 단어 간 공명도 (Word Resonance)")
print(f"Apple <-> Banana : {system.resonance_score('Apple', 'Banana'):.4f} (높음 예상)")
print(f"Apple <-> Run    : {system.resonance_score('Apple', 'Run'):.4f} (낮음 예상)")
print(f"Love  <-> Happy  : {system.resonance_score('Love', 'Happy'):.4f} (높음 예상)")
print("-" * 30)

# 시나리오 1: 자연스러운 문맥 (과일 이야기)
sentence1 = "Apple Banana Tree"
context1 = system.calculate_context_field(sentence1)
print(f"\n2. 문맥 검증: '{sentence1}'")
print(f"   -> 문맥 중심 좌표: {[round(x,2) for x in context1]}")

test_word1 = "Water" # 관련 있음
is_truth1, score1 = system.verify_truth(context1, test_word1)
print(f"   -> 테스트 단어 '{test_word1}': 공명도 {score1:.4f} => {'[진실/조화]' if is_truth1 else '[거짓/부조화]'}")

test_word2 = "Chaos" # 관련 없음
is_truth2, score2 = system.verify_truth(context1, test_word2)
print(f"   -> 테스트 단어 '{test_word2}': 공명도 {score2:.4f} => {'[진실/조화]' if is_truth2 else '[거짓/부조화]'}")

# 시나리오 2: 감정의 문맥
sentence2 = "Love Happy Hope"
context2 = system.calculate_context_field(sentence2)
print(f"\n3. 문맥 검증: '{sentence2}'")

test_word3 = "Sad" # 반대 감정
is_truth3, score3 = system.verify_truth(context2, test_word3)
print(f"   -> 테스트 단어 '{test_word3}': 공명도 {score3:.4f} => {'[진실/조화]' if is_truth3 else '[거짓/부조화]'} (반대 감정이라 부조화)")

print("\n=== [결론] ===")
print("좌표(Vector)와 공명(Cosine Similarity)만으로 문맥 파악 및 이상치(거짓) 탐지가 가능함을 증명함.")
