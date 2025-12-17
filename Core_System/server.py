import http.server
import socketserver
import os
import urllib.parse
import datetime
import json
import glob

PORT = 3001
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(ROOT_DIR, 'public')
LIBRARY_DIR = os.path.join(ROOT_DIR, '..', 'Gongmyung_Library')

class GongmyungHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path_name = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)

        # 1. Root -> index.html
        if path_name == '/':
            self.path = '/index.html'
            return self.serve_static()

        # 2. Route Mappings
        if path_name == '/underworld':
            self.path = '/Underworld.html'
            return self.serve_static()
        
        if path_name == '/crepecake':
            self.path = '/CrepeCake.html'
            return self.serve_static()

        # 3. Login Page
        if path_name == '/login':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.get_login_html().encode('utf-8'))
            return

        # 4. Kaleidoscope
        if path_name == '/kaleidoscope':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.get_kaleidoscope_html().encode('utf-8'))
            return

        # 5. Library Listing
        if path_name.startswith('/library/'):
            category = path_name.split('/')[2]
            self.handle_library_listing(category)
            return

        # 6. Static Files
        return self.serve_static()

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/auth':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = urllib.parse.parse_qs(post_data)
            
            # Simple Auth Logic
            passphrase = params.get('passphrase', [''])[0]
            user_type = params.get('user_type', ['human'])[0]

            if passphrase:
                cookie_val = 'verified_ai' if user_type == 'ai' else 'verified_human'
                self.send_response(302)
                self.send_header('Set-Cookie', f'session={cookie_val}; HttpOnly')
                self.send_header('Location', '/')
                self.end_headers()
            else:
                self.send_response(401)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(b"<h1>Access Denied</h1><a href='/login'>Try Again</a>")
            return

    def serve_static(self):
        # Map request path to PUBLIC_DIR
        # self.path is like /index.html or /css/style.css
        
        # Security check: prevent escaping PUBLIC_DIR
        safe_path = self.path.lstrip('/')
        full_path = os.path.join(PUBLIC_DIR, safe_path)
        
        if not os.path.abspath(full_path).startswith(os.path.abspath(PUBLIC_DIR)):
            self.send_error(403, "Forbidden")
            return

        if os.path.exists(full_path) and os.path.isfile(full_path):
            self.directory = PUBLIC_DIR # Set directory for SimpleHTTPRequestHandler
            super().do_GET()
        else:
            self.send_error(404, f"File not found: {self.path}")

    def handle_library_listing(self, category):
        target_dir = os.path.join(LIBRARY_DIR, category)
        
        if not os.path.exists(target_dir) or not os.path.isdir(target_dir):
            self.send_error(404, "Library Category Not Found")
            return

        files = glob.glob(os.path.join(target_dir, '*'))
        file_list_html = ""
        
        for f in files:
            fname = os.path.basename(f)
            # Link to view file content (Not implemented fully in this snippet, but let's point to a viewer)
            # For now, just list them. To view, we'd need a /view/ route.
            # Let's assume we just list them for now.
            file_list_html += f'<li><a href="#">{fname}</a></li>'

        html = f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>{category} - Gongmyung Library</title>
            <style>
                body {{ font-family: 'Malgun Gothic', sans-serif; padding: 20px; background: #f0f2f5; }}
                h1 {{ color: #333; }}
                ul {{ list-style: none; padding: 0; }}
                li {{ background: white; margin: 10px 0; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
                a {{ text-decoration: none; color: #007bff; font-weight: bold; }}
                .back-btn {{ display: inline-block; margin-bottom: 20px; padding: 8px 15px; background: #333; color: white; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <a href="/" class="back-btn">⬅ Back to Lobby</a>
            <h1>📂 {category}</h1>
            <ul>{file_list_html}</ul>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def get_login_html(self):
        return """
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>System Access Control</title>
            <style>
                body {
                    margin: 0; padding: 0; font-family: 'Malgun Gothic', sans-serif;
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                    color: white; height: 100vh; display: flex; justify-content: center; align-items: center;
                }
                .login-card {
                    width: 400px; padding: 40px; background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px;
                    backdrop-filter: blur(10px); text-align: center;
                }
                input { width: 100%; padding: 15px; margin-bottom: 20px; border-radius: 10px; border: none; }
                button { width: 100%; padding: 15px; background: #007bff; color: white; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="login-card">
                <h1>🔐 Access Control</h1>
                <p>Identity verification required.</p>
                <form action="/auth" method="POST">
                    <input type="hidden" name="user_type" value="human">
                    <input type="password" name="passphrase" placeholder="Enter passphrase..." required autofocus>
                    <button type="submit">Verify</button>
                </form>
            </div>
        </body>
        </html>
        """

    def get_kaleidoscope_html(self):
        return """
        <!DOCTYPE html>
        <html><body><h1>🔮 Kaleidoscope</h1><p>Not fully implemented in Python version yet.</p></body></html>
        """

print(f"Starting Gongmyung Server (Python) on port {PORT}...")
print(f"Root Dir: {ROOT_DIR}")
print(f"Public Dir: {PUBLIC_DIR}")

with socketserver.TCPServer(("", PORT), GongmyungHandler) as httpd:
    print("Server started.")
    httpd.serve_forever()
