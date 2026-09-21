# Lecture 137: Dynamic Programming Foundations: Memoization, Tabulation & Space Optimization

> **One-Line Purpose:** Master the transition from exponential recursion ($O(2^N)$) to linear polynomial time ($O(N)$) using Overlapping Subproblems and Optimal Substructure.

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

- Identify the two mandatory prerequisites for Dynamic Programming:
  1. **Overlapping Subproblems:** Same subproblems evaluated repeatedly in the recursion tree.
  2. **Optimal Substructure:** Optimal solution to the global problem constructed from optimal solutions of subproblems.
- Master the 3 Levels of DP Optimization:
  1. **Level 1 (Top-Down):** Recursion + Memoization table.
  2. **Level 2 (Bottom-Up):** Iterative Tabulation from base cases.
  3. **Level 3 (Space Optimization):** State variable compaction ($O(N) \to O(1)$ space).

---

## 🔵 Complete C++ Fibonacci Progression

```cpp
#include <vector>
#include <iostream>
using namespace std;

// Level 1: Top-Down Recursion + Memoization
int fibMemo(int n, vector<int>& dp) {
    if (n <= 1) return n;
    if (dp[n] != -1) return dp[n];
    return dp[n] = fibMemo(n - 1, dp) + fibMemo(n - 2, dp);
}

// Level 2: Bottom-Up Tabulation (Iterative)
int fibTab(int n) {
    if (n <= 1) return n;
    vector<int> dp(n + 1);
    dp[0] = 0;
    dp[1] = 1;
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    return dp[n];
}

// Level 3: Space Optimized O(1) Memory
int fibOptimized(int n) {
    if (n <= 1) return n;
    int prev2 = 0;
    int prev1 = 1;
    for (int i = 2; i <= n; i++) {
        int curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```
