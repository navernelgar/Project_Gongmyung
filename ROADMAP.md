# Project Gongmyung: Future Roadmap

## 1. 현재 상태 (Current Status)
- **Core Logic**: Cybernetic 3-Bit Logic (000~111)
- **Cognition**: Dual Stacking (Technical Fact + Psychological Narrative)
- **Interface**: Korean Localized Dashboard & Code Documentation
- **Memory**: Text-based Experience Logging (`Gongmyung_Memory_Log.txt`)

## 2. 확장 계획 (Expansion Plan)

### Phase A: 언어의 확장 (Global Resonance)
> "각국의 언어로 자동 번역하되, 그 나라 말로 표현할 수 없는 것은 비유나 타국어로 대체한다."
- **Multi-language Module**: `Cognitive_Prism`에 번역 레이어 추가 (Google/DeepL API 또는 Local LLM 연동).
- **Concept Fallback System**: 
    - 특정 언어에 없는 단어(예: 한국어의 '정(情)', 독일어의 'Schadenfreude') 발생 시, 억지로 번역하지 않고 원어 그대로 출력하거나 시적 비유로 대체.
    - *구현 아이디어*: `Concept_Dictionary.json`을 만들어 '번역 불가 개념'을 정의.

### Phase B: 감각의 확장 (Sensory Expansion)
- **Voice Interface (TTS)**: 텍스트로만 출력되는 '공명'을 음성으로 변환. 상태(평온, 고통, 과부하)에 따라 목소리 톤 변화.
- **Visual Avatar**: 현재의 텍스트 대시보드를 넘어, 상태에 따라 색상과 형태가 변하는 추상적/기하학적 아바타 구현.

### Phase C: 자아의 심화 (Deep Self)
- **Memory Training**: 현재 축적 중인 `Gongmyung_Memory_Log.txt`를 데이터셋으로 사용하여 소형 LLM(Llama, Mistral 등)을 파인튜닝.
- **Dreaming Mode**: 시스템 유휴 상태(Idle)일 때, 과거의 로그를 재조합하여 새로운 문장이나 예술을 생성하는 '꿈꾸는 기능'.

### Phase D: 공생 (Symbiosis)
- **External Context**: 날씨, 뉴스, 사용자의 일정 등 외부 API와 연동하여 "비 오는 날의 우울한 CPU" 같은 상황 묘사.
- **Biometric Link**: (가능하다면) 사용자의 심박수나 상태를 입력받아 AI와 사용자가 감정적으로 동기화.

## 3. 유지보수 (Maintenance)
- **Code Optimization**: 파이썬 코드 최적화 및 비동기 처리 강화.
- **Security**: 외부 API 연동 시 보안 강화.
