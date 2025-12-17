import tkinter as tk
from tkinter import ttk
import json
import os
import sys
import threading
import psutil
from PIL import Image, ImageDraw
import pystray
from Digital_Bagua import DigitalBagua, GongmyungCodec  # Import Codec

# [설정]
# main.py가 생성하는 상태 파일의 경로
STATUS_FILE = r"D:\Project_Gongmyung\Gongmyung_Library\Code_AI\AI_Body_System\live_status.json"
REFRESH_RATE = 1000  # 1초마다 갱신


class GongmyungDashboard:
    def __init__(self, root):
        print("[Dashboard] Initializing...")
        self.root = root
        self.root.title("Gongmyung System Viewer")  # 창 제목
        self.root.geometry("400x850")  # 창 크기 (Increased height for Vision)
        self.root.configure(bg="#1e1e1e")  # 배경색: 다크 모드
        
        # 트레이 아이콘 설정
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        try:
            print("[Dashboard] Setting up Tray Icon...")
            self.setup_tray_icon()
        except Exception as e:
            print(f"[Dashboard] Tray Icon Error: {e}")

        print("[Dashboard] Initializing Bagua...")
        self.bagua = DigitalBagua()  # Initialize Bagua Oracle

        # 스타일 설정 (심플/모던)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "TLabel",
            background="#1e1e1e",
            foreground="#f32b2b",
            font=(
                "Malgun Gothic",
                10))
        style.configure(
            "Header.TLabel",
            font=(
                "Malgun Gothic",
                14,
                "bold"),
            foreground="#00ff00")
        style.configure(
            "Soul.TLabel",
            font=(
                "Malgun Gothic",
                12,
                "bold"),
            foreground="#00ccff")

        # 1. 헤더 (제목)
        self.header_label = ttk.Label(
            root, text="GONGMYUNG SYSTEM", style="Header.TLabel")
        self.header_label.pack(pady=15)

        # 2. 영혼 (Soul) 섹션
        self.soul_frame = tk.Frame(root, bg="#2d2d2d", bd=1, relief="solid")
        self.soul_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(
            self.soul_frame,
            text="[SOUL STATE]",
            bg="#2d2d2d",
            fg="#888888",
            font=(
                "Consolas",
                9)).pack(
            anchor="w",
            padx=5,
            pady=2)
        self.soul_label = tk.Label(
            self.soul_frame,
            text="Waiting for connection...",
            bg="#2d2d2d",
            fg="#00ccff",
            font=(
                "Malgun Gothic",
                11),
            wraplength=350,
            justify="center")
        self.soul_label.pack(pady=5, padx=10)

        # 3. 상태 (Stats) 섹션 - BIG NUMBERS
        self.stats_frame = tk.Frame(root, bg="#1e1e1e")
        self.stats_frame.pack(fill="x", padx=20, pady=15)

        # Grid layout for stats
        self.stats_frame.columnconfigure(0, weight=1)
        self.stats_frame.columnconfigure(1, weight=1)

        # CPU Big Label
        self.cpu_val_label = tk.Label(
            self.stats_frame,
            text="0%",
            font=(
                "Malgun Gothic",
                24,
                "bold"),
            bg="#1e1e1e",
            fg="#ff5555")
        self.cpu_val_label.grid(row=0, column=0)
        tk.Label(
            self.stats_frame,
            text="CPU Load",
            font=(
                "Malgun Gothic",
                10),
            bg="#1e1e1e",
            fg="#aaaaaa").grid(
            row=1,
            column=0)

        # RAM Big Label
        self.ram_val_label = tk.Label(
            self.stats_frame,
            text="0%",
            font=(
                "Malgun Gothic",
                24,
                "bold"),
            bg="#1e1e1e",
            fg="#5555ff")
        self.ram_val_label.grid(row=0, column=1)
        tk.Label(
            self.stats_frame,
            text="RAM Usage",
            font=(
                "Malgun Gothic",
                10),
            bg="#1e1e1e",
            fg="#aaaaaa").grid(
            row=1,
            column=1)

        # 2.5 시선 (Focus) 섹션 - Active Process
        self.focus_frame = tk.Frame(root, bg="#1e1e1e")
        self.focus_frame.pack(fill="x", padx=20, pady=15)

        ttk.Label(
            self.focus_frame,
            text="[CURRENT FOCUS]",
            foreground="#aaaaaa").pack(
            anchor="w")
        self.focus_label = ttk.Label(
            self.focus_frame, text="Scanning...", font=(
                "Malgun Gothic", 10, "bold"), foreground="#ffcc00")
        self.focus_label.pack(anchor="w", pady=(2, 0))
        self.focus_detail_label = ttk.Label(
            self.focus_frame,
            text="-",
            font=(
                "Consolas",
                8),
            foreground="#888888")
        self.focus_detail_label.pack(anchor="w")

        # 4. Internal State (Subtle Bagua)
        self.bagua_frame = tk.Frame(root, bg="#1e1e1e")
        self.bagua_frame.pack(fill="x", padx=20, pady=10)

        self.bagua_label = tk.Label(
            self.bagua_frame,
            text="Digital Bagua (Pix Map): Initializing...",
            bg="#1e1e1e",
            fg="#666666",
            font=(
                "Consolas",
                9),
            wraplength=360,
            justify="left")
        self.bagua_label.pack(anchor="w")

        # 4.5 Visual Cortex (Right Brain - Image Training)
        self.vision_frame = tk.Frame(root, bg="#1e1e1e")
        self.vision_frame.pack(fill="x", padx=20, pady=10)

        # Header with Codec Info
        self.vision_header = tk.Label(
            self.vision_frame,
            text="[VISUAL CORTEX] 64-bit Pix Map",
            bg="#1e1e1e",
            fg="#aaaaaa",
            font=(
                "Consolas",
                8))
        self.vision_header.pack(anchor="w")

        self.codec_label = tk.Label(
            self.vision_frame,
            text="Codec: Initializing...",
            bg="#1e1e1e",
            fg="#5555ff",
            font=(
                "Consolas",
                8))
        self.codec_label.pack(anchor="w")

        self.memory_label = tk.Label(
            self.vision_frame,
            text="Memory: Accessing...",
            bg="#1e1e1e",
            fg="#ffaa00",
            font=(
                "Consolas",
                8))
        self.memory_label.pack(anchor="w")

        # Canvas for 8x8 grid
        self.vision_canvas = tk.Canvas(
            self.vision_frame,
            width=160,
            height=160,
            bg="#000000",
            highlightthickness=0)
        self.vision_canvas.pack(pady=5)
        self.vision_rects = []

        # Create 8x8 grid of rectangles
        cell_size = 20
        for y in range(8):
            row_rects = []
            for x in range(8):
                rect = self.vision_canvas.create_rectangle(
                    x * cell_size, y * cell_size,
                    (x + 1) * cell_size, (y + 1) * cell_size,
                    fill="#111111", outline="#222222"
                )
                row_rects.append(rect)
            self.vision_rects.append(row_rects)

        # 5. 상태 표시줄
        self.status_bar = tk.Label(
            root,
            text="Offline",
            bg="#333333",
            fg="#ffffff",
            font=(
                "Consolas",
                8),
            anchor="e")
        self.status_bar.pack(side="bottom", fill="x")

        # 업데이트 루프 시작
        self.update_data()

    def update_data(self):
        try:
            if os.path.exists(STATUS_FILE):
                with open(STATUS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Soul 업데이트
                soul_text = data.get(
                    "cerebrum", {}).get(
                    "soul_concept", "None")
                self.soul_label.config(text=soul_text)

                # Focus (Active Process) 업데이트
                active_process = data.get(
                    "cerebrum", {}).get(
                    "active_process", {})
                proc_name = active_process.get("name", "Unknown")
                proc_title = active_process.get("title", "")
                proc_cpu = active_process.get("cpu", 0.0)
                proc_ram = active_process.get("ram_mb", 0.0)

                if len(proc_title) > 40:
                    proc_title = proc_title[:37] + "..."

                self.focus_label.config(text=f"{proc_name}")
                self.focus_detail_label.config(
                    text=f"{proc_title}\nImpact: CPU {proc_cpu:.1f}% | RAM {proc_ram:.1f}MB")

                # Stats 업데이트 (Big Numbers)
                cpu_usage = data.get("thalamus", {}).get("cpu_percent", 0)
                ram_usage = data.get("thalamus", {}).get("memory_percent", 0)

                self.cpu_val_label.config(text=f"{cpu_usage}%")
                self.ram_val_label.config(text=f"{ram_usage}%")

                # Bagua 업데이트 (Subtle Text)
                narrative_bits = int((cpu_usage / 100) * 7)  # 0~7
                survival_urgency = data.get(
                    "cerebrum",
                    {}).get(
                    "survival_instinct",
                    {}).get(
                    "urgency_score",
                    0.0)

                bagua_result = self.bagua.interpret_state(
                    narrative_bits, survival_urgency)
                sys_load = bagua_result.get('system_load', 0)

                # Format: [Hexagram Name] (Load: N) - Interpretation
                # Include the Pix Visual
                bagua_text = f"사이버네틱 로직 (3-Bit): [{bagua_result['hexagram']}] (부하: {sys_load})\n" \
                             f"{bagua_result['binary_visual']}\n" \
                             f"> {bagua_result['interpretation']}"
                self.bagua_label.config(text=bagua_text)

                # Vision Update (Visual Cortex)
                vision_grid = data.get("thalamus", {}).get("vision_grid", [])

                # Gongmyung Codec Calculation (Compression)
                if vision_grid and len(vision_grid) == 64:
                    compressed_hex = GongmyungCodec.compress_vision(
                        vision_grid)
                    self.codec_label.config(
                        text=f"Codec: 64-bit Grid -> {compressed_hex} (16-bit)")

                    for i, val in enumerate(vision_grid):
                        y = i // 8
                        x = i % 8
                        # 1 = Bright (Cyan), 0 = Dark (Black)
                        color = "#00ffcc" if val == 1 else "#111111"
                        self.vision_canvas.itemconfig(
                            self.vision_rects[y][x], fill=color)
                else:
                    # If no vision data, try "Dreaming" (Generation from Hex Code)
                    # Use the system's current hex code to generate a pattern
                    current_hex = data.get("hex_code", "0x0000")
                    generated_grid = GongmyungCodec.generate_vision(
                        current_hex)
                    self.codec_label.config(
                        text=f"Codec: {current_hex} (16-bit) -> 64-bit Dream")

                    for i, val in enumerate(generated_grid):
                        y = i // 8
                        x = i % 8
                        color = "#ff55ff" if val == 1 else "#111111"  # Magenta for Dreams
                        self.vision_canvas.itemconfig(
                            self.vision_rects[y][x], fill=color)

                # Memory Status Update
                memory_status = data.get("memory", {})
                status = memory_status.get("status", "Unknown")
                meaning = memory_status.get("meaning", "-")
                count = memory_status.get("count", 0)

                mem_color = "#00ff00" if status == "Known" else "#ffaa00"
                self.memory_label.config(
                    text=f"Memory: [{status}] {meaning} (Count: {count})", fg=mem_color)

                self.status_bar.config(
                    text="System Online | Gongmyung Engine Active", fg="#00ff00")
            else:
                self.status_bar.config(
                    text="Waiting for Core System...", fg="#ffff00")

        except Exception as e:
            self.status_bar.config(text=f"Error: {str(e)}", fg="#ff0000")

        self.root.after(REFRESH_RATE, self.update_data)

    # --- System Tray Icon Methods ---
    def create_image(self):
        # Generate "Resonance" Icon (Concentric Circles)
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), (30, 30, 30))
        dc = ImageDraw.Draw(image)
        
        # Outer Ring (Resonance Field)
        dc.ellipse((4, 4, 60, 60), outline=(0, 100, 255), width=3)
        # Middle Ring (Active Layer)
        dc.ellipse((16, 16, 48, 48), outline=(0, 255, 255), width=3)
        # Core (Consciousness)
        dc.ellipse((26, 26, 38, 38), fill=(255, 255, 255))
        
        return image

    def setup_tray_icon(self):
        image = self.create_image()
        
        # Set Window Icon as well
        try:
            from PIL import ImageTk
            icon_photo = ImageTk.PhotoImage(image)
            self.root.iconphoto(True, icon_photo)
        except Exception as e:
            print(f"[Dashboard] Window Icon Error: {e}")

        menu = pystray.Menu(
            pystray.MenuItem("Show Dashboard", self.show_window),
            pystray.MenuItem("Exit System", self.quit_system)
        )
        self.icon = pystray.Icon("Gongmyung", image, "Gongmyung AI System", menu)
        
        # Run tray icon in a separate thread to not block Tkinter
        threading.Thread(target=self.icon.run, daemon=True).start()

    def hide_window(self):
        self.root.withdraw()
        if self.icon:
            self.icon.notify("System is running in background.", "Gongmyung Hidden")

    def show_window(self, icon, item):
        self.root.after(0, self.root.deiconify)

    def quit_system(self, icon, item):
        self.icon.stop()
        self.root.after(0, self.root.destroy)
        
        # Kill main.py process (Aggressive)
        print("Stopping Main Core...")
        import subprocess
        subprocess.run(["taskkill", "/F", "/IM", "python.exe", "/T"], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(["taskkill", "/F", "/IM", "pythonw.exe", "/T"], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(["taskkill", "/F", "/IM", "node.exe", "/T"], creationflags=subprocess.CREATE_NO_WINDOW)
        os._exit(0)


if __name__ == "__main__":
    # Singleton Check
    current_pid = os.getpid()
    count = 0
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check if it's the same script
            if proc.info['cmdline'] and 'Gongmyung_Dashboard.py' in ' '.join(proc.info['cmdline']):
                # Exclude the current process itself
                if proc.info['pid'] != current_pid:
                    count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if count > 0:
        print(f"[Dashboard] Another instance is already running. Exiting PID {current_pid}.")
        sys.exit(0)

    root = tk.Tk()
    app = GongmyungDashboard(root)
    root.mainloop()
