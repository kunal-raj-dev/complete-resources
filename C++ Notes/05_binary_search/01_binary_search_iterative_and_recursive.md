# Lecture 17: Binary Search Algorithm (Iterative & Recursive)

> **One-Line Purpose:** Master the search space halving principle, overflow-safe midpoint calculation, iterative vs recursive implementations, and mathematical complexity derivation for Binary Search.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #17  
> **Video ID:** `TbbSJrY5GqQ`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=TbbSJrY5GqQ)  
> **Duration:** 44:16  
> **Transcript:** `.transcripts/05_binary_search/017_Binary_Search_Algorithm_-_Iterative_and_Recursive_Method____Theory___Code__with_.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The fundamental prerequisite for Binary Search: **Monotonicity (Sorted Order)**.
- The search space halving intuition reducing time from $O(N)$ to $O(\log_2 N)$.
- The critical integer overflow bug with `(start + end) / 2` and the canonical fix.
- Iterative ($O(1)$ space) versus Recursive ($O(\log N)$ stack space) implementations.
- Mathematical derivation of logarithmic complexity via recurrence relations.

---

## 🔵 Lecture Context

Binary Search is one of the most powerful algorithms in computer science. While simple in concept, research shows that over 80% of professional software engineers make off-by-one errors or overflow bugs when implementing it from scratch. In technical interviews, Binary Search extends far beyond simple arrays into "Binary Search on Answer Spaces" (Lectures 21-23).

---

## 1. The Core Halving Intuition

> 🔵 **Lecture Content**

In a **sorted array**, comparing the target against the middle element gives absolute directional information:
```
Target = 18
Array: [ 2 | 4 | 7 | 10 | 14 | 18 | 21 | 25 | 30 ]
                         ▲
                        mid = 14

Since 14 < 18, and array is sorted, 18 CANNOT exist in [2, 4, 7, 10, 14]!
ELIMINATE THE ENTIRE LEFT HALF IN O(1) TIME!
Search space shrinks from 9 elements to 4 elements instantly.
```

---

## 2. Midpoint Calculation & The Overflow Bug

```cpp
int mid = (start + end) / 2; // BUGGY IN PRODUCTION!
```
- **Why it fails:** If `start` and `end` are large positive integers close to $2^{31}-1$ (e.g. `start = 2 * 10^9`, `end = 2 * 10^9`), their sum `start + end = 4 * 10^9`, which exceeds the maximum signed 32-bit integer capacity ($2.14 \times 10^9$). It overflows into a negative number, resulting in a negative index and immediate segmentation fault.
- **The Safe Formula:**
  $$\text{mid} = \text{start} + \frac{\text{end} - \text{start}}{2}$$
  Because `end - start` is non-negative and strictly smaller than `end`, no intermediate overflow can ever occur.

---

## 3. Iterative Implementation (Optimal $O(1)$ Space)

```cpp
#include <vector>
#include <iostream>
using namespace std;

int binarySearchIterative(const vector<int>& nums, int target) {
    int start = 0;
    int end = nums.size() - 1;

    while (start <= end) {
        int mid = start + (end - start) / 2;

        if (nums[mid] == target) {
            return mid; // Target found
        } else if (nums[mid] < target) {
            start = mid + 1; // Target lies in right half
        } else {
            end = mid - 1;   // Target lies in left half
        }
    }
    return -1; // Target does not exist
}
```

- **Time Complexity:** Best Case $O(1)$, Worst Case $O(\log_2 N)$.
- **Auxiliary Space:** $O(1)$ constant memory.

---

## 4. Recursive Implementation ($O(\log N)$ Space)

```cpp
int binarySearchRecursive(const vector<int>& nums, int target, int start, int end) {
    if (start > end) {
        return -1; // Base Case: Search space exhausted
    }

    int mid = start + (end - start) / 2;

    if (nums[mid] == target) {
        return mid;
    } else if (nums[mid] < target) {
        return binarySearchRecursive(nums, target, mid + 1, end);
    } else {
        return binarySearchRecursive(nums, target, start, mid - 1);
    }
}
```

- **Time Complexity:** $O(\log_2 N)$.
- **Auxiliary Space:** $O(\log_2 N)$ due to the recursive Call Stack activation records.

---

## 5. Mathematical Complexity Derivation

Let $N$ be the number of elements:
- Iteration 1: $\frac{N}{2^1}$ elements remaining.
- Iteration 2: $\frac{N}{2^2}$ elements remaining.
- $\dots$
- Iteration $k$: $\frac{N}{2^k}$ elements remaining.

The search terminates when the search space reduces to 1 element:
$$\frac{N}{2^k} = 1 \implies 2^k = N \implies k = \log_2 N$$
Thus, the maximum number of loop iterations is strictly $\lceil \log_2 N \rceil$.

### Linear Search vs Binary Search Comparison:
For $N = 1,000,000,000$ ($10^9$ elements):
- Linear Search ($O(N)$): Up to $10^9$ operations ($\approx 10$ seconds).
- Binary Search ($O(\log N)$): At most $\approx 30$ comparisons ($\approx 0.000001$ seconds)!

---

## ⚠️ Common Mistakes

1. **Loop Condition (`<` vs `<=`):** Writing `while (start < end)` fails to inspect the single remaining element when `start == end`. Always use `while (start <= end)`.
2. **Updating `mid` without `+1` / `-1`:** Writing `start = mid` or `end = mid` can cause an **Infinite Loop** when `start` and `end` differ by 1. Always use `start = mid + 1` and `end = mid - 1`.

---

## 🔥 Interview Questions

### Q1: [Lower Bound vs Upper Bound] What is `std::lower_bound` and `std::upper_bound`?
- **Lower Bound:** Returns an iterator pointing to the first element that is $\ge \text{target}$.
- **Upper Bound:** Returns an iterator pointing to the first element that is $> \text{target}$.
- Both execute in $O(\log N)$ time on random-access iterators.

---

## Key Takeaways

1. **Prerequisite:** Array must be sorted (monotonic).
2. **Safe Mid:** `mid = start + (end - start) / 2`.
3. **Loop Boundary:** `start <= end` ensures all valid elements are inspected.
4. **Efficiency:** Reduces $10^9$ operations down to just 30 comparisons.

---

## ⚡ 2-Minute Revision

- While condition: `start <= end`.
- If `nums[mid] < target`: `start = mid + 1`.
- If `nums[mid] > target`: `end = mid - 1`.
- Time: $O(\log N)$. Space: Iterative $O(1)$, Recursive $O(\log N)$.
