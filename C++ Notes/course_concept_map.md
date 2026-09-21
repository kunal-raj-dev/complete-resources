# 🌐 Course Concept Map & Dependency Graph

> **Relational Knowledge Graph:** Visualizing prerequisite pathways, deep concept cross-connections, and real-world interview applications across all 16 topics of the course.

---

## 🗺️ Master Dependency Graph

```
[ Problem Solving & Flowcharts (T01) ]
                  │
                  ▼
[ C++ Types, Operators & Memory Layout ] ────────┐
                  │                              │
                  ▼                              │
[ Branching & Loops (Invariants) ]               │
                  │                              │
                  ▼                              │
[ Functions & Call Stack Activation Frames ]     │
                  │                              │
                  ├──────────────────────────────┐   │
                  ▼                              ▼   ▼
[ Bitwise Operations & 2's Complement (T02) ]  [ 1D Contiguous Arrays & Vectors (T03) ]
                  │                              │
                  │                              ▼
                  │                     [ Pointers & Direct Heap (T04) ]
                  │                              │
                  ├──────────────────────────────┼───────────────────────────┐
                  ▼                              ▼                           ▼
[ Number Theory & Sieve (T09) ]         [ Object-Oriented C++ (T13) ]  [ Binary Search Halving (T05) ]
                                                 │                           │
                  ┌──────────────────────────────┼───────────────┐           ▼
                  ▼                              ▼               ▼     [ Sorting & DNF (T06) ]
[ Singly / Doubly Linked Lists (T14) ]   [ Stack / Queues (T15-16) ]   [ Strings & Sliding Windows (T08) ]
                  │                              │                           │
                  ▼                              ▼                           ▼
[ LRU Cache System Design ]              [ Monotonic Invariants ]      [ 2D Matrix Searches (T10) ]
                                                 │                           │
                                                 ▼                           ▼
                                         [ Trees & BSTs (T17-18) ]     [ Hashing & Prefix Sums (T11) ]
                                                 │                           │
                                                 ├───────────────────────────┘
                                                 ▼
                                         [ Recursion & Backtracking (T12) ]
                                                 │
                                                 ▼
                                         [ Graphs & Topologies (T19) ]
                                                 │
                                                 ▼
                                         [ Dynamic Programming & Knapsack (T20) ]
```

---

## 📋 Comprehensive Concept Matrix

| Prerequisite Concept | Core Concept | Dependent Concept | Real-World Application |
|---|---|---|---|
| **Memory Addresses** | Variables & Data Types | Pointers (`int*`) | Stack vs Heap allocation |
| **Bitwise AND / Shifts** | Two's Complement | Bitmasking | $O(1)$ set bit counting & parity flags |
| **Contiguous Memory** | Arrays | Two-Pointer Technique | In-place reversals & DNF partitioning |
| **Prefix Accumulation** | Kadane's Algorithm | 1D Dynamic Programming | Subarray maximization |
| **Monotonic Functions** | Binary Search | Search on Answer Space | Capacity optimization & book allocation |
| **Memory Call Stack** | Recursion | Backtracking & Trees | Exhaustive constraint satisfaction |
| **Non-Contiguous Nodes** | Pointers | Linked Lists | LRU Cache & dynamic memory chains |
| **LIFO Invariants** | Stacks | Monotonic Stacks | Histogram area & stock spanning |
| **FIFO Queues** | Queues | Level-Order & BFS | Shortest paths in unweighted graphs |
| **Tree Hierarchies** | Binary Trees | Binary Search Trees | Logarithmic key retrieval & indexing |
| **Adjacency Graphs** | BFS / DFS | Shortest Paths & MST | Network routing & Dijkstra |
| **Overlapping Subproblems**| Recursion + Memoization | Dynamic Programming | Polynomial resource optimization |
