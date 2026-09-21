# Lecture 45: Permutations of an Array & String (LeetCode 46)

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
For $N = 3$, elements $\{1, 2, 3\}$ have $3! = 3 	imes 2 	imes 1 = 6$ unique permutations:
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
        cout << "]
";
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
  - $10! = 3,628,800 pprox 3.6 	imes 10^6$ operations (completes in $pprox 20	ext{ ms}$).
  - $12! = 479,001,600 pprox 4.8 	imes 10^8$ operations (approaching timeout).
  - $13! = 6.22 	imes 10^9$ operations (guaranteed TLE).
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

1. **$N = 1$:** `nums = [1]` $	o$ Returns `[[1]]`.
2. **Distinct Elements:** Handled with strict $O(N \cdot N!)$ time.

---

## Complexity Analysis

- **Time Complexity:** $O(N \cdot N!)$ ($N!$ leaves, each taking $O(N)$ to copy to output).
- **Auxiliary Space Complexity:** $O(N)$ (Recursion stack height is $N$).

---

## Key Takeaways

1. **Total Count:** Exactly $N!$ permutations for $N$ distinct items.
2. **In-Place Swapping:** `swap(nums[idx], nums[i])` $	o$ Recurse $	o$ `swap(nums[idx], nums[i])`.
3. **Restoration Invariant:** Backtracking always leaves the shared array in its exact initial configuration.

---

## ⚡ 2-Minute Revision

- In-place swapping loop: `for (int i = idx; i < n; i++)`.
- Swap, recurse on `idx + 1`, and swap back.
- Time: $O(N \cdot N!)$ | Space: $O(N)$ stack depth.

---

## 🧠 Core Intuition — Why Swapping Generates All Permutations

### The Decision Tree for `[1, 2, 3]`

```
Level 0: Fix position 0 — choose from {1, 2, 3}
  ┌─────────┬─────────┬─────────┐
  │swap(0,0)│swap(0,1)│swap(0,2)│
  │  [1,2,3]│  [2,1,3]│  [3,2,1]│
  └────┬────┴────┬────┴────┬────┘
Level 1: Fix position 1 — choose from remaining
  [1,2,3]      [2,1,3]      [3,2,1]
  /     \       /    \       /    \
swap(1,1) sw(1,2) sw(1,1) sw(1,2) sw(1,1) sw(1,2)
[1,2,3] [1,3,2] [2,1,3] [2,3,1] [3,2,1] [3,1,2]
Level 2: Base case — record permutation
```

**The key insight:** At position `idx`, we "choose" which element sits there by swapping it from the remaining pool (`idx` to `n-1`). After exploring all arrangements with that choice, we **swap back** to restore the pool for the next candidate.

### Why the Backtrack Swap Is Non-Negotiable
```
Without backtracking swap:
  swap(0,1) → [2,1,3]
  swap(1,2) → [2,3,1] ← recorded ✓
  // NO backtrack: array stays [2,3,1]
  swap(1,1) → WRONG: now working on corrupted [2,3,1] not [2,1,3]!
  Records [2,3,1] again instead of [2,1,3] ✗
```

### Approach 2: Visited Array (Generates Lexicographic Order)
```cpp
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    void permuteHelper2(vector<int>& nums, vector<bool>& visited,
                        vector<int>& current, vector<vector<int>>& result) {
        if (current.size() == nums.size()) {
            result.push_back(current);
            return;
        }
        for (int i = 0; i < nums.size(); i++) {
            if (!visited[i]) {
                visited[i] = true;
                current.push_back(nums[i]);
                permuteHelper2(nums, visited, current, result);
                current.pop_back();
                visited[i] = false;
            }
        }
    }

    vector<vector<int>> permuteV2(vector<int>& nums) {
        sort(nums.begin(), nums.end());  // Sort for lexicographic order
        vector<vector<int>> result;
        vector<int> current;
        vector<bool> visited(nums.size(), false);
        permuteHelper2(nums, visited, current, result);
        return result;
    }
};
// Pros: generates lexicographic order; easy to reason about
// Cons: O(N) extra space for visited[] + current[] arrays
```

---

## 🎯 Pattern Recognition — When This Is a Permutation Problem

### Signals in Problem Statement
- "All possible **orderings**" or "all **arrangements**"
- "Next permutation" variant
- "Find the K-th permutation" (use Factorial Number System)
- Constraint: each element used **exactly once** AND **order matters**

### Permutation vs. Combination vs. Subset
| Aspect | Permutation | Combination | Subset |
|---|---|---|---|
| Order matters? | ✅ Yes | ❌ No | ❌ No |
| All elements used? | ✅ Yes (LeetCode 46) | ❌ No | ❌ No |
| Template | Swap in-place or visited[] | for-loop with start index | Include/Exclude binary |

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] Does in-place swapping generate permutations in lexicographic order?
**Answer:** **No.** Because swapping `nums[0]` with `nums[2]` places a larger element at position 0 before exploring all arrangements starting with the smaller element at position 0. The output order is: `[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,2,1], [3,1,2]` — not lexicographic. To get lexicographic order, use the **visited array approach** after sorting the input.

---

### Q2: [Extension] How do you handle DUPLICATE elements in permutations (LeetCode 47: Permutations II)?
**Answer:** Two approaches:
1. **Swap approach + set at each level:**
   ```cpp
   void permuteWithDup(vector<int>& nums, int idx, vector<vector<int>>& result) {
       if (idx == nums.size()) { result.push_back(nums); return; }
       unordered_set<int> seen;  // Track elements placed at position idx
       for (int i = idx; i < nums.size(); i++) {
           if (seen.count(nums[i])) continue;  // Skip duplicate choice
           seen.insert(nums[i]);
           swap(nums[idx], nums[i]);
           permuteWithDup(nums, idx + 1, result);
           swap(nums[idx], nums[i]);
       }
   }
   ```
2. **Visited array + sort:** Sort the array. In the for-loop, skip `if (visited[i] || (i > 0 && nums[i] == nums[i-1] && !visited[i-1])) continue;` — the second condition ensures we always place duplicates in order (pick the first before the second), preventing symmetric duplicate trees.

---

### Q3: [Complexity] Derive the time complexity $O(N \cdot N!)$ from first principles.
**Answer:** 
- The recursion tree has exactly $N!$ leaf nodes (one per distinct permutation).
- At each leaf, we copy the $N$-element array to the result → $O(N)$ cost per leaf.
- Internal nodes: at depth $d$, there are $N! / (N - d)!$ nodes, each doing $O(1)$ swap work. Total internal work:
$$\sum_{d=0}^{N-1} \frac{N!}{(N-d)!} \cdot O(1) = N! \sum_{k=1}^{N} \frac{1}{k!} < N! \cdot e \approx O(N!)$$
Total: $O(N! + N \cdot N!) = O(N \cdot N!)$.

---

### Q4: [Output Prediction / Debug] What bug exists in this code?
```cpp
void permute(vector<int>& nums, int idx, vector<vector<int>>& result) {
    if (idx == nums.size()) {
        result.push_back(nums);
        return;
    }
    for (int i = 0; i < nums.size(); i++) {  // BUG: starts from 0, not idx
        swap(nums[idx], nums[i]);
        permute(nums, idx + 1, result);
        swap(nums[idx], nums[i]);
    }
}
```
**Answer:** The bug is `for (int i = 0; ...)` — it starts from index `0` instead of `idx`. This causes the "fixed" prefix (indices `0` to `idx-1`) to be swapped, which generates duplicate permutations and potentially incorrect ones. For `nums = [1,2]`: at `idx=1`, `i=0` swaps position 1 with position 0, undoing a previous placement. Fix: `for (int i = idx; ...)`.

---

### Q5: [Extension] What is the next permutation algorithm? How is it related to generating all permutations?
**Answer:** `std::next_permutation` generates the next permutation in lexicographic order in $O(N)$ time using the following 3-step algorithm:
1. Find the largest index `i` such that `nums[i] < nums[i+1]`. If none, reverse entire array (it was the last permutation).
2. Find the largest index `j > i` such that `nums[i] < nums[j]`.
3. Swap `nums[i]` and `nums[j]`, then reverse `nums[i+1:]`.

To generate ALL $N!$ permutations in order: sort the array, then call `next_permutation` in a loop until it returns false. This avoids explicit recursion but visits the same permutations.

---

### Q6: [System Design] If N = 20, you have 20! ≈ 2.4 × 10^18 permutations. How would you find the K-th permutation without generating all?
**Answer:** Use the **Factorial Number System** (LeetCode 60: Permutation Sequence):
1. For each position `i` from 0 to N-1, compute `(N-1-i)!` (the number of permutations with a given first element).
2. The index of the element at position `i` is `k / fact`, where `fact = (N-1-i)!`.
3. Remove that element from the candidate list and update `k = k % fact`.
This finds the K-th permutation in $O(N^2)$ time (dominated by list deletion) without generating any other permutations.

---

## 📊 Complexity Analysis — Extended

| Approach | Time | Auxiliary Space |
|---|---|---|
| Swap In-Place | $O(N \cdot N!)$ | $O(N)$ stack only |
| Visited Array | $O(N \cdot N!)$ | $O(N)$ visited + $O(N)$ current + $O(N)$ stack |
| `next_permutation` loop | $O(N \cdot N!)$ | $O(1)$ auxiliary |
| K-th permutation (Factorial System) | $O(N^2)$ | $O(N)$ candidates list |

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Approach |
|---|---|---|
| 46 | Permutations | Swap in-place backtracking |
| 47 | Permutations II | Swap + unordered_set at each level OR visited + sort |
| 60 | Permutation Sequence | Factorial Number System — O(N²), no enumeration |
| 31 | Next Permutation | 3-step O(N) algorithm; modifies array in-place |
| 567 | Permutation in String | Sliding window + frequency counting (not backtracking!) |

---

## 🔗 Cross-Topic Connections

- **→ Subsets (File 03):** Subsets are combinations (order doesn't matter). Permutations are ordered arrangements. Both use backtracking.
- **→ N-Queens (File 05):** N-Queens is essentially permuting which column each queen goes in, with additional diagonal constraints.
- **→ DP (Factorial Number System):** K-th permutation uses DP-like precomputed factorials to skip enumeration entirely.
- **→ String Problems:** Permutation in String (LC 567) uses sliding window over character frequencies — a non-backtracking permutation application.

---

## ⚡ 2-Minute Revision Flash Card (Enhanced)

- **Two approaches:** (1) Swap in-place: `O(1)` aux, non-lexicographic; (2) Visited array: `O(N)` aux, lexicographic after sort.
- **Backtrack swap is mandatory:** Omitting the second `swap` corrupts the array for sibling branches.
- **Total permutations:** Exactly $N!$ for $N$ distinct elements.
- **Duplicate handling:** Use `unordered_set<int> seen` at each recursion level (swap approach) or `!visited[i-1]` guard (visited approach).
- **$N! \text{ grows fast}$:** $10! \approx 3.6 \times 10^6$ (fast); $13! \approx 6.2 \times 10^9$ (TLE). Problems cap $N \le 8$–$12$.
