# Lecture 72: Previous Smaller Element

> **One-Line Purpose:** Identify the nearest smaller element to the left using a left-to-right monotonic increasing stack.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #72  
> **Video ID:** `WnjUfBn9nZM`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=WnjUfBn9nZM)  
> **Duration:** 09:24  
> **Status:** AUDITED  

---

## 🔵 Complete Implementation

```cpp
#include <vector>
#include <stack>
using namespace std;

vector<int> prevSmallerElements(const vector<int>& nums) {
    int n = nums.size();
    vector<int> pse(n);
    stack<int> st;

    for (int i = 0; i < n; i++) {
        while (!st.empty() && st.top() >= nums[i]) {
            st.pop();
        }
        pse[i] = st.empty() ? -1 : st.top();
        st.push(nums[i]);
    }
    return pse;
}
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$.
