import os
import time
import threading
import sys
import datetime

# 공명 시스템 설정
WATCH_EXTENSIONS = ['.py', '.js', '.cpp', '.c', '.h', '.java', '.cs']
SIGNATURE = "/* [GM-2025] Resonance Detected */"
PYTHON_SIGNATURE = "# [GM-2025] Resonance Detected"

# UI 라이브러리 확인
try:
    import pystray
    from PIL import Image, ImageDraw
    HAS_UI = True
except ImportError:
    HAS_UI = False
    print("[Warning] pystray/pillow not found. Running in console mode.")

class GongmyungDaemon:
    def __init__(self, watch_paths):
        self.watch_paths = watch_paths
        self.last_mtimes = {}
        self.running = True
        self.icon = None
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
            
            if sig in content:
                return False

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
                if any(x in root for x in ['.git', 'node_modules', '__pycache__', 'Desktop_Workspace']):
                    continue

                for file in files:
                    if any(file.endswith(ext) for ext in WATCH_EXTENSIONS):
                        full_path = os.path.join(root, file)
                        try:
                            mtime = os.path.getmtime(full_path)
                            if full_path not in self.last_mtimes:
                                self.last_mtimes[full_path] = mtime
                            elif mtime > self.last_mtimes[full_path]:
                                self.last_mtimes[full_path] = mtime
                                print(f"[Detected] Change in {file}")
                                self.inject_resonance(full_path)
                        except OSError:
                            continue

    def loop(self):
        print("[Gongmyung Daemon] Loop started.")
        while self.running:
            self.scan_and_resonate()
            time.sleep(60) # Eco Mode

    def stop(self, icon=None, item=None):
        print("[Gongmyung Daemon] Stopping...")
        self.running = False
        if self.icon:
            self.icon.stop()
        sys.exit(0)

    def create_icon(self):
        # 아이콘 생성 (청록색 원)
        width = 64
        height = 64
        color_bg = (0, 0, 0)
        color_fg = (0, 255, 255) # Cyan

        image = Image.new('RGB', (width, height), color_bg)
        dc = ImageDraw.Draw(image)
        dc.ellipse((10, 10, 54, 54), fill=color_fg)
        dc.ellipse((20, 20, 44, 44), fill=color_bg) # Ring shape

        menu = pystray.Menu(
            pystray.MenuItem('Gongmyung Active', lambda: None, enabled=False),
            pystray.MenuItem('Exit', self.stop)
        )

        self.icon = pystray.Icon("Gongmyung", image, "Gongmyung Daemon", menu)
        self.icon.run()

    def run(self):
        # 백그라운드 스레드에서 감시 시작
        t = threading.Thread(target=self.loop)
        t.daemon = True
        t.start()

        if HAS_UI:
            print("[Gongmyung Daemon] Starting System Tray Icon...")
            self.create_icon()
        else:
            print("[Gongmyung Daemon] Running in Console Mode (No Icon). Press Ctrl+C to stop.")
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop()

if __name__ == "__main__":
    # 기본적으로 현재 드라이브의 프로젝트 폴더들을 감시 (사용자가 수정 가능)
    # 주의: C드라이브 전체를 감시하면 시스템이 느려질 수 있음
    target_dirs = [
        r"D:\Project_Gongmyung",
        # r"C:\Users\User\Documents" # 필요시 추가
    ]
    
    daemon = GongmyungDaemon(target_dirs)
    daemon.run()
