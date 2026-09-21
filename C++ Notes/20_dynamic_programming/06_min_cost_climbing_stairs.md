# Lecture 142: DP 6: Min Cost Climbing Stairs (LeetCode 746)

> **One-Line Purpose:** Calculate minimal cost to reach the top floor given step costs where you can initiate the climb from either index 0 or index 1, taking 1 or 2 steps per leap.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #142  
> **Video ID:** `KwItlcfF9vE`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=KwItlcfF9vE)  
> **Duration:** 26:08  
> **Status:** AUDITED  

---

## 🧠 Core Intuition — Two Key Twists

### How This Differs from Climbing Stairs
Climbing Stairs counts **how many ways** to reach step $N$ (all steps cost equally "1 decision").

Min Cost Climbing Stairs asks: what is the **minimum cost** to reach the **top** (one step past the last step) when each step has an associated cost you pay **when you stand on it and jump off**.

Two important nuances:
1. **You pay cost when you LEAVE a step**, not when you arrive.
2. **You can start from step 0 or step 1** (either is free to "stand on" initially).
3. **The destination is "beyond" the array** — after `cost[n-1]`, not at it.

### Real-World Analogy
Imagine each stair is a launchpad. Standing on it and pressing the launch button costs `cost[i]`. You want to exit the staircase (reach "the top" which is beyond the last stair) with minimum total launch costs spent.

```
cost = [10, 15, 20]
         0   1   2

Possible paths to "top" (index 3):
  Path A: step 0 → step 2 → top:   10 + 20 = 30
  Path B: step 1 → top:             15     = 15  ← minimum!
  Path C: step 0 → step 1 → top:   10 + 15 = 25
  Path D: step 1 → step 2 → top:   15 + 20 = 35

Answer: 15 ✓
```

---

## 📐 The 4-Step DP Framework Applied

**Step 1: State Definition**
`dp[i]` = minimum cost to **reach** step $i$ (not pay its cost yet).

Or equivalently: define `dp[i]` as minimum cost starting FROM step $i$ to the top.

The tabulation approach uses: `dp[i]` = minimum cost to LAND ON step $i$.
- `dp[0] = cost[0]` (pay cost[0] to leave step 0)
- `dp[1] = cost[1]` (pay cost[1] to leave step 1)

**Step 2: Recurrence**
$$dp[i] = cost[i] + \min(dp[i-1], dp[i-2])$$
You arrive at step $i$ from either step $i-1$ or step $i-2$, paying the minimum of those two prior costs. Then you pay `cost[i]` to leave.

**Step 3: Base Cases**
- `dp[0] = cost[0]`
- `dp[1] = cost[1]`

**Step 4: Space Optimize**
Only `dp[i-1]` and `dp[i-2]` needed → two rolling variables.

**Final Answer:**
`min(dp[n-1], dp[n-2])` — you can jump to "top" from the last step OR the second-to-last step.

---

## 💻 Complete C++ Implementation

```cpp
#include <vector>
#include <algorithm>
#include <iostream>

using namespace std;

class SolutionMinCostClimbingStairs {
public:
    // Space-Optimized: O(N) Time, O(1) Space
    int minCostClimbingStairs(vector<int>& cost) {
        int n = cost.size();
        int prev2 = cost[0];
        int prev1 = cost[1];

        for (int i = 2; i < n; ++i) {
            int curr = cost[i] + min(prev1, prev2);
            prev2 = prev1;
            prev1 = curr;
        }

        // To reach top of floor (index n), we can jump from step n-1 or n-2
        return min(prev1, prev2);
    }

    // Tabulation version: O(N) Time, O(N) Space (easier to trace)
    int minCostClimbingStairsTabulation(vector<int>& cost) {
        int n = cost.size();
        if (n == 1) return cost[0]; // Edge case
        vector<int> dp(n);
        dp[0] = cost[0];
        dp[1] = cost[1];
        for (int i = 2; i < n; ++i) {
            dp[i] = cost[i] + min(dp[i-1], dp[i-2]);
        }
        return min(dp[n-1], dp[n-2]);
    }

    // Top-Down Memoization: O(N) Time, O(N) Space
    int solve(int i, vector<int>& cost, vector<int>& memo) {
        if (i < 0) return 0; // Free to start
        if (i <= 1) return cost[i];
        if (memo[i] != -1) return memo[i];
        return memo[i] = cost[i] + min(solve(i-1, cost, memo), solve(i-2, cost, memo));
    }
    int minCostMemo(vector<int>& cost) {
        int n = cost.size();
        vector<int> memo(n, -1);
        // The "top" (index n) is reached from n-1 or n-2
        return min(solve(n-1, cost, memo), solve(n-2, cost, memo));
    }
};

int main() {
    SolutionMinCostClimbingStairs solver;
    vector<int> cost = {10, 15, 20};
    cout << "Min Cost: " << solver.minCostClimbingStairs(cost) << endl; // Output: 15

    vector<int> cost2 = {1, 100, 1, 1, 1, 100, 1, 1, 100, 1};
    cout << "Min Cost: " << solver.minCostClimbingStairs(cost2) << endl; // Output: 6
    return 0;
}
```

---

## 🔍 Dry Run Trace — `cost = [10, 15, 20]`

```
n=3
Initial: prev2 = 10 (dp[0])   prev1 = 15 (dp[1])

i=2: curr = 20 + min(15, 10) = 20 + 10 = 30
     prev2=15, prev1=30

Final: min(prev1, prev2) = min(30, 15) = 15 ✓

Interpretation:
  dp[0]=10 means: if you leave from step 0 directly, cost = 10
  dp[1]=15 means: if you leave from step 1 directly, cost = 15
  dp[2]=30 means: cheapest way to reach step 2 AND leave = 30 (came from step 0: 10, then pay 20)

  To reach top: from step 1 (cost 15) or step 2 (cost 30) → min = 15
```

---

## 🔍 Dry Run Trace — `cost = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]`

```
dp: [1, 100, 2, 3, 3, 103, 4, 5, 104, 6]
     0   1   2  3  4   5   6  7   8   9

Trace:
dp[0]=1, dp[1]=100
dp[2]=1 + min(100,1) = 1+1 = 2
dp[3]=1 + min(2,100) = 1+2 = 3
dp[4]=1 + min(3,2)   = 1+2 = 3
dp[5]=100 + min(3,3) = 100+3 = 103
dp[6]=1 + min(103,3) = 1+3 = 4
dp[7]=1 + min(4,103) = 1+4 = 5
dp[8]=100 + min(5,4) = 100+4 = 104
dp[9]=1 + min(104,5) = 1+5 = 6

Answer = min(dp[9], dp[8]) = min(6, 104) = 6 ✓
```

---

## ⚠️ Common Interview Mistakes

1. **Confusing where you pay:** You pay `cost[i]` when you **step off** step $i$ (to take a jump). This means `dp[i] = cost[i] + min(dp[i-1], dp[i-2])`, NOT `dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])`.

2. **Wrong final answer:** Returning `dp[n-1]` instead of `min(dp[n-1], dp[n-2])`. You can reach the top from EITHER of the last two steps.

3. **Confusing with Frog Jump:** In Frog Jump, the cost is the height difference (`|h[i]-h[j]|`). Here, the cost is `cost[i]` at the source step. Different cost models, same DP skeleton.

4. **Starting index confusion:** You can start at step 0 OR step 1 for free. This is captured by the base cases `dp[0] = cost[0]` and `dp[1] = cost[1]`. If a candidate initializes `dp[0] = 0`, that's wrong (you still pay to leave step 0).

5. **Edge case `n=2`:** With only 2 steps, the loop doesn't run. Answer = `min(cost[0], cost[1])`. The code handles this correctly since no iterations occur.

---

## 📊 Complexity Analysis
- **Time Complexity:** $O(N)$ — single linear pass.
- **Space Complexity:** $O(1)$ — two rolling variables `prev1` and `prev2`.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] What is the exact semantic difference between Climbing Stairs and Min Cost Climbing Stairs?
**Answer:**
| Property | Climbing Stairs (LC 70) | Min Cost Climbing Stairs (LC 746) |
|---|---|---|
| Objective | Count distinct ways | Minimize total cost |
| Cost per step | Free (or uniform) | `cost[i]` paid when leaving |
| Starting position | Must start at step 0 | Can start at step 0 OR step 1 |
| Destination | Reach step N | Reach "top" (beyond step N-1) |
| Operator | Addition (sum of ways) | Minimum (min of costs) |
| Recurrence | `dp[i] = dp[i-1] + dp[i-2]` | `dp[i] = cost[i] + min(dp[i-1], dp[i-2])` |

---

### Q2: [Debugging] Identify the bug and predict the output for `cost = [10, 15, 20]`:
```cpp
int minCostClimbingStairs(vector<int>& cost) {
    int n = cost.size();
    int prev2 = cost[0], prev1 = cost[1];
    for (int i = 2; i < n; ++i) {
        int curr = cost[i] + min(prev1, prev2);
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1; // BUG: should be min(prev1, prev2)
}
```
**Answer:** For `cost = [10, 15, 20]`: loop runs once (i=2), prev1=30. Returns 30 instead of min(30, 15) = 15. The bug is returning only `prev1` (best ending at last step) without considering jumping from step n-2 directly to top.

---

### Q3: [Extension] What if you can take 1, 2, or 3 steps?
**Answer:**
$$dp[i] = cost[i] + \min(dp[i-1], dp[i-2], dp[i-3])$$
Base cases: `dp[0]=cost[0]`, `dp[1]=cost[1]`, `dp[2]=cost[2]+min(cost[0],cost[1])`.
Final answer: `min(dp[n-1], dp[n-2], dp[n-3])`.
Use three rolling variables instead of two.

---

### Q4: [Conceptual] Prove that the greedy approach (always jump from the cheaper of the current two steps) fails.
**Answer:** Counterexample: `cost = [1, 100, 1, 1]`. Greedy: at step 0 (cost 1) vs step 1 (cost 100) → pick step 0. From step 0 (prev=0, curr=2), step 0 vs step 1 → pick step 0. Greedy path: step 0 → step 2 → top = 1+1=2. DP: same answer here. Let's try `cost = [0, 2, 0, 1]`. Greedy: start step 0 (cost 0) → step 2 (cost 0) → top. Total = 0. DP gives same. The greedy here happens to work by accident. A cleaner counterexample: `cost = [10, 15, 20, 10, 100]`. Greedy might route through 10 and 20 (sum=30) when DP finds 10+10=20 via steps 0 and 3. The point: greedy can't look ahead to see that skipping a "cheap" step leads to a cheaper overall path.

---

### Q5: [Extension] How does Min Cost Climbing Stairs relate to Shortest Path algorithms?
**Answer:** Min Cost Climbing Stairs is equivalent to finding the **shortest path in a DAG** (Directed Acyclic Graph) where:
- Nodes are steps 0 to N (N = "top")
- Edge from step $i$ to step $i+1$ has weight `cost[i]`
- Edge from step $i$ to step $i+2` has weight `cost[i]`

DP on DAGs = topological order processing = same as Dijkstra on DAG but simpler (can use DP directly since graph is acyclic and we process left to right).

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Insight |
|---|---|---|
| 746 | Min Cost Climbing Stairs | This problem |
| 70 | Climbing Stairs | Same structure, counting ways instead |
| 983 | Minimum Cost for Tickets | DP on days with 3 ticket options |
| 322 | Coin Change | Min cost with unlimited step sizes |
| 931 | Minimum Falling Path Sum | 2D version of min cost on a grid |

---

## 🔗 Cross-Topic Connections
- **Climbing Stairs (LC 70):** Same recurrence structure, different objective.
- **Frog Jump:** Both minimize cost; difference is Frog Jump's cost depends on height difference, not a fixed array.
- **Coin Change (LC 322):** Generalization — can jump arbitrary step sizes (coin denominations) with uniform cost (1 coin).
- **Shortest Path on DAG:** This problem IS shortest path on a 2-neighbor DAG.
- **Min Path Sum (LC 64):** 2D generalization — same min-accumulation DP pattern on a grid.

---

## ⚡ 2-Minute Revision Flash Card
- **Recurrence:** $dp[i] = cost[i] + \min(dp[i-1], dp[i-2])$.
- **Base cases:** `prev2 = cost[0]`, `prev1 = cost[1]` (pay to leave step 0 and step 1).
- **Final answer:** `min(prev1, prev2)` — can jump to top from EITHER of last two steps.
- **Key pitfall:** Don't return `prev1` alone — always take min with `prev2` at the end.
- **Distinction:** In Climbing Stairs you sum; here you minimize. Both use the same `dp[i-1], dp[i-2]` dependency.
