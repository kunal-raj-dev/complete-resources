# Lecture 19: Peak Index in a Mountain Array (LeetCode 852)

> **One-Line Purpose:** Master Binary Search on non-monotonic arrays using slope gradient analysis to locate the peak element in $O(\log N)$ time and $O(1)$ space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #19  
> **Video ID:** `RjxD6UXGlhc`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=RjxD6UXGlhc)  
> **Duration:** 23:34  
> **Transcript:** `.transcripts/05_binary_search/019_Peak_Index_in_Mountain_Array___Binary_Search___Leetcode_852.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The formal mathematical definition of a Mountain Array (strictly increasing up to peak, strictly decreasing thereafter).
- Why Binary Search is applicable to non-sorted arrays as long as a directional gradient exists.
- How to classify any midpoint into one of three regions: Increasing Slope, Decreasing Slope, or Peak Element.
- Boundary initialization optimization (`start = 1, end = n - 2`) avoiding out-of-bounds neighbor checks.
- Generalization to LeetCode 162 (Find Peak Element in an arbitrary unsorted array).

---

## 🔵 Lecture Context

This lecture dismantles the myth that Binary Search requires a completely sorted array. It teaches you to analyze **derivative slopes** (local gradients), setting the stage for Binary Search on monotonic mathematical functions and optimization answer spaces (Lectures 21-23: Book Allocation, Painter's Partition, Aggressive Cows).

---

## 1. Mountain Array Structure

A **Mountain Array** (or Bitonic Array) has length $N \ge 3$ such that:
$$arr[0] < arr[1] < \dots < arr[i - 1] < \mathbf{arr[i]} > arr[i + 1] > \dots > arr[N - 1]$$

```
             Peak (arr[i])
                 /\
                /  \
  Increasing   /    \  Decreasing
    Slope     /      \    Slope
             /        \
            /          \
```

---

## 2. Slope Gradient Classification

For any arbitrary index `mid`:

```
1. Peak Element:
      arr[mid - 1] < arr[mid] > arr[mid + 1]
      -> FOUND PEAK! Return mid.

2. Increasing Slope (Uphill):
      arr[mid - 1] < arr[mid] < arr[mid + 1]
      -> Peak lies strictly to the RIGHT!
      -> start = mid + 1.

3. Decreasing Slope (Downhill):
      arr[mid - 1] > arr[mid] > arr[mid + 1]
      -> Peak lies strictly to the LEFT!
      -> end = mid - 1.
```

---

## 3. C++ Implementation with Boundary Optimization

Because a mountain array guarantees the peak cannot be at the boundary (`0` or $N-1$), we can safely restrict `start = 1` and `end = n - 2`. This guarantees that `mid - 1` and `mid + 1` never cause out-of-bounds indexing!

```cpp
#include <vector>
#include <iostream>
using namespace std;

int peakIndexInMountainArray(const vector<int>& arr) {
    int start = 1;
    int end = arr.size() - 2; // Safe from boundary overflows

    while (start <= end) {
        int mid = start + (end - start) / 2;

        // Condition 1: Peak element found
        if (arr[mid] > arr[mid - 1] && arr[mid] > arr[mid + 1]) {
            return mid;
        }
        // Condition 2: On the increasing slope -> go right
        else if (arr[mid] > arr[mid - 1]) {
            start = mid + 1;
        }
        // Condition 3: On the decreasing slope -> go left
        else {
            end = mid - 1;
        }
    }

    return -1; // Unreachable in valid mountain array
}

int main() {
    vector<int> mountain = {0, 3, 8, 15, 12, 6, 2};
    cout << "Peak index: " << peakIndexInMountainArray(mountain) << endl; // Prints 3 (value 15)
    return 0;
}
```

- **Time Complexity:** $O(\log_2 N)$
- **Space Complexity:** $O(1)$

---

## 🔍 Detailed Trace

Input: `arr = [0, 3, 8, 15, 12, 6, 2]` ($N = 7$)
- Initial: `start = 1` (val 3), `end = 5` (val 6)

| Iteration | `start` | `end` | `mid` | `arr[mid-1]` | `arr[mid]` | `arr[mid+1]` | Slope Region | Next Action |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 5 | 3 | 8 | **15** | 12 | `8 < 15 > 12` | **PEAK FOUND!** Return 3 |

Terminates in a single step!

---

## 🔥 Interview Questions

### Q1: [LeetCode 162] How does this approach generalize to find *any* peak in an arbitrary unsorted array where multiple peaks exist?
- **Short Answer:** The exact same binary search works!
- **Detailed Explanation:** In LeetCode 162, `nums[-1] = nums[n] = -\infty`. If `nums[mid] < nums[mid + 1]`, there is guaranteed to be at least one peak in the right half (even if elements keep rising until the boundary). Thus, following the increasing slope direction is always guaranteed to find a local maximum in $O(\log N)$ time.

---

## Key Takeaways

1. **Binary Search Beyond Sorted Arrays:** Can be applied whenever a local condition (gradient) deterministically rules out half the search space.
2. **Boundary Safety:** Setting `start = 1, end = n - 2` eliminates edge checks for `mid - 1` and `mid + 1`.
3. **Logarithmic Runtime:** Finds peak in $\approx \log_2 N$ operations.

---

## ⚡ 2-Minute Revision

- Peak: `arr[mid - 1] < arr[mid] > arr[mid + 1]`.
- Uphill (`arr[mid] > arr[mid - 1]`): `start = mid + 1`.
- Downhill (`arr[mid] < arr[mid - 1]`): `end = mid - 1`.
- Complexity: $O(\log N)$ Time, $O(1)$ Space.
