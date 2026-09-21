# Lecture 40: 4 Sum: Optimal Multi-Pointer Reduction (LeetCode 18)

> **One-Line Purpose:** Extend two-pointer quadratic reduction to 4-quadruplet discovery with 64-bit integer overflow protection.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #40  
> **Video ID:** `X6sL8JTROLY`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=X6sL8JTROLY)  
> **Duration:** 23:02  
> **Status:** AUDITED  

---

## 🔵 Lecture Content & Implementation

```cpp
#include <vector>
#include <algorithm>
using namespace std;

class SolutionFourSum {
public:
    vector<vector<int>> fourSum(vector<int>& nums, int target) {
        vector<vector<int>> res;
        int n = nums.size();
        sort(nums.begin(), nums.end());

        for (int i = 0; i < n - 3; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;

            for (int j = i + 1; j < n - 2; j++) {
                if (j > i + 1 && nums[j] == nums[j - 1]) continue;

                int left = j + 1;
                int right = n - 1;

                while (left < right) {
                    // Use 64-bit integer to prevent overflow during sum
                    long long sum = (long long)nums[i] + nums[j] + nums[left] + nums[right];

                    if (sum == target) {
                        res.push_back({nums[i], nums[j], nums[left], nums[right]});
                        while (left < right && nums[left] == nums[left + 1]) left++;
                        while (left < right && nums[right] == nums[right - 1]) right--;
                        left++;
                        right--;
                    } else if (sum < target) {
                        left++;
                    } else {
                        right--;
                    }
                }
            }
        }
        return res;
    }
};
```
- **Time Complexity:** $O(N^3)$.
- **Space Complexity:** $O(1)$ auxiliary.
