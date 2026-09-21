import os

root = r"C:\Users\kunal\Desktop\notes\C++ DSA - Interview Notes"

for r, d, fnames in os.walk(root):
    for f in fnames:
        if f.endswith(".md"):
            p = os.path.join(r, f)
            with open(p, "r", encoding="utf-8") as fl:
                lines = fl.readlines()
            
            fences = []
            for i, l in enumerate(lines):
                s = l.strip()
                if s.startswith("```"):
                    fences.append((i + 1, s))
            
            if len(fences) % 2 != 0:
                print(f"Unbalanced in {os.path.relpath(p, root)}: {len(fences)} fences")
                for line_no, text in fences:
                    print(f"   Line {line_no}: {text}")
