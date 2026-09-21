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
- If `solve(board)` succeeds $	o$ return `true`; else reset to `'.'`.
