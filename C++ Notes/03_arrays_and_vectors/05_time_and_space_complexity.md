# Lecture 12: Time & Space Complexity Analysis

> **One-Line Purpose:** Master asymptotic notations (Big O, Omega, Theta), growth rates, auxiliary space accounting, and the $10^8$ operations rule to deduce optimal algorithm requirements directly from problem constraints.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #12  
> **Video ID:** `PwKv8fOcriM`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=PwKv8fOcriM)  
> **Duration:** 01:25:41  
> **Transcript:** `.transcripts/03_arrays_and_vectors/012_Time___Space_Complexity_-_DSA_Series_by_Shradha_Ma_am.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- Why absolute clock time (seconds) cannot evaluate algorithms, and why operation count scaling is the universal standard.
- The mathematical definitions of Asymptotic Notations: Big O ($O$), Big Omega ($\Omega$), and Big Theta ($\Theta$).
- Hierarchy of Complexity Classes: from $O(1)$ up to $O(N!)$.
- Principles of Asymptotic Simplification: Dropping lower-order terms and constant coefficients.
- The difference between Input Space, Auxiliary Space, and Call Stack Space.
- The **$10^8$ Operations / Second Rule** to predict expected algorithm complexity from input constraints ($N$).

---

## 🔵 Lecture Context

Complexity analysis is the universal language of technical interviews. You are never judged merely on whether your solution produces the correct output—you are evaluated on whether your solution meets the optimal asymptotic time and space bounds.

---

## 1. Why Absolute Time Fails

Execution time measured with a stopwatch or system clock varies based on:
1. CPU clock frequency and architecture.
2. Background OS process contention.
3. Programming language runtime overhead.
4. Compiler optimization flags (`-O2`, `-O3`).

**Asymptotic Analysis** evaluates how the **number of fundamental operations grows** as the input size $N$ approaches infinity ($N \to \infty$).

---

## 2. Asymptotic Notations

> 🔵 **Lecture Content**

```
        Upper Bound: f(N) <= c1 * g(N)  -> Big O (O)
       /
f(N) ─── Tight Bound: c2 * g(N) <= f(N) <= c1 * g(N) -> Big Theta (Θ)
       \
        Lower Bound: f(N) >= c2 * g(N)  -> Big Omega (Ω)
```

| Notation | Formal Meaning | Practical Interview Context |
|---|---|---|
| **Big O ($O$)** | Asymptotic **Upper Bound** | **Worst-Case Performance** (Guaranteed that runtime will not exceed this). |
| **Big Omega ($\Omega$)** | Asymptotic **Lower Bound** | **Best-Case Performance** (Algorithm will take at least this many operations). |
| **Big Theta ($\Theta$)** | Asymptotic **Tight Bound** | **Average-Case / Exact Bound** (Algorithm scales strictly within these bounds). |

---

## 3. Hierarchy of Common Complexity Classes

$$O(1) < O(\log N) < O(\sqrt{N}) < O(N) < O(N \log N) < O(N^2) < O(2^N) < O(N!)$$

```
Operations (f(N))
  ▲
  │                                    / O(N!)
  │                                  / / O(2^N)
  │                                 / / / O(N^2)
  │                                / / / /
  │                               / / / / / O(N log N)
  │                              / / / / / / O(N)
  │                             / / / / / / /
  │                            / / / / / / / / O(log N)
  │───────────────────────────/─/─/─/─/─/─/─/─/─ O(1)
  └───────────────────────────────────────────────────► Input Size (N)
```

### Concrete Examples:
- **$O(1)$ (Constant):** Array indexing (`arr[i]`), basic arithmetic (`a + b`), hash table lookup (average).
- **$O(\log N)$ (Logarithmic):** Binary Search, binary exponentiation (`pow(x, n)`). Each step divides search space by half.
- **$O(N)$ (Linear):** Linear search, Kadane's algorithm, array reversal, single-pass traversals.
- **$O(N \log N)$ (Linearithmic):** Merge Sort, QuickSort (average), Heap Sort.
- **$O(N^2)$ (Quadratic):** Nested loops, Bubble Sort, Selection Sort.
- **$O(2^N)$ (Exponential):** Generating all subsets, naive recursive Fibonacci.
- **$O(N!)$ (Factorial):** Generating all permutations of an array/string.

---

## 4. Space Complexity: Auxiliary vs Input Space

$$\text{Total Space Complexity} = \text{Input Space} + \text{Auxiliary Space}$$

- **Input Space:** Memory required to store the problem input itself (e.g., input array of size $N$ requires $O(N)$ space).
- **Auxiliary Space:** **Extra or temporary memory** allocated by your algorithm to solve the problem (e.g., temporary buffers, hash maps, recursive call stack).
- In interview evaluation, **Auxiliary Space** is what interviewers examine when they ask "Can you do this in $O(1)$ space?".

---

## 5. The $10^8$ Operations Rule (Interview Deduction Blueprint)

> 🔥 **Interview Secret:** Most online judges (LeetCode, Codeforces) and interview environments enforce a **1.0 second time limit**, which corresponds to roughly **$10^8$ basic operations**.

| Input Constraint ($N$) | Allowed Time Complexity | Expected Optimal Approach |
|---|---|---|
| $N \le 10 \dots 12$ | $O(N!)$ | Backtracking, Brute Force Permutations |
| $N \le 20 \dots 25$ | $O(2^N)$ | Bitmasking, Recursive Subsets |
| $N \le 100 \dots 500$ | $O(N^3)$ | 3D Dynamic Programming, Matrix Multiplication |
| $N \le 5,000 \dots 10^4$ | $O(N^2)$ | 2D Dynamic Programming, Two Pointers nested |
| $N \le 10^5 \dots 10^6$ | $O(N \log N)$ or $O(N)$ | Sorting, Binary Search, Kadane, Prefix Sums, Monotonic Stack |
| $N \ge 10^9$ | $O(\log N)$ or $O(1)$ | Binary Search on Answer, Mathematical Formulas |

---

## ⚠️ Common Mistakes

1. **Ignoring Log Base in Big O:** $O(\log_2 N)$ and $O(\log_{10} N)$ differ by a constant multiplier ($\frac{1}{\log_2 10}$). Because constants are dropped, all logarithmic bases belong to $O(\log N)$.
2. **Confusing Worst Case with Big O:** Big O is an upper bound notation, NOT synonymous with worst case. You can have a Big O of the best case ($O(1)$ for linear search best case).

---

## 🔥 Interview Questions

### Q1: What is the Time Complexity of a loop that increments by multiplying: `for (int i = 1; i <= n; i *= 2)`?
- **Short Answer:** $O(\log_2 N)$.
- **Proof:** In iteration $k$, the value of $i$ is $2^k$. The loop terminates when $2^k \ge N \implies k = \log_2 N$.

### Q2: What is the Time Complexity of this nested loop?
```cpp
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= n; j += i) {
        // O(1) work
    }
}
```
- **Short Answer:** $O(N \log N)$.
- **Proof:** The inner loop runs $\frac{N}{i}$ times for each $i$:
  $$\text{Total Steps} = \sum_{i=1}^N \frac{N}{i} = N \left( 1 + \frac{1}{2} + \frac{1}{3} + \dots + \frac{1}{N} \right)$$
  The harmonic series $\sum_{i=1}^N \frac{1}{i} \approx \ln N$. Thus, total operations $= N \ln N = O(N \log N)$.

---

## Key Takeaways

1. **Asymptotics:** Measures operational scalability as $N \to \infty$.
2. **$10^8$ Rule:** $1$ second runtime limit $\approx 10^8$ operations.
3. **Auxiliary Space:** Focus on extra allocated memory and recursive stack depth.

---

## ⚡ 2-Minute Revision

- **Big O:** Upper bound $\le c \cdot g(N)$.
- **Big Omega ($\Omega$):** Lower bound $\ge c \cdot g(N)$.
- **Big Theta ($\Theta$):** Sandwiched tight bound.
- **Rule of Thumb:** $N \le 10^5 \implies O(N \log N)$ or $O(N)$ is required to avoid TLE.
