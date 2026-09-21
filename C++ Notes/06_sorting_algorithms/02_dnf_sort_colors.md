# Lecture 25: Sort an Array of 0s, 1s & 2s (DNF Algorithm — LeetCode 75)

> **One-Line Purpose:** Master Edsger Dijkstra's Dutch National Flag (DNF) 3-way partitioning algorithm to sort tri-value arrays in a single $O(N)$ pass with $O(1)$ space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #25  
> **Video ID:** `J48aGjfjYTI`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=J48aGjfjYTI)  
> **Duration:** 33:39  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The limitations of counting sort ($2$ passes) vs DNF ($1$ pass).
- The 4 logical invariant regions maintained by 3 pointers: `low`, `mid`, `high`.
- Why `mid` advances when swapping with `low` (`nums[mid] == 0`), but does **NOT** advance when swapping with `high` (`nums[mid] == 2`).
- How DNF generalizes to Quicksort 3-way partitioning (dealing with duplicate keys).

---

## 🔵 Lecture Content

### 1. Invariant Regions of DNF

The array is divided into 4 contiguous zones at any point during iteration:
```text
[ 0 0 ... 0 | 1 1 ... 1 | ? ? ... ? | 2 2 ... 2 ]
  0       low-1   low   mid-1   mid   high  high+1     n-1
```
1. `arr[0 ... low - 1]` contains exclusively `0`s.
2. `arr[low ... mid - 1]` contains exclusively `1`s.
3. `arr[mid ... high]` contains **unknown / unsorted** elements (`?`).
4. `arr[high + 1 ... n - 1]` contains exclusively `2`s.

The algorithm terminates when `mid > high`, meaning the unknown region has shrunk to zero size.

---

## 2. Pointer Movement Rules

Inspect `arr[mid]`:
- **Case 0 (`arr[mid] == 0`):**
  Swap `arr[low]` and `arr[mid]`.
  Advance both: `low++`, `mid++`.
  *(Since the element swapped from `arr[low]` is guaranteed to be a `1`, `mid` can safely advance).*
- **Case 1 (`arr[mid] == 1`):**
  Element is in its correct region. Just advance `mid++`.
- **Case 2 (`arr[mid] == 2`):**
  Swap `arr[mid]` and `arr[high]`.
  Decrement `high--`.
  *(CRITICAL: Do NOT increment `mid`! The element incoming from `arr[high]` was unknown and must be re-evaluated in the next step).*

---

## 3. Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    void sortColors(vector<int>& nums) {
        int low = 0;
        int mid = 0;
        int high = nums.size() - 1;

        while (mid <= high) {
            if (nums[mid] == 0) {
                swap(nums[low], nums[mid]);
                low++;
                mid++;
            } else if (nums[mid] == 1) {
                mid++;
            } else { // nums[mid] == 2
                swap(nums[mid], nums[high]);
                high--;
                // Note: mid is NOT incremented here
            }
        }
    }
};

int main() {
    Solution sol;
    vector<int> colors = {2, 0, 2, 1, 1, 0};
    sol.sortColors(colors);
    cout << "Sorted: ";
    for (int x : colors) cout << x << " "; // Output: 0 0 1 1 2 2
    cout << endl;
    return 0;
}
```

---

## 4. Complexity Analysis

- **Time Complexity:** $O(N)$ — Exactly $1$ pass through the array. Each operation advances `mid` or decrements `high`.
- **Space Complexity:** $O(1)$ — Modified strictly in-place.

---

## 🧠 Core Intuition — Why This Works
Imagine sorting three types of balls: Red (0), White (1), and Blue (2). We can throw all Reds to the left, all Blues to the right, and the Whites will naturally end up in the middle. The algorithm uses three pointers: `low` to track the boundary of 0s, `high` for 2s, and `mid` to explore the unknown elements. As `mid` traverses, it classifies the current element and swaps it to its correct territory, shrinking the unknown region until it vanishes.

## 🎯 Pattern Recognition — When to Use This
- **Trigger cues:** "Sort an array of 3 distinct values", "Partition array into three categories", "Sort colors", "Dutch National Flag".
- **Keywords:** $O(N)$ time, $1$ pass, in-place, $O(1)$ space.

## 📐 Algorithm Walk-Through
1. Initialize `low = 0`, `mid = 0`, `high = n - 1`.
2. Iterate while `mid <= high`:
   - If `arr[mid] == 0`: Swap `arr[low]` and `arr[mid]`, increment both `low` and `mid`.
   - If `arr[mid] == 1`: Leave it alone, increment `mid`.
   - If `arr[mid] == 2`: Swap `arr[mid]` and `arr[high]`, decrement `high` (do NOT increment `mid`).

## 🔍 Dry Run Trace
Array: `[2, 0, 2, 1, 1, 0]`
1. `mid=0, high=5, arr[0]=2` -> Swap with `high`. Array: `[0, 0, 2, 1, 1, 2]`. `high=4`.
2. `mid=0, high=4, arr[0]=0` -> Swap `low, mid`. `low=1, mid=1`.
3. `mid=1, high=4, arr[1]=0` -> Swap `low, mid`. `low=2, mid=2`.
4. `mid=2, high=4, arr[2]=2` -> Swap with `high`. Array: `[0, 0, 1, 1, 2, 2]`. `high=3`.
5. `mid=2, high=3, arr[2]=1` -> `mid++`. `mid=3`.
6. `mid=3, high=3, arr[3]=1` -> `mid++`. `mid=4`.
7. `mid > high`, terminate.

## ⚠️ Common Interview Mistakes
- **Incrementing `mid` when swapping with `high`:** The element swapped from `high` could be a 0 or a 2. It must be evaluated, so `mid` must NOT be incremented.
- **Using `mid < high` instead of `mid <= high`:** The element at `high` is unknown and needs to be evaluated when `mid == high`.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Why not just use Counting Sort (Count 0s, 1s, 2s)?
**Answer:** Counting Sort requires two passes and overwrites elements. If array elements are objects (e.g., `{color: 0, id: 5}`), overwriting loses the `id`. DNF uses swaps, preserving object references, and runs in exactly one pass.

### Q2: What if we have 4 colors instead of 3?
**Answer:** DNF handles exactly 3 partitions. For 4 colors, we would need a 4-way partitioning scheme (often requiring an extra pass or additional pointers, complicating the invariant).

### Q3: Is DNF a stable sorting algorithm?
**Answer:** No. Swapping elements across long distances (like swapping `arr[mid]` and `arr[high]`) breaks the relative order of identical elements.

### Q4: How does this relate to Quicksort?
**Answer:** DNF is exactly the 3-way partitioning scheme used in modern Quicksort to efficiently handle arrays with many duplicate elements, placing all elements equal to the pivot in the middle.

### Q5: Can this be used to segregate even and odd numbers?
**Answer:** Yes, a simplified 2-way version of this (just `low` and `high` pointers) can segregate evens/odds, positives/negatives, or 0s/1s.

## 🏆 Related Problems (Leetcode)
- **LeetCode 75:** Sort Colors (The direct implementation)
- **LeetCode 283:** Move Zeroes (2-way partitioning)
- **LeetCode 324:** Wiggle Sort II (Uses 3-way partitioning under the hood)

## 🔗 Cross-Topic Connections
- **Quicksort:** This algorithm is fundamental to 3-way Quicksort.
- **Two Pointers:** An advanced variation of the two-pointer technique (using three).

## ⚡ 2-Minute Revision Flash Card
- **Problem:** Sort 0s, 1s, and 2s in one pass.
- **Algorithm:** Dutch National Flag (3 pointers: `low`, `mid`, `high`).
- **Rule 0:** Swap `low`, `mid`, increment both.
- **Rule 1:** Increment `mid`.
- **Rule 2:** Swap `mid`, `high`, decrement `high` (do NOT increment `mid`).
- **Condition:** `while (mid <= high)`.
