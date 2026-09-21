# Lecture 31: Permutation in String: Fixed-Length Sliding Window (LeetCode 567)

> **One-Line Purpose:** Master frequency-matching over a fixed-size sliding window to detect anagrams in linear $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #31  
> **Video ID:** `VXewy91P0S4`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=VXewy91P0S4)  
> **Duration:** 21:41  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

- Understand why a permutation of $s_1$ inside $s_2$ implies a contiguous substring of length $|s_1|$ with identical character frequency distribution.
- Implement the **Fixed Sliding Window** technique with 26-element integer arrays.
- Achieve $O(|s_2|)$ time complexity with $O(1)$ constant space (26 characters).

---

## 🔵 Lecture Content & Implementation

```cpp
#include <string>
#include <vector>
#include <iostream>
using namespace std;

class SolutionPermutation {
public:
    bool checkInclusion(string s1, string s2) {
        int n1 = s1.length();
        int n2 = s2.length();
        if (n1 > n2) return false;

        vector<int> freq1(26, 0);
        vector<int> freq2(26, 0);

        // Populate initial window of size n1
        for (int i = 0; i < n1; i++) {
            freq1[s1[i] - 'a']++;
            freq2[s2[i] - 'a']++;
        }

        if (freq1 == freq2) return true;

        // Slide the window across s2
        for (int i = n1; i < n2; i++) {
            freq2[s2[i] - 'a']++;          // Add newly included character
            freq2[s2[i - n1] - 'a']--;     // Remove character falling out of window

            if (freq1 == freq2) return true;
        }

        return false;
    }
};
```
- **Time Complexity:** $O(26 \times |s_2|) = O(|s_2|)$ time.
- **Space Complexity:** $O(1)$ space (fixed 26-size frequency arrays).
