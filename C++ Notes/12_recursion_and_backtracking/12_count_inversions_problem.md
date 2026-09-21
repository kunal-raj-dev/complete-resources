# Lecture 54: Count Inversions Problem: Enhanced Merge Sort (Divide & Conquer)

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

## 🎯 Pattern Recognition — When to Use This
- **Trigger Cues:** "Find how far the array is from being sorted", "Count pairs $(i, j)$ such that $i < j$ and $A[i] > A[j]$", "Determine the number of swaps needed in Bubble Sort".
- **Why Merge Sort?** A brute force nested loop takes $O(N^2)$ time. The Divide-and-Conquer strategy of Merge Sort naturally processes elements in sorted relative order. When merging, if an element from the right half is smaller than an element from the left half, it is smaller than *all remaining elements* in the left half, allowing us to count inversions in $O(1)$ math rather than counting them one by one.

## 🏆 Related Problems (Leetcode)
- **Leetcode 315. Count of Smaller Numbers After Self:** You must track the actual count of smaller elements to the right for *each specific index*. Solved by augmenting Merge Sort with original index tracking.
- **Leetcode 493. Reverse Pairs:** Count pairs where $i < j$ and $nums[i] > 2 \times nums[j]$. Requires doing the counting step *before* the merging step inside `mergeSort()`.
- **Leetcode 327. Count of Range Sum:** Count number of range sums that lie in `[lower, upper]`. Solved using Merge Sort on a prefix sum array.

## 🔗 Cross-Topic Connections
- **Divide and Conquer:** The ultimate application of modifying a standard sorting algorithm to solve a counting problem.
- **Advanced Data Structures (Fenwick Tree / Segment Tree):** Counting inversions can also be solved by mapping array values to their ranks and querying the number of already-inserted elements that are greater than the current element in a Fenwick Tree in $O(N \log N)$ time.

### 🔥 Additional Interview Q&A
#### Q2: What is the relationship between the number of inversions and Bubble Sort?
- **Answer:** The number of inversions in an array is exactly equal to the number of adjacent swaps required to sort the array using Bubble Sort. Each adjacent swap in Bubble Sort resolves exactly one inversion.

#### Q3: How do you handle duplicate elements when counting inversions?
- **Answer:** Duplicate elements (where $A[i] == A[j]$) are **not** considered inversions, since an inversion requires a strictly greater value ($A[i] > A[j]$). By maintaining the strict `<` or `<=` condition for left-half preference during merging, duplicates are placed without incrementing the inversion counter.

#### Q4: Why can't we use Quick Sort to count inversions in $O(N \log N)$ time?
- **Answer:** Quick Sort's partitioning step swaps elements over long distances, which simultaneously creates and destroys an unpredictable number of inversions in a single $O(1)$ swap. Merge Sort only shifts elements past each other linearly, which allows exact mathematical counting.

#### Q5: Can we count inversions in $O(N)$ time if the elements are within a small range (e.g., $1$ to $K$)?
- **Answer:** Yes, if $K$ is very small, we can use a frequency array. As we iterate through the array from left to right, we query the sum of frequencies of elements strictly greater than $A[i]$, then increment the frequency of $A[i]$. This takes $O(N \cdot K)$ time. If $K$ is large, we replace the frequency array with a Fenwick Tree, bringing it to $O(N \log N)$.

## ⚡ 2-Minute Revision Flash Card

- Condition: `if (arr[i] > arr[j]) invCount += (mid - i + 1);`.
- Complexity: $O(N \log N)$ Time, $O(N)$ Space.
- Counter type: `long long` (Critical to prevent overflow).
