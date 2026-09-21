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
- Master the Unbounded Knapsack-style backtracking paradigm by picking elements with unlimited reuse.
- Understand how sorting candidates allows for **early break pruning** to avoid exploring invalid (negative target) states.
- Learn why advancing to index `i` (instead of `i + 1`) allows unlimited reuse of the same element, while still preventing duplicate permutations.

## 🧠 Core Intuition — Why This Works
Combination Sum introduces the concept of **unbounded selection**. 
Imagine a coin dispenser where you have an infinite supply of specific coins (e.g., $2, $3, $6, $7).
You want to make exact change for $7.
You can repeatedly press the $2 button. If you go over the target, you "backtrack" (take the coin out) and try the $3 button.
To avoid duplicate combinations like `[2, 3, 2]` and `[3, 2, 2]`, we enforce an **order**. Once we decide to stop using the $2 coin and move to the $3 coin, we can *never* go back to the $2 coin.

**Visualization (Recursion Tree for `candidates=[2,3], target=5`):**
```text
                          f(i=0, T=5, [])
                         /               \
            Pick 2      /                 \ Skip 2
          f(0, T=3, [2])                   f(1, T=5, [])
           /         \                         /        \
    Pick 2/           \Skip 2           Pick 3/          \Skip 3
f(0, 1, [2,2])   f(1, 3, [2])       f(1, 2, [3])      f(2, 5, []) (End)
    /      \           |                   |
Pick 2    Skip 2     Pick 3              Pick 3
f(0,-1) f(1,1,[2,2]) f(1,0,[2,3])    f(1, -1) 
(Pruned)     |       (✅ MATCH!)       (Pruned)
           Pick 3
         f(1,-2) (Pruned)
```

## 🎯 Pattern Recognition — When to Use This
**Trigger cues:**
- "Find all combinations summing to target" + "Elements can be chosen an unlimited number of times" → **Backtracking with `i` instead of `i + 1`**.
- Unbounded Knapsack DP problems (where you only need the max/min value instead of all paths).

## 📐 Algorithm Walk-Through
At each candidate index `i`:
1. **Base Case (Success):** If `target == 0`, add `current` path to `result`.
2. **Base Case (Failure):** If `target < 0` or we exhaust candidates (`i == size`), return.
3. **Option 1 (Pick):** If `candidates[i] <= target`:
   - Add `candidates[i]` to `current`.
   - **Recurse with the SAME index `i`** (`target - candidates[i]`).
   - Backtrack: pop `candidates[i]`.
4. **Option 2 (Skip):**
   - Recurse with index `i + 1` (`target` remains the same).

## 🔵 Complete C++ Implementation

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

## 🔍 Dry Run Trace
*(Covered in the Core Intuition visualization above)*

## ⚠️ Common Interview Mistakes
- **Advancing `i + 1` on Pick:** Passing `i + 1` after picking `candidates[i]` restricts each number to single use (this solves Combination Sum II / 0-1 Knapsack, not unbounded).
- **Generating Permutations instead of Combinations:** Using a `for (int j = 0; j < candidates.size(); ++j)` loop starting from `0` every time. This creates duplicate sets like `[2,3,2]` and `[2,2,3]`. You must start the loop from `i`, or use the Pick/Skip logic above.
- **Infinite Loops from Zero Values:** If candidates could contain `0`, picking `0` without reducing target causes infinite recursion. (LeetCode 39 guarantees candidates $\ge 2$).

## 📊 Complexity Analysis
- **Time Complexity:** $O(2^T \cdot K)$ where $T = \frac{\text{target}}{\text{min\_val}}$ (the maximum depth of the tree) and $K$ is the average length of a combination. In the worst case, every node in the exponential tree could be valid, and copying the array to the result takes $O(K)$.
- **Space Complexity:** $O(T)$ auxiliary stack space for the recursion depth. For `target = 40` and `min_val = 2`, max depth is 20 frames.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: [Conceptual] Why does passing the index `i` forward prevent duplicate combinations?
**Answer:** Because it enforces a strict ordering. Once we move to index `i=1` (value 3), we can only pick 3s, 6s, and 7s. We can never go back to pick a 2. This guarantees that `[2, 3, 2]` is impossible to generate; only the sorted version `[2, 2, 3]` is produced.

### Q2: [Optimization] How does sorting the candidates array help?
**Answer:** Sorting allows us to break early. In a loop-based implementation `for(int j = i; j < n; j++)`, if `candidates[j] > target`, we can immediately `break` the loop because all subsequent elements will also be greater than the target. This prunes massive dead branches of the recursion tree.

### Q3: [Variant] How does this differ from Coin Change? (LeetCode 322)
**Answer:** Combination Sum asks for *all unique paths* (the exact combinations), which forces us to use Backtracking (exponential time). Coin Change asks for the *minimum number of coins*, which allows us to use Dynamic Programming (polynomial time $O(\text{target} \times N)$) because we only store the optimal answer for subproblems, not the actual paths.

### Q4: [Edge Case] What if the target is 0?
**Answer:** The algorithm immediately hits the base case `target == 0` and adds an empty list `[]` to the result, returning `[[]]`.

### Q5: [Complexity] Is it possible to tightly bound the time complexity?
**Answer:** It's notoriously difficult. $O(2^T)$ is a loose upper bound. The exact number of combinations is related to the partition function from number theory, making the exact time complexity heavily dependent on the specific values in the `candidates` array.

## 🏆 Related Problems (Leetcode)
- **Leetcode 40:** Combination Sum II (Medium) - *Each number used only once, array contains duplicates.*
- **Leetcode 216:** Combination Sum III (Medium) - *Exactly $k$ numbers, digits 1-9.*
- **Leetcode 377:** Combination Sum IV (Medium) - *Permutations are distinct, DP approach.*
- **Leetcode 322:** Coin Change (Medium) - *Optimization version of the same unbounded choice.*

## 🔗 Cross-Topic Connections
- **Dynamic Programming (Unbounded Knapsack):** The pick/skip recursion state (`i`, `target`) is identical to the memoization state in DP problems like Coin Change or Rod Cutting.

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Find combinations summing to target with unlimited reuse.
- **Pick:** `backtrack(target - candidates[i], i)` (Keep `i` to allow reuse!).
- **Skip:** `backtrack(target, i + 1)` (Move on to next).
- **Base Cases:** `target == 0` (Add to result), `target < 0` or `i == N` (Return).
- **No Duplicates:** Directional picking (never look back to `i-1`) prevents `[2,3,2]` vs `[2,2,3]`.
