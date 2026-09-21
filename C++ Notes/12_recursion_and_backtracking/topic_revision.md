# Topic 12 Revision: Recursion & Backtracking

> **High-Density Review:** Inductive proofs, call stack mechanics, subsets vs permutations, and $O(1)$ pruning techniques.

---

## 1. The Core 3-Step Framework
1. **Base Case:** When does the recursion stop? (e.g., `idx == n`, `target == 0`).
2. **Do Work / Make Choice:** Add element to path, place queen, swap elements.
3. **Recursive Call:** Pass the updated state to the next step.
4. **Backtrack (Undo Choice):** Revert the state modification to explore other branches (e.g., `path.pop_back()`).

---

## 2. Classic Problem Topologies

| Problem | Paradigm | Recursion Tree Branching | Time Complexity |
|---|---|---|---|
| **Subsets / Combinations** | Include / Exclude | Binary Branching ($2$) | $O(2^N)$ |
| **Permutations** | Swap with all remaining | Shrinking Branching ($N!$) | $O(N!)$ |
| **Sudoku Solver** | Try 1-9 in empty cell | Fixed bounded ($9$) | $O(9^{81})$ worst-case |
| **N-Queens** | Try N columns per row | bounded by safe spots | $O(N!)$ worst-case |
| **Merge / Quick Sort** | Divide & Conquer | Binary splitting ($2$) | $O(N \log N)$ |

---

## 3. High-Yield Code Snippets

**Subset Backtracking Pattern:**
```cpp
void backtrack(int idx, vector<int>& nums, vector<int>& current) {
    if (idx == nums.size()) {
        result.push_back(current);
        return;
    }
    // Include
    current.push_back(nums[idx]);
    backtrack(idx + 1, nums, current);
    current.pop_back(); // Undo
    // Exclude
    backtrack(idx + 1, nums, current);
}
```

**Permutation Backtracking Pattern:**
```cpp
void permute(int idx, vector<int>& nums) {
    if (idx == nums.size()) {
        result.push_back(nums);
        return;
    }
    for (int i = idx; i < nums.size(); ++i) {
        swap(nums[idx], nums[i]);
        permute(idx + 1, nums);
        swap(nums[idx], nums[i]); // Undo
    }
}
```

---

## 4. Pruning Rules to Memorize
- **Avoiding Duplicates in Subsets (Subsets II):** Sort array first. Inside the recursive loop/call, skip adjacent duplicates `if (i > idx && nums[i] == nums[i-1]) continue;`.
- **Combination Sum (Infinite Supply):** Instead of passing `idx + 1`, pass `idx` again in the recursive call so the same element can be selected again.
- **Valid Palindrome Partitioning:** Only recurse on the remaining string if the prefix `s.substr(idx, i - idx + 1)` is already a valid palindrome.

---

## 5. Tail Recursion & Compiler Optimizations
- **Tail Recursion:** If the recursive call is the absolutely *last* instruction in the function (with no computation acting on its return value), the compiler can optimize it into a `while` loop, preventing $O(N)$ stack memory usage (reduces to $O(1)$ stack space).
- **Not Tail Recursive:** `return N * fact(N - 1);` is NOT tail-recursive because the multiplication happens *after* the recursive call returns.

## 6. Time Complexity Recurrences (Master Theorem)
- **Binary Search:** $T(N) = T(N/2) + O(1) \implies O(\log N)$.
- **Merge Sort:** $T(N) = 2T(N/2) + O(N) \implies O(N \log N)$.
- **Fibonacci:** $T(N) = T(N-1) + T(N-2) \implies O(2^N)$.

## 7. State Space Tree Math
- For a decision tree where you make $B$ choices at each step (Branching factor) and the maximum depth is $D$, the total number of leaves is bounded by $O(B^D)$. Total nodes in the tree is $O(B^D)$ as well (sum of geometric series).
- Space complexity is strictly determined by the maximum depth $D$, which is $O(D)$.

## ⚡ 2-Minute Revision Flash Card
- Backtracking is DFS on a State Space Tree.
- Time Complexity is usually $O(\text{Branching Factor}^{\text{Depth}})$. Space is $O(\text{Depth})$.
- Always `pop_back()` or un-swap after the recursive call returns to restore state!
