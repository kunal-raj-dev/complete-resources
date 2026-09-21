import subprocess
import json
import os

OUTPUT_DIR = r"C:\Users\kunal\Desktop\notes\C++ DSA - Interview Notes"
TRANSCRIPT_DIR = os.path.join(OUTPUT_DIR, ".transcripts")
TEMP_DIR = os.path.join(OUTPUT_DIR, ".temp")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

manifest_file = os.path.join(OUTPUT_DIR, "playlist_manifest.json")
processing_file = os.path.join(OUTPUT_DIR, "processing_manifest.json")

cmd = [
    r"C:\Users\kunal\AppData\Roaming\Python\Python314\Scripts\yt-dlp.exe",
    "--flat-playlist",
    "-J",
    "https://youtube.com/playlist?list=PLfqMhTWNBTe137I_EPQd34TsgV6IO55pt"
]

print("Executing yt-dlp to inspect playlist...")
res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
if res.returncode != 0:
    print("yt-dlp error:", res.stderr)
    exit(1)

data = json.loads(res.stdout)
entries = data.get("entries", [])
print(f"Discovered {len(entries)} entries in playlist.")

videos = []
for i, entry in enumerate(entries, 1):
    vid_id = entry.get("id")
    dur = entry.get("duration")
    dur_str = ""
    if dur:
        h = dur // 3600
        m = (dur % 3600) // 60
        s = dur % 60
        dur_str = f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"

    vid_info = {
        "playlist_position": i,
        "video_id": vid_id,
        "title": entry.get("title", ""),
        "url": f"https://www.youtube.com/watch?v={vid_id}",
        "duration_seconds": dur,
        "duration": dur_str,
        "status": "DISCOVERED",
        "transcription_status": "PENDING",
        "notes_status": "PENDING",
        "audited": False
    }
    videos.append(vid_info)

manifest = {
    "playlist_url": "https://youtube.com/playlist?list=PLfqMhTWNBTe137I_EPQd34TsgV6IO55pt&si=KuxJx7f5ootw2zs-",
    "playlist_title": data.get("title", "Complete C++ DSA Course | Data Structures & Algorithms Playlist"),
    "channel": data.get("uploader") or data.get("channel", "Apna College"),
    "total_videos_discovered": len(videos),
    "videos": videos
}

with open(manifest_file, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"Saved {manifest_file} with {len(videos)} videos.")
