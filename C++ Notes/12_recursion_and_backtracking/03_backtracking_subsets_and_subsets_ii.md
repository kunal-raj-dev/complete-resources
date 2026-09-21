# Lecture 44: Backtracking: Subsets & Subsets II (Handling Duplicates)

> **One-Line Purpose:** Master combinatorial backtracking using the Include/Exclude choice paradigm to generate Power Sets (LeetCode 78) and prune duplicate branches via element sorting (LeetCode 90).

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #44  
> **Video ID:** `pNzljlzDCiI`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=pNzljlzDCiI)  
> **Duration:** 42:20  
> **Transcript:** `.transcripts/12_recursion_and_backtracking/044_Recursion_Part_3___Backtracking_in_Detail___Print_all_Subsets___Subsets_II.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The fundamental definition of **Backtracking**: exploring paths in a state-space tree, detecting invalid/complete states, and undoing choices (backtracking) to explore alternatives.
- How to generate all subsets (Power Set) of a distinct collection in $O(N \cdot 2^N)$ time using binary decision trees (Include vs Exclude).
- The state restoration step (`pop_back()`) that differentiates backtracking from simple recursion.
- How to solve **Subsets II (LeetCode 90)** when the input array contains duplicate elements.
- The duplicate pruning technique: sorting the array and skipping adjacent identical elements (`nums[i] == nums[i-1]`).

---

## 🔵 Lecture Context

Combinatorial search is central to DSA interviews. The Include/Exclude pattern learned here is the direct template for Combination Sum (Lecture 49), Palindrome Partitioning (Lecture 50), and 0/1 Knapsack in Dynamic Programming.

---

## 1. What is Backtracking?

Backtracking is an algorithmic paradigm that systematically searches for solutions to computational problems by trying out partial candidates. When the algorithm realizes that a partial candidate cannot possibly lead to a valid final solution (or when a solution branch has been fully recorded), it **backtracks** (reverts the last decision) and explores alternative choices.

### The 3 Core Steps of Every Backtracking Step:
1. **Choose:** Make a choice and append it to the current path vector.
2. **Explore:** Recurse into deeper decisions with the updated state.
3. **Un-choose (Backtrack):** Undo the choice (e.g. `path.pop_back()`) to restore the data structure to its exact prior state before exploring sibling branches.

---

## 2. Problem 1: Subsets (Power Set) — LeetCode 78

Given an integer array `nums` of **unique** elements, return all possible subsets (the power set).

### Algorithmic Logic:
At each index `i` from $0$ to $n-1$, we face a binary decision:
1. **Include `nums[i]`:** Add `nums[i]` to our subset, recurse on `i + 1`, and then pop `nums[i]` off upon return.
2. **Exclude `nums[i]`:** Recurse directly on `i + 1` without adding `nums[i]`.

### C++ Implementation
```cpp
#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    void generateSubsets(const vector<int>& nums, int i, vector<int>& current, vector<vector<int>>& result) {
        // Base Case: Reached beyond the last element
        if (i == nums.size()) {
            result.push_back(current);
            return;
        }

        // Choice 1: Include nums[i]
        current.push_back(nums[i]);
        generateSubsets(nums, i + 1, current, result);

        // Backtrack: Undo Choice 1
        current.pop_back();

        // Choice 2: Exclude nums[i]
        generateSubsets(nums, i + 1, current, result);
    }

    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> result;
        vector<int> current;
        generateSubsets(nums, 0, current, result);
        return result;
    }
};
```

---

## 3. Problem 2: Subsets II (With Duplicates) — LeetCode 90

Given an integer array `nums` that may contain **duplicates**, return all possible unique subsets.

### The Duplicate Trap:
If `nums = [1, 2, 2]`, naive generation produces duplicate subsets: `[2]` appears twice (from index 1 and index 2).

### The Duplicate Elimination Strategy:
1. **Sort the array:** Group identical elements adjacent to each other: `[1, 2, 2]`.
2. **Loop over candidates:** For the current position, iterate `for (int j = i; j < n; j++)`.
3. **Skip duplicates:** If `j > i && nums[j] == nums[j-1]`, skip `nums[j]` because taking it at this level would generate identical combinations to those already explored by `nums[j-1]`.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class SolutionSubsetsWithDup {
public:
    void backtrack(const vector<int>& nums, int start, vector<int>& current, vector<vector<int>>& result) {
        // Every state in the prefix tree is a valid subset
        result.push_back(current);

        for (int i = start; i < nums.size(); i++) {
            // Prune duplicate branches at the same tree depth
            if (i > start && nums[i] == nums[i - 1]) {
                continue;
            }

            current.push_back(nums[i]);
            backtrack(nums, i + 1, current, result);
            current.pop_back(); // Backtrack
        }
    }

    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        sort(nums.begin(), nums.end()); // Essential sorting step
        vector<vector<int>> result;
        vector<int> current;
        backtrack(nums, 0, current, result);
        return result;
    }
};
```

---

## 🔍 Detailed Trace: Binary Decision Tree for `[1, 2]`

```
                       []
                    /      \
             (Inc 1)        (Exc 1)
              [1]              []
             /   \           /   \
        (Inc 2) (Exc 2)   (Inc 2) (Exc 2)
        [1, 2]   [1]        [2]     []
```
Total subsets generated = $2^2 = 4$: `[1, 2], [1], [2], []`.

---

## 🧠 Mental Model: The State Trail

Think of backtracking as walking through a labyrinth with a rope tied to your waist:
- Walking forward represents making a choice (`current.push_back(val)`).
- Reaching a dead end represents hitting a base case.
- Pulling the rope to walk backward represents undoing your choice (`current.pop_back()`), leaving the path pristine for the next corridor.

---

## ⚠️ Common Mistakes

1. **Forgetting to Backtrack:** Omitting `current.pop_back()` causes elements from previous branches to contaminate subsequent search paths.
2. **Passing `current` by Value:** Writing `void backtrack(vector<int> current)` creates a deep copy per stack frame, degrading performance from $O(N \cdot 2^N)$ to $O(N^2 \cdot 2^N)$. Pass by reference `vector<int>& current`.
3. **Filtering Duplicates with `std::set`:** Collecting all $2^N$ subsets into a `set<vector<int>>` wastes significant time and memory ($O(N \cdot 2^N \log(2^N))$). Pruning duplicate branches at source via sorting is optimal ($O(N \cdot 2^N)$).

---

## 🖥️ System-Specific Notes

- The power set of size $N=20$ produces $2^{20} = 1,048,576$ subsets ($pprox 10^6$), requiring $pprox 40	ext{ MB}$ of RAM. For $N \ge 30$, $2^{30} pprox 10^9$ elements will exceed typical heap memory limits and time out ($> 1	ext{ second}$).

---

## 🟡 Additional Essential Context

Subsets can also be generated using **Bit Manipulation**:
Every integer from $0$ to $2^N - 1$ corresponds to a unique bitmask. If the $j$-th bit of mask $M$ is set (`(M >> j) & 1`), include `nums[j]`. This non-recursive approach generates all subsets in $O(N \cdot 2^N)$ time and $O(1)$ auxiliary space.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why is `sort()` required before pruning duplicates in Subsets II?  
**A:** Because duplicate elements must be adjacent (`nums[i] == nums[i-1]`) so the condition `i > start && nums[i] == nums[i-1]` can identify and prune duplicate choices at the current tree level.

**Q2:** What is the maximum depth of the call stack for Subsets?  
**A:** Exactly $N$ frames, corresponding to the length of the array.

---

### 🔥 Interview Questions

#### Q1: What is the difference between `i > start` versus `i > 0` when checking `nums[i] == nums[i-1]`?
- **Short Answer:** `i > start` allows duplicates across different recursion depths (vertical branches) while pruning duplicates at the same recursion depth (horizontal siblings).
- **Detailed Explanation:** If `nums = [2, 2]`, we need the subset `[2, 2]`. When selecting the first `2` at depth 0, we must be allowed to pick the second `2` at depth 1. Writing `i > 0` would prevent picking the second `2` even at depth 1! `i > start` ensures that the first duplicate element at any given depth can always be chosen.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
#include <iostream>
#include <vector>
using namespace std;

void printSub(const string& s, int i, string curr) {
    if (i == s.length()) {
        cout << """ << curr << "" ";
        return;
    }
    printSub(s, i + 1, curr + s[i]);
    printSub(s, i + 1, curr);
}

int main() {
    printSub("ab", 0, "");
    return 0;
}
```
**Output:** `"ab" "a" "b" "" `  
**Explanation:** Inclusion branch runs first, followed by the exclusion branch.

---

## Edge Cases

1. **Empty Input Array:** `nums = []` $	o$ Returns `[[]]`.
2. **Single Element:** `nums = [7]` $	o$ Returns `[[], [7]]`.
3. **All Identical Elements:** `nums = [2, 2, 2]` $	o$ Returns `[], [2], [2, 2], [2, 2, 2]`.

---

## Complexity Analysis

- **Time Complexity:** $O(N \cdot 2^N)$ (There are $2^N$ subsets, and each subset takes $O(N)$ time to copy into the result vector).
- **Auxiliary Space Complexity:** $O(N)$ (Maximum recursion stack depth is $N$).

---

## Key Takeaways

1. **State Preservation:** Always restore state with `pop_back()` when exploring sibling branches.
2. **Duplicate Pruning Pattern:** `sort()` + `if (i > start && nums[i] == nums[i-1]) continue;`.
3. **Power Set Size:** Exactly $2^N$ subsets exist for any set of size $N$.

---

## ⚡ 2-Minute Revision

- Subsets = Include / Exclude binary decision tree.
- Subsets II = Sort first; skip duplicate siblings with `i > start && nums[i] == nums[i-1]`.
- Space = $O(N)$ stack depth; Time = $O(N \cdot 2^N)$.

---

## 🧠 Core Intuition — Why Backtracking Is Recursion + Undo

### The "Make Choice → Explore → Undo" Pattern
Think of exploring a maze where you carry a piece of chalk:
1. **Make a mark** (make choice: `current.push_back(val)`)
2. **Walk down the corridor** (explore: recurse)
3. **Erase the mark when you return** (undo: `current.pop_back()`)

Without erasing (backtracking), future corridors appear pre-marked → wrong results.

### Full Decision Tree for Subsets of `[1, 2, 3]`

```
                           [] (start)
                     /                \
            Include 1                Exclude 1
               [1]                       []
            /       \               /         \
      Inc 2         Exc 2      Inc 2          Exc 2
      [1,2]          [1]        [2]             []
      /   \         /   \      /   \           /   \
  Inc3  Exc3   Inc3  Exc3  Inc3  Exc3      Inc3  Exc3
 [1,2,3][1,2] [1,3]  [1] [2,3]  [2]       [3]    []
```

**All 8 leaf nodes = $2^3 = 8$ subsets.** Each level = one element's Include/Exclude decision.

### The Critical Insight: WHY We Need `pop_back()`
```
Path of [1, 2, 3] branch:
  push(1) → [1]
    push(2) → [1,2]
      push(3) → [1,2,3] ← record subset
      pop(3)  → [1,2]   ← BACKTRACK: restore for Exclude-3 branch
    pop(2)  → [1]       ← BACKTRACK: restore for Exclude-2 branch
  pop(1)  → []          ← BACKTRACK: restore for Exclude-1 branch
```
Without `pop_back()`, after recording `[1,2,3]`, the `current` vector stays as `[1,2,3]`. The Exclude-3 branch would record `[1,2,3]` instead of `[1,2]`.

---

## 🎯 Pattern Recognition — When to Use Subsets/Backtracking

### Keywords That Signal Subset/Backtracking Problems
- "Return **all** subsets / combinations / partitions"
- "Power set", "all possible ways to...", "enumerate all..."
- "No duplicate subsets" → sort + prune with `i > start && nums[i] == nums[i-1]`

### Include/Exclude vs. For-Loop Backtracking: The Two Templates
```
Template 1 (Include/Exclude — binary tree):
  At index i, two choices: include nums[i] OR exclude nums[i]
  → Used in: LeetCode 78 (Subsets), 0/1 Knapsack DP

Template 2 (For-loop — multi-branch tree):
  At position start, loop j from start to n-1; pick nums[j]
  → Used in: LeetCode 90 (Subsets II), 39 (Combination Sum)
```
Both generate the same subsets, but the for-loop template handles duplicates more naturally.

### Distinguishing Subsets vs. Combinations vs. Permutations
| Problem | Order Matters? | Repeats Allowed? | Count |
|---|---|---|---|
| Subsets (78) | No | No | $2^N$ |
| Combinations (77) | No | No | $\binom{N}{K}$ |
| Permutations (46) | Yes | No | $N!$ |
| Combination Sum (39) | No | Yes (unbounded) | Depends |

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] Why must you sort the array before handling duplicates in Subsets II?
**Answer:** The duplicate pruning condition `if (i > start && nums[i] == nums[i-1]) continue;` relies on the two duplicate values being **adjacent**. If they are not adjacent (unsorted), then `nums[i] == nums[i-1]` would fail to detect the duplicate even if they are equal. Sorting guarantees all equal elements cluster together, making the condition reliable. Example: `[2, 1, 2]` unsorted — the two `2`s are at positions 0 and 2. The condition `nums[2] == nums[1]` checks `2 == 1` → false → no pruning! After sorting `[1, 2, 2]`, position 1 and 2 are both `2` → correctly pruned.

---

### Q2: [Complexity] Derive the time complexity of generating all subsets: why $O(N \cdot 2^N)$?
**Answer:** There are exactly $2^N$ subsets (each element is either included or excluded — $N$ binary decisions). For each subset, we copy it into the result vector — copying takes $O(N)$ time in the worst case (for the subset containing all elements). Therefore: total time = (number of subsets) × (copy cost) = $2^N \times O(N) = O(N \cdot 2^N)$. The recursion tree itself has $2^{N+1} - 1$ nodes, each doing $O(1)$ work (push/pop), adding $O(2^N)$ to the total.

---

### Q3: [Conceptual] What is the exact difference between `i > 0` and `i > start` in the duplicate pruning condition?
**Answer:** This is the single most common Subsets II bug.
- `i > 0 && nums[i] == nums[i-1]` → skips element whenever it's a duplicate of the previous one **at any level**.
- `i > start && nums[i] == nums[i-1]` → skips element only when it would generate a **duplicate sibling branch at the current recursion depth**.

**Why `i > 0` is WRONG:** Consider `nums = [1, 2, 2]`, backtrack called with `start = 1`.  
Loop: `i = 1` (pick 2), recurse → at depth 2, `i = 2` (pick 2 again).  
Here `i > 0` is true AND `nums[2] == nums[1]` → it **skips the second 2**!  
But `[2, 2]` IS a valid unique subset that should be included!  
`i > start` is false when `i == start == 1`, so it does NOT skip → `[2, 2]` is correctly generated.

---

### Q4: [Output Prediction] What does this code output?
```cpp
#include <iostream>
#include <vector>
using namespace std;

void f(vector<int>& nums, int i, vector<int> curr) {  // BUG: pass by value!
    if (i == nums.size()) {
        for (int x : curr) cout << x << " ";
        cout << "| ";
        return;
    }
    curr.push_back(nums[i]);
    f(nums, i + 1, curr);
    curr.pop_back();
    f(nums, i + 1, curr);
}

int main() {
    vector<int> nums = {1, 2};
    f(nums, 0, {});
}
```
**Answer:** Output is `1 2 | 1 | 2 | | `. The code actually works correctly (generates all 4 subsets of `[1,2]`), BUT the `pop_back()` on a by-value copy is redundant — `curr` is already a separate copy per call frame, so the push/pop doesn't matter. **However, the performance is $O(N^2 \cdot 2^N)$** because each frame copies the entire vector. The bug is a performance bug, not a correctness bug. In interviews, this should be flagged.

---

### Q5: [Extension] Can you solve Subsets without backtracking using bit manipulation? Compare time complexities.
**Answer:** Yes. For N elements, there are $2^N$ possible subsets. Represent each subset as an integer bitmask $M$ from $0$ to $2^N - 1$. If bit $j$ of $M$ is set, include `nums[j]`.
```cpp
vector<vector<int>> subsets(vector<int>& nums) {
    int n = nums.size();
    vector<vector<int>> result;
    for (int mask = 0; mask < (1 << n); mask++) {
        vector<int> sub;
        for (int j = 0; j < n; j++) {
            if (mask & (1 << j)) sub.push_back(nums[j]);
        }
        result.push_back(sub);
    }
    return result;
}
```
**Time:** $O(N \cdot 2^N)$ — same asymptotic complexity. **Space:** $O(1)$ auxiliary (no recursion stack). Bitmask approach is preferred for $N \le 20$ due to simplicity, but cannot handle Subsets II (duplicates) as cleanly.

---

### Q6: [System Design Follow-up] If N = 30, generating all subsets produces $2^{30} \approx 10^9$ subsets. How would you handle this in production?
**Answer:** At $N = 30$, storing all subsets requires $\approx 10^9 \times O(N)$ memory — roughly 30GB. This is infeasible. Production approaches:
1. **Streaming/Iterator:** Generate subsets one at a time using the bitmask approach without storing them all. Process each subset immediately (e.g., evaluate a function on it).
2. **Parallelism:** Partition the bitmask range $[0, 2^N)$ across multiple CPU cores or machines.
3. **Sampling:** If you need random subsets for ML/statistics, sample random bitmasks uniformly.
4. **Pruning with early termination:** Use backtracking with aggressive pruning (e.g., Combination Sum with target constraint) to limit the explored subset space.

---

### Q7: [Proof] Prove that there are exactly $2^N$ subsets of an N-element set.
**Answer:** By induction. **Base:** N=0, only the empty set → $1 = 2^0$ subset. **Inductive step:** Assume an $(N-1)$-element set has $2^{N-1}$ subsets. For an $N$-element set, each of the $2^{N-1}$ subsets of the first $(N-1)$ elements either includes or excludes the $N$-th element — doubling the count: $2 \times 2^{N-1} = 2^N$. ∎

---

## 📊 Complexity Analysis — Extended

### Recursion Tree Analysis
- **Total nodes in decision tree:** $2 + 2^2 + \dots + 2^N = 2^{N+1} - 1 = O(2^N)$ nodes.
- **Work per node:** $O(1)$ for push/pop + $O(N)$ at leaf nodes for copying.
- **Total:** $O(2^N) \cdot O(1) + 2^N \cdot O(N) = O(N \cdot 2^N)$.

### Subsets II Additional Analysis
- Sorting costs $O(N \log N)$ upfront.
- Pruning eliminates duplicate branches, reducing the tree — but asymptotic worst case remains $O(N \cdot 2^N)$ (all distinct elements).

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Approach |
|---|---|---|
| 78 | Subsets | Include/Exclude or for-loop backtracking |
| 90 | Subsets II | Sort + skip `nums[i] == nums[i-1]` at same depth |
| 77 | Combinations | For-loop backtracking with exactly K picks |
| 39 | Combination Sum | Unbounded pick (stay at same index) |
| 40 | Combination Sum II | Sort + one-use pick + duplicate skip |

---

## 🔗 Cross-Topic Connections

- **→ 0/1 Knapsack DP (File 02):** The Include/Exclude decision tree IS the DP state tree. Memoizing the `(index, remaining_capacity)` state converts backtracking to DP.
- **→ Combination Sum (File 08):** Same for-loop backtracking template; only difference is unbounded reuse.
- **→ Permutations (File 04):** When order matters AND all elements used → permutations.
- **→ Palindrome Partitioning (File 09):** For-loop backtracking on string cut positions.
- **→ Bit Manipulation:** Bitmask approach is the non-recursive alternative generating identical results.

---

## ⚡ 2-Minute Revision Flash Card (Enhanced)

- **Choose → Explore → Undo:** The 3-step mantra. Missing `pop_back()` = wrong answers.
- **$2^N$ subsets:** Each element has exactly 2 choices (in or out).
- **Duplicate pruning:** Sort + `if (i > start && nums[i] == nums[i-1]) continue;` — note `i > start`, NOT `i > 0`.
- **By value vs by reference:** Always pass `current` by reference; creating copies per frame costs $O(N^2 \cdot 2^N)$.
- **Space = $O(N)$ stack:** The recursion depth equals array length N, not the number of subsets.
