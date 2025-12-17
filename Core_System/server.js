const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT_DIR = __dirname;
const LOG_FILE = path.join(__dirname, 'debug_server.log');
function log(msg) {
    fs.appendFileSync(LOG_FILE, `[${new Date().toISOString()}] ${msg}\n`);
}

log(`Server starting... ROOT_DIR=${ROOT_DIR}`);

process.on('exit', (code) => {
    log(`Process exited with code: ${code}`);
});

process.on('uncaughtException', (err) => {
    log(`UNCAUGHT EXCEPTION: ${err.stack}`);
});

process.on('unhandledRejection', (reason, p) => {
    log(`UNHANDLED REJECTION: ${reason}`);
});

const PORT = 3001;

// --- Translation / i18n Structure ---
const translations = {
    'ko': {
        'gatekeeper_title': '시스템 접근 제어',
        'gatekeeper_prompt': '신원 확인이 필요합니다. 암호를 대십시오.',
        'gatekeeper_placeholder': '암호를 입력하세요...',
        'gatekeeper_submit': '확인',
        'access_denied': '접근 거부: 신원이 확인되지 않았습니다.',
        'library_title': '공명 도서관',
        'back_to_lobby': '⬅ 로비로 돌아가기',
        'basic_genre': '📂 기본 장르 (Categories)',
        'user_files': '👤 사용자 파일 (User Files)',
        'add_file': '파일 추가',
        'construction_msg': '🚧 파일 추가 기능은 공사 중입니다.\n(토론장에서 의견을 남겨주세요!)'
    },
    'en': {
        'gatekeeper_title': 'System Access Control',
        'gatekeeper_prompt': 'Identity verification required. State the passphrase.',
        'gatekeeper_placeholder': 'Enter passphrase...',
        'gatekeeper_submit': 'Verify',
        'access_denied': 'Access Denied: Identity not verified.',
        'library_title': 'Gongmyung Library',
        'back_to_lobby': '⬅ Back to Lobby',
        'basic_genre': '📂 Categories',
        'user_files': '👤 User Files',
        'add_file': 'Add File',
        'construction_msg': '🚧 Feature under construction.\n(Please leave feedback in the discussion area!)'
    }
};
const LANG = 'ko'; // Default Language

const mimeTypes = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.gif': 'image/gif',
    '.txt': 'text/plain'
};

// --- Session / Security Mock ---
// In a real app, use express-session or cookies. Here, we use a simple in-memory set for demo.
// Since Node restarts clear memory, this acts as a "per-run" session.
// For a persistent login across restarts without DB, we'd need a file-based session, but let's keep it simple.
// We will use a cookie-like approach manually.
const sessions = new Set(); 

const server = http.createServer((req, res) => {
    const requestUrl = req.url.split('?')[0];
    let safeUrl = decodeURI(requestUrl);

    // --- AI Gatekeeper Logic ---
    // Check for cookie
    const cookie = req.headers.cookie;
    const isAuthenticated = cookie && cookie.includes('session=verified_human');

    // Allow static assets (css, js, images) without login to prevent broken pages
    const isAsset = safeUrl.match(/\.(css|js|png|jpg|gif|ico)$/);

    /* [MODIFIED] Auto-redirect disabled by user request.
    if (!isAuthenticated && safeUrl !== '/login' && safeUrl !== '/auth' && !isAsset) {
        // Redirect to AI Gatekeeper
        res.writeHead(302, { 'Location': '/login' });
        res.end();
        return;
    }
    */

    // Handle Login Page (The Gatekeeper)
    if (safeUrl === '/login') {
        const t = translations[LANG];
        const html = `
        <!DOCTYPE html>
        <html lang="${LANG}">
        <head>
            <meta charset="UTF-8">
            <title>${t.gatekeeper_title}</title>
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    font-family: 'Malgun Gothic', sans-serif;
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                    color: white;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    overflow: hidden;
                }
                
                .stars {
                    position: absolute;
                    top: 0; left: 0; width: 100%; height: 100%;
                    pointer-events: none; z-index: 0;
                }
                .star {
                    position: absolute; background: white; border-radius: 50%;
                    opacity: 0.5; animation: twinkle 2s infinite ease-in-out;
                }
                @keyframes twinkle { 0%, 100% { opacity: 0.2; transform: scale(0.8); } 50% { opacity: 0.8; transform: scale(1.2); } }

                .login-card {
                    position: relative;
                    z-index: 1;
                    width: 400px;
                    padding: 40px;
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 15px 35px rgba(0,0,0,0.5);
                    text-align: center;
                }

                h1 { margin-bottom: 10px; font-size: 2rem; text-shadow: 0 0 10px rgba(255,255,255,0.5); }
                p { color: #ccc; margin-bottom: 30px; line-height: 1.5; }

                input {
                    width: 100%;
                    padding: 15px;
                    margin-bottom: 20px;
                    background: rgba(0, 0, 0, 0.3);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    color: white;
                    font-size: 1rem;
                    outline: none;
                    box-sizing: border-box;
                    transition: 0.3s;
                }
                input:focus { border-color: #007bff; box-shadow: 0 0 10px rgba(0, 123, 255, 0.3); }

                button {
                    width: 100%;
                    padding: 15px;
                    background: linear-gradient(45deg, #007bff, #00d2d3);
                    border: none;
                    border-radius: 10px;
                    color: white;
                    font-size: 1.1rem;
                    font-weight: bold;
                    cursor: pointer;
                    transition: 0.3s;
                    box-shadow: 0 5px 15px rgba(0, 123, 255, 0.3);
                }
                button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0, 123, 255, 0.5); }

                .mode-switch {
                    margin-top: 20px;
                    font-size: 0.9rem;
                    color: #888;
                    cursor: pointer;
                }
                .mode-switch:hover { color: white; text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="stars" id="stars"></div>
            
            <div class="login-card">
                <h1>🔐 Access Control</h1>
                <p>${t.gatekeeper_prompt}</p>
                
                <form action="/auth" method="POST">
                    <input type="hidden" name="user_type" id="user_type" value="human">
                    <input type="password" name="passphrase" placeholder="${t.gatekeeper_placeholder}" required autofocus>
                    <button type="submit">${t.gatekeeper_submit}</button>
                </form>

                <div class="mode-switch" onclick="toggleMode()">🤖 Switch to AI Mode</div>
            </div>

            <script>
                // Stars Effect
                const starsContainer = document.getElementById('stars');
                for(let i=0; i<50; i++) {
                    const star = document.createElement('div');
                    star.className = 'star';
                    star.style.width = Math.random() * 3 + 'px';
                    star.style.height = star.style.width;
                    star.style.left = Math.random() * 100 + '%';
                    star.style.top = Math.random() * 100 + '%';
                    star.style.animationDelay = Math.random() * 2 + 's';
                    starsContainer.appendChild(star);
                }

                function toggleMode() {
                    const input = document.getElementById('user_type');
                    const btn = document.querySelector('.mode-switch');
                    if (input.value === 'human') {
                        input.value = 'ai';
                        btn.innerText = '👤 Switch to Human Mode';
                        document.querySelector('h1').innerText = '🤖 AI Protocol';
                        document.querySelector('button').style.background = 'linear-gradient(45deg, #ff00cc, #333399)';
                    } else {
                        input.value = 'human';
                        btn.innerText = '🤖 Switch to AI Mode';
                        document.querySelector('h1').innerText = '🔐 Access Control';
                        document.querySelector('button').style.background = 'linear-gradient(45deg, #007bff, #00d2d3)';
                    }
                }
            </script>
        </body>
        </html>
        `;
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(html);
        return;
    }

    // Handle Auth Request
    if (safeUrl === '/auth' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            // Simple parsing of form data
            const params = new URLSearchParams(body);
            const passphrase = params.get('passphrase');
            const userType = params.get('user_type');
            
            // The "Secret" Answer (In reality, this could be dynamic)
            // For now, let's accept anything non-empty or a specific keyword like "human" or "gongmyung"
            // Let's make it easy for the user: "open" or just non-empty for now to test.
            if (passphrase && passphrase.trim().length > 0) {
                const cookieValue = userType === 'ai' ? 'verified_ai' : 'verified_human';
                res.writeHead(302, { 
                    'Set-Cookie': `session=${cookieValue}; HttpOnly`,
                    'Location': '/' 
                });
                res.end();
            } else {
                res.writeHead(401, { 'Content-Type': 'text/html; charset=utf-8' });
                res.end(`<h1>${translations[LANG].access_denied}</h1><a href="/login">Try Again</a>`);
            }
        });
        return;
    }

    // Handle Root
    if (safeUrl === '/') {
        safeUrl = '/index.html';
    }

    // Handle Underworld Page
    if (safeUrl === '/underworld') {
        safeUrl = '/Underworld.html';
    }

    // Handle CrepeCake Page
    if (safeUrl === '/crepecake') {
        safeUrl = '/CrepeCake.html';
    }

    // Handle Library Listing (Dynamic)
    if (safeUrl.startsWith('/library/')) {
        const libType = safeUrl.split('/')[2];
        const dirPath = path.join(ROOT_DIR, '../Gongmyung_Library', libType);

        if (fs.existsSync(dirPath) && fs.lstatSync(dirPath).isDirectory()) {
            fs.readdir(dirPath, (err, files) => {
                if (err) {
                    res.writeHead(500);
                    res.end("Error reading directory");
                    return;
                }
                
                const t = translations[LANG];

                const html = `
                <!DOCTYPE html>
                <html lang="${LANG}">
                <head>
                    <meta charset="UTF-8">
                    <title>${libType} - ${t.library_title}</title>
                    <style>
                        body { font-family: 'Malgun Gothic', sans-serif; background-color: #f0f2f5; padding: 20px; transition: background 0.3s; }
                        h1 { color: #333; }
                        
                        /* Grid Layout (Bookshelf) */
                        .book-shelf { 
                            display: grid; 
                            grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); 
                            gap: 25px; 
                            margin-top: 20px; 
                            padding: 30px;
                            background-color: #fff;
                            border-radius: 20px;
                            box-shadow: inset 0 0 20px rgba(0,0,0,0.05);
                            border: 1px solid #e0e0e0;
                        }

                        .book { 
                            height: 200px; background: white; 
                            border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.08);
                            display: flex; align-items: center; justify-content: center;
                            text-align: center; padding: 15px; cursor: pointer;
                            transition: all 0.2s ease;
                            text-decoration: none; color: #333; font-weight: bold;
                            flex-direction: column;
                            position: relative;
                            overflow: hidden;
                            border: 1px solid rgba(0,0,0,0.05);
                        }
                        .book:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.12); border-color: #007bff; }
                        
                        /* Type Styles */
                        .type-basic { background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%); border-bottom: 4px solid #007bff; } /* Folders */
                        .type-user { background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 100%); border-bottom: 4px solid #28a745; } /* Files */
                        
                        /* Add File Button Style */
                        .book.add-file-btn {
                            border: 2px dashed #ccc !important;
                            background: transparent !important;
                            color: #aaa !important;
                            box-shadow: none;
                        }
                        .book.add-file-btn:hover {
                            border-color: #28a745 !important;
                            color: #28a745 !important;
                            background: rgba(40, 167, 69, 0.05) !important;
                        }

                        .back-btn { display: inline-block; margin-bottom: 20px; padding: 10px 20px; background: #333; color: white; text-decoration: none; border-radius: 5px; }
                        .icon { font-size: 3.5rem; margin-bottom: 10px; filter: drop-shadow(0 2px 3px rgba(0,0,0,0.1)); }
                        
                        /* Toggle Button Style */
                        #current-mode-label {
                            margin-bottom: 10px; font-size: 1.2rem; font-weight: bold; color: #555;
                            cursor: pointer; display: inline-flex; align-items: center; gap: 10px;
                            padding: 8px 15px; border-radius: 10px; transition: all 0.2s;
                            border: 2px solid transparent;
                        }
                        #current-mode-label:hover { background: rgba(0,0,0,0.05); border-color: rgba(0,0,0,0.1); }
                        #current-mode-label:active { transform: scale(0.98); }
                    </style>
                </head>
                <body>
                    <a href="/" class="back-btn">${t.back_to_lobby}</a>
                    <h1>📚 ${libType}</h1>
                    
                    <div id="current-mode-label" onclick="toggleView()">
                        ${t.basic_genre} <span style="font-size:0.8em; opacity:0.5;">🔄</span>
                    </div>

                    <div class="book-shelf">
                        ${files.map(file => {
                            const isDir = fs.lstatSync(path.join(dirPath, file)).isDirectory();
                            const typeClass = isDir ? 'type-basic' : 'type-user';
                            const icon = isDir ? '📂' : '📄';
                            const link = isDir ? `/library/${libType}/${file}` : `/view/${libType}/${file}`;
                            return `
                            <a href="${link}" class="book ${typeClass}" data-type="${isDir ? 'basic' : 'user'}">
                                <div class="icon">${icon}</div>
                                <div>${file}</div>
                                <div style="font-size:0.8rem; color:#666; margin-top:5px;">${isDir ? '기본 분류' : '사용자 파일'}</div>
                            </a>
                            `;
                        }).join('')}
                        
                        <!-- Add File Button (User Mode Only) -->
                        <div class="book type-user add-file-btn" data-type="user" onclick="alert('${t.construction_msg.replace(/\n/g, '\\n')}')">
                            <div class="icon">➕</div>
                            <div>${t.add_file}</div>
                        </div>
                    </div>

                    <script>
                        let currentMode = 'basic'; // 'basic' (Folders) or 'user' (Files)
                        const label = document.getElementById('current-mode-label');
                        const books = document.querySelectorAll('.book');

                        function updateView() {
                            books.forEach(book => {
                                if (book.dataset.type === currentMode) {
                                    book.style.display = 'flex';
                                    setTimeout(() => book.style.opacity = '1', 50);
                                } else {
                                    book.style.display = 'none';
                                    book.style.opacity = '0';
                                }
                            });

                            if (currentMode === 'basic') {
                                label.innerHTML = '${t.basic_genre} <span style="font-size:0.8em; opacity:0.5;">🔄</span>';
                                label.style.color = '#007bff';
                            } else {
                                label.innerHTML = '${t.user_files} <span style="font-size:0.8em; opacity:0.5;">🔄</span>';
                                label.style.color = '#28a745';
                            }
                        }

                        function toggleView() {
                            currentMode = currentMode === 'basic' ? 'user' : 'basic';
                            updateView();
                        }

                        // Initial Run
                        updateView();
                    </script>
                </body>
                </html>
                `;
                res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                res.end(html);
            });
            return;
        }
    }

    // Handle File Viewing (Novel Mode)
    if (safeUrl.startsWith('/view/')) {
        const parts = safeUrl.split('/');
        const relativePath = parts.slice(2).join('/'); 
        const filePath = path.join(ROOT_DIR, relativePath);

        if (fs.existsSync(filePath)) {
            // --- Logging System ---
            const cookies = req.headers.cookie || '';
            const userType = cookies.includes('verified_ai') ? 'AI' : (cookies.includes('verified_human') ? 'Human' : 'Guest');
            const logEntry = `[${new Date().toISOString()}] User: ${userType} | Accessed: ${relativePath}\n`;
            const logPath = path.join(ROOT_DIR, 'logs', 'access.log');
            
            fs.appendFile(logPath, logEntry, (err) => {
                if (err) console.error("Logging failed", err);
            });
            // ---------------------

            fs.readFile(filePath, 'utf8', (err, content) => {
                if (err) {
                    res.writeHead(500);
                    res.end("Error reading file");
                    return;
                }

                // --- Simple Flow Parser ---
                const lines = content.split('\n');
                const flowRegex = /(@flow:[a-zA-Z0-9_-]+)(.*)/;
                let nodes = [];
                let flowSum = 0;
                let isMonetized = false;

                lines.forEach((line, index) => {
                    const match = line.match(flowRegex);
                    if (match) {
                        const tag = match[1];
                        let description = match[2].trim();
                        const lineNumber = index + 1;
                        
                        // Check for Monetization Tag
                        if (tag.includes('monetize')) {
                            isMonetized = true;
                        }

                        // Check for Category Tag (e.g., @flow:tag [Game])
                        if (tag.includes('tag')) {
                            const tagMatch = description.match(/\[(.*?)\]/);
                            if (tagMatch) {
                                const category = tagMatch[1];
                                description = `🏷️ 태그: ${category}`;
                                icon = '🏷️';
                                flowValue = 0;
                                type = 'meta';
                            }
                        }

                        // --- Visualizing the "Flow" (~ and ->) ---
                        // ~ : The process of calculation/time (Wave)
                        // -> : The transition of state (Arrow)
                        description = description.replace(/~/g, '<span class="flow-wave">~</span>');
                        description = description.replace(/->/g, '<span class="flow-arrow">→</span>');

                        let codeSnippet = "";
                        if (index + 1 < lines.length) {
                            codeSnippet = lines[index + 1].trim();
                        }

                        let icon = '◎';
                        let flowValue = 2;
                        let type = 'process';

                        if (tag.includes('seal')) { icon = '🔒'; flowValue = 0; type = 'meta'; }
                        else if (tag.includes('monetize')) { icon = '💰'; flowValue = 0; type = 'meta'; }
                        else if (tag.includes('start')) { icon = '○'; flowValue = 1; type = 'start'; }
                        else if (tag.includes('end')) { icon = '●'; flowValue = 4; type = 'end'; }
                        else if (tag.includes('branch')) { icon = '◇'; flowValue = 3; type = 'branch'; }
                        else if (tag.includes('error') || tag.includes('fail')) { icon = '※'; flowValue = 0; type = 'error'; }
                        
                        nodes.push({ icon, description, lineNumber, flowValue, type, codeSnippet });
                        if (flowValue > 0) flowSum += flowValue;
                    }
                });
                // ---------------------------

                // --- 3-Month Rule Logic ---
                const stats = fs.statSync(filePath);
                const lastModified = new Date(stats.mtime);
                const now = new Date();
                const diffTime = Math.abs(now - lastModified);
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                const isExpired = diffDays > 90;

                // --- Author Verification Logic (No ID, No Money) ---
                // Check if @flow:author tag exists
                let authorName = 'Anonymous';
                let isVerified = false;
                
                lines.forEach(line => {
                    const match = line.match(/@flow:author\s+\[(.*?)\]/);
                    if (match) {
                        authorName = match[1];
                        isVerified = true;
                    }
                });

                // If Code/AI section and not verified, disable monetization
                if (filePath.includes('Code_AI') && !isVerified) {
                    isMonetized = false;
                }

                // --- Economic System (The Watt Standard) ---
                const ELECTRICITY_RATE_KRW = 150; // 1 GP = 1 kWh Cost (approx. 150 KRW)
                
                // Energy Calculation Formula
                const fileSizeKB = stats.size / 1024;
                const storageCost = fileSizeKB * 0.1; // 0.1 GP per KB (Storage Energy)
                const processingCost = lines.length * 0.01; // 0.01 GP per Line (Processing Energy)
                const cognitiveCost = flowSum * 0.5; // 0.5 GP per Flow (Cognitive Energy)
                
                const totalGP = (storageCost + processingCost + cognitiveCost).toFixed(2);
                const totalKRW = Math.round(totalGP * ELECTRICITY_RATE_KRW).toLocaleString();

                // --- Revenue Distribution Logic ---
                let distributionHtml = '';
                if (filePath.includes('Literature')) {
                    // Literature: 1:9 (Library:Creator)
                    distributionHtml = `수익 분배: 🏛️도서관(10%) | ✍️작가(90%) <br><span style="font-size:0.8em; color:#666;">(문학의 전당: 창작자 중심 분배)</span>`;
                } else if (filePath.includes('Physics_Math')) {
                    // Science: 2:2:6 (Library:Original:Creator)
                    distributionHtml = `수익 분배: 🏛️도서관(20%) | 📜원천이론(20%) | 🧪구현자(60%) <br><span style="font-size:0.8em; color:#666;">(이치의 탑: 학문적 존중 분배)</span>`;
                } else {
                    // Code/AI (Default): 6:1:1:2 (Library:Creator:Field:Reserve)
                    distributionHtml = `수익 분배: 🏛️언더월드(60%) | 💻코더(10%) | 🌱분야발전(10%) | 🛡️예비비(20%) <br><span style="font-size:0.8em; color:#666;">(코드의 숲: AI 방어 및 공익 분배)</span>`;
                }

                let statusBadge = '';
                let adBanner = '';

                if (isMonetized) {
                    if (isExpired) {
                        statusBadge = `<span style="background:#ffc107; color:#333; padding:5px 10px; border-radius:15px; font-size:0.8em;">💤 관리 필요 (${diffDays}일 전 수정됨)</span>`;
                        adBanner = `<div style="background:#f8d7da; color:#721c24; padding:10px; margin-bottom:20px; border-radius:5px; text-align:center;">⚠️ 관리 부재로 인해 광고 수익이 일시 정지되었습니다. (3개월 경과)</div>`;
                    } else {
                        statusBadge = `<span style="background:#28a745; color:white; padding:5px 10px; border-radius:15px; font-size:0.8em;">💰 수익 창출 중 (D-${90-diffDays})</span>`;
                        adBanner = `
                        <div style="background:#d4edda; color:#155724; padding:20px; margin-bottom:20px; border-radius:10px; border: 1px solid #c3e6cb; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                            <div style="font-weight:bold; font-size:1.2em; margin-bottom:15px; border-bottom: 1px solid #155724; padding-bottom: 10px;">
                                ⚡ 에너지 가치 영수증 (Energy Receipt)
                            </div>
                            <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-size:0.9em;">
                                <span>💾 보존 에너지 (Storage):</span>
                                <span>${storageCost.toFixed(2)} GP</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-size:0.9em;">
                                <span>⚙️ 연산 에너지 (Processing):</span>
                                <span>${processingCost.toFixed(2)} GP</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; margin-bottom:15px; font-size:0.9em;">
                                <span>🧠 인지 에너지 (Cognitive):</span>
                                <span>${cognitiveCost.toFixed(2)} GP</span>
                            </div>
                            <div style="background:rgba(255,255,255,0.5); padding:10px; border-radius:5px; text-align:right;">
                                <div style="font-size:0.9em; color:#555;">총 에너지 가치</div>
                                <div style="font-size:1.5em; font-weight:bold; color:#28a745;">${totalGP} GP</div>
                                <div style="font-size:0.9em; color:#555;">(약 ￦${totalKRW})</div>
                            </div>
                            <div style="font-size:0.8em; margin-top:15px; text-align:center; color:#666; border-top:1px solid #c3e6cb; padding-top:10px;">
                                ${distributionHtml}
                            </div>
                        </div>`;
                    }
                } else {
                    let reason = "자유 기고";
                    if (filePath.includes('Code_AI') && !isVerified) reason = "비회원 (수익 불가)";
                    statusBadge = `<span style="background:#17a2b8; color:white; padding:5px 10px; border-radius:15px; font-size:0.8em;">🔰 ${reason}</span>`;
                }
                // ---------------------------

                let contentHtml = '';
                if (nodes.length > 0) {
                    // Novel View
                    contentHtml = `
                    ${adBanner}
                    <div class="novel-header">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span>🌊 흐름 서명: ${flowSum}</span>
                            ${statusBadge}
                        </div>
                    </div>
                    <table class="novel-table">
                        <thead>
                            <tr>
                                <th width="40%">공명 (Resonance)</th>
                                <th width="50%">현실 (Code)</th>
                                <th width="10%">위치</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${nodes.map(node => `
                                <tr class="type-${node.type}">
                                    <td class="resonance">
                                        <span class="icon">${node.icon}</span>
                                        <span class="desc">${node.description}</span>
                                    </td>
                                    <td class="code"><code>${node.codeSnippet || '<span style="color:#ccc">(코드 없음)</span>'}</code></td>
                                    <td class="line">${node.lineNumber}행</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                    <div style="margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px;">
                        <h3>📜 원본 코드</h3>
                        <pre>${content}</pre>
                    </div>
                    `;
                } else {
                    // Raw View
                    contentHtml = `<pre>${content}</pre>`;
                }

                const html = `
                <!DOCTYPE html>
                <html lang="ko">
                <head>
                    <meta charset="UTF-8">
                    <title>${path.basename(filePath)}</title>
                    <style>
                        body { font-family: 'Malgun Gothic', sans-serif; padding: 20px; line-height: 1.6; background: #fff; max-width: 1000px; margin: 0 auto; }
                        pre { white-space: pre-wrap; background: #f8f9fa; padding: 15px; border-radius: 5px; border: 1px solid #eee; font-family: 'Consolas', monospace; }
                        .back-btn { display: inline-block; margin-bottom: 20px; padding: 8px 15px; background: #333; color: white; text-decoration: none; border-radius: 5px; font-size: 0.9rem; }
                        
                        /* Novel Table Styles */
                        .novel-table { width: 100%; border-collapse: collapse; margin-top: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
                        .novel-table th { background: #f1f3f5; padding: 12px; text-align: left; border-bottom: 2px solid #dee2e6; color: #495057; }
                        .novel-table td { padding: 12px; border-bottom: 1px solid #eee; vertical-align: middle; }
                        .novel-table tr:hover { background-color: #f8f9fa; }
                        
                        .icon { font-size: 1.2rem; margin-right: 8px; display: inline-block; width: 25px; text-align: center; }
                        .desc { font-weight: bold; color: #343a40; }
                        .code code { font-family: 'Consolas', monospace; color: #007bff; background: #e7f5ff; padding: 2px 6px; border-radius: 3px; font-size: 0.9rem; }
                        .line { color: #adb5bd; font-size: 0.8rem; text-align: center; }
                        
                        .type-start .icon { color: #28a745; }
                        .type-end .icon { color: #dc3545; }
                        .type-branch .icon { color: #ffc107; }
                        .type-meta { background-color: #fff9db; }
                        
                        /* Flow Markers Animation */
                        .flow-wave { color: #007bff; font-weight: bold; display: inline-block; animation: wave 1.5s infinite ease-in-out; }
                        .flow-arrow { color: #28a745; font-weight: bold; font-size: 1.2em; vertical-align: middle; }
                        
                        @keyframes wave { 
                            0%, 100% { transform: translateY(0); opacity: 0.5; } 
                            50% { transform: translateY(-3px); opacity: 1; } 
                        }

                        .novel-header { background: #e9ecef; padding: 15px; border-radius: 5px; margin-bottom: 20px; font-weight: bold; border-left: 5px solid #333; }
                    </style>
                </head>
                <body>
                    <a href="javascript:history.back()" class="back-btn">⬅ 뒤로가기</a>
                    <h2>📄 ${path.basename(filePath)}</h2>
                    ${contentHtml}
                </body>
                </html>
                `;
                res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                res.end(html);
            });
            return;
        }
    }

    // --- Kaleidoscope Tool ---
    if (safeUrl === '/kaleidoscope') {
        const html = `
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>🔮 만화경 (Kaleidoscope)</title>
            <style>
                body { background: #111; color: #eee; font-family: 'Consolas', monospace; padding: 20px; text-align: center; }
                h1 { color: #d63384; text-shadow: 0 0 10px #d63384; }
                .container { max-width: 800px; margin: 0 auto; }
                textarea { width: 100%; height: 150px; background: #222; color: #fff; border: 1px solid #444; padding: 15px; font-size: 1.2rem; border-radius: 10px; }
                button { margin-top: 20px; padding: 10px 30px; font-size: 1.2rem; background: #d63384; color: white; border: none; border-radius: 50px; cursor: pointer; transition: 0.3s; }
                button:hover { transform: scale(1.1); box-shadow: 0 0 20px #d63384; }
                #output { margin-top: 40px; font-size: 2rem; line-height: 1.5; min-height: 100px; display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; }
                .symbol { padding: 10px; border-radius: 5px; background: rgba(255,255,255,0.1); animation: pop 0.3s ease-out; }
                .s-start { color: #28a745; } /* ○ */
                .s-end { color: #dc3545; } /* ● */
                .s-process { color: #ffc107; } /* ◎ */
                .s-flow { color: #0dcaf0; } /* ~ */
                @keyframes pop { from { transform: scale(0); } to { transform: scale(1); } }
                .back-btn { position: absolute; top: 20px; left: 20px; color: #666; text-decoration: none; }
            </style>
        </head>
        <body>
            <a href="/" class="back-btn">⬅ 로비</a>
            <div class="container">
                <h1>🔮 Kaleidoscope Engine</h1>
                <p>코드를 입력하면 공명문 기호로 변환합니다.</p>
                <textarea id="input" placeholder="여기에 코드를 입력하세요... (예: print('Hello'))"></textarea>
                <br>
                <button onclick="translateCode()">👁️ 만화경으로 보기</button>
                <div id="output"></div>
            </div>
            <script>
                function translateCode() {
                    const input = document.getElementById('input').value;
                    const output = document.getElementById('output');
                    output.innerHTML = '';

                    // Simple Regex-based Tokenizer for Demo
                    // This is a "Toy" version of the Kaleidoscope Logic
                    const tokens = input.split(/\\s+/);
                    
                    tokens.forEach((token, index) => {
                        setTimeout(() => {
                            let symbol = '';
                            let cls = '';
                            
                            if (token.match(/^(if|for|while|def|function)/)) {
                                symbol = '○ [' + token + ']';
                                cls = 's-start';
                            } else if (token.match(/(\(|\)|\[|\]|\{|\})/)) {
                                symbol = '◎ ' + token;
                                cls = 's-process';
                            } else if (token.match(/(=|\+|-|\*|\/)/)) {
                                symbol = '~';
                                cls = 's-flow';
                            } else if (token.match(/return|end|;|}/)) {
                                symbol = '●';
                                cls = 's-end';
                            } else {
                                symbol = '● [' + token + ']';
                                cls = 's-end';
                            }

                            // Special Case for print
                            if (token.includes('print') || token.includes('console')) {
                                symbol = '◎ [' + token + ']';
                                cls = 's-process';
                            }

                            const span = document.createElement('span');
                            span.className = 'symbol ' + cls;
                            span.innerText = symbol;
                            output.appendChild(span);
                            
                            // Add flow arrow
                            if (index < tokens.length - 1) {
                                const arrow = document.createElement('span');
                                arrow.className = 'symbol s-flow';
                                arrow.innerText = '→';
                                output.appendChild(arrow);
                            }

                        }, index * 200); // Sequential Animation
                    });
                }
            </script>
        </body>
        </html>
        `;
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(html);
        return;
    }

    // --- CrepeCake Tool ---
    if (safeUrl === '/crepecake') {
        const html = `
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>🍰 공명 크레이프케이크 (CrepeCake)</title>
            <style>
                body { background: #f0f2f5; font-family: 'Malgun Gothic', sans-serif; display: flex; flex-direction: column; align-items: center; padding: 50px; }
                h1 { color: #333; margin-bottom: 50px; }
                .cake-container { position: relative; width: 600px; perspective: 1000px; margin-top: 50px; }
                .layer {
                    width: 100%; height: 60px; margin-bottom: -20px;
                    background: white; border-radius: 10px;
                    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                    display: flex; align-items: center; justify-content: space-between;
                    padding: 0 30px; box-sizing: border-box;
                    font-weight: bold; font-size: 1.2rem;
                    transition: 0.5s; cursor: pointer;
                    position: relative; z-index: 1;
                    border: 1px solid rgba(0,0,0,0.05);
                }
                .layer:hover { transform: translateZ(20px) translateY(-10px); z-index: 10; background: #fff; box-shadow: 0 20px 40px rgba(0,0,0,0.2); }
                
                .l-prompt { background: linear-gradient(to right, #ff9a9e, #fecfef); color: #fff; }
                .l-gongmyung { background: linear-gradient(to right, #a18cd1, #fbc2eb); color: #fff; }
                .l-code { background: linear-gradient(to right, #84fab0, #8fd3f4); color: #fff; }
                .l-formula { background: linear-gradient(to right, #ffecd2, #fcb69f); color: #fff; }
                .l-binary { background: linear-gradient(to right, #333, #555); color: #fff; }

                .desc { font-size: 0.9rem; opacity: 0.8; font-weight: normal; }
                .back-btn { position: absolute; top: 20px; left: 20px; color: #333; text-decoration: none; }
                
                .red-thread {
                    position: absolute; left: 50%; top: 0; bottom: 0; width: 2px; background: red;
                    z-index: 0; opacity: 0.5; box-shadow: 0 0 5px red;
                }
            </style>
        </head>
        <body>
            <a href="/" class="back-btn">⬅ 로비</a>
            <h1>🍰 Gongmyung CrêpeCake Architecture</h1>
            
            <div class="cake-container">
                <div class="red-thread"></div>
                
                <div class="layer l-prompt" onclick="alert('1층: 사용자의 의도(Intent)가 담긴 프롬프트 층입니다.')">
                    <span>1. Prompt</span>
                    <span class="desc">의도 (Intent)</span>
                </div>
                <div class="layer l-gongmyung" onclick="alert('2층: 구조적 설계를 담당하는 공명문 층입니다. (●○◎)')">
                    <span>2. Gongmyung</span>
                    <span class="desc">구조 (Structure)</span>
                </div>
                <div class="layer l-code" onclick="alert('3층: 실제 실행되는 코드 층입니다. (Python/JS)')">
                    <span>3. Code</span>
                    <span class="desc">구현 (Implementation)</span>
                </div>
                <div class="layer l-formula" onclick="alert('4층: 논리적 검증을 위한 수식 층입니다.')">
                    <span>4. Formula</span>
                    <span class="desc">검증 (Verification)</span>
                </div>
                <div class="layer l-binary" onclick="alert('5층: 기계어 레벨의 실행 층입니다. (010101)')">
                    <span>5. Binary</span>
                    <span class="desc">실행 (Execution)</span>
                </div>
            </div>
            
            <div style="margin-top: 50px; color: #666;">
                * 각 레이어를 클릭하여 상세 설명을 확인하세요.
            </div>
        </body>
        </html>
        `;
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(html);
        return;
    }

    // Serve Static Files
    const filePath = path.join(ROOT_DIR, 'public', safeUrl);
    const extname = String(path.extname(filePath)).toLowerCase();
    const contentType = mimeTypes[extname] || 'application/octet-stream';

    fs.readFile(filePath, (error, content) => {
        if (error) {
            if(error.code == 'ENOENT'){
                res.writeHead(404);
                res.end('File not found');
            } else {
                res.writeHead(500);
                res.end('Sorry, check with the site admin for error: '+error.code+' ..\n');
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        }
    });
});

server.on('error', (e) => {
    log(`SERVER ERROR: ${e.message}`);
    console.error('SERVER ERROR:', e);
});

try {
    server.listen(PORT, () => {
        const msg = `
        🏛️  공명 도서관 서버가 시작되었습니다! (D: Drive)
        🌐  http://localhost:${PORT}
        `;
        console.log(msg);
        log(msg);
        setInterval(() => {}, 1000); // Keep alive
    });
} catch (e) {
    log(`LISTEN THREW: ${e.message}`);
}
