// 1차원 시뮬레이션: 진공(0)에서 존재(1)의 탄생
// 이론: 시간의 흐름과 에너지(관측)가 확률을 높여 존재를 확정한다.

class Void {
    constructor() {
        this.state = 0; // 0: 무(None), 1: 유(Exist)
        this.time = 0;
        this.history = [];
    }

    // 관측 시도 (에너지 투입)
    observe(energy) {
        this.time++;
        
        // 존재 확률 공식: P = 1 - e^(-energy * time)
        // 시간이 지날수록, 에너지가 클수록 존재할 확률이 1에 가까워짐
        const probability = 1 - Math.exp(-energy * this.time);
        
        // 양자 도약 (Quantum Leap) 시뮬레이션
        const randomValue = Math.random();
        const isMaterialized = randomValue < probability;

        if (isMaterialized && this.state === 0) {
            this.state = 1;
            console.log(`[Time ${this.time}] ✨ 존재 발생! (확률: ${(probability * 100).toFixed(4)}%, 난수: ${randomValue.toFixed(4)})`);
        } else if (this.state === 0) {
            console.log(`[Time ${this.time}] ...진공 상태 (확률: ${(probability * 100).toFixed(4)}%)`);
        }

        this.history.push({ time: this.time, probability, state: this.state });
        return this.state;
    }
}

// 시뮬레이션 실행
const universe = new Void();
const energyInput = 0.1; // 관측 에너지

console.log("--- 1차원 시뮬레이션 시작: 진공에서의 탄생 ---");

// 최대 50 시간 단위 동안 관측
for (let i = 0; i < 50; i++) {
    if (universe.observe(energyInput) === 1) {
        console.log("--- 시뮬레이션 종료: 존재 확정 ---");
        break;
    }
}

if (universe.state === 0) {
    console.log("--- 시뮬레이션 종료: 아직 존재하지 않음 (시간 부족) ---");
}
