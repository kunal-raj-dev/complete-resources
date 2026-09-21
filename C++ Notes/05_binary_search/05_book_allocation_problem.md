# Lecture 21: Book Allocation Problem: Binary Search on Answer Space

> **One-Line Purpose:** Master the "Binary Search on Answer" paradigm by minimizing the maximum number of pages allocated to $M$ students under contiguous distribution constraints.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #21  
> **Video ID:** `JRAByolWqhw`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=JRAByolWqhw)  
> **Duration:** 32:59  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The formulation of "Binary Search on Answer Space" vs searching on an input array.
- The 4 core rules of Book Allocation:
  1. Each book must be allocated to exactly one student.
  2. Each student must be allocated at least one book.
  3. Books must be allocated in **contiguous order**.
  4. Minimize the maximum pages allocated to any single student.
- Defining the search space boundaries: $\text{low} = \max(\text{arr})$, $\text{high} = \sum \text{arr}$.
- Formulating the greedy feasibility predicate `isValid(maxPages)`.

---

## 🔵 Lecture Context

Book Allocation is the prototype problem for a major interview archetype: **Minimizing the Maximum (or Maximizing the Minimum)**. The exact same pattern solves Painter's Partition (Lecture 22), Aggressive Cows (Lecture 23), Capacity To Ship Packages Within D Days (LeetCode 1011), and Split Array Largest Sum (LeetCode 410).

---

## 1. Problem Statement

Given an array `arr` of $N$ integers where `arr[i]` denotes the number of pages in the $i$-th book, and an integer $M$ representing the number of students. Allocate all books to $M$ students such that:
1. Each book is assigned to contiguous students.
2. The maximum number of pages assigned to a student is minimized.
If allocation is impossible ($M > N$), return `-1`.

```text
Example:
arr = [25, 46, 28, 49, 24], M = 2
Possibilities of 2 contiguous partitions:
1. [25] | [46, 28, 49, 24] -> Max = 147
2. [25, 46] | [28, 49, 24] -> Max = 101
3. [25, 46, 28] | [49, 24] -> Max = 99
4. [25, 46, 28, 49] | [24] -> Max = 148

Minimum of Maximums = 99 (Partition: [25, 46, 28] and [49, 24]).
```

---

## 2. Defining the Monotonic Search Space

Notice the monotonicity of the predicate:
- If it is possible to allocate books such that no student receives $> K$ pages, then it is **also possible** for any limit $> K$.
- If it is **impossible** for $K$, it is also impossible for any limit $< K$.

Therefore, the feasibility function is monotonic: `[False, False, ..., False, True, True, True]`. We can binary search for the first `True`!

### Search Range:
- $\text{low} = \max(\text{arr})$: No student can receive fewer pages than the largest single book.
- $\text{high} = \sum \text{arr}$: If 1 student gets all books, they receive all pages.

---

## 3. Feasibility Predicate: `isValid(maxPagesAllowed)`

Greedy check:
1. Initialize `studentCount = 1`, `currentPageSum = 0`.
2. For each book `pages` in `arr`:
   - If `currentPageSum + pages <= maxPagesAllowed`, add `pages` to current student.
   - Else, allocate to next student: `studentCount++`, `currentPageSum = pages`.
   - If `studentCount > M`, return `false`.
3. Return `true`.

---

## 4. Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

class Solution {
private:
    bool isValid(const vector<int>& arr, int n, int m, int maxPagesAllowed) {
        int students = 1;
        int currentPages = 0;

        for (int i = 0; i < n; i++) {
            if (arr[i] > maxPagesAllowed) return false;

            if (currentPages + arr[i] <= maxPagesAllowed) {
                currentPages += arr[i];
            } else {
                students++;
                currentPages = arr[i];
                if (students > m) {
                    return false;
                }
            }
        }
        return true;
    }

public:
    int allocateBooks(const vector<int>& arr, int n, int m) {
        if (m > n) return -1; // Impossible to allocate at least 1 book per student

        int low = *max_element(arr.begin(), arr.end());
        int high = accumulate(arr.begin(), arr.end(), 0);
        int ans = -1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (isValid(arr, n, m, mid)) {
                ans = mid;         // Feasible, try to find a smaller maximum
                high = mid - 1;
            } else {
                low = mid + 1;     // Infeasible, must increase allowed pages
            }
        }
        return ans;
    }
};

int main() {
    Solution sol;
    vector<int> books = {25, 46, 28, 49, 24};
    int m = 2;
    cout << "Minimum Maximum Pages: " << sol.allocateBooks(books, books.size(), m) << endl; // Output: 99
    return 0;
}
```

---

## 5. Complexity Analysis

- **Time Complexity:** $O(N \times \log(\sum \text{pages} - \max(\text{pages})))$ — In each step of binary search over the page range, we do an $O(N)$ linear pass.
- **Space Complexity:** $O(1)$ — Only primitive counters.

---

## 🔥 Interview Questions

### Q1: Why must the search space start at $\max(\text{arr})$ instead of $1$?
- **Answer:** If the upper bound were less than $\max(\text{arr})$, that individual book could never be assigned to any student because a single book cannot be split. Setting $\text{low} = \max(\text{arr})$ establishes a physically valid lower bound.
