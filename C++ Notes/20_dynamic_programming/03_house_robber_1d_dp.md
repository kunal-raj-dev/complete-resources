# Lecture 139: DP 3: House Robber (LeetCode 198)

> **One-Line Purpose:** Maximize stolen treasure across non-adjacent houses using optimal substructure state selection in $O(N)$ time and $O(1)$ memory.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #139  
> **Video ID:** `BRmLlJA6ncI`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=BRmLlJA6ncI)  
> **Duration:** 25:43  
> **Status:** AUDITED  

---

## 🔵 Recurrence & Implementation

$$\text{rob}(i) = \max(\text{nums}[i] + \text{rob}(i - 2), \text{rob}(i - 1))$$

```cpp
#include <vector>
#include <algorithm>
using namespace std;

class SolutionHouseRobber {
public:
    int rob(vector<int>& nums) {
        int n = nums.size();
        if (n == 1) return nums[0];

        int prev2 = 0;
        int prev1 = nums[0];

        for (int i = 1; i < n; i++) {
            int pick = nums[i] + prev2;
            int notPick = prev1;
            int curr = max(pick, notPick);

            prev2 = prev1;
            prev1 = curr;
        }

        return prev1;
    }
};
```
- **Time Complexity:** $O(N)$. Space Complexity: $O(1)$.
