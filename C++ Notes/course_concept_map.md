# 🌐 Course Concept Map & Dependency Graph

> **Relational Knowledge Graph:** Visualizing prerequisite pathways, deep concept cross-connections, and real-world interview applications across the course.

---

## 🗺️ Master Dependency Graph

```
[ Problem Solving & Flowcharts ]
              │
              ▼
[ C++ Types, Operators & Memory Layout ] ────────┐
              │                                  │
              ▼                                  │
[ Branching & Loops (Invariants) ]               │
              │                                  │
              ▼                                  │
[ Functions & Call Stack Activation Frames ]     │
              │                                  │
              ├──────────────────────────────┐   │
              ▼                              ▼   ▼
[ Bitwise Operations & 2's Complement ]  [ 1D Contiguous Arrays & Vectors ]
              │                              │
              │                              ▼
              │                     [ Pointer Decay & Addressing ]
              │                              │
              ├──────────────────────────────┼───────────────────────────┐
              ▼                              ▼                           ▼
[ Low-Level Bitmasking ]             [ Pointers & Dynamic Heap ]  [ Binary Search & Halving ]
                                             │                           │
              ┌──────────────────────────────┼───────────────┐           │
              ▼                              ▼               ▼           ▼
[ Singly / Doubly Linked Lists ]     [ Call Stack Recursion ]    [ Rotated / Mountain Search ]
              │                              │
              ▼                              ▼
[ LRU Cache (List + Hash Map) ]      [ Exhaustive Backtracking ]
                                             │
                                             ├───────────────────────────┐
                                             ▼                           ▼
                                     [ Merge Sort & QuickSort ]   [ Trees & Graph DFS ]
                                                                         │
                                                                         ▼
                                                              [ Dynamic Programming (DP) ]
```

---

## 📋 Comprehensive Concept Matrix

| Prerequisite Concept | Core Concept | Dependent Concept | Interview Application |
|---|---|---|---|
| **Memory Addresses** | Variables & Data Types | Pointers (`int*`) | Understanding Stack vs Heap memory allocation. |
| **Bitwise AND / Shifts** | Two's Complement | Bitmasking | $O(1)$ set bit counting, Power of 2 verification. |
| **Contiguous Memory** | Arrays | Two-Pointer Technique | Pair Sum, In-place Reversal, Container With Most Water. |
| **Prefix Accumulation** | Kadane's Algorithm | 1D Dynamic Programming | Maximum Subarray Sum, Circular Subarray Max. |
| **Base Address Arithmetic** | Pointer Decay | Node-based Structures | Array indexing equivalence `arr[i] == *(arr + i)`. |
| **Monotonic Functions** | Binary Search | Search on Rotated Arrays | Logarithmic search space halving in $O(\log N)$. |
| **Gradient Analysis** | Mountain Slope Derivatives | Binary Search on Answer Space | Peak Index, Aggressive Cows, Book Allocation. |
| **Memory Call Stack** | Recursion | Backtracking & Tree Traversals | Activation record depth, base case termination, undoing state. |
| **Non-Contiguous Nodes** | Pointers & Dynamic Memory | Linked Lists | Floyd's Cycle Detection, LRU Cache, Multilevel Flattening. |
| **Divide and Conquer** | Recursion Trees | Merge Sort & Quick Sort | Counting Inversions, stable sorting, partitioning algorithms. |
| **State Trees** | Backtracking | 2D Constraint Solvers | N-Queens, Sudoku Solver, Rat in a Maze. |
| **Overlapping Subproblems** | Recursion + Memoization | Dynamic Programming | Converting exponential $O(2^N)$ trees to polynomial $O(N)$ grids. |

---

## 🔗 Key Cross-Lecture Links

- **Pointers $\to$ Linked Lists:** [Lecture 16 (Pointers)](./04_pointers/01_pointers_in_cpp_in_detail.md) is the absolute prerequisite for [Lecture 57 (Linked List Introduction)](./14_linked_list/01_introduction_to_linked_list.md).
- **Call Stack $\to$ Recursion:** [Lecture 05 (Functions & Call Stack)](./01_cpp_basics/05_functions.md) explains the stack frame mechanics required to trace [Lecture 42 (Recursion Basics)](./12_recursion_and_backtracking/01_recursion_basics_to_advanced_part1.md).
- **Two Pointers $\to$ Binary Search:** [Lecture 08 & 11 (Two Pointers)](./03_arrays_and_vectors/01_array_data_structure_part1.md) provides the boundary narrowing intuition applied in [Lecture 17 (Binary Search)](./05_binary_search/01_binary_search_iterative_and_recursive.md).
- **Prefix Products $\to$ Trapping Rainwater:** [Lecture 15 (Product Except Self)](./03_arrays_and_vectors/08_product_of_array_except_self.md) uses the exact left/right boundary precomputation needed for Stack & Rainwater problems.
