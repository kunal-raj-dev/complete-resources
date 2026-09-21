# ⚡ Rapid Revision — Topic 20: Dynamic Programming

> **Target:** 5-minute pre-interview refresher on DP recurrences and space-optimization tricks.

---

## 🔑 Recurrence Quick Reference
- **Climbing Stairs:** `dp[i] = dp[i-1] + dp[i-2]`.
- **House Robber:** `dp[i] = max(nums[i] + dp[i-2], dp[i-1])`.
- **House Robber Circular:** `max(rob(0, n-2), rob(1, n-1))`.
- **0/1 Knapsack 1D:** `for (int w = W; w >= wt[i]; w--) dp[w] = max(dp[w], val[i] + dp[w - wt[i]])`.
