import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t12_dir = os.path.join(root, "12_recursion_and_backtracking")

notes = {}

# 05: N-Queens
notes["05_n_queens_problem.md"] = """# Lecture 46: N-Queens Problem: Classical Backtracking (LeetCode 51)

> **One-Line Purpose:** Master 2D grid backtracking by placing $N$ non-attacking queens on an $N \times N$ chessboard, establishing diagonal invariant collision math, and optimizing safety checks from $O(N)$ to $O(1)$.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #46  
> **Video ID:** `BdSJnIdR-4s`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=BdSJnIdR-4s)  
> **Duration:** 24:26  
> **Transcript:** `.transcripts/12_recursion_and_backtracking/046_N-Queens_Problem___using_Backtracking___Leetcode_Hard.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The rules of the N-Queens problem: placing $N$ queens on an $N \times N$ chessboard such that no two queens threaten each other.
- Why placing exactly **one queen per row** eliminates all row-conflict checks.
- The 3 safety invariants to check before placing a queen: Vertical Column, Upper-Left Diagonal ($\nwarrow$), and Upper-Right Diagonal ($\nearrow$).
- Why lower diagonals do not need to be checked (because future rows have not been populated yet).
- How to optimize safety checks from $O(N)$ down to $O(1)$ using hash sets or boolean lookup bitmasks.

---

## 🔵 Lecture Context

N-Queens is the canonical benchmark problem for constraint satisfaction and state-space pruning. It demonstrates how intelligent constraint checking prunes an intractable search space ($N^N$ brute force) into an efficient $O(N!)$ backtracking tree.

---

## 1. Problem Statement & Queen Mechanics

A Queen in chess can move any number of squares horizontally, vertically, or diagonally.
Two queens attack each other if they share:
1. The same row: $\text{row}_1 == \text{row}_2$
2. The same column: $\text{col}_1 == \text{col}_2$
3. The same diagonal: $|\text{row}_1 - \text{row}_2| == |\text{col}_1 - \text{col}_2|$

**Goal:** Return all distinct board configurations for $N$ non-attacking queens on an $N \times N$ board. Represent empty squares as `'.'` and queens as `'Q'`.

```
4-Queens Valid Solution:
. Q . .
. . . Q
Q . . .
. . Q .
```

---

## 2. The Algorithmic Insight: Row-by-Row Placement

Instead of trying to place queens in arbitrary cells:
- Since every valid configuration must have exactly 1 queen in each of the $N$ rows, we advance row-by-row: `row = 0, 1, 2, ..., N-1`.
- In each row `r`, try placing a queen in column `c` (from $0$ to $N-1$).
- If cell `(r, c)` is safe, place the queen (`board[r][c] = 'Q'`), recurse on `r + 1`, and then backtrack (`board[r][c] = '.'`).

### The Safety Invariant:
When placing in row `r`:
1. **Column:** No queen above in column `c`.
2. **Upper-Left Diagonal ($\nwarrow$):** No queen in `(r-1, c-1), (r-2, c-2), \dots`.
3. **Upper-Right Diagonal ($\nearrow$):** No queen in `(r-1, c+1), (r-2, c+2), \dots`.

---

## 3. Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <string>
using namespace std;

class Solution {
public:
    bool isSafe(const vector<string>& board, int row, int col, int n) {
        // 1. Check Vertical Column upward
        for (int i = 0; i < row; i++) {
            if (board[i][col] == 'Q') return false;
        }

        // 2. Check Upper-Left Diagonal (r - 1, col - 1)
        for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--) {
            if (board[i][j] == 'Q') return false;
        }

        // 3. Check Upper-Right Diagonal (r - 1, col + 1)
        for (int i = row - 1, j = col + 1; i >= 0 && j < n; i--, j++) {
            if (board[i][j] == 'Q') return false;
        }

        return true;
    }

    void nQueensHelper(vector<string>& board, int row, int n, vector<vector<string>>& result) {
        // Base Case: All N queens successfully placed in rows 0 ... N-1
        if (row == n) {
            result.push_back(board);
            return;
        }

        // Try placing queen in each column of the current row
        for (int col = 0; col < n; col++) {
            if (isSafe(board, row, col, n)) {
                // Choose
                board[row][col] = 'Q';

                // Explore deeper rows
                nQueensHelper(board, row + 1, n, result);

                // Backtrack (Un-choose)
                board[row][col] = '.';
            }
        }
    }

    vector<vector<string>> solveNQueens(int n) {
        vector<vector<string>> result;
        vector<string> board(n, string(n, '.'));
        nQueensHelper(board, 0, n, result);
        return result;
    }
};

int main() {
    Solution solver;
    int n = 4;
    vector<vector<string>> solutions = solver.solveNQueens(n);

    cout << "Total Solutions for N=" << n << ": " << solutions.size() << "\n\n";
    for (const auto& sol : solutions) {
        for (const string& row : sol) {
            cout << row << "\n";
        }
        cout << "\n";
    }
    return 0;
}
```

---

## 4. $O(1)$ Safety Check Optimization via Hash Sets

In the standard approach, `isSafe()` takes $O(N)$ time. We can achieve $O(1)$ checks:
1. `cols[col]`: Tracks whether column `col` is occupied.
2. `leftDiag[row - col + (n - 1)]`: Invariant for upper-left to bottom-right diagonals ($\backslash$): $row - col$ is constant.
3. `rightDiag[row + col]`: Invariant for upper-right to bottom-left diagonals ($/$): $row + col$ is constant.

```cpp
// O(1) Check using 3 boolean arrays
if (!cols[col] && !leftDiag[row - col + n - 1] && !rightDiag[row + col]) {
    cols[col] = leftDiag[row - col + n - 1] = rightDiag[row + col] = true;
    board[row][col] = 'Q';
    
    nQueensHelper(row + 1);
    
    // Backtrack
    cols[col] = leftDiag[row - col + n - 1] = rightDiag[row + col] = false;
    board[row][col] = '.';
}
```

---

## 🧠 Mental Model: The Diagonal Invariants

```
Main Diagonal (row - col):
   c=0  c=1  c=2  c=3
r=0  0   -1   -2   -3
r=1  1    0   -1   -2
r=2  2    1    0   -1
r=3  3    2    1    0
All cells along any parallel diagonal have the IDENTICAL value of (row - col)!

Anti-Diagonal (row + col):
   c=0  c=1  c=2  c=3
r=0  0    1    2    3
r=1  1    2    3    4
r=2  2    3    4    5
r=3  3    4    5    6
All cells along any anti-diagonal have the IDENTICAL value of (row + col)!
```

---

## ⚠️ Common Mistakes

1. **Checking Lower Rows:** Checking `row + 1` or lower diagonals is unnecessary because lower rows have no queens yet. Doing so wastes CPU cycles.
2. **Incorrect Diagonal Offset:** Forgetting the `+ (n - 1)` offset in `row - col`. Since `row - col` can be negative (down to $-(n-1)$), array indexing without the offset causes an out-of-bounds crash.

---

## 🖥️ System-Specific Notes

- For $N = 1$, there is 1 solution (`["Q"]`).
- For $N = 2$ and $N = 3$, there are **0 solutions** mathematically.
- For $N = 8$, there are 92 distinct solutions (12 fundamental symmetric solutions).
- For $N = 14$, there are 365,596 solutions; memory allocations must be handled carefully.

---

## 🟡 Additional Essential Context

In LeetCode 52 (N-Queens II), you only need to return the *total count* of solutions rather than all board layouts. Using bitmasks (`int` bitwise flags for columns and diagonals) makes LeetCode 52 run under $1\text{ ms}$.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why does N-Queens run in $O(N!)$ time rather than $O(N^N)$?  
**A:** Because in row 0 we have $N$ choices, in row 1 at most $N-1$ choices (since one column is blocked), in row 2 at most $N-2$ choices, and so on. This strictly bounds the state tree leaves by $N \times (N-1) \times (N-2) \times \dots = N!$.

---

### 🔥 Interview Questions

#### Q1: How do you represent diagonals using bit manipulation in C++?
- **Short Answer:** Use an `int` mask where the $k$-th bit represents whether the $k$-th diagonal is occupied.
- **Detailed Explanation:** `colMask |= (1 << col)`, `diag1Mask |= (1 << (row + col))`, and `diag2Mask |= (1 << (row - col + n - 1))`. Checking safety is a single bitwise AND: `(colMask & (1 << col)) == 0`.

---

## 💻 Output / Debugging Questions

### Output Prediction
How many solutions exist for $N = 4$?  
**Output:** `2` solutions:
`[".Q..", "...Q", "Q...", "..Q."]` and `["..Q.", "Q...", "...Q", ".Q.."]`.

---

## Edge Cases

1. **$N = 1$:** Returns `[["Q"]]`.
2. **$N = 2, 3$:** Returns `[]` (empty vector).

---

## Complexity Analysis

- **Time Complexity:** $O(N!)$ (Bounded by $N$ choices in first row, $N-1$ in second, etc.).
- **Auxiliary Space Complexity:** $O(N^2)$ for board storage + $O(N)$ for the recursion stack.

---

## Key Takeaways

1. **Row-by-Row Advancement:** Eliminates row conflict checks entirely.
2. **Three Safety Invariants:** Check Column, Upper-Left Diagonal, Upper-Right Diagonal.
3. **$O(1)$ Optimization:** Use mathematical invariants `row - col + n - 1` and `row + col`.

---

## ⚡ 2-Minute Revision

- One queen per row: `nQueens(row + 1)`.
- Upper-left diagonal: `(r-1, c-1)`; Upper-right diagonal: `(r-1, c+1)`.
- Revert: `board[r][c] = '.'` during backtracking.
"""

# 06: Sudoku Solver
notes["06_sudoku_solver.md"] = """# Lecture 47: Sudoku Solver: 2D Constraint Backtracking (LeetCode 37)

> **One-Line Purpose:** Master multi-constraint 2D grid backtracking by solving 9x9 Sudoku boards in-place, enforcing row, column, and $3 \times 3$ sub-box invariants with early-exit boolean recursion.

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
- The mathematical mapping for $3 \times 3$ sub-grid box checking: row $3 \times (r / 3) + i / 3$ and column $3 \times (c / 3) + i \% 3$.
- State restoration (`board[i][j] = '.'`) when a tested digit causes an downstream dead end.

---

## 🔵 Lecture Context

Sudoku Solver is a classic LeetCode Hard interview problem. It combines nested coordinate grid traversal, multi-rule validation, and early-exit backtracking.

---

## 1. Problem Statement & Rules of Sudoku

A Sudoku board is a $9 \times 9$ grid partially filled with digits `'1'` through `'9'`, and empty cells indicated by `'.'`.
A valid solution must satisfy three non-negotiable constraints simultaneously:
1. Each of the digits `1-9` must occur exactly once in each **row**.
2. Each of the digits `1-9` must occur exactly once in each **column**.
3. Each of the digits `1-9` must occur exactly once in each of the nine **$3 \times 3$ sub-boxes**.

---

## 2. Core Idea: Early-Exit Backtracking

Unlike Subsets or Permutations (where we want *all* solutions), Sudoku asks us to find **one valid completed board**.
Therefore:
- The recursive function returns `bool`.
- As soon as a branch returns `true`, we immediately return `true` up the call stack, halting further exploration.
- If all digits `'1'` through `'9'` fail for a cell, we reset the cell to `'.'` (backtrack) and return `false`.

### The 3x3 Sub-Box Mathematical Formula
To check if digit `d` exists in the $3 \times 3$ box containing cell `(row, col)`:
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

- **Time Complexity Upper Bound:** Since the grid size is constant ($9 \times 9 = 81$ cells), the time complexity is technically $O(1)$ in Big-O notation. However, in terms of empty cells $E$, the worst-case bound is $O(9^E)$. For practical boards ($E \le 60$), constraint propagation solves the board in milliseconds.
- **Maximum Recursion Depth:** At most 81 stack frames. Consumes negligible stack memory ($< 10\text{ KB}$).

---

## 🟡 Additional Essential Context

In competitive programming and production solvers, Sudoku is optimized using:
- **Minimum Remaining Values (MRV) Heuristic:** Always solve the cell with the fewest valid candidate digits first.
- **Dancing Links (Algorithm X by Donald Knuth):** Formulates Sudoku as an Exact Cover Problem, solving in sub-millisecond times.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why can we check the row, column, and $3 \times 3$ box in a single loop from $0$ to $8$?  
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
"""

print("Writing batch 2 notes...")
for fn, content in notes.items():
    with open(os.path.join(t12_dir, fn), "w", encoding="utf-8") as f:
        f.write(content)
print("Updated 05, 06.")
