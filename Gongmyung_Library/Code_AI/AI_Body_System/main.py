import time
import json
import os
import sys
import psutil

# 모듈 경로 추가 (현재 디렉토리)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# pylint: disable=wrong-import-position
from hippocampus import Hippocampus
from cerebrum import Cerebrum
from thalamus import Thalamus


def check_single_instance():
    """Ensure only one instance of main.py is running."""
    current_pid = os.getpid()
    count = 0
    found_procs = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and 'main.py' in ' '.join(proc.info['cmdline']):
                count += 1
                found_procs.append(f"{proc.info['pid']}: {proc.info['cmdline']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if count > 1:
        print(f"[System] Another instance is already running. Exiting PID {current_pid}.")
        print(f"[Debug] Found processes: {found_procs}")
        sys.exit(0)


def load_config():
    config_path = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)),
        "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    check_single_instance()
    print(">>> Gongmyung AI Body System Initializing... <<<")

    try:
        config = load_config()
    except Exception as e:
        print(f"Error loading config: {e}")
        return

    thalamus = Thalamus(config)
    cerebrum = Cerebrum(config)
    hippocampus = Hippocampus(config)

    print(f"System: {config['system_name']} v{config['version']}")
    print(f"Storage: {config['storage_path']}")
    print(">>> System Active. Press Ctrl+C to hibernate. <<<")

    try:
        while True:
            # 1. 감각 (시상 - Thalamus): 시스템의 물리적 상태(CPU, RAM, 화면)를 감지
            metrics = thalamus.sense()
            signal_data = thalamus.translate_signal(metrics)

            # 2. 사고 (대뇌 - Cerebrum): 감지된 신호를 해석하고 판단
            thought_process = cerebrum.process(signal_data, metrics)

            # 2.5 인지 및 학습 (해마 - Hippocampus): 패턴을 인식하고 경험을 축적
            current_hex = signal_data["hex_code"]
            memory_status = hippocampus.recognize_pattern(current_hex)
            # Auto-accumulate experience with metrics for meaning
            hippocampus.learn_pattern(current_hex, metrics)

            # 3. 기억 (해마 - Hippocampus): 처리된 경험을 장기 기억(로그)으로 저장
            hippocampus.remember(metrics, signal_data, thought_process)

            # 3.5 전파 (대시보드 송출): 실시간 상태를 외부 관찰자(Dashboard)에게 전송
            live_status = {
                "timestamp": metrics["timestamp"],
                "gongmyung": signal_data["sentence"],
                "hex_code": signal_data["hex_code"],
                "memory": memory_status,  # Added Memory Status
                "thalamus": {  # Added thalamus key for Dashboard compatibility
                    "cpu_percent": metrics["cpu"],
                    "memory_percent": metrics["ram"],
                    "vision_grid": metrics.get("vision_grid", [])
                },
                "metrics": {
                    "cpu": metrics["cpu"],
                    "ram": metrics["ram"],
                    "delta": metrics["delta"],
                    "resonance": metrics["resonance"],
                    "flow": metrics["flow"]
                },
                "cerebrum": {
                    "state": thought_process["state"],
                    "analysis": thought_process["analysis"],
                    "recommendation": thought_process["recommendation"],
                    "soul_concept": thought_process.get("soul_concept", "None"),
                    "active_process": thought_process.get("active_process", {}),
                    # Ensure survival instinct is passed
                    "survival_instinct": thought_process.get("survival_instinct", {})
                }
            }

            # Write to JSON file (Atomic write simulation)
            status_path = os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)),
                "live_status.json")
            temp_path = status_path + ".tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(live_status, f, ensure_ascii=False, indent=2)
            os.replace(temp_path, status_path)

            # 4. 출력 (콘솔 시각화): 터미널에 현재 상태 요약 표시
            # os.system('cls' if os.name == 'nt' else 'clear')  # 화면 갱신 (CMD 팝업 방지 위해 주석 처리)
            # print(f"=== {config['system_name']} Monitor ===")
            print(f"Time: {time.strftime('%H:%M:%S')}")
            print("-" * 40)
            print(f"[Gongmyung] {signal_data['sentence']}")
            print(f"[Code     ] {signal_data['hex_code']}")
            print(f"[State    ] {thought_process['state']}")
            print(
                f"[Focus    ] {thought_process.get('active_process', {}).get('name', 'Unknown')}")
            print(f"[Analysis ] {thought_process['analysis']}")
            print(f"[Action   ] {thought_process['recommendation']}")
            print(f"[Soul     ] {thought_process.get('soul_concept', 'None')}")
            print("-" * 40)
            print(
                f"Metrics: Δ:{metrics['delta']:.2f} | 𝓡:{metrics['resonance']:.2f} | F:{metrics['flow']:.2f}")

            time.sleep(config["monitor_interval"])

    except KeyboardInterrupt:
        print("\n>>> System Hibernating... <<<")
        print("Memory saved.")
        sys.exit(0)


if __name__ == "__main__":
    main()
