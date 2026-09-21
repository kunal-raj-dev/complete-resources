# Lecture 39: 3 Sum: Sorting & Two Pointers (LeetCode 15)

> **One-Line Purpose:** Master two-pointer inward scanning with comprehensive duplicate skipping to identify all unique zero-sum triplets in $O(N^2)$ time and $O(1)$ auxiliary space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #39  
> **Video ID:** `K-RsltkN63w`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=K-RsltkN63w)  
> **Duration:** 43:43  
> **Status:** AUDITED  

---

## 🔵 Lecture Content & Implementation

```cpp
#include <vector>
#include <algorithm>
#include <iostream>
using namespace std;

class SolutionThreeSum {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        vector<vector<int>> res;
        int n = nums.size();
        sort(nums.begin(), nums.end()); // Crucial: Sort first

        for (int i = 0; i < n - 2; i++) {
            // Optimization: If smallest element is > 0, three positive numbers cannot sum to 0
            if (nums[i] > 0) break;

            // Skip duplicates for the first element
            if (i > 0 && nums[i] == nums[i - 1]) continue;

            int left = i + 1;
            int right = n - 1;

            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];

                if (sum == 0) {
                    res.push_back({nums[i], nums[left], nums[right]});

                    // Skip duplicates for left and right
                    while (left < right && nums[left] == nums[left + 1]) left++;
                    while (left < right && nums[right] == nums[right - 1]) right--;

                    left++;
                    right--;
                } else if (sum < 0) {
                    left++;
                } else {
                    right--;
                }
            }
        }
        return res;
    }
};
```
- **Time Complexity:** $O(N \log N + N^2) = O(N^2)$.
- **Space Complexity:** $O(1)$ auxiliary (excluding output).
