# Lecture 49: Combination Sum: Unbounded Choice Backtracking (LeetCode 39)

> **One-Line Purpose:** Master the Unbounded Knapsack-style backtracking paradigm by picking elements with unlimited reuse, implementing arithmetic pruning to avoid negative target states.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #49  
> **Video ID:** `jkgZw2WEaqA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=jkgZw2WEaqA)  
> **Duration:** 23:35  
> **Transcript:** `.transcripts/12_recursion_and_backtracking/049_Combination_Sum_Problem___Recursion___Backtracking.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The requirements of LeetCode 39 (Combination Sum): finding all unique combinations of distinct integers summing to `target`.
- Why elements can be chosen **unlimited times**, and how this modifies the recursive transition (staying at index `i` vs advancing to `i + 1`).
- The Include / Skip decision logic and base-case termination when `target == 0` or `target < 0`.
- How sorting the candidate array allows **early break pruning** to eliminate unpromising branches.

---

## 🔵 Lecture Context

Combination Sum introduces unbounded element selection, bridging combinatorial backtracking with Unbounded Knapsack and Coin Change in Dynamic Programming.

---

## 1. Problem Statement

Given an array of **distinct** integers `candidates` and a target integer `target`, return a list of all **unique combinations** where the chosen numbers sum to `target`.
- The same number may be chosen from `candidates` an **unlimited number of times**.
- Two combinations are unique if the frequency of at least one chosen number is different.

```
Input: candidates = [2, 3, 6, 7], target = 7
Output: [[2, 2, 3], [7]]
```

---

## 2. Core Idea: The Unbounded Pick Decision Tree

At each candidate index `i`:
1. **Option 1 (Pick):** If `candidates[i] <= target`:
   - Subtract `candidates[i]` from `target`.
   - Add `candidates[i]` to `current`.
   - **Crucial Invariant:** Recurse with the **SAME index `i`** (not `i + 1`), because we are allowed to pick `candidates[i]` again!
   - Backtrack: pop `candidates[i]` and restore `target`.
2. **Option 2 (Skip):**
   - Advance to index `i + 1` to consider subsequent candidates without picking `candidates[i]`.

---

## 3. Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    void backtrack(const vector<int>& candidates, int target, int i, vector<int>& current, vector<vector<int>>& result) {
        // Base Case 1: Target reached
        if (target == 0) {
            result.push_back(current);
            return;
        }

        // Base Case 2: Exceeded target or exhausted candidates
        if (target < 0 || i == candidates.size()) {
            return;
        }

        // Option 1: Include candidates[i] (stay at index i for unbounded reuse)
        if (candidates[i] <= target) {
            current.push_back(candidates[i]);
            backtrack(candidates, target - candidates[i], i, current, result);
            current.pop_back(); // Backtrack
        }

        // Option 2: Skip candidates[i] (advance to i + 1)
        backtrack(candidates, target, i + 1, current, result);
    }

    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        sort(candidates.begin(), candidates.end()); // Sorting allows early pruning
        vector<vector<int>> result;
        vector<int> current;
        backtrack(candidates, target, 0, current, result);
        return result;
    }
};

int main() {
    Solution solver;
    vector<int> candidates = {2, 3, 6, 7};
    int target = 7;
    vector<vector<int>> ans = solver.combinationSum(candidates, target);

    cout << "Combinations for target " << target << ":\n";
    for (const auto& comb : ans) {
        cout << "[ ";
        for (int x : comb) cout << x << " ";
        cout << "]\n";
    }
    return 0;
}
```

---

## 🔍 Detailed Trace: `candidates = [2, 3]`, `target = 5`

```
(i=0, val=2, target=5)
- Pick 2 -> target=3. Path: [2]
  - Pick 2 -> target=1. Path: [2, 2]
    - Pick 2 -> target=-1 (target < 0 -> Prune & backtrack)
    - Skip 2 -> (i=1, val=3, target=1)
      - Pick 3 -> target=-2 (Prune)
      - Skip 3 -> exhausted.
  - Skip 2 -> (i=1, val=3, target=3). Path: [2]
    - Pick 3 -> target=0 -> MATCH! Record [2, 3]
    - Skip 3 -> exhausted.
- Skip 2 -> (i=1, val=3, target=5). Path: []
  - Pick 3 -> target=2. Path: [3]
    ...
```

---

## 🧠 Mental Model: Coin Dispenser

Imagine a coin dispenser with infinite coins of denominations $2, 3, 6, 7$. You repeatedly push the coin 2 button until total exceeds target. Then you take back one coin and push the coin 3 button.

---

## ⚠️ Common Mistakes

1. **Advancing `i + 1` on Pick:** Passing `i + 1` after picking `candidates[i]` restricts each number to single use (solving 0/1 Knapsack instead of Unbounded Knapsack).
2. **Infinite Loops from Zero Values:** If candidates could contain `0`, picking `0` without reducing target causes infinite recursion. (LeetCode 39 guarantees candidates $\ge 2$).

---

## 🖥️ System-Specific Notes

- **Max Tree Depth:** Since the minimum candidate value is $2$, the maximum recursion depth is bounded by $\frac{\text{target}}{2}$. For `target = 40`, depth $\le 20$ frames ($\approx 1\text{ KB}$).

---

## 🟡 Additional Essential Context

In LeetCode 40 (Combination Sum II):
- Each candidate can only be used **once** (advance `i + 1`).
- The array may contain **duplicates**, requiring the duplicate skipping check: `if (j > i && candidates[j] == candidates[j-1]) continue;`.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why does this generate unique combinations without duplicates like `[2, 3, 2]` and `[3, 2, 2]`?  
**A:** Because we only consider elements at or after index `i`. Once we skip `candidates[0]` (2) to move to `candidates[1]` (3), we can never pick `2` again! This directional invariant guarantees uniqueness.

---

### 🔥 Interview Questions

#### Q1: What is the time complexity bound for Combination Sum?
- **Short Answer:** $O(2^T \cdot K)$ where $T = \text{target} / \text{min\_val}$ and $K$ is average combination length.
- **Detailed Explanation:** In the worst case (e.g. `candidates = [1]`), the tree branches up to $T$ levels deep. Loose upper bound is exponential in target value.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
// candidates = [2], target = 3
// Output: [] (No solution possible)
```

---

## Edge Cases

1. **Target Smaller Than Smallest Candidate:** `candidates = [5, 10], target = 3` $\to$ Returns `[]`.
2. **Exact Single Match:** `candidates = [7], target = 7` $\to$ Returns `[[7]]`.

---

## Complexity Analysis

- **Time Complexity:** $O(2^T \cdot K)$ where $T = \text{target} / \text{min(candidates)}$.
- **Auxiliary Space Complexity:** $O(T)$ stack frames.

---

## Key Takeaways

1. **Unbounded selection:** Recurse with index `i` on pick; advance to `i + 1` on skip.
2. **Target reduction:** `target - candidates[i]`.
3. **Directional order:** Eliminates permutation duplicates automatically.

---

## ⚡ 2-Minute Revision

- Pick: `backtrack(target - candidates[i], i)`.
- Skip: `backtrack(target, i + 1)`.
- Stop when `target == 0` or `target < 0`.
