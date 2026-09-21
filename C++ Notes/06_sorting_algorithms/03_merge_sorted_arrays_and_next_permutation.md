# Lecture 26: Merge Sorted Arrays (LeetCode 88) & Next Permutation (LeetCode 31)

> **One-Line Purpose:** Master reverse three-pointer in-place buffer filling and mathematical lexicographic ordering through pivot discovery and suffix inversion.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #26  
> **Video ID:** `-1cLK6PaLsQ`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=-1cLK6PaLsQ)  
> **Duration:** 43:49  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- **Merge Sorted Array:** Why filling from the front causes $O(N)$ element shifts, and how filling from the back (`m + n - 1`) achieves $O(1)$ space without extra memory.
- **Next Permutation:** The mathematical definition of lexicographical order.
- The 3-step canonical algorithm for Next Permutation:
  1. Locate the first decreasing element from the right (Pivot).
  2. Find the smallest element to the right of Pivot that is strictly greater than Pivot.
  3. Swap them and reverse the suffix to obtain the smallest lexicographical sequence.

---

## 🔵 Lecture Content

### 1. Merge Sorted Array (In-Place Backwards Fill)

Given `nums1` of size $m + n$ (with $m$ valid elements and $n$ trailing zeros) and `nums2` of size $n$, merge `nums2` into `nums1` in sorted order.

```cpp
#include <vector>
#include <algorithm>
#include <iostream>
using namespace std;

class SolutionMerge {
public:
    void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
        int p1 = m - 1;       // Pointer at end of nums1 valid elements
        int p2 = n - 1;       // Pointer at end of nums2
        int writeIdx = m + n - 1; // Write pointer at very end of buffer

        while (p1 >= 0 && p2 >= 0) {
            if (nums1[p1] > nums2[p2]) {
                nums1[writeIdx--] = nums1[p1--];
            } else {
                nums1[writeIdx--] = nums2[p2--];
            }
        }

        // If nums2 has remaining elements, flush them into nums1
        while (p2 >= 0) {
            nums1[writeIdx--] = nums2[p2--];
        }
        // (If p1 has remaining elements, they are already in their correct places)
    }
};
```
- **Time Complexity:** $O(m + n)$.
- **Space Complexity:** $O(1)$ auxiliary.

---

### 2. Next Permutation (Lexicographic Invariant)

```text
Example: [1, 2, 5, 4, 3]
Step 1: Scan from right to find pivot where nums[i] < nums[i+1].
        nums[1] (2) < nums[2] (5). Pivot = index 1 (value 2).
Step 2: Scan from right to find element strictly greater than nums[pivot].
        nums[4] is 3. Since 3 > 2, swap index 1 and index 4.
        Array becomes: [1, 3, 5, 4, 2]
Step 3: Reverse the suffix from pivot + 1 to end (index 2 to 4).
        Reverse [5, 4, 2] -> [2, 4, 5].
        Final Result: [1, 3, 2, 4, 5].
```

```cpp
class SolutionNextPermutation {
public:
    void nextPermutation(vector<int>& nums) {
        int n = nums.size();
        int pivot = -1;

        // Step 1: Find rightmost index i such that nums[i] < nums[i + 1]
        for (int i = n - 2; i >= 0; i--) {
            if (nums[i] < nums[i + 1]) {
                pivot = i;
                break;
            }
        }

        // If no pivot exists, array is in descending order (highest permutation)
        if (pivot == -1) {
            reverse(nums.begin(), nums.end());
            return;
        }

        // Step 2: Find rightmost element strictly greater than nums[pivot]
        for (int i = n - 1; i > pivot; i--) {
            if (nums[i] > nums[pivot]) {
                swap(nums[pivot], nums[i]);
                break;
            }
        }

        // Step 3: Reverse the descending suffix to make it ascending (minimal)
        reverse(nums.begin() + pivot + 1, nums.end());
    }
};
```

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$ — Scanning for pivot ($O(N)$), scanning for successor ($O(N)$), and reversing suffix ($O(N)$).
- **Space Complexity:** $O(1)$ auxiliary.

## 🧠 Core Intuition — Why This Works
**Merge Sorted Arrays:** If we start merging from the front of `nums1`, we would overwrite its existing elements before we can evaluate them. By starting from the back (where there is empty space), we safely write the largest elements first without overwriting any valid un-processed data.
**Next Permutation:** A sequence in descending order cannot be made any larger (it is the last permutation). So, to find the *next* permutation, we must find the first element from the right that breaks this descending order (the pivot). By swapping it with the smallest element larger than it in the suffix, and then reversing the suffix (which sorts it), we get the next lexicographical sequence.

## 🎯 Pattern Recognition — When to Use This
- **Trigger cues for Next Permutation:** "Find the next lexicographically greater arrangement", "Generate permutations".
- **Trigger cues for Merge Sorted:** "Merge in-place", "Two sorted arrays into one with extra space at the end".
- **Keywords:** 3-pointer backwards traversal, Suffix inversion.

## 🔍 Dry Run Trace (Merge Sorted Arrays)
`nums1 = [1,2,3,0,0,0]`, `m=3`, `nums2 = [2,5,6]`, `n=3`
- `p1=2 (val=3), p2=2 (val=6), writeIdx=5`
- `6 > 3` -> `nums1[5] = 6`, `p2--`, `writeIdx--`
- `p1=2 (val=3), p2=1 (val=5), writeIdx=4`
- `5 > 3` -> `nums1[4] = 5`, `p2--`, `writeIdx--`
- `p1=2 (val=3), p2=0 (val=2), writeIdx=3`
- `3 > 2` -> `nums1[3] = 3`, `p1--`, `writeIdx--`
- `p1=1 (val=2), p2=0 (val=2), writeIdx=2`
- `2 == 2` -> `nums1[2] = 2`, `p2--`, `writeIdx--`
- `p2 < 0`, loop ends. Result: `[1,2,2,3,5,6]`.

## ⚠️ Common Interview Mistakes
- **Merge Arrays:** Trying to merge from the front, leading to $O(N^2)$ shifting or $O(N)$ extra space usage.
- **Next Permutation:** Forgetting to handle the edge case where the entire array is descending (e.g., `[3, 2, 1]`). In this case, there is no pivot, and the answer is the reverse of the array (`[1, 2, 3]`).

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Why do we reverse the suffix in Next Permutation instead of sorting it?
**Answer:** The suffix is guaranteed to be in strictly descending order by the way we found the pivot. Reversing a descending array is an $O(N)$ operation that results in an ascending array (which is the same as sorting it, but much faster than $O(N \log N)$).

### Q2: What if `nums2` is empty in Merge Sorted Arrays?
**Answer:** `n` will be 0, `p2` will be -1, and the main loop will never execute. `nums1` is already in its correct state, so the algorithm perfectly handles this edge case in $O(1)$ time.

### Q3: How do you handle duplicates in Next Permutation?
**Answer:** The algorithm naturally handles duplicates because we strictly look for `nums[i] < nums[i+1]` and swap with an element *strictly greater* than the pivot. Reversing the suffix still properly sorts identical elements.

### Q4: Can Merge Sorted Arrays be done in $O(1)$ space if `nums1` didn't have padding?
**Answer:** If `nums1` didn't have padding, we would have to either allocate a new array of size $M+N$ ($O(M+N)$ space) or use a complex algorithm like Gap Method (Shell Sort intuition) to do it in-place in $O((M+N) \log(M+N))$ time.

### Q5: What is the C++ STL equivalent for these?
**Answer:** For Next Permutation, C++ provides `std::next_permutation(nums.begin(), nums.end())`. For Merge, `std::merge` exists but requires a separate destination iterator.

## 🏆 Related Problems (Leetcode)
- **LeetCode 46:** Permutations (Generate all using backtracking)
- **LeetCode 977:** Squares of a Sorted Array (Similar two-pointer backward fill)
- **LeetCode 556:** Next Greater Element III (Applies next permutation on digits of a number)

## 🔗 Cross-Topic Connections
- **Two Pointers:** Merge Sorted Array is a classic backward two-pointer problem.
- **Math/Combinatorics:** Next Permutation is the fundamental algorithm for lexicographical generation.

## ⚡ 2-Minute Revision Flash Card
- **Merge Arrays:** Use 3 pointers. `p1` at end of valid `nums1`, `p2` at end of `nums2`, `writeIdx` at end of `nums1` buffer. Compare and fill backwards.
- **Next Permutation Step 1:** Find pivot `i` from right where `nums[i] < nums[i+1]`.
- **Next Permutation Step 2:** Find `j` from right where `nums[j] > nums[i]`. Swap them.
- **Next Permutation Step 3:** Reverse everything after `i`. (If no pivot, reverse entire array).
