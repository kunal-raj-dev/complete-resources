# Lecture 140: DP 4: House Robber II: Circular Array (LeetCode 213)

> **One-Line Purpose:** Solve non-adjacent maximization in circular neighborhoods by decomposing into two linear subproblems.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #140  
> **Video ID:** `hSMJj9AdNBo`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=hSMJj9AdNBo)  
> **Duration:** 22:30  
> **Status:** AUDITED  

---

## 🔵 Circular Subproblem Decomposition
Since House $0$ and House $N-1$ are adjacent, they cannot both be robbed:
- Subproblem A: Rob houses `[0 ... N - 2]` (exclude last house).
- Subproblem B: Rob houses `[1 ... N - 1]` (exclude first house).
- Global Optimal: $\max(\text{Subproblem A}, \text{Subproblem B})$.

```cpp
#include <vector>
#include <algorithm>
using namespace std;

class SolutionHouseRobberII {
private:
    int robLinear(const vector<int>& nums, int start, int end) {
        int prev2 = 0, prev1 = 0;
        for (int i = start; i <= end; i++) {
            int curr = max(nums[i] + prev2, prev1);
            prev2 = prev1;
            prev1 = curr;
        }
        return prev1;
    }

public:
    int rob(vector<int>& nums) {
        int n = nums.size();
        if (n == 1) return nums[0];
        return max(robLinear(nums, 0, n - 2), robLinear(nums, 1, n - 1));
    }
};
```
