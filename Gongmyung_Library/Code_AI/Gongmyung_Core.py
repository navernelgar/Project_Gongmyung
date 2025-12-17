import time
import subprocess
import os
import sys
import threading
from Gongmyung_Philosophy_v2 import GongmyungThought

class GongmyungCore:
    def __init__(self):
        self.brain = GongmyungThought()
        self.processes = {}
        self.running = True

    def log(self, msg):
        print(f"[Core] {msg}")

    def start_server(self, name, script, port):
        self.log(f"Starting {name} on port {port}...")
        try:
            # Use python executable from current environment
            python_exe = sys.executable
            cmd = [python_exe, script]
            
            # Start process
            proc = subprocess.Popen(
                cmd, 
                cwd=os.path.dirname(os.path.abspath(__file__)),
                creationflags=subprocess.CREATE_NO_WINDOW # Windows specific: Hidden window
            )
            self.processes[name] = proc
            self.log(f"{name} started (PID: {proc.pid})")
        except Exception as e:
            self.log(f"Failed to start {name}: {e}")

    def stop_all(self):
        self.log("Stopping all subsystems...")
        for name, proc in self.processes.items():
            proc.terminate()
            self.log(f"{name} terminated.")
        self.running = False

    def cognitive_loop(self):
        self.log("Cognitive Loop Activated.")
        while self.running:
            try:
                # 1. Sense (Mock Data for now)
                # In reality, this would check system stats, file changes, or user input queues
                input_data = {"type": "system_status", "cpu": 10, "active_servers": len(self.processes)}
                
                # 2. Run Cycle
                thought = self.brain.sense(input_data) \
                    .interpret() \
                    .conceptualize() \
                    .concretize() \
                    .act() \
                    .transition()
                
                # self.log(f"Thought Cycle: {thought['concept']} -> {thought['action']}")
                
                time.sleep(5) # Think every 5 seconds
            except KeyboardInterrupt:
                self.stop_all()
                break
            except Exception as e:
                self.log(f"Cognitive Error: {e}")
                time.sleep(5)

    def run(self):
        # 1. Start Subsystems
        self.start_server("Main Server", "server.py", 3000)
        self.start_server("Game Server", "game_server.py", 3002)
        
        # 2. Start Thinking
        try:
            self.cognitive_loop()
        except KeyboardInterrupt:
            self.stop_all()

if __name__ == "__main__":
    core = GongmyungCore()
    core.run()
