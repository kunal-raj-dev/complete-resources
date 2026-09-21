# Lecture 23: Aggressive Cows Problem: Maximizing the Minimum Distance

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

## 🧠 Core Intuition — Why This Works
Instead of calculating distances and trying to maximize them directly (which leads to combinatorial explosion), we reverse the problem. We ask: "Is it possible to place cows such that the minimum distance between them is at least `mid`?" If it is possible, maybe we can place them even further apart! The boolean answer flips monotonically from `true` (easy to place them close) to `false` (impossible to place them far). This monotonicity allows Binary Search. By sorting the array, we can greedily place cows left-to-right to verify feasibility.

## 🎯 Pattern Recognition — When to Use This
- **Trigger cues:** "Maximize the minimum distance", "Place items in discrete positions with max separation".
- **Keywords:** Maximize Minimum, Binary Search on Answer Space, Greedy Placement.

## 📐 Algorithm Walk-Through
1. **Sort** the stalls array.
2. Setup search space: `low = 1`, `high = stalls[N-1] - stalls[0]`.
3. Binary search `mid` from `low` to `high`:
   - `mid = low + (high - low) / 2`.
   - Call `canPlaceCows(stalls, K, mid)`.
   - In `canPlaceCows`, place cow 1 at `stalls[0]`. Iterate through stalls. If `stalls[i] - lastPos >= mid`, place next cow, update `lastPos`.
   - If `cowsPlaced == K`, return `true`.
   - If feasible, `ans = mid`, try for more: `low = mid + 1`.
   - Else, limit too high: `high = mid - 1`.
4. Return `ans`.

## 🔍 Dry Run Trace
`stalls = [1, 2, 8, 4, 9], K = 3`
1. Sorted: `[1, 2, 4, 8, 9]`. `low=1, high=8`.
2. **Iter 1:** `mid = 4`.
   - Place C1 at 1. Need $\ge 1+4=5$.
   - Skip 2, 4. Place C2 at 8. Need $\ge 8+4=12$.
   - Skip 9. Only placed 2 cows. Feasible? `false`.
   - `high = mid - 1 = 3`.
3. **Iter 2:** `mid = 2`.
   - C1 at 1. Need 3.
   - C2 at 4. Need 6.
   - C3 at 8. Placed 3! Feasible? `true`.
   - `ans = 2`, `low = 3`.
4. **Iter 3:** `mid = 3`.
   - C1 at 1. Need 4.
   - C2 at 4. Need 7.
   - C3 at 8. Placed 3! Feasible? `true`.
   - `ans = 3`, `low = 4`. Loop ends. Result = 3.

## ⚠️ Common Interview Mistakes
- **Forgetting to sort:** Binary search on answer space requires the greedy placement to move strictly left-to-right. Sorting is non-negotiable here (unlike Book Allocation, where sorting destroys contiguous subarrays).
- **Incorrect High Bound:** Setting `high = max(stalls)`. The maximum distance is `max(stalls) - min(stalls)`.
- **Flipping logic:** Confusing this with Min-Max problems. Here, feasibility means we should try `low = mid + 1`, not `high = mid - 1`.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Why is greedy placement optimal in `canPlaceCows`?
**Answer:** Placing the first cow as far left as possible (`stalls[0]`) leaves the maximum possible remaining track length for placing the remaining $C-1$ cows. Any alternative non-greedy choice restricts the remaining distance, strictly reducing feasibility.

### Q2: What if we have 2 cows?
**Answer:** If $C = 2$, we place one at the first stall and one at the last stall. The answer is `stalls[N-1] - stalls[0]`.

### Q3: Why search space `low = 1`? Can distance be 0?
**Answer:** If there are multiple identical stall locations, distance could be 0, but stalls are typically unique coordinates. Thus minimum positive distance is 1.

### Q4: How does this differ from Book Allocation/Painter's Partition?
**Answer:** In Book Allocation (Min-Max), `mid` is a cap on the sum. If feasible, we want to tighten the cap (`high = mid - 1`). In Aggressive Cows (Max-Min), `mid` is a floor on the distance. If feasible, we want to push the floor higher (`low = mid + 1`).

## 🏆 Related Problems (Leetcode)
- **LeetCode 1552:** Magnetic Force Between Two Balls (Exact same problem)
- **LeetCode 2517:** Maximum Tastiness of Candy Basket (Same logic, different story)
- **LeetCode 410:** Split Array Largest Sum (The Min-Max sibling problem)

## 🔗 Cross-Topic Connections
- **Greedy Algorithms:** The boolean checker is a perfect illustration of greedy choice property preserving optimality.

## ⚡ 2-Minute Revision Flash Card
- **Problem:** Maximize the minimum separation between items.
- **Pre-step:** Sort the array.
- **Search Space:** `low = 1`, `high = max - min`.
- **Feasibility:** Place item 1 at `arr[0]`. Find next item $\ge$ `last + mid`.
- **BS Logic:** If feasible, `ans = mid; low = mid + 1;` (Push for larger).
- **Trap:** Do not forget to sort. Search logic is opposite of Min-Max.
