# 💼 Complete C++ & DSA Master Interview Question Bank

> **Long-Term Placement Bank:** High-frequency FAANG interview questions, conceptual traps, system architecture queries, and algorithmic proofs with comprehensive solutions across all 16 course modules.

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
- **Answer:** ISO C++ standard mandates `main()` return an integer process termination status code to the OS shell. An exit code of `0` denotes success, while non-zero values denote runtime errors.
### Q1.2: What is the performance impact of `std::endl` vs `'\n'`?
- **Answer:** `'\n'` inserts a newline into the stream buffer; `std::endl` inserts `'\n'` AND triggers an explicit hardware flush via an OS system call, degrading loop I/O speed.

---

## 2. Bitwise Operations & Number Systems
### Q2.1: How do you verify if an integer $N$ is a Power of 2 in $O(1)$ time?
- **Answer:** `(n > 0) && ((n & (n - 1)) == 0)`. Powers of 2 possess exactly one set bit; subtracting 1 flips all trailing bits.
### Q2.2: How does Brian Kernighan's Algorithm count set bits?
- **Answer:** `n &= (n - 1)` clears the lowest set bit in each iteration, completing in strictly $O(k)$ operations where $k$ is set bit count.

---

## 3. Arrays, Vectors & Linear Time Techniques
### Q3.1: How does Kadane's Algorithm achieve $O(N)$ time for Maximum Subarray Sum?
- **Answer:** Maintains running sum `currSum`. Any prefix sum dropping below zero is immediately discarded since it reduces subsequent contiguous sums.
### Q3.2: Why does Boyer-Moore's Voting Algorithm achieve $O(1)$ auxiliary space?
- **Answer:** Distinct elements cancel each other in pairs. Since the majority element occurs $> N/2$ times, its count strictly survives all cancellations.

---

## 4. Pointers & Low-Level Memory
### Q4.1: What is Pointer Decay in C++?
- **Answer:** When an array identifier is passed to a function, it implicitly decays into a raw pointer pointing to its first element (`int*`), losing its compiled `sizeof` extent.

---

## 5. Binary Search & Monotonic Optimization
### Q5.1: How do you formulate "Binary Search on Answer Space"?
- **Answer:** Identify an answer domain $[L, R]$ with a monotonic feasibility predicate `isValid(x)`. If value $x$ is valid, all values $> x$ are guaranteed valid (or invalid). Search for the transition boundary in $O(N \log(R - L))$.

---

## 6. Sorting Algorithms & DNF
### Q6.1: Why does DNF sort 0s, 1s, and 2s in a single pass while Counting Sort takes two?
- **Answer:** Counting Sort calculates frequencies then overwrites elements in pass 2. DNF maintains 4 partitioned pointer regions (`low`, `mid`, `high`) and places elements strictly via in-place pointer swaps in one pass.

---

## 7. C++ Standard Template Library
### Q7.1: What is the complexity distinction between `std::map` and `std::unordered_map`?
- **Answer:** `std::map` uses Red-Black Trees guaranteeing $O(\log N)$ worst-case operations with ordered keys. `std::unordered_map` uses hash tables offering $O(1)$ amortized average operations but can degrade to $O(N)$ on heavy hash collisions.

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
- **Answer:** Negative integers destroy the monotonic window expansion property. Prefix sum difference equation $\text{prefix}[j] - \text{prefix}[i] = K$ works universally regardless of signs.

---

## 12. Recursion & Backtracking
### Q12.1: How does Backtracking differ from Brute Force recursion?
- **Answer:** Backtracking prunes dead-end search paths early using constraint predicates before generating illegitimate subtrees, and explicitly un-mutates state upon return.

---

## 13. Object-Oriented Programming
### Q13.1: Why must a base class destructor always be declared `virtual`?
- **Answer:** To prevent resource leaks. Deleting a derived instance via a base pointer with a non-virtual destructor invokes only `~Base()`, skipping derived cleanups.

---

## 14. Linked Lists & Cache System Design
### Q14.1: Why does LRU Cache combine a Doubly Linked List with a Hash Map?
- **Answer:** Doubly Linked List allows $O(1)$ node removal and head insertion once a pointer is known; Hash Map provides $O(1)$ key-to-node lookup.

---

## 15. Stacks & Monotonic Invariants
### Q15.1: Why does the Monotonic Stack run in $O(N)$ despite a nested loop?
- **Answer:** Aggregate amortized analysis: Each array element is pushed onto the stack exactly once and popped at most once, bounding total operations by $2N$.

---

## 16. Queues & Deques
### Q16.1: How does a Monotonic Deque find Sliding Window Maximums in $O(N)$?
- **Answer:** It stores indices whose values are strictly decreasing. Smaller elements at the back are popped whenever a larger value arrives; the front always holds the current window maximum.

---

## 17. Binary Trees & Traversals
### Q17.1: How does Morris Traversal achieve $O(1)$ auxiliary space?
- **Answer:** It temporarily threads the right child of the inorder predecessor back to the current root, eliminating the need for a call stack.

---

## 18. Binary Search Trees
### Q18.1: Why is checking `left < root && right > root` insufficient for BST validation?
- **Answer:** It checks only immediate local children. An invalid BST can have a node in the right subtree smaller than an ancestor. Range bounds `(minAllowed, maxAllowed)` must be propagated down.

---

## 19. Graphs & Network Topologies
### Q19.1: When is Dijkstra's algorithm preferred over Bellman-Ford?
- **Answer:** Dijkstra runs in $O((V + E) \log V)$ for non-negative weights; Bellman-Ford runs in slower $O(V \times E)$ but handles negative weights and detects negative cycles.

---

## 20. Dynamic Programming & Knapsack
### Q20.1: Why must the 1D DP capacity loop in 0/1 Knapsack run in reverse?
- **Answer:** Running capacity $w$ backwards ($W$ down to $wt[i]$) ensures `dp[w - wt[i]]` accesses values from the previous item's row, preventing the same item from being selected multiple times.
