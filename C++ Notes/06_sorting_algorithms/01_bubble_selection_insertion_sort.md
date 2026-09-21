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
