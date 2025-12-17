import * as vscode from 'vscode';

// 공명 데이터베이스 (프로토타입용 하드코딩 데이터)
const GONGMYUNG_DB: { [key: string]: { [level: string]: string } } = {
    "toggleLayer": {
        "seed": "📦 **[상자 열기/닫기]**\n\n이 기능은 사용자가 클릭한 상자만 열고, 나머지는 닫아주는 역할을 합니다.\n\n● **입력**: 클릭한 상자 번호\n◎ **결과**: 상자가 열리거나 닫힘",
        "stem": "⚙️ **[Function: toggleLayer]**\n\nID를 매개변수로 받아 DOM 요소를 순회하며 클래스를 토글합니다.\n\n○ **Logic**: `forEach` 루프를 돌며 ID 일치 여부 확인",
        "flower": "🌸 **[Optimization Note]**\n\n`querySelectorAll`은 매번 DOM을 탐색하므로, 리스트를 캐싱하면 성능이 향상될 수 있습니다.\n\n◎ **Complexity**: O(n)"
    },
    "querySelectorAll": {
        "seed": "🔍 **[모두 찾기]**\n\n문서 안에 있는 모든 상자(.layer)를 샅샅이 뒤져서 찾아냅니다.",
        "stem": "📡 **[DOM Query]**\n\nCSS 선택자와 일치하는 모든 요소를 NodeList로 반환합니다.",
        "flower": "⚡ **[Performance]**\n\nLive NodeList가 아닌 Static NodeList를 반환합니다."
    }
};

export function activate(context: vscode.ExtensionContext) {
    console.log('Gongmyung Lens is now active!');

    // 1. 호버 프로바이더 (마우스 올렸을 때 설명 표시)
    const hoverProvider = vscode.languages.registerHoverProvider(
        ['javascript', 'html'],
        {
            provideHover(document, position, token) {
                const range = document.getWordRangeAtPosition(position);
                if (!range) {
                    return;
                }
                const word = document.getText(range);
                
                // 설정된 난이도 가져오기
                const config = vscode.workspace.getConfiguration('gongmyung');
                const difficulty = config.get<string>('difficulty') || 'seed';

                if (GONGMYUNG_DB[word]) {
                    const explanation = GONGMYUNG_DB[word][difficulty];
                    return new vscode.Hover(explanation);
                }
            }
        }
    );

    // 2. 명령어: 난이도 변경
    const difficultyCommand = vscode.commands.registerCommand('gongmyung.setDifficulty', async () => {
        const result = await vscode.window.showQuickPick(['seed', 'stem', 'flower'], {
            placeHolder: 'Select Difficulty Level (씨앗/줄기/꽃)'
        });
        
        if (result) {
            await vscode.workspace.getConfiguration('gongmyung').update('difficulty', result, true);
            vscode.window.showInformationMessage(`Gongmyung Level set to: ${result}`);
        }
    });

    context.subscriptions.push(hoverProvider);
    context.subscriptions.push(difficultyCommand);
}

export function deactivate() {}