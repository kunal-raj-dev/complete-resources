# Lecture 11: Majority Element & Moore's Voting Algorithm + Pair Sum

> **One-Line Purpose:** Master the Two-Pointer Pair Sum technique and Boyer-Moore's Voting Algorithm to identify the majority element ($> \lfloor N/2 \rfloor$) in $O(N)$ time and $O(1)$ auxiliary space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #11  
> **Video ID:** `_xqIp2rj8bo`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=_xqIp2rj8bo)  
> **Duration:** 39:10  
> **Transcript:** `.transcripts/03_arrays_and_vectors/011_Majority_Element___Brute-_Better-Best_Approach___Moore_s_Voting_Algorithm____Pai.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The Two-Pointer Pair Sum technique on sorted arrays ($O(N)$ time, $O(1)$ space).
- The formal definition of Majority Element (frequency strictly $> \lfloor N/2 \rfloor$).
- Progressive algorithmic evolution:
  - Brute Force: $O(N^2)$ time, $O(1)$ space.
  - Sorting Method: $O(N \log N)$ time, $O(1)$ space.
  - Frequency Hash Map: $O(N)$ time, $O(N)$ space.
  - **Boyer-Moore's Voting Algorithm**: $O(N)$ time, $O(1)$ space.
- The mathematical cancellation intuition underpinning Moore's Voting Algorithm.
- The necessity of a second verification pass when majority element existence is not guaranteed.

---

## 🔵 Lecture Context

Finding the Majority Element is a canonical interview question testing your ability to move beyond standard Hash Map solutions ($O(N)$ space) to achieve optimal $O(1)$ memory. The cancellation logic introduced here directly generalizes to Moore's Voting Algorithm for elements appearing $> \lfloor N/3 \rfloor$ times (LeetCode 229).

---

## 1. Problem 1: Pair Sum in Sorted Array

> 🔵 **Lecture Content**

**Problem:** Given a sorted array and a `target`, find two distinct indices whose elements sum to `target`.

### Two-Pointer Optimal Approach:
1. Initialize `left = 0`, `right = n - 1`.
2. Compute `currentSum = arr[left] + arr[right]`.
3. If `currentSum == target` $\to$ return `{left, right}`.
4. If `currentSum < target` $\to$ increment `left++` (increase sum).
5. If `currentSum > target` $\to$ decrement `right--` (decrease sum).

```cpp
#include <vector>
#include <iostream>
using namespace std;

vector<int> pairSum(const vector<int>& nums, int target) {
    int left = 0, right = nums.size() - 1;

    while (left < right) {
        int sum = nums[left] + nums[right];
        if (sum == target) {
            return {left, right};
        } else if (sum < target) {
            left++;
        } else {
            right--;
        }
    }
    return {}; // No pair found
}
```
- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(1)$

---

## 2. Problem 2: Majority Element (LeetCode 169)

> 🔵 **Lecture Content**

An element is a **Majority Element** if it occurs **strictly more than $\lfloor N / 2 \rfloor$ times** in an array of size $N$.

---

### Solution Evolution

#### 1. Sorting Approach ($O(N \log N)$ Time, $O(1)$ Space)
If an element occurs $> N/2$ times, sorting the array guarantees that this element will occupy the middle index $\lfloor N / 2 \rfloor$.
```cpp
int majorityElementSorting(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    return nums[nums.size() / 2];
}
```

#### 2. Hash Map Approach ($O(N)$ Time, $O(N)$ Space)
Count frequencies in an `unordered_map<int, int>` and check if `count > N / 2`.

---

### 3. Boyer-Moore's Voting Algorithm (Optimal: $O(N)$ Time, $O(1)$ Space)

> 💡 **Core Intuition (Pairwise Cancellation):**
> Imagine an election where the majority candidate holds more than 50% of the total votes. If every non-majority voter pairs up with a majority voter to cancel each other out, the majority candidate will **still have at least one vote remaining** at the end.

#### Algorithm Steps:
1. Initialize `candidate = 0`, `count = 0`.
2. Traverse array:
   - If `count == 0`, set `candidate = nums[i]`.
   - If `nums[i] == candidate`, increment `count++`.
   - Else, decrement `count--`.
3. `candidate` is the winner.

```cpp
#include <vector>
#include <iostream>
using namespace std;

int majorityElement(const vector<int>& nums) {
    int candidate = 0;
    int count = 0;

    for (int num : nums) {
        if (count == 0) {
            candidate = num;
        }
        if (num == candidate) {
            count++;
        } else {
            count--;
        }
    }

    // Verification Pass (Necessary if existence is not guaranteed)
    int freq = 0;
    for (int num : nums) {
        if (num == candidate) freq++;
    }
    if (freq > nums.size() / 2) {
        return candidate;
    }

    return -1; // No majority element exists
}
```

---

## 🔍 Detailed Trace

Input: `nums = [2, 2, 1, 1, 1, 2, 2]` ($N = 7$, threshold $> 3.5 \to 4$)

| Index | `num` | `count` Before | `candidate` | Action Taken | `count` After |
|---|---|---|---|---|---|
| 0 | 2 | 0 | 2 (new) | Match $\to$ `count++` | 1 |
| 1 | 2 | 1 | 2 | Match $\to$ `count++` | 2 |
| 2 | 1 | 2 | 2 | Mismatch $\to$ `count--` | 1 |
| 3 | 1 | 1 | 2 | Mismatch $\to$ `count--` | 0 |
| 4 | 1 | 0 | 1 (new) | Match $\to$ `count++` | 1 |
| 5 | 2 | 1 | 1 | Mismatch $\to$ `count--` | 0 |
| 6 | 2 | 0 | 2 (new) | Match $\to$ `count++` | 1 |

**Winner Candidate:** `2`.  
Verification: `2` appears 4 times in `[2, 2, 1, 1, 1, 2, 2]`. $4 > 7/2$. Valid!

---

## 🔥 Interview Questions

### Q1: Can Boyer-Moore's Voting Algorithm identify a majority element if the threshold is $> \lfloor N / 3 \rfloor$?
- **Short Answer:** Yes! We maintain **two candidates** and **two counters** (since at most 2 distinct elements can each appear $> N/3$ times).
- **Explanation:** This is LeetCode 229 (Majority Element II). When an incoming element matches neither candidate, both counters are decremented simultaneously (canceling triplets of distinct elements).

---

## Key Takeaways

1. **Pair Sum:** Two pointers from boundaries converge in $O(N)$ on sorted inputs.
2. **Moore's Logic:** Pairwise cancellation guarantees the $> 50\%$ candidate survives.
3. **Efficiency:** Reduces auxiliary space from $O(N)$ (Hash Map) down to $O(1)$.
4. **Verification:** Always run a second pass if the existence of a majority element is not guaranteed.

---

## ⚡ 2-Minute Revision

- **Pair Sum:** `sum < target ? left++ : right--`.
- **Moore's Loop:**
  ```cpp
  if (count == 0) candidate = x;
  count += (x == candidate) ? 1 : -1;
  ```
- **Time/Space:** $O(N)$ Time, $O(1)$ Space.
