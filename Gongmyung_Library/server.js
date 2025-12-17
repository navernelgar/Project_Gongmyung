const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;
const ROOT_DIR = __dirname;

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

const server = http.createServer((req, res) => {
    // Remove query parameters (VS Code adds them automatically)
    const requestUrl = req.url.split('?')[0];
    console.log(`Request: ${requestUrl} (Original: ${req.url})`);
    
    // Decode URL to handle Korean characters
    let safeUrl = decodeURI(requestUrl);
    
    // Handle Root
    if (safeUrl === '/') {
        safeUrl = '/index.html';
    }

    // Handle Library Listing (Dynamic)
    if (safeUrl.startsWith('/library/')) {
        const libType = safeUrl.split('/')[2];
        const dirPath = path.join(ROOT_DIR, libType);

        if (fs.existsSync(dirPath) && fs.lstatSync(dirPath).isDirectory()) {
            fs.readdir(dirPath, (err, files) => {
                if (err) {
                    res.writeHead(500);
                    res.end("Error reading directory");
                    return;
                }
                
                const html = `
                <!DOCTYPE html>
                <html lang="ko">
                <head>
                    <meta charset="UTF-8">
                    <title>${libType} - 공명 도서관</title>
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
                    <a href="/" class="back-btn">⬅ 로비로 돌아가기</a>
                    <h1>📚 ${libType}</h1>
                    
                    <div id="current-mode-label" onclick="toggleView()">
                        📂 기본 장르 (Categories) <span style="font-size:0.8em; opacity:0.5;">🔄</span>
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
                        <div class="book type-user add-file-btn" data-type="user" onclick="alert('🚧 파일 추가 기능은 공사 중입니다.\\n(토론장에서 의견을 남겨주세요!)')">
                            <div class="icon">➕</div>
                            <div>파일 추가</div>
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
                                label.innerHTML = '📂 기본 장르 (Categories) <span style="font-size:0.8em; opacity:0.5;">🔄</span>';
                                label.style.color = '#007bff';
                            } else {
                                label.innerHTML = '👤 사용자 파일 (User Files) <span style="font-size:0.8em; opacity:0.5;">🔄</span>';
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

    // Serve Static Files
    const filePath = path.join(ROOT_DIR, safeUrl);
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

server.listen(PORT, () => {
    console.log(`
    🏛️  공명 도서관 서버가 시작되었습니다!
    🌐  http://localhost:${PORT}
    `);
});
