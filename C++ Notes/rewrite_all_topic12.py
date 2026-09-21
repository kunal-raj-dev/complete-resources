import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t12_dir = os.path.join(root, "12_recursion_and_backtracking")

notes = {}

# 01
notes["01_recursion_basics_to_advanced_part1.md"] = """# Lecture 42: Recursion Basics: Call Stack, Induction & Recurrence

> **One-Line Purpose:** Master the mathematical foundations of recursion via the Principle of Mathematical Induction (PMI), analyze runtime call-stack frame mechanics, and prove base-case termination invariants.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #42  
> **Video ID:** `9OsMG4fI4OY`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=9OsMG4fI4OY)  
> **Duration:** 46:22  
> **Transcript:** `.transcripts/12_recursion_and_backtracking/042_Recursion_Tutorial_-_Basics_to_Advanced___Part_1.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The formal definition of recursion: a function solving a problem by invoking itself on strictly smaller sub-instances.
- The **Principle of Mathematical Induction (PMI)** framework: Base Case, Inductive Hypothesis (Recursive Assumption), and Self-Work.
- The physical mechanics of the **Call Stack** during invocation and unwinding.
- The root causes of **Stack Overflow** and how to prevent unbounded recursion.
- Standard introductory patterns: Printing $N \dots 1$, Printing $1 \dots N$, Factorial ($N!$), Sum of first $N$ numbers, and Exponentiation ($x^n$).
- Memory and execution speed trade-offs between recursion and iteration.

---

## 🔵 Lecture Context

Recursion is the foundational algorithmic paradigm required for Divide-and-Conquer (Merge Sort, Quick Sort), Binary Tree Traversals, Backtracking (N-Queens, Sudoku), Graph DFS, and Dynamic Programming. If you cannot trace call frames on the stack, you cannot solve complex tree or graph interview problems.

---

## 1. Why Recursion Exists & Core Idea

Iterative loops require explicit state management via counter variables and termination conditions. However, many real-world and mathematical structures are inherently self-referential or hierarchical (e.g. tree nodes containing smaller trees, nested directories, mathematical recurrences).

Recursion decomposes a large problem of size $N$ into identical sub-problems of size $N-1$ (or $N/2$), delegates the sub-problem, and composes the final answer with minimal self-work.

### The 3 Core Pillars of Recursion (PMI Framework)
1. **Base Case:** The smallest possible input for which the answer is trivially known without recursive calls. It acts as the mandatory stopping condition.
2. **Recursive Assumption (Leap of Faith):** We assume our recursive function correctly computes the solution for smaller sub-problems (e.g., $N-1$).
3. **Self-Work:** The local computation we must perform to combine the sub-problem's result into the solution for size $N$.

---

## 2. The Internal Memory Engine: The Call Stack

When a function executes in C++, an **Activation Record (Stack Frame)** is pushed onto the thread's call stack. This frame contains:
- Function arguments
- Local variables
- Return address (where control resumes after the function completes)

```
Stack Growth (Calling phase)                Stack Shrinkage (Return/Unwinding phase)
|                                |         |                                |
| printDecreasing(1) [n=1]       |  --->   | (returns and pops frame)       |
| printDecreasing(2) [n=2]       |         | printDecreasing(2) resumes...  |
| printDecreasing(3) [n=3]       |         | printDecreasing(3) resumes...  |
| main()                         |         | main()                         |
+--------------------------------+         +--------------------------------+
```

> ⚠️ **Stack Overflow Invariant:**
> If the base case is missing or unreachable, recursive calls continue indefinitely until the OS stack memory limit (typically 1MB to 8MB) is exhausted, triggering a fatal `SIGSEGV` (Segmentation Fault).

---

## 3. Recursion vs Iteration Comparison

| Metric | Recursion | Iteration (Loops) |
|---|---|---|
| **Definition** | Function calling itself with smaller parameters | Continuous execution of a block until condition fails |
| **Auxiliary Memory** | $O(N)$ stack frames on the call stack | $O(1)$ constant extra space |
| **Execution Speed** | Slower due to call frame setup/teardown | Faster due to direct register manipulation |
| **Code Expressiveness** | Clean, concise for trees, graphs, backtracking | Verbose and complex when managing explicit stacks |

---

## 4. Fundamental Implementations

### Problem 1: Print Numbers from $N$ Down to $1$ (Decreasing)
```cpp
#include <iostream>
using namespace std;

void printDecreasing(int n) {
    // 1. Base Case: Stop at 0
    if (n == 0) {
        return;
    }
    
    // 2. Self-Work: Print current number first
    cout << n << " ";
    
    // 3. Recursive Call: Delegate remaining (n - 1) numbers
    printDecreasing(n - 1);
}
```

### Problem 2: Print Numbers from $1$ Up to $N$ (Increasing)
```cpp
#include <iostream>
using namespace std;

void printIncreasing(int n) {
    // 1. Base Case: Stop at 0
    if (n == 0) {
        return;
    }
    
    // 2. Recursive Call: First print numbers 1 to (n - 1)
    printIncreasing(n - 1);
    
    // 3. Self-Work: Print current number during unwinding (return time)
    cout << n << " ";
}
```

### Problem 3: Factorial of $N$ ($N!$)
```cpp
#include <iostream>
using namespace std;

long long factorial(int n) {
    // Base Case: 0! = 1, 1! = 1
    if (n <= 1) {
        return 1;
    }
    
    // Recurrence: n! = n * (n - 1)!
    return (long long)n * factorial(n - 1);
}
```

### Problem 4: Optimized Power Function ($x^n$)
```cpp
#include <iostream>
using namespace std;

// O(log n) Divide-and-Conquer Power
double powerOptimized(double x, long long n) {
    if (n == 0) return 1.0;
    if (n < 0) {
        x = 1.0 / x;
        n = -n;
    }
    
    double half = powerOptimized(x, n / 2);
    if (n % 2 == 0) {
        return half * half;
    } else {
        return half * half * x;
    }
}
```

---

## 🔍 Detailed Trace: `printIncreasing(3)`

```
1. main() calls printIncreasing(3)
2. printIncreasing(3) calls printIncreasing(2)
3. printIncreasing(2) calls printIncreasing(1)
4. printIncreasing(1) calls printIncreasing(0)
5. printIncreasing(0) hits Base Case (n == 0) -> Returns to printIncreasing(1)
6. printIncreasing(1) prints: 1 -> Returns to printIncreasing(2)
7. printIncreasing(2) prints: 2 -> Returns to printIncreasing(3)
8. printIncreasing(3) prints: 3 -> Returns to main()
Output: 1 2 3
```

---

## 🧠 Mental Model: Top-Down vs Bottom-Up

Notice the difference in execution order:
- **Pre-Recursive Work (Top-Down):** Work is executed on the way **down** the stack (e.g., `printDecreasing`).
- **Post-Recursive Work (Bottom-Up):** Work is executed on the way **up** (during stack unwinding, e.g., `printIncreasing`).

---

## ⚠️ Common Mistakes

1. **Omitting the Base Case:** Leads directly to infinite recursion and stack overflow.
2. **Incorrect Parameter Progression:** Calling `func(n)` instead of `func(n - 1)`, resulting in zero shrinkage toward the base case.
3. **Redundant Duplicate Work:** Computing values twice (e.g. naive Fibonacci without memoization).

---

## 🖥️ System-Specific Notes

- **Default Stack Size:** On Linux systems, the default stack limit is usually 8MB (`ulimit -s`). On Windows MSVC, the default thread stack size is 1MB. Exceeding ~200,000 stack frames on Windows triggers `0xC00000FD (Stack Overflow Exception)`.
- **Tail-Call Optimization (TCO):** If the recursive call is the absolute final statement executed in a function, modern optimizing compilers (`-O2` or `-O3`) can replace the call frame with a jump, converting recursion into $O(1)$ space iteration.

---

## 🟡 Additional Essential Context

Every recursive algorithm can be converted into an iterative algorithm using an explicit `std::stack` data structure. This is how iterative DFS and iterative tree traversals operate in systems where call-stack memory is constrained.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** What is Tail Recursion?  
**A:** A function is tail-recursive if the recursive call is the very last operation performed before returning, meaning no computation is left to be performed after the call returns.

**Q2:** Can modern C++ compilers optimize non-tail recursive functions into loops?  
**A:** Generally no, because the compiler must preserve intermediate state in stack frames to complete the post-recursive computation during stack unwinding.

---

### 🔥 Interview Questions

#### Q1: How do you solve $x^n$ for negative powers and large $n$ without stack overflow?
- **Short Answer:** Convert $n$ to $64$-bit `long long`, invert $x = 1/x$, and use logarithmic halving ($O(\log n)$ recursion depth).
- **Detailed Explanation:** When $n = -2^{31}$, negating $n$ in a 32-bit signed integer causes signed integer overflow because $+2^{31}$ cannot be represented in a 32-bit signed `int` (max is $2^{31}-1$). Storing $n$ in `long long` avoids undefined behavior.
- **Why Interviewers Ask:** Evaluates awareness of boundary limits, data types, and logarithmic complexity.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
#include <iostream>
using namespace std;

void fun(int n) {
    if (n == 0) return;
    cout << n << " ";
    fun(n - 1);
    cout << n << " ";
}

int main() {
    fun(3);
    return 0;
}
```
**Output:** `3 2 1 1 2 3 `  
**Explanation:** The first `cout` executes during stack descent ($3, 2, 1$). The second `cout` executes during stack unwinding ($1, 2, 3$).

---

## Edge Cases

1. **$N = 0$ Input:** Base case must handle $0$ cleanly (e.g. $0! = 1$, power $x^0 = 1$).
2. **Negative $N$:** For factorial, negative inputs are mathematically undefined and must be validated before recursion.

---

## Complexity Analysis

- **Factorial / Print Numbers:** Time $O(N)$, Space $O(N)$ (recursion stack depth).
- **Optimized Power ($x^n$):** Time $O(\log N)$, Space $O(\log N)$.

---

## Key Takeaways

1. **PMI Rule:** Base Case + Inductive Hypothesis + Self-Work = Complete Correctness.
2. **Descent vs Unwinding:** Pre-call code executes top-down; post-call code executes bottom-up.
3. **Stack Discipline:** Recursion always consumes memory proportional to the maximum tree depth.

---

## ⚡ 2-Minute Revision

- Base case is mandatory to prevent stack overflow.
- Time Complexity = (Number of recursive nodes in tree) $\times$ (Work per node).
- Space Complexity = (Maximum depth of the recursion tree).
"""

print("Writing notes...")
for fn, content in notes.items():
    with open(os.path.join(t12_dir, fn), "w", encoding="utf-8") as f:
        f.write(content)
print("Updated 01.")
