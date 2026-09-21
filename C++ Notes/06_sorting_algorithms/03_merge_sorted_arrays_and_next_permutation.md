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
