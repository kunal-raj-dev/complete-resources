# 💼 Topic 06 Interview Question Bank: Sorting Algorithms

> **Curated FAANG Question Bank:** Sorting invariants, stability analysis, in-place partitions, and permutation algorithms.

---

## 📌 Conceptual & Architectural Questions

### Q1: What is a Stable Sort and why does stability matter in real-world systems?
- **Answer:** A sorting algorithm is stable if elements with equal keys maintain their relative original input order in the sorted output. Stability is critical in multi-key sorting (e.g. sorting by Date, then by Price). If the second sort is unstable, the earlier Date ordering is destroyed for items with identical prices.

---

### Q2: Why does DNF sort 0s, 1s, and 2s in a single pass while Counting Sort requires two passes?
- **Answer:** Counting sort computes frequencies in pass 1 and overwrites array values in pass 2. DNF maintains 4 invariant partitions (`[0..low-1]` for 0s, `[low..mid-1]` for 1s, `[mid..high]` for unknown, `[high+1..N-1]` for 2s) and places elements directly via in-place swaps, finishing in a single pass without extra memory.

---

### Q3: Why is QuickSort generally preferred over MergeSort for arrays, but MergeSort preferred for Linked Lists?
- **Answer:**
  - **Arrays:** QuickSort has great cache locality (contiguous memory reads) and in-place $O(1)$ auxiliary space. MergeSort requires allocating an auxiliary array of size $O(N)$, causing memory allocation overhead.
  - **Linked Lists:** MergeSort requires $O(1)$ extra space on linked lists because merging only requires pointer manipulation without memory allocation, whereas QuickSort cannot perform random-access pivot indexing in $O(1)$.
