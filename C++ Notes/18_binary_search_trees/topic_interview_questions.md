# 💼 Topic Interview Question Bank — Topic 18: Binary Search Trees

---

### Q1: Why does `BSTIterator` achieve $O(1)$ amortized time per `next()` call?
**Answer:**
Each node of the BST is pushed onto the iterator's internal stack exactly once and popped from the stack exactly once across all $N$ invocations of `next()`. Over the entire traversal, total operations $\le 2N$. Amortized time per `next()` call is $2N / N = O(1)$. Space complexity is bounded by the height of the tree $O(H)$, which is $O(\log N)$ for balanced BSTs.
