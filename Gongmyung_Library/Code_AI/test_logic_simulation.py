import time

class GongmyungTracer:
    def input(self, desc, value):
        print(f"● [Input] {desc}: {value}")
    
    def logic(self, desc, result):
        print(f"○ [Logic] {desc}: {result}")
        
    def action(self, desc, element):
        print(f"◎ [Action] {desc}: {element}")

# 가상의 HTML 요소 (데이터가 없어도 돌아가는지 확인용)
class MockElement:
    def __init__(self, id):
        self.id = id
        self.classList = set()
    
    def toggle(self, className):
        if className in self.classList:
            self.classList.remove(className)
            return "Removed"
        else:
            self.classList.add(className)
            return "Added"
            
    def remove(self, className):
        if className in self.classList:
            self.classList.remove(className)

# 테스트할 데이터 (실제 DB가 없어도 이 리스트만 있으면 됨)
mock_layers = [MockElement("l1"), MockElement("l2"), MockElement("l3")]
gm = GongmyungTracer()

def toggleLayer(target_id):
    print(f"\n--- Testing toggleLayer('{target_id}') ---")
    
    # [Debug] 추적 시작
    gm.input("Layer ID 수신", target_id)

    # 실제 로직 시뮬레이션
    found = False
    for l in mock_layers:
        # ○ [판단]
        is_match = (l.id == target_id)
        gm.logic(f"ID 비교 ({l.id} == {target_id})", is_match)
        
        if is_match:
            # ◎ [행동]
            result = l.toggle('active')
            gm.action(f"상자 상태 변경 ({result})", l.id)
            found = True
        else:
            # ◎ [행동]
            l.remove('active')
    
    if not found:
        print("⚠️ [Warning] 해당 ID를 가진 상자가 없습니다. (하지만 에러는 안 남)")

# 실행 테스트
if __name__ == "__main__":
    print("시스템 가동: 데이터 연결 없이 로직 검증 시작...")
    toggleLayer("l1") # 정상 케이스
    toggleLayer("l99") # 없는 데이터 케이스 (오류 체크)
    print("\n검증 완료: 데이터가 없어도 멈추지 않습니다.")
