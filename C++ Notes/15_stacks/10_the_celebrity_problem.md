# Lecture 77: The Celebrity Problem

> **One-Line Purpose:** Identify the unique party celebrity in $O(N)$ time using stack elimination or two pointers, followed by verification.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #77  
> **Video ID:** `OZPmEA_8FM8`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=OZPmEA_8FM8)  
> **Duration:** 15:11  
> **Status:** AUDITED  

---

## 🔵 Two-Pointer Elimination & Verification

```cpp
#include <vector>
#include <iostream>
using namespace std;

class SolutionCelebrity {
public:
    int celebrity(vector<vector<int>>& mat) {
        int n = mat.size();
        int top = 0, bottom = n - 1;

        // Phase 1: Elimination
        while (top < bottom) {
            if (mat[top][bottom] == 1) {
                top++;    // top knows bottom, top cannot be celebrity
            } else {
                bottom--; // top does not know bottom, bottom cannot be celebrity
            }
        }

        int candidate = top;

        // Phase 2: Verification
        for (int i = 0; i < n; i++) {
            if (i != candidate) {
                if (mat[candidate][i] == 1 || mat[i][candidate] == 0) {
                    return -1;
                }
            }
        }

        return candidate;
    }
};
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$.
