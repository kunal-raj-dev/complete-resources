# Lecture 33: String Compression (LeetCode 443)

> **One-Line Purpose:** Implement in-place Run-Length Encoding (RLE) using two pointers to compress repeating character sequences into character-count pairs.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #33  
> **Video ID:** `cAB15h6-sWA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=cAB15h6-sWA)  
> **Duration:** 19:29  
> **Status:** AUDITED  

---

## 🔵 Lecture Content & Implementation

```cpp
#include <vector>
#include <string>
#include <iostream>
using namespace std;

class SolutionStringCompression {
public:
    int compress(vector<char>& chars) {
        int n = chars.size();
        int writeIdx = 0;
        int i = 0;

        while (i < n) {
            char currChar = chars[i];
            int count = 0;

            // Count contiguous occurrences of currChar
            while (i < n && chars[i] == currChar) {
                count++;
                i++;
            }

            // Write character
            chars[writeIdx++] = currChar;

            // If count > 1, write count digits
            if (count > 1) {
                string countStr = to_string(count);
                for (char c : countStr) {
                    chars[writeIdx++] = c;
                }
            }
        }

        return writeIdx; // New length of compressed array
    }
};
```
- **Time Complexity:** $O(N)$ — Every character is read at most twice and written at most twice.
- **Space Complexity:** $O(1)$ auxiliary memory.
