import os
import json
import time
from youtube_transcript_api import YouTubeTranscriptApi

ROOT_DIR = r"C:\Users\kunal\Desktop\notes\C++ DSA - Interview Notes"
MANIFEST_PATH = os.path.join(ROOT_DIR, "playlist_manifest.json")
TRANSCRIPTS_DIR = os.path.join(ROOT_DIR, ".transcripts")

# Mapping of playlist position to topic folder
def get_topic_folder(pos, title):
    if 1 <= pos <= 5:
        return "01_cpp_basics"
    elif 6 <= pos <= 7:
        return "02_bitwise_number_systems"
    elif 8 <= pos <= 15:
        return "03_arrays_and_vectors"
    elif pos == 16:
        return "04_pointers"
    elif 17 <= pos <= 23:
        return "05_binary_search"
    elif 24 <= pos <= 26:
        return "06_sorting_algorithms"
    elif 27 <= pos <= 28:
        return "07_cpp_stl"
    elif 29 <= pos <= 33:
        return "08_strings_and_character_arrays"
    elif pos == 34:
        return "09_maths_for_dsa"
    elif 35 <= pos <= 37:
        return "10_2d_arrays_and_matrices"
    elif 38 <= pos <= 41:
        return "11_hashing_and_subarrays"
    elif 42 <= pos <= 55:
        return "12_recursion_and_backtracking"
    elif pos == 56:
        return "13_oops"
    elif 57 <= pos <= 67 or pos == 78:
        return "14_linked_list"
    elif 68 <= pos <= 77:
        return "15_stacks"
    elif 79 <= pos <= 84:
        return "16_queues"
    elif 85 <= pos <= 97:
        return "17_binary_trees"
    elif 98 <= pos <= 110:
        return "18_binary_search_trees"
    elif 111 <= pos <= 136:
        return "19_graphs"
    elif 137 <= pos <= 144:
        return "20_dynamic_programming"
    else:
        return "21_misc"

def sanitize_filename(name):
    clean = "".join(c if c.isalnum() or c in " -_." else "_" for c in name)
    clean = "_".join(clean.split())
    return clean[:80]

def format_timestamp(seconds):
    s = int(seconds)
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    return f"[{h:02d}:{m:02d}:{sec:02d}]"

def fetch_all_transcripts(limit=None):
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    videos = manifest["videos"]
    if limit:
        videos = videos[:limit]

    api = YouTubeTranscriptApi()
    success_count = 0
    fail_count = 0

    print(f"Starting transcript acquisition for {len(videos)} videos...")

    for v in videos:
        pos = v["playlist_position"]
        vid = v["video_id"]
        title = v["title"]
        topic = get_topic_folder(pos, title)
        topic_dir = os.path.join(TRANSCRIPTS_DIR, topic)
        os.makedirs(topic_dir, exist_ok=True)

        safe_title = sanitize_filename(title)
        filename = f"{pos:03d}_{safe_title}.txt"
        file_path = os.path.join(topic_dir, filename)

        if os.path.exists(file_path) and os.path.getsize(file_path) > 100:
            print(f"[{pos:03d}/144] Transcript already exists: {filename}")
            v["transcription_status"] = "TRANSCRIBED"
            success_count += 1
            continue

        print(f"[{pos:03d}/144] Fetching transcript for {vid}: {title}...")
        try:
            tlist = api.list(vid)
            # Find appropriate language
            target_t = None
            for t in tlist:
                if t.language_code in ['hi', 'en', 'en-IN']:
                    target_t = t
                    break
            if not target_t:
                target_t = tlist[0]

            fetched = target_t.fetch()
            snippets = fetched.snippets

            with open(file_path, "w", encoding="utf-8") as out:
                out.write(f"Source: https://www.youtube.com/watch?v={vid}\n")
                out.write(f"Lecture #{pos}: {title}\n")
                out.write(f"Language: {target_t.language} ({target_t.language_code})\n")
                out.write(f"Snippets: {len(snippets)}\n")
                out.write("=" * 60 + "\n\n")

                for s in snippets:
                    ts = format_timestamp(s.start)
                    out.write(f"{ts} {s.text}\n")

            v["transcription_status"] = "TRANSCRIBED"
            v["transcript_path"] = os.path.relpath(file_path, ROOT_DIR).replace("\\", "/")
            print(f"  -> Saved {len(snippets)} snippets to {filename}")
            success_count += 1
        except Exception as e:
            print(f"  -> FAILED {vid}: {e}")
            v["transcription_status"] = f"FAILED: {str(e)[:100]}"
            fail_count += 1

        time.sleep(0.5)

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\nTranscript Acquisition Complete. Success: {success_count}, Failed: {fail_count}")

if __name__ == "__main__":
    fetch_all_transcripts()
