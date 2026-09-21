# Lecture 73: Design Min Stack (LeetCode 155)

> **One-Line Purpose:** Implement a stack with $O(1)$ push, pop, top, and getMin using an encoding transformation formula to achieve $O(1)$ auxiliary space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #73  
> **Video ID:** `wHDm-N2m2XY`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=wHDm-N2m2XY)  
> **Duration:** 24:34  
> **Status:** AUDITED  

---

## 🔵 Optimal $O(1)$ Space Mathematical Encoding

When a new element `val < currentMin` arrives:
Push the encoded value:
$$\text{encodedVal} = 2 \times \text{val} - \text{minVal}$$
When popping, if `top() < minVal`, restore previous minimum via:
$$\text{prevMin} = 2 \times \text{minVal} - \text{top()}$$

```cpp
#include <stack>
#include <climits>
using namespace std;

class MinStack {
private:
    stack<long long> st;
    long long minVal;

public:
    MinStack() {
        minVal = LLONG_MAX;
    }

    void push(int val) {
        if (st.empty()) {
            st.push(val);
            minVal = val;
        } else if (val >= minVal) {
            st.push(val);
        } else {
            st.push(2LL * val - minVal);
            minVal = val;
        }
    }

    void pop() {
        if (st.empty()) return;
        long long topVal = st.top();
        st.pop();

        if (topVal < minVal) {
            minVal = 2LL * minVal - topVal;
        }
    }

    int top() {
        if (st.empty()) return -1;
        long long topVal = st.top();
        if (topVal < minVal) {
            return (int)minVal;
        }
        return (int)topVal;
    }

    int getMin() {
        return (int)minVal;
    }
};
```
- **Time Complexity:** All operations strictly $O(1)$.
- **Auxiliary Space:** $O(1)$ beyond the single underlying stack.
