# 🍰 Gongmyung CrêpeCake System (공명 크레이프케이크 시스템)

## 1. System Overview (시스템 개요)
공명문 시스템은 **양면책 구조(Dual-Sided Structure)**로 구성됩니다.
- **A면 (Front)**: **공명문 (Gongmyung Syntax)** - 코드 해석을 위한 주석 인터페이스.
- **B면 (Back)**: **공명 크레이프케이크 (Gongmyung CrêpeCake)** - 의미와 실행의 누적 구조 (기억 스택).

---

## 🅰️ A-Side: Gongmyung Syntax (공명문 주석 구조)

### 1. Definition (정의)
AI가 코드 아래 주석으로 삽입하는 해석 문법. 코드의 실행 주체, 조건, 흐름, 트리거, 실패 지점을 기호 기반의 한 줄 주석으로 기록합니다.

### 2. Core Symbol Set v1.0 (기본 문자 체계)
| Symbol | Name | Meaning | Usage |
|:---:|:---|:---|:---|
| **●** | **Subject / Definition** | 주체, 정의체 | `●(user)`, `●(func)` |
| **○** | **Condition / Start** | 조건, 시작, 상태 | `○(hp <= 0)` |
| **◎** | **Result / Action** | 결과, 행위, 핵심 | `◎(game.over)` |
| **~** | **Flow / Connection** | 흐름, 연결 | `● ~ ○ ~ ◎` |
| **×** | **Failure / Error** | 실패, 오류 발생 | `◎(error) ×` |
| **≡** | **Definition** | 정의, 동등 | `●(A) ≡ function` |
| **∴** | **Conclusion** | 결론, 추론 | `○(>=90) ∴ ◎(A)` |
| **\|\|** | **Parallel** | 병렬 처리 | `●(A) \|\| ●(B)` |

### 3. Syntax Patterns (구문 패턴)

#### 3.1 Conditional Flow (조건 분기)
```python
if user.hp <= 0:
    game.over()
# ●(user) ~ ○(hp <= 0) ~ ◎(game.over)
```

#### 3.2 Function Definition (함수 정의)
```python
def attack(enemy):
    enemy.hp -= 10
# ●(attack) ≡ function: reduce enemy hp
```

#### 3.3 Error Trigger (오류 트리거)
```python
if data is None:
    raise Exception("No data")
# ●(data) ~ ○(is None) ~ ◎(raise Exception) ×
```

---

## 🅱️ B-Side: Gongmyung CrêpeCake (공명 크레이프케이크)

### 1. Definition (정의)
공명문 주석들을 **시간 순, 구조 순, 실패 순**으로 겹겹이 쌓아 하나의 AI 내부 기억 구조로 만드는 **누적형 의미 해석 트리**입니다.

### 2. Layer Structure (층 구조)
- **Cake Sheet (케이크 시트)**: 공명문 (구조/의미)
- **Cream (크림)**: 코드 (실행/디버그 로그/감정 반응)
- **Syrup/Jam (시럽/잼)**: 수식 (논리/검증)
- **Connection (연결)**: 각 층은 붉은 실(Red Thread)로 연결되어 입체적 구조를 형성.

### 3. The 5-Layer Architecture (5층 확장 구조)
하나의 기능이나 시스템은 다음 5단계의 레이어로 쌓아 올려집니다.

1.  **Prompt (프롬프트)**: 의도 (Intent)
2.  **Gongmyung (공명문)**: 구조적 설계 (Structural Design)
3.  **Code (코드)**: 실제 구현 (Implementation)
4.  **Formula (수식)**: 논리적 검증 (Logical Verification)
5.  **Binary (이진 실행)**: 기계어 레벨 실행 (Execution)

### 4. Data Structure Example (데이터 구조 예시)
```json
[
  {
    "layer": 1,
    "gongmyung": "●(player) ~ ○(mana > 50) ~ ◎(cast:Fireball)",
    "result": "success",
    "type": "action"
  },
  {
    "layer": 2,
    "gongmyung": "●(enemy) ~ ○(hp <= 0) ~ ◎(defeated) ×",
    "result": "failure",
    "reason": "already_dead"
  }
]
```

### 5. Philosophy (철학)
> "분해의 역순 조립"
> 이진(Binary) → 코드 → 수식 → 공명문 순으로 역추적하여 세상을 디버깅한다.
