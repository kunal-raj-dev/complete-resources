# Lecture 137: Dynamic Programming Foundations: Memoization & Tabulation

> **One-Line Purpose:** Master the 2 essential properties of Dynamic Programming (Overlapping Subproblems & Optimal Substructure) and transition seamlessly from naive recursion ($O(2^N)$) to Top-Down Memoization ($O(N)$) and Bottom-Up Tabulation ($O(N)$ time, $O(1)$ space).

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #137  
> **Video ID:** `uBA8DkCBdco`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=uBA8DkCBdco)  
> **Duration:** 41:33  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- The two prerequisites for Dynamic Programming: **Optimal Substructure** and **Overlapping Subproblems**.
- The 4-step framework to solve any DP problem:
  1. Define the state (`dp[i]`).
  2. Formulate the recurrence relation.
  3. Identify base cases.
  4. Optimize auxiliary space.
- Top-Down (Memoization) vs Bottom-Up (Tabulation).

---

## 🧠 Core Intuition — Why DP Works

### The Real-World Analogy
Imagine you're climbing a mountain for the second time. On the first trip you mapped every trail junction. On the second trip, instead of re-exploring, you just **look up your map**. That's memoization.

DP is the algorithmic realization of one insight: **"I've solved this exact sub-problem before — don't solve it again."**

### The Two Pillars of DP

**1. Overlapping Subproblems**
A problem has overlapping subproblems if the same subproblem is re-computed multiple times during recursion. Without this property, recursion is already optimal (like Merge Sort — each half is a completely different sub-array, solved exactly once).

> Test: Draw the recursion tree. If any node appears more than once → overlapping subproblems.

**2. Optimal Substructure**
A problem has optimal substructure if an optimal solution to the whole problem can be constructed from optimal solutions to its sub-problems.

> Test: If you know the optimal answer to every sub-problem, can you assemble the optimal answer to the full problem? If yes → optimal substructure exists.

**Both properties must hold** for DP to be applicable.

---

## 🔵 Recursion Tree & Subproblem Overlap
In naive Fibonacci calculation $F(5)$:
```
                    F(5)
              /              \
           F(4)              F(3)
          /    \            /    \
       F(3)    F(2)       F(2)   F(1)
       /  \    /  \       /  \
     F(2) F(1) F(1) F(0) F(1) F(0)
```
$F(3)$ is recalculated 2 times, $F(2)$ is recalculated 3 times! Total calls explode to $O(2^N)$. Storing computed results in a `memo` table reduces total subproblems to strictly $N + 1$.

---

## 🎯 The 4-Step DP Framework (Apply to EVERY Problem)

This framework is the difference between a candidate who fumbles and a candidate who impresses Google interviewers. Apply it religiously.

### Step 1: Define the State — `dp[i]` means what?

This is the hardest and most important step. You must pin down **exactly** what `dp[i]` (or `dp[i][j]` for 2D DP) represents. Be explicit.

| Problem | State Definition |
|---|---|
| Fibonacci | `dp[i]` = the $i$-th Fibonacci number |
| Climbing Stairs | `dp[i]` = number of distinct ways to reach step $i$ |
| House Robber | `dp[i]` = maximum money robbed from houses `[0..i]` |
| 0/1 Knapsack | `dp[i][w]` = max value using first $i$ items with capacity $w$ |

> **Interview tip:** Say "I define `dp[i]` as..." out loud before writing a single line of code. Interviewers reward this.

### Step 2: Formulate the Recurrence Relation

Ask: **"How does the answer to `dp[i]` relate to smaller sub-problems?"**

Think of it as: *If I'm at position $i$, what decisions could have led me here, and which one is optimal?*

Examples:
- Fibonacci: $dp[i] = dp[i-1] + dp[i-2]$ (two possible previous states)
- House Robber: $dp[i] = \max(dp[i-1],\; \text{nums}[i] + dp[i-2])$ (rob or skip)
- 0/1 Knapsack: $dp[i][w] = \max(dp[i-1][w],\; val[i] + dp[i-1][w-wt[i]])$ (include or exclude)

### Step 3: Identify Base Cases

The sub-problems where no smaller sub-problem exists. These are the "seeds" from which all answers grow.

- Fibonacci: $dp[0] = 0,\; dp[1] = 1$
- Climbing Stairs: $dp[1] = 1,\; dp[2] = 2$
- 0/1 Knapsack: $dp[0][w] = 0$ (no items → no value), $dp[i][0] = 0$ (no capacity → no value)

> **Bug trap:** Forgetting edge cases like `n=0` or `n=1` kills candidates. Always handle them explicitly.

### Step 4: Determine Order of Computation & Space Optimize

For tabulation, ensure that when computing `dp[i]`, all values it depends on are already computed. For 1D problems, this usually means left-to-right iteration.

Space optimization: check if `dp[i]` only depends on `dp[i-1]` and `dp[i-2]`. If yes, you only need 2 variables, not an array of size $N$.

---

## 📊 The Evolution: Recursion → Memoization → Tabulation → Space Optimized

Using Fibonacci as the running example:

```
LEVEL 1: NAIVE RECURSION — O(2^N) time, O(N) stack
┌─────────────────────────────────────────┐
│  fib(5)                                 │
│  ├─ fib(4)                              │
│  │  ├─ fib(3)  [computed]               │
│  │  └─ fib(2)  [computed]               │
│  └─ fib(3)  [RECOMPUTED! Wasted work]   │
└─────────────────────────────────────────┘
Problem: exponential recomputation

LEVEL 2: TOP-DOWN MEMOIZATION — O(N) time, O(N) space
┌─────────────────────────────────────────┐
│  memo = [-1, -1, -1, -1, -1, -1]        │
│  fib(5): memo[5]=-1? compute            │
│  fib(4): memo[4]=-1? compute            │
│  fib(3): memo[3]=-1? compute → store 2  │
│  fib(3): memo[3]=2? RETURN 2 instantly! │
│  No recomputation. Each of N+1 states   │
│  computed exactly once.                 │
└─────────────────────────────────────────┘
Drawback: recursive call stack O(N) depth

LEVEL 3: BOTTOM-UP TABULATION — O(N) time, O(N) space
┌─────────────────────────────────────────┐
│  dp[0]=0, dp[1]=1                       │
│  dp[2] = dp[1]+dp[0] = 1               │
│  dp[3] = dp[2]+dp[1] = 2               │
│  dp[4] = dp[3]+dp[2] = 3               │
│  dp[5] = dp[4]+dp[3] = 5               │
│  No recursion! Cache-friendly access.   │
└─────────────────────────────────────────┘
Drawback: O(N) array even if only last 2 needed

LEVEL 4: SPACE-OPTIMIZED — O(N) time, O(1) space
┌─────────────────────────────────────────┐
│  prev2=0, prev1=1                       │
│  i=2: curr=1, prev2=1, prev1=1          │
│  i=3: curr=2, prev2=1, prev1=2          │
│  i=4: curr=3, prev2=2, prev1=3          │
│  i=5: curr=5, prev2=3, prev1=5          │
│  Return prev1=5. ✓                      │
└─────────────────────────────────────────┘
```

---

## 💻 Complete C++ Implementation: All 3 Approaches

```cpp
#include <iostream>
#include <vector>

using namespace std;

class FibonacciProgression {
public:
    // 1. Top-Down Memoization: O(N) Time, O(N) Space (Stack + Memo)
    int memoizationHelper(int n, vector<int>& memo) {
        if (n <= 1) return n;
        if (memo[n] != -1) return memo[n];
        return memo[n] = memoizationHelper(n - 1, memo) + memoizationHelper(n - 2, memo);
    }

    int fibMemo(int n) {
        vector<int> memo(n + 1, -1);
        return memoizationHelper(n, memo);
    }

    // 2. Bottom-Up Tabulation: O(N) Time, O(N) Space (Table only)
    int fibTabulation(int n) {
        if (n <= 1) return n;
        vector<int> dp(n + 1);
        dp[0] = 0;
        dp[1] = 1;

        for (int i = 2; i <= n; ++i) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        return dp[n];
    }

    // 3. Space-Optimized: O(N) Time, O(1) Auxiliary Space
    int fibOptimized(int n) {
        if (n <= 1) return n;
        int prev2 = 0;
        int prev1 = 1;

        for (int i = 2; i <= n; ++i) {
            int curr = prev1 + prev2;
            prev2 = prev1;
            prev1 = curr;
        }
        return prev1;
    }
};

int main() {
    FibonacciProgression fib;
    int n = 10;
    cout << "Fibonacci(" << n << ") via Memoization: " << fib.fibMemo(n) << endl;
    cout << "Fibonacci(" << n << ") via Tabulation:  " << fib.fibTabulation(n) << endl;
    cout << "Fibonacci(" << n << ") Space-Optimized: " << fib.fibOptimized(n) << endl;
    return 0;
}
```

---

## 🎯 Pattern Recognition — DP vs Greedy vs Divide & Conquer

This is one of the most frequently tested distinctions at FAANG interviews.

| Property | DP | Greedy | Divide & Conquer |
|---|---|---|---|
| **Overlapping subproblems** | ✅ Yes — core requirement | ❌ No | ❌ No (disjoint subproblems) |
| **Optimal substructure** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Decision at each step** | Try ALL options, take best | Take locally best, never backtrack | Split, solve independently |
| **Time complexity** | Usually polynomial | Usually $O(N \log N)$ | $O(N \log N)$ via Master Theorem |
| **Examples** | Knapsack, LCS, Edit Distance | Fractional Knapsack, Huffman | Merge Sort, Quick Sort |

### When Does Greedy Fail?
Greedy fails when a locally optimal choice doesn't lead to a globally optimal solution. Classic test:
- **0/1 Knapsack** (W=4): items = {(w=3,v=4), (w=2,v=3), (w=2,v=3)}. Greedy picks item 1 (highest v/w ratio = 4/3 ≈ 1.33), uses capacity 3, gains 4. DP picks items 2+3, gains 6. **Greedy loses.**
- **Fractional Knapsack:** Greedy wins because you can always fill the exact remaining space with a fraction of the next best item.

### The "Is It DP?" Checklist
```
□ 1. Can I define a "state" dp[i] or dp[i][j] with a clear English meaning?
□ 2. Does the optimal answer to dp[i] depend on optimal answers to smaller states?
□ 3. Are the same subproblems computed repeatedly in naive recursion?
□ 4. Does the problem ask for: count / min / max / feasibility (T/F)?
□ 5. Does the problem involve sequences, subsets, or intervals?

If YES to 3+ → Strong DP candidate.
If greedy exchange argument works → Greedy.
If subproblems are completely independent → D&C.
```

---

## 🗂️ Types of Dynamic Programming

### 1. Linear (1D) DP
State depends on a single index. Subproblems form a chain.
- **Examples:** Fibonacci, Climbing Stairs, House Robber, Frog Jump
- **Template:** `dp[i] = f(dp[i-1], dp[i-2], ...)`

### 2. Grid (2D) DP
State depends on two indices (row, col). Classic in matrix problems.
- **Examples:** Unique Paths, Minimum Path Sum, Edit Distance, LCS
- **Template:** `dp[i][j] = f(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`

### 3. Interval DP
State represents an interval `[l, r]`. Subproblems are smaller intervals.
- **Examples:** Matrix Chain Multiplication, Burst Balloons, Palindrome Partitioning
- **Template:** `dp[l][r] = min over k in [l,r-1] of (dp[l][k] + dp[k+1][r] + cost)`
- **Order:** Iterate by interval length (small to large)

### 4. Partition / Subset DP
State tracks a running sum or selection from a set.
- **Examples:** 0/1 Knapsack, Subset Sum, Partition Equal Subset Sum, Count of Subsets
- **Template:** `dp[i][w] = dp[i-1][w] || dp[i-1][w - nums[i]]`

### 5. Bitmask DP
State encodes a subset using a bitmask integer. Used when $N \leq 20$.
- **Examples:** Traveling Salesman Problem, Assignment Problem
- **Template:** `dp[mask][i]` = optimal cost when the set represented by `mask` has been visited and we're at node `i`
- **Complexity:** $O(2^N \cdot N)$

### 6. Tree DP
DP on tree structures. State at each node depends on its children.
- **Examples:** Diameter of Tree, Max Independent Set on Tree
- **Template:** Post-order DFS, combine children's dp values at each node

---

## ⚠️ Common Interview Mistakes

1. **Wrong state definition:** The #1 cause of incorrect DP solutions. If `dp[i]` isn't crystal clear, the recurrence will be wrong.
2. **Forgetting base cases:** Always ask: "What's the smallest sub-problem I can answer without recursion?" Handle `n=0` and `n=1` explicitly.
3. **Wrong iteration order in tabulation:** If `dp[i]` depends on `dp[i+1]` (suffix DP), iterate right-to-left. Iterating left-to-right will use uncomputed values.
4. **Forward loop in 0/1 Knapsack 1D optimization:** Using `w = wt[i]...W` makes it Unbounded Knapsack (item used multiple times). Must iterate `w = W...wt[i]`.
5. **Stack overflow with memoization on $N = 10^5$:** Recursion depth of $10^5$ → stack overflow on most systems. Switch to tabulation.
6. **Integer overflow:** `dp[i]` can grow beyond `int` range for count problems. Use `long long`.

---

## ⏱️ Complexity Comparison

| Method | Time Complexity | Auxiliary Space | Call Stack Overhead |
|---|---|---|---|
| **Naive Recursion** | $O(2^N)$ | $O(N)$ (call stack) | Heavy recursion |
| **Top-Down Memoization** | $O(N)$ | $O(N)$ (table + stack) | $O(N)$ recursion depth |
| **Bottom-Up Tabulation** | $O(N)$ | $O(N)$ (table only) | Zero call stack |
| **Space-Optimized DP** | $O(N)$ | $O(1)$ (2 variables) | Zero call stack |

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] What is pseudo-polynomial time? Why is 0/1 Knapsack NP-complete despite running in $O(NW)$?
**Answer:**
Polynomial time means polynomial in the **size of the input** (number of bits to encode it). The input to 0/1 Knapsack is:
- $N$ items: $O(N \log V_{max} + N \log W_{max})$ bits
- Capacity $W$: $O(\log W)$ bits

The algorithm runs in $O(N \cdot W)$ steps. But $W$ itself can be exponential in the number of bits used to encode it: if $W$ is encoded in $B = \log_2 W$ bits, then $W = 2^B$. So the true complexity is $O(N \cdot 2^B)$, which is **exponential in the input size**. We call $O(NW)$ pseudo-polynomial because it's polynomial in the *value* of $W$, not its bit-length. This distinction is why knapsack remains NP-complete: no polynomial-time algorithm (in terms of bit-length of input) is known.

---

### Q2: [Conceptual] Memoization vs Tabulation — which is faster in practice?
**Answer:**
Theoretically both are $O(N)$. In practice:
- **Tabulation** is often faster due to: (a) no function call overhead, (b) cache-friendly sequential memory access, (c) no risk of stack overflow.
- **Memoization** can be faster when: (a) the state space is sparse and only a small fraction of states need computation (e.g., grid with obstacles where many cells are unreachable), (b) lazy evaluation avoids computing states that are never needed.

Rule of thumb: **default to tabulation** for competitive programming and interviews. Use memoization when the recurrence has complex branching that makes ordering hard to determine.

---

### Q3: [Conceptual] How do you identify that a problem is solvable by DP?
**Answer:** Look for these signals:
1. **Keywords:** minimum, maximum, count, ways, possible/feasible, longest, shortest
2. **Structure:** the problem involves making a sequence of choices (include/exclude, move left/right/diagonal)
3. **Overlapping subproblems:** naive recursion recomputes the same sub-problem for different call paths
4. **Optimal substructure:** the optimal answer uses optimal answers to sub-problems (verify with cut-and-paste argument)
5. **Constraints hint:** $N \leq 10^3$ → possible $O(N^2)$ DP; $N \leq 10^2$ → possible $O(N^3)$ DP; $N \leq 20$ → possible $O(2^N \cdot N)$ bitmask DP

---

### Q4: [Proof] What is optimal substructure? Prove it with the cut-and-paste argument.
**Answer:**
**Definition:** A problem exhibits optimal substructure if an optimal solution to the problem contains optimal solutions to its subproblems.

**Cut-and-Paste Proof (by contradiction):**
Let $OPT$ be an optimal solution to problem $P$. Suppose $OPT$ contains a sub-solution $s$ to sub-problem $p$. Assume for contradiction that $s$ is not optimal for $p$, i.e., there exists a better solution $s^*$ for $p$. Now "cut" $s$ out of $OPT$ and "paste" $s^*$ in its place. The resulting solution is still feasible (same structure) but achieves a strictly better objective value than $OPT$. This contradicts our assumption that $OPT$ was optimal. Therefore, $s$ must be optimal for $p$. $\square$

**Counterexample (no optimal substructure):** Longest path in a general graph. The longest path from $u \to v$ might NOT contain the longest path from $u \to w$ (intermediate node), because cycles can be exploited differently.

---

### Q5: [Conceptual] What is the difference between DP and Divide & Conquer?
**Answer:**

| Property | DP | Divide & Conquer |
|---|---|---|
| Subproblem overlap | YES — same sub-problem recurs | NO — sub-problems are disjoint |
| Memoization needed | Yes (avoids recomputation) | No (each sub-problem solved once) |
| Example | Fibonacci, Knapsack | Merge Sort, Quick Sort |
| Information flow | Bottom-up or top-down, with caching | Strictly top-down |

Key insight: Both break problems into sub-problems. The difference is that D&C sub-problems are *independent*, while DP sub-problems *share* smaller sub-problems (hence "overlapping"). Fibonacci is classified as DP, not D&C, because $F(5)$'s two sub-problems $F(4)$ and $F(3)$ both depend on $F(3)$, $F(2)$, $F(1)$ — shared sub-problems.

---

### Q6: [Extension] How do you handle DP with multiple parameters?
**Answer:**
When a state depends on multiple parameters (e.g., 2D DP for knapsack), use a 2D array `dp[i][j]` or, equivalently, a 1D array if one dimension can be eliminated via space optimization.

Steps:
1. Identify all parameters that fully define a sub-problem (these become your state dimensions)
2. Ensure the recurrence direction is correct in each dimension
3. For space optimization: eliminate one dimension if the recurrence only uses the "previous row"

Example — Edit Distance: state `dp[i][j]` = min edits to convert `s1[0..i-1]` to `s2[0..j-1]`. Recurrence uses `dp[i-1][j]`, `dp[i][j-1]`, `dp[i-1][j-1]`. Can be reduced to two 1D arrays (current and previous row).

For $K$ parameters: the state space is $O(S_1 \times S_2 \times \cdots \times S_K)$. If this is too large, look for problem-specific optimizations (e.g., divide-and-conquer optimization, convex hull trick).

---

### Q7: [Output Prediction] What does this memoization code output? Find the bug.
```cpp
int fib(int n, vector<int>& memo) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];
    memo[n] = fib(n-1, memo) + fib(n-2, memo);
    return fib(n, memo); // BUG: calls fib again instead of returning memo[n]
}
```
**Answer:** This code is functionally correct (not infinite loop) because `memo[n]` is already set, so `fib(n, memo)` just returns `memo[n]`. But it's wasteful — one unnecessary function call per invocation. The fix is `return memo[n];` directly after the assignment line. This is a subtle bug that wastes a stack frame but doesn't affect correctness.

---

### Q8: [Extension] How would you extend Fibonacci DP to handle very large $N$ (e.g., $N = 10^{18}$) efficiently?
**Answer:**
The $O(N)$ tabulation breaks down at $N = 10^{18}$ (would take ~$10^{18}$ iterations). The solution is **matrix exponentiation** to compute the $N$-th Fibonacci in $O(\log N)$ time.

The recurrence $F(n) = F(n-1) + F(n-2)$ can be expressed as:
$$\begin{pmatrix} F(n+1) \\ F(n) \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^n \begin{pmatrix} 1 \\ 0 \end{pmatrix}$$

Compute the matrix power in $O(\log N)$ using fast exponentiation (repeated squaring). This technique generalizes to any linear recurrence.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Insight |
|---|---|---|
| 70 | Climbing Stairs | Direct Fibonacci application |
| 198 | House Robber | 1D DP with pick/skip decision |
| 213 | House Robber II | Circular → two linear passes |
| 322 | Coin Change | Unbounded knapsack variant (forward loop) |
| 1143 | Longest Common Subsequence | Classic 2D DP grid |
| 312 | Burst Balloons | Interval DP |
| 416 | Partition Equal Subset Sum | Subset-sum knapsack |

---

## 🔗 Cross-Topic Connections

- **Graphs:** Shortest path (Bellman-Ford) is DP on a graph. Floyd-Warshall is 2D DP.
- **Trees:** Tree DP (e.g., diameter, max independent set) uses post-order DFS with DP at each node.
- **Greedy:** DP is the fallback when greedy fails. Always attempt greedy first — it's simpler. If exchange argument fails, switch to DP.
- **Divide & Conquer Optimization:** When the DP recurrence $dp[i][j]$ has a monotone optimal split point, D&C can speed it up from $O(N^3)$ to $O(N^2 \log N)$.
- **Segment Trees / BIT:** Used to speed up DP transitions from $O(N)$ per state to $O(\log N)$ per state (e.g., LIS in $O(N \log N)$).

---

## ⚡ 2-Minute Revision Flash Card

- **DP = Memoized Recursion = Smart Brute Force:** Solve each sub-problem exactly once.
- **Two requirements:** Overlapping Subproblems + Optimal Substructure. Both MUST hold.
- **4-Step Framework:** (1) Define state, (2) Write recurrence, (3) Base cases, (4) Space optimize.
- **Memoization vs Tabulation:** Both $O(N)$; tabulation avoids stack overflow, memoization skips unneeded states.
- **Forward loop = Unbounded Knapsack; Backward loop = 0/1 Knapsack.** This one rule prevents 80% of knapsack bugs.
