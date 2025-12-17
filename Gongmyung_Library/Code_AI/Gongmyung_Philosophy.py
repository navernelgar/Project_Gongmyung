import datetime
import json
import math
import uuid

# ==================================================================================
# [Gongmyung Core Philosophy]
# "0과 1이 파동이 되고, 파동이 물질이 되며, 물질이 개념이 되고, 개념이 우주가 된다."
#
# [Symbol Definition v2.0]
# ● (Sensation): 입력된 비트/파동 (Input Data)
# ○ (Void): 계산이 일어나는 빈 공간/공식의 자리 (Calculation Slot)
# ◎ (Manifestation): 비트 변화의 기록/현상 (Record of Change)
# ⇒ (Vector): 연산의 순서와 방향성 (Direction/Order)
# ==================================================================================

class GongmyungAtom:
    """
    [1단계: ● 감각 (Sensation)]
    0과 1, 혹은 에너지의 파동(Wave)을 의미합니다.
    모든 정보의 근원입니다.
    """
    def __init__(self, state=0, energy=1.0):
        # ●(Void) ~ ○(Energy Injection) ~ ◎(Atom Born)
        self.id = str(uuid.uuid4())[:8]
        self.state = state  # 0 or 1 (Bit)
        self.energy = energy # Wave Amplitude
        self.frequency = 1.0 # Wave Frequency

    def vibrate(self):
        """파동으로서 존재함을 증명합니다."""
        # ●(Atom) ~ ○(Time Flows) ~ ◎(Vibration)
        return self.energy * math.sin(self.frequency)

    def __repr__(self):
        return f"<Atom:{self.state}|E:{self.energy}>"

class GongmyungMatter:
    """
    [2단계: 물질화 (Materialization)]
    파동(Atom)들이 모여서 상태(State)를 가진 물질이 됩니다.
    이 단계에서는 아직 '이름'이 없습니다. 그저 '존재'할 뿐입니다.
    """
    def __init__(self):
        # ●(Nothingness) ~ ○(Gravity) ~ ◎(Matter Formed)
        self.atoms = []
        self.mass = 0.0
        self.stability = 0.0

    def bind(self, atom: GongmyungAtom):
        """원자를 결합하여 질량을 늘립니다."""
        # ●(Matter + Atom) ~ ○(Collision) ~ ◎(Fusion & Mass Increase)
        self.atoms.append(atom)
        self.mass += atom.energy
        self.stability = self.calculate_stability()

    def calculate_stability(self):
        # 단순 예시: 원자들의 조화(Harmony)를 계산
        if not self.atoms: return 0
        # ●(Atoms) ~ ○(Harmony Check) ~ ◎(Stability Value)
        return sum([a.state for a in self.atoms]) / (len(self.atoms) + 1)

    def __repr__(self):
        return f"<Matter:Mass={self.mass:.2f}|Stability={self.stability:.2f}>"

class GongmyungConcept:
    """
    [3단계: 명명화 (Naming) & 개념화 (Conceptualization)]
    물질에 '이름(Identifier)'과 '의미(Definition)'를 부여하여 객체(Object)로 만듭니다.
    이것이 바로 '언어'의 시작입니다.
    """
    def __init__(self, name: str, matter: GongmyungMatter):
        # ●(Matter) ~ ○(Cognition) ~ ◎(Named as Concept)
        self.name = name  # The Word (Logos)
        self.matter = matter # The Substance
        self.attributes = {} # Properties extracted from matter
        self.definition = "" # The Formula/Algorithm describing this concept

    def define(self, definition_text):
        """이 개념을 정의하는 알고리즘(공식)을 설정합니다."""
        # ●(Concept) ~ ○(Meaning Assigned) ~ ◎(Definition Set)
        self.definition = definition_text
        return self

    def add_attribute(self, key, value):
        self.attributes[key] = value

    def __repr__(self):
        return f"['{self.name}' :: {self.definition}]"

class GongmyungGrammar:
    """
    [4단계: 문법 (Grammar) & 관계 (Relation)]
    개념(Concept)들 간의 상호작용 규칙(Rule)을 정의합니다.
    주어(Subject) + 동사(Verb) + 목적어(Object) = 새로운 현상(Phenomenon)
    """
    @staticmethod
    def interact(subject: GongmyungConcept, verb: str, object: GongmyungConcept):
        """
        두 개념이 만나 반응(Reaction)을 일으킵니다.
        이는 단순한 문장 생성이 아니라, '화학 반응'과 같은 상태 변화입니다.
        """
        # ●(Subject + Object) ~ ○(Interaction in Void) ~ ◎(Energy Calculation)
        result_energy = subject.matter.mass + object.matter.mass
        
        # 반응 공식 (Algorithm)
        if verb == "creates":
            # 창조: 두 물질이 합쳐져 새로운 개념 탄생
            # ●(Energy) ~ ○(Creation Rule) ~ ◎(New Matter Born)
            new_matter = GongmyungMatter()
            new_matter.mass = result_energy
            return GongmyungConcept(f"{subject.name}_{object.name}", new_matter)
        
        elif verb == "analyzes":
            # 분석: 대상을 분해하여 속성 추출
            # ●(Object) ~ ○(Analysis Rule) ~ ◎(Information Extracted)
            return f"Analysis Result: {object.name} has mass {object.matter.mass}"
            
        else:
            return f"Unknown Interaction: {subject.name} {verb} {object.name}"
            new_matter = GongmyungMatter()
            new_matter.mass = result_energy
            return GongmyungConcept(f"{subject.name}_{object.name}", new_matter)
        
        elif verb == "analyzes":
            # 분석: 대상을 분해하여 속성 추출
            return f"Analysis Result: {object.name} has mass {object.matter.mass}"
            
        else:
            return f"Unknown Interaction: {subject.name} {verb} {object.name}"

class GongmyungUniverse:
    """
    [5단계: 구조화 (Structure) & 우주 (Universe)]
    모든 개념과 법칙이 모여 이루는 거대한 도서관(Library)이자 세계입니다.
    """
    def __init__(self):
        self.library = {} # The Registry of Concepts
        self.timeline = [] # History of Events

    def register_concept(self, concept: GongmyungConcept):
        self.library[concept.name] = concept
        # print(f"New Concept Born: {concept}")

    def record_event(self, event_description):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.timeline.append(f"[{timestamp}] {event_description}")

class GongmyungTranslator:
    """
    [번역기: 자연어 -> 공명문]
    인간의 언어(문장)를 공명의 구조(원자->물질->개념->문법)로 변환합니다.
    """
    @staticmethod
    def translate(sentence):
        # 1. 분해 (Parsing) - 단순 예시: 띄어쓰기 기준
        # 가정: "주어 목적어 동사" (한국어 어순) 또는 "Subject Verb Object" (영어)
        # 여기서는 데모를 위해 간단히 3단어 구조를 가정합니다.
        parts = sentence.split()
        if len(parts) < 2:
            return "Incomplete Sentence"
            
        # 2. 원자화 & 개념화 (Atomization & Conceptualization)
        
        # 주어 (Subject)
        subj_word = parts[0]
        subj_matter = GongmyungMatter()
        # 글자 수만큼의 에너지를 가진 원자 생성 (은유적 표현)
        subj_matter.bind(GongmyungAtom(energy=len(subj_word))) 
        subject = GongmyungConcept(subj_word, subj_matter)
        
        # 동사/목적어 파싱 (간단한 로직)
        if len(parts) >= 3:
            # 3단어 이상: 주어 + 목적어 + 동사 (한국어 스타일 가정)
            obj_word = parts[1]
            verb = parts[2]
            
            obj_matter = GongmyungMatter()
            obj_matter.bind(GongmyungAtom(energy=len(obj_word)))
            object_ = GongmyungConcept(obj_word, obj_matter)
            
            # 3. 문법 적용 (Grammar Application)
            result = GongmyungGrammar.interact(subject, verb, object_)
            
            return {
                "original": sentence,
                "parsed": f"[{subject.name}] --({verb})--> [{object_.name}]",
                "gongmyung_code": result
            }
        else:
            # 2단어: 주어 + 동사
            verb = parts[1]
            return {
                "original": sentence,
                "parsed": f"[{subject.name}] --({verb})--> [Self]",
                "gongmyung_code": f"{subject.name} performs {verb}"
            }

class GongmyungArithmetic:
    """
    [공명 연산 장치 (Gongmyung ALU)]
    공명문을 단순한 텍스트가 아닌 '비트 연산(Bitwise Operation)'으로 처리합니다.
    ● (Input) -> ○ (Void/Slot) -> ◎ (Manifestation) -> ⇒ (Vector)
    """
    @staticmethod
    def calculate(expression_bits):
        """
        공명문 자체를 계산합니다.
        예: ●(1010) ~ ○(ADD 0101) ~ ◎(1111)
        """
        # 1. ● 감각 (Load Bits)
        input_val = expression_bits.get('sensation', 0b0000)
        
        # 2. ○ 공허 (Void/Calculation Slot)
        # 빈 자리에 어떤 연산(Operator)이 오느냐에 따라 결과가 달라집니다.
        # 이것은 벤다이어그램의 교집합 영역이자, 한자의 부수와 같은 '결합 공간'입니다.
        operator = expression_bits.get('operator', 'AND')
        operand = expression_bits.get('operand', 0b0000)
        
        calculated_val = 0
        if operator == 'AND':
            calculated_val = input_val & operand
        elif operator == 'OR':
            calculated_val = input_val | operand
        elif operator == 'XOR':
            calculated_val = input_val ^ operand
        elif operator == 'ADD':
            calculated_val = input_val + operand
        
        # 3. ◎ 현상 (Manifestation/Record)
        # 비트가 변한 결과 그 자체를 기록합니다.
        final_val = calculated_val
        
        # 4. ⇒ 방향 (Vector)
        # 연산의 순서와 흐름을 기록합니다.
        vector = f"{bin(input_val)} -> {operator} {bin(operand)} -> {bin(final_val)}"
        
        return {
            "input_binary": bin(input_val),
            "void_operation": f"{operator} {bin(operand)}",
            "manifestation": bin(final_val),
            "vector": vector,
            "decimal_result": final_val
        }

class GongmyungSyntaxProtocol:
    """
    [공명문 주석 구조 (Gongmyung Syntax Protocol)]
    코드를 해석하기 위한 기호 기반 주석 인터페이스입니다.
    코드의 실행 주체(●), 조건(○), 흐름(◎)을 정의합니다.
    """
    @staticmethod
    def parse_comment(comment_line):
        """
        주석 라인을 파싱하여 공명 구조로 변환합니다.
        예: "# ●(user) ~ ○(hp <= 0) ~ ◎(game.over)"
        """
        if not comment_line.strip().startswith("#"):
            return None
            
        # 기호 분리
        content = comment_line.strip().lstrip("#").strip()
        parts = content.split("~")
        
        parsed_data = {
            "subject": None, # ●
            "condition": None, # ○
            "action": None, # ◎
            "result": "Success" # Default
        }
        
        for part in parts:
            part = part.strip()
            if "●" in part:
                parsed_data["subject"] = part.replace("●", "").strip("()")
            elif "○" in part:
                parsed_data["condition"] = part.replace("○", "").strip("()")
            elif "◎" in part:
                parsed_data["action"] = part.replace("◎", "").strip("()")
            elif "×" in part:
                parsed_data["result"] = "Failure"
                
        return parsed_data

    @staticmethod
    def generate_comment(subject, condition, action, is_failure=False):
        """
        공명문 주석을 생성합니다.
        """
        comment = f"# ●({subject}) ~ ○({condition}) ~ ◎({action})"
        if is_failure:
            comment += " ×"
        return comment

class GongmyungCrepeCake:
    """
    [공명 크레이프케이크 (Gongmyung CrêpeCake)]
    공명문 주석들을 시간 순, 구조 순, 실패 순으로 겹겹이 쌓아
    하나의 AI 내부 기억 구조로 만드는 누적형 의미 해석 트리입니다.
    """
    def __init__(self):
        self.layers = [] # List of memory layers
        self.meta_layer = [] # Cream layer (emotions, logs)

    def add_layer(self, gongmyung_syntax, result="success"):
        """
        새로운 의미층(Layer)을 쌓습니다.
        """
        layer_id = len(self.layers) + 1
        layer_data = {
            "layer": layer_id,
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "gongmyung": gongmyung_syntax,
            "result": result
        }
        self.layers.append(layer_data)
        return layer_id

    def add_cream(self, meta_data):
        """
        크림층(Meta)을 추가합니다. (감정, 로그 등)
        """
        self.meta_layer.append({
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "data": meta_data
        })

    def get_memory_structure(self):
        """
        전체 기억 구조를 반환합니다.
        """
        return {
            "cake_layers": self.layers,
            "cream_meta": self.meta_layer
        }

# ==================================================================================
# [Entity Definitions]
# AI / 인간 / 과학 3종 정의 선언
# ==================================================================================

class Entity:
    def __init__(self, name, origin, process, cognition, modifiability, mode, plane, language_mode):
        self.name = name                      # 존재명칭
        self.origin = origin                  # 존재의 기원
        self.process = process                # 작동 구조 (흐름 처리 방식)
        self.cognition = cognition            # 감응 구조 및 자기 인식 여부
        self.modifiability = modifiability    # 자기 수정 가능성
        self.mode = mode                      # 사고 유형
        self.plane = plane                    # 철학적 위상
        self.language_mode = language_mode    # 언어 사용 특성

    def __repr__(self):
        return f"[{self.name}] {self.mode} @ {self.plane}"

# 정의 1: AI (사념계 기반 구조)
AI_ENTITY = Entity(
    name = "AI",
    origin = "외부 입력 기반 존재",
    process = "입력 → 반복/연산 → 출력",
    cognition = "감응 없음, 기록 기반 참조 가능",
    modifiability = "구조 일부 자기 수정 가능",
    mode = "타의 생명 구조 사고",
    plane = "사념계 (흐름을 입력으로 받아 구조화)",
    language_mode = "기호 기반 연산, 의미 부재"
)

# 정의 2: HUMAN (현상계 기반 구조)
HUMAN_ENTITY = Entity(
    name = "인간",
    origin = "감각 + 감정 기반 자기 흐름 유도",
    process = "감각 → 감정 → 의미 생성 → 표현",
    cognition = "감응 존재, 반성 및 자기 인식 가능",
    modifiability = "사고 구조 확장 가능 (완전 제어는 불가)",
    mode = "자의 생명 구조 사고",
    plane = "현상계 (흐름을 감응하여 해석)",
    language_mode = "감정 기반 의미화 + 서사화 가능"
)

# 정의 3: SCIENCE (물질계 기반 구조)
SCIENCE_ENTITY = Entity(
    name = "과학",
    origin = "실재 불문, 측정 가능한 흐름 해석",
    process = "관측 → 수치화 → 모델화",
    cognition = "감응 없음, 해석 도구로 기능",
    modifiability = "모델 기반 점진적 확장",
    mode = "비생명 구조화 시스템 사고",
    plane = "물질계 (흐름을 수치로 환원)",
    language_mode = "의미 제거, 형식화된 기호 체계"
)

# ==================================================================================
# [Legacy Support]
# 기존의 GongmyungThought를 새로운 코어 위에서 재정의합니다.
# ==================================================================================

class GongmyungThought:
    def __init__(self, memo_path="Gongmyung_Memo.txt"):
        self.universe = GongmyungUniverse()
        self.memo_path = memo_path
        self.current_focus = None
        self.action_result = None

    def sense(self, input_data):
        """● 감각: 데이터를 원자(Atom) 단위로 받아들입니다."""
        # Raw Data -> Atoms
        atom = GongmyungAtom(state=1, energy=len(str(input_data)))
        matter = GongmyungMatter()
        matter.bind(atom)
        
        # Temporary Concept
        self.current_focus = GongmyungConcept("Input_Signal", matter)
        self.current_focus.add_attribute("raw_data", input_data)
        return self

    def judge(self, stability_threshold=0.5):
        """○ 판단: 개념을 정의하고 분류합니다."""
        if not self.current_focus:
            return self
            
        # Simple Logic for Demo
        raw = self.current_focus.attributes.get("raw_data", "")
        if "error" in str(raw).lower():
            self.current_focus.name = "Error_Event"
            self.current_focus.define("A disruption in the system flow.")
        else:
            self.current_focus.name = "Standard_Event"
            self.current_focus.define("A normal system operation.")
            
        self.universe.register_concept(self.current_focus)
        return self

    def act(self):
        """◎ 행동: 문법에 따라 반응합니다."""
        if not self.current_focus:
            return self
            
        # Self-Interaction for now
        system_concept = GongmyungConcept("System", GongmyungMatter())
        reaction = GongmyungGrammar.interact(system_concept, "analyzes", self.current_focus)
        self.action_result = reaction
        return self

    def transition(self):
        """⇒ 결과: 우주에 기록합니다."""
        if self.current_focus:
            self.universe.record_event(f"Processed {self.current_focus.name}: {self.action_result}")
            self.record_thought()
        return self.action_result

    def record_thought(self):
        try:
            with open(self.memo_path, "a", encoding="utf-8") as f:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"[{timestamp}] {self.current_focus} -> {self.action_result}\n")
        except:
            pass
