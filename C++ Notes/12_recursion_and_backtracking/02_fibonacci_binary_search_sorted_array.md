# Lecture 43: Recursion Part 2: Fibonacci, Binary Search & Sorted Array Check

> **One-Line Purpose:** Master multi-branch recursion trees through the Fibonacci sequence, analyze overlapping subproblems, and implement recursive domain reduction for Binary Search and Array Sorted verification.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #43  
> **Video ID:** `4iT-GhvSKzc`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=4iT-GhvSKzc)  
> **Duration:** 41:30  
> **Transcript:** `.transcripts/12_recursion_and_backtracking/043_Recursion_Part_2___Fibonacci_numbers_problem__Binary_search_problem__Find_if_arr.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- How to trace multi-branch recursive functions (Tree Recursion) where a function makes two or more recursive calls.
- The Fibonacci recurrence relation $F(n) = F(n-1) + F(n-2)$ and why naive recursion runs in exponential $O(2^n)$ time.
- How to verify if an array is strictly sorted using linear recursive induction.
- How to implement Binary Search recursively by passing halved search boundaries (`start`, `end`).
- How stack frame memory scales: tree height ($O(N)$ or $O(\log N)$) versus total node count.

---

## 🔵 Lecture Context

In Lecture 42, we explored linear recursion where each call spawned at most one subsequent call. In this lecture, the instructor transitions to **Tree Recursion** (branching factor $\ge 2$). Understanding branching recursion trees is the prerequisite for Divide-and-Conquer (Merge Sort), Backtracking, and Dynamic Programming.

---

## 1. Problem 1: Nth Fibonacci Number

The Fibonacci sequence is defined by:
$$F(0) = 0, \quad F(1) = 1$$
$$F(n) = F(n-1) + F(n-2) \quad 	ext{for } n \ge 2$$

Sequence: $0, 1, 1, 2, 3, 5, 8, 13, 21, 34, \dots$

### C++ Implementation
```cpp
#include <iostream>
using namespace std;

int fibonacci(int n) {
    // Base Cases
    if (n == 0) return 0;
    if (n == 1) return 1;
    
    // Recursive Calls
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
    int n = 6;
    cout << "Fibonacci(" << n << ") = " << fibonacci(n) << "
"; // Output: 8
    return 0;
}
```

### 🌳 Recursion Tree for $n = 4$
```
                    fib(4)
                  /        \
            fib(3)          fib(2)
           /      \        /      \
       fib(2)    fib(1)  fib(1)   fib(0)
      /      \
   fib(1)   fib(0)
```

> ⚠️ **Overlapping Subproblems:**
> Notice that `fib(2)` is evaluated twice independently, and `fib(1)` is evaluated three times. For large $n$, this duplicate work causes exponential $O(2^n)$ runtime, necessitating Dynamic Programming (Memoization).

---

## 2. Problem 2: Check if Array is Strictly Sorted

Given an array of $n$ integers, check if elements are sorted in strictly ascending order: $arr[i] < arr[i+1]$.

### Algorithmic Steps:
1. **Base Case:** If current index `i == n - 1` (last element reached), return `true`.
2. **Self-Work:** If `arr[i] >= arr[i+1]`, the array is unsorted $\implies$ return `false`.
3. **Recursive Call:** Return `isSorted(arr, n, i + 1)`.

### C++ Implementation
```cpp
#include <iostream>
#include <vector>
using namespace std;

bool isSorted(const vector<int>& arr, int n, int i = 0) {
    // Base Case: Reached the last element
    if (i == n - 1) {
        return true;
    }
    
    // Self-Work: Check adjacent pair
    if (arr[i] >= arr[i + 1]) {
        return false;
    }
    
    // Recursive Call for remainder of array
    return isSorted(arr, n, i + 1);
}
```

- **Time Complexity:** $O(N)$ (Visits each element once).
- **Space Complexity:** $O(N)$ auxiliary stack space.

---

## 3. Problem 3: Recursive Binary Search

Binary Search on a sorted array can be cleanly formulated as recursive search-space halving.

### C++ Implementation
```cpp
#include <iostream>
#include <vector>
using namespace std;

int recursiveBinarySearch(const vector<int>& arr, int target, int start, int end) {
    // Base Case: Target not present in search space
    if (start > end) {
        return -1;
    }
    
    int mid = start + (end - start) / 2;
    
    // Target found
    if (arr[mid] == target) {
        return mid;
    }
    
    // Search left half
    if (target < arr[mid]) {
        return recursiveBinarySearch(arr, target, start, mid - 1);
    }
    // Search right half
    else {
        return recursiveBinarySearch(arr, target, mid + 1, end);
    }
}
```

- **Time Complexity:** $O(\log N)$ (Search space halved at each step).
- **Auxiliary Space Complexity:** $O(\log N)$ stack frames.

---

## 🔍 Detailed Trace: Recursive Binary Search

Input: `arr = [2, 4, 6, 8, 10, 12]`, `target = 10`

| Call Frame | `start` | `end` | `mid` | `arr[mid]` | Comparison | Next Action |
|---|---|---|---|---|---|---|
| Frame 1 | 0 | 5 | 2 | 6 | $10 > 6$ | Call `(arr, 10, 3, 5)` |
| Frame 2 | 3 | 5 | 4 | 10 | $10 == 10$ | Match! Return index `4` |

---

## 🧠 Mental Model

- **Linear Recursion (Array Sorted Check):** Behaves like a straight line of dominoes; frame $i$ triggers frame $i+1$.
- **Binary Search Recursion:** A single downward path through a binary search tree.
- **Tree Recursion (Fibonacci):** An exponentially blossoming binary tree where each node branches into two children.

---

## ⚠️ Common Mistakes

1. **Fibonacci Base Case Omission:** Forgetting `n == 0` causes `fib(0)` to call `fib(-1)`, resulting in an immediate stack overflow.
2. **Midpoint Overflow:** Writing `(start + end) / 2` instead of `start + (end - start) / 2`.
3. **Passing Arrays by Value:** Writing `bool isSorted(vector<int> arr)` creates a deep copy of the array on every stack frame ($O(N^2)$ time and memory!). Always pass by `const &`.

---

## 🖥️ System-Specific Notes

- In Recursive Binary Search, stack memory is strictly $O(\log_2 N)$. Even for an array of $10^9$ elements, maximum recursion depth is only $pprox 30$ stack frames ($pprox 1.5	ext{ KB}$), making stack overflow impossible under normal operation.
- In naive Fibonacci, `fib(50)` requires $pprox 2^{50} pprox 10^{15}$ operations, taking weeks to run without memoization.

---

## 🟡 Additional Essential Context

The recursion tree model allows calculating time complexity via the Master Theorem or recurrence tree summation:
- Fibonacci: $T(N) = T(N-1) + T(N-2) + O(1) \implies O(\phi^N) pprox O(1.618^N) pprox O(2^N)$.
- Binary Search: $T(N) = T(N/2) + O(1) \implies O(\log N)$.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why does naive recursive Fibonacci have $O(N)$ space complexity when there are $O(2^N)$ total calls?  
**A:** Because space complexity is governed by the **maximum height of the call stack at any single instant**, not the total number of calls. The stack only holds frames along the current active branch from root to leaf, which is at most $N$ frames deep.

**Q2:** When should you prefer Iterative Binary Search over Recursive Binary Search?  
**A:** In production embedded systems and low-latency environments, iterative binary search is preferred because it runs in $O(1)$ auxiliary space without function-call overhead.

---

### 🔥 Interview Questions

#### Q1: How can you compute the Nth Fibonacci number in $O(\log N)$ time?
- **Short Answer:** Using Matrix Exponentiation.
- **Detailed Explanation:** $egin{pmatrix} F(n+1) & F(n) \ F(n) & F(n-1) \end{pmatrix} = egin{pmatrix} 1 & 1 \ 1 & 0 \end{pmatrix}^n$. By applying binary exponentiation to the transformation matrix, $F(n)$ can be calculated in $O(\log N)$ time and $O(1)$ auxiliary space.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
#include <iostream>
using namespace std;

int countCalls = 0;
int fib(int n) {
    countCalls++;
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);
}

int main() {
    fib(4);
    cout << "Total calls: " << countCalls << "
";
    return 0;
}
```
**Output:** `Total calls: 9`  
**Explanation:** For $n=4$: calls at $n=4$ (1), $n=3$ (1), $n=2$ (2), $n=1$ (3), $n=0$ (2). Total = $1 + 1 + 2 + 3 + 2 = 9$.

---

## Edge Cases

1. **Fibonacci $n = 0, 1$:** Handled by direct base cases.
2. **Array of length $1$ for `isSorted`:** Returns `true` immediately (`0 == n - 1`).
3. **Binary Search with target absent:** Terminates when `start > end` and returns `-1`.

---

## Complexity Analysis

| Problem | Time Complexity | Auxiliary Space Complexity |
|---|---|---|
| Naive Fibonacci | $O(2^N)$ | $O(N)$ (Tree depth) |
| Check Sorted Array | $O(N)$ | $O(N)$ (Call stack) |
| Recursive Binary Search | $O(\log N)$ | $O(\log N)$ (Call stack) |

---

## Key Takeaways

1. **Call Stack Height = Space:** Auxiliary stack memory equals the maximum depth of the active recursion path.
2. **Tree Recursion Danger:** Multi-branch calls without memoization cause exponential $O(2^N)$ explosions.
3. **Pass By Reference:** Always pass large containers by `const &` to avoid hidden $O(N)$ copy overhead per frame.

---

## ⚡ 2-Minute Revision

- Fibonacci recurrence: $F(n) = F(n-1) + F(n-2)$ with base cases $0$ and $1$.
- Binary search recurrence: $T(N) = T(N/2) + O(1) \implies O(\log N)$.
- Pass boundaries `start` and `end` explicitly to keep array slices virtual.

---

## 🧠 Core Intuition — The Bridge from Recursion to DP

### Why Fibonacci Screams for Memoization
Draw the recursion tree for `fib(5)`:
```
                        fib(5)
                      /        \
                fib(4)          fib(3)  ← computed AGAIN!
               /      \        /      \
           fib(3)    fib(2)  fib(2)   fib(1)  ← fib(2) computed 3×!
          /     \
       fib(2)  fib(1)
```
**The insight:** `fib(3)` appears in TWO independent subtrees. Naive recursion recomputes it from scratch both times. This is the definition of **Overlapping Subproblems** — the characteristic that makes Dynamic Programming applicable.

Memoization emerges naturally: *"Before computing `fib(n)`, check if we've already computed it."*

```cpp
// Memoized Fibonacci: O(N) time, O(N) space
#include <vector>
using namespace std;

vector<int> memo(100, -1);  // -1 = not computed yet

int fibMemo(int n) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];  // Cache hit!
    memo[n] = fibMemo(n - 1) + fibMemo(n - 2);  // Cache miss → compute
    return memo[n];
}
```
This converts $O(2^N)$ to $O(N)$ time by ensuring each `fib(k)` is computed exactly once.

### Binary Search Analogy: The Phone Book
Finding a name in a phone book: open to the middle. Is the name before or after? Eliminate half the book. Repeat. At each step, the search space halves: $N \to N/2 \to N/4 \to \dots \to 1$. This takes $\log_2 N$ steps. **Binary search is recursion on a shrinking domain.**

### Why `start + (end - start) / 2` and NOT `(start + end) / 2`
If `start = 2,000,000,000` and `end = 2,000,000,001`, then `start + end = 4,000,000,001` which **overflows** a 32-bit signed integer ($2^{31}-1 \approx 2.1 \times 10^9$). The safe formula avoids this overflow entirely.

---

## 🎯 Pattern Recognition — When You Need This

### Fibonacci Pattern Signals
- Problem has **two or more recursive sub-problems** of smaller size
- Subproblems **overlap** (same `(i, j)` state computed multiple times)
- → **Solution:** Memoize with `map<int,int>` or `vector<int>` indexed by parameter

### Binary Search Pattern Signals  
- Array is **sorted** (or has a monotonic property)
- You can determine which half to discard after one comparison
- Keywords: "find target", "first/last occurrence", "minimum in rotated array"
- → **Key invariant:** `start <= end`; always compute `mid` using safe formula

### isSorted Pattern Signals
- "Check property across entire array"
- Each step checks one pair `(arr[i], arr[i+1])`
- → **Recursion:** Check current pair + assume `isSorted(i+1)` is correct

---

## 🔍 Enhanced Dry Run: Binary Search on Edge Case

Input: `arr = [5]`, `target = 5`, `start = 0`, `end = 0`
```
Call: recursiveBinarySearch(arr, 5, 0, 0)
  mid = 0 + (0 - 0) / 2 = 0
  arr[0] == 5 → target found! Return index 0.
```
Single-element array works correctly because `start > end` is false initially.

Input: `arr = [5]`, `target = 3`, `start = 0`, `end = 0`
```
Call: recursiveBinarySearch(arr, 3, 0, 0)
  mid = 0
  arr[0] = 5 > 3 → search left: recursiveBinarySearch(arr, 3, 0, -1)
  start(0) > end(-1) → BASE CASE: return -1
```

---

## ⚠️ Common Interview Mistakes — Extended

4. **Fibonacci with only `n == 1` base case:** If `n == 0` is not handled separately, `fib(0)` calls `fib(-1)` and `fib(-2)`, causing infinite recursion.
5. **Binary Search: `start = mid` instead of `start = mid + 1`:** When target > arr[mid], if you set `start = mid`, you never eliminate `mid` from the search space. When `start == end == mid`, this loops forever.
6. **isSorted: Wrong base case:** `if (i == n)` should be `if (i == n - 1)`. At `i == n - 1`, there's no `arr[i+1]` to compare — accessing it is undefined behavior.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] Why does naive recursive Fibonacci have $O(N)$ space complexity despite $O(2^N)$ total calls?
**Answer:** Space complexity measures the **maximum memory used simultaneously**, not the total across the program's lifetime. At any instant, the call stack holds only the frames along the current active path from root to the deepest leaf. This path has at most $N$ frames (from `fib(N)` down to `fib(1)` on the leftmost branch). Once `fib(1)` returns, its frame is popped. The right subtree's frames then get pushed on top of the same stack positions. Peak concurrent stack usage = tree height = $N$.

---

### Q2: [Extension] How do you compute Fibonacci in $O(\log N)$ time?
**Answer:** Using **Matrix Exponentiation**.

$$\begin{pmatrix} F(n+1) \\ F(n) \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^n \begin{pmatrix} 1 \\ 0 \end{pmatrix}$$

Apply binary exponentiation to this 2×2 matrix: square it $\log N$ times, then read off $F(n)$. Time: $O(\log N)$, Space: $O(1)$ (just 2×2 matrices).

---

### Q3: [Conceptual] When should you prefer iterative binary search over recursive?
**Answer:** In **production, embedded systems, and performance-critical code**, iterative binary search is preferred because:
1. $O(1)$ auxiliary space (no call stack frames) vs $O(\log N)$ stack frames for recursive.
2. No function-call overhead (stack frame setup, return address storage).
3. Modern CPUs have limited branch prediction buffers; iterative loops are more predictable.

However, recursive binary search is cleaner to reason about and is safer from off-by-one errors in interviews.

---

### Q4: [Output Prediction / Debug] What is wrong with this Fibonacci implementation?
```cpp
int fib(int n) {
    if (n == 1) return 1;  // Only one base case!
    return fib(n - 1) + fib(n - 2);
}
```
**Answer:** Bug: `fib(0)` is not handled. When `fib(2)` calls `fib(0)`, that call computes `fib(-1) + fib(-2)`, and the recursion goes infinitely negative, causing a stack overflow. Fix: add `if (n == 0) return 0;` before the `n == 1` check.

---

### Q5: [Complexity] Prove that the total number of function calls in `fib(N)` is $O(2^N)$.
**Answer:** Let $T(N)$ = total calls made by `fib(N)`. Then:
$$T(N) = T(N-1) + T(N-2) + 1$$
This recurrence has the same form as Fibonacci itself. Since $F(N) \approx \phi^N / \sqrt{5}$ where $\phi = 1.618...$, we get $T(N) = \Theta(\phi^N) = O(2^N)$. Specifically, $T(N) = 2F(N+1) - 1$ (provable by induction).

---

### Q6: [Extension] How does memoization change the total call count?
**Answer:** With memoization, each unique value `fib(k)` for $k = 0, 1, \dots, N$ is computed exactly **once**. The first call to `fib(k)` executes recursively; all subsequent calls return immediately from cache. Total distinct states = $N+1$ → Total calls = $O(N)$. Space = $O(N)$ for the memo table.

---

## 📊 Complexity Analysis — Extended

### Deriving Fibonacci Time Complexity from First Principles
The recurrence $T(N) = T(N-1) + T(N-2) + 1$ has characteristic equation $x^2 = x + 1$ with roots $\phi = (1+\sqrt{5})/2 \approx 1.618$ and $\hat{\phi} = (1-\sqrt{5})/2 \approx -0.618$.

General solution: $T(N) = A\phi^N + B\hat{\phi}^N$. Since $|\hat{\phi}| < 1$, its term vanishes for large $N$, giving $T(N) = \Theta(\phi^N) \approx \Theta(1.618^N) \subset O(2^N)$.

### The Master Theorem for Binary Search
$T(N) = T(N/2) + O(1)$: Here $a=1$, $b=2$, $f(n)=O(1)=O(n^0)$.  
$\log_b a = \log_2 1 = 0$. Since $f(n) = \Theta(n^{\log_b a}) = \Theta(n^0) = \Theta(1)$, Master Theorem Case 2 applies:  
$$T(N) = \Theta(N^{\log_b a} \log N) = \Theta(\log N)$$

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Pattern |
|---|---|---|
| 509 | Fibonacci Number | Direct application; also solve with DP and matrix expo |
| 70 | Climbing Stairs | Fibonacci variant: $f(n) = f(n-1) + f(n-2)$ |
| 704 | Binary Search | Direct recursive binary search application |
| 35 | Search Insert Position | Binary search variant: return `start` when target absent |
| 875 | Koko Eating Bananas | Binary search on answer (monotonic property) |

---

## 🔗 Cross-Topic Connections

- **→ Dynamic Programming:** Memoized Fibonacci IS DP top-down. `fib(n)` with a cache = tabulated DP bottom-up.
- **→ Divide & Conquer (Files 10-11):** Binary search is the simplest divide-and-conquer: discard one half.
- **→ Backtracking (Files 03-09):** Tree recursion (branching factor ≥ 2) is the foundation of all backtracking search.
- **→ Trees:** Recursive tree traversal has the same structure as Fibonacci — left subtree + right subtree + current node work.

---

## ⚡ 2-Minute Revision Flash Card (Enhanced)

- **Fibonacci overlapping subproblems:** `fib(3)` computed multiple times → memoize → $O(2^N)$ becomes $O(N)$.
- **Space ≠ Total Calls:** Space = max stack depth = $N$; total calls = $O(2^N)$.
- **Safe midpoint:** Always `start + (end - start) / 2` to prevent overflow.
- **Binary search invariant:** After each step, `start <= answer_index <= end` is maintained.
- **DP bridge:** Any overlapping-subproblem recursion is a DP problem waiting to be optimized.
