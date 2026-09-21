# ⚡ Topic 06 Revision: Sorting Algorithms & Linear Partitions

> **High-Density Review:** Comparison matrix, stability, memory models, and partition invariants for placement interviews.

---

## 1. Algorithm Complexity Matrix

| Algorithm | Best Time | Average Time | Worst Time | Space | Stable? | Key Mechanism |
|---|---|---|---|---|---|---|
| **Bubble Sort** | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes | Adjacent swaps; early exit if no swaps |
| **Selection Sort** | $O(N^2)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | No | Find minimum and swap to prefix |
| **Insertion Sort** | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes | Shift elements to insert into sorted prefix |
| **Merge Sort** | $O(N \log N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | Yes | Divide & conquer; 2-way array merge |
| **Quick Sort** | $O(N \log N)$ | $O(N \log N)$ | $O(N^2)$ | $O(\log N)$ | No | Pivot partitioning (Lomuto / Hoare) |
| **DNF Sort** | $O(N)$ | $O(N)$ | $O(N)$ | $O(1)$ | No | 3-way partition using 3 pointers |

---

## 2. Dutch National Flag (DNF) 3-Way Partition Template
```cpp
void sortColors(vector<int>& nums) {
    int low = 0, mid = 0, high = nums.size() - 1;
    while (mid <= high) {
        if (nums[mid] == 0) {
            swap(nums[low++], nums[mid++]);
        } else if (nums[mid] == 1) {
            mid++;
        } else {
            swap(nums[mid], nums[high--]); // DO NOT increment mid! Swapped element from high is unexamined!
        }
    }
}
```

---

## 3. Next Permutation Algorithm (LeetCode 31)
1. Find longest non-increasing suffix from right: find first $i$ where `nums[i] < nums[i+1]`.
2. If no such $i$ exists, reverse entire array (was in descending order).
3. Find smallest element in suffix larger than `nums[i]`: index $j$ where `nums[j] > nums[i]`.
4. `swap(nums[i], nums[j])`.
5. Reverse suffix starting at $i + 1$.
