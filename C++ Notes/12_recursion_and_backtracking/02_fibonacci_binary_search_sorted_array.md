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
