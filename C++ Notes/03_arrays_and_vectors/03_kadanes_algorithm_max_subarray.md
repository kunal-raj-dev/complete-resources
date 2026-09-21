# Lecture 10: Kadane's Algorithm — Maximum Subarray Sum

> **One-Line Purpose:** Master the continuous subarray concept, compare $O(N^3)$ and $O(N^2)$ approaches against Kadane's $O(N)$ dynamic programming technique, and resolve the all-negative edge case.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #10  
> **Video ID:** `9IZYqostl2M`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=9IZYqostl2M)  
> **Duration:** 23:29  
> **Transcript:** `.transcripts/03_arrays_and_vectors/010_Kadane_s_Algorithm___Maximum_Subarray_Sum___DSA_Series_by_Shradha_Ma_am.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The precise definitions and distinctions between **Subarray**, **Subsequence**, and **Subset**.
- The mathematical derivation for total subarrays in an array of size $N$ ($\frac{N(N+1)}{2}$).
- Why the Brute Force approach requires $O(N^3)$ and how Prefix Accumulation reduces it to $O(N^2)$.
- The core intuition of **Kadane's Algorithm**: why negative prefix sums are discarded immediately.
- The critical edge case: Arrays consisting exclusively of negative numbers.
- Full C++ implementation with comprehensive trace.

---

## 🔵 Lecture Context

Maximum Subarray Sum (LeetCode 53) is one of the most frequently asked interview questions across FAANG and top product companies. It serves as the primary stepping stone to 1D Dynamic Programming and greedy prefix optimization.

---

## 1. Subarray vs Subsequence vs Subset

> 🔵 **Lecture Content**

Given array `arr = [1, 2, 3]`:

| Concept | Definition | Example for `[1, 2, 3]` | Contiguous? | Total Count |
|---|---|---|---|---|
| **Subarray** | Continuous slice of an array. | `[1]`, `[2]`, `[1, 2]`, `[2, 3]`, `[1, 2, 3]` | **YES** | $\frac{N(N+1)}{2}$ |
| **Subsequence** | Derived by deleting zero or more elements without changing relative order. | `[1, 3]`, `[2]`, `[1, 2, 3]` | NO | $2^N$ |
| **Subset** | Any mathematical collection of elements; order does not matter. | `{3, 1}`, `{1, 2}` | NO | $2^N$ |

### Formula for Total Subarrays:
An array of size $N$ has:
- Subarrays of size 1: $N$
- Subarrays of size 2: $N - 1$
- $\dots$
- Subarrays of size $N$: $1$
$$\text{Total Subarrays} = N + (N-1) + (N-2) + \dots + 1 = \frac{N(N+1)}{2} = O(N^2)$$

---

## 2. Evolution of Solutions

### Approach 1: Brute Force ($O(N^3)$)
Iterate over all possible start indices $i$, all possible end indices $j$, and compute the sum using a third loop $k$ from $i$ to $j$.
```cpp
int maxSubarraySumBrute(const vector<int>& nums) {
    int n = nums.size();
    int maxSum = INT_MIN;

    for (int i = 0; i < n; i++) {
        for (int j = i; j < n; j++) {
            int currentSum = 0;
            for (int k = i; k <= j; k++) {
                currentSum += nums[k];
            }
            maxSum = max(maxSum, currentSum);
        }
    }
    return maxSum;
}
```
- **Complexity:** Time: $O(N^3)$, Space: $O(1)$. TLE (Time Limit Exceeded) for $N \ge 10^3$.

---

### Approach 2: Optimized Prefix Summation ($O(N^2)$)
Avoid the third loop by maintaining a running sum as the ending index $j$ expands.
```cpp
int maxSubarraySumBetter(const vector<int>& nums) {
    int n = nums.size();
    int maxSum = INT_MIN;

    for (int i = 0; i < n; i++) {
        int currentSum = 0;
        for (int j = i; j < n; j++) {
            currentSum += nums[j];
            maxSum = max(maxSum, currentSum);
        }
    }
    return maxSum;
}
```
- **Complexity:** Time: $O(N^2)$, Space: $O(1)$. TLE for $N \ge 10^5$.

---

### Approach 3: Kadane's Algorithm (Optimal $O(N)$)

> 💡 **Intuition:**
> As you traverse the array from left to right, keep accumulating numbers into `currSum`.
> - If `currSum` becomes **negative**, it is a liability! Adding a negative prefix to any subsequent subarray will only **reduce** its potential sum.
> - Therefore, whenever `currSum < 0`, immediately reset `currSum = 0` (start fresh from the next element).

```cpp
#include <iostream>
#include <vector>
#include <climits>
using namespace std;

int maxSubArray(const vector<int>& nums) {
    int maxSum = INT_MIN;
    int currSum = 0;

    for (int val : nums) {
        currSum += val;
        maxSum = max(maxSum, currSum);

        if (currSum < 0) {
            currSum = 0; // Reset liability
        }
    }
    return maxSum;
}
```

---

## 🔍 Detailed Trace

Input: `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`

| Index | `val` | `currSum += val` | `maxSum = max(maxSum, currSum)` | `currSum < 0` ? Reset |
|---|---|---|---|---|
| Init | — | 0 | `INT_MIN` | — |
| 0 | -2 | -2 | `max(INT_MIN, -2) = -2` | Yes $\to$ `currSum = 0` |
| 1 | 1 | 1 | `max(-2, 1) = 1` | No |
| 2 | -3 | -2 | `max(1, -2) = 1` | Yes $\to$ `currSum = 0` |
| 3 | 4 | 4 | `max(1, 4) = 4` | No |
| 4 | -1 | 3 | `max(4, 3) = 4` | No |
| 5 | 2 | 5 | `max(4, 5) = 5` | No |
| 6 | 1 | 6 | `max(5, 6) = 6` | No |
| 7 | -5 | 1 | `max(6, 1) = 6` | No |
| 8 | 4 | 5 | `max(6, 5) = 6` | No |

**Final Result:** `maxSum = 6` (corresponding to subarray `[4, -1, 2, 1]`).

---

## ⚠️ The All-Negative Edge Case

> 🧠 **Brain Trigger**
> 
> What happens if the array contains only negative numbers, e.g., `nums = [-5, -2, -8, -1]`?
> 
> **Answer:** If we update `maxSum` **after** resetting `currSum = 0`, the algorithm would mistakenly return `0`. But by placing `maxSum = max(maxSum, currSum)` **before** `if (currSum < 0) currSum = 0;`, `maxSum` correctly captures `-1` (the maximum single negative value).

---

## 🔥 Interview Questions

### Q1: [Follow-up] How do you return the actual Subarray (indices `start` and `end`) that achieves the maximum sum?
- **Short Answer:** Maintain `start`, `end`, and a tracking variable `tempStart` that updates whenever `currSum` resets to 0.
- **Code:**
  ```cpp
  pair<int, int> maxSubArrayIndices(const vector<int>& nums) {
      int maxSum = INT_MIN, currSum = 0;
      int start = 0, end = 0, tempStart = 0;

      for (int i = 0; i < nums.size(); i++) {
          currSum += nums[i];
          if (currSum > maxSum) {
              maxSum = currSum;
              start = tempStart;
              end = i;
          }
          if (currSum < 0) {
              currSum = 0;
              tempStart = i + 1;
          }
      }
      return {start, end};
  }
  ```

---

## Key Takeaways

1. **Subarray Count:** $\frac{N(N+1)}{2}$ contiguous slices.
2. **Kadane's Rule:** Discard negative prefix sums by resetting `currSum = 0`.
3. **Complexity:** $O(N)$ Time, $O(1)$ Space.
4. **All-Negative Safety:** Update `maxSum` before resetting `currSum`.

---

## ⚡ 2-Minute Revision

- Subarray is contiguous; Subsequence preserves relative order; Subset has no order constraints.
- Kadane's single loop:
  ```cpp
  currSum += x;
  maxSum = max(maxSum, currSum);
  if (currSum < 0) currSum = 0;
  ```
- Handles all-negative arrays correctly when `maxSum` starts at `INT_MIN`.
