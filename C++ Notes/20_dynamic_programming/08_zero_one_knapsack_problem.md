# Lecture 144: DP 8: 0/1 Knapsack Problem (Recursion to 1D Space Optimized DP)

> **One-Line Purpose:** Solve the classical NP-complete 0/1 Knapsack problem through recursion, 2D tabulation, and state-of-the-art 1D reverse-capacity space optimization in $O(N \times W)$ time and $O(W)$ space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #144  
> **Video ID:** `tEW-zDckvFw`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=tEW-zDckvFw)  
> **Duration:** 45:03  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Understanding the 0/1 decision boundary: an item can either be included once or excluded.
- Formulate the fundamental 2D Recurrence Relation for bounded knapsack.
- Master DP state-space reduction from 2D $O(N \times W)$ to 1D $O(W)$.
- Understand the critical "Reverse-Loop Invariant" that prevents multi-counting.

---

## 🧠 Core Intuition — Why This Works

You are a thief with a bag holding exactly $W$ kg. You are looking at item $i$ which weighs $wt[i]$ and is worth $val[i]$. 
You have two choices:
1. **Exclude It:** You just skip it. Your bag's capacity stays the same, and your profit is whatever the best profit was for the previous $i-1$ items at the same capacity.
2. **Include It:** You put it in the bag. You gain $val[i]$. BUT, your bag now has $wt[i]$ less capacity. So the rest of your bag must be filled by the *best* combination of the previous $i-1$ items that fit into the *remaining* capacity ($W - wt[i]$).

You are greedy! You just take the $\max$ of these two choices.

**The DP Equation:**
$$dp[i][w] = \max(dp[i-1][w],\; val[i-1] + dp[i-1][w - wt[i-1]])$$

*(Note: Indexing often uses $i-1$ for weights/values arrays if $dp[i]$ represents the first $i$ items).*

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Maximize value with limited capacity"**: Direct keyword.
- **"Subset selection with a budget constraint"**: e.g., Pick a subset of numbers that sum exactly to $K$.
- **0/1 restriction**: "Each item can only be used once."

---

## 📐 Algorithm Walk-Through (1D Optimized)

We don't actually need a 2D matrix. To compute row $i$, we ONLY look at row $i-1$. This means a single 1D array of size $W+1$ is enough.
But there is a catch! 

If we iterate capacities left-to-right (`w = 0` to `W`):
When computing `dp[w]`, we need `dp[w - wt[i]]`. But since `w - wt[i]` is smaller than `w`, we *already overwrote it* in the current iteration! This means we might pack the *same* item multiple times (which solves the **Unbounded Knapsack**, not 0/1).

**The Solution:**
Iterate backwards (`w = W` down to `wt[i]`).
When computing `dp[w]`, the value of `dp[w - wt[i]]` is strictly from the *previous* item's row, because we haven't overwritten the smaller indices yet!

1. **Initialize**: `vector<int> dp(W + 1, 0)`.
2. **Item Loop**: `for (int i = 0; i < n; ++i)`
3. **Weight Loop (Reverse)**: `for (int w = W; w >= wt[i]; --w)`
4. **Transition**: `dp[w] = max(dp[w], val[i] + dp[w - wt[i]])`

---

## 💻 Complete C++ Implementation: All 3 Approaches

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

class KnapsackSolver {
public:
    // Approach 1: 2D Tabulation - O(N * W) Time, O(N * W) Space
    static int knapsack2D(int W, const vector<int>& wt, const vector<int>& val, int n) {
        vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));

        for (int i = 1; i <= n; ++i) {
            for (int w = 0; w <= W; ++w) {
                if (wt[i - 1] <= w) {
                    dp[i][w] = max(dp[i - 1][w], val[i - 1] + dp[i - 1][w - wt[i - 1]]);
                } else {
                    dp[i][w] = dp[i - 1][w];
                }
            }
        }
        return dp[n][W];
    }

    // Approach 2: 1D Space-Optimized - O(N * W) Time, O(W) Space
    static int knapsack1D(int W, const vector<int>& wt, const vector<int>& val, int n) {
        vector<int> dp(W + 1, 0);

        for (int i = 0; i < n; ++i) {
            // MUST ITERATE BACKWARDS to ensure dp[w - wt[i]] comes from previous item!
            for (int w = W; w >= wt[i]; --w) {
                dp[w] = max(dp[w], val[i] + dp[w - wt[i]]);
            }
        }
        return dp[W];
    }
};

int main() {
    int W = 50;
    vector<int> val = {60, 100, 120};
    vector<int> wt = {10, 20, 30};
    int n = val.size();

    cout << "2D DP Max Value: " << KnapsackSolver::knapsack2D(W, wt, val, n) << endl;
    cout << "1D DP Max Value: " << KnapsackSolver::knapsack1D(W, wt, val, n) << endl; 
    // Both output: 220
    
    return 0;
}
```

---

## 🔍 Dry Run Trace (1D DP)

**W = 50.**
Items: `0: (val=60, wt=10)`, `1: (val=100, wt=20)`, `2: (val=120, wt=30)`
`dp` array size 51. Initialized to 0.

**Item 0 (v=60, w=10):**
- Loop `w` from 50 down to 10.
- `dp[w] = max(0, 60 + dp[w-10]) = 60`.
- All `dp[10...50]` become 60.

**Item 1 (v=100, w=20):**
- Loop `w` from 50 down to 20.
- `w=50`: `dp[50] = max(dp[50], 100 + dp[30])` = `max(60, 100 + 60) = 160`.
- `w=40`: `dp[40] = max(dp[40], 100 + dp[20])` = `max(60, 100 + 60) = 160`.
- `w=30`: `dp[30] = max(dp[30], 100 + dp[10])` = `max(60, 100 + 60) = 160`.
- `w=20`: `dp[20] = max(dp[20], 100 + dp[0])` = `max(60, 100 + 0) = 100`.
- `dp` array now: `[0..9]=0, [10..19]=60, [20..29]=100, [30..50]=160`.

**Item 2 (v=120, w=30):**
- Loop `w` from 50 down to 30.
- `w=50`: `dp[50] = max(160, 120 + dp[20])` = `max(160, 120 + 100) = 220`.
- `w=40`: `dp[40] = max(160, 120 + dp[10])` = `max(160, 120 + 60) = 180`.
- `w=30`: `dp[30] = max(160, 120 + dp[0])` = `max(160, 120 + 0) = 160`.

**Final Result**: `dp[50] = 220`. (Taking Item 1 & 2).

---

## ⚠️ Common Interview Mistakes

1. **Forgetting the Reverse Loop for 1D**: The #1 reason candidates fail the 1D space optimization is looping forwards `for(int w = wt[i]; w <= W; w++)`. As traced above, this solves the Unbounded Knapsack, allowing infinite duplicates.
2. **Loop Bounds off-by-one**: Knapsack weights use 1-based indexing in DP commonly. In the 1D version `i` goes from `0` to `n-1` cleanly, but the weight boundary `w >= wt[i]` is an inclusive bound. 
3. **Pseudo-polynomial Trap**: Don't say time is simply polynomial. If $W$ is $10^9$, this $O(NW)$ algorithm will Time Limit Exceed (TLE). Time complexity depends on the *magnitude* of $W$, making it pseudo-polynomial.

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N \times W)$ where $N$ is items and $W$ is max weight.
- **Space Complexity:** $O(N \times W)$ for 2D Tabulation, optimized to $O(W)$ for the 1D array approach.

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: What happens if you want to know EXACTLY which items were picked?
**Answer:** The 1D space optimization destroys the history of choices. If the interviewer asks you to reconstruct the items picked, you **must** use the 2D $O(N \times W)$ DP table. You start at `dp[n][W]` and trace backward: if `dp[i][w] == dp[i-1][w]`, item $i$ was skipped. If `dp[i][w] == val[i] + dp[i-1][w-wt[i]]`, it was picked!

### Q2: What if W is massive (e.g., $10^9$), but N is small (e.g., 40)?
**Answer:** The DP will fail due to memory/time. Use **Meet in the Middle**. Split the $N=40$ items into two arrays of 20. Generate all $2^{20}$ subset sums for both. Sort one array, and for every element in the first array, binary search (`upper_bound`) for the best complement in the second array. Runs in $O(2^{N/2} \log(2^{N/2}))$.

### Q3: What if N is 100, W is $10^9$, but max value is small (e.g., $v \le 1000$)?
**Answer:** Swap the DP dimensions! Instead of `dp[capacity] = max_value`, define `dp[value] = min_weight`. The table size is $N \times (N \times V_{\max})$, which is $100 \times 100000 = 10^7$ cells. Much faster than $100 \times 10^9$.

### Q4: How is this different from Unbounded Knapsack?
**Answer:** Unbounded knapsack allows unlimited copies of an item. To solve it, you simply change the inner weight loop of the 1D optimized version to run forwards (`w = wt[i]` to `W`) instead of backwards.

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 416: Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/)** — Exact 0/1 knapsack variant. "Is there a subset that sums to `TotalSum / 2`?"
2. **[Leetcode 494: Target Sum](https://leetcode.com/problems/target-sum/)** — Can be reduced mathematically directly to 0/1 subset sum.
3. **[Leetcode 1049: Last Stone Weight II](https://leetcode.com/problems/last-stone-weight-ii/)** — Beautiful problem reducing to dividing stones into two sets of minimum difference (a Knapsack variant).

---

## 🔗 Cross-Topic Connections
- **Meet-in-the-Middle:** Required for massive $W$ but small $N$.
- **Backtracking:** DFS + Memoization is the top-down equivalent of this tabular DP.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Maximize value in bag of capacity $W$, 1 copy per item.
- **2D DP Equation:** `dp[i][w] = max(dp[i-1][w], val[i] + dp[i-1][w-wt[i]])`.
- **1D DP Equation:** `dp[w] = max(dp[w], val[i] + dp[w-wt[i]])`.
- **Crucial Detail:** For 1D, `w` MUST iterate BACKWARDS from `W` down to `wt[i]`.
- **Reconstruction:** If you need the items themselves, you must use 2D DP to backtrack the choices.
- **Time/Space:** $O(NW)$ Time | $O(W)$ Space (1D approach).
