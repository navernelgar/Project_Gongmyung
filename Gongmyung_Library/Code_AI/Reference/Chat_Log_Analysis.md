# 📝 Project Gongmyung: AI 작업 승계 및 학습 가이드 (Annotations)

**작성일:** 2025년 12월 11일
**작성자:** GitHub Copilot (Project Gongmyung AI Assistant)
**참조 문서:** `D:\Project_Gongmyung\Gongmyung_Library\Chat_History_Full.md`

---

## 1. 개요 (Overview)
본 문서는 **Project Gongmyung**의 개발 과정에서 발생한 주요 이슈, 의사결정 과정, 그리고 시행착오를 기록한 **AI 학습용 주석(Annotation)** 모음집입니다. 
이후 작업을 이어받을 AI 에이전트나 개발자는 이 문서를 통해 프로젝트의 맥락(Context)을 빠르게 파악하고, 동일한 실수를 반복하지 않도록 해야 합니다.

---

## 2. 주요 학습 포인트 및 주석 (Key Learnings & Annotations)

### 2.1. 초기 환경 설정 및 도구 적응 (Session: e1d80979...)
*   **상황:** 사용자가 처음 VS Code와 Copilot 환경에 적응하며, Python 및 확장 프로그램 설치를 요청함.
*   **이슈:** `pip` 명령어가 인식되지 않는 `CommandNotFoundException` 발생.
*   **원인:** Python이 설치되어 있었으나, 환경 변수(PATH) 설정이 제대로 되지 않았거나 쉘이 갱신되지 않음.
*   **💡 AI 주석:** 
    > "사용자의 로컬 환경(Windows PowerShell)은 Python/Node.js 등의 경로 설정이 불안정할 수 있음. 명령어가 실패할 경우, 단순히 재시도를 하기보다 `python -m pip`와 같이 **절대 경로**나 **모듈 실행 방식**을 우선 제안하는 것이 안정적임."

### 2.2. 프로젝트 구조화 및 파일 정리 (Session: 3a86f180...)
*   **상황:** C, D, E 드라이브에 흩어진 파일들을 `D:\Project_Gongmyung`으로 통합 요청.
*   **이슈:** 초기에 AI가 '현재 열린 폴더'만 작업 범위로 인식하여 사용자의 의도("전체 드라이브 정리")를 파악하지 못함.
*   **💡 AI 주석:** 
    > "사용자의 요청이 '정리해줘'와 같이 포괄적일 때, 반드시 **작업 범위(Scope)**가 워크스페이스 내부인지, 시스템 전체인지 먼저 확인해야 함. 특히 파일 이동 작업은 데이터 손실 위험이 있으므로, `Move-Item` 사용 시 신중해야 하며 백업 절차를 고려해야 함."

### 2.3. 서버 구축 및 언어 전환 (Session: 3a86f180...)
*   **상황:** Node.js 기반 `server.js` 실행 시도 중 `node` 명령어 인식 불가 문제 발생.
*   **해결:** 즉시 가용한 Python 환경(`server.py`)으로 전환하여 서비스 복구.
*   **💡 AI 주석:** 
    > "개발 환경의 불확실성(Node.js 미설치 등)에 대비해, **대체 가능한 기술 스택(Fallback Plan)**을 항상 준비해야 함. 본 프로젝트에서는 Python이 더 안정적인 런타임으로 확인되었으므로, 향후 스크립트 작성 시 Python을 우선순위로 둠."

### 2.4. 데이터 파싱 및 대화 로그 분석
*   **상황:** 10만 줄 이상의 대화 로그(`json`)를 분석하여 학습 목차 생성 요청.
*   **접근:** 전체 파일을 직접 읽는 것은 비효율적이므로, 파싱 스크립트(`parse_all_chats.py`)를 제작하여 Markdown으로 변환 후 분석.
*   **💡 AI 주석:** 
    > "대용량 데이터 처리 시, AI가 직접 읽으려 하기보다 **도구(Script)를 생성하여 데이터를 가공**하는 것이 훨씬 효율적임. 또한, 결과물은 사람이 읽기 쉬운 포맷(Markdown)으로 저장하여 문서화(Documentation)의 가치를 높여야 함."

---

## 3. 시스템 아키텍처 및 규칙 (System Architecture & Rules)

### 3.1. 폴더 구조 (Directory Structure)
*   **`Core_System`**: 웹 서버 및 핵심 로직 (`server.py`, `public/`)
*   **`Gongmyung_Library`**: 지식 저장소 및 데이터 아카이브
*   **`Workshop`**: 유지보수용 스크립트 및 도구 모음 (`parse_chat.py` 등)
*   **`Warehouse`**: 원본 데이터 및 백업 파일 보관소

### 3.2. 코딩 컨벤션 (Coding Conventions)
*   **언어:** Python 3.x (주력), PowerShell (시스템 제어)
*   **경로:** Windows 환경을 고려하여 `os.path.join` 또는 Raw String(`r"..."`) 사용 필수.
*   **인코딩:** 한글 처리를 위해 모든 파일 입출력 시 `encoding='utf-8'` 명시.

---

## 4. 향후 과제 (Future Tasks)
1.  **Node.js 환경 복구:** 장기적으로 웹 생태계 확장을 위해 Node.js 경로 설정 및 패키지 관리 복구 필요.
2.  **자동화 스크립트 고도화:** `Workshop` 폴더 내의 스크립트들을 메뉴화하여 쉽게 실행할 수 있도록 개선.
3.  **지식 베이스 확장:** `Gongmyung_Library`에 축적된 데이터를 검색 가능하도록 인덱싱 시스템 도입 고려.

---
*이 문서는 Project Gongmyung의 AI 에이전트가 작업을 수행할 때 가장 먼저 참고해야 할 지침서입니다.*
