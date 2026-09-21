# 💼 Complete C++ & DSA Master Interview Question Bank

> **Long-Term Placement Bank:** High-frequency FAANG interview questions, conceptual traps, system architecture queries, and algorithmic proofs with comprehensive solutions.

---

## 📑 Table of Contents
1. [C++ Fundamentals & Memory Architecture](#1-c-fundamentals--memory-architecture)
2. [Bitwise Operations & Number Systems](#2-bitwise-operations--number-systems)
3. [Arrays, Vectors & Linear Time Techniques](#3-arrays-vectors--linear-time-techniques)
4. [Pointers & Low-Level Memory](#4-pointers--low-level-memory)
5. [Binary Search & Monotonic Optimization](#5-binary-search--monotonic-optimization)
6. [Recursion & Backtracking](#6-recursion--backtracking)
7. [Linked Lists & Cache System Design](#7-linked-lists--cache-system-design)

---

## 1. C++ Fundamentals & Memory Architecture

### Q1.1: Why does `main()` return an `int` rather than `void`?
- **Concept Tested:** ISO C++ Standard compliance, OS process exit codes.
- **Difficulty:** Level 2 (Understanding).
- **Source Lecture:** [Lecture 01](./01_cpp_basics/01_flowchart_and_pseudocode.md)
- **Answer:** The ISO C++ standard specifies that `main()` must return an integer exit status to the calling environment. An exit code of `0` denotes successful execution; any non-zero value represents a specific process failure or exit condition code inspected by parent processes or bash scripts via `$?`.
- **Common Trap:** Writing `void main()` which is accepted by antiquated legacy compilers (like Turbo C++) but rejected by modern conforming compilers (`g++`, `clang++`, `cl`).
- **Follow-up:** What happens if you omit `return 0;` at the end of `main()`?
  - *Answer:* In C++98 and later, if control reaches the end of `main()` without encountering a return statement, the compiler implicitly inserts `return 0;`. This special rule applies *only* to `main()`.

---

### Q1.2: What is the difference between `std::endl` and `'\n'`?
- **Concept Tested:** Stream buffering, I/O performance bottlenecks.
- **Difficulty:** Level 3 (Application / Performance).
- **Source Lecture:** [Lecture 01](./01_cpp_basics/01_flowchart_and_pseudocode.md)
- **Answer:** `'\n'` emits a newline character into the output stream buffer. `std::endl` emits `'\n'` AND explicitly calls `.flush()`, forcing the operating system to flush the buffer to the display or file immediately via an expensive OS system call.
- **Common Trap:** Using `endl` in tight loops printing $10^5$ items, turning an $O(N)$ CPU algorithm into an I/O-bound process that times out.

---

### Q1.3: What is Short-Circuit Evaluation and how does it prevent null-pointer dereferences?
- **Concept Tested:** Boolean operator evaluation order.
- **Difficulty:** Level 3 (Application).
- **Source Lecture:** [Lecture 02](./01_cpp_basics/02_variables_data_types_operators.md)
- **Answer:** In `A && B`, if `A` evaluates to `false`, `B` is guaranteed **never** to be executed. In `A || B`, if `A` evaluates to `true`, `B` is never executed.
- **Defensive Idiom:**
  ```cpp
  if (ptr != nullptr && ptr->val == target) {
      // Safe: ptr->val is never evaluated if ptr is nullptr
  }
  ```
  If `ptr` is `nullptr`, the first condition is `false`, and the right operand (`ptr->val`) is skipped entirely, safely avoiding a segmentation fault.

---

## 2. Bitwise Operations & Number Systems

### Q2.1: How do you verify if an integer $N$ is a Power of 2 in $O(1)$ time?
- **Concept Tested:** Bitmasking, binary representations.
- **Difficulty:** Level 3 (Application).
- **Source Lecture:** [Lecture 07](./02_bitwise_number_systems/02_bitwise_operators_and_modifiers.md)
- **Answer:**
  ```cpp
  bool isPowerOfTwo(int n) {
      return (n > 0) && ((n & (n - 1)) == 0);
  }
  ```
- **Why It Works:** Powers of 2 have exactly one set bit (e.g., $16 = 10000_2$). Subtracting 1 flips that bit to 0 and all lower bits to 1 ($15 = 01111_2$). The bitwise AND between $N$ and $N-1$ produces 0.
- **Common Trap:** Omitting `n > 0`. Without it, `n = 0` or negative values will produce false positives or undefined results.

---

### Q2.2: How does Brian Kernighan's Algorithm count set bits?
- **Concept Tested:** Bit manipulation speedup.
- **Difficulty:** Level 4 (Interview Reasoning).
- **Source Lecture:** [Lecture 07](./02_bitwise_number_systems/02_bitwise_operators_and_modifiers.md)
- **Answer:** It repeatedly clears the least significant set bit using `n &= (n - 1)`. The loop terminates in exactly $k$ iterations, where $k$ is the number of set bits, rather than always looping 32 or 64 times.

---

## 3. Arrays, Vectors & Linear Time Techniques

### Q3.1: How does Kadane's Algorithm achieve $O(N)$ time for Maximum Subarray Sum?
- **Concept Tested:** Dynamic programming prefix optimization.
- **Difficulty:** Level 4 (Interview Reasoning).
- **Source Lecture:** [Lecture 10](./03_arrays_and_vectors/03_kadanes_algorithm_max_subarray.md)
- **Answer:** It maintains a running sum `currSum`. If `currSum` becomes negative, it cannot contribute positively to any subsequent subarray, so `currSum` is discarded and reset to 0.
- **Common Trap:** Initializing `maxSum = 0` instead of `INT_MIN`. If the array contains only negative numbers (e.g. `[-3, -1, -5]`), initializing to 0 returns 0, whereas the correct answer is `-1`.

---

### Q3.2: Why does Boyer-Moore's Voting Algorithm find the Majority Element in $O(1)$ space?
- **Concept Tested:** Pairwise cancellation logic.
- **Difficulty:** Level 4 (Interview Reasoning).
- **Source Lecture:** [Lecture 11](./03_arrays_and_vectors/04_majority_element_moores_voting.md)
- **Answer:** Because the majority element occurs $> \lfloor N/2 \rfloor$ times, even if every instance of a non-majority element cancels out one instance of the majority element, the majority element will remain with a positive count at the end of the pass.
- **Follow-up:** Does Moore's Voting work if no majority element exists?
  - *Answer:* No, it will return a false candidate. You must perform a second linear pass to verify that the candidate's actual frequency strictly exceeds $N/2$.

---

### Q3.3: How do you solve Product of Array Except Self without using the division operator?
- **Concept Tested:** Prefix and suffix accumulation.
- **Difficulty:** Level 4 (Interview Reasoning).
- **Source Lecture:** [Lecture 15](./03_arrays_and_vectors/08_product_of_array_except_self.md)
- **Answer:** Decompose the product into `ans[i] = prefix[i-1] * suffix[i+1]`. First pass accumulates prefix products into the return vector; second pass traverses backwards from $N-1$ using a single running suffix scalar, achieving $O(N)$ time and $O(1)$ extra space.

---

## 4. Pointers & Low-Level Memory

### Q4.1: Why does pointer arithmetic increment by `sizeof(T)` bytes rather than 1 byte?
- **Concept Tested:** CPU memory addressing, data type strides.
- **Difficulty:** Level 3 (Understanding).
- **Source Lecture:** [Lecture 16](./04_pointers/01_pointers_in_cpp_in_detail.md)
- **Answer:** Pointers point to logical elements, not raw individual bytes. When you advance a pointer `ptr++` to point to the next element in an array, the CPU hardware memory controller must advance by the full byte width of that element (`4` bytes for `int`, `8` bytes for `double`) to reach the start of the next contiguous object.

---

### Q4.2: What is the exact difference between `const int* ptr` and `int* const ptr`?
- **Concept Tested:** Constant correctness.
- **Difficulty:** Level 3 (Understanding).
- **Source Lecture:** [Lecture 16](./04_pointers/01_pointers_in_cpp_in_detail.md)
- **Answer:** Read from right to left:
  - `const int* ptr`: Pointer to a constant integer (value at address cannot be changed through `ptr`).
  - `int* const ptr`: Constant pointer to an integer (address stored in `ptr` cannot be changed).

---

## 5. Binary Search & Monotonic Optimization

### Q5.1: Why must midpoint be computed as `start + (end - start) / 2`?
- **Concept Tested:** Signed integer overflow.
- **Difficulty:** Level 3 (Application / Defensive Coding).
- **Source Lecture:** [Lecture 17](./05_binary_search/01_binary_search_iterative_and_recursive.md)
- **Answer:** If `start` and `end` are large integers close to $2 \times 10^9$, `start + end` overflows signed 32-bit `int` into a negative number, resulting in an invalid negative index and a memory crash.

---

### Q5.2: What is the core invariant used in Search in Rotated Sorted Array?
- **Concept Tested:** Invariant preservation in non-monotonic Binary Search.
- **Difficulty:** Level 4 (Interview Reasoning).
- **Source Lecture:** [Lecture 18](./05_binary_search/02_search_in_rotated_sorted_array.md)
- **Answer:** For any midpoint `mid`, at least one of the two halves (`[start...mid]` or `[mid...end]`) is strictly sorted. Check if target lies within the sorted half's bounds; if yes, discard the other half; if no, search the unsorted half.

---

## 6. Recursion & Backtracking

### Q6.1: What is the difference between Subsets I (distinct elements) and Subsets II (duplicate elements)?
- **Concept Tested:** Duplicate pruning in recursion trees.
- **Difficulty:** Level 4 (Interview Reasoning).
- **Source Lecture:** [Lecture 44](./12_recursion_and_backtracking/03_backtracking_subsets_and_subsets_ii.md)
- **Answer:** In Subsets II, the input array is sorted first. When looping through choices at the current recursion level, if `i > idx && nums[i] == nums[i-1]`, we skip `nums[i]` using `continue` to avoid generating identical subset branches.

---

### Q6.2: Why does N-Queens safety checking take only $O(1)$ time with boolean vectors?
- **Concept Tested:** Coordinate geometry mapping in backtracking.
- **Difficulty:** Level 5 (Trap / Optimization).
- **Source Lecture:** [Lecture 46](./12_recursion_and_backtracking/05_n_queens_problem.md)
- **Answer:** Because all squares on a main diagonal have identical $r - c$, and all squares on an anti-diagonal have identical $r + c$. Storing occupied diagonals in boolean hash tables allows $O(1)$ safety verification instead of traversing the 2D board.

---

## 7. Linked Lists & Cache System Design

### Q7.1: Why does an LRU Cache require a Doubly Linked List paired with a Hash Map?
- **Concept Tested:** System design of $O(1)$ composite data structures.
- **Difficulty:** Level 5 (Architecture & Design).
- **Source Lecture:** [Lecture 78 / 12](./14_linked_list/12_lru_cache.md)
- **Answer:**
  - A Hash Map provides $O(1)$ lookup for key-to-node mapping.
  - A Doubly Linked List allows $O(1)$ node removal and insertion at the head (Most Recently Used) because each node has direct pointers to both its `prev` and `next` neighbors. A Singly Linked List cannot delete a node in $O(1)$ because finding the predecessor requires an $O(N)$ traversal.
