import time
import math
import ctypes
import psutil
from PIL import ImageGrab, Image


class Thalamus:
    """
    [시상: Thalamus]
    시스템의 물리적 감각(CPU, RAM)을 수용하고
    1차적인 공명 신호(Gongmyung Signal)로 변환하여 전달하는 기관.
    """

    def __init__(self, config):
        self.config = config
        self.prev_cpu = psutil.cpu_percent()
        self.prev_ram = psutil.virtual_memory().percent

        # 공명 기호 정의
        self.SYM_START = "●"   # 주체/감각
        self.SYM_COND = "○"   # 조건/판단
        self.SYM_ACT = "◎"   # 작용/흐름
        self.SYM_RES = "⇒"   # 결과/전이

    def sense_vision(self):
        """
        [시각 감지] 화면 전체를 캡처하여 8x8 픽셀 그리드(64비트)로 변환합니다.
        이 데이터는 '우뇌(Right Brain)'의 이미지 트레이닝 기초 자료로 사용됩니다.
        - 1: 밝음 (활성)
        - 0: 어두움 (비활성)
        """
        try:
            # 화면 캡처 (전체 화면)
            screen = ImageGrab.grab()
            # 8x8로 리사이즈 (단순화)
            small = screen.resize((8, 8), Image.Resampling.BILINEAR)
            # 흑백 변환
            gray = small.convert("L")

            # 픽셀 데이터 추출 (0~255)
            pixels = list(gray.getdata())

            # 0(어두움)과 1(밝음)로 이진화 (Threshold 128)
            binary_grid = [1 if p > 128 else 0 for p in pixels]

            return binary_grid
        except Exception:
            # 에러 시 빈 그리드 반환 (0으로 채움)
            return [0] * 64

    def get_active_process_info(self):
        """
        [초점 감지] 현재 사용자가 보고 있는(활성화된) 윈도우와 프로세스 정보를 수집합니다.
        - Name: 프로세스 이름 (예: chrome.exe)
        - Title: 창 제목 (예: Google - Chrome)
        - Resource: 해당 프로세스의 CPU/RAM 점유율
        """
        try:
            # 1. 활성 윈도우 핸들 가져오기
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            if hwnd == 0:
                return {
                    "name": "Unknown",
                    "title": "None",
                    "cpu": 0.0,
                    "ram": 0.0}

            # 2. 프로세스 ID (PID) 가져오기
            pid = ctypes.c_ulong()
            ctypes.windll.user32.GetWindowThreadProcessId(
                hwnd, ctypes.byref(pid))
            pid = pid.value

            # 3. 프로세스 정보 조회
            process = psutil.Process(pid)
            name = process.name()
            title = "Unknown"

            # 윈도우 제목 가져오기 (ctypes 사용)
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
            title = buff.value

            # 리소스 사용량 (CPU는 interval=None으로 호출하여 즉시 반환값 사용, 정확도는 낮을 수 있음)
            # process.cpu_percent()는 첫 호출시 0.0을 반환하므로, 지속적인 모니터링이 아니면 정확하지 않음.
            # 여기서는 시스템 전체 부하와 별개로 '이 프로세스가 살아있다'는 것에 집중.
            cpu_usage = process.cpu_percent(interval=None) / psutil.cpu_count()
            mem_info = process.memory_info()
            ram_usage_mb = mem_info.rss / (1024 * 1024)  # MB 단위
            
            # [심층 신호 감지] 스레드 수와 I/O 카운터 (비트 신호의 전조)
            num_threads = process.num_threads()
            try:
                io_counters = process.io_counters()
                io_activity = io_counters.read_count + io_counters.write_count
            except Exception:
                io_activity = 0

            # [네트워크/파일 감지] 외부와의 연결 확인 (시냅스 연결)
            connections = 0
            try:
                # net_connections는 권한 문제로 실패할 수 있음
                connections = len(process.net_connections())
            except Exception:
                pass

            return {
                "name": name,
                "title": title,
                "cpu": cpu_usage,
                "ram_mb": ram_usage_mb,
                "threads": num_threads, # 생명력 (맥박)
                "io": io_activity,      # 호흡 (데이터 교환)
                "net": connections      # 소통 (외부 연결)
            }
        except Exception as e:
            return {"name": "Error", "title": str(e), "cpu": 0.0, "ram": 0.0, "threads": 0, "io": 0, "net": 0}

    def sense(self):
        """
        [감각 수용] 시스템의 물리적 상태(CPU, RAM, 변화량)를 측정하여 메트릭(Metrics)을 생성합니다.
        """
        current_cpu = psutil.cpu_percent(
            interval=None)  # Non-blocking call preferred in loop
        current_ram = psutil.virtual_memory().percent

        # 활성 프로세스 정보 감지
        active_process = self.get_active_process_info()

        # Δ (Delta): 변화량
        delta_cpu = current_cpu - self.prev_cpu
        delta_ram = current_ram - self.prev_ram
        delta_total = math.sqrt(delta_cpu**2 + delta_ram**2)

        # 𝓡 (Resonance): 안정도 (0~1)
        resonance = 1.0 / (1.0 + abs(delta_total) * 0.1)

        # F (Flow): 흐름/부하
        flow = (current_cpu + current_ram) / 2.0

        # 상태 업데이트
        self.prev_cpu = current_cpu
        self.prev_ram = current_ram

        # 시각 정보 수집 (우뇌)
        vision_grid = self.sense_vision()

        return {
            "cpu": current_cpu,
            "ram": current_ram,
            "active_process": active_process,
            "vision_grid": vision_grid,
            "delta": delta_total,
            "resonance": resonance,
            "flow": flow,
            "timestamp": time.time()
        }

    def translate_signal(self, metrics):
        """
        감각 데이터를 공명문과 16bit 코드로 변환합니다.
        """
        cpu = metrics["cpu"]
        ram = metrics["ram"]
        resonance = metrics["resonance"]
        delta = metrics["delta"]

        # 16bit Code Generation
        header = int((cpu / 100.0) * 15)
        core = int((ram / 100.0) * 15)
        decision = int(resonance * 15)
        result = (header + core) % 16
        hex_code = f"0x{header:X}{core:X}{decision:X}{result:X}"

        # Gongmyung Sentence Generation
        subject = f"{self.SYM_START}(CPU:{cpu:.1f}%/RAM:{ram:.1f}%)"

        if resonance > self.config["thresholds"]["resonance_stable"]:
            condition = f"{self.SYM_COND}(Stable)"
        elif resonance > self.config["thresholds"]["resonance_unstable"]:
            condition = f"{self.SYM_COND}(Fluctuating)"
        else:
            condition = f"{self.SYM_COND}(Unstable)"

        if delta < 1.0:
            action = f"{self.SYM_ACT}(Maintain)"
        elif delta < self.config["thresholds"]["cpu_surge"]:
            action = f"{self.SYM_ACT}(Adjust)"
        else:
            action = f"{self.SYM_ACT}(Surge)"

        gongmyung_sentence = f"{subject} ~ {condition} ~ {action} ~ {self.SYM_RES}(𝓡:{resonance:.2f})"

        return {
            "hex_code": hex_code,
            "sentence": gongmyung_sentence
        }
