// 퀘스트 시스템 로직

function acceptQuest(questId) {
    console.log(`Quest ${questId} accepted.`);
}

// @flow:start [퀘스트] 수락 프로세스
// @flow:branch [조건] 레벨 10 이상인가?
// @flow:process [수락] 퀘스트 목록에 추가
// @flow:end [완료] UI 업데이트
