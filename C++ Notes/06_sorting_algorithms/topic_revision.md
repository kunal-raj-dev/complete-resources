# ⚡ Rapid Revision — Topic 06: Sorting Algorithms

> **Target:** 5-minute pre-interview refresher on sorting algorithms, complexities, stability, and invariant rules.

---

## 🔑 Quick Comparison Chart

| Algorithm | Best Time | Worst Time | Space | Stable | Key Trick |
|---|---|---|---|---|---|
| **Bubble Sort** | $O(N)$ | $O(N^2)$ | $O(1)$ | Yes | Break if `!isSwapped` |
| **Selection Sort** | $O(N^2)$ | $O(N^2)$ | $O(1)$ | No | Min writes ($N-1$ swaps) |
| **Insertion Sort** | $O(N)$ | $O(N^2)$ | $O(1)$ | Yes | Shift sorted prefix right |
| **DNF Algorithm** | $O(N)$ | $O(N)$ | $O(1)$ | No | `low`, `mid`, `high`; don't advance `mid` on `swap(mid, high)` |
| **Next Permutation**| $O(N)$ | $O(N)$ | $O(1)$ | N/A | Find pivot from right, swap with successor, reverse suffix |
| **Merge Sorted Array**| $O(m+n)$ | $O(m+n)$ | $O(1)$ | Yes | Fill backwards from `m + n - 1` |
