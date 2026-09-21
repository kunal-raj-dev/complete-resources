# ⚡ Topic 10 Revision: 2D Arrays & Matrix Searches

> **High-Density Review:** Row-Major layout, Staircase matrix search, Spiral matrix boundaries, and Transpose math.

---

## 1. Memory Architecture: Row-Major Order
In C++, 2D arrays are stored as a flat 1D sequence in Row-Major order:
$$\text{Address}(r, c) = \text{Base} + (r \times \text{cols} + c) \times \text{sizeof(Type)}$$
- Traversing rows first (`for r ... for c`) has optimal cache spatial locality.
- Traversing columns first (`for c ... for r`) causes cache line thrashing.

---

## 2. Matrix Search Comparison

| Matrix Property | Algorithm | Time Complexity | Auxiliary Space |
|---|---|---|---|
| Entire matrix flattened sorted | Binary Search | $O(\log(R \times C))$ | $O(1)$ |
| Rows sorted & Cols sorted | Staircase Search (Top-Right) | $O(R + C)$ | $O(1)$ |
| Unsorted Matrix | Linear Scan | $O(R \times C)$ | $O(1)$ |
