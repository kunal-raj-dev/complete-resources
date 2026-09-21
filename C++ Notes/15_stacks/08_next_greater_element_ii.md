# Lecture 75: Next Greater Element II: Circular Array (LeetCode 503)

> **One-Line Purpose:** Solve Next Greater Element on a circular array by simulating virtual array doubling ($2N - 1$ down to $0$).

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #75  
> **Video ID:** `If--3pm9K3U`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=If--3pm9K3U)  
> **Duration:** 20:04  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Implementation

```cpp
#include <vector>
#include <stack>
using namespace std;

class SolutionNextGreaterII {
public:
    vector<int> nextGreaterElements(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n, -1);
        stack<int> st;

        for (int i = 2 * n - 1; i >= 0; i--) {
            int idx = i % n;

            while (!st.empty() && st.top() <= nums[idx]) {
                st.pop();
            }

            if (i < n) {
                res[idx] = st.empty() ? -1 : st.top();
            }

            st.push(nums[idx]);
        }
        return res;
    }
};
```
- **Time Complexity:** $O(N)$ (exactly $2N$ iterations).
- **Space Complexity:** $O(N)$.
