import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t05_dir = os.path.join(root, "05_binary_search")

notes = {}

# Lecture 20: Single Element in a Sorted Array (LeetCode 540)
notes["04_single_element_in_sorted_array.md"] = r"""# Lecture 20: Single Element in a Sorted Array (LeetCode 540)

> **One-Line Purpose:** Master the Even-Odd Index Parity invariant in a sorted duplicate array to locate the unique single element in $O(\log N)$ time and $O(1)$ space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #20  
> **Video ID:** `qsbCBduIs40`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=qsbCBduIs40)  
> **Duration:** 27:33  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The structure of an array where every element appears exactly twice except for one single element.
- Why the total length of the array is always odd ($2k + 1$).
- The **Index Parity Property**:
  - Before the single element: Pairs start at an **even index** and end at an **odd index** (`(even, odd)`).
  - After the single element: The disruption shifts pairs to start at an **odd index** and end at an **even index** (`(odd, even)`).
- How to eliminate half of the search space using this parity transition point.
- Boundary condition handling (`mid == 0` and `mid == n - 1`).

---

## 🔵 Lecture Content

### 1. Problem Definition
Given a sorted array consisting of only integers where every element appears exactly twice, except for one element which appears exactly once. Find this single element that appears only once. Your solution must run in $O(\log N)$ time and $O(1)$ space.

```text
Example 1:
Index:   0  1  2  3  4  5  6  7  8
Array: [ 1, 1, 2, 3, 3, 4, 4, 8, 8 ]
Output: 2

Observation of Pairs:
(1, 1) -> Indices (0, 1) [even, odd]  <-- Before single element
Single: 2 at Index 2
(3, 3) -> Indices (3, 4) [odd, even]   <-- After single element
(4, 4) -> Indices (5, 6) [odd, even]
(8, 8) -> Indices (7, 8) [odd, even]
```

---

## 2. Mathematical Insight: The Parity Invariant

1. **Left of the Unique Element:**
   - For any pair `nums[i] == nums[i+1]`, `i` is **even**.
   - Equivalently, if `mid` is even, its partner is at `mid + 1`. If `mid` is odd, its partner is at `mid - 1`.
2. **Right of the Unique Element:**
   - The pattern is inverted: For any pair `nums[i] == nums[i+1]`, `i` is **odd**.
   - If `mid` is even, its partner is at `mid - 1`. If `mid` is odd, its partner is at `mid + 1`.
3. **At the Unique Element:**
   - Neither `nums[mid - 1]` nor `nums[mid + 1]` equals `nums[mid]`. This is the target!

---

## 3. Binary Search Algorithm Step-by-Step

1. Initialize `low = 0, high = n - 1`.
2. Edge cases:
   - If `n == 1`, return `nums[0]`.
   - If `nums[0] != nums[1]`, return `nums[0]`.
   - If `nums[n - 1] != nums[n - 2]`, return `nums[n - 1]`.
3. Search in the trimmed space `low = 1, high = n - 2`:
   - Compute `mid = low + (high - low) / 2`.
   - If `nums[mid] != nums[mid - 1]` and `nums[mid] != nums[mid + 1]`, return `nums[mid]`.
   - If `(mid % 2 == 1 && nums[mid] == nums[mid - 1]) || (mid % 2 == 0 && nums[mid] == nums[mid + 1])`:
     - We are in the left half! The single element lies to the right. Set `low = mid + 1`.
   - Else:
     - We are in the right half! The single element lies to the left. Set `high = mid - 1`.

---

## 4. Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int singleNonDuplicate(const vector<int>& nums) {
        int n = nums.size();
        
        // Base edge cases
        if (n == 1) return nums[0];
        if (nums[0] != nums[1]) return nums[0];
        if (nums[n - 1] != nums[n - 2]) return nums[n - 1];

        // Trimmed search space to avoid out-of-bounds checks for mid - 1 and mid + 1
        int low = 1, high = n - 2;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            // Target condition: unique element differs from both left and right neighbors
            if (nums[mid] != nums[mid - 1] && nums[mid] != nums[mid + 1]) {
                return nums[mid];
            }

            // Check if mid is in the left sorted segment:
            // Case A: mid is odd and matches previous element (even index)
            // Case B: mid is even and matches next element (odd index)
            if ((mid % 2 == 1 && nums[mid] == nums[mid - 1]) ||
                (mid % 2 == 0 && nums[mid] == nums[mid + 1])) {
                // Single element is to the right
                low = mid + 1;
            } else {
                // Single element is to the left
                high = mid - 1;
            }
        }

        return -1; // Unreachable for valid inputs
    }
};

int main() {
    Solution sol;
    vector<int> nums = {1, 1, 2, 3, 3, 4, 4, 8, 8};
    cout << "Single Element: " << sol.singleNonDuplicate(nums) << endl; // Output: 2
    return 0;
}
```

---

## 5. Complexity Analysis

- **Time Complexity:** $O(\log_2 N)$ — Search space halves at every step.
- **Space Complexity:** $O(1)$ — Only constant auxiliary variables (`low`, `high`, `mid`).

---

## ⚠️ Common Pitfalls

1. **Out of bounds access on `mid - 1` or `mid + 1`:** Handled cleanly by checking `0` and `n - 1` initially and bounding search to `[1, n - 2]`.
2. **XOR Index Trick Alternative:** Notice that if `mid` is even, `mid ^ 1 == mid + 1`. If `mid` is odd, `mid ^ 1 == mid - 1`. Thus, the condition simplifies to checking if `nums[mid] == nums[mid ^ 1]`.

---

## 🔥 Interview Questions

### Q1: Can this problem be solved with XOR in $O(N)$? Why do interviewers insist on Binary Search?
- **Answer:** XORing all elements yields the unique element in $O(N)$ time and $O(1)$ space. However, XOR ignores the **sorted order** precondition. An interviewer asks this problem specifically to test your ability to exploit monotonicity and index parity to achieve logarithmic time $O(\log N)$.

---

## Key Takeaways

1. **Parity Switch:** Pairs go from `(even, odd)` to `(odd, even)` across the unique element.
2. **Index Bitwise Trick:** `mid ^ 1` automatically maps `even -> even + 1` and `odd -> odd - 1`.
"""

# Lecture 21: Book Allocation Problem
notes["05_book_allocation_problem.md"] = r"""# Lecture 21: Book Allocation Problem: Binary Search on Answer Space

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
"""

# Lecture 22: Painter's Partition Problem
notes["06_painters_partition_problem.md"] = r"""# Lecture 22: Painter's Partition Problem: Minimizing Max Workload

> **One-Line Purpose:** Apply the Binary Search on Answer framework to partition continuous board segments among $K$ painters to minimize the overall completion time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #22  
> **Video ID:** `srsFN5OHBgw`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=srsFN5OHBgw)  
> **Duration:** 27:44  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The equivalence of the Painter's Partition Problem to the Book Allocation Problem and LeetCode 410 (Split Array Largest Sum).
- How the problem statement maps:
  - Books $\to$ Boards
  - Pages $\to$ Board lengths
  - Students $\to$ Painters
- How unit painting time ($T$) scales the answer mathematically: $\text{Total Time} = \text{Optimal Length} \times T$.
- The necessity of 64-bit integer types (`long long`) to prevent arithmetic overflow during sum calculations.

---

## 🔵 Lecture Context

The Painter's Partition Problem demonstrates an essential interview realization: **algorithmic isomorphism**. Problems that look completely different on the surface (allocating pages vs painting boards) share the exact same underlying mathematical structure and code template.

---

## 1. Problem Statement

Given $N$ boards with lengths `boards[0...N-1]` and $K$ painters. Each painter takes 1 unit of time to paint 1 unit length of a board. Any painter will only paint continuous sections of boards. A board can only be painted by 1 painter. Find the minimum time required to paint all boards under the constraint that all painters work simultaneously.

```text
Example:
boards = [10, 20, 30, 40], K = 2
Possible 2 partitions:
- [10] | [20, 30, 40] -> Max = 90
- [10, 20] | [30, 40] -> Max = 70
- [10, 20, 30] | [40] -> Max = 60 (Optimal)

Minimum time to finish = 60 units.
```

---

## 2. Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

class Solution {
private:
    bool isFeasible(const vector<int>& boards, int k, long long maxLimit) {
        int painters = 1;
        long long currentWork = 0;

        for (int length : boards) {
            if (length > maxLimit) return false;

            if (currentWork + length <= maxLimit) {
                currentWork += length;
            } else {
                painters++;
                currentWork = length;
                if (painters > k) return false;
            }
        }
        return true;
    }

public:
    long long paint(int k, int t, const vector<int>& boards) {
        int n = boards.size();
        long long low = *max_element(boards.begin(), boards.end());
        long long high = 0;
        for (int b : boards) high += b;

        long long optimalLength = high;

        while (low <= high) {
            long long mid = low + (high - low) / 2;

            if (isFeasible(boards, k, mid)) {
                optimalLength = mid;
                high = mid - 1; // Try minimizing further
            } else {
                low = mid + 1;  // Workload mid is too small, increase limit
            }
        }

        // Multiply by time per unit length t (using modulo 10000003 if asked in interview)
        return (optimalLength * t);
    }
};

int main() {
    Solution sol;
    vector<int> boards = {10, 20, 30, 40};
    int k = 2, t = 1;
    cout << "Minimum Painting Time: " << sol.paint(k, t, boards) << endl; // Output: 60
    return 0;
}
```

---

## 3. Complexity & Boundary Conditions

- **Time Complexity:** $O(N \log(\sum \text{boards}))$.
- **Space Complexity:** $O(1)$.
- **Edge Cases:** If $K \ge N$, every painter can paint 1 board; the answer is simply $\max(\text{boards}) \times t$.
"""

# Lecture 23: Aggressive Cows Problem
notes["07_aggressive_cows_problem.md"] = r"""# Lecture 23: Aggressive Cows Problem: Maximizing the Minimum Distance

> **One-Line Purpose:** Master the inverse optimization pattern — "Maximize the Minimum Distance" — placing $C$ aggressive cows into stalls using Binary Search on Answer Space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #23  
> **Video ID:** `7wOzDqsfXy0`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=7wOzDqsfXy0)  
> **Duration:** 30:12  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The distinction between **Minimizing the Maximum** (Book Allocation) and **Maximizing the Minimum** (Aggressive Cows).
- Why the stall coordinate array must be **sorted** first even if the input stalls are given out of order.
- The search space range:
  - $\text{low} = 1$ (minimum possible distance between any two stalls).
  - $\text{high} = \text{stalls}[N-1] - \text{stalls}[0]$ (maximum possible span).
- The Greedy placement strategy for cows: always place the first cow at `stalls[0]`, then place subsequent cows at the earliest stall with separation $\ge \text{mid}$.

---

## 🔵 Lecture Context

In Book Allocation and Painter's Partition, feasibility was true for large values and false for small values (`[F, F, ..., T, T]`). In Aggressive Cows, the monotonicity flips: it is trivial to place cows far apart when the required distance is very small, but impossible when the distance is too large (`[T, T, T, ..., F, F]`). We search for the **last `True`**!

---

## 1. Problem Statement

Farmer John has built a new long barn with $N$ stalls at positions $x_1, x_2, \dots, x_N$. He wants to place $C$ cows into the stalls such that the minimum distance between any two of them is as large as possible. Return the maximum possible minimum distance.

```text
Example:
stalls = [1, 2, 8, 4, 9], C = 3
1. Sort stalls: [1, 2, 4, 8, 9]
2. Try distance = 3:
   - Place Cow 1 at stall 1
   - Next stall >= 1 + 3 = 4 -> Place Cow 2 at stall 4
   - Next stall >= 4 + 3 = 7 -> Place Cow 3 at stall 8
   All 3 cows placed successfully! Distance 3 is feasible.
3. Try distance = 4:
   - Place Cow 1 at stall 1
   - Next stall >= 1 + 4 = 5 -> Place Cow 2 at stall 8
   - Next stall >= 8 + 4 = 12 -> No stall available for Cow 3!
   Distance 4 is NOT feasible.

Maximum minimum distance = 3.
```

---

## 2. Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
private:
    bool canPlaceCows(const vector<int>& stalls, int k, int dist) {
        int cowsPlaced = 1;
        int lastPos = stalls[0];

        for (size_t i = 1; i < stalls.size(); i++) {
            if (stalls[i] - lastPos >= dist) {
                cowsPlaced++;
                lastPos = stalls[i];
                if (cowsPlaced == k) return true;
            }
        }
        return false;
    }

public:
    int aggressiveCows(vector<int>& stalls, int k) {
        sort(stalls.begin(), stalls.end()); // Crucial: Stalls must be ordered

        int n = stalls.size();
        int low = 1;
        int high = stalls[n - 1] - stalls[0];
        int ans = 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (canPlaceCows(stalls, k, mid)) {
                ans = mid;        // Distance mid is feasible, try for an even larger distance
                low = mid + 1;
            } else {
                high = mid - 1;   // Distance mid is too large, reduce requirement
            }
        }

        return ans;
    }
};

int main() {
    Solution sol;
    vector<int> stalls = {1, 2, 8, 4, 9};
    int k = 3;
    cout << "Maximized Minimum Distance: " << sol.aggressiveCows(stalls, k) << endl; // Output: 3
    return 0;
}
```

---

## 3. Complexity Analysis

- **Sorting Time:** $O(N \log N)$.
- **Binary Search Time:** $O(N \times \log(\text{max\_stall} - \text{min\_stall}))$.
- **Total Time Complexity:** $O(N \log N + N \log(\Delta x))$.
- **Space Complexity:** $O(1)$ auxiliary space.

---

## 🔥 Interview Questions

### Q1: Why is greedy placement optimal in `canPlaceCows`?
- **Answer:** Placing the first cow as far left as possible (`stalls[0]`) leaves the maximum possible remaining track length for placing the remaining $C-1$ cows. Any alternative non-greedy choice restricts the remaining distance, strictly reducing feasibility.
"""

# Update 00_master_index.md in 05_binary_search
notes["00_master_index.md"] = r"""# Topic 05: Binary Search & Divide and Conquer — Master Index

> **Domain:** Logarithmic Search Space Halving, Monotonic Optimization, and Modified Binary Search Patterns

---

## 📋 Topic Overview

This module covers Binary Search from its foundational iterative and recursive formulations to advanced modified variants on non-monotonic, rotated structures, and binary search on answer spaces. Key concepts include overflow-safe midpoint calculations, the half-sorted invariant on rotated arrays, slope gradient analysis on bitonic mountain arrays, index parity tricks, and greedy predicate evaluation for allocation and spacing optimization ($O(\log N)$).

---

## 📑 Lecture Index

| # | Lecture Title | Focus Areas | Notes Link | Status |
|---|---|---|---|---|
| **17** | Binary Search Algorithm (Iterative & Recursive) | Halving intuition, overflow-safe `mid`, recurrence relation, iterative vs recursive | [01_binary_search_iterative_and_recursive.md](./01_binary_search_iterative_and_recursive.md) | **AUDITED** |
| **18** | Search in Rotated Sorted Array | Rotation mechanics, half-sorted invariant, target isolation in sorted half | [02_search_in_rotated_sorted_array.md](./02_search_in_rotated_sorted_array.md) | **AUDITED** |
| **19** | Peak Index in Mountain Array | Bitonic arrays, slope gradients, boundary safety, local peak isolation | [03_peak_index_in_mountain_array.md](./03_peak_index_in_mountain_array.md) | **AUDITED** |
| **20** | Single Element in Sorted Array | Index parity invariant, bitwise XOR partner mapping, duplicate elimination | [04_single_element_in_sorted_array.md](./04_single_element_in_sorted_array.md) | **AUDITED** |
| **21** | Book Allocation Problem | Binary Search on Answer space, monotonic feasibility predicate, contiguous partitioning | [05_book_allocation_problem.md](./05_book_allocation_problem.md) | **AUDITED** |
| **22** | Painter's Partition Problem | Minimizing maximum workload, 64-bit overflow safety, algorithmic isomorphism | [06_painters_partition_problem.md](./06_painters_partition_problem.md) | **AUDITED** |
| **23** | Aggressive Cows Problem | Maximizing minimum separation, greedy cow placement, inverted search space | [07_aggressive_cows_problem.md](./07_aggressive_cows_problem.md) | **AUDITED** |

---

## 🎯 Topic Revision & Interview Preparation
- **Topic Quick Revision:** [topic_revision.md](./topic_revision.md)
- **Topic Interview Question Bank:** [topic_interview_questions.md](./topic_interview_questions.md)

---

## 🗺️ Algorithmic Progression

```
[ Monotonic Sorted Binary Search (L17) ]
                    ↓
[ Rotated Half-Sorted Invariant Search (L18) ]
                    ↓
[ Slope / Gradient Non-Monotonic Peak Search (L19) ]
                    ↓
[ Even-Odd Index Parity Optimization (L20) ]
                    ↓
[ Binary Search on Answer Space: Min-Max (L21-L22) ]
                    ↓
[ Binary Search on Answer Space: Max-Min (L23) ]
```
"""

# Update topic_revision.md in 05_binary_search
notes["topic_revision.md"] = r"""# ⚡ Rapid Revision — Topic 05: Binary Search & Answer Spaces

> **Target:** 5-minute pre-interview refresher on all Binary Search patterns, formulas, invariants, and edge cases.

---

## 🔑 Core Invariants Summary

| Pattern | Search Space | Key Decision Formula | Direction Rule |
|---|---|---|---|
| **Classical Binary Search** | Monotonic array | `nums[mid] == target` | `nums[mid] < target ? low = mid + 1 : high = mid - 1` |
| **Rotated Sorted Array** | Half-sorted array | Identify sorted half: `nums[low] <= nums[mid]` | Target inside sorted half? Search it; else search unsorted half |
| **Peak in Mountain** | Bitonic array | `nums[mid] < nums[mid + 1]` | Ascending slope: `low = mid + 1`; Descending slope: `high = mid` |
| **Single Element** | Sorted pairs | `nums[mid] == nums[mid ^ 1]` | True: left side clean $\to$ `low = mid + 1`; False: `high = mid - 1` |
| **Book Allocation** | Answer $[\max(arr), \sum arr]$ | `isValid(mid)` checks if student count $\le M$ | Feasible: `ans = mid, high = mid - 1`; Infeasible: `low = mid + 1` |
| **Aggressive Cows** | Answer $[1, \text{stall}_{max} - \text{stall}_{min}]$ | `canPlace(mid)` checks if cow count $\ge K$ | Feasible: `ans = mid, low = mid + 1`; Infeasible: `high = mid - 1` |

---

## ⚠️ High-Risk Traps
1. **Integer Overflow:** Always use `mid = low + (high - low) / 2`. Never `(low + high) / 2`.
2. **Rotated Search Invariant:** Must use `<=` when checking `nums[low] <= nums[mid]` to handle 2-element subproblems.
3. **Answer Space Boundaries:**
   - Min-Max partition: `low = max(arr)`, `high = sum(arr)`.
   - Max-Min separation: `low = 1`, `high = arr[n-1] - arr[0]` (array must be sorted!).
"""

# Update topic_interview_questions.md in 05_binary_search
notes["topic_interview_questions.md"] = r"""# 💼 Topic Interview Question Bank — Topic 05: Binary Search

---

### Q1: How do you identify whether a problem can be solved with "Binary Search on Answer"?
**Answer:**
Look for these key indicators:
1. The question asks to **"Minimize the Maximum"** or **"Maximize the Minimum"**.
2. There is a monotonic property in the feasibility of the answer: if answer $X$ is feasible, all answers $> X$ (or $< X$) are guaranteed to be feasible.
3. A greedy verification function (`isValid(X)`) can check whether a candidate value $X$ is valid in $O(N)$ time.

---

### Q2: What is the significance of the `mid ^ 1` trick in Single Element in Sorted Array?
**Answer:**
In a paired array:
- If `mid` is even, `mid ^ 1 = mid + 1`.
- If `mid` is odd, `mid ^ 1 = mid - 1`.
Thus, `nums[mid] == nums[mid ^ 1]` checks if `mid` belongs to a valid pair matching the expected `(even, odd)` order in a single line without branching on parity.

---

### Q3: Why does Aggressive Cows require sorting while Book Allocation does not?
**Answer:**
- In Book Allocation, books must be distributed in **contiguous subarray order** to students as given in the problem statement. Reordering would change subarray partitions.
- In Aggressive Cows, stalls are spatial points in a 1D barn. The cows can occupy any stalls; sorting stall coordinates allows a straightforward single-pass greedy distance check from left to right.
"""

for filename, content in notes.items():
    fpath = os.path.join(t05_dir, filename)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {fpath}")

print("Completed Topic 05 remaining generation.")
