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

## 🔥 Interview Questions

### Q1: Why not just use Counting Sort (Count 0s, 1s, 2s)?
**Answer:** Counting Sort requires two passes (Pass 1: count frequencies, Pass 2: overwrite array) and is not an in-place element-swapping algorithm. If elements are rich objects (e.g., structs containing color and payload), overwriting loses object identity. DNF sorts strictly via element swaps in a single pass.
