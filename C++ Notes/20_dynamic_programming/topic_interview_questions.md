# 💼 Topic 20 Interview Question Bank: Dynamic Programming & Knapsack

> **Curated FAANG Interview Bank:** High-frequency technical interview questions, complexity proofs, and optimization puzzles for Dynamic Programming.

---

## 📌 Core DP Concepts & Theory

### Q1: How do you mathematically prove that a problem has Optimal Substructure?
**Answer:** By a cut-and-paste argument (proof by contradiction). Assume an optimal solution $S$ to problem $P$ contains a suboptimal solution $s'$ to subproblem $p$. If there existed a better solution $s''$ to $p$, replacing $s'$ with $s''$ in $S$ would yield a strictly better solution to $P$. This contradicts the assumption that $S$ was optimal, proving that optimal solutions to the global problem *must* contain optimal solutions to all subproblems.

### Q2: When should you prefer Top-Down (Memoization) over Bottom-Up (Tabulation)?
**Answer:**
- **Prefer Memoization:** When the state space is sparse. If only a small fraction of all possible subproblems need to be evaluated to reach the answer (e.g., recursive paths that prune early), top-down avoids computing useless states.
- **Prefer Tabulation:** When all subproblems must be visited anyway (dense state space). Tabulation eliminates recursion call-stack overhead, prevents stack overflow, and critically, enables space-optimization (reducing 2D arrays to 1D arrays).

### Q3: What is the difference between "Overlapping Subproblems" and "Optimal Substructure"?
**Answer:**
- **Optimal Substructure** means the optimal solution can be built from optimal solutions of its subproblems. (This dictates *if* DP or Greedy can be used).
- **Overlapping Subproblems** means the algorithm re-solves the exact same subproblems repeatedly. (This dictates *why* DP is efficient, as it caches these repeats).
Merge Sort has optimal substructure but *non-overlapping* subproblems (hence Divide & Conquer, not DP).

---

## 🎒 Knapsack & Variants

### Q4: Why is 0/1 Knapsack considered NP-Complete when it runs in $O(N \times W)$?
**Answer:** $O(N \times W)$ is **Pseudo-Polynomial** time, not strictly polynomial time. In complexity theory, input size $n$ is defined by the number of bits required to represent the input. To represent capacity $W$, you need $B = \log_2 W$ bits. Thus, the time complexity in terms of input size is $O(N \cdot 2^B)$, which is exponential with respect to the bit-length of the input $W$.

### Q5: Why does iterating backwards optimize 0/1 Knapsack to 1D space, while forward iteration solves Unbounded Knapsack?
**Answer:**
- **Backwards ($w = W \dots wt[i]$):** When computing $dp[w]$, the value $dp[w - wt[i]]$ has not yet been overwritten in the current item's loop; it still strictly holds the result from item $i-1$. This guarantees item $i$ is chosen at most once.
- **Forwards ($w = wt[i] \dots W$):** The value $dp[w - wt[i]]$ has already been updated to include item $i$ earlier in the same loop. Thus, we can pack item $i$, and then pack it again, solving Unbounded Knapsack.

### Q6: Can you solve the Fractional Knapsack problem using Dynamic Programming?
**Answer:** Technically yes, but it is vastly inefficient. DP would evaluate discrete capacity states, which is impossible if fractions are continuous, or terribly slow if fractions are granular (e.g., evaluating every 0.001 kg). The Greedy approach solves it perfectly and continuously in $O(N \log N)$ time.

### Q7: In the 0/1 Knapsack DP, how do you reconstruct exactly which items were chosen?
**Answer:** You cannot reliably do this if you used 1D space optimization, because history is lost. You must use the full 2D $dp[i][w]$ table. Start at $dp[N][W]$. 
- If $dp[i][W] \neq dp[i-1][W]$, it means item $i$ was included. Record item $i$, and move to $dp[i-1][W - wt[i]]$.
- If $dp[i][W] == dp[i-1][W]$, item $i$ was skipped. Move to $dp[i-1][W]$.

### Q8: What if $W$ is massive (e.g., $10^9$) but $N$ is very small (e.g., $N \le 40$)?
**Answer:** DP will result in Memory Limit Exceeded. Instead, use **Meet-in-the-Middle**. Divide the 40 items into two sets of 20. Generate all $2^{20}$ possible subset weights for both sets. Sort the second set. For each weight sum in the first set, use binary search (`upper_bound`) on the second set to find the maximum valid complement. Complexity: $O(2^{N/2} \log(2^{N/2}))$.

### Q9: What if $N \le 100$, $W = 10^9$, but the maximum value of any item is small ($v_i \le 1000$)?
**Answer:** Swap the DP dimensions! Instead of $dp[capacity] = \text{max\_value}$, change the state definition to $dp[value] = \text{min\_capacity}$.
The maximum possible value is $N \times V_{max} = 100,000$. The DP array is now size 100,000 instead of $10^9$. 
$dp[i][v] = \min(dp[i-1][v], wt[i] + dp[i-1][v - val[i]])$.

---

## 🧠 DP State Design & Transitions

### Q10: "House Robber" and "Maximum Sum Non-Adjacent Elements" are the same problem. How does the DP state change if the houses are arranged in a circle?
**Answer:** If houses are in a circle, house $0$ and house $N-1$ are adjacent. You cannot rob both. Therefore, run the standard House Robber DP twice:
1. Run DP from house $0$ to $N-2$ (ignoring the last house).
2. Run DP from house $1$ to $N-1$ (ignoring the first house).
Return the maximum of the two runs.

### Q11: How do you identify the "State" when formulating a DP solution?
**Answer:** A state is a set of parameters that uniquely defines a specific position or subproblem. Ask yourself: "What information do I need to make the *next* decision?" 
- For Knapsack: Current Item index `i`, Remaining Capacity `w`.
- For Buy/Sell Stock: Current Day `i`, Holding a stock `hasStock` (bool), Transactions left `k`.

### Q12: Explain the "State Machine" approach to DP.
**Answer:** Many DP problems (like Buy/Sell Stock with Cooldown, or regex matching) are best modeled as Finite State Machines. Each state (e.g., `Rest`, `Bought`, `Sold`) has a transition equation based on the action taken on day `i`. 
`dp[Bought][i] = max(dp[Bought][i-1], dp[Rest][i-1] - price[i])`

---

## 💻 Debugging Challenges

### Q13: [Debugging] Identify the bug in this 0/1 Knapsack snippet:
```cpp
int knapSack(int W, vector<int>& wt, vector<int>& val, int n) {
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < n; i++) {
        for (int w = wt[i]; w <= W; w++) { // BUG!
            dp[w] = max(dp[w], val[i] + dp[w - wt[i]]);
        }
    }
    return dp[W];
}
```
**Answer:** The inner loop iterates forward from `wt[i]` to `W`. This allows the same item `i` to be selected multiple times, incorrectly implementing Unbounded Knapsack.
**Fix:** Iterate backwards: `for (int w = W; w >= wt[i]; w--)`.

### Q14: [Debugging] Why does this recursive DP return TLE (Time Limit Exceeded) even with memoization?
```cpp
int solve(int i, int w, vector<vector<int>> memo) { ... }
```
**Answer:** The `memo` array is being passed by value! This means $O(N \times W)$ time is spent creating a deep copy of the memoization table on *every single recursive call*, defeating the entire purpose of caching.
**Fix:** Pass by reference: `vector<vector<int>>& memo`.

### Q15: How can you optimize the space of a 2D DP table if the transition formula is $dp[i][j] = dp[i-1][j-1] + dp[i-1][j]$?
**Answer:** Notice that computing row `i` only requires values from row `i-1`. You can reduce the $N \times M$ matrix to just two 1D arrays (size $M$): `prevRow` and `currRow`. After calculating `currRow`, set `prevRow = currRow`. This reduces space from $O(N \times M)$ to $O(M)$. (Sometimes it can even be optimized to a single 1D array if traversed backwards).
