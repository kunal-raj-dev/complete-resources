# ⚡ Topic 07 Revision: C++ Standard Template Library (STL)

> **High-Density Review:** Sequence containers, Associative containers, Unordered containers, Adaptors, Iterators, and Algorithms.

---

## 1. Container Complexity Comparison

| Container | Internal Structure | Access | Insert/Delete Front | Insert/Delete Back | Insert/Delete Middle |
|---|---|---|---|---|---|
| `std::vector` | Contiguous dynamic array | $O(1)$ | $O(N)$ | $O(1)$ amortized | $O(N)$ |
| `std::deque` | Array of fixed-size chunks | $O(1)$ | $O(1)$ | $O(1)$ | $O(N)$ |
| `std::list` | Doubly linked list | $O(N)$ | $O(1)$ | $O(1)$ | $O(1)$ (given iterator) |
| `std::set` / `std::map` | Red-Black Self-Balancing Tree | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ |
| `std::unordered_map` | Hash Table with Buckets | $O(1)$ avg, $O(N)$ worst | $O(1)$ avg | $O(1)$ avg | $O(1)$ avg |

---

## 2. STL Key Algorithms Reference
- **Sorting:** `std::sort(begin, end)` (IntroSort: Hybrid QuickSort + HeapSort + InsertionSort).
- **Binary Search:**
  - `std::lower_bound(begin, end, val)`: First element $\ge val$.
  - `std::upper_bound(begin, end, val)`: First element $> val$.
- **Custom Comparator Rule:** Must establish **Strict Weak Ordering** (`return a < b;`). Returning `<=` causes undefined behavior and segmentation faults!
