import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t12_dir = os.path.join(root, "12_recursion_and_backtracking")

notes = {}

# 10: Merge Sort Algorithm
notes["10_merge_sort_algorithm.md"] = r"""# Lecture 51: Merge Sort Algorithm: Divide & Conquer, Stability & Recurrence

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
"""

# 11: Quick Sort Algorithm
notes["11_quick_sort_algorithm.md"] = r"""# Lecture 53: Quick Sort Algorithm: Partitioning, Pivot Selection & Worst-Case Avoidance

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

## ⚡ 2-Minute Revision

- Lomuto partition: `if (arr[j] <= pivot) { i++; swap(arr[i], arr[j]); }`.
- Place pivot: `swap(arr[i + 1], arr[end])`.
- Average: $O(N \log N)$; Worst: $O(N^2)$ (sorted input).
"""

# 12: Count Inversions Problem
notes["12_count_inversions_problem.md"] = r"""# Lecture 54: Count Inversions Problem: Enhanced Merge Sort (Divide & Conquer)

> **One-Line Purpose:** Master the enhanced Merge Sort technique to count inverted pairs in $O(N \log N)$ time by exploiting the sorted property of subarrays during the merge phase.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #54  
> **Video ID:** `ynnWDBTdVi0`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=ynnWDBTdVi0)  
> **Duration:** 24:33  
> **Transcript:** `.transcripts/12_recursion_and_backtracking/054_Count_Inversions_Problem___Brute_and_Optimal.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The formal definition of an **Inversion**: a pair of indices $(i, j)$ such that $i < j$ and $arr[i] > arr[j]$.
- Why inversion count measures how far an array is from being sorted (0 for sorted; $N(N-1)/2$ for reverse sorted).
- The Brute Force approach ($O(N^2)$ time via nested loops).
- The Optimal Approach ($O(N \log N)$ time) using modified Merge Sort.
- The mathematical deduction: if $arr[i] > arr[j]$ during merge, then all remaining elements in the left sorted half (`mid - i + 1`) form inversions with $arr[j]$.

---

## 🔵 Lecture Context

Counting inversions is a classic Divide-and-Conquer problem. It is used in ranking systems (collaborative filtering), measuring dataset entropy, and is the algorithmic sibling to LeetCode 315 (Count of Smaller Numbers After Self).

---

## 1. Problem Statement

Given an integer array `arr`, return the **number of inversions**.
An inversion occurs when two elements are out of sorted order:
$$i < j \quad \text{and} \quad arr[i] > arr[j]$$

```
Input: arr = [6, 3, 5, 2, 7]
Inversions:
- (6, 3), (6, 5), (6, 2)  [3 pairs]
- (3, 2)                  [1 pair]
- (5, 2)                  [1 pair]
Total Inversions = 5
```

---

## 2. Algorithmic Insight: Inversion Math During Merge

Consider two sorted halves being merged:
- Left Half: `[3, 5, 6]` (`start` to `mid`)
- Right Half: `[1, 2]` (`mid + 1` to `end`)

Suppose pointer `i` points to `3` and pointer `j` points to `1`.
Notice that `arr[i] > arr[j]` ($3 > 1$).
Because the left half is **already sorted**, every element from index `i` to `mid` ($3, 5, 6$) is guaranteed to be strictly greater than $arr[j]$ ($1$)!
Therefore, all remaining elements in the left half form valid inversions with $arr[j]$:
$$\text{Inversions added} = (\text{mid} - i + 1)$$

We count these inversions in $O(1)$ time, skipping individual element checks!

---

## 3. Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
using namespace std;

long long mergeAndCount(vector<int>& arr, int start, int mid, int end) {
    vector<int> temp;
    int i = start;
    int j = mid + 1;
    long long invCount = 0;

    while (i <= mid && j <= end) {
        if (arr[i] <= arr[j]) {
            temp.push_back(arr[i++]);
        } else {
            // arr[i] > arr[j]: Inversion detected!
            // All elements from i to mid are > arr[j]
            invCount += (mid - i + 1);
            temp.push_back(arr[j++]);
        }
    }

    while (i <= mid) temp.push_back(arr[i++]);
    while (j <= end) temp.push_back(arr[j++]);

    for (int k = 0; k < temp.size(); k++) {
        arr[start + k] = temp[k];
    }

    return invCount;
}

long long mergeSortAndCount(vector<int>& arr, int start, int end) {
    long long invCount = 0;
    if (start < end) {
        int mid = start + (end - start) / 2;

        // Inversions in left half
        invCount += mergeSortAndCount(arr, start, mid);

        // Inversions in right half
        invCount += mergeSortAndCount(arr, mid + 1, end);

        // Split inversions across both halves
        invCount += mergeAndCount(arr, start, mid, end);
    }
    return invCount;
}

int main() {
    vector<int> arr = {6, 3, 5, 2, 7};
    long long total = mergeSortAndCount(arr, 0, arr.size() - 1);
    cout << "Total Inversions: " << total << "\n"; // Output: 5
    return 0;
}
```

---

## 🔍 Detailed Trace: Merging `[3, 5]` and `[2, 4]`

`mid = 1`, `i = 0` (val 3), `j = 2` (val 2).
- `arr[i] > arr[j]` ($3 > 2$):
  - Inversions added: `mid - i + 1` $= 1 - 0 + 1 = 2$ (Pairs: $(3, 2)$ and $(5, 2)$).
  - `temp` takes `2`, `j` advances to index 3 (val 4).
- Next comparison: `arr[i] < arr[j]` ($3 < 4$):
  - `temp` takes `3`, `i` advances to index 1 (val 5).
- Next comparison: `arr[i] > arr[j]` ($5 > 4$):
  - Inversions added: `mid - i + 1` $= 1 - 1 + 1 = 1$ (Pair: $(5, 4)$).
  - `temp` takes `4`, `j` exhausted.
- Copy remaining `5`. Total inversions = $2 + 1 = 3$.

---

## 🧠 Mental Model: Overtaking on a Highway

Imagine cars on a two-lane highway. Every time a car in the right lane merges ahead of cars in the left lane, it has "overtaken" all cars currently waiting behind in that left lane. The number of cars waiting is `mid - i + 1`.

---

## ⚠️ Common Mistakes

1. **Integer Overflow on Inversion Count:** For an array of size $10^5$ sorted in reverse, total inversions $= \frac{10^5 \times 10^5}{2} \approx 5 \times 10^9$. This exceeds signed 32-bit `int` ($\approx 2 \times 10^9$). Always use `long long` for inversion counters!
2. **Writing `<` instead of `<=`:** Writing `if (arr[i] < arr[j])` incorrectly flags equal elements as inversions. An inversion strictly requires $arr[i] > arr[j]$.

---

## 🖥️ System-Specific Notes

- In competitive programming platforms, `long long` is 64-bit on both Windows and Linux, preventing arithmetic overflow for counts up to $9 \times 10^{18}$.

---

## 🟡 Additional Essential Context

Inversions can also be counted in $O(N \log N)$ time using a **Fenwick Tree (Binary Indexed Tree)** or a **Segment Tree** by mapping elements to coordinate ranks and querying prefix sums.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** What does an inversion count of $0$ mean? What does an inversion count of $\frac{N(N-1)}{2}$ mean?  
**A:** $0$ inversions means the array is already sorted in ascending order. $\frac{N(N-1)}{2}$ means the array is strictly in reverse descending order (every pair is inverted).

---

### 🔥 Interview Questions

#### Q1: Can we count inversions without modifying the original array?
- **Short Answer:** Yes, by passing a copy of the array to `mergeSortAndCount()`.
- **Detailed Explanation:** Merge Sort reorders elements in-place. If the original order must be preserved, duplicate the array first.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
// arr = [1, 2, 3, 4]
// Output: 0 (Already sorted)

// arr = [4, 3, 2, 1]
// Output: 4 * 3 / 2 = 6 inversions
```

---

## Complexity Analysis

- **Time Complexity:** $O(N \log N)$ (Exact same recurrence as Merge Sort: $T(N) = 2T(N/2) + O(N)$).
- **Auxiliary Space Complexity:** $O(N)$ for temporary merge buffer.

---

## Key Takeaways

1. **Inversion Counting Math:** When `arr[i] > arr[j]`, add `mid - i + 1`.
2. **Return Type:** Always use `long long` to prevent 32-bit integer overflow.
3. **Preserve Merge Sort Structure:** Operates in identical $O(N \log N)$ time to standard Merge Sort.

---

## ⚡ 2-Minute Revision

- Condition: `if (arr[i] > arr[j]) invCount += (mid - i + 1);`.
- Complexity: $O(N \log N)$ Time, $O(N)$ Space.
- Counter type: `long long`.
"""

# 13: Knight's Tour Problem
notes["13_knights_tour_problem.md"] = r"""# Lecture 55: Knight's Tour Problem: Board Traversal Backtracking (LeetCode 2596)

> **One-Line Purpose:** Master constrained 2D grid path finding by visiting all $N^2$ squares of a chessboard exactly once using the Knight's L-shaped moves and Warnsdorff's heuristic.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #55  
> **Video ID:** `Sp1jzttFVdE`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=Sp1jzttFVdE)  
> **Duration:** 22:32  
> **Transcript:** `.transcripts/12_recursion_and_backtracking/055_KNIGHTS_TOUR_Problem_-_Backtracking___Leetcode_2596.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The rules of the Knight's Tour: visiting all $N \times N$ cells of a chessboard with a knight, landing on each square exactly once.
- The 8 legal L-shaped moves of a knight in 2D coordinate space.
- The distinction between verifying an existing tour (LeetCode 2596: $O(N^2)$ simulation) versus generating a tour from scratch (Backtracking: $O(8^{N^2})$).
- Warnsdorff's Heuristic: choosing the move that has the minimum number of onward legal moves.

---

## 🔵 Lecture Context

The Knight's Tour is a historical mathematical puzzle (Euler, 1759) and a premier computer science demonstration of Hamiltonian paths on graphs and state-space pruning.

---

## 1. Problem Statement & Knight Mechanics

A Knight moves in an "L-shape": two squares along one axis and one square along the perpendicular axis.
From cell `(r, c)`, there are at most 8 possible moves:
1. `(r + 2, c + 1)`
2. `(r + 2, c - 1)`
3. `(r - 2, c + 1)`
4. `(r - 2, c - 1)`
5. `(r + 1, c + 2)`
6. `(r + 1, c - 2)`
7. `(r - 1, c + 2)`
8. `(r - 1, c - 2)`

**Goal:** Fill an $N \times N$ board with step numbers $0, 1, 2, \dots, N^2 - 1$ such that each step represents a valid knight jump from the preceding step.

---

## 2. Complete C++ Implementation (Backtracking Generator)

```cpp
#include <iostream>
#include <vector>
using namespace std;

// 8 legal knight move offsets
const int dRow[8] = {-2, -2, -1, -1,  1,  1,  2,  2};
const int dCol[8] = {-1,  1, -2,  2, -2,  2, -1,  1};

bool isValidMove(int r, int c, int n, const vector<vector<int>>& board) {
    return (r >= 0 && r < n && c >= 0 && c < n && board[r][c] == -1);
}

bool solveKnightTour(vector<vector<int>>& board, int r, int c, int step, int n) {
    // Base Case: All N*N squares visited!
    if (step == n * n) {
        return true;
    }

    // Try all 8 possible moves
    for (int i = 0; i < 8; i++) {
        int nextRow = r + dRow[i];
        int nextCol = c + dCol[i];

        if (isValidMove(nextRow, nextCol, n, board)) {
            board[nextRow][nextCol] = step; // Choose

            if (solveKnightTour(board, nextRow, nextCol, step + 1, n)) {
                return true; // Stop immediately upon finding complete tour
            }

            board[nextRow][nextCol] = -1; // Backtrack
        }
    }

    return false;
}

int main() {
    int n = 8;
    vector<vector<int>> board(n, vector<int>(n, -1));

    // Start at (0, 0) as step 0
    board[0][0] = 0;

    if (solveKnightTour(board, 0, 0, 1, n)) {
        cout << "Knight's Tour Found:\n";
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                cout << (board[i][j] < 10 ? " " : "") << board[i][j] << " ";
            }
            cout << "\n";
        }
    } else {
        cout << "No Knight's Tour exists.\n";
    }
    return 0;
}
```

---

## 3. LeetCode 2596: Check Knight Tour Configuration

In LeetCode 2596, we are given an existing board and must determine if it represents a valid tour starting from `grid[0][0] == 0`:

```cpp
class Solution {
public:
    bool checkValidGrid(vector<vector<int>>& grid) {
        if (grid[0][0] != 0) return false;
        int n = grid.size();

        // Map step number to (row, col) coordinates
        vector<pair<int, int>> pos(n * n);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                pos[grid[i][j]] = {i, j};
            }
        }

        // Verify that consecutive steps are valid L-moves
        for (int step = 1; step < n * n; step++) {
            int dr = abs(pos[step].first - pos[step - 1].first);
            int dc = abs(pos[step].second - pos[step - 1].second);

            if (!((dr == 1 && dc == 2) || (dr == 2 && dc == 1))) {
                return false;
            }
        }
        return true;
    }
};
```

---

## 🧠 Mental Model: Warnsdorff's Heuristic

Naive backtracking on an $8 \times 8$ board can take hours because it explores billions of dead-end paths.
**Warnsdorff's Rule:** Always move the knight to the neighbor cell that has the **fewest onward available moves**! This keeps the knight along the outer borders and corners first, preventing it from isolating open squares in corners later.

---

## ⚠️ Common Mistakes

1. **Not checking `grid[0][0] == 0`:** In LeetCode 2596, if the knight does not start at the top-left square, the grid is invalid by definition.
2. **Missing `board[r][c] == -1` check:** Visiting an already-stepped cell triggers infinite cyclic wandering.

---

## 🖥️ System-Specific Notes

- For an $8 \times 8$ board, pure brute force without heuristics has $8^{64}$ worst-case complexity. Warnsdorff's heuristic solves the $8 \times 8$ tour in under $5\text{ ms}$.

---

## 🟡 Additional Essential Context

The Knight's Tour problem is a specific instance of finding a **Hamiltonian Path** in a graph where vertices are board cells and edges are legal knight moves.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** What is an "Open Tour" vs a "Closed Tour"?  
**A:** In an Open Tour, the knight finishes on a square that does not attack the starting square. In a Closed (Re-entrant) Tour, the final square is exactly one knight move away from the starting square, forming a continuous cycle.

---

### 🔥 Interview Questions

#### Q1: What is the time complexity of verifying a Knight's Tour (LeetCode 2596)?
- **Short Answer:** $O(N^2)$ time and $O(N^2)$ space.
- **Detailed Explanation:** We map all $N^2$ numbers to coordinates in a single pass, then check the distance between adjacent numbers in $N^2 - 1$ steps.

---

## 💻 Output / Debugging Questions

### Output Prediction
Is `abs(r1 - r2) * abs(c1 - c2) == 2` a valid check for knight moves?  
**Answer:** Yes! The product of $\Delta r$ and $\Delta c$ must be $1 \times 2 = 2$ or $2 \times 1 = 2$. If either is $0$ or equal, the product cannot be $2$.

---

## Edge Cases

1. **Small Boards ($N \le 4$):** No knight's tour exists for $N = 2, 3, 4$ (except trivial $N=1$).
2. **$N = 5$:** The smallest odd board with a tour.

---

## Complexity Analysis

- **Verification (LeetCode 2596):** Time $O(N^2)$, Auxiliary Space $O(N^2)$.
- **Generation (Backtracking):** Time $O(8^{N^2})$, Auxiliary Space $O(N^2)$ board + $O(N^2)$ stack frames.

---

## Key Takeaways

1. **8 Moves:** Defined by $(\pm 1, \pm 2)$ and $(\pm 2, \pm 1)$.
2. **Warnsdorff's Rule:** Move to square with minimum onward degree.
3. **L-Move Invariant:** `(dr == 1 && dc == 2) || (dr == 2 && dc == 1)`.

---

## ⚡ 2-Minute Revision

- Base Case: `step == n * n`.
- 8 moves: `{-2, -2, -1, -1, 1, 1, 2, 2}` and `{-1, 1, -2, 2, -2, 2, -1, 1}`.
- Backtrack: reset `board[r][c] = -1`.
"""

print("Writing batch 4 notes...")
for fn, content in notes.items():
    with open(os.path.join(t12_dir, fn), "w", encoding="utf-8") as f:
        f.write(content)
print("Updated 10, 11, 12, 13.")
