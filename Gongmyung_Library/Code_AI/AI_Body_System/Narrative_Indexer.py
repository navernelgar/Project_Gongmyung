import os
import json
from Flow_Parser import FlowParser


class NarrativeIndexer:
    """
    [서사 인덱서: Narrative Indexer]
    프로젝트 내의 모든 파일을 스캔하여 '서사 비트(Narrative Bit)' 지도를 만듭니다.
    사용자가 원하는 '의미'로 즉시 점프(Jump)할 수 있게 해주는 네비게이션 장치입니다.
    """

    def __init__(self, root_path):
        self.root_path = root_path
        self.parser = FlowParser()
        self.index = []

    def scan_project(self):
        print(f"Scanning narrative landscape in: {self.root_path}...")

        for root, _, files in os.walk(self.root_path):
            # .git, .venv 등 불필요한 폴더 제외
            if any(
                ignore in root for ignore in [
                    '.git',
                    '.venv',
                    '__pycache__',
                    'node_modules']):
                continue

            for file in files:
                if file.endswith(('.py', '.js', '.md', '.txt')):
                    file_path = os.path.join(root, file)
                    result = self.parser.parse_file(file_path)

                    if result and result['narrative_value'] > 0:
                        # 서사 에너지가 있는 파일만 인덱싱
                        self.index.append({
                            "path": file_path,
                            "name": result['file'],
                            "signature": result['hex_signature'],
                            "energy": result['narrative_value'],
                            "density": result['density'],
                            "flow_count": len(result['sequence'])
                        })
                        print(
                            f"  Found Signal: {result['file']} (Sig: {result['hex_signature']})")

    def save_index(self, output_file="narrative_index.json"):
        # Convert list to dict for easier lookup by path in GongmyungGate
        index_dict = {item['path']: item for item in self.index}

        # Save to the current directory (AI_Body_System) to ensure it's found
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_dir, output_file)

        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(index_dict, f, indent=2, ensure_ascii=False)
        print(
            f"\nIndex saved to {full_path}. Total {len(self.index)} narrative nodes found.")

    def search_by_bit(self, target_bit):
        """
        특정 비트(의미)를 포함하는 파일을 검색합니다.
        예: 0x4 (Branch/분기)가 있는 파일 찾기
        """
        print(
            f"\n[Search] Jumping to nodes containing Bit {hex(target_bit)}...")
        results = []
        for node in self.index:
            # 비트 연산 (&)으로 해당 속성이 있는지 확인
            if (node['energy'] & target_bit) == target_bit:
                results.append(node)
                print(
                    f"  -> Detected in: {node['name']} (Energy: {node['energy']})")
        return results


if __name__ == "__main__":
    # 현재 프로젝트 폴더 스캔
    project_root = r"D:\Project_Gongmyung\Gongmyung_Library"
    indexer = NarrativeIndexer(project_root)

    # 1. 지도 생성 (Excel 만들기)
    indexer.scan_project()
    indexer.save_index()

    # 2. 점프 테스트 (BitNet Style Search)
    # 예: '분기(Branch, 0x4)'가 있는 지점으로 점프
    indexer.search_by_bit(0x4)
