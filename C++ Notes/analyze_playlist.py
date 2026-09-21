import json

manifest_file = r"C:\Users\kunal\Desktop\notes\C++ DSA - Interview Notes\playlist_manifest.json"
with open(manifest_file, "r", encoding="utf-8") as f:
    manifest = json.load(f)

videos = manifest["videos"]
print("=== VIDEOS 1 TO 45 ===")
for v in videos[:45]:
    print(f"{v['playlist_position']:03d} | {v['video_id']} | {v['duration']:>8} | {v['title']}")

print("\n=== VIDEOS 46 TO 90 ===")
for v in videos[45:90]:
    print(f"{v['playlist_position']:03d} | {v['video_id']} | {v['duration']:>8} | {v['title']}")

print("\n=== VIDEOS 91 TO 144 ===")
for v in videos[90:]:
    print(f"{v['playlist_position']:03d} | {v['video_id']} | {v['duration']:>8} | {v['title']}")
