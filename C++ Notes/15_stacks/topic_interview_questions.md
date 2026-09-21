# 💼 Topic Interview Question Bank — Topic 15: Stacks

---

### Q1: Why does the Monotonic Stack achieve $O(N)$ time even with a nested `while` loop?
**Answer:**
This is proven via **Aggregate Amortized Analysis**. Every element from the input array is pushed onto the stack exactly once. An element that has been popped from the stack is never re-pushed. Over the course of the entire algorithm, the inner `while` loop can perform at most $N$ total `pop()` operations across all iterations. Thus, Total Operations $\le N \text{ pushes} + N \text{ pops} = 2N = O(N)$.
