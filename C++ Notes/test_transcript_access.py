import sys
import io
import json
from youtube_transcript_api import YouTubeTranscriptApi

test_videos = [
    ("001", "VTLCoHnyACE", "Lecture 1 : Flowchart & Pseudocode"),
    ("002", "Dxu7GKtdbnA", "Lecture 2 : Variable, Data Types & Operators"),
    ("016", "qYEjR6M0wSk", "Lecture 16 : Pointers in C++"),
    ("057", "LyuuqCVkP5I", "Lecture 57 : Introduction to Linked List"),
    ("111", "RpgyCJBbl5E", "Lecture 111 : Introduction to Graphs"),
    ("137", "uBA8DkCBdco", "Lecture 137 : Dynamic Programming Intro")
]

api = YouTubeTranscriptApi()

for num, vid, title in test_videos:
    print(f"\n--- Testing Video {num}: {vid} ({title}) ---")
    try:
        tlist = api.list(vid)
        available = [(t.language, t.language_code, t.is_generated) for t in tlist]
        print(f"Available transcripts: {available}")
        
        # Try fetching Hindi or English
        pref_langs = ['en', 'hi', 'en-IN']
        # Find which of pref_langs is in tlist
        found_code = None
        for pref in pref_langs:
            for t in tlist:
                if t.language_code.startswith(pref):
                    found_code = t.language_code
                    break
            if found_code:
                break
        if not found_code and available:
            found_code = available[0][1]
            
        print(f"Fetching language: {found_code}...")
        fetched = api.fetch(vid, languages=[found_code])
        print(f"Success! Snippets count: {len(fetched.snippets)}")
        if fetched.snippets:
            first = fetched.snippets[0]
            last = fetched.snippets[-1]
            print(f"  First snippet: [{first.start:.1f}s]: {first.text}")
            print(f"  Last snippet:  [{last.start:.1f}s]: {last.text}")
    except Exception as e:
        print(f"Error fetching transcript for {vid}: {type(e).__name__} - {e}")
