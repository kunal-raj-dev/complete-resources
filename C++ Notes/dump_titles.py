import json

manifest_file = r"C:\Users\kunal\Desktop\notes\C++ DSA - Interview Notes\playlist_manifest.json"
with open(manifest_file, "r", encoding="utf-8") as f:
    manifest = json.load(f)

with open(r"C:\Users\kunal\Desktop\notes\C++ DSA - Interview Notes\.scripts\all_titles.txt", "w", encoding="utf-8") as out:
    for v in manifest["videos"]:
        out.write(f"{v['playlist_position']:03d} | {v['video_id']} | {v['duration']:>8} | {v['title']}\n")

print("Dumped all 144 titles to all_titles.txt")
