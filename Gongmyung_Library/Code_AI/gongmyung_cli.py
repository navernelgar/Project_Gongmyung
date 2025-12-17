import sys
import os

# [통합] 공명 철학(Brain)을 가져옵니다.
try:
    from Gongmyung_Philosophy_v2 import GongmyungPhilosophy
except ImportError:
    # 파일이 없으면 기본 클래스 생성 (안전 장치)
    class GongmyungPhilosophy:
        def __init__(self):
            self.symbols = {
                "Input": "●", "Logic": "○", "Action": "◎",
                "Serendipity": "⊕", "Distortion": "⊗"
            }

class GongmyungCLI:
    """
    [공명 커맨드 라인 도구 (Gongmyung CLI)]
    CMD에서 직접 실행하여 코드의 상태를 진단하거나 철학을 조회하는 도구입니다.
    """
    
    def __init__(self):
        self.version = "1.1.0 (Integrated)"
        # 뇌(Philosophy)와 연결
        self.brain = GongmyungPhilosophy()
        self.philosophy = self.brain.symbols

    def run(self):
        print(f"\n=== Gongmyung CLI v{self.version} ===")
        print(f"시스템 상태: {len(self.philosophy)}개의 공명 기호가 로드되었습니다.")
        
        # Check for command line arguments for non-interactive mode
        if len(sys.argv) > 1:
            op = sys.argv[1].lower()
            if op == "analyze" and len(sys.argv) > 2:
                self.analyze_file(sys.argv[2])
            elif op == "status":
                self.show_status()
            return

        print("명령을 입력하세요 (help, status, analyze <file>, exit)")
        
        while True:
            try:
                cmd = input("\nGM> ").strip().split()
                if not cmd: continue
                
                op = cmd[0].lower()
                
                if op == "exit":
                    print("공명을 종료합니다.")
                    break
                elif op == "help":
                    self.show_help()
                elif op == "status":
                    self.show_status()
                elif op == "analyze":
                    if len(cmd) < 2:
                        print("사용법: analyze <파일경로>")
                    else:
                        self.analyze_file(cmd[1])
                else:
                    print(f"알 수 없는 명령입니다: {op}")
            except EOFError:
                break
            else:
                print(f"알 수 없는 명령입니다: {op}")

    def show_help(self):
        print("\n[도움말]")
        print("- status: 현재 정의된 공명 기호들을 보여줍니다.")
        print("- analyze: 파일을 읽어서 공명문 주석이 있는지 확인합니다.")
        print("- exit: 종료합니다.")

    def show_status(self):
        print("\n[현재 공명 상태 정의 (Brain Link)]")
        for key, symbol in self.philosophy.items():
            print(f"  {symbol} : {key}")

    def analyze_file(self, filepath):
        if not os.path.exists(filepath):
            print(f"❌ 파일을 찾을 수 없습니다: {filepath}")
            return
            
        print(f"\n🔍 '{filepath}' 분석 중...")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 공명 기호 카운팅
            stats = {sym: content.count(sym) for sym in self.philosophy.values()}
            
            total_resonance = sum(stats.values())
            
            print("\n[분석 결과]")
            for sym, count in stats.items():
                if count > 0:
                    print(f"- {sym}: {count}개 발견됨")
            
            print(f"\n총 공명도: {total_resonance}")
            
            if total_resonance == 0:
                print("⚠️ 이 파일은 아직 '죽어있는 코드'입니다. (공명 없음)")
            else:
                print("✅ 이 파일은 '살아있는 코드'입니다. (공명 중)")
                
        except Exception as e:
            print(f"에러 발생: {e}")


if __name__ == "__main__":
    cli = GongmyungCLI()
    cli.run()
