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
