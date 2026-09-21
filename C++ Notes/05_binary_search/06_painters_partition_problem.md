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
