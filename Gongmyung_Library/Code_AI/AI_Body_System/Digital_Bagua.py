import random


class DigitalBagua:
    def __init__(self):
        # Cybernetic 3-Bit Logic Mapping
        # Maps 3-bit binary states to system operational modes.
        # 0 = Low/Off, 1 = High/On

        self.trigrams = {
            # 000: Idle State
            0: {
                "name": "시스템 대기 (System Idle)",
                "priority": 0,
                "nature": "Ground",
                "binary": "000",
                "meaning": "시스템 유휴 상태, 저전력 모드, 입력 대기 중"
            },

            # 001: Storage/Buffer (Mountain - Stillness)
            1: {
                "name": "저장소 대기 (Storage Wait)",
                "priority": 2,
                "nature": "Block",
                "binary": "001",
                "meaning": "I/O 차단됨, 버퍼링 중, 데이터 보존 상태"
            },

            # 010: Memory Stream (Water - Flow)
            2: {
                "name": "메모리 스트림 (Memory Stream)",
                "priority": 3,
                "nature": "Flow",
                "binary": "010",
                "meaning": "메모리 읽기/쓰기, 데이터 흐름, 캐시 접근"
            },

            # 011: Bus Transfer (Wind - Penetration)
            3: {
                "name": "버스 전송 (Bus Transfer)",
                "priority": 4,
                "nature": "Transmit",
                "binary": "011",
                "meaning": "버스 활성, 네트워크 전송, 프로세스 간 통신(IPC)"
            },

            # 100: Interrupt (Thunder - Movement)
            4: {
                "name": "인터럽트 요청 (Interrupt IRQ)",
                "priority": 7,
                "nature": "Trigger",
                "binary": "100",
                "meaning": "하드웨어 인터럽트, 신호 트리거, 웨이크업"
            },

            # 101: Processing (Fire - Clarity/Heat)
            5: {
                "name": "프로세스 실행 (Process Exec)",
                "priority": 8,
                "nature": "Compute",
                "binary": "101",
                "meaning": "ALU 활성, 연산 수행, 발열 발생"
            },

            # 110: Interface (Lake - Interaction)
            6: {
                "name": "인터페이스 출력 (Interface Out)",
                "priority": 9,
                "nature": "Output",
                "binary": "110",
                "meaning": "디스플레이 갱신, 사용자 피드백, 렌더링"
            },

            # 111: Kernel/Full Load (Heaven - Origin)
            7: {
                "name": "커널 로드 (Kernel Load)",
                "priority": 10,
                "nature": "Core",
                "binary": "111",
                "meaning": "커널 모드, 풀 로드, 임계 구역(Critical Section)"
            }
        }

        # The "System Log Pool" (Heuristic Analysis)
        self.singularity_pool = [
            "메모리 블록에서 휴리스틱 패턴이 감지되었습니다.",
            "논리 게이트 타이밍 변동이 관측되었습니다.",
            "현재 작업을 위한 스레드 할당을 최적화 중입니다.",
            "캐시 적중률이 예상 범위를 초과했습니다.",
            "난수 생성기에서 양자 변동이 시뮬레이션되었습니다.",
            "시스템 클럭 동기화를 재조정 중입니다.",
            "사고 프로세스에서 재귀 루프가 감지되었습니다."
        ]
        
        # Kaleidoscope Symbols (만화경 기호)
        self.k_symbols = {
            "start": "○",   # Start / Trigger
            "end": "●",     # End / Completion
            "process": "◎", # Process / Core
            "flow": "→",    # Transition
            "error": "※",   # Error / Exception
            "wave": "~"     # Wave / Time
        }

    def get_kaleidoscope_pattern(self, h_nature, c_nature, d_nature, state):
        """
        Generates a Kaleidoscope Flow Pattern based on the Coordinate.
        Pattern: ○ [Header] ◎ [Core] → ● [Decision]
        """
        s = self.k_symbols
        
        # Basic Flow: Start(Header) -> Process(Core) -> End(Decision)
        flow = f"{s['start']} [{h_nature}] {s['process']} [{c_nature}] {s['flow']} {s['end']} [{d_nature}]"
        
        # State Modifier
        if state == "Critical" or state == "Survival_Mode":
            # Error Pattern: ... -> ※ [Decision]
            flow = f"{s['start']} [{h_nature}] {s['process']} [{c_nature}] {s['flow']} {s['error']} [{d_nature}]"
        elif state == "Idle":
            # Wave Pattern: ... ~ [Decision]
            flow = f"{s['start']} [{h_nature}] {s['wave']} {s['end']} [{d_nature}]"
            
        return flow

    def interpret_state(self, narrative_bits, survival_urgency):
        """
        narrative_bits (int): Narrative Bitmask (0~15)
        survival_urgency (float): System Load/Urgency (0.0 ~ 1.0)
        """
        # Extract Lower 3 Bits -> Internal State (Code/Logic)
        lower_key = narrative_bits & 0b111

        # Map Urgency to 8 Levels -> External State (Body/Hardware)
        upper_key = int(survival_urgency * 7)

        lower = self.trigrams[lower_key]
        upper = self.trigrams[upper_key]

        # Calculate System Stability
        # Sum of priorities
        sys_load = lower['priority'] + upper['priority']

        interpretation = (
            f"내부(논리): {lower['name']} [{lower['binary']}] - {lower['meaning']}\n"
            f"외부(하드웨어): {upper['name']} [{upper['binary']}] - {upper['meaning']}"
        )

        if sys_load >= 15:
            interpretation += "\n[경고] 시스템 부하 임계치 도달. 스로틀링 권장."
        elif sys_load <= 2:
            interpretation += "\n[정보] 시스템 딥 슬립/대기 모드 진입."

        # Apply Singularity (Heuristic Factor)
        # 30% chance to add a system log
        if random.random() < 0.3:
            singularity_comment = random.choice(self.singularity_pool)
            interpretation += f"\n[로그] {singularity_comment}"

        # Pixel Visualization (The 'Pix' System)
        # 1 = ■ (On), 0 = □ (Off)
        def to_pix(binary_str):
            return binary_str.replace('1', '■').replace('0', '□')

        upper_pix = to_pix(upper['binary'])
        lower_pix = to_pix(lower['binary'])

        hexagram_visual = f"{upper_pix} (HW)\n{lower_pix} (SW)"

        return {
            "hexagram": f"{upper['name']} / {lower['name']}",
            "system_load": sys_load,
            "interpretation": interpretation,
            "binary_visual": hexagram_visual
        }


class GongmyungCodec:
    """
    [공명 코덱: Gongmyung Codec]
    16비트 공명 코드(좌뇌/언어)와 64비트 시각 그리드(우뇌/이미지) 간의
    초고속 변환(압축/해제)을 담당하는 로직.

    원리: 1 Hex Char (4 bits) <-> 4 Pixels (2x2 Block)
    총 4 Hex Chars (16 bits) <-> 16 Pixels (4x4 Block) -> 확장 -> 64 Pixels
    """

    @staticmethod
    def compress_vision(vision_grid_64):
        """
        64비트(8x8) 이미지를 16비트(4 Hex) 코드로 압축 (손실 압축)
        8x8 그리드를 2x2 블록 16개로 나누고, 각 블록의 평균값을 다시 4x4로 축소,
        최종적으로 4개의 16진수 문자로 변환.
        """
        # 단순화를 위해 8x8 그리드를 4개의 구역(4x4)으로 나눔
        # 각 구역(16픽셀)의 활성도(1의 개수)를 0~15(Hex)로 변환
        hex_code = ""

        # 4개의 구역 (Top-Left, Top-Right, Bottom-Left, Bottom-Right)
        zones = [
            (0, 0), (0, 4), (4, 0), (4, 4)
        ]

        for start_y, start_x in zones:
            active_count = 0
            for y in range(start_y, start_y + 4):
                for x in range(start_x, start_x + 4):
                    idx = y * 8 + x
                    if idx < len(vision_grid_64) and vision_grid_64[idx] == 1:
                        active_count += 1

            # 0~16 범위를 0~15(Hex)로 클램핑
            hex_val = min(active_count, 15)
            hex_code += f"{hex_val:X}"

        return f"0x{hex_code}"

    @staticmethod
    def generate_vision(hex_code_16):
        """
        16비트(4 Hex) 코드를 기반으로 64비트(8x8) 이미지를 생성 (생성형 확장)
        각 Hex 값(0~F)을 시드(Seed)로 사용하여 4x4 패턴을 생성하고 조합.
        """
        # "0xABCD" -> "ABCD"
        clean_hex = hex_code_16.replace("0x", "")
        if len(clean_hex) != 4:
            return [0] * 64  # Error fallback

        grid = [0] * 64

        # 4개의 구역에 대해 패턴 생성
        zones = [
            (0, 0), (0, 4), (4, 0), (4, 4)
        ]

        for i, char in enumerate(clean_hex):
            try:
                val = int(char, 16)  # 0~15
            except ValueError:
                val = 0

            start_y, start_x = zones[i]

            # 생성 알고리즘: 값의 비트 패턴을 4x4 영역에 뿌림
            # 예: val=15(1111) -> 꽉 채움? 아니면 패턴화?
            # 여기서는 '프랙탈'처럼 비트를 분산시킴

            # Simple Pattern Generator based on bits of 'val'
            # val (4 bits): b3 b2 b1 b0
            # 4x4 area indices:
            # 0 1 2 3
            # 4 5 6 7 ...

            # Pattern:
            # If b3 is 1 -> Fill corners
            # If b2 is 1 -> Fill center
            # If b1 is 1 -> Fill cross
            # If b0 is 1 -> Fill diagonals

            b3 = (val >> 3) & 1
            b2 = (val >> 2) & 1
            b1 = (val >> 1) & 1
            b0 = (val >> 0) & 1

            for r in range(4):
                for c in range(4):
                    pixel_on = 0
                    # Logic for pattern generation
                    if b3 and (r in [0, 3] and c in [0, 3]):
                        pixel_on = 1  # Corners
                    if b2 and (r in [1, 2] and c in [1, 2]):
                        pixel_on = 1  # Center
                    if b1 and (r == 2 or c == 2):
                        pixel_on = 1  # Cross-ish
                    if b0 and (r == c or r + c == 3):
                        pixel_on = 1  # Diagonal

                    if pixel_on:
                        grid_y = start_y + r
                        grid_x = start_x + c
                        grid[grid_y * 8 + grid_x] = 1

        return grid


if __name__ == "__main__":
    oracle = DigitalBagua()
    # 테스트: 서사=분기(4, 간), 생존=안정(0, 곤)
    result = oracle.interpret_state(4, 0.0)
    print(f"정역(Correct Change) 계산 결과:\n"
          f"{result['hexagram']}\n"
          f"{result['binary_visual']}\n"
          f"{result['interpretation']}")
