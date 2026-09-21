import os, re

root = r"C:\Users\kunal\Desktop\notes\C++ DSA - Interview Notes"

hinglish_words = ['karo', 'karna', 'hoga', 'hota', 'hai', 'hain', 'bacha', 'raasta', 'kyunki', 'aage', 'pehle', 'baad', 'agar', 'bhi', 'nahi', 'karega', 'rakho', 'aakhiri', 'sabse', 'isko', 'socho', 'tumhe', 'darr', 'chhod', 'karke']

for topic in ["12_recursion_and_backtracking", "14_linked_list"]:
    tdir = os.path.join(root, topic)
    print(f"\n=== {topic} ===")
    for f in sorted(os.listdir(tdir)):
        if f.endswith(".md"):
            fp = os.path.join(tdir, f)
            with open(fp, "r", encoding="utf-8") as fl:
                lines = fl.readlines()
            h_count = 0
            for l in lines:
                words = re.findall(r'\b[a-zA-Z]+\b', l.lower())
                if any(w in hinglish_words for w in words):
                    h_count += 1
            print(f"  {f:<45} | Lines: {len(lines):<4} | Hinglish lines: {h_count}")
