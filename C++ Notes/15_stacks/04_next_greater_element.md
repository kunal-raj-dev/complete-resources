# Lecture 71: Next Greater Element I (LeetCode 496)

> **One-Line Purpose:** Compute the first greater element to the right using a right-to-left monotonic decreasing stack in linear $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #71  
> **Video ID:** `NKbExYwvjb0`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=NKbExYwvjb0)  
> **Duration:** 23:32  
> **Status:** AUDITED  

---

## 🔵 Complete Implementation

```cpp
#include <vector>
#include <stack>
#include <iostream>
using namespace std;

vector<int> nextGreaterElements(const vector<int>& nums) {
    int n = nums.size();
    vector<int> nge(n);
    stack<int> st;

    // Traverse from right to left
    for (int i = n - 1; i >= 0; i--) {
        while (!st.empty() && st.top() <= nums[i]) {
            st.pop();
        }

        nge[i] = st.empty() ? -1 : st.top();
        st.push(nums[i]);
    }
    return nge;
}
```
- **Time Complexity:** $O(N)$ amortized.
- **Space Complexity:** $O(N)$ stack memory.
