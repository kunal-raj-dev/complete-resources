# Lecture 53: Quick Sort Algorithm: Partitioning, Pivot Selection & Worst-Case Avoidance

> **One-Line Purpose:** Master the in-place Divide-and-Conquer sorting paradigm via Lomuto Partitioning, analyze pivot selection strategies, and eliminate $O(N^2)$ worst-case degradation using randomized pivots.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #53  
> **Video ID:** `8MNB0Mba_Dc`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=8MNB0Mba_Dc)  
> **Duration:** 26:23  
> **Transcript:** `.transcripts/12_recursion_and_backtracking/053_Quick_Sort_Algorithm_-_Lecture_51_of_Complete_DSA_Placement_Series.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The core philosophy of Quick Sort: **Pivot Selection & Partitioning**.
- How the Partition algorithm places the pivot element into its **exact final sorted position** in $O(N)$ time.
- The step-by-step mechanics of **Lomuto Partitioning** using two pointers (`i` and `j`).
- Why Quick Sort achieves $O(N \log N)$ average time with $O(1)$ auxiliary heap space.
- What causes the $O(N^2)$ worst-case scenario (already sorted inputs with boundary pivot) and how **Randomized Pivot Selection** avoids it.

---

## 🔵 Lecture Context

Quick Sort is the default sorting algorithm used in standard libraries (like C++ `std::sort`, which uses Introsort—a hybrid of Quick Sort, Heap Sort, and Insertion Sort). Its exceptional cache locality makes it the fastest practical sorting algorithm for in-memory arrays.

---

## 1. The Core Idea: Partitioning

Unlike Merge Sort (which divides first and does all the work during merging), Quick Sort **does the heavy lifting first** during Partitioning:
1. Choose an element as the **Pivot** (e.g. `arr[end]`).
2. Rearrange the array such that:
   - All elements $\le \text{pivot}$ are moved to the left of the pivot.
   - All elements $> \text{pivot}$ are moved to the right of the pivot.
3. The pivot is now at its **permanent sorted index** `pIdx`!
4. Recursively sort `[start ... pIdx - 1]` and `[pIdx + 1 ... end]`.

---

## 2. Lomuto Partitioning Algorithm

- Set `pivot = arr[end]`.
- Maintain pointer `i = start - 1` (tracks boundary of elements $\le \text{pivot}$).
- Iterate `j` from `start` to `end - 1`:
  - If `arr[j] <= pivot`: Increment `i`, then `swap(arr[i], arr[j])`.
- Finally, place the pivot: `swap(arr[i + 1], arr[end])`.
- Return pivot index `i + 1`.

---

## 3. Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <cstdlib>
using namespace std;

// Lomuto Partition Scheme
int partition(vector<int>& arr, int start, int end) {
    int pivot = arr[end];
    int i = start - 1; // Boundary for elements <= pivot

    for (int j = start; j < end; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }

    // Place pivot at its final sorted position
    swap(arr[i + 1], arr[end]);
    return i + 1;
}

void quickSort(vector<int>& arr, int start, int end) {
    // Base Case: 0 or 1 element
    if (start >= end) {
        return;
    }

    // Partition array around pivot
    int pIdx = partition(arr, start, end);

    // Recursively sort left and right partitions
    quickSort(arr, start, pIdx - 1);
    quickSort(arr, pIdx + 1, end);
}

int main() {
    vector<int> arr = {6, 3, 9, 5, 2, 8};
    quickSort(arr, 0, arr.size() - 1);

    cout << "Sorted Array: ";
    for (int x : arr) cout << x << " ";
    cout << "\n";
    return 0;
}
```

---

## 🔍 Detailed Trace: Partitioning `[6, 3, 9, 5, 2, 8]`

Pivot = `8`. Initial `i = -1`.
- `j = 0` (val 6): $6 \le 8 \to i=0$, Swap `arr[0]` with `arr[0]`. `[6, 3, 9, 5, 2, 8]`
- `j = 1` (val 3): $3 \le 8 \to i=1$, Swap `arr[1]` with `arr[1]`. `[6, 3, 9, 5, 2, 8]`
- `j = 2` (val 9): $9 > 8 \to$ do nothing.
- `j = 3` (val 5): $5 \le 8 \to i=2$, Swap `arr[2]` (9) with `arr[3]` (5). `[6, 3, 5, 9, 2, 8]`
- `j = 4` (val 2): $2 \le 8 \to i=3$, Swap `arr[3]` (9) with `arr[4]` (2). `[6, 3, 5, 2, 9, 8]`
- End of loop. Place pivot: Swap `arr[i+1]` (9) with `arr[end]` (8).
- Array state: `[6, 3, 5, 2, 8, 9]`. Pivot `8` is at index `4`!

---

## 🧠 Mental Model: Bouncer at the Door

Think of the pivot as a height requirement at an amusement park. The bouncer sweeps through the line. Anyone shorter than the requirement is shoved to the left; anyone taller is pushed to the right. Finally, the bouncer stands right between the two groups.

---

## ⚠️ Common Mistakes

1. **Worst-Case on Sorted Arrays:** If the array is already sorted `[1, 2, 3, 4, 5]` and the last element is picked as pivot, the partitions are sized $N-1$ and $0$. The recurrence degrades to $T(N) = T(N-1) + O(N) \implies O(N^2)$!
2. **Assuming Stability:** Quick Sort is **UNSTABLE**. Swapping distant elements across the pivot disrupts the relative order of duplicate keys.

---

## 🖥️ System-Specific Notes

- **Randomized Quick Sort:** To avoid $O(N^2)$ worst-case on sorted inputs:
  ```cpp
  int randomIdx = start + rand() % (end - start + 1);
  swap(arr[randomIdx], arr[end]);
  // Now proceed with standard partition
  ```
- **Introsort in C++ STL:** `std::sort` starts with Quick Sort. If recursion depth exceeds $2 \log_2 N$, it automatically switches to Heap Sort to guarantee $O(N \log N)$ worst-case time.

---

## 🟡 Additional Essential Context

Quickselect (Hoare's Selection Algorithm) uses the same partitioning logic to find the **K-th Smallest / Largest Element** (LeetCode 215) in average $O(N)$ time by recursing into only *one* partition instead of both.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** What is the auxiliary space complexity of Quick Sort?  
**A:** $O(1)$ heap memory, but $O(\log N)$ average call stack memory ($O(N)$ worst-case stack depth).

---

### 🔥 Interview Questions

#### Q1: What is the difference between Lomuto Partitioning and Hoare Partitioning?
- **Short Answer:** Hoare's scheme uses two pointers converging from both ends and does roughly three times fewer swaps on average than Lomuto's scheme.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
// arr = [1, 2, 3, 4] with pivot = arr[end]
// Comparisons in partition: 3 + 2 + 1 = 6 -> O(N^2)
```

---

## Complexity Analysis

| Case | Time Complexity | Auxiliary Space Complexity |
|---|---|---|
| Best Case | $O(N \log N)$ | $O(\log N)$ (Stack) |
| Average Case | $O(N \log N)$ | $O(\log N)$ (Stack) |
| Worst Case | $O(N^2)$ | $O(N)$ (Degenerate tree) |

---

## Key Takeaways

1. **In-place sorting:** Re-arranges array elements without allocating temporary vectors.
2. **Pivot guarantees:** Once partitioned, the pivot element never moves again.
3. **Randomized pivot:** Shields against $O(N^2)$ worst-case attacks on pre-sorted inputs.

---

## 🎯 Pattern Recognition — When to Use This
- **Trigger Cues:** "Sort an array in $O(1)$ space", "Sort primitve types natively", "Find the K-th largest element in $O(N)$ average time".
- **Why Quick Sort?** It is the standard `std::sort` mechanism (usually as Introsort). You apply Quick Sort algorithms directly when solving selection problems (Quickselect) or when partitioning arrays around a value (Dutch National Flag problem).

## 🏆 Related Problems (Leetcode)
- **Leetcode 215. Kth Largest Element in an Array:** Solved in average $O(N)$ time using Quickselect (a modification of Quick Sort's partitioning).
- **Leetcode 75. Sort Colors:** Dutch National Flag problem, which extends Quick Sort partitioning to 3 regions ($<, ==, >$).
- **Leetcode 912. Sort an Array:** A classic test of writing a robust sorting algorithm that won't TLE on adversarial inputs (requires Randomized Quick Sort or Merge Sort).

## 🔗 Cross-Topic Connections
- **Arrays & Two Pointers:** The partitioning logic is entirely two-pointer based.
- **Binary Search Trees (BST):** The recursion tree of Quick Sort behaves identically to the construction of a BST. If you insert elements into a BST in a random order, the shape of the tree matches the Quick Sort recursion tree.

### 🔥 Additional Interview Q&A
#### Q2: What is the worst-case scenario for Quick Sort and how do we mitigate it?
- **Answer:** The worst-case is $O(N^2)$, which occurs when the array is already sorted (or reverse sorted) and the pivot is chosen as the last (or first) element. This causes partitions of size 1 and $N-1$, leading to $N$ levels of recursion. We mitigate this by choosing a **Random Pivot** or the **Median of Three** (first, middle, last), ensuring balanced partitions on average.

#### Q3: What is "Introsort"?
- **Answer:** Introsort is a hybrid sorting algorithm used in `std::sort`. It begins with Quick Sort for speed, but if the recursion depth exceeds $2 \log_2 N$ (indicating pathological inputs pushing towards $O(N^2)$), it switches to **Heap Sort** to guarantee $O(N \log N)$ worst-case time. It also uses Insertion Sort for small subarrays.

#### Q4: Why is Quick Sort generally faster than Merge Sort for in-memory arrays despite both being $O(N \log N)$?
- **Answer:** Quick Sort operates in-place, which provides superior **cache locality**. Merge Sort allocates and writes to a temporary buffer array, resulting in constant cache misses and memory allocation overhead. Quick Sort's inner loop (the partition step) is exceptionally tight and hardware-friendly.

#### Q5: Is Quick Sort Stable?
- **Answer:** No, standard Quick Sort is **not stable**. The swapping during the partition step can jump elements past identical keys, disrupting their original relative order. If stability is required, Merge Sort is the go-to.

## ⚡ 2-Minute Revision Flash Card

- Lomuto partition: `if (arr[j] <= pivot) { i++; swap(arr[i], arr[j]); }`.
- Place pivot: `swap(arr[i + 1], arr[end])`.
- Average: $O(N \log N)$; Worst: $O(N^2)$ (sorted input).
- Space: $O(1)$ auxiliary + $O(\log N)$ stack.
