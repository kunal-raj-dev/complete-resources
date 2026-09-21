# Lecture 83: Sliding Window Maximum: Monotonic Deque (LeetCode 239)

> **One-Line Purpose:** Master double-ended monotonic decreasing queue indices to maintain sliding window maximums in strictly linear $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #83  
> **Video ID:** `XwG5cozqfaM`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=XwG5cozqfaM)  
> **Duration:** 31:22  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Monotonic Deque Implementation

```cpp
#include <vector>
#include <deque>
#include <iostream>
using namespace std;

class SolutionSlidingWindowMax {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        deque<int> dq;
        vector<int> result;

        for (int i = 0; i < nums.size(); i++) {
            // 1. Remove indices out of window boundary
            if (!dq.empty() && dq.front() <= i - k) {
                dq.pop_front();
            }

            // 2. Monotonic decreasing property
            while (!dq.empty() && nums[dq.back()] <= nums[i]) {
                dq.pop_back();
            }

            dq.push_back(i);

            // 3. Record maximum
            if (i >= k - 1) {
                result.push_back(nums[dq.front()]);
            }
        }

        return result;
    }
};
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(k)$.
