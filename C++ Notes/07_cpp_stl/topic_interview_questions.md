# 💼 Topic Interview Question Bank — Topic 07: C++ STL

---

### Q1: What is the difference between `map` and `unordered_map`?
**Answer:**
- `std::map` is implemented via a Self-Balancing Binary Search Tree (Red-Black Tree). Keys are stored in sorted order. Search, insertion, and deletion are guaranteed $O(\log N)$ worst-case.
- `std::unordered_map` is implemented via a Hash Table with buckets. Keys are unordered. Search, insertion, and deletion are $O(1)$ amortized average, but can degrade to $O(N)$ in the event of hash collisions.
