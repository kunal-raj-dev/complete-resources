# 💼 Topic Interview Question Bank — Topic 20: Dynamic Programming

---

### Q1: Why must the capacity loop run backwards (`W` down to `wt[i]`) in 1D 0/1 Knapsack?
**Answer:**
If we iterate forwards from `wt[i]` to `W`, `dp[w - wt[i]]` would refer to the newly updated value from the *current* item in the same iteration, allowing the same item to be included multiple times (which solves the Unbounded Knapsack problem). Iterating in reverse ensures that `dp[w - wt[i]]` accesses the value from the *previous* item's row before it was overwritten, enforcing the 0/1 restriction that each item can be selected at most once.
