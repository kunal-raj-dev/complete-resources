# 💼 Topic Interview Question Bank — Topic 16: Queues

---

### Q1: Why is the amortized time complexity of `pop()` in Queue-using-Two-Stacks $O(1)$?
**Answer:**
Each element is pushed into `inStack` once ($O(1)$). When `outStack` becomes empty, elements from `inStack` are transferred to `outStack` once ($O(1)$ per element). The element is then popped from `outStack` once ($O(1)$). Over $N$ total elements, at most $3N$ operations occur across the lifetime of the queue $\implies$ average $O(1)$ per operation.
