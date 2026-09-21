# ⚡ Rapid Revision — Topic 15: Stacks

> **Target:** 5-minute pre-interview refresher on Stack patterns and Monotonic invariants.

---

## 🔑 Monotonic Stack Patterns
- **Next Greater to Right:** Scan right to left. While `st.top() <= curr`, `st.pop()`.
- **Previous Smaller to Left:** Scan left to right. While `st.top() >= curr`, `st.pop()`.
- **Histogram Max Area:** Monotonic increasing stack of indices. Width = `i - st.top() - 1`.
- **Min Stack Formula:** Encode `2 * val - minVal`. Decode `2 * minVal - top()`.
- **Celebrity Problem:** If `knows(a, b)` $\implies$ `a` is not celebrity; else `b` is not celebrity.
