# Lecture 18: Search in Rotated Sorted Array (LeetCode 33)

> **One-Line Purpose:** Master the Modified Binary Search technique on rotated arrays by identifying which half is sorted at every step, achieving strict $O(\log N)$ time and $O(1)$ auxiliary space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #18  
> **Video ID:** `6WNZQBHWQJs`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=6WNZQBHWQJs)  
> **Duration:** 19:30  
> **Transcript:** `.transcripts/05_binary_search/018_Search_in_Rotated_Sorted_Array___Binary_Search___Leetcode_33.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- What a Rotated Sorted Array is and why linear scan ($O(N)$) fails the logarithmic interview requirement.
- The fundamental mathematical invariant: **At least one half of a rotated sorted array is always strictly sorted**.
- How to check whether the left half vs right half is sorted using `nums[start] <= nums[mid]`.
- Two-level decision tree logic to discard the unsorted or non-target half in $O(1)$ time at each step.
- Full C++ implementation, line-by-line tracing, edge cases, and the critical follow-up problem with duplicates (LeetCode 81).

---

## 🔵 Lecture Context

Search in Rotated Sorted Array is a Tier-1 FAANG interview problem. It tests whether an engineer truly understands the prerequisite of Binary Search—not that the *entire* array must be monotonically sorted, but that you must be able to deterministically eliminate half the search space on every iteration.

---

## 1. Problem Statement & Rotation Mechanics

An array originally sorted in ascending order with distinct values is rotated around an unknown pivot index $k$ ($1 \le k < n$):
$$\text{Original:} \quad [0, 1, 2, 4, 5, 6, 7]$$
$$\text{Rotated at pivot 3:} \quad [4, 5, 6, 7, 0, 1, 2]$$

**Goal:** Given `target`, return its index in $O(\log N)$ time. Return `-1` if target does not exist.

---

## 2. The Core Algorithmic Insight

> 💡 **The Half-Sorted Invariant:**
> When you choose any arbitrary midpoint `mid`, the array is split into two halves:
> `[start ... mid]` (Left Half) and `[mid ... end]` (Right Half).
> **No matter how many times or where the array is rotated, AT LEAST ONE of these two halves is guaranteed to be strictly sorted!**

```
Array: [ 4 | 5 | 6 | 7 | 0 | 1 | 2 ]
  start = 0 (val 4), mid = 3 (val 7), end = 6 (val 2)

Notice:
nums[start] <= nums[mid] (4 <= 7) -> The LEFT half [4, 5, 6, 7] is SORTED!
The right half [7, 0, 1, 2] contains the rotation pivot (unsorted).
```

---

## 3. The 2-Case Decision Logic

### Case 1: Is the Left Half Sorted?
If `nums[start] <= nums[mid]`: The Left Half `[start ... mid]` is sorted.
- **Does `target` lie inside this sorted Left Half?**  
  Check: `target >= nums[start] && target < nums[mid]`.
  - **Yes:** Search left $\to$ `end = mid - 1`.
  - **No:** Search right $\to$ `start = mid + 1`.

### Case 2: Otherwise, the Right Half MUST be Sorted!
If `nums[start] > nums[mid]`: The Right Half `[mid ... end]` is sorted.
- **Does `target` lie inside this sorted Right Half?**  
  Check: `target > nums[mid] && target <= nums[end]`.
  - **Yes:** Search right $\to$ `start = mid + 1`.
  - **No:** Search left $\to$ `end = mid - 1`.

---

## 4. Complete C++ Implementation

```cpp
#include <vector>
#include <iostream>
using namespace std;

int search(const vector<int>& nums, int target) {
    int start = 0;
    int end = nums.size() - 1;

    while (start <= end) {
        int mid = start + (end - start) / 2;

        if (nums[mid] == target) {
            return mid; // Target found
        }

        // Case 1: Left Half is Sorted
        if (nums[start] <= nums[mid]) {
            if (target >= nums[start] && target < nums[mid]) {
                end = mid - 1;   // Target lies in left sorted half
            } else {
                start = mid + 1; // Target lies in right half
            }
        }
        // Case 2: Right Half is Sorted
        else {
            if (target > nums[mid] && target <= nums[end]) {
                start = mid + 1; // Target lies in right sorted half
            } else {
                end = mid - 1;   // Target lies in left half
            }
        }
    }

    return -1; // Target not found
}

int main() {
    vector<int> nums = {4, 5, 6, 7, 0, 1, 2};
    int target = 0;
    int index = search(nums, target);
    cout << "Target index: " << index << "\n"; // Output: 4
    return 0;
}
```

- **Time Complexity:** $O(\log_2 N)$ (Halves the search space on each iteration).
- **Space Complexity:** $O(1)$ auxiliary memory.

---

## 🔍 Detailed Trace

Input: `nums = [4, 5, 6, 7, 0, 1, 2]`, `target = 0`

| Iteration | `start` | `end` | `mid` | `nums[mid]` | Which Half Sorted? | Target Range Check | Action Taken |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 7 | Left (`4 <= 7`) | `0 >= 4 && 0 < 7` (False) | `start = mid + 1 = 4` |
| 2 | 4 | 6 | 5 | 1 | Right (`1 <= 2`) | `0 > 1 && 0 <= 2` (False) | `end = mid - 1 = 4` |
| 3 | 4 | 4 | 4 | 0 | Equal | `nums[4] == 0` (Match!) | **Return 4** |

---

## 🧠 Mental Model

Visualize the rotated array as two rising linear line segments separated by a cliff (the rotation drop):
```
Values
  ^
  |        /| (Segment 1: High Sorted Range)
  |       / |
  |      /  |
  |     /   |
  |    /    |          /| (Segment 2: Low Sorted Range)
  |   /     |         / |
  |  /      |        /  |
  +---------+-----------+-----> Indices
    start  mid-1    end
```
When choosing `mid`:
- If `nums[start] <= nums[mid]`, both `start` and `mid` reside on Segment 1 $\implies$ The range between them is continuous and strictly increasing.
- If `nums[start] > nums[mid]`, the cliff lies between `start` and `mid`, which mathematically guarantees that the right half `[mid ... end]` resides cleanly on Segment 2 and is strictly sorted.

---

## ⚠️ Common Mistakes

1. **Forgetting `<=` in sorted check:** Writing `if (nums[start] < nums[mid])` fails when `start == mid` (e.g. array of size 1 or 2). Always write `nums[start] <= nums[mid]`.
2. **Inclusive vs Exclusive boundary checks:** In `target >= nums[start] && target < nums[mid]`, using `<` for `nums[mid]` is intentional because `nums[mid] == target` was already handled by the early exit check.
3. **Integer overflow on `mid`:** Always use `mid = start + (end - start) / 2` rather than `(start + end) / 2`.

---

## 🖥️ System-Specific Notes

- **Cache Locality:** Binary search performs non-sequential memory jumps ($N/2, N/4, \dots$). On modern x86/ARM architectures, this incurs cache misses compared to sequential scans. However, because $\log_2(10^6) \approx 20$ iterations versus $10^6$ comparisons, the algorithmic speedup dwarfs any cache penalty.
- **Signed Integer Sizes:** If indices exceed $2^{31}-1$, `int` must be replaced with `int64_t` or `size_t`.

---

## 🟡 Additional Essential Context

The technique of identifying a sorted monotone subrange and checking target membership before pruning is called **Domain Reduction via Invariant Elimination**. It extends to:
- Finding the Minimum in Rotated Sorted Array (LeetCode 153).
- Finding the Rotation Count of a Sorted Array.
- Searching in a 2D sorted matrix.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why can we only check target membership against the half that is sorted?  
**A:** If a half is unsorted, it contains a discontinuous jump (the rotation pivot). You cannot tell whether a target is inside an unsorted range simply by checking its endpoints! Only a sorted subrange allows a deterministic $O(1)$ boundary check: `target >= start && target <= end`.

**Q2:** What happens when `start == end`?  
**A:** `mid = start`. If `nums[mid] == target`, it returns `mid`. Otherwise, the boundary condition updates (`start = mid + 1` or `end = mid - 1`), causing `start > end`, which cleanly terminates the `while (start <= end)` loop and returns `-1`.

---

### 🔥 Interview Questions

#### Q1: [Follow-up / LeetCode 81] What if the array contains DUPLICATES (e.g. `[1, 0, 1, 1, 1]`)?
- **Short Answer:** The worst-case time complexity degrades from $O(\log N)$ to $O(N)$.
- **Detailed Explanation:** When `nums[start] == nums[mid] == nums[end]`, both `nums[start] <= nums[mid]` and `nums[mid] <= nums[end]` are true, making it impossible to determine whether the left or right half is sorted! The only safe action is to shrink the search space linearly by incrementing `start++` and decrementing `end--`. In the worst case (e.g. `[1, 1, 1, 1, 2, 1, 1]`), this linear shrinkage runs in $O(N)$ time.
- **Why Interviewers Ask:** Evaluates whether you know the mathematical limits of binary search and how duplicate elements destroy monotonicity.

#### Q2: How do you find the rotation pivot index $k$ in $O(\log N)$?
- **Short Answer:** Binary search for the unique index where `nums[i] > nums[i+1]`, or find the minimum element (LeetCode 153).
- **Detailed Explanation:** Compare `nums[mid]` with `nums[end]`. If `nums[mid] > nums[end]`, the minimum element (and the pivot) lies strictly to the right (`start = mid + 1`). Otherwise, it lies at or to the left of `mid` (`end = mid`).

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
#include <iostream>
#include <vector>
using namespace std;

int search(const vector<int>& nums, int target);

int main() {
    vector<int> nums = {5, 1, 3};
    cout << search(nums, 5) << " ";
    cout << search(nums, 1) << " ";
    cout << search(nums, 2) << "\n";
    return 0;
}
```
**Output:** `0 1 -1`  
**Explanation:** `nums[0] = 5`, `nums[1] = 1`. Target 2 is absent, returning `-1`.

---

### 🐛 Debugging Challenge
What is wrong with this implementation?
```cpp
int buggySearch(const vector<int>& nums, int target) {
    int start = 0, end = nums.size() - 1;
    while (start <= end) {
        int mid = start + (end - start) / 2;
        if (nums[mid] == target) return mid;
        
        if (nums[start] < nums[mid]) { // <-- SUBTLE BUG!
            if (target >= nums[start] && target < nums[mid]) end = mid - 1;
            else start = mid + 1;
        } else {
            if (target > nums[mid] && target <= nums[end]) start = mid + 1;
            else end = mid - 1;
        }
    }
    return -1;
}
```
**Why it fails:** Using `<` instead of `<=` fails for an array of size 2, e.g. `nums = [3, 1]`, `target = 1`.
When `start = 0, end = 1`, `mid = 0`.
`nums[start] < nums[mid]` evaluates `3 < 3` which is **False**!
It enters the `else` block, checking `target > nums[mid] && target <= nums[end]` $\to$ `1 > 3 && 1 <= 1` (False), setting `end = mid - 1 = -1`. The search terminates prematurely and returns `-1` instead of `1`!  
**Correction:** Must use `nums[start] <= nums[mid]`.

---

## Edge Cases

1. **Single Element Array ($N = 1$):** `nums = [1], target = 0` $\to$ Returns `-1`. `target = 1` $\to$ Returns `0`.
2. **Two Element Rotated Array ($N = 2$):** `nums = [3, 1], target = 1` $\to$ Handled correctly by `<=` condition.
3. **Unrotated Array ($k = 0$):** `nums = [1, 2, 3, 4, 5]` $\to$ Left half is always sorted; behaves identically to standard binary search.
4. **Target at Boundaries:** `target == nums[0]` or `target == nums[n-1]`. Boundary conditions `>=` and `<=` preserve correct target inclusion.

---

## Complexity Analysis

- **Time Complexity:** $O(\log_2 N)$ (Every iteration eliminates at least $\lfloor N/2 \rfloor$ elements).
- **Auxiliary Space Complexity:** $O(1)$ (Only scalar index pointers `start`, `end`, `mid`).

---

## Key Takeaways

1. **Half-Sorted Invariant:** At least one half of a rotated sorted array is always strictly sorted.
2. **Target Isolation:** Only test target membership against the half that is **guaranteed to be sorted**.
3. **Logarithmic Bound:** Maintains $O(\log N)$ time and $O(1)$ space for distinct elements.

---

## ⚡ 2-Minute Revision

```cpp
while (start <= end) {
    int mid = start + (end - start) / 2;
    if (nums[mid] == target) return mid;
    if (nums[start] <= nums[mid]) { // Left half sorted
        if (target >= nums[start] && target < nums[mid]) end = mid - 1;
        else start = mid + 1;
    } else { // Right half sorted
        if (target > nums[mid] && target <= nums[end]) start = mid + 1;
        else end = mid - 1;
    }
}
return -1;
```
- Condition: `nums[start] <= nums[mid]`.
- Always verify `<` vs `<=` to prevent 2-element off-by-one errors.
