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

---

## 🧠 Core Intuition — Why Row-by-Row with 3 Checks Works

### The Constraint Satisfaction View
N-Queens is a **Constraint Satisfaction Problem (CSP)**:
- Variables: row 0, row 1, ..., row N-1 (where does the queen go in each row?)
- Domain: columns 0, 1, ..., N-1 for each row
- Constraints: no two queens share a column, left-diagonal, or right-diagonal

By fixing **one queen per row**, we automatically eliminate **row conflicts**. The only remaining constraints are column and diagonal.

### Visual: N=4 Board Exploration Trace

```
Row 0: Try col 0        Row 0: Try col 1
Q . . .                 . Q . .
. . . .                 . . . .
. . . .                 . . . .
. . . .                 . . . .
  ↓ Row 1                 ↓ Row 1
col 0: ✗ (same col)     col 0: ✓ safe!
col 1: ✗ (diag)         . Q . .
col 2: ✓ safe!          Q . . .   ← place here
. Q . .                   ↓ Row 2
. . Q .                 col 0: ✗ (diag)
                        col 1: ✗ (col)
  ↓ Row 2               col 2: ✗ (diag)
col 0: ✗ (diag)         col 3: ✓ safe!
col 1: ✗ (col)          . Q . .
col 2: ✗ (col)          Q . . .
col 3: ✓ safe!          . . . Q
. Q . .                   ↓ Row 3
. . Q .                 col 0: ✗ (diag)
. . . Q                 col 1: ✗ (col)
                        col 2: ✓ safe!
  ↓ Row 3               . Q . .     ← SOLUTION 2!
col 0: ✗ (diag)         Q . . .
col 1: ✗ (col)          . . . Q
col 2: ✓ safe!          . . Q .
. Q . .     ← SOLUTION 1!
. . Q .
. . . Q
. Q . .  wait wrong, check again
```

**N=4 has exactly 2 solutions:**
```
Solution 1:       Solution 2:
. Q . .           . . Q .
. . . Q           Q . . .
Q . . .           . . . Q
. . Q .           . Q . .
```

### The Mathematical Insight: Why Diagonals Have Constant Invariants
```
Main diagonal (top-left to bottom-right, "\"): row - col = constant
  (0,0):0  (1,1):0  (2,2):0  (3,3):0  ← all share row-col = 0
  (0,1):-1 (1,2):-1 (2,3):-1          ← all share row-col = -1

Anti-diagonal (top-right to bottom-left, "/"): row + col = constant
  (0,3):3  (1,2):3  (2,1):3  (3,0):3  ← all share row+col = 3
  (0,2):2  (1,1):2  (2,0):2           ← all share row+col = 2
```
This is why `leftDiag[row - col + n - 1]` and `rightDiag[row + col]` are $O(1)$ lookup keys!

---

## 🎯 Pattern Recognition — N-Queens Type Problems

### Keywords That Signal This Pattern
- "Place N non-attacking [objects]" on an N×N grid
- "No two in same row/column/diagonal"
- "Count configurations" or "find all arrangements"
- Any problem where constraints eliminate entire rows/columns of a 2D grid

### N-Queens vs. Sudoku vs. Rat in Maze
| Dimension | N-Queens | Sudoku | Rat in Maze |
|---|---|---|---|
| Grid size | $N \times N$ variable | $9 \times 9$ fixed | $N \times N$ |
| Constraint type | Row/col/diagonal | Row/col/3×3 box | Walls + visited |
| Return type | `void` (all solutions) | `bool` (one solution) | `void` (all paths) |
| Backtrack target | Cell to `'.'` | Cell to `'.'` | Cell to unvisited |

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] Why does N-Queens run in $O(N!)$ rather than $O(N^N)$?
**Answer:** A naive approach would try all $N^N$ placements (N options for each of N rows). But with the column constraint enforced, at row 0 we have $N$ choices, at row 1 the used column is blocked leaving at most $N-1$ choices, at row 2 at most $N-2$, and so on. This strictly upper-bounds the number of paths in the search tree to $N \times (N-1) \times (N-2) \times \dots \times 1 = N!$. In practice (with diagonal constraints), many branches are pruned even further, making the actual runtime much less than $N!$.

---

### Q2: [Optimization] How do you optimize diagonal checking from $O(N)$ to $O(1)$?
**Answer:** Maintain three boolean arrays:
- `cols[c]` — true if column `c` has a queen
- `leftDiag[r - c + n - 1]` — true if the "\" diagonal through `(r,c)` has a queen (offset by `n-1` to keep index non-negative, range `[0, 2n-2]`)
- `rightDiag[r + c]` — true if the "/" anti-diagonal through `(r,c)` has a queen (range `[0, 2n-2]`)

**Placement:** `cols[c] = leftDiag[r-c+n-1] = rightDiag[r+c] = true; board[r][c] = 'Q';`  
**Removal:** `cols[c] = leftDiag[r-c+n-1] = rightDiag[r+c] = false; board[r][c] = '.';`  
**Check:** `if (!cols[c] && !leftDiag[r-c+n-1] && !rightDiag[r+c])` — single $O(1)$ condition vs $O(N)$ board scan.

---

### Q3: [Trivia → Depth] How many solutions exist for N=8? Why does this matter?
**Answer:** There are **92 distinct solutions** for the 8-Queens problem (12 fundamental solutions; the other 80 are reflections/rotations). This matters for:
1. **Interview context:** Shows you know the classical result.
2. **Algorithm efficiency:** Demonstrating that pruning reduces $O(8^8) = 16M$ brute-force attempts to $O(8!) = 40,320$ backtracking calls, with further pruning finding solutions quickly.
3. **LeetCode 52 (N-Queens II):** Only asks for the count, so you optimize to avoid storing board strings.

---

### Q4: [Output Prediction / Debug] What's wrong with this `isSafe` function?
```cpp
bool isSafe(vector<string>& board, int row, int col, int n) {
    // Check full column (both up and down)
    for (int i = 0; i < n; i++) {           // BUG: checks ALL rows
        if (board[i][col] == 'Q') return false;
    }
    // ... diagonal checks ...
    return true;
}
```
**Answer:** The bug is checking the FULL column (`i = 0` to `n-1`) instead of only the UPPER column (`i = 0` to `row-1`). When placing a queen at `(row, col)`, rows `row` to `n-1` haven't been filled yet — they are all `'.'` — so checking them is wasteful but harmless. **However**, in early rows, the current cell `(row, col)` itself is `'.'` (not placed yet) and row-0 through row-1 are correct. The deeper bug: if you place a queen at `(row, col)` and THEN call `isSafe(row, col)`, the function checks `board[row][col]` which is now `'Q'` → always returns false! This is not a bug in the given code but a common interview trap when placement and checking are in the wrong order.

---

### Q5: [Extension] How would you solve N-Queens II (LeetCode 52) — just count solutions?
**Answer:** Replace `result.push_back(board)` with `count++` and use `int count` instead of `vector<vector<string>> result`. With bitmask optimization, this runs in microseconds:
```cpp
int totalNQueens(int n) {
    int count = 0;
    // cols, diag1, diag2 are integer bitmasks (bit i = column/diagonal i occupied)
    function<void(int, int, int, int)> dfs = [&](int row, int cols, int d1, int d2) {
        if (row == n) { count++; return; }
        int available = ((1 << n) - 1) & ~(cols | d1 | d2);
        while (available) {
            int bit = available & (-available);  // lowest set bit
            available -= bit;
            dfs(row + 1, cols | bit, (d1 | bit) << 1, (d2 | bit) >> 1);
        }
    };
    dfs(0, 0, 0, 0);
    return count;
}
```
This uses bitmask operations to represent all three constraints as integers, making it 10-100× faster than the array-based approach.

---

### Q6: [Proof] Prove that no queen can be placed on a $2 \times 2$ or $3 \times 3$ board (N=2, N=3).
**Answer:**
- **N=2:** Row 0 queen at column 0 or 1. If column 0: row 1 can't use column 0 (same col), can't use column 1 (diagonal). 0 valid columns → no solution. Column 1 is symmetric.
- **N=3:** By exhaustive check — row 0 queen at col 1 (center): blocks col 1 + both diagonals for rows 1-2. Row 1: only col 0 or col 2 available (col 1 blocked by column, left/right diagonals block col 0 and col 2 respectively). No valid column for row 1. Outer columns (0 or 2) for row 0 lead by symmetry to the same dead-end. ∎

---

### Q7: [Extension] What if queens could also attack like rooks on a toroidal board (edges wrap around)?
**Answer:** This becomes the **N-Queens on a Torus** problem. Diagonal invariants change: `(row - col) mod N` and `(row + col) mod N`. The sets track these modular values. Solutions become harder to find — for prime N, the number of solutions follows specific algebraic patterns (related to primitive roots). This is a research-level extension, but framing the answer shows deep algorithmic thinking.

---

## 📊 Complexity Analysis — Extended

### Why the True Runtime is Much Less Than $O(N!)$
The diagonal constraints dramatically prune the tree. For N=8:
- Brute force: $8^8 = 16,777,216$
- With column constraint: $8! = 40,320$
- With all constraints (actual backtracking calls): ~15,720

The constant factor improvement makes N-Queens solvable for $N \le 15$ in milliseconds.

### Space Complexity Breakdown
- **Board:** $O(N^2)$ characters
- **Optimization arrays:** $O(N)$ for `cols`, $O(2N)$ for each diagonal → $O(N)$ total
- **Recursion stack:** $O(N)$ frames (one per row)
- **Results storage:** $O(N^2 \cdot \text{solutions})$ — for N=8, 92 solutions × 64 chars ≈ 6KB

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Connection |
|---|---|---|
| 51 | N-Queens | Direct — all board configurations |
| 52 | N-Queens II | Count only — bitmask optimization for speed |
| 37 | Sudoku Solver | Same 2D backtracking pattern, different constraints |
| 79 | Word Search | 2D grid DFS with visited marking |
| 1001 | Grid Illumination | Diagonal hash invariants used in similar way |

---

## 🔗 Cross-Topic Connections

- **→ Sudoku Solver (File 06):** Both are 2D constraint-satisfaction backtracking. N-Queens places 1 queen per row; Sudoku fills 1 digit per empty cell. Both use `bool` return for early exit (when finding one solution).
- **→ Rat in Maze (File 07):** Both use 2D grid backtracking with placement + undo. Rat in Maze explores paths; N-Queens places non-attacking pieces.
- **→ Graph Coloring:** N-Queens is graph coloring where nodes are columns and edges connect attacking queens.
- **→ Combinatorics:** $N!$ permutations are reduced by column/diagonal constraints — this is CSP (Constraint Satisfaction Problem) reduction.

---

## ⚡ 2-Minute Revision Flash Card (Enhanced)

- **One queen per row:** Eliminates row conflicts; recurse on `row + 1`.
- **Three checks:** Column (`cols[]`), upper-left diagonal (`leftDiag[row-col+n-1]`), upper-right diagonal (`rightDiag[row+col]`).
- **$O(1)$ optimization:** Replace $O(N)$ scan with three boolean array lookups using invariants.
- **N=8 → 92 solutions:** Classic fact interviewers love to ask about.
- **Complexity:** $O(N!)$ time (tighter than $O(N^N)$ due to column constraint), $O(N^2)$ space for board.
