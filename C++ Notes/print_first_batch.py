import json

manifest_file = r"C:\Users\kunal\Desktop\notes\C++ DSA - Interview Notes\playlist_manifest.json"
with open(manifest_file, "r", encoding="utf-8") as f:
    manifest = json.load(f)

for v in manifest["videos"][:48]:
    print(f"{v['playlist_position']:03d} | {v['video_id']} | {v['duration']:>8} | {v['title']}")
