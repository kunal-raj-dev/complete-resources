# Lecture 76: Trapping Rainwater (LeetCode 42)

> **One-Line Purpose:** Compute total trapped rainwater between terrain elevation bars in optimal $O(N)$ time and $O(1)$ space using the Two-Pointer inward boundary scan.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #76  
> **Video ID:** `UHHp8USwx4M`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=UHHp8USwx4M)  
> **Duration:** 30:50  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Formulate the fundamental math equation for trapped water at a single index.
- Understand the 3-pass Array pre-computation method ($O(N)$ space).
- Understand the Monotonic Stack method ($O(N)$ space).
- Master the optimal Two-Pointer approach ($O(1)$ space) based on dynamic bottleneck tracking.

---

## 🧠 Core Intuition — Why This Works

If you pour water over a histogram of bars, how much water stays directly above bar $i$?
It's determined completely by the tallest bar anywhere to its left (`leftMax`), and the tallest bar anywhere to its right (`rightMax`).
The water level will rise until it spills over the *shorter* of those two walls.
**Core Formula:**
`water[i] = max(0, min(leftMax, rightMax) - height[i])`

**The Two-Pointer Magic (How to drop to $O(1)$ space):**
We place a pointer at `left = 0` and `right = N - 1`.
We maintain `leftMax` and `rightMax`.
If `height[left] <= height[right]`, we are 100% mathematically certain that `leftMax` will be $\le$ whatever the true `rightMax` ends up being. Why? Because `height[right]` is already taller than `height[left]`, so the right side forms a guaranteed taller wall!
Therefore, the bottleneck for the `left` pointer is strictly `leftMax`. We don't even need to know the *exact* `rightMax` for that cell!
We can confidently calculate `trappedWater += leftMax - height[left]` and move `left++`. We do the inverse if `height[right] < height[left]`.

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Trapping water", "Holding capacity"**: Direct keyword.
- **"Find the bottleneck bounded by two extremes"**: Often solved by Two-Pointer inward scan.
- **Histogram problems with water/filling**: If it asks for Area, use Monotonic Stack (Largest Rectangle). If it asks for trapped capacity, use Two-Pointer.

---

## 📐 Algorithm Walk-Through

1. Initialize `left = 0`, `right = n - 1`.
2. Initialize `leftMax = 0`, `rightMax = 0`, `water = 0`.
3. Loop `while (left <= right)`:
   - **Case 1: Left wall is shorter or equal** (`height[left] <= height[right]`):
     - If `height[left] >= leftMax`, it means this bar is the new highest left wall. It cannot hold water. `leftMax = height[left]`.
     - Else, it holds water! `water += leftMax - height[left]`.
     - `left++`.
   - **Case 2: Right wall is shorter** (`height[left] > height[right]`):
     - If `height[right] >= rightMax`, update `rightMax = height[right]`.
     - Else, it holds water! `water += rightMax - height[right]`.
     - `right--`.
4. Return `water`.

---

## 💻 Complete C++ Implementation: Optimal Two-Pointer

```cpp
#include <vector>
#include <algorithm>
#include <iostream>

using namespace std;

class SolutionTrappingWater {
public:
    int trap(vector<int>& height) {
        int left = 0, right = height.size() - 1;
        int leftMax = 0, rightMax = 0;
        int trappedWater = 0;

        while (left <= right) {
            // The side with the smaller current height dictates the bottleneck
            if (height[left] <= height[right]) {
                if (height[left] >= leftMax) {
                    leftMax = height[left]; // Update max wall
                } else {
                    trappedWater += leftMax - height[left]; // Collect water
                }
                left++;
            } else {
                if (height[right] >= rightMax) {
                    rightMax = height[right]; // Update max wall
                } else {
                    trappedWater += rightMax - height[right]; // Collect water
                }
                right--;
            }
        }

        return trappedWater;
    }
};

int main() {
    SolutionTrappingWater solver;
    // Classic LeetCode example
    vector<int> elevation = {0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1};
    cout << "Trapped Water: " << solver.trap(elevation) << endl; 
    // Output: 6
    return 0;
}
```

---

## 🔍 Dry Run Trace

**Input:** `[0, 1, 0, 2, 1, 0, 1, 3]`
- `L=0, R=7`. `h[0]=0, h[7]=3`. `L` is smaller. `leftMax = 0`. `water += 0`. `L++`.
- `L=1, R=7`. `h[1]=1, h[7]=3`. `L` is smaller. `leftMax = 1`. `water += 0`. `L++`.
- `L=2, R=7`. `h[2]=0, h[7]=3`. `L` is smaller. `leftMax` is 1. `h[L] < leftMax`. 
  - `water += 1 - 0 = 1`. `L++`. (Water pools at index 2).
- `L=3, R=7`. `h[3]=2, h[7]=3`. `L` is smaller. `leftMax = 2`. `water += 0`. `L++`.
- `L=4, R=7`. `h[4]=1, h[7]=3`. `L` is smaller. `h[L] < leftMax (2)`.
  - `water += 2 - 1 = 1`. `L++`.
- `L=5, R=7`. `h[5]=0, h[7]=3`. `L` is smaller. `h[L] < leftMax (2)`.
  - `water += 2 - 0 = 2`. `L++`.
- `L=6, R=7`. `h[6]=1, h[7]=3`. `L` is smaller. `h[L] < leftMax (2)`.
  - `water += 2 - 1 = 1`. `L++`.
- `L=7, R=7`. `h[7]=3 <= h[7]=3`. `L` is smaller/equal. `leftMax = 3`. `water += 0`. `L++`.
- Loop ends (`L > R`).

**Total water = 1 + 1 + 2 + 1 = 5 units.**

---

## ⚠️ Common Interview Mistakes

1. **Forgetting `left <= right` boundary**: The loop condition must be `<` or `<=`. If you use `<=`, make sure you don't double count if `left` and `right` point to the same index (our logic naturally adds `0` water when they meet on a peak, so it's safe).
2. **Missing `leftMax` updates**: You must explicitly check `if (height[left] >= leftMax)` and update it, instead of blinding doing `water += leftMax - height[left]`. If you blindly subtract, you will get negative water when climbing a new hill.
3. **Not knowing the Stack or Array approaches**: An interviewer might specifically ask for the Stack approach to test if you know Monotonic Stacks, even though Two-Pointer is better for space. (The stack approach computes horizontal strips of water instead of vertical columns).

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N)$. Each element is processed exactly once by either the left or right pointer.
- **Space Complexity:** $O(1)$. We only use a few integer variables, vastly superior to the $O(N)$ `leftMaxArray` / `rightMaxArray` pre-computation approach.

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Can you explain the Monotonic Stack approach to this problem?
**Answer:** Yes. We use a decreasing monotonic stack. If we find a bar `height[i]` taller than `st.top()`, it means the bar at `st.top()` is a bounded depression (a puddle). We pop it. The new `st.top()` is the left wall, and `height[i]` is the right wall. The water trapped in that horizontal strip is `distance * (min(left_wall, right_wall) - puddle_height)`. We add it and continue popping until monotonicity is restored.

### Q2: Why is the Two-Pointer approach strictly better than the Stack approach?
**Answer:** The Two-Pointer approach uses $O(1)$ space, while the Stack uses $O(N)$ space. Additionally, the Two-Pointer approach does a single pass with simple arithmetic, avoiding the constant-time overhead of stack `push`/`pop` operations.

### Q3: What if the terrain is a 2D grid (Trapping Rain Water II)?
**Answer:** The Two-Pointer approach fails on a 2D grid because water can spill in 4 directions, not just 2. We must use a **Min-Priority Queue**. We push all the boundary cells of the grid into the Min-Heap. We repeatedly pop the lowest boundary cell, check its unvisited neighbors, fill them with water if they are lower, and push the neighbors into the heap with `max(height, water_level)`. This takes $O(R \cdot C \log(R \cdot C))$ time.

### Q4: If the array is sorted (ascending or descending), how much water is trapped?
**Answer:** Exactly 0. If it's ascending, `rightMax` is always the bottleneck, but `leftMax` matches the current height, so `water += 0`. To trap water, you strictly need a "valley" shape (decreasing then increasing).

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 407: Trapping Rain Water II](https://leetcode.com/problems/trapping-rain-water-ii/)** — The infamous 3D/2D grid variant requiring a Min-Heap.
2. **[Leetcode 11: Container With Most Water](https://leetcode.com/problems/container-with-most-water/)** — Another Two-Pointer problem, but you want to maximize Area (width $\times$ height) between just 2 lines, not total volume.
3. **[Leetcode 84: Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/)** — The inverse problem (Area vs Trapped Capacity).

---

## 🔗 Cross-Topic Connections
- **Two Pointers:** The ultimate optimization technique for bounding-box arrays.
- **Monotonic Stacks:** The alternate solution path.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Find total trapped water volume.
- **Formula:** `water = min(leftMax, rightMax) - currentHeight`.
- **Optimal Approach:** Two Pointers (`L=0, R=N-1`).
- **Core Logic:** The shorter pointer dictates the bottleneck. If `h[L] <= h[R]`, evaluate L, update `leftMax` or add water, `L++`. Else evaluate R, update `rightMax` or add water, `R--`.
- **Time/Space:** $O(N)$ Time | $O(1)$ Space.
