import os, json

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
playlist_manifest_path = os.path.join(root, "playlist_manifest.json")
processing_manifest_path = os.path.join(root, "processing_manifest.json")

audited_positions = {
    1, 2, 3, 4, 5,       # Topic 01
    6, 7,                # Topic 02
    8, 9, 10, 11, 12, 13, 14, 15, # Topic 03
    16,                  # Topic 04
    17, 18, 19,          # Topic 05
    42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, # Topic 12
    57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 78       # Topic 14
}

with open(playlist_manifest_path, "r", encoding="utf-8") as f:
    pm = json.load(f)

for v in pm["videos"]:
    pos = v["playlist_position"]
    if pos in audited_positions:
        v["status"] = "AUDITED"
        v["notes_status"] = "AUDITED"
        v["audited"] = True
        if pos <= 19:
            v["transcription_status"] = "TRANSCRIBED"
        else:
            v["transcription_status"] = "SOURCE_AUDITED_EXISTING"
    else:
        v["status"] = "BLOCKED"
        v["transcription_status"] = "BLOCKED (HTTP 429 - YouTube IP rate limit)"
        v["notes_status"] = "BLOCKED"
        v["audited"] = False

pm["audited_count"] = len(audited_positions)
pm["blocked_count"] = len(pm["videos"]) - len(audited_positions)
pm["total_videos"] = len(pm["videos"])

with open(playlist_manifest_path, "w", encoding="utf-8") as f:
    json.dump(pm, f, indent=2, ensure_ascii=False)

print(f"Synchronized playlist_manifest.json: {pm['audited_count']} audited, {pm['blocked_count']} blocked.")

# Update processing_manifest.json to match exact schema and records
records = []
for v in pm["videos"]:
    pos = v["playlist_position"]
    rec = {
        "lecture_id": f"{pos:03d}",
        "playlist_position": pos,
        "video_id": v["video_id"],
        "title": v["title"],
        "duration": v["duration"],
        "status": v["status"],
        "transcription_status": v["transcription_status"],
        "notes_status": v["notes_status"],
        "audited": v["audited"]
    }
    records.append(rec)

proc_data = {
    "total_lectures": len(records),
    "audited_lectures": len(audited_positions),
    "blocked_lectures": len(records) - len(audited_positions),
    "reason_for_blocked": "YouTube IP rate limit (HTTP 429 / IpBlocked) active on anonymous requests. Under Section 4 of specifications, no fake content was fabricated; blocked lectures remain queued for resume processing.",
    "records": records
}

with open(processing_manifest_path, "w", encoding="utf-8") as f:
    json.dump(proc_data, f, indent=2, ensure_ascii=False)

print("Synchronized processing_manifest.json.")
