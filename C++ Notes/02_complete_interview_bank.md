# 💼 Complete C++ & DSA Master Interview Question Bank

> **Long-Term Placement Bank:** High-frequency FAANG interview questions, conceptual traps, system architecture queries, and algorithmic proofs with comprehensive solutions across all 20 course modules.

---

## 📑 Table of Contents
1. [C++ Fundamentals & Memory Architecture (Topic 01)](#1-c-fundamentals--memory-architecture)
2. [Bitwise Operations & Number Systems (Topic 02)](#2-bitwise-operations--number-systems)
3. [Arrays, Vectors & Linear Time Techniques (Topic 03)](#3-arrays-vectors--linear-time-techniques)
4. [Pointers & Low-Level Memory (Topic 04)](#4-pointers--low-level-memory)
5. [Binary Search & Monotonic Optimization (Topic 05)](#5-binary-search--monotonic-optimization)
6. [Sorting Algorithms & DNF (Topic 06)](#6-sorting-algorithms--dnf)
7. [C++ Standard Template Library (Topic 07)](#7-c-standard-template-library)
8. [Strings & Sliding Windows (Topic 08)](#8-strings--sliding-windows)
9. [Maths for DSA & Number Theory (Topic 09)](#9-maths-for-dsa--number-theory)
10. [2D Arrays & Matrix Searches (Topic 10)](#10-2d-arrays--matrix-searches)
11. [Hashing & Prefix Sums (Topic 11)](#11-hashing--prefix-sums)
12. [Recursion & Backtracking (Topic 12)](#12-recursion--backtracking)
13. [Object-Oriented Programming (Topic 13)](#13-object-oriented-programming)
14. [Linked Lists & Cache System Design (Topic 14)](#14-linked-lists--cache-system-design)
15. [Stacks & Monotonic Invariants (Topic 15)](#15-stacks--monotonic-invariants)
16. [Queues & Deques (Topic 16)](#16-queues--deques)
17. [Binary Trees & Traversals (Topic 17)](#17-binary-trees--traversals)
18. [Binary Search Trees (Topic 18)](#18-binary-search-trees)
19. [Graphs & Network Topologies (Topic 19)](#19-graphs--network-topologies)
20. [Dynamic Programming & Knapsack (Topic 20)](#20-dynamic-programming--knapsack)

---

## 1. C++ Fundamentals & Memory Architecture
### Q1.1: Why does `main()` return an `int` rather than `void`?
- **Answer:** The ISO C++ standard mandates that `main()` must return an integer exit code to the operating system shell (`0` indicates success, non-zero values denote specific error termination codes). Returning `void` from `main()` is non-standard and rejected by compliant compilers.

### Q1.2: What is the performance impact of `std::endl` vs `'\n'`?
- **Answer:** `'\n'` inserts a newline into the stream output buffer. `std::endl` inserts `'\n'` AND issues an explicit system call to flush the buffer (`WriteFile` / `write`), which causes enormous I/O performance bottlenecks in loops.

### Q1.3: What is Undefined Behavior (UB) in signed integer overflow?
- **Answer:** The C++ standard leaves signed integer overflow strictly undefined. Modern optimizing compilers (GCC/Clang) assume signed overflow never happens and may eliminate safety checks such as `if (x + 1 > x)`.

---

## 2. Bitwise Operations & Number Systems
### Q2.1: How do you verify if an integer $N$ is a Power of 2 in $O(1)$ time?
- **Answer:** `(n > 0) && ((n & (n - 1)) == 0)`. Powers of 2 possess exactly one set bit in binary representation; subtracting 1 flips that bit and sets all lower bits, so their bitwise AND is strictly zero.

### Q2.2: How does Brian Kernighan's Algorithm count set bits?
- **Answer:** `n &= (n - 1)` clears the lowest set bit in each iteration. It completes in strictly $O(k)$ operations where $k$ is the number of set bits.

---

## 3. Arrays, Vectors & Linear Time Techniques
### Q3.1: How does Kadane's Algorithm achieve $O(N)$ time for Maximum Subarray Sum?
- **Answer:** It maintains a running sum `currSum`. Any prefix sum that drops below zero is discarded (`currSum = 0`) because adding a negative sum to any subsequent subarray strictly reduces its value.

### Q3.2: Why does Boyer-Moore's Voting Algorithm achieve $O(1)$ auxiliary space?
- **Answer:** Distinct elements cancel each other in pairs. Because the majority element occurs strictly more than $N/2$ times, its count will strictly survive all pairwise cancellations.

---

## 4. Pointers & Low-Level Memory
### Q4.1: What is Pointer Decay in C++?
- **Answer:** When an array name is passed to a function, it implicitly decays into a pointer pointing to its first element (`int*`), losing its compiled `sizeof` extent and length information.

### Q4.2: What is a Dangling Pointer and how do you prevent it?
- **Answer:** A pointer that references deallocated memory (e.g. stack variable of an exited function or deleted heap memory). Prevent by assigning `ptr = nullptr` immediately after deletion and preferring smart pointers (`std::unique_ptr`, `std::shared_ptr`).

---

## 5. Binary Search & Monotonic Optimization
### Q5.1: How do you formulate "Binary Search on Answer Space"?
- **Answer:** Identify a bounded monotonic search domain $[L, R]$ with a predicate function `isValid(x)`. If value $x$ is feasible, all values $\ge x$ (or $\le x$) are guaranteed feasible. Perform binary search over the answer range in $O(N \log(R - L))$.

### Q5.2: How do you search in a Rotated Sorted Array (LeetCode 33)?
- **Answer:** In any rotated sorted array, the midpoint divides the array such that **at least one half is strictly sorted**. Check if `nums[low] <= nums[mid]`. If yes, the left half is sorted; check if target falls in `[nums[low], nums[mid]]`. Otherwise, the right half is sorted; check if target falls in `[nums[mid], nums[high]]`.

---

## 6. Sorting Algorithms & DNF
### Q6.1: Why does DNF sort 0s, 1s, and 2s in a single pass while Counting Sort takes two?
- **Answer:** Counting Sort counts frequencies in pass 1 then overwrites values in pass 2. DNF maintains 4 partitioned pointer regions (`low`, `mid`, `high`) and places elements via in-place pointer swaps in a single pass without auxiliary memory.

---

## 7. C++ Standard Template Library
### Q7.1: What is the complexity distinction between `std::map` and `std::unordered_map`?
- **Answer:** `std::map` uses Red-Black Trees guaranteeing $O(\log N)$ worst-case operations with sorted key traversal. `std::unordered_map` uses hash tables offering $O(1)$ amortized average operations but can degrade to $O(N)$ on hash collisions.

---

## 8. Strings & Sliding Windows
### Q8.1: How does the fixed-size sliding window solve Permutation in String in $O(N)$?
- **Answer:** Two strings are permutations if and only if their 26-character frequency arrays match. Slide a window of length $|s_1|$ over $s_2$, incrementing incoming and decrementing outgoing characters in $O(1)$ per step.

---

## 9. Maths for DSA & Number Theory
### Q9.1: Why does the Sieve of Eratosthenes inner loop start at $i \times i$?
- **Answer:** Any composite multiple $k \times i$ with $k < i$ has already been marked composite by a smaller prime factor $k$. The earliest unmarked multiple is strictly $i \times i$.

---

## 10. 2D Arrays & Matrix Searches
### Q10.1: Why does Staircase Search start at the top-right corner of a sorted matrix?
- **Answer:** At `(0, C-1)`, moving left strictly decreases values and moving down strictly increases values. This allows a deterministic $O(1)$ elimination of an entire row or column.

---

## 11. Hashing & Prefix Sums
### Q11.1: Why does Subarray Sum Equals K require Hash Maps instead of Two Pointers?
- **Answer:** Negative integers destroy the monotonic window expansion property. The prefix sum frequency equation $\text{prefix}[j] - \text{prefix}[i] = K$ works universally regardless of signs.

---

## 12. Recursion & Backtracking
### Q12.1: What is the difference between Subsets, Permutations, and Combinations?
- **Answer:**
  - **Subsets:** All $2^N$ power set combinations; order does not matter; elements can be included or excluded.
  - **Permutations:** All $N!$ orderings of elements; order matters.
  - **Combinations:** Fixed-size selections of $K$ elements from $N$; order does not matter.

---

## 13. Object-Oriented Programming
### Q13.1: Why must a Base class destructor always be declared `virtual`?
- **Answer:** If a derived class object is deleted through a base class pointer (`delete basePtr;`), declaring `virtual ~Base()` ensures dynamic dispatch correctly invokes `~Derived()` first, preventing memory leaks in the derived class.

---

## 14. Linked Lists & Cache System Design
### Q14.1: How does LRU Cache achieve $O(1)$ `get()` and `put()`?
- **Answer:** By combining a Hash Map (`unordered_map<int, Node*>`) for $O(1)$ key lookup with a Doubly Linked List for $O(1)$ node removal and insertion at the MRU head.

---

## 15. Stacks & Monotonic Invariants
### Q15.1: How does Min Stack achieve $O(1)$ space without a second stack?
- **Answer:** Value encoding: When pushing a value $x < \text{minVal}$, push $2x - \text{minVal}$. Because $x < \text{minVal}$, the stored value is strictly $< x$. When popping, if top $< \text{minVal}$, the previous minimum is restored via $2 \cdot \text{minVal} - \text{top}$.

---

## 16. Queues & Deques
### Q16.1: How does Monotonic Deque achieve $O(N)$ for Sliding Window Maximum?
- **Answer:** Every index enters and leaves the deque at most once across the entire array scan. The aggregate number of operations is bounded by $2N$, guaranteeing amortized $O(1)$ per window.

---

## 17. Binary Trees & Traversals
### Q17.1: How does Morris Traversal achieve $O(1)$ space?
- **Answer:** By using temporary threaded predecessor pointers: point the inorder predecessor's right pointer to current root, then remove the thread on the second visit before moving right.

---

## 18. Binary Search Trees
### Q18.1: Why must Validate BST propagate $(-\infty, +\infty)$ range bounds?
- **Answer:** Checking only local child relationships (`left < root < right`) fails if a node deep in the right subtree is smaller than an ancestor above it. Propagating `(minVal, maxVal)` bounds guarantees global invariant satisfaction.

---

## 19. Graphs & Network Topologies
### Q19.1: Compare Dijkstra, Bellman-Ford, and Floyd-Warshall.
- **Dijkstra:** SSSP on non-negative weighted graphs in $O((V + E) \log V)$ via greedy Min-Heap.
- **Bellman-Ford:** SSSP on graphs with negative weights, detects negative cycles in $O(V \times E)$ via $V-1$ edge relaxations.
- **Floyd-Warshall:** APSP (All-Pairs Shortest Path) in $O(V^3)$ via 3 nested DP loops.

### Q19.2: How does Kahn's algorithm detect directed cycles?
- **Answer:** Nodes in a cycle never reach in-degree 0 and therefore never enter the BFS queue. If `topoOrder.size() < V`, a directed cycle is confirmed.

---

## 20. Dynamic Programming & Knapsack
### Q20.1: Why does 0/1 Knapsack require a reverse capacity loop in 1D DP?
- **Answer:** Iterating backwards ($w = W \dots wt[i]$) ensures $dp[w - wt[i]]$ comes from the previous item row, guaranteeing item $i$ is selected at most once. Forward iteration allows reuse of the same item, which solves Unbounded Knapsack.
