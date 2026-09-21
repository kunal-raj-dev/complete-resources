# 💼 Topic Interview Question Bank — Topic 06: Sorting Algorithms

---

### Q1: When is Insertion Sort faster than QuickSort or MergeSort?
**Answer:**
For small arrays ($N \le 16 - 32$) or arrays that are already "nearly sorted", Insertion Sort runs in linear $O(N)$ time with minimal constant factors, zero recursion overhead, and excellent CPU cache locality. This is why standard library implementations (`std::sort`) switch to Insertion Sort for small partitions.

---

### Q2: Why does DNF not increment `mid` when `nums[mid] == 2`?
**Answer:**
When `nums[mid] == 2`, it is swapped with `nums[high]`. The element previously at `high` was in the "unknown" partition `[mid...high]`. Because its value has not yet been inspected, we cannot increment `mid`; it must be evaluated on the subsequent iteration.
