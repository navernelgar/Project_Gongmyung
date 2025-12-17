import http.server
import socketserver
import json
import os
import urllib.parse
import functools
import socket
import threading
import time
import tkinter as tk
from tkinter import filedialog
import direct_analysis  # Import the analysis module
import scraper # Import the scraper module
from Gongmyung_Philosophy import GongmyungThought # Import the philosophy module

# Global Lock for Sequential Processing (Single Core Optimization)
thought_lock = threading.Lock()

# Logging setup
def log_debug(message):
    with open("server_debug.log", "a", encoding="utf-8") as f:
        f.write(f"{time.ctime()}: {message}\n")

# Function to find an available port
def find_available_port(start_port, max_attempts=10):
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
    raise Exception("No available ports found")

PORT = find_available_port(3000)
SYSTEM_ROOT = os.path.dirname(os.path.abspath(__file__))
log_debug(f"Server starting. SYSTEM_ROOT: {SYSTEM_ROOT}")

# Default to Obsidian Vault if available, otherwise System Root
OBSIDIAN_VAULT_PATH = r"D:\Obsidian Vault"
if os.path.exists(OBSIDIAN_VAULT_PATH):
    WORKSPACE_ROOT = OBSIDIAN_VAULT_PATH
    log_debug(f"Defaulting to Obsidian Vault: {WORKSPACE_ROOT}")
    print(f"Defaulting to Obsidian Vault: {WORKSPACE_ROOT}")
else:
    # Create it if it doesn't exist, as per user request to use D:
    try:
        os.makedirs(OBSIDIAN_VAULT_PATH)
        WORKSPACE_ROOT = OBSIDIAN_VAULT_PATH
        log_debug(f"Created and defaulting to Obsidian Vault: {WORKSPACE_ROOT}")
        print(f"Created and defaulting to Obsidian Vault: {WORKSPACE_ROOT}")
    except Exception as e:
        WORKSPACE_ROOT = SYSTEM_ROOT # Fallback
        log_debug(f"Failed to create Obsidian Vault on D:. Defaulting to System Root: {WORKSPACE_ROOT}. Error: {e}")
        print(f"Failed to create Obsidian Vault on D:. Defaulting to System Root: {WORKSPACE_ROOT}")

# Force change directory to ensure files are served correctly
try:
    os.chdir(SYSTEM_ROOT)
    log_debug(f"Working directory set to: {SYSTEM_ROOT}")
    print(f"Working directory set to: {SYSTEM_ROOT}")
except Exception as e:
    log_debug(f"Failed to set working directory: {e}")
    print(f"Failed to set working directory: {e}")

class GongmyungHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global WORKSPACE_ROOT

        # Redirect root to Gongmyung_Viewer.html (The "Viewer First" philosophy)
        if self.path == '/':
            self.send_response(302)
            self.send_header('Location', '/Gongmyung_Viewer.html')
            self.end_headers()
            return

        parsed_path = urllib.parse.urlparse(self.path)
        print(f"DEBUG: path={self.path}, parsed={parsed_path.path}", flush=True)
        
        # API: Change Workspace Root
        if parsed_path.path == '/api/change_root':
            query = urllib.parse.parse_qs(parsed_path.query)
            new_path = query.get('path', [None])[0]
            
            # Handle URL decoding for Windows paths
            if new_path:
                new_path = urllib.parse.unquote(new_path)
            else:
                # Open Native Dialog if no path provided
                try:
                    root = tk.Tk()
                    root.withdraw() # Hide main window
                    root.attributes('-topmost', True) # Bring to front
                    new_path = filedialog.askdirectory(title="Select Workspace Folder")
                    root.destroy()
                except Exception as e:
                    print(f"Dialog Error: {e}")

            if new_path and os.path.isdir(new_path):
                WORKSPACE_ROOT = new_path
                print(f"Workspace changed to: {WORKSPACE_ROOT}")
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "path": WORKSPACE_ROOT}).encode('utf-8'))
            else:
                # If user cancelled or invalid path
                if new_path == "": # Cancelled
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "cancelled"}).encode('utf-8'))
                else:
                    self.send_error(400, "Invalid directory path")
            return

        if parsed_path.path.startswith('/api/thought'):
            # Sequential Processing Block
            # Acquires lock to ensure only one thought process runs at a time
            with thought_lock:
                import random
                # Simulate system sensation
                sensation_data = {
                    'cpu': random.randint(10, 95),
                    'ram': random.randint(20, 80),
                    'network': random.choice(['Connected', 'Slow', 'Disconnected'])
                }
                
                try:
                    thought = GongmyungThought()
                    result = thought.sense(sensation_data).judge().act().transition()
                    
                    # Artificial delay to prevent CPU overheating on single-core systems
                    time.sleep(0.2) 
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode('utf-8'))
                except Exception as e:
                    print(f"Error in thought process: {e}")
                    self.send_error(500, str(e))
            return

        if parsed_path.path == '/api/capture_screen':
            try:
                vision_dir = os.path.join(SYSTEM_ROOT, 'Vision')
                if not os.path.exists(vision_dir):
                    os.makedirs(vision_dir)
                
                timestamp = int(time.time())
                filename = f"vision_{timestamp}.png"
                filepath = os.path.join(vision_dir, filename)
                
                # Method 1: PIL (Pillow)
                try:
                    from PIL import ImageGrab
                    screenshot = ImageGrab.grab()
                    screenshot.save(filepath)
                except ImportError:
                    # Method 2: PowerShell Fallback
                    import subprocess
                    # Use raw string for path to avoid escape issues
                    ps_script = f"""
                    Add-Type -AssemblyName System.Windows.Forms
                    Add-Type -AssemblyName System.Drawing
                    $bmp = New-Object System.Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height)
                    $graphics = [System.Drawing.Graphics]::FromImage($bmp)
                    $graphics.CopyFromScreen([System.Drawing.Point]::Empty, [System.Drawing.Point]::Empty, $bmp.Size)
                    $bmp.Save('{filepath}')
                    """
                    subprocess.run(["powershell", "-Command", ps_script], check=True)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "url": f"/Vision/{filename}"}).encode('utf-8'))
                
            except Exception as e:
                print(f"Vision Error: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        if parsed_path.path == '/api/files':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            files = []
            print(f"DEBUG: Listing files in {WORKSPACE_ROOT}")
            
            try:
                # Vault Listing - Should be fast and complete
                for root, dirs, filenames in os.walk(WORKSPACE_ROOT):
                    # Skip hidden folders
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    
                    for filename in filenames:
                        if filename.startswith('.'): continue 
                        
                        # List all relevant Vault files
                        if not filename.lower().endswith(('.md', '.txt', '.json', '.png', '.jpg', '.html', '.js', '.css')):
                            continue

                        try:
                            full_path = os.path.join(root, filename)
                            rel_path = os.path.relpath(full_path, WORKSPACE_ROOT)
                            rel_path = rel_path.replace('\\', '/')
                            files.append(rel_path)
                        except Exception as e:
                            print(f"Error processing file {filename}: {e}")
                        
            except Exception as e:
                print(f"Error walking directory: {e}")
                
            self.wfile.write(json.dumps(files).encode('utf-8'))
        
        elif parsed_path.path == '/api/view_analysis':
            query = urllib.parse.parse_qs(parsed_path.query)
            filepath = query.get('path', [None])[0]
            
            if filepath:
                # Join with WORKSPACE_ROOT
                full_path = os.path.join(WORKSPACE_ROOT, filepath)
                if os.path.exists(full_path):
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Use the shared analysis logic
                        analysis_result = direct_analysis.analyze_structure(content)
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(analysis_result).encode('utf-8'))
                    except Exception as e:
                        self.send_error(500, str(e))
                else:
                    self.send_error(404, "File not found")
            else:
                # If no path provided, return a default demo or error
                self.send_error(400, "Missing path parameter")

        elif parsed_path.path.startswith('/api/read'):
            query = urllib.parse.parse_qs(parsed_path.query)
            filepath = query.get('path', [None])[0]
            if filepath:
                full_path = os.path.join(WORKSPACE_ROOT, filepath)
                # Simple security check
                if os.path.exists(full_path):
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        self.send_response(200)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(content.encode('utf-8'))
                    except Exception as e:
                        self.send_error(500, str(e))
                else:
                    self.send_error(404, "File not found")
            else:
                self.send_error(400, "Missing path parameter")

        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/scrape':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            url = data.get('url')
            
            if url:
                print(f"DEBUG: Scraping {url}")
                title, content = scraper.fetch_and_convert(url)
                
                if title:
                    # Save to 00_Inbox
                    inbox_dir = os.path.join(WORKSPACE_ROOT, "00_Inbox")
                    if not os.path.exists(inbox_dir):
                        os.makedirs(inbox_dir)
                    
                    filename = f"{title}.md"
                    filepath = os.path.join(inbox_dir, filename)
                    
                    try:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"status": "success", "file": f"00_Inbox/{filename}"}).encode('utf-8'))
                    except Exception as e:
                        self.send_error(500, f"Save Error: {str(e)}")
                else:
                    self.send_error(500, f"Scrape Error: {content}") # content contains error msg
            else:
                self.send_error(400, "Missing URL")
            return

        if self.path == '/api/vision_ocr':
            # Placeholder for Vision OCR
            # In a real implementation, this would receive an image or capture screen,
            # run OCR (Tesseract/EasyOCR/WindowsOCR), and return text.
            
            # For prototype, we return a mock response based on the game mode if provided
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            game_mode = data.get('game_mode', 'general')
            
            mock_text = ""
            if game_mode == 'guigubahuang':
                mock_text = "[System] 천도筑基(축기) 경지에 도달했습니다.\n[Event] 의형제 '이무기'가 당신을 찾아왔습니다."
            elif game_mode == 'baldursgate3':
                mock_text = "[Dialogue] 아스타리온: \"피 냄새가 나는군...\"\n[Roll] 설득(Charisma): 15 (성공)"
            else:
                mock_text = "[System] OCR Module not fully installed.\n[Info] Please install Tesseract or enable Windows OCR."
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "text": mock_text}).encode('utf-8'))
            return

        if self.path == '/api/analyze':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            layer_type = data.get('type') # 'concept', 'code', or 'narrative'
            content = data.get('content')
            print(f"DEBUG: Received type={layer_type}, content_len={len(content) if content else 0}")
            
            result = {}
            
            if layer_type == 'code':
                # [Left Brain] Logic/Code Analysis
                gongmyung_lines = []
                for line in content.split('\n'):
                    line = line.strip()
                    if not line: continue
                    
                    # Simple Rule-Based Parsing
                    if line.startswith('print'):
                        gongmyung_lines.append(f"○'print'● call ◎ → stdout")
                    elif line.startswith('if'):
                        gongmyung_lines.append(f"○ condition ● check ◎ → branch")
                    elif line.startswith('def'):
                        gongmyung_lines.append(f"● function ≡ define")
                    elif '=' in line:
                        gongmyung_lines.append(f"○ variable ● assign ◎ → memory")
                    else:
                        gongmyung_lines.append(f"○ process ● execute ◎ → next")
                
                result['layer_6'] = '\n'.join(gongmyung_lines)
                result['layer_2'] = "1. Initialize\n2. Process Logic\n3. Output Result"
                
            elif layer_type == 'narrative':
                # [Right Brain] Omni-Perspective Analysis
                # 1. Narrative (Story) / 2. Chat (Conversation) / 3. Academic (Logic) / 4. Raw (Data)
                
                lines = [l for l in content.split('\n') if l.strip()]
                total_lines = len(lines)
                if total_lines == 0: return

                # --- 1. Narrative Perspective (서사적 관점) ---
                narrative_log = []
                keywords_turn = ['그러나', '하지만', '그런데', '갑자기', '반전', 'But', 'However']
                keywords_concl = ['결국', '마침내', '따라서', 'Finally', 'In the end']
                
                for i, line in enumerate(lines):
                    progress = (i + 1) / total_lines
                    if progress < 0.05 or progress > 0.95 or any(k in line for k in keywords_turn + keywords_concl):
                        phase = "起" if progress <= 0.25 else "承" if progress <= 0.5 else "轉" if progress <= 0.75 else "結"
                        symbol = "🌱" if phase=="起" else "🌿" if phase=="承" else "⚡" if phase=="轉" else "🍎"
                        narrative_log.append(f"{symbol} {phase}: {line[:40]}...")
                
                # --- 2. Chat Perspective (대화적 관점) ---
                chat_log = []
                chat_markers = ['User:', 'ChatGPT:', '나의 말:', 'ChatGPT의 말:', 'System:', 'Assistant:']
                chat_score = 0
                for line in lines:
                    if any(m in line for m in chat_markers):
                        chat_score += 1
                        clean_line = line
                        for m in chat_markers: clean_line = clean_line.replace(m, "")
                        speaker = "👤 User" if 'User' in line or '나의 말' in line else "🤖 AI"
                        chat_log.append(f"{speaker}: {clean_line.strip()[:40]}...")
                
                # --- 3. Academic Perspective (학술/논리적 관점) ---
                academic_log = []
                academic_keywords = ['정의', '개념', '분석', '결론', '연구', 'Chapter', 'Section', 'Abstract', '1.', '2.']
                academic_score = 0
                for line in lines:
                    if line.startswith('#') or any(line.strip().startswith(k) for k in ['1.', '2.', '-', '*']):
                        academic_score += 1
                        academic_log.append(f"📝 {line.strip()[:50]}")
                
                # --- 4. Raw Perspective (원형적 관점) ---
                raw_log = []
                char_count = sum(len(l) for l in lines)
                raw_log.append(f"📏 Total Lines: {total_lines}")
                raw_log.append(f"🔤 Total Chars: {char_count}")
                raw_log.append(f"📊 Avg Line Len: {char_count // total_lines if total_lines else 0}")

                # --- Synthesis (종합 분석) ---
                synthesis = []
                primary_type = "Unknown"
                
                # Determine Type
                if chat_score > total_lines * 0.1:
                    primary_type = "💬 Chat Log (대화 기록)"
                    synthesis.append(f"Main Focus: Interaction & QnA")
                    synthesis.append(f"User Intent: Detected {chat_score // 2} interactions.")
                elif academic_score > total_lines * 0.2:
                    primary_type = "🎓 Academic/Technical (논문/기술 문서)"
                    synthesis.append(f"Main Focus: Structure & Logic")
                    synthesis.append(f"Key Sections: {len(academic_log)} structural elements found.")
                else:
                    primary_type = "📖 Narrative/Story (소설/서사)"
                    synthesis.append(f"Main Focus: Flow & Emotion")
                    synthesis.append(f"Story Arc: Gi-Seung-Jeon-Gyeol detected.")

                # Construct Final Output
                final_output = []
                final_output.append(f"🔮 [Final Synthesis]: {primary_type}")
                final_output.append("-" * 30)
                final_output.extend(synthesis)
                final_output.append("\n" + "="*30)
                
                final_output.append("\n👁️ [1. Narrative View (서사)]")
                final_output.extend(narrative_log[:10]) # Show top 10
                if len(narrative_log) > 10: final_output.append(f"...(+{len(narrative_log)-10} more)")

                final_output.append("\n🗣️ [2. Chat View (대화)]")
                final_output.extend(chat_log[:10])
                if len(chat_log) > 10: final_output.append(f"...(+{len(chat_log)-10} more)")

                final_output.append("\n🎓 [3. Academic View (논리)]")
                final_output.extend(academic_log[:10])
                if len(academic_log) > 10: final_output.append(f"...(+{len(academic_log)-10} more)")

                final_output.append("\n📊 [4. Raw View (데이터)]")
                final_output.extend(raw_log)

                result['layer_6'] = '\n'.join(final_output)
                
                # Generate Table of Contents (Layer 2)
                toc_lines = ["# Analysis Report"]
                toc_lines.append(f"1. Type: {primary_type}")
                toc_lines.append("2. Perspectives:")
                toc_lines.append("   - Narrative (Flow)")
                toc_lines.append("   - Chat (Interaction)")
                toc_lines.append("   - Academic (Structure)")
                toc_lines.append("   - Raw (Statistics)")
                result['layer_2'] = '\n'.join(toc_lines)

            elif layer_type == 'concept':
                # Generate Structure (Layer 2) from Concept (Layer 1)
                # Extract headers if present, otherwise use template
                headers = [l.strip() for l in content.split('\n') if l.strip().startswith('#')]
                if headers:
                    result['layer_2'] = '\n'.join(headers)
                else:
                    result['layer_2'] = f"1. Define '{content[:20]}...'\n2. Analyze Requirements\n3. Design Algorithm"
                
                result['layer_3'] = "# Auto-generated skeleton\ndef main():\n    # TODO: Implement logic based on concept\n    pass"

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
            return

        if parsed_path.path == '/api/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            filepath = data.get('path')
            content = data.get('content')
            
            if filepath and content is not None:
                full_path = os.path.join(WORKSPACE_ROOT, filepath)
                try:
                    # Ensure directory exists
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
                except Exception as e:
                    self.send_error(500, str(e))
            else:
                self.send_error(400, "Missing parameters")

print(f"Serving Gongmyung Library at http://localhost:{PORT} from {WORKSPACE_ROOT}")
socketserver.TCPServer.allow_reuse_address = True
# Remove functools.partial and rely on os.chdir
with socketserver.TCPServer(("", PORT), GongmyungHandler) as httpd:
    httpd.serve_forever()
