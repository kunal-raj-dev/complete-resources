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

### Q2: Why is Merge Sort preferred for Linked Lists, while Quick Sort is preferred for Arrays?
- **Short Answer:**
  1. **For Linked Lists:** Merge Sort requires **$O(1)$ auxiliary memory** because nodes can be rewired using pointers without allocating temporary arrays. Moreover, linked lists lack random access ($O(1)$ indexing), making Quick Sort partitioning inefficient.
  2. **For Arrays:** Quick Sort has superior **cache locality**, runs in-place ($O(1)$ extra array memory), and has much lower constant factors than Merge Sort.

### Q3: What causes QuickSort to degrade to $O(N^2)$ time, and how can it be prevented in production?
- **Short Answer:** Choosing a bad pivot (e.g. smallest or largest element) on an already sorted or reverse-sorted array.
- **Remedy:**
  1. **Randomized QuickSort:** Choose a random pivot index between `low` and `high`.
  2. **Median-of-Three:** Take the median of `arr[low]`, `arr[mid]`, and `arr[high]`.
  3. **Introsort:** Switch to Heap Sort if recursion depth exceeds $2 \log_2 N$ (used in `std::sort`).

### Q4: Explain the difference between Backtracking and standard Recursion.
- **Answer:** Standard recursion passes state forward or returns a result backward without modifying the global environment. Backtracking explicitly explores a choice by modifying a shared state (e.g., placing a piece on a board, adding an element to a path), recursing, and then **undoing that choice** (restoring the state) before exploring the next option. It is a systematic, depth-first search of the solution space.

### Q5: How does Memoization relate to Backtracking, and when should you use it?
- **Answer:** Backtracking explores all valid paths, often resulting in exponential time $O(2^N)$ or $O(N!)$. If the state space contains **overlapping subproblems** (i.e., we can reach the exact same state via different paths) and we only need the *optimal* path or *count* of paths (not printing every single path), we can cache the results of states to avoid redundant work. This turns Backtracking into Memoized Dynamic Programming, often reducing time complexity to polynomial.

### Q6: Can any recursive function be converted to an iterative one? If so, how?
- **Answer:** Yes, theoretically, every recursive algorithm can be converted into an iterative one by explicitly simulating the call stack using a `std::stack` (or a `while` loop). Variables that would normally be local to a function call are bundled into a struct and pushed onto the stack. For simple "tail-recursive" functions, the conversion is trivial and requires no extra stack space (just updating variables in a `while` loop).

### Q7: What is Tail Recursion, and does C++ optimize for it?
- **Answer:** Tail Recursion occurs when the recursive call is the *very last* operation performed in the function (there is no computation after the call returns). Modern C++ compilers (with `-O2` or `-O3`) optimize tail-recursive functions into `while` loops, reusing the current stack frame and reducing the space complexity from $O(N)$ to $O(1)$, thus preventing Stack Overflow.
### Q8: What is the maximum recursion depth, and what happens if it is exceeded?
- **Answer:** The maximum recursion depth is limited by the size of the call stack allocated by the operating system to the thread (typically 1MB to 8MB). If the recursion goes too deep (e.g., (N)$ depth for  = 10^5$), it exceeds this memory limit, resulting in a **Stack Overflow** error, causing the program to crash. This is why (N)$ depth is dangerous in production without tail-call optimization or explicit iterative stacks.

### Q9: In Backtracking, how do you decide whether to pass the state by value or by reference?
- **Answer:** Passing by value creates a full copy of the state at each recursive step, which simplifies code (no need for explicit undo) but costs (\text{State Size})$ time and space per call. Passing by reference avoids copying, keeping time and space overhead minimal ((1)$ per call), but requires explicitly undoing the change (backtracking) before returning. In performance-critical applications or large states (like boards or arrays), passing by reference with explicit backtracking is strongly preferred.

### Q10: How can Bitmasking optimize Backtracking state?
- **Answer:** When the state represents a small set of boolean choices (e.g., visited nodes in a graph up to 32/64 nodes, or columns in N-Queens), we can use a single 32-bit or 64-bit integer instead of an array or hash set. Marking a state becomes an (1)$ bitwise OR (mask | (1 << i)), checking becomes a bitwise AND (mask & (1 << i)), and unmarking becomes mask & ~(1 << i). This drastically reduces memory overhead and improves CPU cache efficiency.

### Q11: Explain the 'Pruning' technique in Backtracking. Give an example.
- **Answer:** Pruning is the process of terminating a recursive exploration path early when we can provably determine that it cannot lead to a valid or optimal solution. For example, in the Combination Sum problem, if the array is sorted and the current sum exceeds the target, we can immediately stop exploring further additions in that branch. Pruning drastically reduces the size of the search space from theoretical worst-case to practically feasible.

### Q12: How do you identify if a problem can be solved using Recursion or Backtracking?
- **Answer:** Problems that require exploring "all possible configurations", "all permutations", "all combinations", or "all valid paths" are classic backtracking candidates. Key phrases include "find all ways", "generate all valid", or "count the number of valid configurations". If the problem only asks for "the maximum/minimum/optimal" or "is it possible", and has overlapping subproblems, it usually points to Dynamic Programming (which often starts as a recursive backtracking solution).

### Q13: What is the Time and Space Complexity of generating all permutations of a string of length True
- **Answer:** 
  - **Time Complexity:** (N \cdot N!)$. There are !$ permutations, and for each, we might take (N)$ time to process/print/copy it into a result array.
  - **Space Complexity:** (N)$ for the recursion call stack, plus (N \cdot N!)$ if we store all generated permutations in an array/list.

### Q14: Why do we sometimes sort the input array before applying Backtracking?
- **Answer:** Sorting the input array serves two main purposes:
  1. **Deduplication:** It places duplicate elements adjacent to each other. During backtracking, if we see rr[i] == arr[i-1] and we skipped rr[i-1], we can skip rr[i] to avoid generating duplicate combinations/subsets (e.g., in Subsets II or Combination Sum II).
  2. **Early Pruning:** In problems where we accumulate a sum, a sorted array allows us to stop the loop early if the current element causes the sum to exceed the target.

### Q15: Compare DFS (Depth-First Search) and Backtracking. Are they the same?
- **Answer:** They are closely related but conceptually distinct. DFS is an algorithm for traversing or searching tree/graph data structures, marking nodes as visited to avoid cycles. Backtracking is a general algorithmic technique for solving constraint satisfaction problems. Backtracking can be thought of as a DFS on the *implicit state-space graph* of the problem, where edges represent choices and we "unvisit" (backtrack) nodes to explore other choices.
