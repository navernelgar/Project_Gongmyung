// 중력 가속도 공식
const G = 9.8; // m/s^2

function calculateFallSpeed(time) {
    // v = g * t
    return G * time;
}

// @flow:start [물리 엔진] 중력 계산 시작
// @flow:process [가속] 시간(t)에 따른 속도 증가
// @flow:end [결과] 현재 낙하 속도 반환
