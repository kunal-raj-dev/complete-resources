# Lecture 139: DP 3: House Robber (LeetCode 198)

> **One-Line Purpose:** Maximize stolen loot from a linear row of houses where adjacent houses have linked security systems, using the "Pick vs Don't Pick" DP recurrence.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #139  
> **Video ID:** `BRmLlJA6ncI`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=BRmLlJA6ncI)  
> **Duration:** 25:43  
> **Status:** AUDITED  

---

## 🧠 Core Intuition — The Binary Choice

### The Mental Model
At every house you face a **binary decision**:
- **Rob it:** Gain `nums[i]`, but house `i-1` is automatically skipped (alarm would trigger). Your total becomes `nums[i] + best_from[0..i-2]`.
- **Skip it:** Don't rob house `i`. Your total is just `best_from[0..i-1]`.

You want the best of these two options **at every house**. This is the "Pick vs Don't Pick" paradigm — the most common DP structure in existence.

```
Houses: [2, 7, 9, 3, 1]
         0   1   2   3   4

At house 4 (val=1):
  Option A (ROB):   1 + dp[2] = 1 + 11 = 12
  Option B (SKIP):  dp[3]     = 11
  Choice: max(12, 11) = 12

At house 3 (val=3):
  Option A (ROB):   3 + dp[1] = 3 + 7 = 10
  Option B (SKIP):  dp[2]     = 11
  Choice: max(10, 11) = 11

At house 2 (val=9):
  Option A (ROB):   9 + dp[0] = 9 + 2 = 11
  Option B (SKIP):  dp[1]     = 7
  Choice: max(11, 7) = 11

At house 1 (val=7):
  Option A (ROB):   7 + 0 = 7   (dp[-1] = 0 by convention)
  Option B (SKIP):  dp[0] = 2
  Choice: max(7, 2) = 7

At house 0 (val=2):
  Only option: dp[0] = 2
```

### Why Greedy Fails
A greedy approach (always rob the highest-value visible house) fails. Consider `[10, 1, 10]`. Greedy might pick the middle house first? No — greedy by value density here is ambiguous. The point: you cannot decide to rob house 2 without knowing if you robbed house 0. DP captures this dependency.

---

## 🔵 Recurrence Formulation: Pick vs Don't Pick
At house $i$:
1. **Rob house $i$:** Gain `nums[i]` + maximum loot from non-adjacent houses up to $i-2$: `nums[i] + dp[i-2]`.
2. **Skip house $i$:** Gain maximum loot up to house $i-1$: `dp[i-1]`.
$$\text{dp}[i] = \max(\text{dp}[i - 1],\, \text{nums}[i] + \text{dp}[i - 2])$$

---

## 📐 The 4-Step DP Framework Applied

**Step 1: State Definition**
`dp[i]` = maximum money that can be robbed from houses `[0..i]`.

**Step 2: Recurrence**
$dp[i] = \max(dp[i-1],\; \text{nums}[i] + dp[i-2])$

The invariant: `dp[i]` always stores the maximum achievable loot considering all houses up to index `i`. We never violate the adjacency constraint because robbing house `i` always pairs with `dp[i-2]`, not `dp[i-1]`.

**Step 3: Base Cases**
- `dp[-1] = 0` (conceptually: no houses → 0 loot; implemented as `prev2 = 0`)
- `dp[0] = nums[0]` (only one house: rob it)

**Step 4: Space Optimize**
`dp[i]` depends only on `dp[i-1]` and `dp[i-2]` → two rolling variables suffice.

---

## 💻 Complete C++ Implementation

```cpp
#include <vector>
#include <algorithm>
#include <iostream>

using namespace std;

class SolutionHouseRobber {
public:
    // Approach 1: Tabulation — O(N) Time, O(N) Space
    int robTabulation(vector<int>& nums) {
        int n = nums.size();
        if (n == 0) return 0;
        if (n == 1) return nums[0];

        vector<int> dp(n);
        dp[0] = nums[0];
        dp[1] = max(nums[0], nums[1]);

        for (int i = 2; i < n; ++i) {
            dp[i] = max(dp[i - 1], nums[i] + dp[i - 2]);
        }
        return dp[n - 1];
    }

    // Approach 2: Space-Optimized — O(N) Time, O(1) Space
    int rob(vector<int>& nums) {
        int n = nums.size();
        if (n == 0) return 0;
        if (n == 1) return nums[0];

        int prev2 = 0;           // dp[i-2]
        int prev1 = nums[0];     // dp[i-1]

        for (int i = 1; i < n; ++i) {
            int pick = nums[i] + prev2;
            int notPick = prev1;
            int curr = max(pick, notPick);

            prev2 = prev1;
            prev1 = curr;
        }

        return prev1;
    }

    // Approach 3: Memoization — O(N) Time, O(N) Space
    int robHelper(int i, vector<int>& nums, vector<int>& memo) {
        if (i < 0) return 0;
        if (i == 0) return nums[0];
        if (memo[i] != -1) return memo[i];
        int pick = nums[i] + robHelper(i - 2, nums, memo);
        int notPick = robHelper(i - 1, nums, memo);
        return memo[i] = max(pick, notPick);
    }
    int robMemo(vector<int>& nums) {
        int n = nums.size();
        vector<int> memo(n, -1);
        return robHelper(n - 1, nums, memo);
    }
};

int main() {
    SolutionHouseRobber solver;
    vector<int> houses = {2, 7, 9, 3, 1};
    cout << "Max Loot: " << solver.rob(houses) << endl; // Output: 12 (2 + 9 + 1)
    return 0;
}
```

---

## 🔍 Dry Run Trace — `nums = [2, 7, 9, 3, 1]`

```
Initial: prev2 = 0, prev1 = nums[0] = 2

i=1: nums[1]=7
  pick    = 7 + prev2 = 7 + 0 = 7
  notPick = prev1 = 2
  curr    = max(7, 2) = 7
  prev2=2, prev1=7

i=2: nums[2]=9
  pick    = 9 + prev2 = 9 + 2 = 11
  notPick = prev1 = 7
  curr    = max(11, 7) = 11
  prev2=7, prev1=11

i=3: nums[3]=3
  pick    = 3 + prev2 = 3 + 7 = 10
  notPick = prev1 = 11
  curr    = max(10, 11) = 11
  prev2=11, prev1=11

i=4: nums[4]=1
  pick    = 1 + prev2 = 1 + 11 = 12
  notPick = prev1 = 11
  curr    = max(12, 11) = 12
  prev2=11, prev1=12

Return prev1 = 12 ✓  (robbed houses 0, 2, 4: 2+9+1=12)
```

---

## ⚠️ Common Interview Mistakes

1. **Initializing `dp[1] = nums[1]` instead of `dp[1] = max(nums[0], nums[1])`:** When using tabulation, `dp[1]` must be the best choice among the first TWO houses, not just house 1.
2. **Off-by-one in space-optimized version:** Starting `prev2 = nums[0]` and `prev1 = nums[1]` without comparing them first. The correct init: `prev2 = 0`, `prev1 = nums[0]`, then loop starts at `i=1`.
3. **Not handling `n=1`:** With `n=1`, the loop doesn't execute and you rely on the initial value. Always add the `n==1` guard.
4. **Confusing indices:** In the space-optimized version, `prev2` corresponds to `dp[i-2]` and `prev1` to `dp[i-1]`. Update `prev2 = prev1` BEFORE updating `prev1`.
5. **Interviewer extension: "What if you can skip at most 2 consecutive houses?"** — This changes the recurrence: can rob `i` if you skipped only `i-1`, or skipped `i-1` AND `i-2`. State needs rethinking.

---

## 📊 Complexity Analysis
- **Time Complexity:** $O(N)$ — single linear pass over the array.
- **Space Complexity:** $O(1)$ — two integer variables, independent of $N$.
- **Why O(1) space is possible:** The recurrence `dp[i] = max(dp[i-1], nums[i] + dp[i-2])` only looks back 2 positions, so only 2 past values need to be retained.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] Prove that the greedy "always rob the maximum nearby house" strategy fails.
**Answer:** Counterexample: `nums = [4, 1, 1, 4]`. Greedy might rob index 0 (value 4) and then index 3 (value 4) = 8 total. But if it robbed index 3 first and greedy goes left, it might pick index 1. The point is greedy has no consistent strategy. The optimal is `4 + 4 = 8` (houses 0 and 3), but greedy with "pick max, skip neighbors" can fail on `[4, 1, 4, 1, 4]` — correct answer is 4+4+4=12, greedy might get 4+4=8 if it greedily picks the three visible maxes wrong. DP is necessary.

---

### Q2: [Extension] What is the follow-up when houses are arranged in a circle? (House Robber II)
**Answer:** In a circle, house 0 and house $N-1$ are adjacent. The key insight: they **cannot both** be robbed. So split into two independent linear sub-problems:
- Run House Robber on `nums[0..N-2]` (exclude last house)
- Run House Robber on `nums[1..N-1]` (exclude first house)
- Answer = max of both results

This works because any optimal circular solution either excludes house 0 or excludes house N-1 (or both). By taking max of both scenarios, we cover all valid combinations. See Lecture 140.

---

### Q3: [Debugging] Identify the bug:
```cpp
int rob(vector<int>& nums) {
    int n = nums.size();
    int prev2 = nums[0], prev1 = nums[1]; // BUG for n==1, and wrong semantics
    for (int i = 2; i < n; ++i) {
        int curr = max(prev1, nums[i] + prev2);
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```
**Answer:** Two bugs:
1. **Crash for `n==1`:** `nums[1]` is out of bounds.
2. **Wrong semantics for `prev1`:** `prev1 = nums[1]` means "only consider house 1". But the optimal for the first 2 houses is `max(nums[0], nums[1])`. Fix: `prev2 = 0; prev1 = nums[0];` and start loop at `i=1`.

---

### Q4: [Extension] How do you reconstruct WHICH houses were robbed (not just the max value)?
**Answer:** Store the full `dp` array (can't reconstruct from 2 variables). Then backtrack:
```cpp
vector<int> getSelectedHouses(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(n);
    dp[0] = nums[0];
    if (n > 1) dp[1] = max(nums[0], nums[1]);
    for (int i = 2; i < n; ++i)
        dp[i] = max(dp[i-1], nums[i] + dp[i-2]);

    vector<int> selected;
    int i = n - 1;
    while (i >= 0) {
        if (i == 0 || dp[i] != dp[i-1]) {
            // This house was robbed
            selected.push_back(i);
            i -= 2; // Skip adjacent
        } else {
            i -= 1; // This house was skipped
        }
    }
    return selected; // Reverse for correct order
}
```

---

### Q5: [Complexity] Can House Robber be solved in O(1) space without two passes? Prove it.
**Answer:** Yes. The space-optimized solution using `prev1` and `prev2` does it in a **single pass** with $O(1)$ space. We don't need to store the full `dp` array because `dp[i]` only references `dp[i-1]` and `dp[i-2]`. Proof of correctness: at any step $i$, `prev1` holds the exact value of `dp[i-1]` and `prev2` holds `dp[i-2]`. The update `curr = max(prev1, nums[i] + prev2)` correctly computes `dp[i]`. After the loop, `prev1 = dp[n-1]` = answer.

---

### Q6: [Variant] House Robber III — houses arranged as a binary tree. How do you approach it?
**Answer:** This is **Tree DP** (LeetCode 337). For each node, compute two values:
- `rob_node`: max loot if we rob this node (cannot rob its children)
- `skip_node`: max loot if we skip this node (children can be robbed or skipped)

```
rob_node  = node->val + skip(left) + skip(right)
skip_node = max(rob(left), skip(left)) + max(rob(right), skip(right))
```

Post-order DFS, return pair `{rob, skip}` for each subtree. Time: $O(N)$, Space: $O(H)$ where $H$ is tree height.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Insight |
|---|---|---|
| 198 | House Robber | This problem — 1D Pick/Skip DP |
| 213 | House Robber II | Circular: two linear runs |
| 337 | House Robber III | Tree DP: post-order DFS with rob/skip pairs |
| 740 | Delete and Earn | Convert to house robber on frequency array |
| 2560 | House Robber IV | Binary search + greedy on the answer |

---

## 🔗 Cross-Topic Connections
- **Climbing Stairs:** Same Fibonacci structure, different operation (max vs sum).
- **House Robber II:** Direct extension — handle circular constraint by splitting.
- **Delete and Earn (LC 740):** If you "earn" value `v`, you must delete all `v-1` and `v+1`. After bucketing by value, this reduces exactly to House Robber on the frequency-value product array.
- **Maximum Sum of Non-Adjacent Elements:** Identical formulation — same solution, different name.
- **Tree DP (LC 337):** Generalizes House Robber from linear to arbitrary tree structures.

---

## ⚡ 2-Minute Revision Flash Card
- **State:** `dp[i]` = max loot from houses `[0..i]`.
- **Recurrence:** $dp[i] = \max(dp[i-1],\; \text{nums}[i] + dp[i-2])$.
- **Base cases:** `prev2 = 0` (no houses), `prev1 = nums[0]` (first house only). Loop from `i=1`.
- **Adjacency constraint enforced by:** using `dp[i-2]` (not `dp[i-1]`) when robbing house `i`.
- **Follow-up circles → House Robber II:** Run twice on `[0..N-2]` and `[1..N-1]`, take max.
