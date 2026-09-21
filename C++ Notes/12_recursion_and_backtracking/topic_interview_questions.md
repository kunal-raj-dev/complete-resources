# Topic 12 Interview Questions: Recursion & Backtracking

> **Curated Question Bank:** FAANG interview questions, recursion tree puzzles, and pruning optimizations.

---

## 📌 Technical Interview Questions

### Q1: [LeetCode 51] How do you optimize N-Queens board safety checking from $O(N)$ to $O(1)$?
- **Short Answer:** Maintain three boolean hash sets (or bit vectors) for:
  1. Columns: `col[c]`
  2. Main Diagonals ($\backslash$): `diag1[r - c + n - 1]`
  3. Anti-Diagonals ($/$): `diag2[r + c]`
- **Explanation:** In an $N \times N$ board:
  - All cells on the same anti-diagonal have a constant sum $r + c$.
  - All cells on the same main diagonal have a constant difference $r - c$ (offset by $+ (n - 1)$ to keep indices positive).
  Checking whether placing a Queen at `(r, c)` is safe becomes three $O(1)$ boolean lookups rather than scanning the board.

---

### Q2: Why is Merge Sort preferred for Linked Lists, while Quick Sort is preferred for Arrays?
- **Short Answer:**
  1. **For Linked Lists:** Merge Sort requires **$O(1)$ auxiliary memory** because nodes can be rewired using pointers without allocating temporary arrays. Moreover, linked lists lack random access ($O(1)$ indexing), making Quick Sort partitioning inefficient.
  2. **For Arrays:** Quick Sort has superior **cache locality**, runs in-place ($O(1)$ extra array memory), and has much lower constant factors than Merge Sort.

---

### Q3: What causes QuickSort to degrade to $O(N^2)$ time, and how can it be prevented in production?
- **Short Answer:** Choosing a bad pivot (e.g. smallest or largest element) on an already sorted or reverse-sorted array.
- **Remedy:**
  1. **Randomized QuickSort:** Choose a random pivot index between `low` and `high`.
  2. **Median-of-Three:** Take the median of `arr[low]`, `arr[mid]`, and `arr[high]`.
  3. **Introsort:** Switch to Heap Sort if recursion depth exceeds $2 \log_2 N$ (used in `std::sort`).
