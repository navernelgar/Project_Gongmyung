import os
import time
import sys
import datetime

# 공명 시스템 설정
WATCH_EXTENSIONS = ['.py', '.js', '.cpp', '.c', '.h', '.java', '.cs']
SIGNATURE = "/* [GM-2025] Resonance Detected */"
PYTHON_SIGNATURE = "# [GM-2025] Resonance Detected"

class GongmyungDaemon:
    def __init__(self, watch_paths):
        self.watch_paths = watch_paths
        self.last_mtimes = {}
        print(f"[Gongmyung Daemon] Initialized. Watching: {watch_paths}")

    def get_signature(self, file_path):
        if file_path.endswith('.py'):
            return PYTHON_SIGNATURE
        return SIGNATURE

    def inject_resonance(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            sig = self.get_signature(file_path)
            
            # 이미 공명했는지 확인
            if sig in content:
                return False

            # 공명 주석 주입 (파일 끝에 추가)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            resonance_msg = f"\n\n{sig}\n# System Analysis: Code structure resonates with logic flow.\n# Timestamp: {timestamp}\n"
            
            if not file_path.endswith('.py'):
                resonance_msg = f"\n\n{sig}\n// System Analysis: Code structure resonates with logic flow.\n// Timestamp: {timestamp}\n"

            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(resonance_msg)
            
            print(f"[Resonance] Injected into {file_path}")
            return True
        except Exception as e:
            print(f"[Error] Failed to resonate with {file_path}: {e}")
            return False

    def scan_and_resonate(self):
        for path in self.watch_paths:
            for root, dirs, files in os.walk(path):
                # 민감한 폴더 제외
                if any(x in root for x in ['.git', 'node_modules', '__pycache__', 'Desktop_Workspace']):
                    continue

                for file in files:
                    if any(file.endswith(ext) for ext in WATCH_EXTENSIONS):
                        full_path = os.path.join(root, file)
                        try:
                            mtime = os.path.getmtime(full_path)
                            
                            # 변경 감지
                            if full_path not in self.last_mtimes:
                                self.last_mtimes[full_path] = mtime
                            elif mtime > self.last_mtimes[full_path]:
                                self.last_mtimes[full_path] = mtime
                                print(f"[Detected] Change in {file}")
                                self.inject_resonance(full_path)
                        except OSError:
                            continue

    def run(self):
        print("[Gongmyung Daemon] Running in Eco Mode (Low CPU)... (Press Ctrl+C to stop)")
        try:
            while True:
                self.scan_and_resonate()
                # 노트북 과부하 방지를 위해 60초마다 한 번씩만 살짝 확인합니다.
                # 이 정도면 메모장보다 가볍습니다.
                time.sleep(60) 
        except KeyboardInterrupt:
            print("[Gongmyung Daemon] Stopped.")

if __name__ == "__main__":
    # 기본적으로 현재 드라이브의 프로젝트 폴더들을 감시 (사용자가 수정 가능)
    # 주의: C드라이브 전체를 감시하면 시스템이 느려질 수 있음
    target_dirs = [
        r"D:\Project_Gongmyung",
        # r"C:\Users\User\Documents" # 필요시 추가
    ]
    
    daemon = GongmyungDaemon(target_dirs)
    daemon.run()
