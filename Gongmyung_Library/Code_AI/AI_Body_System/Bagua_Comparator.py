class BaguaComparator:
    def __init__(self):
        # 8괘 기본 정보 (Binary: Bottom-to-Top)
        self.trigrams = {
            "Qian": {"name": "건 (Heaven)", "bin": "111", "icon": "☰"},
            "Kun": {"name": "곤 (Earth)", "bin": "000", "icon": "☷"},
            "Li": {"name": "리 (Fire)", "bin": "101", "icon": "☲"},
            "Kan": {"name": "감 (Water)", "bin": "010", "icon": "☵"},
            "Zhen": {"name": "진 (Thunder)", "bin": "001", "icon": "☳"},
            # Note: Binary might vary by convention, using standard
            "Xun": {"name": "손 (Wind)", "bin": "110", "icon": "☴"},
            "Gen": {"name": "간 (Mountain)", "bin": "100", "icon": "☶"},
            "Dui": {"name": "태 (Lake)", "bin": "011", "icon": "☱"}
        }

    def get_layout(self, style):
        """
        Returns the South, North, East, West trigrams for the given style.
        Note: In Bagua maps, South is usually TOP, North is BOTTOM.
        """
        if style == "FuXi":  # 선천 (Early Heaven) - 우주 생성 원리 (대칭)
            return {
                "South (Top)": self.trigrams["Qian"],
                "North (Btm)": self.trigrams["Kun"],
                "East (Left)": self.trigrams["Li"],
                "West (Rght)": self.trigrams["Kan"],
                "Meaning": "천지정위 (하늘과 땅이 자리를 정함) - 완벽한 대칭/균형"
            }
        elif style == "KingWen":  # 후천 (Later Heaven) - 자연의 순환/변화
            return {
                "South (Top)": self.trigrams["Li"],
                "North (Btm)": self.trigrams["Kan"],
                "East (Left)": self.trigrams["Zhen"],
                "West (Rght)": self.trigrams["Dui"],
                "Meaning": "이화수제 (불과 물이 섞임) - 만물의 성장과 변화"
            }
        elif style == "JeongYeok":  # 정역 (Correct Change) - 완성된 미래
            return {
                "South (Top)": self.trigrams["Kun"],   # 10 (Earth)
                "North (Btm)": self.trigrams["Qian"],  # 1 (Heaven)
                "East (Left)": self.trigrams["Li"],    # 8 (Fire)
                "West (Rght)": self.trigrams["Kan"],   # 3 (Water)
                "Meaning": "지천태 (땅이 위에, 하늘이 아래에) - 상생과 완성 (11의 합)"
            }

    def display_comparison(self):
        styles = ["FuXi", "KingWen", "JeongYeok"]
        print(f"{'='*20} 팔괘 배치 비교 (Bagua Comparison) {'='*20}")

        for style in styles:
            layout = self.get_layout(style)
            print(f"\n[{style} - {layout['Meaning']}]")
            print(
                f"      {layout['South (Top)']['icon']} {layout['South (Top)']['name']}")
            print("      |")
            print(
                f"{layout['East (Left)']['icon']} --+-- {layout['West (Rght)']['icon']}")
            print("      |")
            print(
                f"      {layout['North (Btm)']['icon']} {layout['North (Btm)']['name']}")

            if style == "JeongYeok":
                print(">> 특징: 하늘(건)이 아래로 내려와 땅(곤)을 받드는 겸손과 완성의 형상")
            elif style == "FuXi":
                print(">> 특징: 하늘(건)이 위에 있어 권위와 질서를 상징")


if __name__ == "__main__":
    comparator = BaguaComparator()
    comparator.display_comparison()
