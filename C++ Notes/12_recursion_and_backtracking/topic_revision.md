# Topic 12 Revision: Recursion & Backtracking

> **High-Density Revision Guide:** Recursive models, backtracking decision trees, pruning techniques, and divide-and-conquer sorting.

---

## 1. The 3 Laws of Recursion
1. **Base Case:** Stopping condition where recursion terminates without making further self-calls.
2. **Recursive Hypothesis / Subproblem:** Trust that the smaller instance $f(N-1)$ computes the correct sub-result.
3. **Self Work:** Combine the sub-result with current state to solve the original instance $f(N)$.

---

## 2. The Backtracking Blueprint
Backtracking is **exhaustive DFS exploration with state restoration**:
```cpp
void backtrack(State &state) {
    if (isGoal(state)) {
        recordSolution(state);
        return;
    }

    for (Choice choice : getChoices(state)) {
        if (isValid(choice, state)) {
            makeChoice(choice, state);     // 1. Take choice
            backtrack(state);              // 2. Explore subtree
            undoChoice(choice, state);     // 3. BACKTRACK (Restore state)
        }
    }
}
```

---

## 3. High-Frequency Patterns & Classical Problems

| Problem | Key Technique | Time Complexity | Space Complexity |
|---|---|---|---|
| **Subsets (Power Set)** | Include / Exclude binary decision tree | $O(2^N)$ | $O(N)$ (Stack) |
| **Subsets II** | Sort array, skip duplicates `if (i > idx && nums[i] == nums[i-1]) continue;` | $O(2^N)$ | $O(N)$ |
| **Permutations** | In-place element swap or visited boolean array | $O(N! \times N)$ | $O(N)$ |
| **N-Queens** | Column + 2 Diagonal boolean lookup arrays | $O(N!)$ | $O(N)$ |
| **Sudoku Solver** | Check Row, Col, and $3 \times 3$ Box constraint | $O(9^{81})$ worst | $O(81) = O(1)$ |
| **Rat in a Maze** | Mark visited `vis[r][c] = 1`, explore D-L-R-U, unmark `vis[r][c] = 0` | $O(4^{N^2})$ | $O(N^2)$ |
| **Merge Sort** | Divide at mid, sort left & right, merge with 2 pointers | $O(N \log N)$ | $O(N)$ |
| **Quick Sort** | Partition around pivot, recursively sort partitions | Average $O(N \log N)$, Worst $O(N^2)$ | $O(\log N)$ |
| **Count Inversions** | Count cross-inversions during merge step: `invCount += (mid - i + 1)` | $O(N \log N)$ | $O(N)$ |
