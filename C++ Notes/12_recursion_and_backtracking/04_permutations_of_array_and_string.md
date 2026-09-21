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
