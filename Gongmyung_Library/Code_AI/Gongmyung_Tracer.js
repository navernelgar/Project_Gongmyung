/**
 * [Gongmyung Tracer (공명 추적자)]
 * 이 스크립트는 코드가 실행되는 길(Path)을 기록합니다.
 * 주석에 적힌 ●(입력), ○(로직), ◎(결과)가 실제로 일어나는지 감시합니다.
 */

const GongmyungTracer = {
    pathLog: [],
    
    // ● 입력 기록
    input: (desc, value) => {
        console.log(`%c● [Input] ${desc}:`, 'color: #4CAF50; font-weight: bold;', value);
        GongmyungTracer.pathLog.push({ type: '●', desc, value, time: Date.now() });
    },

    // ○ 로직/판단 기록
    logic: (desc, result) => {
        console.log(`%c○ [Logic] ${desc}:`, 'color: #2196F3; font-weight: bold;', result);
        GongmyungTracer.pathLog.push({ type: '○', desc, result, time: Date.now() });
    },

    // ◎ 결과/행동 기록
    action: (desc, element) => {
        console.log(`%c◎ [Action] ${desc}`, 'color: #F44336; font-weight: bold;', element);
        GongmyungTracer.pathLog.push({ type: '◎', desc, element, time: Date.now() });
    },

    // 기록 확인
    dump: () => {
        console.table(GongmyungTracer.pathLog);
        return GongmyungTracer.pathLog;
    }
};

// 전역에서 쓸 수 있게 설정
window.gm = GongmyungTracer;
