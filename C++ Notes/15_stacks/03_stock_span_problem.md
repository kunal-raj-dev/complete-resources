# Lecture 70: Stock Span Problem: Monotonic Decreasing Stack

> **One-Line Purpose:** Calculate consecutive preceding days with stock price $\le$ today using an index-storing monotonic decreasing stack in amortized $O(1)$ per query.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #70  
> **Video ID:** `01vBuZyMfqk`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=01vBuZyMfqk)  
> **Duration:** 26:29  
> **Status:** AUDITED  

---

## 🔵 Lecture Content & Implementation

```cpp
#include <vector>
#include <stack>
#include <iostream>
using namespace std;

class StockSpanner {
private:
    stack<pair<int, int>> st; // pair: <price, span>

public:
    StockSpanner() {}

    int next(int price) {
        int span = 1;
        while (!st.empty() && st.top().first <= price) {
            span += st.top().second;
            st.pop();
        }
        st.push({price, span});
        return span;
    }
};
```
- **Time Complexity:** Amortized $O(1)$ per `next()` call.
- **Space Complexity:** $O(N)$ in the worst case.
