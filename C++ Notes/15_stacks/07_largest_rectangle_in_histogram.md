# Lecture 74: Largest Rectangle in Histogram (LeetCode 84)

> **One-Line Purpose:** Compute maximum rectangular area under a histogram in a single pass using a monotonic increasing index stack in $O(N)$ time.

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

## 🔵 Complete C++ Single-Pass Implementation

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
        stack<int> st;
        int maxArea = 0;

        for (int i = 0; i <= n; i++) {
            int currHeight = (i == n) ? 0 : heights[i];

            while (!st.empty() && currHeight < heights[st.top()]) {
                int h = heights[st.top()];
                st.pop();

                int width = st.empty() ? i : (i - st.top() - 1);
                maxArea = max(maxArea, h * width);
            }
            st.push(i);
        }
        return maxArea;
    }
};
```
- **Time Complexity:** $O(N)$ — Every bar index is pushed and popped at most once.
- **Space Complexity:** $O(N)$ stack memory.
