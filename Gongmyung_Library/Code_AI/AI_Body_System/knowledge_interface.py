import random
import webbrowser
import subprocess
import json
import time
import os
import datetime
import pyautogui
import pyperclip
import requests
import io
import base64
from PIL import ImageGrab


class KnowledgeInterface:
    """
    [지식 인터페이스: Knowledge Interface]
    외부의 거대 AI(Gemini, GPT 등)와 연결하여
    공명 시스템이 모르는 패턴(Unknown Pattern)의 의미를 물어보는 기관.
    """

    def __init__(self):
        # 절대 경로로 설정 파일 지정 (실행 위치에 따른 오류 방지)
        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brain_config.json")
        self.config = self._load_config()
        self.last_browser_call_time = 0  # 쿨타임 관리를 위한 타임스탬프
        self.browser_cooldown = 1        # 1초 쿨타임 (테스트용)

        # 선천적 지식 (Innate Knowledge) - 시뮬레이션용 데이터
        # 실제로는 여기서 외부 API를 호출하여 이미지를 분석하고 의미를 가져옵니다.
        self.innate_dictionary = {
            "High_CPU": ["고강도 연산 중", "렌더링 작업", "복잡한 계산 수행", "시스템 과부하"],
            "Low_CPU": ["대기 상태", "유휴 모드", "사용자 입력 대기", "평화로운 상태"],
            "High_RAM": ["메모리 누수 의심", "대용량 데이터 로드", "무거운 프로그램 실행"],
            "YouTube_Pattern": ["영상 시청 중", "스트리밍 서비스 이용", "멀티미디어 소비"],
            "Coding_Pattern": ["코드 작성 중", "개발 환경 활성화", "디버깅 수행"],
            "Gaming_Pattern": ["게임 플레이 중", "그래픽 리소스 집중", "엔터테인먼트 모드"]
        }

    def _load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (OSError, json.JSONDecodeError):
                print("[KnowledgeInterface] ⚠️ 설정 파일 로드 실패. 기본값(API)을 사용합니다.")
                return {"brain_mode": "api"} # 기본값을 API로 변경 (안전장치)
        print("[KnowledgeInterface] ⚠️ 설정 파일 없음. 기본값(API)을 사용합니다.")
        return {"brain_mode": "api"} # 기본값을 API로 변경 (안전장치)

    def ask_meaning(self, hex_code, metrics):
        """
        미지의 패턴(Hex Code)과 현재 상태(Metrics)를 기반으로
        외부 AI에게 그 의미를 추론해달라고 요청합니다.
        """
        # 설정에 따라 동작 방식 결정
        mode = self.config.get("brain_mode", "browser")

        # 1. API 모드인 경우 (미래 확장)
        if mode == "api":
            api_key = self.config.get("api_keys", {}).get("gemini", "")
            if api_key:
                return self._consult_api(hex_code, metrics, api_key)
            print("[KnowledgeInterface] API 키가 없습니다. 브라우저 모드로 전환합니다.")
            # Fallback to browser logic below

        # 2. 기존 로직 (Innate Dictionary + Browser)
        cpu = metrics.get("cpu", 0)
        ram = metrics.get("ram", 0)
        active_process = metrics.get("active_process", {}).get("name", "")

        result = "새로운 패턴 (분석 필요)"

        # 1. 프로세스 이름 기반 추론 (가장 강력한 단서)
        if "Code" in active_process or "python" in active_process:
            result = "개발/코딩 작업"
        elif "Chrome" in active_process or "Edge" in active_process:
            result = "웹 브라우징 (동영상/무거운 작업)" if cpu > 30 else "웹 서핑 / 정보 검색"
        elif "Game" in active_process or "Unity" in active_process:
            result = "게임 / 3D 작업"
        else:
            # 2. 하드웨어 상태 기반 추론 (보조 단서)
            context = []
            if cpu > 70:
                context.append("High_CPU")
            elif cpu < 10:
                context.append("Low_CPU")

            if ram > 80:
                context.append("High_RAM")

            # 3. 의미 생성 (Simulation)
            if context:
                key = context[0]
                meaning = random.choice(
                    self.innate_dictionary.get(
                        key, ["알 수 없는 작업"]))
                result = f"{meaning} (추정)"

        return result

    def _consult_api(self, hex_code, metrics, api_key):
        """
        [Node.js Bridge] 로컬 Node.js 서버(localhost:3000)로 요청을 보냅니다.
        """
        try:
            print(f"[KnowledgeInterface] 🧠 Node.js AI 서버 호출 중...")
            
            # 1. 화면 캡처 및 파일 저장 (Vision Memory)
            image_data = None
            vision_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Memory_Vision")
            if not os.path.exists(vision_dir):
                os.makedirs(vision_dir)

            # 파일명 생성 (타임스탬프)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"Vision_{timestamp}.png"
            image_path = os.path.join(vision_dir, image_filename)

            try:
                # 캡처 및 저장
                screenshot = ImageGrab.grab()
                screenshot.save(image_path, format="PNG")
                print(f"[KnowledgeInterface] 📸 화면 캡처 저장됨: {image_filename}")

                # Base64 인코딩 (전송용)
                with open(image_path, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')
                
                # [Vision Lifecycle] 오래된 이미지 정리 (최근 10장만 유지)
                self._cleanup_vision_memory(vision_dir, keep_count=10)

            except Exception as e:
                print(f"[KnowledgeInterface] ⚠️ 화면 캡처 실패: {e}")

            # 2. 프롬프트 구성
            prompt = f"""
            [시스템 상태 분석]
            - Hex Code: {hex_code}
            - CPU: {metrics.get('cpu')}%
            - RAM: {metrics.get('ram')}%
            - Process: {metrics.get('active_process', {}).get('name')}
            
            첨부된 화면(스크린샷)과 위의 시스템 상태를 보고, 
            현재 사용자가 무엇을 하고 있는지 '한글로 한 문장만' 명확하게 답변해줘.
            (예: '유튜브에서 코딩 강의를 시청하고 있습니다.', '고사양 게임을 플레이 중입니다.')
            """

            # 3. Node.js 서버로 요청 전송
            payload = {
                "prompt": prompt,
                "image": image_data
            }
            
            # 타임아웃 30초 설정
            response = requests.post("http://localhost:3000/analyze", json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get("text", "응답 없음")
                print(f"[KnowledgeInterface] 💡 Node.js 답변: {answer}")
                return answer
            else:
                print(f"[KnowledgeInterface] ❌ Node.js 서버 오류: {response.status_code} - {response.text}")
                return f"서버 오류 ({response.status_code})"

        except Exception as e:
            print(f"[KnowledgeInterface] ❌ 연결 오류: {e}")
            return "AI 서버 연결 실패"

    def _cleanup_vision_memory(self, directory, keep_count=10):
        """
        [Vision Lifecycle] 이미지 보관 정책
        - 지정된 개수(keep_count)를 초과하면 오래된 순서대로 삭제합니다.
        """
        try:
            files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".png")]
            files.sort(key=os.path.getctime) # 생성 시간순 정렬

            if len(files) > keep_count:
                remove_count = len(files) - keep_count
                for i in range(remove_count):
                    os.remove(files[i])
                    print(f"[KnowledgeInterface] 🗑️ 오래된 기억(이미지) 파기: {os.path.basename(files[i])}")
        except Exception as e:
            print(f"[KnowledgeInterface] ⚠️ 이미지 정리 중 오류: {e}")

    def consult_internet_via_browser(self, hex_code, metrics):
        """
        [사용자 요청 기능: 완전 자동화]
        API 키 없이, 브라우저를 직접 열고 마우스/키보드를 제어하여 질문합니다.
        """
        # API 모드이면 브라우저 제어 생략
        if self.config.get("brain_mode") == "api":
            return "API 모드 사용 중 (브라우저 제어 생략)"

        # 쿨타임 체크
        current_time = time.time()
        elapsed = current_time - self.last_browser_call_time
        if elapsed < self.browser_cooldown:
            print(f"[KnowledgeInterface] ⏳ 브라우저 쿨타임 중... ({int(self.browser_cooldown - elapsed)}초 남음)")
            return "쿨타임 대기 중"

        self.last_browser_call_time = current_time

        prompt = f"""
        [시스템 상태 분석 요청]
        - Hex Code: {hex_code}
        - CPU: {metrics.get('cpu')}%
        - RAM: {metrics.get('ram')}%
        - Process: {metrics.get('active_process', {}).get('name')}

        이 상태가 무엇을 의미하는지 '한글로 한 문장만' 답변해줘. (예: '고사양 게임 플레이 중')
        """

        print("[KnowledgeInterface] 🌐 브라우저 자동화 시작 (마우스 제어권 가져옴)")

        # 1. 클립보드에 질문 복사
        try:
            pyperclip.copy(prompt)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"[Error] Pyperclip copy failed: {e}")
            # Fallback removed to prevent CMD popups
            pass

        # 2. 브라우저 열기 (Google Gemini)
        url = "https://gemini.google.com/app"
        webbrowser.open(url)

        # 3. 로딩 대기 및 입력 자동화
        time.sleep(5)  # 페이지 로딩 대기 (인터넷 속도에 따라 조절 필요)

        # 입력창 클릭 (좌표는 해상도마다 다르므로, 탭 키를 활용하거나 이미지 인식이 좋음)
        # 여기서는 가장 범용적인 'Tab' 키 탐색 후 붙여넣기 시도
        # Gemini 페이지는 보통 열리면 입력창에 포커스가 가 있음.

        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')

        print("[KnowledgeInterface] ✅ 질문 입력 완료. 답변을 기다립니다.")
        return "브라우저에 질문 입력됨 (답변 확인 필요)"
