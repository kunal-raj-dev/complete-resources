# Lecture 140: DP 4: House Robber II: Circular Neighborhood (LeetCode 213)

> **One-Line Purpose:** Solve the circular house robber problem where house 0 and house $N-1$ are adjacent, reducing circular constraints to two independent linear House Robber subproblems in $O(N)$ time and $O(1)$ space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #140  
> **Video ID:** `hSMJj9AdNBo`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=hSMJj9AdNBo)  
> **Duration:** 22:30  
> **Status:** AUDITED  

---

## 🧠 Core Intuition — The Circle Breaking Trick

### Why Circular DP is Different
In House Robber I, we robbed a **line** of houses. The recurrence worked because house 0 had no "left neighbor." Now houses form a **circle**, meaning house 0 and house $N-1$ share an alarm. The problem: if we rob house 0, we **cannot** rob house $N-1$, and vice versa.

### The Key Insight: Exhaustive Case Splitting
In any valid optimal solution, exactly one of these must be true:
- **Case 1:** House 0 is **NOT robbed** → houses `[1..N-1]` are unconstrained (linear problem!)
- **Case 2:** House $N-1$ is **NOT robbed** → houses `[0..N-2]` are unconstrained (linear problem!)

Note: Both houses can be skipped (covered by either case). The case where BOTH are robbed is illegal. By solving both linear sub-problems and taking the max, we cover every valid solution exactly.

```
Circular array:  [2, 3, 2]
                  0  1  2

Case 1 (exclude house 0): subarray = [3, 2]
  → House Robber on [3, 2] = 3

Case 2 (exclude house N-1=2): subarray = [2, 3]
  → House Robber on [2, 3] = 3

Answer = max(3, 3) = 3 ✓

Another example: [1, 2, 3, 1]
Case 1: rob [2, 3, 1] → dp = 2,3,3 → 4 (rob 2 and 1? no, rob 3: dp[1]=2, dp[2]=max(3,2+2)=4, dp[3]=max(4,1+2)=4) = 4
Case 2: rob [1, 2, 3] → dp[0]=1, dp[1]=2, dp[2]=max(2,3+1)=4 → answer=4

Answer = max(4, 4) = 4 ✓ (rob houses 0 and 2: 1+3=4)
```

### Why Splitting Into Two Linear Problems is Correct

**Formal proof:** Let $OPT$ be the optimal solution for the circular problem.
- If $OPT$ does not include house 0: then $OPT$ is a valid solution for the linear sub-problem `[1..N-1]`, so `case1 ≥ OPT`.
- If $OPT$ does not include house $N-1$: then $OPT$ is valid for `[0..N-2]`, so `case2 ≥ OPT`.
- Since at least one of the above must be true (both can't be robbed in $OPT$), $\max(\text{case1}, \text{case2}) \geq OPT$.
- Also, both case1 and case2 are valid sub-solutions → $\max(\text{case1}, \text{case2}) \leq OPT$.
- Therefore: $\max(\text{case1}, \text{case2}) = OPT$. $\square$

---

## 🔵 Circular Constraint Reduction
Because house $0$ and house $N-1$ are adjacent, they cannot both be robbed simultaneously. This creates 2 mutually exclusive linear scenarios:
1. **Exclude House $0$:** Rob within range $[1, N-1]$.
2. **Exclude House $N-1$:** Rob within range $[0, N-2]$.
$$\text{Answer} = \max(\text{robLinear}(0, N-2),\, \text{robLinear}(1, N-1))$$

---

## 💻 Complete C++ Implementation

```cpp
#include <vector>
#include <algorithm>
#include <iostream>

using namespace std;

class SolutionHouseRobberII {
private:
    // Linear House Robber on subarray nums[start..end]
    int robLinear(const vector<int>& nums, int start, int end) {
        int prev2 = 0;
        int prev1 = 0;

        for (int i = start; i <= end; ++i) {
            int curr = max(prev1, nums[i] + prev2);
            prev2 = prev1;
            prev1 = curr;
        }
        return prev1;
    }

public:
    int rob(vector<int>& nums) {
        int n = nums.size();
        if (n == 0) return 0;
        if (n == 1) return nums[0];
        if (n == 2) return max(nums[0], nums[1]);

        return max(robLinear(nums, 0, n - 2), robLinear(nums, 1, n - 1));
    }
};

int main() {
    SolutionHouseRobberII solver;
    vector<int> circularHouses = {2, 3, 2};
    cout << "Max Circular Loot: " << solver.rob(circularHouses) << endl; // Output: 3

    vector<int> ex2 = {1, 2, 3, 1};
    cout << "Max Circular Loot: " << solver.rob(ex2) << endl; // Output: 4
    return 0;
}
```

---

## 🔍 Dry Run Trace — `nums = [2, 3, 2]`

```
n = 3

---- Case 1: robLinear(0, 1) → nums[0..1] = [2, 3] ----
prev2=0, prev1=0
i=0: curr = max(0, 2+0) = 2.  prev2=0, prev1=2
i=1: curr = max(2, 3+0) = 3.  prev2=2, prev1=3
Result = 3

---- Case 2: robLinear(1, 2) → nums[1..2] = [3, 2] ----
prev2=0, prev1=0
i=1: curr = max(0, 3+0) = 3.  prev2=0, prev1=3
i=2: curr = max(3, 2+0) = 3.  prev2=3, prev1=3
Result = 3

Answer = max(3, 3) = 3 ✓
```

---

## 🔍 Dry Run Trace — `nums = [1, 2, 3, 1]`

```
n = 4

---- Case 1: robLinear(0, 2) → [1, 2, 3] ----
prev2=0, prev1=0
i=0: curr=max(0,1+0)=1.  prev2=0, prev1=1
i=1: curr=max(1,2+0)=2.  prev2=1, prev1=2
i=2: curr=max(2,3+1)=4.  prev2=2, prev1=4
Result = 4

---- Case 2: robLinear(1, 3) → [2, 3, 1] ----
prev2=0, prev1=0
i=1: curr=max(0,2+0)=2.  prev2=0, prev1=2
i=2: curr=max(2,3+0)=3.  prev2=2, prev1=3
i=3: curr=max(3,1+2)=3.  prev2=3, prev1=3
Result = 3

Answer = max(4, 3) = 4 ✓  (robbed houses 0 and 2: 1+3=4)
```

---

## ⚠️ Common Interview Mistakes

1. **Forgetting the `n==2` edge case:** With `n=2`, both `robLinear(0,0)` and `robLinear(1,1)` return single elements — the answer is `max(nums[0], nums[1])`. Without this guard, the code works anyway since `robLinear` handles single-element ranges, but it's good to state it explicitly.

2. **Trying to handle the circle with a modified recurrence:** Some candidates add a boolean flag "robbed house 0?" to the state. This becomes `dp[i][0/1]` — a valid 2-state DP but more complex. The two-pass approach is cleaner.

3. **Off-by-one in range:** `robLinear(0, n-2)` means including indices 0 through N-2 (excludes house N-1). `robLinear(1, n-1)` means including indices 1 through N-1 (excludes house 0). Any off-by-one here (e.g., `n-1` vs `n`) is a common bug.

4. **Three or more cycles:** What if the "circle" is more complex (e.g., houses on a grid with neighbor constraints)? This approach doesn't generalize. Would require proper graph DP or bitmask DP.

5. **All zeros:** `nums = [0, 0, 0]` → answer is 0. Code handles this correctly since `max(0, 0) = 0`.

---

## 📊 Complexity Analysis
- **Time Complexity:** $O(N)$ — two linear passes of $O(N)$ each, total $2N = O(N)$.
- **Space Complexity:** $O(1)$ — only four integer variables (`prev2`, `prev1`, `curr`, and loop counter), independent of $N$.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Proof] Why does splitting into two linear problems give the optimal answer for the circular case?
**Answer:** (Reproduced from Core Intuition for completeness)
In any valid optimal circular solution $OPT$, house 0 and house $N-1$ cannot both be included. Therefore:
- Either house 0 is excluded → $OPT$ is feasible for `[1..N-1]` → `case1 ≥ OPT`
- Or house $N-1$ is excluded → $OPT$ is feasible for `[0..N-2]` → `case2 ≥ OPT`

Both cases yield valid solutions for the circular problem, so $\max(\text{case1}, \text{case2}) = OPT$. The split is **lossless** because every valid circular solution is captured by at least one of the two linear sub-problems.

---

### Q2: [Conceptual] Can you solve House Robber II with a single DP pass (no two sub-problems)?
**Answer:** Yes, using a **2-state DP**: `dp[i][0]` = max loot up to house `i` when house 0 was NOT robbed; `dp[i][1]` = max loot when house 0 WAS robbed. This adds a dimension but avoids splitting. However, the two-pass approach is simpler, equally efficient, and more readable. The interviewer may ask you to describe both; prefer the two-pass for clarity.

---

### Q3: [Debugging] What is wrong with this solution?
```cpp
int rob(vector<int>& nums) {
    int n = nums.size();
    // Attempt: just add constraint that first and last can't both be selected
    vector<int> dp(n);
    dp[0] = nums[0];
    dp[1] = max(nums[0], nums[1]);
    for (int i = 2; i < n; ++i) {
        dp[i] = max(dp[i-1], nums[i] + dp[i-2]);
    }
    // "Fix" circular by subtracting if both ends were chosen
    return dp[n-1]; // BUG: ignores circular adjacency entirely
}
```
**Answer:** This is plain House Robber I — it doesn't handle the circular constraint at all. `dp[n-1]` might include both house 0 and house $N-1$ in the optimal combination. For `[2,3,2]`, this returns 4 (rob 2+2=4), but house 0 and house 2 are adjacent in a circle, so this is invalid. The correct answer is 3.

---

### Q4: [Extension] What if there are 3 houses and all values are equal, e.g., `[5, 5, 5]`?
**Answer:**
- `robLinear(0, 1)` on `[5, 5]` → `max(5, 5) = 5`
- `robLinear(1, 2)` on `[5, 5]` → `max(5, 5) = 5`
- Answer = `max(5, 5) = 5`

Correct: in a 3-house circle, you can only rob 1 house (any 2 adjacent houses, and with 3 total forming a circle, any 2 are adjacent to the third). Max = 5.

---

### Q5: [Variant] House Robber III (LeetCode 337): houses form a binary tree. Sketch the approach.
**Answer:** Tree DP via post-order DFS. At each node, return a pair `(rob, skip)`:
- `rob(node) = node->val + skip(left) + skip(right)`
- `skip(node) = max(rob(left), skip(left)) + max(rob(right), skip(right))`

Final answer: `max(rob(root), skip(root))`. Time: $O(N)$, Space: $O(H)$ recursion stack.

---

### Q6: [Complexity] What is the exact number of operations performed by the two-pass approach?
**Answer:**
- `robLinear(0, n-2)` performs exactly $N-1$ iterations.
- `robLinear(1, n-1)` performs exactly $N-1$ iterations.
- Total: $2(N-1)$ iterations + constant setup = $O(N)$.
- Space: 4 variables per call (prev2, prev1, curr, i) × 2 calls = 8 variables = $O(1)$.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Insight |
|---|---|---|
| 198 | House Robber | Base linear version |
| 213 | House Robber II | This problem — circle split trick |
| 337 | House Robber III | Tree DP — post-order rob/skip pairs |
| 3186 | Maximum Total Damage with Spell Casting | House Robber variant with sorted unique values |
| 213 variant | Circular Array Max Sum (No Adjacency) | Same two-split technique |

---

## 🔗 Cross-Topic Connections
- **House Robber I:** Direct prerequisite — this is HR I + circular constraint.
- **Tree DP (LC 337):** Generalizes the linear/circular to arbitrary graph topology.
- **Circular Array Problems:** The "split circle into two linear cases" trick applies broadly (e.g., Max Circular Subarray Sum using Kadane's on circular arrays).
- **Graph Coloring / Independent Sets:** House Robber is equivalent to finding Maximum Weight Independent Set on a path graph (or cycle graph for HR II).

---

## ⚡ 2-Minute Revision Flash Card
- **Key Insight:** House 0 and House $N-1$ can't BOTH be robbed in the circle.
- **Solution:** Run linear House Robber twice: on `[0..N-2]` and `[1..N-1]`. Take max.
- **Why it works:** Every valid solution excludes at least one endpoint, so both cases are covered.
- **Edge cases:** `n=1` → return `nums[0]`; `n=2` → return `max(nums[0], nums[1])`.
- **Proof:** By exhaustive case split — any optimal solution must fall into Case 1 or Case 2.
