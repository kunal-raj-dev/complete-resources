# Lecture 38: Two Sum, Find Duplicate & Repeating/Missing Values

> **One-Line Purpose:** Master hash map complement lookups, Floyd's cycle detection on array indices, and algebraic sum/sum-of-squares formulas for repeating and missing values.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #38  
> **Video ID:** `0Fxc_jKj2vo`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=0Fxc_jKj2vo)  
> **Duration:** 53:30  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

- **Two Sum (LeetCode 1):** One-pass hash map complement matching in $O(N)$ time.
- **Find the Duplicate Number (LeetCode 287):** Pointer cycling via Floyd's Tortoise and Hare algorithm in $O(N)$ time and $O(1)$ space without mutating the array.
- **Find Repeating & Missing Values:** Solve via frequency hashing or mathematical equation system ($\sum x$ and $\sum x^2$).

---

## 🔵 Lecture Content & Implementations

### 1. Two Sum (One-Pass Hash Map)
```cpp
#include <vector>
#include <unordered_map>
using namespace std;

class SolutionTwoSum {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> mp;
        for (int i = 0; i < nums.size(); i++) {
            int complement = target - nums[i];
            if (mp.count(complement)) {
                return {mp[complement], i};
            }
            mp[nums[i]] = i;
        }
        return {};
    }
};
```

---

### 2. Find Duplicate Number: Floyd's Cycle Detection ($O(1)$ Space)
Since numbers are in range $[1, n]$ and array has $n + 1$ elements, each index forms a linked-list node where `next = nums[curr]`. A duplicate value indicates two indices pointing to the same node $\implies$ cycle entry point!

```cpp
class SolutionFindDuplicate {
public:
    int findDuplicate(vector<int>& nums) {
        int slow = nums[0];
        int fast = nums[0];

        // Phase 1: Detect cycle
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);

        // Phase 2: Find entrance to cycle
        slow = nums[0];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        return slow;
    }
};
```
- **Time Complexity:** $O(N)$. Space Complexity: $O(1)$ without modifying the input array.
