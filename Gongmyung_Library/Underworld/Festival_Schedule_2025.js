@flow:start [축제 시작] 언더월드 개장 축제 기획안
@flow:tag [Event]
@flow:monetize

// 1. 오프닝 행사
@flow:process [입장] 모든 참가자는 가면을 쓰고 입장한다 (익명성 보장)
function enterUnderworld(user) {
    user.mask = true;
    user.role = 'player';
    return user;
}

// 2. 메인 이벤트: 코드 백일장
@flow:branch [선택] 참가 분야를 선택하세요 (문학/코딩/물리)
if (choice == 'coding') {
    startHackathon();
} else if (choice == 'literature') {
    startPoetryBattle();
}

// 3. 보상 지급
@flow:process [정산] 축제 수익금의 60%는 다음 축제 예산으로 적립
@flow:process [배당] 참가자들에게 '공명 토큰' 지급

@flow:end [폐막] 가면을 벗고 현실로 복귀
