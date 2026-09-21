# Lecture 41: Subarray Sum Equals K: Prefix Sum & Hash Map (LeetCode 560)

> **One-Line Purpose:** Master the prefix sum hash table technique to count arbitrary-sum subarrays in $O(N)$ linear time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #41  
> **Video ID:** `KDH4mhFVvHw`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=KDH4mhFVvHw)  
> **Duration:** 34:45  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

- Understand why Two Pointers / Sliding Window fails when arrays contain negative integers.
- The Prefix Sum algebraic relation:
  $$\text{sum}(i, j) = \text{prefixSum}[j] - \text{prefixSum}[i - 1] = K \implies \text{prefixSum}[i - 1] = \text{prefixSum}[j] - K$$
- Why the hash map must be pre-populated with `mp[0] = 1` (accounting for subarrays starting at index $0$).

---

## 🔵 Complete C++ Implementation

```cpp
#include <vector>
#include <unordered_map>
#include <iostream>
using namespace std;

class SolutionSubarraySum {
public:
    int subarraySum(vector<int>& nums, int k) {
        unordered_map<int, int> prefixFreq;
        prefixFreq[0] = 1; // Base case: prefix sum of 0 appears once before any elements

        int currentSum = 0;
        int count = 0;

        for (int x : nums) {
            currentSum += x;
            int targetPrefix = currentSum - k;

            if (prefixFreq.count(targetPrefix)) {
                count += prefixFreq[targetPrefix];
            }

            prefixFreq[currentSum]++;
        }

        return count;
    }
};
```
- **Time Complexity:** $O(N)$ — Single linear scan with $O(1)$ average hash map lookups.
- **Space Complexity:** $O(N)$ — Hash table storing distinct prefix sums.
