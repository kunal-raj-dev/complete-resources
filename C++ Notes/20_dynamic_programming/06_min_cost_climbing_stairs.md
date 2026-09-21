# Lecture 142: DP 6: Min Cost Climbing Stairs (LeetCode 746)

> **One-Line Purpose:** Find minimum cost path to reach the top of a staircase starting from step 0 or step 1.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #142  
> **Video ID:** `KwItlcfF9vE`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=KwItlcfF9vE)  
> **Duration:** 26:08  
> **Status:** AUDITED  

---

## 🔵 Implementation

```cpp
#include <vector>
#include <algorithm>
using namespace std;

class SolutionMinCostClimbingStairs {
public:
    int minCostClimbingStairs(vector<int>& cost) {
        int n = cost.size();
        int prev2 = cost[0];
        int prev1 = cost[1];

        for (int i = 2; i < n; i++) {
            int curr = cost[i] + min(prev1, prev2);
            prev2 = prev1;
            prev1 = curr;
        }

        return min(prev1, prev2);
    }
};
```
