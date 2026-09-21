# Lecture 141: DP 5: Frog Jump (Minimum Energy 1D DP)

> **One-Line Purpose:** Determine the minimum total energy expended for a frog to reach stair $N-1$ where jumping from stair $i$ to $j$ costs $|height[i] - height[j]|$, choosing jumps of 1 or 2 steps.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #141  
> **Video ID:** `AKqlgskrZwI`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=AKqlgskrZwI)  
> **Duration:** 29:29  
> **Status:** AUDITED  

---

## 🧠 Core Intuition — How This Differs from Climbing Stairs

### The Critical Distinction
Climbing Stairs asks: **how many ways** to reach step $N$ (count problem, cost is uniform = 1 per jump).

Frog Jump asks: **minimum energy** to reach step $N-1$ (optimization problem, cost **varies** per jump).

The structural skeleton is the same (jump 1 or 2 steps), but the variation in step costs breaks the pure Fibonacci pattern and requires full DP with the `min` operator.

### Real-World Analogy
Think of the stones as stepping stones across a river at different heights. Jumping across a large height gap (like 10m → 1m) costs more energy than a small gap (10m → 9m). You want the route with minimum total height-change expenditure. You can't just take the "shortest" path — you need to consider the height profile to find the globally cheapest route.

```
Heights: [10, 20, 30, 10]
          0   1   2   3

Possible routes from 0 to 3:
  0→1→2→3: |20-10| + |30-20| + |10-30| = 10+10+20 = 40
  0→1→3:   |20-10| + |10-20|            = 10+10    = 20
  0→2→3:   |30-10| + |10-30|            = 20+20    = 40
Answer: 20 ✓ (route 0→1→3)
```

### Why Greedy Fails Here
Greedy "always take the 1-step jump" would take route 0→1→2→3 = 40. Greedy "always take the 2-step jump" takes route 0→2 (cost 20), but can't reach 3 from 2 in one jump. There's no single greedy choice — the height profile determines everything, requiring DP to evaluate all routes.

---

## 🔵 Recurrence Formulation
Let $dp[i]$ be the minimum energy required to reach stone $i$:
$$dp[i] = \min(dp[i-1] + |height[i] - height[i-1]|,\; dp[i-2] + |height[i] - height[i-2]|)$$

---

## 📐 The 4-Step DP Framework Applied

**Step 1: State Definition**
`dp[i]` = minimum energy to reach stone $i$ from stone 0.

**Step 2: Recurrence**
$$dp[i] = \min(\underbrace{dp[i-1] + |h[i] - h[i-1]|}_{\text{1-step jump from i-1}},\; \underbrace{dp[i-2] + |h[i] - h[i-2]|}_{\text{2-step jump from i-2}})$$

The frog **must** arrive at stone $i$ from either stone $i-1$ or stone $i-2$. We take the minimum.

**Step 3: Base Cases**
- `dp[0] = 0` — frog starts at stone 0, zero cost
- `dp[1] = |h[1] - h[0]|` — only one way to reach stone 1: from stone 0

**Step 4: Space Optimize**
`dp[i]` only depends on `dp[i-1]` and `dp[i-2]` → two rolling variables.

---

## 💻 Complete C++ Implementation

```cpp
#include <vector>
#include <cmath>
#include <algorithm>
#include <climits>
#include <iostream>

using namespace std;

class FrogJump {
public:
    // Space-Optimized: O(N) Time, O(1) Space
    static int minEnergy(int n, const vector<int>& heights) {
        if (n <= 1) return 0;

        int prev2 = 0; // energy to reach step 0
        int prev1 = abs(heights[1] - heights[0]); // energy to reach step 1

        for (int i = 2; i < n; ++i) {
            int jumpOne = prev1 + abs(heights[i] - heights[i - 1]);
            int jumpTwo = prev2 + abs(heights[i] - heights[i - 2]);
            int curr = min(jumpOne, jumpTwo);

            prev2 = prev1;
            prev1 = curr;
        }

        return prev1;
    }

    // Tabulation version: O(N) Time, O(N) Space (for clarity)
    static int minEnergyTabulation(int n, const vector<int>& heights) {
        if (n <= 1) return 0;
        vector<int> dp(n, 0);
        dp[0] = 0;
        dp[1] = abs(heights[1] - heights[0]);

        for (int i = 2; i < n; ++i) {
            int jumpOne = dp[i - 1] + abs(heights[i] - heights[i - 1]);
            int jumpTwo = dp[i - 2] + abs(heights[i] - heights[i - 2]);
            dp[i] = min(jumpOne, jumpTwo);
        }
        return dp[n - 1];
    }

    // EXTENSION: Frog Jump with K steps — O(N*K) Time, O(N) Space
    // dp[i] = min energy to reach stone i, can jump 1..K steps
    static int minEnergyKSteps(int n, const vector<int>& heights, int k) {
        vector<int> dp(n, INT_MAX);
        dp[0] = 0;

        for (int i = 1; i < n; ++i) {
            for (int j = 1; j <= k && j <= i; ++j) {
                if (dp[i - j] != INT_MAX) {
                    int cost = dp[i - j] + abs(heights[i] - heights[i - j]);
                    dp[i] = min(dp[i], cost);
                }
            }
        }
        return dp[n - 1];
    }
};

int main() {
    vector<int> heights = {10, 20, 30, 10};
    int n = heights.size();
    cout << "Min Energy (2-step): " << FrogJump::minEnergy(n, heights) << endl; // Output: 20
    cout << "Min Energy (3-step): " << FrogJump::minEnergyKSteps(n, heights, 3) << endl; // Output: 20
    return 0;
}
```

---

## 🔍 Dry Run Trace — `heights = [10, 20, 30, 10]`

```
n=4

Initial:
  prev2 = 0                         (dp[0] = 0, start at stone 0)
  prev1 = |20 - 10| = 10            (dp[1] = 10, only path: 0→1)

i=2: heights[2]=30
  jumpOne = prev1 + |30-20| = 10+10 = 20  (path via stone 1)
  jumpTwo = prev2 + |30-10| = 0+20  = 20  (path via stone 0)
  curr = min(20, 20) = 20
  prev2=10, prev1=20

i=3: heights[3]=10
  jumpOne = prev1 + |10-30| = 20+20 = 40  (path via stone 2)
  jumpTwo = prev2 + |10-20| = 10+10 = 20  (path via stone 1)
  curr = min(40, 20) = 20
  prev2=20, prev1=20

Return prev1 = 20 ✓

Optimal path: 0 → 1 → 3 (skipping stone 2)
Cost: |20-10| + |10-20| = 10 + 10 = 20 ✓
```

---

## ⚠️ Common Interview Mistakes

1. **Confusing this with Climbing Stairs:** Climbing Stairs counts ways (additive). Frog Jump minimizes cost (min operator). Same skeleton, different semantics.
2. **Wrong base case for `dp[1]`:** `dp[1]` is NOT 0. The frog PAYS energy to jump from stone 0 to stone 1: `|heights[1] - heights[0]|`.
3. **Forgetting `dp[0] = 0`:** The frog starts at stone 0 with zero energy spent.
4. **In K-step version, not initializing `dp` to `INT_MAX`:** If you leave `dp` at 0, every state looks "reachable for free." Use `INT_MAX` and check before adding.
5. **Arithmetic overflow in K-step version:** `dp[i-j] + cost` where `dp[i-j] = INT_MAX` causes overflow. Guard with `if (dp[i-j] != INT_MAX)`.
6. **Greedy mistake:** "Always jump to the stone with lowest height difference" — this can miss globally cheaper paths that pass through a costly intermediate step.

---

## 📊 Complexity Analysis

| Approach | Time | Space | Notes |
|---|---|---|---|
| Space-Optimized (2-step) | $O(N)$ | $O(1)$ | Optimal |
| Tabulation (2-step) | $O(N)$ | $O(N)$ | Easier to trace |
| K-step generalization | $O(N \cdot K)$ | $O(N)$ | Inner loop over jump sizes |

**Intuition for O(N·K):** For each of the $N$ stones, we consider at most $K$ possible predecessors. Total work = $N \times K$.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] How is Frog Jump different from Climbing Stairs? Both use 1 and 2 steps.
**Answer:** Three key differences:
1. **Objective:** Climbing Stairs **counts** ways (additive, uses `+`). Frog Jump **minimizes** cost (uses `min`).
2. **Cost function:** Climbing Stairs has uniform cost per step (1). Frog Jump has variable cost `|heights[i] - heights[j]|` depending on the actual height difference.
3. **Direction of optimization:** Climbing Stairs accumulates sums. Frog Jump finds the minimum accumulated cost. The recurrence structure is the same, but the operator changes from `sum` to `min`.

---

### Q2: [Extension] Generalize: Frog can jump up to K steps. Derive the recurrence and complexity.
**Answer:**
$$dp[i] = \min_{j=1}^{\min(K,i)} \left( dp[i-j] + |height[i] - height[i-j]| \right)$$

Time: $O(N \cdot K)$ — for each stone, try at most $K$ predecessors.
Space: $O(N)$ for the DP array (can't reduce to $O(1)$ since we need arbitrary lookback).

If $K = N$ (can jump to any stone), this becomes $O(N^2)$. If $K$ is large, this might be optimizable with a sliding window minimum (like the monotonic deque trick), but that's an advanced optimization.

---

### Q3: [Output Prediction] What does this return for `heights = [10, 20, 30, 10]`?
```cpp
int minEnergy(int n, const vector<int>& heights) {
    if (n <= 1) return 0;
    int prev2 = 0;
    int prev1 = 0; // BUG: should be abs(heights[1]-heights[0])
    for (int i = 2; i < n; ++i) {
        int j1 = prev1 + abs(heights[i] - heights[i-1]);
        int j2 = prev2 + abs(heights[i] - heights[i-2]);
        int curr = min(j1, j2);
        prev2 = prev1; prev1 = curr;
    }
    return prev1;
}
```
**Answer:** Bug: `prev1` is initialized to 0 instead of `|heights[1]-heights[0]| = 10`. For `heights=[10,20,30,10]`:
- i=2: j1 = 0+10=10, j2 = 0+20=20 → curr=10. (Wrong: treats stone 1 as having 0 cost to reach)
- i=3: j1 = 10+20=30, j2 = 10+10=20 → curr=20.
- Returns 20. **Happens to give correct answer by coincidence** for this input! But for `heights=[30,10,20]`, correct answer is `|10-30|=20` then `|20-10|=10` = total 30 via stone 0→1→2, OR `|20-30|=10` via 0→2. Correct=10. With the bug: prev1=0, i=2: j1=0+10=10, j2=0+10=10 → curr=10. Gives 10 (still "correct" by coincidence). The bug will surface on inputs where `heights[0]→heights[1]` cost matters as a prerequisite.

---

### Q4: [System Design] If heights are given as a stream (online), can you still solve this?
**Answer:** Yes — the space-optimized approach processes stones left-to-right using only 2 previous values. You don't need the full array ahead of time. Simply read each height as it arrives and update `prev2` and `prev1` accordingly. This is a streaming/online algorithm with $O(1)$ memory.

---

### Q5: [Variant] What if you want to find the actual path (not just the minimum cost)?
**Answer:** You need the full `dp` array to backtrack. After computing all `dp[i]`, start at stone `n-1` and work backwards:
```
path = [n-1]
i = n-1
while i > 0:
    if i >= 2 and dp[i] == dp[i-2] + |h[i]-h[i-2]|:
        i -= 2  # came from stone i-2
    else:
        i -= 1  # came from stone i-1
    path.push(i)
reverse(path)
```
This requires $O(N)$ space to store `dp`. Can't reconstruct from the 2-variable version.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Insight |
|---|---|---|
| 746 | Min Cost Climbing Stairs | Same DP, uniform-direction costs |
| 983 | Minimum Cost for Tickets | 1D DP with 3 jump options (1,7,30 days) |
| 1696 | Jump Game VI | K-step frog jump — optimized with monotonic deque to O(N) |
| 45 | Jump Game II | Greedy works here because cost = #jumps (uniform) |
| 1335 | Minimum Difficulty of a Job Schedule | K-step DP on partitions |

---

## 🔗 Cross-Topic Connections
- **Climbing Stairs:** Same structure, different objective (count vs minimize).
- **Min Cost Climbing Stairs (LC 746):** Very similar — cost at each step, minimize to reach top.
- **Jump Game VI (LC 1696):** K-step Frog Jump, optimized with sliding window maximum (monotone deque) to $O(N)$.
- **Dijkstra's Algorithm:** Frog Jump is essentially shortest-path on a DAG (directed acyclic graph where each node connects to next 1 and 2 nodes). DP on DAGs is equivalent to Dijkstra with edge weights.
- **Segment Tree / Monotone Deque:** For K-step optimization, use a max-deque to maintain the minimum `dp[i-j]` in a sliding window.

---

## ⚡ 2-Minute Revision Flash Card
- **State:** `dp[i]` = minimum energy to reach stone $i$.
- **Recurrence:** $dp[i] = \min(dp[i-1] + |h[i]-h[i-1]|,\; dp[i-2] + |h[i]-h[i-2]|)$.
- **Base cases:** `dp[0] = 0`, `dp[1] = |h[1]-h[0]|`.
- **Key difference from Climbing Stairs:** Cost varies by height difference; use `min`, not `sum`.
- **K-step extension:** Inner loop tries all $j \in [1,K]$; time becomes $O(NK)$; use monotone deque for $O(N)$.
