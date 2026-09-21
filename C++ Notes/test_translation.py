import io
import sys
from youtube_transcript_api import YouTubeTranscriptApi

api = YouTubeTranscriptApi()
vid = "VTLCoHnyACE" # Lecture 1

tlist = api.list(vid)
print("Testing translate on", vid)
for t in tlist:
    print(f"Transcript: {t.language} ({t.language_code}) is_translatable: {t.is_translatable}")
    if t.is_translatable:
        print("Translating to English ('en')...")
        en_t = t.translate('en')
        fetched_en = en_t.fetch()
        print(f"English translation snippet count: {len(fetched_en.snippets)}")
        for s in fetched_en.snippets[:5]:
            print(f"[{s.start:.1f}s]: {s.text}")
