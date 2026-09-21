# Topic 03: Arrays & Vectors — Master Index

> **Domain:** Contiguous Memory Architecture, Dynamic Arrays (`std::vector`), Asymptotic Analysis, and Classical Linear Time Algorithms

---

## 📋 Topic Overview

This module covers 1D contiguous data structures and the foundational linear-time algorithmic patterns that form the core of FAANG coding interviews. Topics include physical memory addressing, pointer decay, vector doubling amortized analysis, Kadane's maximum subarray algorithm, Boyer-Moore's voting algorithm, asymptotic notations ($O, \Omega, \Theta$), binary exponentiation, two-pointer inward scans, and prefix-suffix product accumulation.

---

## 📑 Lecture Index

| # | Lecture Title | Focus Areas | Notes Link | Transcript Link | Status |
|---|---|---|---|---|---|
| **08** | Array Data Structure (Part 1) | Contiguous memory, pointer decay, Linear Search, Two-Pointer Reversal | [01_array_data_structure_part1.md](./01_array_data_structure_part1.md) | [Transcript](../.transcripts/03_arrays_and_vectors/008_Array_Data_Structure_-_Part1___DSA_Series_by_Shradha_Khapra_Ma_am___C__.txt) | **AUDITED** |
| **09** | Vectors in C++ (Arrays Part 2) | Dynamic arrays, size vs capacity, geometric doubling, amortized $O(1)$ | [02_vectors_in_cpp_part2.md](./02_vectors_in_cpp_part2.md) | [Transcript](../.transcripts/03_arrays_and_vectors/009_Vectors_in_C_____Arrays_Part_2___DSA_Series_by_Shradha_Ma_am___Lecture_9.txt) | **AUDITED** |
| **10** | Kadane's Algorithm (Max Subarray Sum) | Subarray vs subsequence, negative sum discard, all-negative edge case | [03_kadanes_algorithm_max_subarray.md](./03_kadanes_algorithm_max_subarray.md) | [Transcript](../.transcripts/03_arrays_and_vectors/010_Kadane_s_Algorithm___Maximum_Subarray_Sum___DSA_Series_by_Shradha_Ma_am.txt) | **AUDITED** |
| **11** | Majority Element & Moore's Voting | Pair sum two pointers, frequency thresholds, pairwise cancellation | [04_majority_element_moores_voting.md](./04_majority_element_moores_voting.md) | [Transcript](../.transcripts/03_arrays_and_vectors/011_Majority_Element___Brute-_Better-Best_Approach___Moore_s_Voting_Algorithm_____Pa.txt) | **AUDITED** |
| **12** | Time & Space Complexity Analysis | Big O/Omega/Theta, hierarchy, $10^8$ ops rule, auxiliary vs input space | [05_time_and_space_complexity.md](./05_time_and_space_complexity.md) | [Transcript](../.transcripts/03_arrays_and_vectors/012_Time___Space_Complexity_-_DSA_Series_by_Shradha_Ma_am.txt) | **AUDITED** |
| **13** | Buy & Sell Stock & Binary Exponentiation | Min-so-far state tracking, `Pow(x, n)`, binary halving, `INT_MIN` safety | [06_buy_sell_stock_and_pow_x_n.md](./06_buy_sell_stock_and_pow_x_n.md) | [Transcript](../.transcripts/03_arrays_and_vectors/013_Buy_and_Sell_Stock_Problem_and_Pow_X_N__Power_exponential_Problem_-_Leetcode___D.txt) | **AUDITED** |
| **14** | Container With Most Water | Two-pointer inward scan, greedy bottleneck proof, $O(N)$ area search | [07_container_with_most_water.md](./07_container_with_most_water.md) | [Transcript](../.transcripts/03_arrays_and_vectors/014_Container_with_Most_Water_Problem___Brute___Optimal_Solution___Two_Pointer_Appro.txt) | **AUDITED** |
| **15** | Product of Array Except Self | Prefix-suffix decomposition without division, $O(1)$ space optimization | [08_product_of_array_except_self.md](./08_product_of_array_except_self.md) | [Transcript](../.transcripts/03_arrays_and_vectors/015_Product_of_Array_Except_Self___Brute_to_Optimal_Solution___Leetcode_238.txt) | **AUDITED** |

---

## 🎯 Topic Revision & Interview Preparation
- **Topic Quick Revision:** [topic_revision.md](./topic_revision.md)
- **Topic Interview Question Bank:** [topic_interview_questions.md](./topic_interview_questions.md)

---

## 🗺️ Algorithmic Pattern Roadmap

```
[ Contiguous Addressing & Pointer Decay (L08) ]
                     ↓
[ Dynamic Heap Vectors & Amortized Doubling (L09) ]
                     ↓
[ Algorithmic Complexity Benchmarks & 10^8 Rule (L12) ]
                     ↓
┌────────────────────┴───────────────────────────┐
▼                                                ▼
[ Prefix State & Greedy Tracking ]      [ Two-Pointer Boundary Scans ]
- Kadane's Max Subarray (L10)           - Pair Sum on Sorted Array (L11)
- Buy & Sell Stock (L13)                - In-place Array Reversal (L08)
- Prefix/Suffix Product (L15)           - Container With Most Water (L14)
- Boyer-Moore Voting (L11)
- Binary Exponentiation (L13)
                     ↓
             Next: Pointers (Topic 04)
```
