import os

demo_path = r"D:\Project_Gongmyung\Sample_Game_Logs"
rel_path = "guigubahuang_log.txt"
full_path = os.path.join(demo_path, rel_path)

print(f"Demo Path: {demo_path}")
print(f"Exists? {os.path.exists(demo_path)}")
print(f"Full Path: {full_path}")
print(f"File Exists? {os.path.exists(full_path)}")

with open(full_path, 'r', encoding='utf-8') as f:
    print(f"Content Preview: {f.read(50)}")
