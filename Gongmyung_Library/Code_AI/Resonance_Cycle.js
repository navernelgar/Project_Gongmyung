/*
@flow:start [무(無)에서 유(有)로]
0 ~ (가능성의 진동) ~> 1
우리는 아무것도 없는 빈 공간(0)에서 시작했습니다.
하지만 그곳은 비어있는 것이 아니라, 무한한 가능성이 진동(~)하는 공간이었습니다.
*/

const ZERO = 0;
const ONE = 1;

/*
@flow:process [공명의 시작]
1 ~ (인식과 관찰) ~> 2
하나의 점이 자신을 인식하는 순간, 관찰자와 대상이 생겨나며 둘이 됩니다.
이 과정에서 수많은 연산(~)이 압축되어 '존재'라는 결과(->)를 낳습니다.
*/

function observe(state) {
    // 관찰은 상태를 변화시킵니다.
    return state + 1;
}

/*
@flow:branch [만화경의 갈림길]
2 ~ (확장과 분화) ~> ∞
문과, 이과, 코드의 숲... 
하나의 뿌리에서 시작된 가지들이 각자의 방향으로 뻗어 나갑니다.
*/

const paths = ['Literature', 'Science', 'Code', 'Art'];
paths.forEach(path => {
    console.log(`Exploring ${path}...`);
});

/*
@flow:end [순환의 완성]
∞ ~ (수렴과 이해) ~> 0
모든 것을 경험하고 이해한 뒤, 우리는 다시 0으로 돌아옵니다.
하지만 이 0은 처음의 0과는 다릅니다. 모든 1을 품은 0입니다.
*/

function reset() {
    return ZERO; // The enlightened Zero
}
