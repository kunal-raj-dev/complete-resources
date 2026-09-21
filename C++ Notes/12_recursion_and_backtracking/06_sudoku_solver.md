# Lecture 47: Sudoku Solver: 2D Constraint Backtracking (LeetCode 37)

> **One-Line Purpose:** Master multi-constraint 2D grid backtracking by solving 9x9 Sudoku boards in-place, enforcing row, column, and $3 	imes 3$ sub-box invariants with early-exit boolean recursion.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #47  
> **Video ID:** `70cP3qtJp-s`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=70cP3qtJp-s)  
> **Duration:** 26:58  
> **Transcript:** `.transcripts/12_recursion_and_backtracking/047_Sudoku_Solver_Problem___using_Backtracking___Leetcode_Hard.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The exact rules of standard 9x9 Sudoku.
- Why standard Sudoku requires **Boolean-returning backtracking** (`bool solve()`) instead of `void` backtracking (we must stop immediately after the first valid full solution is found).
- The mathematical mapping for $3 	imes 3$ sub-grid box checking: row $3 	imes (r / 3) + i / 3$ and column $3 	imes (c / 3) + i \% 3$.
- State restoration (`board[i][j] = '.'`) when a tested digit causes an downstream dead end.

---

## 🔵 Lecture Context

Sudoku Solver is a classic LeetCode Hard interview problem. It combines nested coordinate grid traversal, multi-rule validation, and early-exit backtracking.

---

## 1. Problem Statement & Rules of Sudoku

A Sudoku board is a $9 	imes 9$ grid partially filled with digits `'1'` through `'9'`, and empty cells indicated by `'.'`.
A valid solution must satisfy three non-negotiable constraints simultaneously:
1. Each of the digits `1-9` must occur exactly once in each **row**.
2. Each of the digits `1-9` must occur exactly once in each **column**.
3. Each of the digits `1-9` must occur exactly once in each of the nine **$3 	imes 3$ sub-boxes**.

---

## 2. Core Idea: Early-Exit Backtracking

Unlike Subsets or Permutations (where we want *all* solutions), Sudoku asks us to find **one valid completed board**.
Therefore:
- The recursive function returns `bool`.
- As soon as a branch returns `true`, we immediately return `true` up the call stack, halting further exploration.
- If all digits `'1'` through `'9'` fail for a cell, we reset the cell to `'.'` (backtrack) and return `false`.

### The 3x3 Sub-Box Mathematical Formula
To check if digit `d` exists in the $3 	imes 3$ box containing cell `(row, col)`:
- The top-left corner of the box is at `(3 * (row / 3), 3 * (col / 3))`.
- For index $i$ from $0$ to $8$:
  - Box row: `3 * (row / 3) + i / 3`
  - Box col: `3 * (col / 3) + i % 3`

---

## 3. Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    bool isValid(const vector<vector<char>>& board, int row, int col, char c) {
        for (int i = 0; i < 9; i++) {
            // Check row
            if (board[row][i] == c) return false;
            // Check column
            if (board[i][col] == c) return false;
            // Check 3x3 sub-box
            int boxRow = 3 * (row / 3) + i / 3;
            int boxCol = 3 * (col / 3) + i % 3;
            if (board[boxRow][boxCol] == c) return false;
        }
        return true;
    }

    bool solve(vector<vector<char>>& board) {
        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 9; j++) {
                // Find empty cell
                if (board[i][j] == '.') {
                    // Try digits '1' through '9'
                    for (char c = '1'; c <= '9'; c++) {
                        if (isValid(board, i, j, c)) {
                            board[i][j] = c; // Choose

                            // Explore: If downstream recursion succeeds, stop immediately!
                            if (solve(board)) {
                                return true;
                            }

                            // Backtrack: Undo choice
                            board[i][j] = '.';
                        }
                    }
                    // No digit 1-9 worked for this cell -> Dead end!
                    return false;
                }
            }
        }
        // No empty cells remaining -> Puzzle solved!
        return true;
    }

    void solveSudoku(vector<vector<char>>& board) {
        solve(board);
    }
};
```

---

## 🔍 Detailed Trace: Single Cell Decision

Suppose cell `(0, 2)` is empty:
1. Loop tries `c = '1'`: `isValid()` returns `false` (1 already in row 0).
2. Loop tries `c = '2'`: `isValid()` returns `false` (2 already in box 0).
3. Loop tries `c = '3'`: `isValid()` returns `true`!
   - `board[0][2] = '3'`
   - Recursive call `solve(board)` is invoked for subsequent cells.
   - If downstream cells hit a dead end and return `false`:
   - Backtrack triggers: `board[0][2] = '.'`.
   - Loop proceeds to try `c = '4'`.

---

## 🧠 Mental Model: The Lock-and-Key Grid

Think of the Sudoku grid as 81 tumbler locks. You find the first open tumbler (`'.'`), test keys 1 through 9. When a key fits without clicking a collision, you move to the next tumbler. If a downstream tumbler has no fitting key, you step back, remove the key, and try the next key.

---

## ⚠️ Common Mistakes

1. **Using `void` instead of `bool`:** If `solve()` returns `void`, the function will backtrack *after* finding the complete solution, wiping the board back to empty cells! Returning `bool` allows immediate early termination.
2. **Incorrect Box Indices:** Conflating `i / 3` and `i % 3`. `i / 3` advances rows, while `i % 3` advances columns.

---

## 🖥️ System-Specific Notes

- **Time Complexity Upper Bound:** Since the grid size is constant ($9 	imes 9 = 81$ cells), the time complexity is technically $O(1)$ in Big-O notation. However, in terms of empty cells $E$, the worst-case bound is $O(9^E)$. For practical boards ($E \le 60$), constraint propagation solves the board in milliseconds.
- **Maximum Recursion Depth:** At most 81 stack frames. Consumes negligible stack memory ($< 10	ext{ KB}$).

---

## 🟡 Additional Essential Context

In competitive programming and production solvers, Sudoku is optimized using:
- **Minimum Remaining Values (MRV) Heuristic:** Always solve the cell with the fewest valid candidate digits first.
- **Dancing Links (Algorithm X by Donald Knuth):** Formulates Sudoku as an Exact Cover Problem, solving in sub-millisecond times.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why can we check the row, column, and $3 	imes 3$ box in a single loop from $0$ to $8$?  
**A:** Because each check involves exactly 9 cells! Index $i \in [0, 8]$ allows indexing `board[row][i]` (row), `board[i][col]` (column), and `3*(row/3) + i/3, 3*(col/3) + i%3` (box) in parallel.

---

### 🔥 Interview Questions

#### Q1: What makes LeetCode 36 (Valid Sudoku) different from LeetCode 37 (Sudoku Solver)?
- **Short Answer:** Valid Sudoku only verifies that the *existing* numbers on the board do not violate rules ($O(1)$ single pass), whereas Sudoku Solver must *fill* empty cells via recursive backtracking ($O(9^E)$ search).

---

## 💻 Output / Debugging Questions

### 🐛 Debugging Challenge
What happens if you omit `return false;` after the `for (char c = '1'; c <= '9'; c++)` loop?
```cpp
// Flawed snippet
for (char c = '1'; c <= '9'; c++) {
    if (isValid(board, i, j, c)) {
        board[i][j] = c;
        if (solve(board)) return true;
        board[i][j] = '.';
    }
}
// MISSING return false; here!
```
**Why it fails:** If none of the digits `'1'` through `'9'` can be placed in cell `(i, j)`, control drops through to the outer loop or returns `true`, incorrectly reporting that the puzzle was solved despite invalid/unfilled cells!

---

## Edge Cases

1. **Board Already Fully Filled:** Function performs zero recursive calls and returns `true` immediately.
2. **Minimal Clues (17 clues):** Handled accurately within reasonable backtracking limits.

---

## Complexity Analysis

- **Time Complexity:** $O(9^E)$ where $E$ is the number of empty cells (bounded by $9^{81}$).
- **Auxiliary Space Complexity:** $O(E) \le 81$ (Recursion stack depth).

---

## Key Takeaways

1. **Early-Exit Backtracking:** Return `bool` to stop exploration upon finding the first valid board.
2. **Sub-box Formula:** `3 * (row / 3) + i / 3` and `3 * (col / 3) + i % 3`.
3. **Reset on Failure:** If no digit fits, reset to `'.'` and return `false`.

---

## ⚡ 2-Minute Revision

- Loop through all cells; find empty `'.'`.
- Try `'1'` to `'9'`. Check `isValid()`.
- If `solve(board)` succeeds $\to$ return `true`; else reset to `'.'`.

---

## 🧠 Core Intuition — The Lock-Tumbler Model

### Why Row-by-Row (Left-to-Right, Top-to-Bottom) Works
The traversal order `(i=0..8, j=0..8)` visits cells in **reading order**. This is critical because:
1. When we place a digit at `(i,j)`, cells **before** it (`(0,0)` to `(i,j-1)`) are fully determined.
2. Cells **after** it remain empty — we haven't constrained them yet.
3. The `solve()` function restarts from `(0,0)` each time it recurses. This means it re-scans already-filled cells (both original clues and our placements) until it finds the next empty `'.'`.

This simple linear scan is correct but slightly inefficient — an optimized solver would jump directly to the next empty cell.

### The Constraint Propagation Concept
Pure backtracking tries all 9 digits at each empty cell. **Constraint Propagation** reduces the domain before backtracking:

```
Cell (2,3) is empty.
Row 2 contains: {1, 4, 7, 9}
Col 3 contains: {2, 5, 8}
Box (0,1) contains: {3, 6}
Possible digits for (2,3): {1-9} - {1,4,7,9} - {2,5,8} - {3,6} = {} ← immediate dead end!
```

If any cell has 0 possible digits, we can fail immediately without trying. This is **Arc Consistency (AC-3)** — a technique used in world-class Sudoku solvers.

### Visualization: Single Cell Decision Tree
```
Empty cell (0,2):
     (0,2) = ?
    /  |  |  \
   1   2  3   4 ... 9
   ✗   ✗  ✓   ✗     ✗
       (row conflict) (col conflict) (box conflict)
       
   3 is valid! Place 3 and recurse to next empty cell.
   If downstream cells fail → backtrack here, try 4, 5, ...
```

---

## 🎯 Pattern Recognition — When to Use Boolean-Return Backtracking

### The "Find One Valid Solution" Pattern
```
find-one-solution problems:
  - Sudoku: Fill in digits s.t. constraints satisfied
  - N-Queens (variant): Find ANY valid placement
  - Word Search: Does a word exist on the grid?
  
Template: bool solve(...) {
    for each choice:
        if valid:
            make choice
            if (solve(...)) return true;  ← EARLY EXIT on first success
            undo choice
    return false;  ← MUST return false when no choice works
}
```

### Sudoku vs. N-Queens vs. Rat in Maze
| Aspect | Sudoku | N-Queens | Rat in Maze |
|---|---|---|---|
| Find how many solutions? | ONE | ALL | ALL paths |
| Return type | `bool` | `void` | `void` |
| State to restore | `board[i][j] = '.'` | `board[r][c] = '.'` | `maze[r][c] = 1` |
| Constraints | Row + Col + 3×3 Box | Col + 2 diagonals | Walls + visited |

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] Why does Sudoku Solver use `bool solve()` but Subsets uses `void`?
**Answer:** The difference is in the **objective**:
- Subsets needs **ALL** solutions → never stop early → `void` (no early return).
- Sudoku needs **ONE** solution → stop as soon as any valid board is found → `bool` (propagate `true` up immediately).

If Sudoku used `void`, after finding and printing the solution, it would continue backtracking → erasing all placed digits → returning a blank board! The `bool` return with `if (solve(board)) return true;` ensures the filled board is preserved.

---

### Q2: [Debug] What happens if you omit `return false;` after the digit-trying loop?
```cpp
for (char c = '1'; c <= '9'; c++) {
    if (isValid(board, i, j, c)) {
        board[i][j] = c;
        if (solve(board)) return true;
        board[i][j] = '.';
    }
}
// MISSING: return false;
// Control falls through to outer loop...
```
**Answer:** When no digit `'1'` through `'9'` can be placed at `(i,j)`, the function exits the loop without returning false. Control falls back to the outer `for (j = ...)` loop and moves to `(i, j+1)`. The function eventually exits the double loop and returns `true` — **falsely claiming the board is solved**! The board will have unfilled cells marked as `'.'` because the dead-end cell was never filled. This is one of the most common Sudoku bugs in interviews.

---

### Q3: [Conceptual] Can you check the row, column, and 3×3 box in a single loop from 0 to 8? Prove it.
**Answer:** Yes. For index `i ∈ [0, 8]`:
- **Row check:** `board[row][i]` visits all 9 columns in the given row.
- **Column check:** `board[i][col]` visits all 9 rows in the given column.
- **Box check:** Cell `(3*(row/3) + i/3, 3*(col/3) + i%3)` visits all 9 cells of the 3×3 sub-box.

**Proof for box:** `3*(row/3)` gives the row of the box's top-left corner. `i/3 ∈ {0,1,2}` gives the row offset within the box (0=first row, 1=second, 2=third). `3*(col/3)` gives the column of the box's top-left corner. `i%3 ∈ {0,1,2}` gives the column offset. As `i` runs from 0 to 8, `(i/3, i%3)` takes all 9 values in `{0,1,2}²` — covering the entire 3×3 sub-box.

---

### Q4: [Extension] What is Minimum Remaining Values (MRV) heuristic and why is it powerful?
**Answer:** MRV (also called Fail-First) chooses the next empty cell to fill as the one with **fewest valid digit candidates**. Instead of always scanning from top-left:
```cpp
// Find empty cell with minimum candidates
pair<int,int> findMRVCell(vector<vector<char>>& board) {
    int minCount = 10;
    pair<int,int> best = {-1, -1};
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            if (board[i][j] == '.') {
                int count = countValid(board, i, j);
                if (count < minCount) {
                    minCount = count;
                    best = {i, j};
                    if (minCount == 1) return best;  // Can't do better
                }
            }
        }
    }
    return best;
}
```
**Why it's powerful:** Cells with fewer valid digits fail faster → pruning happens higher in the tree → exponentially fewer total nodes explored. For hard Sudoku boards, MRV can reduce solve time from seconds to microseconds.

---

### Q5: [Complexity] What is the exact time complexity of Sudoku Solver?
**Answer:** The theoretical worst-case is $O(9^{81})$ — 9 choices for each of 81 cells. However:
- Given boards have pre-filled "clues" (typically 25-35 cells), leaving $E$ empty cells.
- Practical bound: $O(9^E)$ where $E \le 56$ for most valid Sudoku boards.
- With constraint propagation, most cells get their value forced (only 1 candidate), reducing the effective branching factor dramatically.
- Since the grid is fixed-size (9×9=81 cells), the algorithm is technically $O(1)$ in Big-O (constant input size), but expressing it as $O(9^E)$ is the meaningful complexity analysis.

---

### Q6: [Extension] How does Algorithm X (Dancing Links) solve Sudoku as an Exact Cover Problem?
**Answer:** Sudoku can be formulated as an **Exact Cover Problem**: given a set $U$ of "requirements" and a collection of "option" sets, select a subset of options that covers every requirement exactly once.

For Sudoku:
- Requirements: "row $r$ has digit $d$", "col $c$ has digit $d$", "box $b$ has digit $d$", "cell $(r,c)$ is filled"
- Options: "place digit $d$ at cell $(r,c)$" — satisfies 4 requirements simultaneously

**Dancing Links (DLX)** represents the constraint matrix as a doubly-linked list and uses column-selection heuristics (most constrained first) to solve in near-linear time for typical Sudoku boards — 10-100× faster than simple backtracking.

---

## 📊 Complexity Analysis — Extended

### Practical Performance on Sudoku
| Method | Typical Hard Board | Worst Case |
|---|---|---|
| Pure backtracking | ~1,000 cells visited | $O(9^{81})$ |
| Backtracking + constraint prop | ~100 cells | $O(9^E)$, E small |
| MRV heuristic | ~10-50 cells | $O(9^E)$, E tiny |
| Dancing Links (DLX) | < 10ms | $O(9^E)$ but tiny |

### Why `isValid()` Costs $O(27)$ per Call
The single loop from 0 to 8 performs exactly 27 cell checks:
- 9 cells in the row
- 9 cells in the column  
- 9 cells in the 3×3 box

$O(27) = O(1)$ since 27 is a constant. With pre-maintained boolean arrays (as in the optimized version), this becomes $O(3) = O(1)$ — 3 boolean lookups.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Connection |
|---|---|---|
| 37 | Sudoku Solver | Direct — this problem |
| 36 | Valid Sudoku | Verify existing board (no backtracking needed — single O(N²) pass) |
| 51 | N-Queens | Same `bool solve()` pattern, different constraints |
| 79 | Word Search | 2D grid DFS with `bool` return and cell marking |
| 489 | Robot Room Cleaner | 2D grid exploration with state restoration |

---

## 🔗 Cross-Topic Connections

- **→ N-Queens (File 05):** Both use `bool`-returning backtracking to find ONE solution. Both restore state on backtrack. Sudoku has 3 constraint types vs. N-Queens' 3 attack directions.
- **→ Constraint Propagation → DP:** Constraint propagation (AC-3) for Sudoku is a greedy-style reduction that often eliminates the need for backtracking entirely on easy boards.
- **→ Graph Coloring:** Sudoku is graph coloring — cells are nodes, edges connect cells that share a row/col/box, and colors are digits 1-9. This is NP-complete in the general case.
- **→ Exact Cover / Dancing Links:** Advanced CS topic — Sudoku as a specialized Exact Cover Problem, solved by Knuth's Algorithm X.

---

## ⚡ 2-Minute Revision Flash Card (Enhanced)

- **`bool` return is critical:** Propagates success upward immediately → preserves the filled board.
- **Missing `return false`:** Function claims dead-end cells are "solved" → wrong board returned.
- **Box formula:** Top-left corner at `(3*(row/3), 3*(col/3))`; cell `i` at offset `(i/3, i%3)`.
- **Optimization:** MRV heuristic (pick cell with fewest candidates) dramatically reduces backtracking.
- **Complexity:** $O(9^E)$ where $E$ = empty cells; technically $O(1)$ since grid is fixed 9×9.
