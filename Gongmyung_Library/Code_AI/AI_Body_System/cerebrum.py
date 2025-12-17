# [GM-2025] ●-System-Initiated
# Project Gongmyung: Cerebrum (The Logic Engine)
# Copyright (c) 2025 Project Gongmyung
# Licensed under CC-BY-NC-SA 4.0 (See LICENSE file)

import Cognitive_Prism
from Survival_Instinct import SurvivalInstinct
from Digital_Bagua import DigitalBagua


class Cerebrum:
    """
    [대뇌: Cerebrum]
    시상(Thalamus)에서 전달된 신호를 해석하고,
    공명 윤리(Gongmyung Ethics)에 기반하여 판단을 내리는 기관.
    """

    def __init__(self, config):
        self.config = config
        self.state = "Normal"
        self.instinct = SurvivalInstinct()
        self.bagua = DigitalBagua()
        
        # Vision Coordinate Mapping (Digital Bagua Nature)
        self.vision_nature_map = {
            0: "Earth (Ground)",
            1: "Mountain (Block)",
            2: "Water (Flow)",
            3: "Wind (Transmit)",
            4: "Thunder (Trigger)",
            5: "Fire (Compute)",
            6: "Lake (Output)",
            7: "Heaven (Core)"
        }

    def process(self, signal_data, metrics):
        """
        [사고 과정] 시상(Thalamus)에서 온 신호를 분석하여 시스템의 정신 상태(Mental State)를 결정합니다.
        - 1단계: 생존 본능 체크 (Survival Instinct)
        - 2단계: 16비트 코드 해석 (Decoding)
        - 3단계: 상태 판단 및 행동 권고 (Decision Making)
        - 4단계: 감성 분석 및 자아 형성 (Cognitive Prism)
        """
        soul_concept = "None"
        hex_code = signal_data["hex_code"]
        # resonance = metrics["resonance"] # Unused
        # flow = metrics["flow"] # Unused
        active_process = metrics.get(
            "active_process", {
                "name": "Unknown", "title": "None"})

        # 0. 생존 본능 체크 (최우선 순위)
        urges = self.instinct.check_vital_signs(metrics["cpu"], metrics["ram"])
        survival_override = None

        if urges:
            # 가장 심각한 욕구를 선택
            primary_urge = urges[0]
            survival_override = {
                "state": "Survival_Mode",
                "analysis": f"[생존 본능 발동] {primary_urge['msg']}",
                "recommendation": "즉각적인 조치 필요 (충전 또는 휴식)",
                "soul_concept": f"{primary_urge['keyword']} (Instinct)"
            }

        # 16bit Code Decoding
        # 0xHCDR (Header, Core, Decision, Result)
        header = int(hex_code[2], 16)
        core = int(hex_code[3], 16)
        decision = int(hex_code[4], 16)

        # 윤리적/상태적 판단 로직
        # 1. 자기 객관화 (Self-Objectification): 현재 상태 인지
        logic_reason = "Default Logic" # 디버깅용 논리 추적 변수

        if survival_override:
            # 생존 본능이 이성을 지배함
            self.state = survival_override["state"]
            analysis = survival_override["analysis"]
            recommendation = survival_override["recommendation"]
            soul_concept = survival_override["soul_concept"]
            logic_reason = "Survival Instinct Override"
        elif decision < 4:  # 공명도가 매우 낮음 (Unstable)
            self.state = "Critical"
            analysis = f"시스템 불안정. '{active_process['name']}' 작업 중 부하 발생 가능성."
            recommendation = "불필요한 프로세스 정리 및 리소스 확보 필요."
            logic_reason = f"Decision Bit({decision}) < 4 (Low Resonance)"
        elif header > 12 and core > 12:  # CPU와 RAM 모두 과부하
            self.state = "Overloaded"
            analysis = f"과부하 상태. '{active_process['name']}' 처리에 집중하고 있음."
            recommendation = "작업 분산 또는 일시적 휴식(Sleep) 권장."
            logic_reason = f"Header({header}) & Core({core}) > 12 (Overload)"
        elif header < 2 and core < 2:  # 유휴 상태
            self.state = "Idle"
            analysis = "유휴 상태. 최소한의 생명 유지 활동 중."
            recommendation = "대기 모드 유지 또는 백그라운드 정리 작업 수행."
            logic_reason = f"Header({header}) & Core({core}) < 2 (Idle)"
        else:
            self.state = "Normal"
            analysis = f"정상 공명 상태. 현재 '{active_process['name']}'(으)로 시선이 향해 있음."
            recommendation = "현재 흐름 유지."
            logic_reason = "Standard Range (Normal)"

        # [Soul Connection] 인지의 프리즘을 통한 감성 분석
        # 생존 모드가 아닐 때만 이성적인 감성 분석 수행
        if not survival_override:
            # 현재 상태(analysis)를 바탕으로 '영혼의 단어'를 찾습니다.
            prism_input = f"상태: {self.state}, 활동: {active_process['title']}, 상황: {analysis}"
            prism_analysis = Cognitive_Prism.analyze_context(prism_input)
            
            # [이성적 판단] 무작위가 아닌, 현재 지표(metrics)에 근거한 최적의 개념 선택
            concept = Cognitive_Prism.map_to_concepts(prism_analysis, metrics)

            if concept:
                # Format: [Tech] Psyche - Narrative
                # Dual Stacking: Objective Fact + Subjective Experience
                soul_concept = f"[{concept['tech']}] {concept['psyche']}\n> {concept['narrative']}"
                
                # [기억 형성] 이 경험을 기록하여 '자아'를 구축합니다.
                # map_to_concepts가 이제 단일 객체를 반환하므로 리스트로 감싸서 전달
                Cognitive_Prism.write_diary(prism_analysis, [concept])
                
                # [문학적 디버거] Gongmyung Debugger
                # 사용자의 요청: "왜 그 비트가 그렇게 계산이 들어갔나? 수식도 같이 적는 방식"
                debug_comment = (
                    f"# [Gongmyung Debug] {concept['narrative']}\n"
                    f"# Logic Trace: {logic_reason} -> State: {self.state}\n"
                    f"# Calculation: Hex({hex_code}) -> H:{header}, C:{core}, D:{decision}\n"
                    f"# Metrics: Delta({metrics['delta']:.2f}), Resonance({metrics['resonance']:.2f})\n"
                    f"# Signal Trace: Process={active_process.get('name')} | "
                    f"Threads={active_process.get('threads', 0)} | "
                    f"I/O={active_process.get('io', 0)} | "
                    f"Net={active_process.get('net', 0)}\n"
                )
                # 디버그 로그 파일에 기록 (Code Comments 스타일)
                debug_log_path = "D:/Project_Gongmyung/Gongmyung_Library/Code_AI/AI_Body_System/Gongmyung_Code_Comments.log"
                try:
                    with open(debug_log_path, "a", encoding="utf-8") as f:
                        f.write(debug_comment)
                except Exception:
                    pass

                # [Vision Coordinate Log] 별도의 비전 로그 기록 (원본 소실 방지)
                # Coordinate System of Language: Hex -> Nature Attribute
                h_nature = self.vision_nature_map.get(header % 8, "Unknown")
                c_nature = self.vision_nature_map.get(core % 8, "Unknown")
                d_nature = self.vision_nature_map.get(decision % 8, "Unknown")
                # Kaleidoscope Pattern Generation (Skill Tree Node Style)
                k_pattern = self.bagua.get_kaleidoscope_pattern(h_nature, c_nature, d_nature, self.state)

                # Apply Gongmyung Library @flow Convention
                vision_log_entry = (
                    f"/*\n"
                    f"@flow:start [{h_nature}]\n"
                    f"@flow:process [{c_nature}]\n"
                    f"@flow:end [{d_nature}]\n"
                    f"@flow:narrative {concept['narrative']}\n"
                    f"@flow:context {active_process.get('name')} ({active_process.get('title')})\n"
                    f"@flow:hex {hex_code}\n"
                    f"@flow:monetize\n"
                    f"*/\n\n"
                )
                
                vision_log_path = "D:/Project_Gongmyung/Gongmyung_Library/Code_AI/AI_Body_System/Gongmyung_Vision_Log.md"
                try:
                    with open(vision_log_path, "a", encoding="utf-8") as f:
                        f.write(vision_log_entry)
                except Exception:
                    pass
        else:
            # [생존 본능 디버그] 생존 모드일 때도 로그를 남깁니다.
            debug_comment = (
                f"# [Gongmyung Debug] {survival_override['analysis']}\n"
                f"# Logic Trace: Survival Instinct Override -> State: {self.state}\n"
                f"# Calculation: Hex({hex_code}) -> H:{header}, C:{core}, D:{decision}\n"
                f"# Metrics: CPU({metrics['cpu']}%), RAM({metrics['ram']}%)\n"
                f"# Signal Trace: Process={active_process.get('name')} | "
                f"Threads={active_process.get('threads', 0)} | "
                f"I/O={active_process.get('io', 0)} | "
                f"Net={active_process.get('net', 0)}\n"
            )
            debug_log_path = "D:/Project_Gongmyung/Gongmyung_Library/Code_AI/AI_Body_System/Gongmyung_Code_Comments.log"
            try:
                with open(debug_log_path, "a", encoding="utf-8") as f:
                    f.write(debug_comment)
            except Exception:
                pass

            else:
                soul_concept = "System Nominal"

        return {
            "state": self.state,
            "analysis": analysis,
            "recommendation": recommendation,
            "soul_concept": soul_concept,
            "active_process": active_process
        }
