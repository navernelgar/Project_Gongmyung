import re
import os


class FlowParser:
    """
    [서사 연산기: Narrative Processor]
    코드 내의 서사적 주석(@flow)을 추출하여
    비트(Bit) 단위의 에너지 값으로 변환하는 모듈.
    """

    # 서사 비트 정의 (Narrative Bits)
    FLOW_BITS = {
        "start": 0x1,  # 0001: 시작
        "process": 0x2,  # 0010: 과정
        "branch": 0x4,  # 0100: 분기
        "end": 0x8,  # 1000: 끝
        "monetize": 0xF  # 1111: 가치 창출 (보너스)
    }

    def __init__(self):
        self.pattern = re.compile(r"@flow:(\w+)\s*(.*)")

    def parse_file(self, file_path):
        """
        파일을 읽어 서사 흐름을 비트로 계산합니다.
        """
        if not os.path.exists(file_path):
            return None

        narrative_sum = 0
        flow_sequence = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line in lines:
                match = self.pattern.search(line)
                if match:
                    tag_type = match.group(1).lower()
                    description = match.group(2).strip()

                    if tag_type in self.FLOW_BITS:
                        bit_value = self.FLOW_BITS[tag_type]
                        narrative_sum += bit_value
                        flow_sequence.append(
                            f"[{tag_type.upper()}:{hex(bit_value)}] {description}")

            # 서사 밀도 (Density) 계산: 줄 수 대비 서사 태그 비율
            density = len(flow_sequence) / len(lines) if lines else 0

            return {
                "file": os.path.basename(file_path),
                "narrative_value": narrative_sum,  # 총 서사 에너지 (10진수)
                "hex_signature": hex(narrative_sum),  # 서사 서명 (16진수)
                "density": round(density, 4),
                "sequence": flow_sequence
            }

        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None


# 테스트 실행
if __name__ == "__main__":
    # 테스트를 위해 가상의 서사 파일을 생성하여 분석
    test_file = "test_narrative.py"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("# @flow:start 공명 시스템 초기화\n")
        f.write("print('Hello')\n")
        f.write("# @flow:process 데이터 로딩 중\n")
        f.write("data = load()\n")
        f.write("# @flow:branch 데이터 유효성 검사\n")
        f.write("if data:\n")
        f.write("    # @flow:process 분석 수행\n")
        f.write("    analyze()\n")
        f.write("# @flow:end 결과 저장 및 종료\n")
        f.write("save()\n")

    parser = FlowParser()
    result = parser.parse_file(test_file)

    print(f"=== 서사 연산 결과: {result['file']} ===")
    print(
        f"총 서사 에너지: {result['narrative_value']} (Signature: {result['hex_signature']})")
    print(f"서사 밀도: {result['density']}")
    print("--- 흐름 ---")
    for step in result['sequence']:
        print(step)

    # 테스트 파일 정리
    os.remove(test_file)
