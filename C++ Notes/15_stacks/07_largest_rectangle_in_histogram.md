# Lecture 74: Largest Rectangle in Histogram (LeetCode 84)

> **One-Line Purpose:** Find the maximum rectangular area in a histogram in $O(N)$ single-pass time using a Monotonic Increasing Stack to calculate boundary extensions.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #74  
> **Video ID:** `ysy1o-QEj3k`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=ysy1o-QEj3k)  
> **Duration:** 32:56  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Master the "Next Smaller Element" (NSE) and "Previous Smaller Element" (PSE) concepts simultaneously.
- Formulate the width of a rectangle expanding from a central bar: `Width = NSE - PSE - 1`.
- Optimize a 3-pass algorithm ($O(N)$ with 3 arrays) down to a beautiful, single-pass $O(N)$ monotonic stack trick.

---

## 🧠 Core Intuition — Why This Works

Imagine picking ANY single bar in the histogram. If you try to form the largest rectangle possible using *that specific bar* as the full height, how wide can the rectangle be?
It can expand left until it hits a bar that is *shorter* than it (Previous Smaller Element, PSE). 
It can expand right until it hits a bar that is *shorter* than it (Next Smaller Element, NSE).

The area for that specific bar is: `height[i] * (NSE_index - PSE_index - 1)`.

**The Monotonic Stack Magic:**
We keep a stack of indices that represents a strictly *increasing* slope of heights. 
Why? Because as long as the heights keep going up, we don't know their Right Boundary (NSE) yet. 
The moment we encounter a bar `height[i]` that is *shorter* than the bar at the top of our stack, we have found the top bar's NSE! 
And what is the top bar's PSE? It is simply the bar right below it in the stack (because the stack is strictly increasing!).
Thus, every time we pop a bar, we instantly know both its boundaries and can calculate its maximum area on the fly.

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Largest Rectangle / Area" in a 1D or 2D grid**: Classic histogram setup.
- **"Maximum Subarray Minimum"**: Problems that require maximizing `min(subarray) * length(subarray)`.
- **"Water trapping" variants**: Although trapping water uses NSE/NGE for boundaries, area maximization relies heavily on NSE/PSE logic.

---

## 📐 Algorithm Walk-Through (Single-Pass Optimal)

1. Initialize a `stack<int> st` to store indices, and `maxArea = 0`.
2. Loop `i` from $0$ to $N$ (inclusive).
   - If `i == N`, pretend we encountered a bar of height $0$. This forces the stack to completely empty out at the end, calculating areas for all remaining bars.
3. **While loop:** If `stack` is not empty AND `currentHeight < height[st.top()]`:
   - We found the Right Boundary (NSE) for the bar at `st.top()`.
   - `h = height[st.top()]`, then `st.pop()`.
   - The Left Boundary (PSE) is now the *new* `st.top()`.
   - `width = st.empty() ? i : (i - st.top() - 1)`.
     *(If stack is empty, it means this bar was the smallest seen so far, so its left boundary extends all the way to index 0. Hence width is `i`).*
   - `maxArea = max(maxArea, h * width)`.
4. **Push:** `st.push(i)`.
5. Return `maxArea`.

---

## 💻 Complete C++ Implementation: Optimal Single-Pass

```cpp
#include <vector>
#include <stack>
#include <algorithm>
#include <iostream>

using namespace std;

class SolutionHistogram {
public:
    int largestRectangleArea(vector<int>& heights) {
        int n = heights.size();
        stack<int> st; // Stores indices of monotonic increasing heights
        int maxArea = 0;

        // Loop runs up to 'n' (inclusive) to flush the stack at the end
        for (int i = 0; i <= n; ++i) {
            // Treat the boundary after the last bar as height 0
            int currentHeight = (i == n) ? 0 : heights[i];

            // If we find a shorter bar, it's the right boundary for the stack's top
            while (!st.empty() && currentHeight < heights[st.top()]) {
                int h = heights[st.top()];
                st.pop();
                
                // If stack is empty, it means the popped bar has no left boundary 
                // that is strictly smaller, so it spans all the way to index 0.
                int width = st.empty() ? i : (i - st.top() - 1);
                
                maxArea = max(maxArea, h * width);
            }

            st.push(i);
        }

        return maxArea;
    }
};

int main() {
    SolutionHistogram solver;
    // Classic LeetCode example
    vector<int> h = {2, 1, 5, 6, 2, 3};
    cout << "Max Histogram Area: " << solver.largestRectangleArea(h) << endl; 
    // Output: 10 (Height 5 & 6 form a 2x5 rectangle)
    return 0;
}
```

---

## 🔍 Dry Run Trace

**Input:** `[2, 1, 5, 6, 2, 3]`. `N = 6`.

- `i=0, h=2`: Stack `[0]`.
- `i=1, h=1`: 1 < height[0](2). 
  - Pop `0` (h=2). Stack empty $\to$ width = `1`. Area = $2 \times 1 = 2$. `maxArea = 2`.
  - Push `1`. Stack `[1]`.
- `i=2, h=5`: 5 > 1. Push `2`. Stack `[1, 2]`.
- `i=3, h=6`: 6 > 5. Push `3`. Stack `[1, 2, 3]`.
- `i=4, h=2`: 2 < height[3](6).
  - Pop `3` (h=6). New top `2`. Width = $4 - 2 - 1 = 1$. Area = $6 \times 1 = 6$. `maxArea = 6`.
  - 2 < height[2](5).
  - Pop `2` (h=5). New top `1`. Width = $4 - 1 - 1 = 2$. Area = $5 \times 2 = 10$. `maxArea = 10`.
  - Push `4`. Stack `[1, 4]`.
- `i=5, h=3`: 3 > 2. Push `5`. Stack `[1, 4, 5]`.
- `i=6, h=0` (End of array flush):
  - Pop `5` (h=3). Top `4`. Width = $6 - 4 - 1 = 1$. Area = 3. 
  - Pop `4` (h=2). Top `1`. Width = $6 - 1 - 1 = 4$. Area = 8.
  - Pop `1` (h=1). Stack empty. Width = 6. Area = 6.
- `maxArea = 10`.

---

## ⚠️ Common Interview Mistakes

1. **Forgetting to Flush the Stack**: If you only iterate from `0` to `n-1`, any strictly increasing sequence (e.g., `[1, 2, 3, 4]`) will leave all indices in the stack and `maxArea` will be 0! You MUST process a dummy `0` height at index `n` to force all pops.
2. **Width Formula Error**: `width = i - st.top() - 1`. Students often write `i - st.top()` or `i - popped_index`. The left boundary is `st.top()` AFTER the pop.
3. **Empty Stack Panic**: When `st.pop()` leaves the stack empty, calling `st.top()` for the width will SegFault. You must check `st.empty()`. If it is empty, the width is simply `i` (the distance from index 0).

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N)$. Even though there is a `while` loop inside the `for` loop, every index is pushed to the stack exactly once and popped exactly once. The amortized cost per element is $O(1)$, leading to $O(N)$ total time.
- **Space Complexity:** $O(N)$ for the stack in the worst-case (a strictly increasing histogram).

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Is the 3-pass algorithm (pre-computing Left-Smaller and Right-Smaller arrays) acceptable in an interview?
**Answer:** Yes, it is heavily recommended to explain the 3-pass $O(N)$ space / $O(N)$ time solution first! It proves you understand the PSE/NSE concept. Once you code or explain it, the interviewer will ask "Can we do it in one pass with less overhead?" That's your cue to introduce the single-pass stack method.

### Q2: How is this problem related to "Maximal Rectangle in a 2D Binary Matrix"?
**Answer:** LeetCode 85 (Maximal Rectangle) literally uses this problem as a subroutine. You treat each row of the 2D matrix as the base of a histogram, accumulating heights of '1's upwards. You then run *this exact algorithm* on every row. A $N \times M$ matrix takes $O(N \times M)$ time.

### Q3: What if multiple bars have the exact same height?
**Answer:** The algorithm still works perfectly. The first duplicate will pop the earlier duplicate (depending on strict `<` or `<=`), but ultimately the final width calculated when they hit a truly smaller bar will encompass all the duplicates correctly.

### Q4: Can this be solved with Divide and Conquer?
**Answer:** Yes. The max area is either: completely to the left of the minimum bar, completely to the right, or crossing the minimum bar (which is `min_height * total_width`). You can find the minimum using a Segment Tree in $O(\log N)$ and recurse. Total time $O(N \log N)$. However, the Stack approach $O(N)$ is strictly superior.

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 85: Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/)** — The 2D matrix version that calls this algorithm on every row.
2. **[Leetcode 42: Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/)** — Sister problem. Uses a monotonically decreasing stack instead to bound water.
3. **[Leetcode 907: Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/)** — Uses the exact same NSE/PSE logic to find how many subarrays a specific element is the minimum for.

---

## 🔗 Cross-Topic Connections
- **Monotonic Stacks:** This is the absolute pinnacle of monotonic stack problems. If you master this, Next Greater/Smaller Element is trivial.
- **Segment Trees:** Mentioned above as an alternative Divide & Conquer approach.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Maximize `height[i] * width` for a histogram.
- **Core Insight:** `Width = NSE_index - PSE_index - 1`.
- **Optimal Strategy:** Increasing Monotonic Stack.
- **Trigger Condition:** `height[i] < height[stack.top()]`. This means `i` is the NSE!
- **Left Boundary (PSE):** The new `stack.top()` immediately after popping the current top.
- **Flush Trick:** Run loop to $N$, forcing a height of $0$ to pop everything at the end.
- **Time/Space:** $O(N)$ Time | $O(N)$ Space.
