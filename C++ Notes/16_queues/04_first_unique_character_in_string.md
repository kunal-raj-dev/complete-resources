# Lecture 82: First Unique Character in String (LeetCode 387)

> **One-Line Purpose:** Locate the first non-repeating character in a stream/string using frequency mapping and queue FIFO order.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #82  
> **Video ID:** `sqyCBvEQN9c`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=sqyCBvEQN9c)  
> **Duration:** 13:23  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Implementation

```cpp
#include <string>
#include <vector>
#include <queue>
using namespace std;

class SolutionFirstUnique {
public:
    int firstUniqChar(string s) {
        vector<int> freq(26, 0);
        for (char ch : s) freq[ch - 'a']++;

        for (int i = 0; i < s.length(); i++) {
            if (freq[s[i] - 'a'] == 1) return i;
        }
        return -1;
    }
};
```
