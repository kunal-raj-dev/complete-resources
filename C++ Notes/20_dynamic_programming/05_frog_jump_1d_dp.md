# Lecture 141: DP 5: Frog Jump: Energy Optimization

> **One-Line Purpose:** Minimize energy expenditure for a frog leaping 1 or 2 stairs with height difference costs.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #141  
> **Video ID:** `AKqlgskrZwI`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=AKqlgskrZwI)  
> **Duration:** 29:29  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Implementation

$$\text{energy}[i] = \min(\text{energy}[i-1] + |h[i] - h[i-1]|, \text{energy}[i-2] + |h[i] - h[i-2]|)$$

```cpp
#include <vector>
#include <cmath>
#include <algorithm>
using namespace std;

int frogJump(int n, vector<int>& heights) {
    int prev2 = 0;
    int prev1 = 0;

    for (int i = 1; i < n; i++) {
        int stepOne = prev1 + abs(heights[i] - heights[i - 1]);
        int stepTwo = (i > 1) ? prev2 + abs(heights[i] - heights[i - 2]) : 1e9;

        int curr = min(stepOne, stepTwo);
        prev2 = prev1;
        prev1 = curr;
    }

    return prev1;
}
```
