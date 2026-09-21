# 💼 Topic 07 Interview Question Bank: C++ Standard Template Library

> **Curated FAANG Question Bank:** Memory allocators, iterator invalidation, comparator contracts, and hash table collisions.

---

## 📌 Conceptual & Architectural Questions

### Q1: What causes Iterator Invalidation in `std::vector` and how do you prevent it?
- **Answer:** When `push_back()` triggers reallocation due to `size() == capacity()`, the entire buffer moves to a new heap address. All existing iterators, pointers, and references become dangling pointers.
- **Prevention:** Call `vec.reserve(expectedSize)` in advance to pre-allocate capacity and prevent reallocations.

---

### Q2: What is the difference between `std::map` and `std::unordered_map`?
- **Answer:**
  - `std::map`: Backed by Red-Black Trees. Elements are stored in sorted order. Operations (`find`, `insert`, `erase`) guarantee $O(\log N)$ worst-case time.
  - `std::unordered_map`: Backed by Hash Tables. Elements are unordered. Operations run in $O(1)$ average time, but can degrade to $O(N)$ in the worst case if all keys collide into the same bucket (e.g. adversarial test cases in competitive programming).

---

### Q3: Why does `std::sort` require a Strict Weak Ordering comparator?
- **Answer:** A comparator `comp(a, b)` must return `false` when `a == b` (irreflexivity). If it returns `true` for equality (e.g. `a <= b`), then `comp(x, x)` is true, violating the mathematical axioms expected by `std::sort`. This causes internal partition loops to skip past boundaries and dereference unallocated memory, resulting in segmentation faults.
