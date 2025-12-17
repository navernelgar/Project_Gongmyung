import http.server
import socketserver
import json
import os
import urllib.parse
import threading
import time
import tkinter as tk
from tkinter import filedialog
import re
from datetime import datetime

# Configuration
PORT = 3002
SYSTEM_ROOT = os.path.dirname(os.path.abspath(__file__))
GAME_ROOT = None # Will be set by user

# Auto-set for demo
DEMO_PATH = r"D:\Project_Gongmyung\Sample_Game_Logs"
if os.path.exists(DEMO_PATH):
    GAME_ROOT = DEMO_PATH
    print(f"Demo Mode: Game Root set to {GAME_ROOT}")

# Global Lock
process_lock = threading.Lock()

# --- Narrative Generation Logic (Ported from log_converter.py) ---
def generate_narrative(logs):
    story = []
    story.append(f"# 🛡️ 모험가 일지: {datetime.now().strftime('%Y-%m-%d')}\n")
    story.append("---\n")
    
    # Context Analysis
    location = "알 수 없음"
    for line in logs:
        if "진입했습니다" in line:
            try: location = re.search(r"'(.*?)'", line).group(1)
            except: pass
            break
            
    story.append(f"오늘 나는 **{location}**으로 발걸음을 옮겼다.\n")
    
    # Process Events
    for line in logs:
        try:
            content = line.strip()
            # Simple Heuristics for Demo
            if "[Chat]" in content:
                parts = content.split(':')
                if len(parts) > 1:
                    speaker = parts[0].replace("[Chat] ", "").strip()
                    msg = ":".join(parts[1:]).strip()
                    story.append(f"**{speaker}**: \"{msg}\"")
            elif "[Combat]" in content:
                if "나타났습니다" in content:
                    mob = re.search(r"'(.*?)'", content).group(1)
                    story.append(f"\n갑자기 **{mob}**가 나타났다!")
                elif "처치" in content:
                    story.append("적을 쓰러뜨렸다.\n")
            elif "[Loot]" in content:
                item = re.search(r"\[(.*?)\]", content).group(1)
                story.append(f"전리품으로 **{item}**을(를) 획득했다.")
            else:
                # Generic line
                story.append(f"> {content}")
        except: continue
        
    return "\n".join(story)

class GameHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        global GAME_ROOT

        parsed_path = urllib.parse.urlparse(self.path)
        
        # API: Ping
        if parsed_path.path == '/api/ping':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"pong")
            return

        # API: Convert Log to Novel
        if parsed_path.path == '/api/convert_log':
            query = urllib.parse.parse_qs(parsed_path.query)
            rel_path = query.get('path', [None])[0]
            
            # HARDCODED DEBUG PATH
            target_path = r"D:\Project_Gongmyung\Sample_Game_Logs\guigubahuang_log.txt"
            
            try:
                with open(target_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                
                novel = generate_narrative(lines)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "novel": novel}).encode('utf-8'))
            except Exception as e:
                self.send_error(500, f"Server Error: {str(e)} | Path: {target_path}")
            return

        # API: Set Game Folder
        if parsed_path.path == '/api/set_game_folder':
            try:
                # Open Native Dialog
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                new_path = filedialog.askdirectory(title="Select Game Folder (e.g., Tale of Immortal)")
                root.destroy()

                if new_path and os.path.isdir(new_path):
                    GAME_ROOT = new_path
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success", "path": GAME_ROOT}).encode('utf-8'))
                else:
                    self.send_error(400, "Invalid path or cancelled")
            except Exception as e:
                self.send_error(500, str(e))
            return

        # API: List Game Files (Optimized for Heavy Folders)
        if parsed_path.path == '/api/game_files':
            if not GAME_ROOT:
                self.send_error(400, "Game Root not set. Call /api/set_game_folder first.")
                return

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            files = []
            try:
                max_files = 1000 # Higher limit for game server
                file_count = 0
                
                # Heavy Optimization for Game Folders
                skip_heavy = ['Data', 'Resources', 'StreamingAssets', 'Shader', 'Texture', 'Audio', 'CacheData', 'Mod', 'MonoBleedingEdge']
                
                for root, dirs, filenames in os.walk(GAME_ROOT):
                    # Filter directories in-place
                    dirs[:] = [d for d in dirs if d not in skip_heavy and not d.startswith('.')]

                    for filename in filenames:
                        if filename.startswith('.'): continue
                        
                        # Whitelist interesting extensions
                        if not filename.lower().endswith(('.txt', '.json', '.xml', '.log', '.ini', '.cfg', '.md')):
                            continue

                        try:
                            full_path = os.path.join(root, filename)
                            rel_path = os.path.relpath(full_path, GAME_ROOT).replace('\\', '/')
                            files.append(rel_path)
                            file_count += 1
                            if file_count >= max_files: break
                        except: pass
                    
                    if file_count >= max_files: break
            except Exception as e:
                print(f"Error walking game dir: {e}")
                
            self.wfile.write(json.dumps(files).encode('utf-8'))
            return

        # Default: Serve files from GAME_ROOT if set, else System Root
        if GAME_ROOT:
            # Security check: prevent traversing up
            safe_path = os.path.normpath(os.path.join(GAME_ROOT, self.path.lstrip('/')))
            if not safe_path.startswith(GAME_ROOT):
                self.send_error(403, "Access Denied")
                return
            
            if os.path.exists(safe_path) and os.path.isfile(safe_path):
                super().do_GET() # Use default handler for file serving
            else:
                self.send_error(404, "File not found in Game Root")
        else:
            self.wfile.write(b"Game Server Running. Please set Game Folder via /api/set_game_folder")

# Threaded Server
class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

if __name__ == "__main__":
    print(f"Starting Game Server on Port {PORT}...")
    server = ThreadedHTTPServer(('0.0.0.0', PORT), GameHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
