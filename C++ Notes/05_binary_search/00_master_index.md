# Topic 05: Binary Search & Divide and Conquer — Master Index

> **Domain:** Logarithmic Search Space Halving, Monotonic Optimization, and Modified Binary Search Patterns

---

## 📋 Topic Overview

This module covers Binary Search from its foundational iterative and recursive formulations to advanced modified variants on non-monotonic, rotated structures, and binary search on answer spaces. Key concepts include overflow-safe midpoint calculations, the half-sorted invariant on rotated arrays, slope gradient analysis on bitonic mountain arrays, index parity tricks, and greedy predicate evaluation for allocation and spacing optimization ($O(\log N)$).

---

## 📑 Lecture Index

| # | Lecture Title | Focus Areas | Notes Link | Status |
|---|---|---|---|---|
| **17** | Binary Search Algorithm (Iterative & Recursive) | Halving intuition, overflow-safe `mid`, recurrence relation, iterative vs recursive | [01_binary_search_iterative_and_recursive.md](./01_binary_search_iterative_and_recursive.md) | **AUDITED** |
| **18** | Search in Rotated Sorted Array | Rotation mechanics, half-sorted invariant, target isolation in sorted half | [02_search_in_rotated_sorted_array.md](./02_search_in_rotated_sorted_array.md) | **AUDITED** |
| **19** | Peak Index in Mountain Array | Bitonic arrays, slope gradients, boundary safety, local peak isolation | [03_peak_index_in_mountain_array.md](./03_peak_index_in_mountain_array.md) | **AUDITED** |
| **20** | Single Element in Sorted Array | Index parity invariant, bitwise XOR partner mapping, duplicate elimination | [04_single_element_in_sorted_array.md](./04_single_element_in_sorted_array.md) | **AUDITED** |
| **21** | Book Allocation Problem | Binary Search on Answer space, monotonic feasibility predicate, contiguous partitioning | [05_book_allocation_problem.md](./05_book_allocation_problem.md) | **AUDITED** |
| **22** | Painter's Partition Problem | Minimizing maximum workload, 64-bit overflow safety, algorithmic isomorphism | [06_painters_partition_problem.md](./06_painters_partition_problem.md) | **AUDITED** |
| **23** | Aggressive Cows Problem | Maximizing minimum separation, greedy cow placement, inverted search space | [07_aggressive_cows_problem.md](./07_aggressive_cows_problem.md) | **AUDITED** |

---

## 🎯 Topic Revision & Interview Preparation
- **Topic Quick Revision:** [topic_revision.md](./topic_revision.md)
- **Topic Interview Question Bank:** [topic_interview_questions.md](./topic_interview_questions.md)

---

## 🗺️ Algorithmic Progression

```
[ Monotonic Sorted Binary Search (L17) ]
                    ↓
[ Rotated Half-Sorted Invariant Search (L18) ]
                    ↓
[ Slope / Gradient Non-Monotonic Peak Search (L19) ]
                    ↓
[ Even-Odd Index Parity Optimization (L20) ]
                    ↓
[ Binary Search on Answer Space: Min-Max (L21-L22) ]
                    ↓
[ Binary Search on Answer Space: Max-Min (L23) ]
```
