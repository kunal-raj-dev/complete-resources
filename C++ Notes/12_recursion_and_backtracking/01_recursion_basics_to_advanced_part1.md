# Lecture 42: Recursion Basics: Call Stack, Induction & Recurrence

> **One-Line Purpose:** Master the foundations of recursion by understanding the Principle of Mathematical Induction (PMI), the runtime call stack architecture, and base-case termination invariants.

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
- The formal definition of recursion: a function solving a problem by calling itself with smaller sub-instances.
- The **Principle of Mathematical Induction (PMI)** approach: Base Case, Recursive Assumption (Inductive Hypothesis), and Self-Work.
- The physical mechanics of the **Call Stack** during recursive invocation and unwinding.
- What causes **Stack Overflow** and how to mathematically prove base-case termination.
- Standard recursion problems: Print $N$ to $1$, Print $1$ to $N$, Factorial of $N$, Sum of first $N$ numbers, and Exponentiation ($x^n$).
- The trade-offs between recursion and iteration regarding space overhead, call-frame overhead, and cache locality.

---

## 🔵 Lecture Context

Recursion is the foundational paradigm underpinning advanced algorithms including Divide-and-Conquer (Merge Sort, Quick Sort), Tree Traversals, Backtracking (N-Queens, Sudoku), Graph DFS, and Dynamic Programming. If you cannot trace call frames on the stack, you cannot solve complex algorithmic problems.

---

## 1. Why Recursion Exists & Core Idea

Writing iterative loops requires explicitly managing state transitions and loop invariant variables. However, many real-world and mathematical structures are inherently self-referential or hierarchical (such as trees, directories, and inductive equations).

Recursion decomposes a large problem of size $N$ into identical sub-problems of size $N-1$ (or $N/2$), solves the sub-problem, and composes the final answer with minimal self-work.

### The 3 Core Pillars of Recursion (PMI Framework)
1. **Base Case:** The smallest possible input for which the answer is trivially known without recursive calls. It acts as the mandatory termination condition.
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

## 🧠 Mental Model: The Return-Time Ladder

Notice the crucial difference between performing work *before* the recursive call versus *after* the recursive call:
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

---

## 🧠 Core Intuition — Why Recursion Works

### The Russian Nesting Dolls Analogy
Imagine a set of Russian nesting dolls (Matryoshka). To count them: open the outer doll, count 1, then ask "how many dolls are **inside**?" — the same question on a smaller doll. The smallest doll (base case) answers "1" without opening further. Recursion is exactly this: **delegate the smaller version of your own problem to yourself**.

The key insight: **trust the recursive call**. Once you define what `f(n-1)` returns correctly, your only job is to use that result to build `f(n)`.

### ASCII Stack Frame Visualization: `factorial(3)`

```
CALL PHASE (stack grows down):
┌──────────────────────────────────┐
│ main()                           │  ← bottom
├──────────────────────────────────┤
│ factorial(3): n=3, waits for f(2)│
├──────────────────────────────────┤
│ factorial(2): n=2, waits for f(1)│
├──────────────────────────────────┤
│ factorial(1): n=1, returns 1     │  ← top (base case reached)
└──────────────────────────────────┘

RETURN PHASE (stack unwinds):
factorial(1) returns 1
factorial(2) computes 2 * 1 = 2, returns 2
factorial(3) computes 3 * 2 = 6, returns 6
main() receives 6
```

Each frame contains: `n` (parameter), return address, local variables.

### The Invariant Every Recursive Function Must Maintain
> "If my recursive call solves the problem of size N-1 correctly, then my current frame must correctly solve the problem of size N using that result."

This is the **Principle of Mathematical Induction** recast as a programming paradigm.

---

## 🎯 Pattern Recognition — When to Use Recursion

### Problem Keywords That Signal Recursion
- "Find all possible ..." → Backtracking (enumerate all paths)
- "Divide the problem in half" → Divide & Conquer (binary search, merge sort)
- "Tree / Graph traversal" → DFS (inherently recursive structure)
- "Optimal substructure" → DP (memoized recursion)
- "Generate all subsets / permutations" → Combinatorial recursion

### The 3 Diagnostic Questions for Backtracking
1. **Am I exploring ALL possibilities?** (If yes → use recursion/backtracking)
2. **Can I prune dead branches early?** (If yes → add pruning condition)
3. **Do I need to undo my choice after exploring?** (If yes → it's backtracking, not pure recursion)

### Recursion vs Iteration Decision Matrix
| Scenario | Prefer |
|---|---|
| Problem has self-similar structure (trees, graphs) | Recursion |
| Problem is linear with simple state | Iteration |
| Memory is constrained (embedded systems) | Iteration |
| Code clarity matters more than micro-perf | Recursion |
| Backtracking / combinatorial search | Recursion (mandatory) |

---

## 📐 Head vs Tail Recursion

### Head Recursion (Work BEFORE recursive call)
```cpp
// Work happens on the way DOWN the call stack
void printDecreasing(int n) {
    if (n == 0) return;
    cout << n << " ";   // ← Work FIRST
    printDecreasing(n - 1);  // ← Recursive call AFTER
}
// Output for n=3: 3 2 1
```

### Tail Recursion (Work AFTER recursive call — during unwinding)
```cpp
// Work happens on the way UP (during stack unwinding)
void printIncreasing(int n) {
    if (n == 0) return;
    printIncreasing(n - 1);  // ← Recursive call FIRST
    cout << n << " ";   // ← Work AFTER (return time)
}
// Output for n=3: 1 2 3
```

> [!TIP] **Tail-Call Optimization (TCO):** When the recursive call is the ABSOLUTE LAST thing executed (no computation after it), modern compilers (`-O2`) can replace the call frame with a `jmp` instruction, making it $O(1)$ space. True tail recursion means **no pending computation** after the recursive call returns.

### Converting Recursion to Iteration
Every recursive function can be converted to iterative using an explicit `std::stack`:
```cpp
// Iterative version of postorder DFS using explicit stack
// (Shows what compiler does for you automatically)
stack<int> callStack;
callStack.push(n);
while (!callStack.empty()) {
    int curr = callStack.top(); callStack.pop();
    // process curr
    if (curr > 0) callStack.push(curr - 1);
}
```

---

## 🔧 Universal Backtracking Template

```cpp
// The template every backtracking problem follows:
void backtrack(State& state, Choices& choices, Results& result) {
    // 1. Base Case: Is the current state a complete solution?
    if (isComplete(state)) {
        result.push_back(state);   // Record solution
        return;
    }

    // 2. Iterate over all possible choices at this decision point
    for (auto& choice : choices) {
        if (isValid(state, choice)) {   // 3. Pruning: skip invalid
            makeChoice(state, choice);          // CHOOSE
            backtrack(state, choices, result);  // EXPLORE
            undoChoice(state, choice);          // UN-CHOOSE (BACKTRACK)
        }
    }
}
```

### When to Use `void` vs `bool` Return Type
- **`void`**: Collect ALL solutions (subsets, permutations, combinations).
- **`bool`**: Find ONE solution and stop immediately (Sudoku, N-Queens with early exit, word search).

---

## ⚠️ Common Interview Mistakes — Extended

4. **Stack Overflow on Large N:** Default stack size on Windows is 1MB ≈ ~10,000–50,000 frames. If `n = 100,000`, a linear recursion will crash. Fix: convert to iterative or increase stack size.
5. **Modifying shared state without undoing:** The classic backtracking bug — pushing to `current` and forgetting `pop_back()`. Always use a symmetric push/pop or pass state by value.
6. **Wrong base case direction:** `if (n == 0)` vs `if (n <= 0)` — when N can be negative (e.g., power function with negative exponent), `n == 0` alone misses edge cases.
7. **Return type mismatch:** Forgetting `return` before a recursive call when the function returns a value. `f(n-1)` without `return` discards the result silently.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] What is the base case and why is it absolutely critical?
**Answer:** The base case is the smallest sub-problem that can be solved without further recursion. It is the termination condition. Without a base case (or with an unreachable base case), the call stack grows indefinitely until OS memory is exhausted — a Stack Overflow (signal `SIGSEGV` on Linux, `0xC00000FD` on Windows). Every valid recursive definition must guarantee the parameters converge toward the base case with each call.

---

### Q2: [Conceptual] What is the difference between head and tail recursion? Which is more memory efficient?
**Answer:** Head recursion performs work **before** the recursive call (descending phase); tail recursion performs work **after** the recursive call (ascending/unwinding phase). Tail recursion is more memory-efficient because it enables **Tail-Call Optimization (TCO)**: the compiler reuses the current stack frame for the next call instead of pushing a new frame. This converts $O(N)$ space to $O(1)$ space. However, TCO only applies when the recursive call is the **absolute last** operation — no pending computation may remain after it returns.

---

### Q3: [Conceptual] Can every recursive function be converted to iterative? How?
**Answer:** Yes — unconditionally. Any recursive function can be converted to iterative by simulating the call stack manually using `std::stack<>`. You push parameters onto the stack, process the top element, and push child calls. Post-recursive work (code that runs after the recursive call returns) requires also pushing the pending computation or the intermediate result onto the stack. This is exactly how iterative DFS and tree traversals work.

---

### Q4: [System] What is the maximum safe recursion depth in competitive programming?
**Answer:** On most online judges (Linux, 64MB stack), safe depth is approximately **100,000 to 500,000** frames for simple functions. For functions with large local variables, depth shrinks proportionally. On LeetCode (typically 8MB stack), around **10,000–50,000** simple frames are safe. In Windows competitive environments with 1MB default stack, only ~5,000–10,000 frames are safe. Rule of thumb: if $N > 10^4$ and the algorithm is linearly recursive, prefer iteration.

---

### Q5: [Complexity] What is the space complexity of recursive vs iterative for the same algorithm?
**Answer:** For the **same algorithm**:
- Recursive: $O(\text{depth})$ implicit call stack space, regardless of whether you use explicit data structures
- Iterative: $O(\text{depth})$ explicit stack space if you simulate recursion; $O(1)$ if the algorithm is tail-recursive and loop-convertible

The total work done is identical; the difference is only in how the "stack" is stored (OS call stack vs heap-allocated `std::stack`).

---

### Q6: [Debug] What does the following output? Explain precisely.
```cpp
#include <iostream>
using namespace std;

int mystery(int n) {
    if (n <= 0) return 0;
    return mystery(n - 1) + n;
}

int main() {
    cout << mystery(5) << endl;
    return 0;
}
```
**Answer:** Output is `15`. This is $1 + 2 + 3 + 4 + 5 = 15$. The stack unwinds as: `mystery(0)=0` → `mystery(1)=1` → `mystery(2)=3` → `mystery(3)=6` → `mystery(4)=10` → `mystery(5)=15`. Classic tail-accumulation pattern.

---

### Q7: [Extension] How would you implement a recursive function that avoids stack overflow for very large N?
**Answer:** Two strategies:
1. **Convert to Tail Recursion + TCO:** Move computation into an accumulator parameter so no pending work remains after the recursive call. Example: `factorial(n, acc=1)` where `factorial(0, acc) = acc`.
2. **Explicit Stack (Trampolining):** Replace the function call with a loop that maintains an explicit `std::stack<>`. This moves from OS stack (limited) to heap memory (much larger).

```cpp
// Tail-recursive factorial with accumulator
long long factTail(int n, long long acc = 1) {
    if (n <= 1) return acc;
    return factTail(n - 1, acc * n);  // Pure tail call — TCO eligible
}
```

---

### Q8: [Output Prediction] What is the output of this code?
```cpp
#include <iostream>
using namespace std;

void f(int n) {
    if (n == 0) return;
    f(n / 2);
    cout << n % 2;
}

int main() {
    f(13);
    return 0;
}
```
**Answer:** Output is `1101`. This function prints the binary representation of `n`. The recursive call processes the most-significant bits first (they print on return), and `n % 2` gives the least-significant bit. `13 = 1101₂`.

---

## 📊 Complexity Analysis — Extended Justification

### Why Factorial / Print is $O(N)$ Time and $O(N)$ Space
- **Time:** Exactly $N$ recursive calls, each doing $O(1)$ work → $N \times O(1) = O(N)$.
- **Space:** At peak, all $N$ frames exist simultaneously on the call stack (each frame holds `n` and return address) → $O(N)$.

### Why Optimized Power is $O(\log N)$
- **Time:** Each call halves `n` → $\log_2 N$ calls → $O(\log N)$.
- **Space:** Recursion depth = $\log_2 N$ → $O(\log N)$ stack frames.

### Recursion Tree Node Count Formula
$$\text{Total nodes} = \frac{b^{h+1} - 1}{b - 1} \quad \text{where } b = \text{branching factor}, \; h = \text{height}$$
For $b=2, h=N$: Total = $2^{N+1} - 1 \approx O(2^N)$ (Fibonacci).
For $b=1, h=N$: Total = $N$ (linear recursion).

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Recursion Pattern |
|---|---|---|
| 509 | Fibonacci Number | Base case + dual recursion (bridges to DP) |
| 50 | Pow(x, n) | Divide-and-conquer: `f(n/2) * f(n/2)` |
| 344 | Reverse String | Two-pointer recursion: swap first/last, recurse on middle |
| 70 | Climbing Stairs | Fibonacci variant: $f(n) = f(n-1) + f(n-2)$ |
| 206 | Reverse Linked List | Recursive pointer rewiring |

---

## 🔗 Cross-Topic Connections

- **→ Backtracking (Files 03-09):** Every backtracking algorithm IS recursion + state restoration.
- **→ Dynamic Programming:** Memoized recursion IS DP top-down. Every DP problem starts as a recursive formulation.
- **→ Tree Traversals:** DFS (preorder/inorder/postorder) are direct applications of head/tail recursion.
- **→ Divide & Conquer (Files 10-11):** Merge Sort, Quick Sort use recursion to halve problem size.
- **→ Graph DFS:** Grid/graph traversal uses recursion where the "stack frame" = current node.

---

## ⚡ 2-Minute Revision Flash Card (Enhanced)

- **PMI Framework:** Base Case + Inductive Hypothesis (trust `f(n-1)`) + Self-Work = Correct solution.
- **Head vs Tail:** Work before call = descending (head); work after call = ascending (tail). Tail enables TCO.
- **Space = Stack Depth:** Never the total call count; always the maximum concurrent frames (= tree height).
- **Universal Backtracking:** Choose → Explore → Un-choose. Always restore state before returning.
- **Overflow Threshold:** ~10K frames on Windows (1MB stack); ~100K on Linux (8MB stack).
