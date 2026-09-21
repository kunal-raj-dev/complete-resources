# ⚡ Topic 20 Revision: Dynamic Programming & Knapsack

> **High-Yield Revision Guide:** 1D and 2D DP state formulations, space-reduction blueprints, and Knapsack problem patterns.

---

## 1. 🎯 Pattern Recognition Cheat Sheet

| Problem Type | Trigger Keywords | Standard Approach | Time / Space |
|---|---|---|---|
| **Max/Min Path in Array** | "Climbing stairs", "Frog Jump" | `dp[i] = cost[i] + max(dp[i-1], dp[i-2])` | $O(N)$ / $O(1)$ |
| **Non-Adjacent Elements** | "House Robber", "No two adjacent" | `dp[i] = max(dp[i-1], val[i] + dp[i-2])` | $O(N)$ / $O(1)$ |
| **0/1 Knapsack** | "Given Capacity W", "Pick once" | `dp[w] = max(dp[w], val[i] + dp[w-wt[i]])` (rev) | $O(NW)$ / $O(W)$ |
| **Unbounded Knapsack** | "Infinite supply", "Multiple times" | `dp[w] = max(dp[w], val[i] + dp[w-wt[i]])` (fwd) | $O(NW)$ / $O(W)$ |
| **Fractional Knapsack** | "Fractions allowed", "Divisible" | **GREEDY**: Sort by `value/weight` | $O(N \log N)$ / $O(1)$ |

---

## 2. 🧠 Core DP Mental Models

### A. The 4-Step DP Framework
1. **Define the State:** What does `dp[i]` or `dp[i][j]` mathematically represent? (e.g., "Max profit using first $i$ items with capacity $j$").
2. **Formulate the Recurrence:** How does state $i$ depend on state $i-1$ or $i-2$? (The transition equation).
3. **Identify Base Cases:** What is `dp[0]`? What happens when capacity is 0?
4. **Determine Traversal Order:** Left-to-right? Right-to-left? Top-down? (Crucial for space optimization).

### B. Memoization vs Tabulation
- **Memoization (Top-Down):** Recursion + Hash Map/Array. Easy to write directly from recurrence relation. Visits only needed states. Risks Stack Overflow.
- **Tabulation (Bottom-Up):** Iterative `for` loops. Computes all states. Eliminates recursion overhead. Enables space optimization.

---

## 3. 📐 DP Space Optimization Golden Rules

If your current DP state `dp[i][j]` depends ONLY on previous rows:

1. **Dependent only on immediate previous row `i-1`:** 
   - Reduce from $O(N \times M)$ 2D matrix to $O(M)$ using two 1D arrays: `prevRow` and `currRow`.
2. **Dependent only on `i-1` and strictly smaller column indices `< j`:** 
   - Reduce to a **single** 1D array of size $M$.
   - **MUST iterate columns backwards** (e.g., $w = W \to wt[i]$). This prevents reading values you just overwrote in the current step (0/1 Knapsack).
3. **Dependent only on `i-1` and strictly smaller/equal column indices `<= j` (where item can be reused):**
   - Reduce to a **single** 1D array of size $M$.
   - **MUST iterate columns forwards** (e.g., $w = wt[i] \to W$). This intentionally reads values overwritten in the current step (Unbounded Knapsack).
4. **Dependent only on the last 2 computed values (e.g., Fibonacci, House Robber):** 
   - Reduce from $O(N)$ array to $O(1)$ space using just two variables: `prev1` and `prev2`.

---

## 4. ⚠️ 3 Fatal Traps to Avoid

1. **The Overlapping 0/1 Bug:** Doing a forward loop in 1D 0/1 Knapsack. It will silently calculate Unbounded Knapsack, passing base test cases but failing larger ones.
2. **Greedy over DP:** Assuming you can just sort items by "highest value" or "lowest weight" for 0/1 Knapsack. This is mathematically proven to fail. You MUST use DP.
3. **Array Bounds Off-by-One:** When moving from 2D to 1D, remember that weights are 1-indexed in the loops (`W+1` size array). But `wt[i]` values are 0-indexed vectors. `w - wt[i-1]` in 2D becomes `w - wt[i]` in 1D.

---

## 5. 🔥 Interview Q&A — Google / Amazon Level

### Q1: How do you know when to use Dynamic Programming vs Greedy?
Both require the **Optimal Substructure** property (optimal solution to the problem incorporates optimal solutions to subproblems). However, DP also handles **Overlapping Subproblems**. Greedy makes a locally optimal choice and never looks back. If a future choice depends on the outcome of a past choice, Greedy fails (e.g., 0/1 Knapsack) because it cannot reconsider. DP implicitly explores all valid possibilities by caching them.

### Q2: Why does Tabulation generally perform better than Memoization, even if Time Complexity is the same?
1. **No Recursion Overhead:** Tabulation avoids function call stack allocation, context switching, and the risk of Stack Overflow.
2. **Cache Locality:** Tabulation accesses arrays sequentially in memory (especially in 1D or 2D loops), which is highly optimized by CPU cache lines. Memoization access patterns can be sporadic.
3. **Space Optimization:** Tabulation allows discarding older states (e.g., keeping only the previous row). Memoization must keep the entire cache intact because the recursive tree traversal is unpredictable.

### Q3: When is Memoization actually faster than Tabulation?
When the state space is sparse. If the problem has $N \times M$ possible states, but the specific input only ever reaches $10\%$ of those states, Tabulation will waste time computing the other $90\%$. Memoization, being demand-driven, will uniquely visit and compute only the strictly required states.

### Q4: In 0/1 Knapsack Space Optimization, why must we traverse the weight array backwards?
If we traverse forwards, `dp[w]` might be updated using `dp[w - wt[i]]` which was *already updated* in the current iteration `i`. This means we would be using the same item multiple times, effectively solving the Unbounded Knapsack problem. Traversing backwards ensures that when calculating `dp[w]`, the values at `< w` are strictly from the previous iteration `i - 1`.

### Q5: What is the most common state dimension design for DP on strings (e.g., Edit Distance, LCS)?
A 2D array `dp[i][j]` representing the answer for the prefix of string A up to index `i` and the prefix of string B up to index `j`. The base cases usually involve `i=0` or `j=0` (comparing an empty string against a prefix).

## 6. ⚡ 2-Minute Revision Flash Card

- **State:** Defines the subproblem (e.g., `dp[i][w] = max profit using i items with capacity w`).
- **Transition:** How to build current state from past states (e.g., `max(skip, take)`).
- **0/1 Knapsack 1D Space:** Iterate weights backwards ($W \to wt[i]$).
- **Unbounded Knapsack 1D Space:** Iterate weights forwards ($wt[i] \to W$).
- **Fibonacci/House Robber Space:** Keep only `prev1` and `prev2`, space becomes $O(1)$.
- **Greedy vs DP:** Fractional = Greedy (sort by value/weight). 0/1 = DP.
