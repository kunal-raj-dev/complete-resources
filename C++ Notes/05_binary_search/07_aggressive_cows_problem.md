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

## 🔥 Interview Questions

### Q1: Why is greedy placement optimal in `canPlaceCows`?
- **Answer:** Placing the first cow as far left as possible (`stalls[0]`) leaves the maximum possible remaining track length for placing the remaining $C-1$ cows. Any alternative non-greedy choice restricts the remaining distance, strictly reducing feasibility.
