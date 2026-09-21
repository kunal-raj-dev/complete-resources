# Lecture 32: Reverse Words in a String (LeetCode 151)

> **One-Line Purpose:** Master two-pointer word reversal and in-place whitespace compaction to reverse sentence semantics in $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #32  
> **Video ID:** `RitppzIdMCo`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=RitppzIdMCo)  
> **Duration:** 14:42  
> **Status:** AUDITED  

---

## 🔵 Lecture Content & Implementation

```cpp
#include <string>
#include <algorithm>
#include <iostream>
using namespace std;

class SolutionReverseWords {
public:
    string reverseWords(string s) {
        // Step 1: Reverse entire string
        reverse(s.begin(), s.end());

        int n = s.size();
        int writeIdx = 0;

        // Step 2: Traverse words and reverse each word individually
        for (int start = 0; start < n; start++) {
            if (s[start] == ' ') continue;

            if (writeIdx != 0) s[writeIdx++] = ' '; // add single separating space

            int end = start;
            while (end < n && s[end] != ' ') end++;

            int wordStart = writeIdx;
            while (start < end) {
                s[writeIdx++] = s[start++];
            }

            reverse(s.begin() + wordStart, s.begin() + writeIdx);
        }

        s.resize(writeIdx); // Trim trailing whitespace
        return s;
    }
};
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$ auxiliary (in-place modification).
