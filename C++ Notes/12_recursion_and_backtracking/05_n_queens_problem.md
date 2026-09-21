# Lecture 46: N-Queens Problem: Classical Backtracking (LeetCode 51)

> **One-Line Purpose:** Master 2D grid backtracking by placing $N$ non-attacking queens on an $N 	imes N$ chessboard, establishing diagonal invariant collision math, and optimizing safety checks from $O(N)$ to $O(1)$.

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
- The rules of the N-Queens problem: placing $N$ queens on an $N 	imes N$ chessboard such that no two queens threaten each other.
- Why placing exactly **one queen per row** eliminates all row-conflict checks.
- The 3 safety invariants to check before placing a queen: Vertical Column, Upper-Left Diagonal ($
warrow$), and Upper-Right Diagonal ($
earrow$).
- Why lower diagonals do not need to be checked (because future rows have not been populated yet).
- How to optimize safety checks from $O(N)$ down to $O(1)$ using hash sets or boolean lookup bitmasks.

---

## 🔵 Lecture Context

N-Queens is the canonical benchmark problem for constraint satisfaction and state-space pruning. It demonstrates how intelligent constraint checking prunes an intractable search space ($N^N$ brute force) into an efficient $O(N!)$ backtracking tree.

---

## 1. Problem Statement & Queen Mechanics

A Queen in chess can move any number of squares horizontally, vertically, or diagonally.
Two queens attack each other if they share:
1. The same row: $	ext{row}_1 == 	ext{row}_2$
2. The same column: $	ext{col}_1 == 	ext{col}_2$
3. The same diagonal: $|	ext{row}_1 - 	ext{row}_2| == |	ext{col}_1 - 	ext{col}_2|$

**Goal:** Return all distinct board configurations for $N$ non-attacking queens on an $N 	imes N$ board. Represent empty squares as `'.'` and queens as `'Q'`.

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
2. **Upper-Left Diagonal ($
warrow$):** No queen in `(r-1, c-1), (r-2, c-2), \dots`.
3. **Upper-Right Diagonal ($
earrow$):** No queen in `(r-1, c+1), (r-2, c+2), \dots`.

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

    cout << "Total Solutions for N=" << n << ": " << solutions.size() << "

";
    for (const auto& sol : solutions) {
        for (const string& row : sol) {
            cout << row << "
";
        }
        cout << "
";
    }
    return 0;
}
```

---

## 4. $O(1)$ Safety Check Optimization via Hash Sets

In the standard approach, `isSafe()` takes $O(N)$ time. We can achieve $O(1)$ checks:
1. `cols[col]`: Tracks whether column `col` is occupied.
2. `leftDiag[row - col + (n - 1)]`: Invariant for upper-left to bottom-right diagonals ($ackslash$): $row - col$ is constant.
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

In LeetCode 52 (N-Queens II), you only need to return the *total count* of solutions rather than all board layouts. Using bitmasks (`int` bitwise flags for columns and diagonals) makes LeetCode 52 run under $1	ext{ ms}$.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why does N-Queens run in $O(N!)$ time rather than $O(N^N)$?  
**A:** Because in row 0 we have $N$ choices, in row 1 at most $N-1$ choices (since one column is blocked), in row 2 at most $N-2$ choices, and so on. This strictly bounds the state tree leaves by $N 	imes (N-1) 	imes (N-2) 	imes \dots = N!$.

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
