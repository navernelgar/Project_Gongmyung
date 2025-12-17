import os
import json
import glob

SEARCH_TERM = "플러그인"
DIR = r"d:\workspaceStorage\chat"

def search():
    files = glob.glob(os.path.join(DIR, "*.json"))
    for fpath in files:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                text = json.dumps(data, ensure_ascii=False)
                if SEARCH_TERM in text:
                    print(f"Found in: {fpath}")
                    # Print a snippet
                    idx = text.find(SEARCH_TERM)
                    print(text[idx-50:idx+50])
        except Exception as e:
            print(f"Error {fpath}: {e}")

if __name__ == "__main__":
    search()
