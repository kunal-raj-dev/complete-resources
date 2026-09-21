# Lecture 14: Container With Most Water (LeetCode 11)

> **One-Line Purpose:** Master the Two-Pointer Greedy Shrink technique for LeetCode 11, understand the mathematical proof for pointer movement, and optimize from $O(N^2)$ to $O(N)$.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #14  
> **Video ID:** `EbkMABpP52U`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=EbkMABpP52U)  
> **Duration:** 32:00  
> **Transcript:** `.transcripts/03_arrays_and_vectors/014_Container_with_Most_Water_Problem___Brute___Optimal_Solution___Two_Pointer_Appro.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The geometric formulation of the Container With Most Water problem: $\text{Area} = \min(h_L, h_R) \times (R - L)$.
- Why the brute-force approach requires $O(N^2)$ operations and fails with Time Limit Exceeded (TLE) on large constraints ($N = 10^5$).
- The Two-Pointer inward scan algorithm achieving $O(N)$ time and $O(1)$ auxiliary space.
- The rigorous mathematical proof for why moving the pointer with the shorter vertical line is **always** optimal and never misses the maximum container.

---

## 🔵 Lecture Context

Container With Most Water is the quintessential interview problem used to test whether a candidate understands how to prune a two-dimensional search space in linear time using physical problem constraints.

---

## 1. Problem Formulation & Geometric Area

Given an integer array `height` of length $N$:
- The distance between indices $i$ and $j$ is the **width**: $w = j - i$.
- The height of trapped water is bounded by the **shorter of the two vertical lines**: $h = \min(\text{height}[i], \text{height}[j])$.
$$\text{Area}(i, j) = (j - i) \times \min(\text{height}[i], \text{height}[j])$$

---

## 2. Progressive Solutions

### A. Brute Force Approach ($O(N^2)$)
Test every combination of pairs $(i, j)$:
```cpp
int maxAreaBrute(const vector<int>& height) {
    int maxWater = 0;
    int n = height.size();

    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int w = j - i;
            int h = min(height[i], height[j]);
            maxWater = max(maxWater, w * h);
        }
    }
    return maxWater;
}
```
- **Complexity:** Time: $O(N^2)$, Space: $O(1)$. TLE for $N = 10^5$.

---

### B. Two-Pointer Greedy Shrink Approach ($O(N)$)

> 💡 **Core Intuition:**
> 1. Start with the **maximum possible width**: `left = 0`, `right = n - 1`.
> 2. Calculate the current trapped water area.
> 3. To potentially find a larger area with a *smaller* width, we **must find a taller line**.
> 4. Since the area is bottlenecked by $\min(\text{height}[left], \text{height}[right])$, moving the taller pointer will *never* increase the area (the width shrinks, and height cannot exceed the current shorter line).
> 5. Therefore, we **always advance the pointer that points to the shorter line**:
>    - If `height[left] < height[right]`: `left++`
>    - Else: `right--`

```cpp
#include <vector>
#include <algorithm>
#include <iostream>
using namespace std;

int maxArea(const vector<int>& height) {
    int left = 0;
    int right = height.size() - 1;
    int maxWater = 0;

    while (left < right) {
        int w = right - left;
        int h = min(height[left], height[right]);
        maxWater = max(maxWater, w * h);

        // Move the pointer pointing to the shorter line
        if (height[left] < height[right]) {
            left++;
        } else {
            right--;
        }
    }

    return maxWater;
}
```

- **Time Complexity:** $O(N)$ (Each step increments `left` or decrements `right`, processing each element at most once).
- **Space Complexity:** $O(1)$ auxiliary space.

---

## 🔍 Detailed Trace

Input: `height = [1, 8, 6, 2, 5, 4, 8, 3, 7]` ($N = 9$)

| Step | `left` | `right` | `h[left]` | `h[right]` | `width` | `min(h)` | Area | `maxWater` | Pointer Moved |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 8 | 1 | 7 | 8 | 1 | 8 | 8 | `left++` (1 < 7) |
| 2 | 1 | 8 | 8 | 7 | 7 | 7 | 49 | **49** | `right--` (8 > 7) |
| 3 | 1 | 7 | 8 | 3 | 6 | 3 | 18 | 49 | `right--` (8 > 3) |
| 4 | 1 | 6 | 8 | 8 | 5 | 8 | 40 | 49 | `right--` (tied) |
| 5 | 1 | 5 | 8 | 4 | 4 | 4 | 16 | 49 | `right--` (8 > 4) |
| 6 | 1 | 4 | 8 | 5 | 3 | 5 | 15 | 49 | `right--` (8 > 5) |
| 7 | 1 | 3 | 8 | 2 | 2 | 2 | 4 | 49 | `right--` (8 > 2) |
| 8 | 1 | 2 | 8 | 6 | 1 | 6 | 6 | 49 | `right--` (8 > 6) |

**Final Maximum Water:** `49` (formed between index 1 [height 8] and index 8 [height 7]).

---

## 🔥 Mathematical Proof of Correctness

Why is it impossible for this greedy movement to discard the optimal pair $(L^*, R^*)$?
- Suppose the true optimal container is formed by lines at indices $L^*$ and $R^*$.
- Since pointers start at `0` and `N-1`, one of the pointers (say `left`) will reach $L^*$ before `right` reaches $R^*$, or `right` reaches $R^*$ first.
- Assume without loss of generality that `right` reaches $R^*$ first while `left < L^*`.
- Can `right` ever prematurely move past $R^*$ before `left` reaches $L^*$?
  - For `right` to move, we must have `height[right] <= height[left]`.
  - But if `height[R*] <= height[left]`, then the area formed by $(left, R^*)$ would be $\text{width} \times \text{height}[R^*] > (R^* - L^*) \times \text{height}[R^*] \ge \text{Area}(L^*, R^*)$, which contradicts the assumption that $(L^*, R^*)$ was the global optimum!
- Thus, the shorter line at an suboptimal index is always safely eliminated without discarding the true optimum.

---

## Key Takeaways

1. **Bottleneck Property:** Water volume is strictly bounded by the shorter line.
2. **Greedy Elimination:** Moving the taller line only shrinks width without any possibility of increasing height.
3. **Linear Scan:** Inspects $N$ lines in $O(N)$ time with $O(1)$ memory.

---

## ⚡ 2-Minute Revision

- Area equation: $(R - L) \times \min(h[L], h[R])$.
- Pointer update rule:
  ```cpp
  if (height[left] < height[right]) left++;
  else right--;
  ```
- Guaranteed to run in $O(N)$ time and $O(1)$ space.
