# Lecture 22: Painter's Partition Problem: Minimizing Max Workload

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

## 🧠 Core Intuition — Why This Works
The problem asks for the minimum possible time to finish painting. If we guess a maximum time capacity (`mid`), we can greedily simulate assigning boards to painters. If we can finish painting without exceeding $K$ painters, our capacity `mid` is feasible. Since the feasibility function monotonically changes from `false` to `true` as capacity increases, we can binary search the exact tipping point. The minimum possible answer is the largest single board (because one painter MUST paint it alone), and the maximum possible answer is the sum of all boards (if only 1 painter exists).

## 🎯 Pattern Recognition — When to Use This
- **Trigger cues:** "Divide continuous array into K contiguous partitions", "Minimize the maximum sum among partitions".
- **Keywords:** Binary Search on Answer Space, Min-Max Optimization, Contiguous allocation.

## 📐 Algorithm Walk-Through
1. Setup search space: `low = max(boards)`, `high = sum(boards)`.
2. Binary search `mid` from `low` to `high`:
   - `mid = low + (high - low) / 2`.
   - Call `isFeasible(boards, K, mid)`.
   - In `isFeasible`, iterate over `boards`. Keep a running `currentWork`.
   - If adding a board exceeds `mid`, assign it to a new painter (`painters++`).
   - If `painters > K`, return `false`.
   - If feasible, we successfully finished under limit `mid`. Record `ans = mid` and try to minimize further (`high = mid - 1`).
   - Else, limit was too strict (`low = mid + 1`).
3. Return `ans * t`.

## 🔍 Dry Run Trace
`boards = [10, 20, 30, 40], K = 2`
- `low = 40, high = 100`
- **Iter 1:** `mid = 70`.
  - P1 takes 10+20+30 = 60. Next is 40. 60+40 > 70.
  - P2 takes 40. Total painters = 2.
  - Feasible! `ans = 70`, `high = 69`.
- **Iter 2:** `mid = (40+69)/2 = 54`.
  - P1 takes 10+20 = 30.
  - P2 takes 30.
  - P3 takes 40. Painters = 3 > 2.
  - Not feasible. `low = 55`.
- **Iter 3:** `mid = (55+69)/2 = 62`.
  - P1 takes 10+20+30 = 60.
  - P2 takes 40.
  - Feasible! `ans = 62`, `high = 61`.
- Continues until `ans = 60`.

## ⚠️ Common Interview Mistakes
- **Overflow:** Summing all boards to find `high` often exceeds $2^{31}-1$. Use `long long` for `low`, `high`, `mid`, and `currentWork`.
- **Initial Limits:** Setting `low = 0` instead of `max(boards)`. A painter *must* be able to paint the largest board, so no capacity below `max(boards)` is physically possible.
- **Sorting the array:** The problem requires contiguous subarrays. Sorting the array destroys the contiguous sequence requirement!

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: What happens if $K$ is greater than the number of boards $N$?
**Answer:** The answer is simply the maximum element in the array. Every board is assigned to a different painter, and the bottleneck is the painter with the largest board.

### Q2: Why is the problem isomorphic to Book Allocation and Split Array Largest Sum?
**Answer:** In all three, you are partitioning an array into $K$ contiguous subarrays to minimize the largest subarray sum. Only the terminology changes (pages vs lengths vs subarray sums). The code template is $100\%$ identical.

### Q3: How do we trace the actual partition boundaries after finding the optimal answer?
**Answer:** Once the optimal minimum capacity `C` is found, run the greedy `isFeasible` algorithm one last time with limit `C`. Whenever you reset `currentWork` to start a new painter, that denotes a partition boundary.

## 🏆 Related Problems (Leetcode)
- **LeetCode 410:** Split Array Largest Sum (Exact same code)
- **LeetCode 1011:** Capacity To Ship Packages Within D Days (Exact same code)
- **LeetCode 1482:** Minimum Number of Days to Make m Bouquets (Binary Search on Answer)

## 🔗 Cross-Topic Connections
- **Greedy:** The `isFeasible` helper function is a pure greedy algorithm.
- **Dynamic Programming:** This problem can also be solved using DP ($O(K \times N^2)$ time), but Binary Search is much faster ($O(N \log \Sigma)$).

## ⚡ 2-Minute Revision Flash Card
- **Problem:** Partition array into $K$ contiguous parts, minimize the max sum.
- **Search Space:** `low = max(arr)`, `high = sum(arr)`.
- **Feasibility:** Iterate array. If `sum + arr[i] > mid`, increment parts, `sum = arr[i]`. If `parts > K`, return `false`.
- **BS Logic:** If feasible, `ans = mid; high = mid - 1;` else `low = mid + 1;`.
- **Trap:** Do NOT sort the array. Use `long long` for sums.
