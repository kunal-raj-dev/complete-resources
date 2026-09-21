# Lecture 55: Knight's Tour Problem: Board Traversal Backtracking (LeetCode 2596)

> **One-Line Purpose:** Master constrained 2D grid path finding by visiting all $N^2$ squares of a chessboard exactly once using the Knight's L-shaped moves and Warnsdorff's heuristic.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #55  
> **Video ID:** `Sp1jzttFVdE`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=Sp1jzttFVdE)  
> **Duration:** 22:32  
> **Transcript:** `.transcripts/12_recursion_and_backtracking/055_KNIGHTS_TOUR_Problem_-_Backtracking___Leetcode_2596.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The rules of the Knight's Tour: visiting all $N \times N$ cells of a chessboard with a knight, landing on each square exactly once.
- The 8 legal L-shaped moves of a knight in 2D coordinate space.
- The distinction between verifying an existing tour (LeetCode 2596: $O(N^2)$ simulation) versus generating a tour from scratch (Backtracking: $O(8^{N^2})$).
- Warnsdorff's Heuristic: choosing the move that has the minimum number of onward legal moves.

---

## 🔵 Lecture Context

The Knight's Tour is a historical mathematical puzzle (Euler, 1759) and a premier computer science demonstration of Hamiltonian paths on graphs and state-space pruning.

---

## 1. Problem Statement & Knight Mechanics

A Knight moves in an "L-shape": two squares along one axis and one square along the perpendicular axis.
From cell `(r, c)`, there are at most 8 possible moves:
1. `(r + 2, c + 1)`
2. `(r + 2, c - 1)`
3. `(r - 2, c + 1)`
4. `(r - 2, c - 1)`
5. `(r + 1, c + 2)`
6. `(r + 1, c - 2)`
7. `(r - 1, c + 2)`
8. `(r - 1, c - 2)`

**Goal:** Fill an $N \times N$ board with step numbers $0, 1, 2, \dots, N^2 - 1$ such that each step represents a valid knight jump from the preceding step.

---

## 2. Complete C++ Implementation (Backtracking Generator)

```cpp
#include <iostream>
#include <vector>
using namespace std;

// 8 legal knight move offsets
const int dRow[8] = {-2, -2, -1, -1,  1,  1,  2,  2};
const int dCol[8] = {-1,  1, -2,  2, -2,  2, -1,  1};

bool isValidMove(int r, int c, int n, const vector<vector<int>>& board) {
    return (r >= 0 && r < n && c >= 0 && c < n && board[r][c] == -1);
}

bool solveKnightTour(vector<vector<int>>& board, int r, int c, int step, int n) {
    // Base Case: All N*N squares visited!
    if (step == n * n) {
        return true;
    }

    // Try all 8 possible moves
    for (int i = 0; i < 8; i++) {
        int nextRow = r + dRow[i];
        int nextCol = c + dCol[i];

        if (isValidMove(nextRow, nextCol, n, board)) {
            board[nextRow][nextCol] = step; // Choose

            if (solveKnightTour(board, nextRow, nextCol, step + 1, n)) {
                return true; // Stop immediately upon finding complete tour
            }

            board[nextRow][nextCol] = -1; // Backtrack
        }
    }

    return false;
}

int main() {
    int n = 8;
    vector<vector<int>> board(n, vector<int>(n, -1));

    // Start at (0, 0) as step 0
    board[0][0] = 0;

    if (solveKnightTour(board, 0, 0, 1, n)) {
        cout << "Knight's Tour Found:\n";
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                cout << (board[i][j] < 10 ? " " : "") << board[i][j] << " ";
            }
            cout << "\n";
        }
    } else {
        cout << "No Knight's Tour exists.\n";
    }
    return 0;
}
```

---

## 3. LeetCode 2596: Check Knight Tour Configuration

In LeetCode 2596, we are given an existing board and must determine if it represents a valid tour starting from `grid[0][0] == 0`:

```cpp
class Solution {
public:
    bool checkValidGrid(vector<vector<int>>& grid) {
        if (grid[0][0] != 0) return false;
        int n = grid.size();

        // Map step number to (row, col) coordinates
        vector<pair<int, int>> pos(n * n);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                pos[grid[i][j]] = {i, j};
            }
        }

        // Verify that consecutive steps are valid L-moves
        for (int step = 1; step < n * n; step++) {
            int dr = abs(pos[step].first - pos[step - 1].first);
            int dc = abs(pos[step].second - pos[step - 1].second);

            if (!((dr == 1 && dc == 2) || (dr == 2 && dc == 1))) {
                return false;
            }
        }
        return true;
    }
};
```

---

## 🧠 Mental Model: Warnsdorff's Heuristic

Naive backtracking on an $8 \times 8$ board can take hours because it explores billions of dead-end paths.
**Warnsdorff's Rule:** Always move the knight to the neighbor cell that has the **fewest onward available moves**! This keeps the knight along the outer borders and corners first, preventing it from isolating open squares in corners later.

---

## ⚠️ Common Mistakes

1. **Not checking `grid[0][0] == 0`:** In LeetCode 2596, if the knight does not start at the top-left square, the grid is invalid by definition.
2. **Missing `board[r][c] == -1` check:** Visiting an already-stepped cell triggers infinite cyclic wandering.

---

## 🖥️ System-Specific Notes

- For an $8 \times 8$ board, pure brute force without heuristics has $8^{64}$ worst-case complexity. Warnsdorff's heuristic solves the $8 \times 8$ tour in under $5\text{ ms}$.

---

## 🟡 Additional Essential Context

The Knight's Tour problem is a specific instance of finding a **Hamiltonian Path** in a graph where vertices are board cells and edges are legal knight moves.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** What is an "Open Tour" vs a "Closed Tour"?  
**A:** In an Open Tour, the knight finishes on a square that does not attack the starting square. In a Closed (Re-entrant) Tour, the final square is exactly one knight move away from the starting square, forming a continuous cycle.

---

### 🔥 Interview Questions

#### Q1: What is the time complexity of verifying a Knight's Tour (LeetCode 2596)?
- **Short Answer:** $O(N^2)$ time and $O(N^2)$ space.
- **Detailed Explanation:** We map all $N^2$ numbers to coordinates in a single pass, then check the distance between adjacent numbers in $N^2 - 1$ steps.

---

## 💻 Output / Debugging Questions

### Output Prediction
Is `abs(r1 - r2) * abs(c1 - c2) == 2` a valid check for knight moves?  
**Answer:** Yes! The product of $\Delta r$ and $\Delta c$ must be $1 \times 2 = 2$ or $2 \times 1 = 2$. If either is $0$ or equal, the product cannot be $2$.

---

## Edge Cases

1. **Small Boards ($N \le 4$):** No knight's tour exists for $N = 2, 3, 4$ (except trivial $N=1$).
2. **$N = 5$:** The smallest odd board with a tour.

---

## Complexity Analysis

- **Verification (LeetCode 2596):** Time $O(N^2)$, Auxiliary Space $O(N^2)$.
- **Generation (Backtracking):** Time $O(8^{N^2})$, Auxiliary Space $O(N^2)$ board + $O(N^2)$ stack frames.

---

## Key Takeaways

1. **8 Moves:** Defined by $(\pm 1, \pm 2)$ and $(\pm 2, \pm 1)$.
2. **Warnsdorff's Rule:** Move to square with minimum onward degree.
3. **L-Move Invariant:** `(dr == 1 && dc == 2) || (dr == 2 && dc == 1)`.

---

## 🎯 Pattern Recognition — When to Use This
- **Trigger Cues:** "Visit every cell on a board exactly once", "Find a path covering all nodes", "Knight's shortest path".
- **Why Backtracking?** Finding a Hamiltonian Path (visiting every cell exactly once) on a grid is an NP-Complete problem. Unless we are just finding the *shortest* path between two points (which uses BFS), covering the *entire* board requires exhaustive search via Backtracking, heavily optimized by heuristics like Warnsdorff's.

## 🏆 Related Problems (Leetcode)
- **Leetcode 2596. Check Knight Tour Configuration:** Verify if a given 2D grid represents a valid knight's tour.
- **Leetcode 1197. Minimum Knight Moves:** Find the shortest path for a knight to reach a target (Uses BFS, not Backtracking!).
- **Leetcode 980. Unique Paths III:** A similar Hamiltonian Path problem where you must walk over every non-obstacle square exactly once.

## 🔗 Cross-Topic Connections
- **Graphs:** The Knight's Tour is fundamentally a search for a Hamiltonian Path in an undirected graph where $V = 64$ and edges are legal L-moves.
- **BFS (Breadth-First Search):** While Backtracking finds a full tour, BFS is the correct approach for finding the *shortest distance* a knight needs to travel between two squares.

### 🔥 Additional Interview Q&A
#### Q2: How does Warnsdorff's Heuristic work and why is it effective?
- **Answer:** Warnsdorff's heuristic dictates that the knight should always move to the adjacent unvisited square that has the *fewest* onward legal moves. This works because it forces the knight to visit the "hard-to-reach" edge and corner squares early. If it left them for later, they would become isolated and unreachable, causing the entire search branch to fail.

#### Q3: What is the Time and Space Complexity of generating a Knight's Tour with Backtracking?
- **Answer:** Without heuristics, the time complexity is $O(8^{N^2})$ in the worst case, as there are at most 8 branches at each of the $N^2$ steps. Space complexity is $O(N^2)$ for the recursion stack and the grid. With Warnsdorff's heuristic, the time complexity is drastically reduced, often finding a solution in near-linear time $O(N^2)$, though it is technically not guaranteed for all board sizes.

#### Q4: Why is BFS not used for finding the full Knight's Tour?
- **Answer:** BFS is used to find the shortest path to a single target. If we used BFS to find a path covering all 64 squares, we would need to store every partial path state in the queue. This would cause a massive combinatorial explosion in memory, quickly leading to an Out-Of-Memory (OOM) error. Backtracking (DFS) uses minimal memory ($O(N^2)$) by exploring one path deeply before trying the next.

#### Q5: Is it possible to have a Knight's Tour on a $3 \times 3$ board?
- **Answer:** No. A knight on the center square cannot move anywhere, and a knight on any outer square can never reach the center square. Thus, no Hamiltonian Path can exist.

## ⚡ 2-Minute Revision Flash Card

- Base Case: `step == n * n`.
- 8 moves: `{-2, -2, -1, -1, 1, 1, 2, 2}` and `{-1, 1, -2, 2, -2, 2, -1, 1}`.
- Backtrack: reset `board[r][c] = -1`.
- Heuristic: Warnsdorff's Rule (always move to square with minimum onward options).
