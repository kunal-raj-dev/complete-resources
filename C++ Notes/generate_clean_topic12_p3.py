import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t12_dir = os.path.join(root, "12_recursion_and_backtracking")

notes = {}

# 03: Subsets & Subsets II
notes["03_backtracking_subsets_and_subsets_ii.md"] = """# Lecture 44: Backtracking: Subsets & Subsets II (Handling Duplicates)

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
                    /      \\
             (Inc 1)        (Exc 1)
              [1]              []
             /   \\           /   \\
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

- The power set of size $N=20$ produces $2^{20} = 1,048,576$ subsets ($\approx 10^6$), requiring $\approx 40\text{ MB}$ of RAM. For $N \ge 30$, $2^{30} \approx 10^9$ elements will exceed typical heap memory limits and time out ($> 1\text{ second}$).

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
        cout << "\"" << curr << "\" ";
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

1. **Empty Input Array:** `nums = []` $\to$ Returns `[[]]`.
2. **Single Element:** `nums = [7]` $\to$ Returns `[[], [7]]`.
3. **All Identical Elements:** `nums = [2, 2, 2]` $\to$ Returns `[], [2], [2, 2], [2, 2, 2]`.

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
"""

# 04: Permutations of Array and String
notes["04_permutations_of_array_and_string.md"] = """# Lecture 45: Permutations of an Array & String (LeetCode 46)

> **One-Line Purpose:** Master the in-place swapping backtracking technique to generate all $N!$ permutations of a sequence in optimal $O(N \cdot N!)$ time without allocating auxiliary boolean lookup tables.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #45  
> **Video ID:** `N4gJDGdhpLw`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=N4gJDGdhpLw)  
> **Duration:** 22:55  
> **Transcript:** `.transcripts/12_recursion_and_backtracking/045_Permutations_of_an_Array_String___Recursion___Backtracking.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The fundamental mathematical difference between a **Combination** (order does not matter) and a **Permutation** (order matters).
- The total permutation count: for an array of $N$ distinct elements, there are exactly $N!$ permutations.
- **Approach 1 (Auxiliary Frequency Array / Visited Map):** $O(N)$ extra memory per state.
- **Approach 2 (Optimal In-Place Swapping):** $O(1)$ auxiliary memory (excluding recursion stack).
- The absolute necessity of the **symmetric backtrack swap** to restore original element order.

---

## 🔵 Lecture Context

Generating permutations tests recursive state control and array restoration. While subsets represent choices of whether to pick an element, permutations represent choices of *which order* to arrange elements.

---

## 1. Mathematical Concept: Permutations

A permutation is an arrangement of all elements in a specific order:
For $N = 3$, elements $\{1, 2, 3\}$ have $3! = 3 \times 2 \times 1 = 6$ unique permutations:
$$[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]$$

---

## 2. The In-Place Swapping Strategy

Instead of maintaining a visited boolean table to track which elements have been used:
1. Divide the array into two zones:
   - `nums[0 ... idx-1]`: Fixed prefix (elements already placed in their permutation slots).
   - `nums[idx ... n-1]`: Pool of available candidate elements.
2. For each index $i$ from `idx` to $n-1$:
   - **Swap `nums[idx]` with `nums[i]`:** Place candidate $i$ into the current position `idx`.
   - **Recurse on `idx + 1`:** Solve for the next position.
   - **Backtrack swap `nums[idx]` with `nums[i]`:** Restore the original array ordering so subsequent candidate swaps operate on the uncorrupted array state!

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    void permuteHelper(vector<int>& nums, int idx, vector<vector<int>>& result) {
        // Base Case: All positions 0 ... n-1 have been assigned
        if (idx == nums.size()) {
            result.push_back(nums);
            return;
        }

        for (int i = idx; i < nums.size(); i++) {
            // Choice: Place nums[i] at position idx
            swap(nums[idx], nums[i]);

            // Explore: Recurse on the remaining positions
            permuteHelper(nums, idx + 1, result);

            // Backtrack: Restore original element order
            swap(nums[idx], nums[i]);
        }
    }

    vector<vector<int>> permute(vector<int>& nums) {
        vector<vector<int>> result;
        permuteHelper(nums, 0, result);
        return result;
    }
};

int main() {
    Solution solver;
    vector<int> nums = {1, 2, 3};
    vector<vector<int>> perms = solver.permute(nums);

    for (const auto& p : perms) {
        cout << "[ ";
        for (int x : p) cout << x << " ";
        cout << "]\n";
    }
    return 0;
}
```

---

## 🔍 Detailed Trace: Permutations of `[1, 2, 3]`

```
Level 0 (idx = 0):
  i = 0: Swap(0, 0) -> [1, 2, 3]
    Level 1 (idx = 1):
      i = 1: Swap(1, 1) -> [1, 2, 3]
        Level 2 (idx = 2): Base case reached -> Output [1, 2, 3]
      i = 2: Swap(1, 2) -> [1, 3, 2]
        Level 2 (idx = 2): Base case reached -> Output [1, 3, 2]
      Backtrack Swap(1, 2) -> Restored [1, 2, 3]
    Backtrack Swap(0, 0) -> Restored [1, 2, 3]

  i = 1: Swap(0, 1) -> [2, 1, 3]
    Level 1 (idx = 1):
      i = 1: Swap(1, 1) -> [2, 1, 3] -> Output [2, 1, 3]
      i = 2: Swap(1, 2) -> [2, 3, 1] -> Output [2, 3, 1]
    Backtrack Swap(0, 1) -> Restored [1, 2, 3]

  i = 2: Swap(0, 2) -> [3, 2, 1]
    ...
```

---

## 🧠 Mental Model: The Decision Wheel

At position `idx`, think of a rotating wheel that tests each candidate from `idx` to $N-1$ in the current slot. After exploring the universe where candidate $i$ sits in the slot, the wheel rotates back (`swap` again) to prepare for candidate $i+1$.

---

## ⚠️ Common Mistakes

1. **Omitting the Backtracking Swap:** If you do not swap back, the array order becomes permanently jumbled, resulting in duplicate permutations and missed arrangements.
2. **Off-by-One in Loop Start:** Starting `for (int i = 0; ...)` instead of `for (int i = idx; ...)`. Starting at 0 swaps already-fixed prefix elements, producing incorrect cyclic permutations.

---

## 🖥️ System-Specific Notes

- $N!$ factorial growth is exceptionally steep:
  - $10! = 3,628,800 \approx 3.6 \times 10^6$ operations (completes in $\approx 20\text{ ms}$).
  - $12! = 479,001,600 \approx 4.8 \times 10^8$ operations (approaching timeout).
  - $13! = 6.22 \times 10^9$ operations (guaranteed TLE).
  Problems requiring full permutations strictly cap $N \le 10$ or $11$.

---

## 🟡 Additional Essential Context

The Standard Template Library provides `std::next_permutation(nums.begin(), nums.end())` from `<algorithm>`, which generates permutations iteratively in lexicographical order in $O(N)$ time per step. In interviews, you must know how to implement the recursive swapping algorithm from scratch.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Does the in-place swapping algorithm generate permutations in lexicographical order?  
**A:** No. Because elements are swapped across distant indices, the resulting order is not sorted lexicographically. To generate lexicographical order, use the visited boolean array approach or sort the result.

**Q2:** How would you modify this algorithm to handle DUPLICATE elements (LeetCode 47: Permutations II)?  
**A:** At each recursion level `idx`, use an unordered set `unordered_set<int> seen` to record elements already placed at position `idx`. If `seen.count(nums[i]) > 0`, `continue` to skip the duplicate swap.

---

### 🔥 Interview Questions

#### Q1: What is the space complexity difference between the Swap approach vs the Boolean Visited array approach?
- **Short Answer:** The Swap approach uses $O(1)$ auxiliary space (excluding stack), whereas the Boolean array approach requires $O(N)$ auxiliary memory per level.
- **Detailed Explanation:** The visited array approach requires an explicit `vector<bool> visited(N)` and a temporary path vector `vector<int> current`. The swap approach operates entirely in-place on the input array, consuming zero heap memory.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

void perm(string s, int idx) {
    if (idx == s.length()) {
        cout << s << " ";
        return;
    }
    for (int i = idx; i < s.length(); i++) {
        swap(s[idx], s[i]);
        perm(s, idx + 1);
    }
}

int main() {
    perm("AB", 0);
    return 0;
}
```
**Output:** `AB BA `  
**Explanation:** For size 2, produces $2! = 2$ arrangements. Notice that here `s` is passed by value, so explicit backtrack swap is avoided, but passing by value incurs $O(N)$ memory copies.

---

## Edge Cases

1. **$N = 1$:** `nums = [1]` $\to$ Returns `[[1]]`.
2. **Distinct Elements:** Handled with strict $O(N \cdot N!)$ time.

---

## Complexity Analysis

- **Time Complexity:** $O(N \cdot N!)$ ($N!$ leaves, each taking $O(N)$ to copy to output).
- **Auxiliary Space Complexity:** $O(N)$ (Recursion stack height is $N$).

---

## Key Takeaways

1. **Total Count:** Exactly $N!$ permutations for $N$ distinct items.
2. **In-Place Swapping:** `swap(nums[idx], nums[i])` $\to$ Recurse $\to$ `swap(nums[idx], nums[i])`.
3. **Restoration Invariant:** Backtracking always leaves the shared array in its exact initial configuration.

---

## ⚡ 2-Minute Revision

- In-place swapping loop: `for (int i = idx; i < n; i++)`.
- Swap, recurse on `idx + 1`, and swap back.
- Time: $O(N \cdot N!)$ | Space: $O(N)$ stack depth.
"""

print("Writing batch 1 notes...")
for fn, content in notes.items():
    with open(os.path.join(t12_dir, fn), "w", encoding="utf-8") as f:
        f.write(content)
print("Updated 03, 04.")
