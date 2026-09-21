# Lecture 51: Merge Sort Algorithm: Divide & Conquer, Stability & Recurrence

> **One-Line Purpose:** Master the Divide-and-Conquer paradigm by recursively halving arrays and merging sorted subsequences in linear time, guaranteeing optimal $O(N \log N)$ time complexity and algorithm stability.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #51  
> **Video ID:** `cQDtOBTy7_Y`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=cQDtOBTy7_Y)  
> **Duration:** 32:04  
> **Transcript:** `.transcripts/12_recursion_and_backtracking/051_Merge_Sort_Algorithm___Recursion___Backtracking.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The 3-phase **Divide and Conquer** paradigm: Divide, Conquer, Combine.
- How Merge Sort divides an array of size $N$ into two subarrays of size $\approx N/2$ until base size $1$ is reached.
- The two-pointer linear merge procedure combining two sorted subarrays in $O(N)$ time.
- Why Merge Sort is a **Stable Sorting Algorithm** (preserves the original relative order of equivalent keys).
- The recurrence relation $T(N) = 2T(N/2) + O(N)$ and its Master Theorem proof yielding $O(N \log N)$ across Best, Average, and Worst cases.

---

## 🔵 Lecture Context

Merge Sort is the gold standard for comparison-based sorting with guaranteed $O(N \log N)$ performance. Its merging technique forms the basis for external sorting (sorting large datasets that do not fit in RAM), Linked List sorting, and the Count Inversions problem (Lecture 54).

---

## 1. The Divide-and-Conquer Mechanism

Merge Sort decomposes the sorting problem into three phases:
1. **Divide:** Find the midpoint index: $\text{mid} = \text{start} + (\text{end} - \text{start}) / 2$.
2. **Conquer:** Recursively sort the left half `[start ... mid]` and right half `[mid+1 ... end]`.
3. **Combine (Merge):** Merge the two sorted halves into a single sorted range using a temporary buffer.

```
                  [ 6, 3, 9, 5, 2, 8 ]
                     /            \
             [ 6, 3, 9 ]        [ 5, 2, 8 ]
              /       \          /       \
           [ 6 ]    [ 3, 9 ]   [ 5 ]    [ 2, 8 ]
                    /     \             /     \
                  [ 3 ]   [ 9 ]       [ 2 ]   [ 8 ]
------------------------------------------------------
Merge Step:
[ 3, 9 ] <--- Merge([3], [9])
[ 3, 6, 9 ] <--- Merge([6], [3, 9])
[ 2, 5, 8 ] <--- Merge([5], [2, 8])
[ 2, 3, 5, 6, 8, 9 ] <--- Merge([3, 6, 9], [2, 5, 8])
```

---

## 2. Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
using namespace std;

// Two-pointer merge procedure
void merge(vector<int>& arr, int start, int mid, int end) {
    vector<int> temp;
    int i = start;     // Pointer for left sorted half [start ... mid]
    int j = mid + 1;   // Pointer for right sorted half [mid+1 ... end]

    while (i <= mid && j <= end) {
        // Condition '<=' guarantees STABILITY!
        if (arr[i] <= arr[j]) {
            temp.push_back(arr[i++]);
        } else {
            temp.push_back(arr[j++]);
        }
    }

    // Copy any remaining elements from left half
    while (i <= mid) {
        temp.push_back(arr[i++]);
    }

    // Copy any remaining elements from right half
    while (j <= end) {
        temp.push_back(arr[j++]);
    }

    // Copy merged elements back into original array
    for (int k = 0; k < temp.size(); k++) {
        arr[start + k] = temp[k];
    }
}

void mergeSort(vector<int>& arr, int start, int end) {
    // Base Case: 0 or 1 element is already sorted
    if (start >= end) {
        return;
    }

    int mid = start + (end - start) / 2;

    // Sort left half
    mergeSort(arr, start, mid);

    // Sort right half
    mergeSort(arr, mid + 1, end);

    // Merge the two sorted halves
    merge(arr, start, mid, end);
}

int main() {
    vector<int> arr = {6, 3, 9, 5, 2, 8};
    mergeSort(arr, 0, arr.size() - 1);

    cout << "Sorted Array: ";
    for (int x : arr) cout << x << " ";
    cout << "\n";
    return 0;
}
```

---

## 🔍 Detailed Trace: Merging `[3, 6]` and `[2, 5]`

```
Left Half:  [3, 6] (i points to 3)
Right Half: [2, 5] (j points to 2)

Step 1: arr[j] (2) < arr[i] (3) -> temp = [2], j advances to 5
Step 2: arr[i] (3) < arr[j] (5) -> temp = [2, 3], i advances to 6
Step 3: arr[j] (5) < arr[i] (6) -> temp = [2, 3, 5], j exhausted
Step 4: Copy remaining left elements -> temp = [2, 3, 5, 6]
Merged Result: [2, 3, 5, 6]
```

---

## 🧠 Mental Model: Two Decks of Cards

Imagine two face-up decks of playing cards, each individually sorted. You compare the top cards of both decks, pick the smaller card, and place it into a new pile. When one deck runs out, you sweep the rest of the other deck onto the pile.

---

## ⚠️ Common Mistakes

1. **Destroying Stability:** Writing `if (arr[i] < arr[j])` instead of `if (arr[i] <= arr[j])`. When elements are equal, taking from the right half first alters the relative order of duplicate elements, making the sort **unstable**!
2. **Buffer Index Offset:** When copying back from `temp` to `arr`, writing `arr[k] = temp[k]` instead of `arr[start + k] = temp[k]`. This overwrites elements starting from index 0 instead of the sub-range `[start ... end]`.

---

## 🖥️ System-Specific Notes

- **Auxiliary Memory Allocation:** Allocating `vector<int> temp` inside `merge()` repeatedly incurs frequent heap allocations. In production and competitive programming, allocate a single auxiliary buffer of size $N$ once in the caller function and reuse it across all recursive calls.
- **Cache Performance:** While Merge Sort has guaranteed $O(N \log N)$ worst-case time, it is generally slower than Quick Sort for in-memory arrays because non-in-place merging generates extra memory copying and poor CPU cache locality.

---

## 🟡 Additional Essential Context

Merge Sort is the preferred sorting algorithm for **Linked Lists** because:
- Splitting a linked list takes $O(1)$ extra space using fast/slow pointers.
- Merging two sorted linked lists takes $O(1)$ extra space by pointer rewiring (no auxiliary array needed!).

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** What is an Algorithm's "Stability"?  
**A:** A sorting algorithm is stable if two objects with equal keys appear in the same order in sorted output as they appeared in the input array. For example, sorting students by grade while preserving their alphabetical submission order.

**Q2:** Solve the Merge Sort Recurrence Relation: $T(N) = 2T(N/2) + O(N)$.  
**A:** By Master Theorem ($a = 2, b = 2, f(n) = n^1$): $\log_b a = \log_2 2 = 1$. Since $f(n) = \Theta(n^{\log_b a})$, Case 2 applies: $T(N) = \Theta(N \log N)$.

---

### 🔥 Interview Questions

#### Q1: Why is Quick Sort preferred over Merge Sort for arrays, but Merge Sort preferred for Linked Lists?
- **Short Answer:** Quick Sort sorts arrays in-place with excellent CPU cache locality; Merge Sort requires $O(N)$ extra memory for arrays but $O(1)$ extra memory for linked lists.
- **Detailed Explanation:** Arrays provide $O(1)$ random access, making Quick Sort's partitioning cache-friendly. Linked lists cannot be indexed in $O(1)$, but can be merged in-place by updating `next` pointers without allocating buffer arrays.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
// arr = [5, 4, 3, 2, 1]
// Time complexity: O(N log N)
// Number of levels in recursion tree: ceil(log2(5)) = 3 levels
```

---

## Edge Cases

1. **Already Sorted Array:** Still takes $O(N \log N)$ time (Merge Sort has no early-exit optimization unless explicitly added).
2. **Array of Identical Elements:** Preserves relative order cleanly.

---

## Complexity Analysis

| Case | Time Complexity | Auxiliary Space Complexity |
|---|---|---|
| Best Case | $O(N \log N)$ | $O(N)$ (Temporary buffer) |
| Average Case | $O(N \log N)$ | $O(N)$ |
| Worst Case | $O(N \log N)$ | $O(N)$ |

---

## Key Takeaways

1. **Divide and Conquer:** Halve $\to$ Sort recursively $\to$ Merge linearly.
2. **Stability Invariant:** Use `<=` in merge comparison.
3. **Guaranteed $O(N \log N)$:** Immune to pathological inputs that cause Quick Sort to degrade.

---

## ⚡ 2-Minute Revision

- Recurrence: $T(N) = 2T(N/2) + O(N) \implies O(N \log N)$.
- Stable: Yes (`arr[i] <= arr[j]`).
- Space: $O(N)$ auxiliary array + $O(\log N)$ stack frames.
