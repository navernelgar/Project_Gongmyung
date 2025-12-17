import json
import os


class GongmyungGate:
    def __init__(self, index_path="narrative_index.json"):
        self.index_path = index_path
        self.index = self._load_index()
        self.trigrams = {
            "000": "곤 (Earth) - 받아들임",
            "001": "진 (Thunder) - 움직임",
            "010": "감 (Water) - 깊음/위험",
            "011": "태 (Lake) - 기쁨/소통",
            "100": "간 (Mountain) - 멈춤",
            # Note: Binary mapping might vary, using consistent internal logic
            "101": "손 (Wind) - 들어감",
            "110": "리 (Fire) - 밝음/화면",
            "111": "건 (Heaven) - 시작/근원"
        }
        # Correcting the binary mapping to match Digital_Bagua.py
        self.trigrams_map = {
            0: "000", 1: "001", 2: "010", 3: "011",
            4: "100", 5: "101", 6: "110", 7: "111"
        }

    def _load_index(self):
        if not os.path.exists(self.index_path):
            print("Index not found. Please run Narrative_Indexer.py first.")
            return {}
        with open(self.index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Handle both list (old format) and dict (new format)
            if isinstance(data, list):
                return {item['path']: item for item in data}
            return data

    def to_pix(self, val):
        # Convert integer 0-7 to 3-bit Pix string (■/□)
        binary = format(val, '03b')
        return binary.replace('1', '■').replace('0', '□')

    def open_gate(self, target_pattern_int):
        """
        target_pattern_int: 0~7 integer representing the Trigram.
        Returns files that match this pattern.
        """
        matches = []
        target_pix = self.to_pix(target_pattern_int)

        print(
            f"\n[Gongmyung Gate] Opening for Pattern: {target_pix} ({target_pattern_int})")

        for filepath, data in self.index.items():
            # Narrative Energy is the sum of flow bits.
            # We map this energy to a Trigram (0-7) by taking modulo 8 or masking.
            # Let's use masking & 7 (0b111) to get the "Nature" of the file.
            # Changed from 'narrative_energy' to 'energy' to match Indexer
            # output
            narrative_energy = data.get("energy", 0)
            file_trigram = narrative_energy & 7

            if file_trigram == target_pattern_int:
                matches.append(filepath)

        return matches

    def calculate_resonance(self, query_type):
        """
        Interprets a high-level query into a Bit Pattern and searches.
        """
        query_map = {
            "UI": 6,       # Fire (110) - Brightness/Screen
            "Logic": 2,    # Water (010) - Deep/Logic
            "Storage": 0,  # Earth (000) - Receptive/Storage
            "Network": 3,  # Lake (011) - Interaction/Comms
            "Core": 7,     # Heaven (111) - Origin/Kernel
            "Branch": 4    # Mountain (100) - Stillness/Decision
        }

        if query_type not in query_map:
            print(f"Unknown query type: {query_type}")
            return

        target = query_map[query_type]
        results = self.open_gate(target)

        print(f"Query: '{query_type}' -> Pattern {self.to_pix(target)}")
        print(f"Found {len(results)} resonant files:")
        for res in results:
            print(f" - {res}")


if __name__ == "__main__":
    gate = GongmyungGate()

    # Example: Find "Branching/Decision" code (Mountain / 100 / ■□□)
    # Note: In our mapping 4 is 100.
    gate.calculate_resonance("Branch")

    # Example: Find "UI/Display" code (Fire / 110 / ■■□)
    # gate.calculate_resonance("UI")
