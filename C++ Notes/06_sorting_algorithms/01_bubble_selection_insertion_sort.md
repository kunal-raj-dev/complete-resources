# Lecture 24: Sorting Algorithms: Bubble, Selection & Insertion Sort

> **One-Line Purpose:** Master foundational $O(N^2)$ quadratic sorting algorithms, their internal loop invariants, stability, adaptive optimizations, and in-place memory characteristics.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #24  
> **Video ID:** `1jCFUv-Xlqo`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=1jCFUv-Xlqo)  
> **Duration:** 34:33  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The distinction between **Comparison-based** and **Non-comparison-based** sorts.
- **Bubble Sort:** Repeatedly swap adjacent inverted elements to "bubble" the maximum to the right; optimize to $O(N)$ with a swapped flag.
- **Selection Sort:** Find the global minimum in the unsorted suffix and swap it with the front; understand why it is fundamentally unstable.
- **Insertion Sort:** Progressively insert elements into an already sorted prefix; understand why it is adaptive and ideal for nearly-sorted data.
- The precise definitions of **In-Place** ($O(1)$ space) and **Stability** (preservation of relative order of equal keys).

---

## 🔵 Lecture Content

### 1. Bubble Sort: Mechanics & Optimization

At each pass $i$ ($0 \le i < n - 1$), adjacent elements `arr[j]` and `arr[j+1]` are compared. If `arr[j] > arr[j+1]`, they are swapped.
After pass $i$, the largest remaining element is placed in its permanent position `n - 1 - i`.

```text
Pass 0: [4, 1, 5, 2, 3] -> [1, 4, 2, 3, 5]  (5 settled at index 4)
Pass 1: [1, 4, 2, 3, 5] -> [1, 2, 3, 4, 5]  (4 settled at index 3)
```

#### Optimized C++ Implementation
```cpp
#include <vector>
#include <iostream>
using namespace std;

void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        bool isSwapped = false;
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
                isSwapped = true;
            }
        }
        // Adaptive check: If no elements were swapped, array is already sorted
        if (!isSwapped) break;
    }
}
```
- **Time Complexity:** Best $O(N)$ (already sorted), Average/Worst $O(N^2)$.
- **Space Complexity:** $O(1)$ auxiliary.
- **Stability:** Stable (strictly `>` prevents swapping identical elements).

---

### 2. Selection Sort: Minimum Selection

Divide the array into sorted prefix and unsorted suffix.
In pass $i$, find the index of the minimum element in `arr[i...n-1]`, then swap it with `arr[i]`.

```cpp
void selectionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIdx]) {
                minIdx = j;
            }
        }
        if (minIdx != i) {
            swap(arr[i], arr[minIdx]);
        }
    }
}
```
- **Time Complexity:** Best, Average, Worst: Strictly $O(N^2)$ (always performs $N(N-1)/2$ comparisons).
- **Space Complexity:** $O(1)$.
- **Stability:** Unstable (e.g. `[4a, 4b, 1]` -> `1` swaps with `4a`, placing `4a` after `4b`).
- **Advantage:** Minimizes the total number of memory write operations (strictly at most $N - 1$ swaps).

---

### 3. Insertion Sort: Card Player's Algorithm

Maintain sorted subarray `arr[0...i-1]`. Pick `current = arr[i]` and shift all elements in the sorted prefix that are greater than `current` one position right. Insert `current` into the created vacancy.

```cpp
void insertionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 1; i < n; i++) {
        int current = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > current) {
            arr[j + 1] = arr[j]; // Shift right
            j--;
        }
        arr[j + 1] = current;    // Insert in correct spot
    }
}
```
- **Time Complexity:** Best $O(N)$ (already sorted), Worst $O(N^2)$ (reverse sorted).
- **Space Complexity:** $O(1)$.
- **Stability:** Stable.
- **Advantage:** Highly efficient for small arrays ($N \le 30$) and nearly-sorted arrays. (Used in hybrid algorithms like Timsort and `std::sort` introsort).

---

## 4. Comprehensive Comparison Table

| Algorithm | Best Time | Avg Time | Worst Time | Auxiliary Space | Stable? | Swaps (Worst) |
|---|---|---|---|---|---|---|
| **Bubble Sort** | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes | $O(N^2)$ |
| **Selection Sort** | $O(N^2)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | No | $O(N)$ |
| **Insertion Sort** | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes | $O(N^2)$ (shifts) |

---

## 🔥 Interview Questions

### Q1: Why is Selection Sort preferred when memory writes are extremely expensive?
**Answer:** While Bubble and Insertion Sort may execute up to $O(N^2)$ write operations, Selection Sort makes at most $N - 1$ writes (swaps) across its entire execution. In systems with flash memory or EEPROM where writes wear down the hardware, Selection Sort's minimal write count is advantageous.


## 🧠 Core Intuition — Why This Works
- **Bubble Sort:** Like bubbles rising to the surface, the largest element is pushed to the rightmost sorted section with each pass.
- **Selection Sort:** Scanning the remaining unsorted elements to select the absolute minimum, placing it at the front of the unsorted section.
- **Insertion Sort:** Like arranging cards in your hand, you pick up one card at a time and insert it into its correct position among the already sorted cards.

## 🎯 Pattern Recognition — When to Use This
- **Trigger cues:** "Sort an array that is almost sorted", "Sort an array with very limited memory writes".
- **Keywords:** Stable sort, in-place sort, adaptive sort.
- **Selection Sort:** When memory writes are costly.
- **Insertion Sort:** When data is nearly sorted or very small ($N \le 30$).

## 📐 Algorithm Walk-Through
1. **Bubble Sort:** Loop $i$ from 0 to $N-1$. Loop $j$ from 0 to $N-1-i$. If $A[j] > A[j+1]$, swap. If no swaps in inner loop, break.
2. **Selection Sort:** Loop $i$ from 0 to $N-1$. Find minimum in $A[i...N-1]$. Swap with $A[i]$.
3. **Insertion Sort:** Loop $i$ from 1 to $N-1$. Store `curr = A[i]`. Shift elements $A[j]$ greater than `curr` to the right. Insert `curr`.

## 🔍 Dry Run Trace
**Insertion Sort on `[4, 3, 2, 10, 12, 1, 5, 6]` (Trace first 3 steps):**
- **Init:** Sorted part `[4]`. `i = 1`, `curr = 3`.
- **Step 1:** `4 > 3`, shift `4` right. Array: `[4, 4, ...]`. Insert `3`. Array: `[3, 4, 2, 10, 12, 1, 5, 6]`.
- **Step 2:** `i = 2`, `curr = 2`. `4 > 2` (shift), `3 > 2` (shift). Array: `[2, 3, 4, 10, 12, 1, 5, 6]`.
- **Step 3:** `i = 3`, `curr = 10`. `4 < 10`, no shift. Array remains `[2, 3, 4, 10, 12, 1, 5, 6]`.

## ⚠️ Common Interview Mistakes
- **Confusing Bubble and Selection Sort:** Bubble sort swaps adjacent elements constantly; Selection sort swaps exactly once per pass.
- **Stability of Selection Sort:** Thinking Selection Sort is stable. It is NOT, because long-distance swaps can reorder equal elements.
- **Off-by-one errors:** Forgetting to do $N-1-i$ in Bubble sort's inner loop, resulting in out-of-bounds or redundant comparisons.

## 🔥 Interview Q&A — Google / Amazon Level
### Q2: Why is Insertion Sort used in modern sorting libraries like `std::sort`?
**Answer:** `std::sort` typically uses Introsort (QuickSort + HeapSort + InsertionSort). When the recursion depth makes the subarray size very small (e.g., 16 elements), Insertion Sort is much faster due to low overhead and excellent cache locality.
### Q3: How can we make Bubble Sort Adaptive?
**Answer:** By adding a boolean `swapped` flag. If a full pass occurs without any swaps, the array is sorted, and we can terminate early, achieving $O(N)$ best-case time.

## 🏆 Related Problems (Leetcode)
- **LeetCode 912:** Sort an Array (Requires faster sorts, but good to test $O(N^2)$ TLE)
- **LeetCode 147:** Insertion Sort List (Implementing Insertion Sort on a Linked List)
- **LeetCode 75:** Sort Colors (DNF, related to linear sorting concepts)

## 🔗 Cross-Topic Connections
- **Linked Lists:** Insertion sort is naturally suited for linked lists because elements can be inserted without shifting arrays.
- **Divide and Conquer:** These fundamental sorts are base cases for Merge Sort and Quick Sort.

## ⚡ 2-Minute Revision Flash Card
- **Bubble:** Swap adjacent, max bubbles to right. $O(N^2)$ time. Stable. Adaptive.
- **Selection:** Find min, swap with front. $O(N^2)$ time. Unstable. Min writes.
- **Insertion:** Insert into sorted prefix. $O(N^2)$ time. Stable. Best for nearly sorted/small data.
