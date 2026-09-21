import os
import re
import json
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "playlist_manifest.json")
PROCESSING = os.path.join(ROOT, "processing_manifest.json")

with open(MANIFEST, "r", encoding="utf-8") as f:
    m = json.load(f)

with open(PROCESSING, "r", encoding="utf-8") as f:
    p = json.load(f)

print("=== FINAL COURSE AUDIT RECORD ===")
print(f"Root Directory: {ROOT}")
print(f"Total Videos in Manifest: {len(m['videos'])}")
print(f"Total Videos in Processing Manifest: {len(p['records'])}")
print(f"Audited Lectures: {p['audited_lectures']}")
print(f"Blocked Lectures: {p['blocked_lectures']}")

# 1. Verify Root Files
root_files = [
    "README.md",
    "00_course_master_index.md",
    "01_course_roadmap.md",
    "02_complete_interview_bank.md",
    "03_rapid_revision.md",
    "course_concept_map.md",
    "playlist_manifest.json",
    "processing_manifest.json"
]

print("\n--- Verifying Root Files ---")
all_root_pass = True
for rf in root_files:
    path = os.path.join(ROOT, rf)
    exists = os.path.exists(path)
    sz = os.path.getsize(path) if exists else 0
    passed = exists and sz > 1000
    if not passed: all_root_pass = False
    print(f"[{'PASS' if passed else 'FAIL'}] {rf:<32} ({sz} bytes)")

# 2. Verify Topic Modules
topics = [
    "01_cpp_basics",
    "02_bitwise_number_systems",
    "03_arrays_and_vectors",
    "04_pointers",
    "05_binary_search",
    "12_recursion_and_backtracking",
    "14_linked_list"
]

print("\n--- Verifying Topic Modules ---")
all_topics_pass = True
for t in topics:
    tdir = os.path.join(ROOT, t)
    exists = os.path.exists(tdir)
    files = [f for f in os.listdir(tdir) if f.endswith(".md")] if exists else []
    # Check for master_index, topic_revision, topic_interview_questions
    has_index = "00_master_index.md" in files
    has_rev = "topic_revision.md" in files
    has_iq = "topic_interview_questions.md" in files
    passed = exists and has_index and has_rev and has_iq and len(files) >= 4
    if not passed: all_topics_pass = False
    print(f"[{'PASS' if passed else 'FAIL'}] Topic: {t:<30} ({len(files)} markdown files)")

# 3. Verify Transcripts
print("\n--- Verifying Transcripts ---")
trans_dir = os.path.join(ROOT, ".transcripts")
trans_count = 0
for r, d, fnames in os.walk(trans_dir):
    for f in fnames:
        if f.endswith(".txt"):
            trans_count += 1
print(f"Total Verified Transcripts on Disk: {trans_count}")

# 4. Check Internal Links Integrity
print("\n--- Verifying Internal Links ---")
link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
broken_links = []
for r, d, fnames in os.walk(ROOT):
    for f in fnames:
        if f.endswith(".md"):
            fp = os.path.join(r, f)
            with open(fp, "r", encoding="utf-8") as fl:
                content = fl.read()
            for text, url in link_pattern.findall(content):
                if url.startswith("http") or url.startswith("#") or url.startswith("mailto"):
                    continue
                clean_url = url.split("#")[0]
                if not clean_url:
                    continue
                target = os.path.normpath(os.path.join(r, clean_url))
                if not os.path.exists(target):
                    broken_links.append((os.path.relpath(fp, ROOT), text, url))

if not broken_links:
    print(f"[PASS] All internal Markdown links resolve successfully (0 broken links).")
else:
    print(f"[FAIL] Found {len(broken_links)} broken internal links:")
    for bl in broken_links:
        print(f"   {bl[0]}: [{bl[1]}] -> {bl[2]}")

# 5. Check Hinglish Residuals
print("\n--- Verifying Language Quality (Zero Colloquial Hinglish) ---")
hinglish_words = ['karo', 'karna', 'hoga', 'hota', 'hai', 'hain', 'bacha', 'raasta', 'kyunki', 'aage', 'pehle', 'baad', 'agar', 'bhi', 'nahi', 'karega', 'rakho', 'aakhiri', 'sabse', 'isko', 'socho', 'tumhe', 'darr', 'chhod', 'karke']
hinglish_findings = []
for r, d, fnames in os.walk(ROOT):
    for f in fnames:
        if f.endswith(".md"):
            fp = os.path.join(r, f)
            with open(fp, "r", encoding="utf-8") as fl:
                for idx, line in enumerate(fl):
                    words = re.findall(r'\b[a-zA-Z]+\b', line.lower())
                    if any(w in hinglish_words for w in words):
                        hinglish_findings.append((os.path.relpath(fp, ROOT), idx + 1, line.strip()))

if not hinglish_findings:
    print("[PASS] Zero Hinglish words found across all knowledge base files (100% clean English).")
else:
    print(f"[FAIL] Found {len(hinglish_findings)} lines with colloquial Hinglish.")

print("\nAUDIT COMPLETE.")
