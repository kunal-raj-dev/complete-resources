# Lecture 138: DP 2: Climbing Stairs (LeetCode 70)

> **One-Line Purpose:** Count total distinct ways to climb a staircase of $N$ steps when you can take either 1 or 2 steps at a time, formulating the fundamental 1D Fibonacci recurrence.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #138  
> **Video ID:** `3GzA0mz6wp0`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=3GzA0mz6wp0)  
> **Duration:** 26:26  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Understanding State Definition: `ways(n)` = ways to reach step $n$.
- Identifying the last move: To land on step $n$, you must have jumped from step $n-1$ (1 step) OR from step $n-2$ (2 steps).
- Deriving the recurrence relation: `ways(n) = ways(n - 1) + ways(n - 2)`.
- Base case identification: `ways(1) = 1`, `ways(2) = 2`.

---

## 🧠 Core Intuition — Why This IS Fibonacci

### The Mental Model
Think of a staircase as a series of **decisions**. At every step, you choose: "Did I just take 1 step, or 2?" Working backwards from step $n$:
- If the last move was **1 step**, you were at step $n-1$ → add all ways to reach $n-1$
- If the last move was **2 steps**, you were at step $n-2$ → add all ways to reach $n-2$

This is exactly the Fibonacci recurrence! The insight is that **counting ways is additive**: when there are two mutually exclusive last-moves, the total count is their sum.

```
         [n]
         / \
     [n-1] [n-2]    ← Two ways to arrive at step n
       /\     /\
  [n-2][n-3][n-3][n-4]   ← Each sub-problem branches again
```

### The Explosion: Why Naive Recursion is O(2^N)

For `climbStairs(5)`, the recursion tree looks like:
```
                        ways(5)
                    /           \
              ways(4)           ways(3)
             /      \          /      \
         ways(3)  ways(2)  ways(2)  ways(1)
         /    \
     ways(2) ways(1)
```
`ways(3)` is computed TWICE, `ways(2)` is computed THREE times. The tree has $O(2^N)$ nodes. For $N = 45$ (LeetCode constraint), that's over 35 billion calls!

---

## 🔵 Algorithmic Intuition & Dry Run

```
Stairs:
Level 0 (Ground)
Level 1: [1] -> 1 way
Level 2: [1+1, 2] -> 2 ways
Level 3: from Level 2 (1 step) + from Level 1 (2 steps) = 2 + 1 = 3 ways
Level 4: from Level 3 + from Level 2 = 3 + 2 = 5 ways
Level 5: 5 + 3 = 8 ways
```

This sequence `1, 2, 3, 5, 8, 13, ...` IS Fibonacci, shifted by 1: `ways(N) = Fib(N+1)` where `Fib(1)=1, Fib(2)=1, Fib(3)=2, ...`

---

## 📐 The 4-Step DP Framework Applied

**Step 1: State Definition**
`dp[i]` = number of distinct ways to reach step $i$ from step 0.

**Step 2: Recurrence Relation**
$$dp[i] = dp[i-1] + dp[i-2]$$
Because the last jump to step $i$ was either from step $i-1$ (took 1 step) or step $i-2$ (took 2 steps).

**Step 3: Base Cases**
- $dp[1] = 1$ (only way: take one 1-step jump)
- $dp[2] = 2$ (two ways: {1,1} or {2})

**Step 4: Order & Space**
Compute left-to-right. Since $dp[i]$ only depends on $dp[i-1]$ and $dp[i-2]$, reduce to $O(1)$ space with two rolling variables.

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <unordered_map>

using namespace std;

class SolutionClimbingStairs {
public:
    // Approach 0: Naive Recursion - O(2^N) Time, O(N) Stack (TLE for large N)
    int climbStairsRecursive(int n) {
        if (n <= 2) return n;
        return climbStairsRecursive(n - 1) + climbStairsRecursive(n - 2);
    }

    // Approach 1: Top-Down Memoization - O(N) Time, O(N) Space
    int climbStairsMemo(int n, unordered_map<int, int>& memo) {
        if (n <= 2) return n;
        if (memo.count(n)) return memo[n];
        return memo[n] = climbStairsMemo(n - 1, memo) + climbStairsMemo(n - 2, memo);
    }
    int climbStairsMemoized(int n) {
        unordered_map<int, int> memo;
        return climbStairsMemo(n, memo);
    }

    // Approach 2: Bottom-up Tabulation - O(N) Time, O(N) Space
    int climbStairsTabulation(int n) {
        if (n <= 2) return n;

        vector<int> dp(n + 1);
        dp[1] = 1;
        dp[2] = 2;

        for (int i = 3; i <= n; ++i) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }

        return dp[n];
    }

    // Approach 3: Optimal Space - O(N) Time, O(1) Space
    int climbStairs(int n) {
        if (n <= 2) return n;

        int prev2 = 1; // ways(1)
        int prev1 = 2; // ways(2)

        for (int i = 3; i <= n; ++i) {
            int curr = prev1 + prev2;
            prev2 = prev1;
            prev1 = curr;
        }

        return prev1;
    }

    // EXTENSION: K-Step Generalization — can take 1 to K steps
    // dp[i] = sum of dp[i-1] + dp[i-2] + ... + dp[i-K]
    // O(N*K) time, O(K) space using sliding window sum
    int climbStairsKSteps(int n, int k) {
        vector<int> dp(n + 1, 0);
        dp[0] = 1; // 1 way to stay at ground
        for (int i = 1; i <= n; ++i) {
            for (int j = 1; j <= k && j <= i; ++j) {
                dp[i] += dp[i - j];
            }
        }
        return dp[n];
    }

    // EXTENSION: Tribonacci (1, 2, or 3 steps at a time) — O(N) Time, O(1) Space
    int climbStairsTribo(int n) {
        if (n <= 2) return n;
        if (n == 3) return 4; // {1,1,1}, {1,2}, {2,1}, {3}
        int a = 1, b = 2, c = 4;
        for (int i = 4; i <= n; ++i) {
            int curr = a + b + c;
            a = b; b = c; c = curr;
        }
        return c;
    }
};

int main() {
    SolutionClimbingStairs solver;
    cout << "Ways to climb 5 stairs: " << solver.climbStairs(5) << endl; // Output: 8
    cout << "Ways to climb 5 stairs (up to 3 steps): " << solver.climbStairsKSteps(5, 3) << endl; // Output: 13
    cout << "Ways to climb 5 stairs (Tribonacci): " << solver.climbStairsTribo(5) << endl; // Output: 13
    return 0;
}
```

---

## 🔍 Dry Run Trace — N = 5 (Space-Optimized)

```
Initial:  prev2 = 1 (dp[1])   prev1 = 2 (dp[2])

i=3: curr = 2 + 1 = 3    prev2 = 2    prev1 = 3
i=4: curr = 3 + 2 = 5    prev2 = 3    prev1 = 5
i=5: curr = 5 + 3 = 8    prev2 = 5    prev1 = 8

Return prev1 = 8 ✓

Verification: Enumerate all ways for N=5:
{1,1,1,1,1}, {1,1,1,2}, {1,1,2,1}, {1,2,1,1}, {2,1,1,1},
{1,2,2}, {2,1,2}, {2,2,1} = 8 ways ✓
```

---

## ⚠️ Common Interview Mistakes

1. **Wrong base case using `dp[0]`:** Setting `dp[0] = 1` is mathematically correct (1 way to "be" at ground), but this can confuse if you're using 1-indexed. Better to just set `dp[1]=1, dp[2]=2` and start loop at 3.
2. **Integer overflow for large N:** `int` overflows at ~$2.1 \times 10^9$. For $N > 44$, `climbStairs(44)` fits in int; `climbStairs(45) = 1836311903` (max int-safe value). LeetCode constrains $N \leq 45$, so `int` barely fits. Use `long long` for safety.
3. **Confusing "ways to reach" vs "ways to climb from":** `dp[n]` counts ways to reach step $n$ from step 0, not from step $n$.
4. **K-step extension bug:** In the K-step version, you need `dp[0] = 1` as the seed. Without it, `dp[1] = dp[0] = 0` and everything is 0.

---

## 📊 Complexity Analysis

| Approach | Time | Space | Notes |
|---|---|---|---|
| Naive Recursion | $O(2^N)$ | $O(N)$ stack | TLE for $N > 30$ |
| Memoization | $O(N)$ | $O(N)$ table + stack | Safe for $N \leq 10^4$ |
| Tabulation | $O(N)$ | $O(N)$ table | Cache-friendly |
| Space-Optimized | $O(N)$ | $O(1)$ | **Optimal for interview** |
| K-Step Generalization | $O(N \cdot K)$ | $O(K)$ | Sliding window trick |

**Why O(N) from exponential?** Memoization ensures each of the $N$ unique states is computed exactly once. The total work is proportional to the number of distinct states times the work per state — here $N \times O(1) = O(N)$.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] Is Climbing Stairs exactly Fibonacci? Prove it.
**Answer:** Yes, with a shifted index. Define $W(n)$ = ways to climb $n$ stairs. We have:
- $W(1) = 1, W(2) = 2$
- $W(n) = W(n-1) + W(n-2)$ for $n \geq 3$

Standard Fibonacci: $F(1)=1, F(2)=1, F(3)=2, F(4)=3, ...$  
Observe: $W(n) = F(n+1)$. Proof by induction: base $W(1) = 1 = F(2)$, $W(2) = 2 = F(3)$. Inductive step: $W(n) = W(n-1) + W(n-2) = F(n) + F(n-1) = F(n+1)$ by Fibonacci definition. $\square$

---

### Q2: [Extension] What if you can take 1, 2, or 3 steps? Derive the recurrence.
**Answer:**
$$W(n) = W(n-1) + W(n-2) + W(n-3)$$
Base cases: $W(1) = 1, W(2) = 2, W(3) = 4$ (verify: {1,1,1}, {1,2}, {2,1}, {3}).

This is the Tribonacci sequence. For up to $K$ steps:
$$W(n) = \sum_{j=1}^{\min(K,n)} W(n-j)$$
Can maintain a running window sum to compute in $O(N)$ time.

---

### Q3: [Output Prediction] What does this output and why?
```cpp
int climbStairs(int n) {
    if (n <= 2) return n;
    int prev2 = 1, prev1 = 2;
    for (int i = 3; i <= n; ++i) {
        prev2 = prev1;           // BUG: prev2 overwritten before curr computed
        prev1 = prev1 + prev2;
    }
    return prev1;
}
// Called with n = 5
```
**Answer:** This is buggy. After `prev2 = prev1`, both variables hold the same value. So `prev1 = prev1 + prev2 = 2 * prev1`. Output for n=5: i=3 → prev1=4, i=4 → prev1=8, i=5 → prev1=16. Correct answer is 8. The fix: compute `curr` in a temporary variable first, then update both.

---

### Q4: [Complexity] Prove the naive recursion is exactly $O(\phi^N)$ where $\phi = \frac{1+\sqrt{5}}{2}$.
**Answer:**
The number of calls $T(n) = T(n-1) + T(n-2) + 1$. The homogeneous part has characteristic equation $x^2 = x + 1$, roots $\phi = \frac{1+\sqrt{5}}{2} \approx 1.618$ and $\hat{\phi} = \frac{1-\sqrt{5}}{2} \approx -0.618$. The solution is $T(n) = \Theta(\phi^n)$ since $|\hat{\phi}| < 1$. For $n=50$, this is $\approx 10^{10}$ operations — clearly infeasible.

---

### Q5: [Extension] What if some steps are broken and you cannot land on them?
**Answer:**
Add a "blocked" set. Modify the recurrence:
```cpp
int climbStairs(int n, unordered_set<int>& broken) {
    vector<int> dp(n + 1, 0);
    dp[0] = 1;
    for (int i = 1; i <= n; ++i) {
        if (broken.count(i)) { dp[i] = 0; continue; } // Can't land here
        if (i >= 1) dp[i] += dp[i-1];
        if (i >= 2) dp[i] += dp[i-2];
    }
    return dp[n];
}
```
Broken steps simply contribute 0 to any future steps. This is a clean extension that tests your DP adaptability.

---

### Q6: [System Design] If N can be up to $10^{18}$, how do you compute `climbStairs(N)` efficiently?
**Answer:** Use **matrix exponentiation** to compute Fibonacci in $O(\log N)$:
$$\begin{pmatrix} W(n+1) \\ W(n) \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^n \begin{pmatrix} 1 \\ 1 \end{pmatrix}$$
Use fast matrix power (repeated squaring). Since results grow astronomically, also apply modular arithmetic: compute answers mod $10^9+7$.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Insight |
|---|---|---|
| 70 | Climbing Stairs | This problem — Fibonacci DP |
| 746 | Min Cost Climbing Stairs | Same recurrence + cost at each step |
| 1137 | N-th Tribonacci Number | 3-way recurrence, same framework |
| 91 | Decode Ways | Climbing stairs with validity constraints |
| 377 | Combination Sum IV | K-step generalization with arbitrary steps |

---

## 🔗 Cross-Topic Connections
- **Fibonacci:** This problem IS Fibonacci. Understanding Fibonacci → understand Climbing Stairs.
- **House Robber:** Same Fibonacci structure but with "max" instead of "sum" — maximization vs counting.
- **Decode Ways (LC 91):** Climbing stairs variant where some "steps" are invalid based on string content.
- **Matrix Exponentiation:** Enables $O(\log N)$ Fibonacci, applicable here for huge $N$.
- **Combinatorics:** The answer is also $\binom{n-1}{0} + \binom{n-2}{1} + \ldots$ (stars and bars on step choices).

---

## ⚡ 2-Minute Revision Flash Card
- **Recurrence:** $dp[i] = dp[i-1] + dp[i-2]$ — identical to Fibonacci.
- **Base cases:** $dp[1]=1$, $dp[2]=2$ (or use $dp[0]=1$ and adjust indices).
- **Space Optimized:** Two rolling variables `prev2`, `prev1`. Always compute `curr` into a temp before updating.
- **K-steps extension:** $dp[i] = \sum_{j=1}^{K} dp[i-j]$, seed with $dp[0]=1$.
- **Broken steps:** Set $dp[i] = 0$ if step $i$ is blocked; recurrence stays the same.
